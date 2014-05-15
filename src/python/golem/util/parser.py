# vim: ts=3:sw=3:expandtab

import datetime
import os
import pwd
import os.path
import math
import re
import golem.util.path
from golem.util.config import Properties, version_compare
import golem.util.tools
import golem.util.constants
import golem.algorithms.helicity

_KEYWORDS = ["else", "for", "if", "select", "case", "with", "elif", "macro"]
_ELSE   = 0
_FOR    = 1
_IF     = 2
_SELECT = 3
_CASE   = 4
_WITH   = 5
_ELIF   = 6
_MACRO  = 7

class TemplateError(Exception):
   def __init__(self, *args):
      Exception.__init__(self, *args)

class Template:
   """
   A template is a file in a special markup language.
   It is translated by the following rules:

   * Trailing whitespace is removed from each line.
   * Markup tags are enclosed in [% ... %]
     The following tags are defined:

     [% some_name %]
     is replaced by self.some_name()

     [% @for some_name %] content [% @end @for %]
     content is evaluated for each environment (Properties) yielded
     by self.some_name()

     Two standard iterators are implemented:
        [% @for each value1 value2 ... [var=varname] %]
        [% @for repeat [from] to [step] [var=varname] %]

     [% @if name %] content [% @elif name
     %] ... [% @else %] ... [% @end @if %]
     evaluates each name and interpretes it as Boolean value
     until the first success is reached and branches accordingly.

     [% @select name @case value1 value2 ... %] ...
     [%@case ...%] ...
     [%@else%] ...
     [% @end @select %]

     [% @with name %] content [% @end @with %]
     expects self.name() to return an environment(Properties)
     and pushes them on top of the stack during evaluation of
     the content.

     [% ' comment %]

   * arguments are passed to the corresponding method
     [% command arg1 arg2 name1=narg1 name2=narg2 ... %]
     would be invoked as self.command(*["arg1", "arg2"],
     **{"name1": "narg1", "name2": "narg2", ...})
   """

   def __init__(self, source):
      """
      Creates a new template from a source.

      PARAMETER

         source -- either a string, a file or an iterator of strings

      """
      self._line_number = 0
      self._macros = {}
      try:
         if isinstance(source, str):
            # read template from a literal string
            self._parse(source.splitlines())
         elif "xreadlines" in dir(source):
            # read template from a file
            self._parse(source.xreadlines())
         else:
            self._parse(source)
      except TemplateError as ex:
         raise TemplateError(" in line %d: %s" % (self._line_number, str(ex)))


   def _tokenize(self, source):
      LEFT="[%"
      RIGHT="%]"

      in_bracket = False
      buffer = ""
      is_first_line=True
      for raw_line in source:
         self._line_number += 1
         line = raw_line.rstrip()

         if is_first_line:
            if line.startswith("%="):
               cmd = line[0:3]
               line = line[3:]
               LEFT = "[" + cmd[2]
               RIGHT = cmd[2] + "]"

         else:
            is_first_line = False

         if (len(line) == 0) and not in_bracket:
            buffer += "\n"
         while len(line) > 0:
            if in_bracket:
               line = line.lstrip()

               if line[0] == "=":
                  yield "="
                  line = line[1:]
               elif line[0] == "_":
                  raise TemplateError("#%d: Names must not start with a '_'"
                        % self._line_number)
               elif line.startswith(RIGHT):
                  yield "%]"
                  line = line[2:]
                  if len(line) == 0:
                     buffer += "\n"
                  in_bracket = False
               else:
                  right_br = line.find(RIGHT)
                  if right_br >= 0:
                     space   = line.find(" ",  0, right_br)
                     tab     = line.find("\t", 0, right_br)
                     equals  = line.find("=",  0, right_br)
                     left_br = line.find(LEFT, 0, right_br)
                  else:
                     space   = line.find(" ")
                     tab     = line.find("\t")
                     equals  = line.find("=")
                     left_br = line.find(LEFT)
                  if left_br >= 0:
                     raise TemplateError(
                           "#%d: '%s' cannot be nested." % (self._line_number, LEFT))
                  if tab >= 0:
                     if space < 0 or tab < space:
                        space = tab
                  if equals >= 0:
                     if space < 0 or equals < space:
                        space = equals
                  if space >= 0:
                     yield line[0:space]
                     line = line[space:]
                  else:
                     if right_br >= 0:
                        if right_br > 0:
                           yield line[0:right_br]
                        line = line[right_br:]
                     else:
                        yield line
                        line = ""
            # if in_bracket
            else:
               right_br = line.find(RIGHT)
               left_br  = line.find(LEFT)
               if left_br < 0:
                  if right_br >= 0:
                     raise TemplateError(
                           "#%d: Unexpected %s" % (self._line_number, RIGHT))
                  else:
                     buffer += line
                     buffer += "\n"
                     line = ""
               else:
                  buffer += line[0:left_br]
                  if len(buffer) > 0:
                     yield buffer
                  buffer = ""
                  yield "[%"
                  line = line[left_br+2:]
                  in_bracket = True
         # while len(line) > 0
      # for raw_line in source
      if len(buffer) > 0:
         yield buffer

   def _pre_parse(self, source):
      """
      Combines the contents of a [% %] - markup
      """
      in_bracket = False
      buffer = []
      for token in self._tokenize(source):
         if in_bracket:
            if token != "%]":
               buffer.append(token)
            else:
               if len(buffer) == 0:
                  continue
               if buffer[0].lower() == "@select":
                  try:
                     c = buffer.index("@case")
                  except ValueError:
                     c = -1
                  if c < 0:
                     raise TemplateError(
                        "#%d: First @case must follow @select in same bracket"
                        % self._line_number)
                  yield self._collect_bracket(buffer[0:c])
                  yield self._collect_bracket(buffer[c:])
               else:
                  if len(buffer) > 0:
                     yield self._collect_bracket(buffer)
               buffer = []
               in_bracket = False
         elif token == "[%":
            in_bracket = True
         else:
            assert token != "%]"
            yield token

   def _collect_bracket(self, buffer):
      cmd = buffer[0]
      args = buffer[1:]
      opts = {}
      is_end = False

      if cmd.startswith("'"):
         return ""

      if cmd.startswith("@"):
         keyword = cmd[1:].lower()
         if keyword == "end":
            is_end = True
            if len(args) == 0:
               raise TemplateError(
                  "#%d: keyword expected after @end" % self._line_number)
            cmd = args[0]
            args = args[1:]
            if cmd.startswith("@"):
               keyword = cmd[1:].lower()
            else:
               raise TemplateError(
                  "#%d: keyword expected after @end" % self._line_number)
         try:
            cmd = _KEYWORDS.index(keyword)
            if is_end:
               if cmd not in [_FOR, _IF, _WITH, _SELECT, _MACRO]:
                  raise TemplateError(
                     "#%d: %s is not allowed here." % (self._line_number, cmd))

               cmd = - cmd
         except ValueError:
               raise TemplateError(
                  "#%d: %s is not a valid keyword" % (self._line_number, cmd))
      try:
         eq = args.index("=")
      except ValueError:
         eq = -1
      while eq >= 0:
         if eq == 0:
            raise TemplateError(
               "#%d: name missing in option; expected 'name=value'"
               % self._line_number)
         elif eq == len(args) - 1:
            raise TemplateError(
               "#%d: value missing in option; expected 'name=value'"
               % self._line_number)
         assert (eq > 0) and (eq < len(args) - 1)
         name = args[eq - 1]
         value = unescape_value(args[eq + 1])

         opts[name] = value
         del args[eq - 1 : eq + 2]
         try:
            eq = args.index("=")
         except ValueError:
            eq = -1
      return (cmd, args, opts)

   def _parse(self, source):
      """
      Parse source into a tree.

      RETURN

      A nested list representing a tree. The first element of a list
      is a tuple ("name", [args], {opt}) or (int, [args], {opt})
      that determines the meaning of the remaining parts of the list.
      """
      stack = [ [] ]
      for token in self._pre_parse(source):
         if isinstance(token, str):
            stack[-1].append(token)
         else:
            cmd, args, opts = token
            if isinstance(cmd, int):
               if cmd < 0:
                  if (len(stack[-1]) == 0) or isinstance(stack[-1][0], str):
                     raise TemplateError(
                        "#%d: Nothing to end here." % self._line_number)

                  old_cmd, old_args, old_opts = stack[-1][0]
                  if not isinstance(old_cmd, int):
                     raise TemplateError("#%d: Nothing to end here."
                        % self._line_number)

                  if old_cmd != - cmd:
                     raise TemplateError(
                        "#%d: @end @%s expected but @end @%s found."
                        % (self._line_number, _KEYWORDS[old_cmd], _KEYWORDS[-cmd]))
                  assert old_cmd == - cmd
                  assert len(stack) > 1
                  block = stack.pop()
                  stack[-1].append(block)
               elif cmd in [_FOR, _IF, _WITH, _SELECT, _MACRO]:
                  stack.append([token])
               else:
                  stack[-1].append(token)
            else:
               stack[-1].append(token)

      if len(stack) != 1:
         assert len(stack) > 1
         old_cmd, old_args, old_opts = stack[-1][0]
         raise TemplateError("#%d: File ended inside @%s."
               % (self._line_number, _KEYWORDS[old_cmd]))

      self._root = stack[-1]


   def __call__(self, *conf):
      """
      Yields chunks of the preprocessed file as strings.
      """
      self._stack = []
      self._stack.extend(conf)

      for chunk in self._evaluate(self._root):
         yield chunk

   def _evaluate_command(self, cmd, args, opts):
      return getattr(self, cmd)(*args, **opts)

   def _evaluate_atom(self, atom):
      if isinstance(atom, list):
         for chunk in self._evaluate(atom):
            yield chunk
      else:
         yield self._evaluate_leaf(atom)

   def _evaluate_leaf(self, leaf):
      if isinstance(leaf, str):
         return leaf
      elif isinstance(leaf, tuple):
         cmd, args, opts = leaf
         return self._evaluate_command(cmd, args, opts)
      else:
         raise TemplateError("Unexpected data type at leaf: %r" % leaf)

   def _evaluate_for(self, args, opts, body):
      if len(args) == 0:
         raise TemplateError("@for needs at least one argument.")
      for props in self._evaluate_command(args[0], args[1:], opts):
         self._stack.append(props)
         for chunk in self._evaluate(body):
            yield chunk
         self._stack.pop()

   def version_newer(self, *args, **opts):
      s1 = self._eval_string(args[0])
      s2 = self._eval_string(args[1])
      op1 = list(map(int, s1.split(".")))
      op2 = list(map(int, s2.split(".")))
      return version_compare(op1, op2) > 0

   def iterator_empty(self, *args, **opts):
      for props in self._evaluate_command(args[0], args[1:], opts):
         return False
      return True

   def count(self, *args, **opts):
      c = 0
      for props in self._evaluate_command(args[0], args[1:], opts):
         c += 1

      return str(c)

   def sum(self, *args, **opts):
      var = args[0]
      lst = [int(props.getProperty(var, 0))
         for props in self._evaluate_command(args[1], args[2:], opts)]

      return str(sum(lst))

   def max(self, *args, **opts):
      var = args[0]
      lst = [int(props.getProperty(var, 0))
         for props in self._evaluate_command(args[1], args[2:], opts)]

      return str(max(lst))

   def min(self, *args, **opts):
      var = args[0]
      lst = [int(props.getProperty(var, 0))
         for props in self._evaluate_command(args[1], args[2:], opts)]

      return str(min(lst))

   def _evaluate_if(self, args, opts, body):
      true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
      if len(args) == 0:
         raise TemplateError("@if needs at least one argument.")

      flag = str(self._evaluate_command(args[0], args[1:], opts))
      flag = flag.strip().lower() in true_values

      sequence = body
      while not flag:
         if len(sequence) == 0:
            flag = True
         else:
            if self._is_command(sequence[0]):
               cmd, args, opts = sequence[0]
               if cmd == _ELIF:
                  if len(args) == 0:
                     raise TemplateError("@elif needs at least one argument.")
                  flag = str(self._evaluate_command(args[0], args[1:], opts)) \
                        .strip().lower() in true_values
               elif cmd == _ELSE:
                  flag = True
               else:
                  raise TemplateError(
                        "@%s unexpected in @if block." %   _KEYWORDS[cmd])
            sequence = sequence[1:]

      while flag:
         if len(sequence) == 0:
            flag = False
         else:
            if self._is_command(sequence[0]):
               cmd, args, opts = sequence[0]
               if cmd == _ELIF:
                  if len(args) == 0:
                     raise TemplateError(
                           "@elif needs at least one argument.")
                  flag = False
               elif cmd == _ELSE:
                  flag = False
               else:
                  raise TemplateError(
                        "@%s unexpected in @if block." % _KEYWORDS[cmd])
            else:
               if isinstance(sequence[0], str):
                  yield sequence[0]
               else:
                  for chunk in self._evaluate_atom(sequence[0]):
                     yield chunk
            sequence = sequence[1:]

   def _evaluate_select(self, args, opts, body):
      if len(args) == 0:
         raise TemplateError("@select needs at least one argument.")

      lhs = self._evaluate_command(args[0], args[1:], opts)
      sequence = body
      flag = False
      while not flag:
         if len(sequence) == 0:
            flag = True
         else:
            if self._is_command(sequence[0]):
               cmd, args, opts = sequence[0]
               if cmd == _CASE:
                  if "convert" in opts:
                     if opts["convert"] == "lower":
                        cmp = lhs.lower()
                     elif opts["convert"] == "upper":
                        cmp = lhs.upper()
                     else:
                        cmp = lhs
                  else:
                     cmp = lhs
                  if "evaluate" in opts:
                     eval_flag = opts["evaluate"].lower() in [
                        "1", "true", ".true.", "t", ".t.", "yes", "y"]
                     if eval_flag:
                        rhs = self._evaluate_command(args[0], args[1:], opts)
                        flag = (cmp == rhs)
                     else:
                        flag = cmp in args
                  else:
                     flag = cmp in args

               elif cmd == _ELSE:
                  flag = True
               else:
                  raise TemplateError(
                        "@%s unexpected in @select block." % _KEYWORDS[cmd])
            sequence = sequence[1:]

      while flag:
         if len(sequence) == 0:
            flag = False
         else:
            if self._is_command(sequence[0]):
               cmd, args, opts = sequence[0]
               if cmd == _CASE:
                  flag = False
               elif cmd == _ELSE:
                  flag = False
               else:
                  raise TemplateError(
                        "@%s unexpecte in @select block." % _KEYWORDS[cmd])
            else:
               for chunk in self._evaluate_atom(sequence[0]):
                  yield chunk
            sequence = sequence[1:]

   def _evaluate_macro(self, args, opts, body):
      name = args[0]
      params = args[1:]
      if name in self._macros:
         raise TemplateError("Macro %s already defined." % name)
      self._macros[name] = (params, opts, body)
      yield ""

   def _evaluate_with(self, args, opts, body):
      if len(args) == 0:
         raise TemplateError("@for needs at least one argument.")

      props = self._evaluate_command(args[0], args[1:], opts)
      self._stack.append(props)
      for chunk in self._evaluate(body):
         yield chunk
      self._stack.pop()

   def _is_command(self, token):
      if isinstance(token, tuple):
         cmd, args, opts = token
         return isinstance(cmd, int)
      else:
         return False

      
   def _evaluate(self, tree):
      assert isinstance(tree, list), "Argument was a %s" % tree.__class__

      if len(tree) > 0:
         if self._is_command(tree[0]):
            iter = None
            cmd, args, opts = tree[0]
            if cmd == _FOR:
               iter = self._evaluate_for(args, opts, tree[1:])
            elif cmd == _IF:
               iter = self._evaluate_if(args, opts, tree[1:])
            elif cmd == _SELECT:
               iter = self._evaluate_select(args, opts, tree[1:])
            elif cmd == _WITH:
               iter = self._evaluate_with(args, opts, tree[1:])
            elif cmd == _MACRO:
               iter = self._evaluate_macro(args, opts, tree[1:])
            else:
               raise TemplateError("Unexpected block: @%s." % _KEYWORDS[cmd])
         
            for chunk in iter:
               if isinstance(chunk, list):
                  for sub_chunk in self._evaluate_atom(chunk):
                     yield sub_chunk
               else:
                  yield self._evaluate_leaf(chunk)
         else:
            # Not a proper block, just a sequence:
            for chunk in tree:
               for sub_chunk in self._evaluate_atom(chunk):
                  yield sub_chunk
      else:
         yield ""

   def _format_value(self, value, *args, **opts):
      if "substr" in opts:
         coords = opts["substr"]
         line=coords.split(":")
         if len(line) == 1:
            value = value[self._eval_int(line[0]):]
         elif len(line) == 2:
            value = value[self._eval_int(line[0]):self._eval_int(line[1])]

      if "convert" in opts:
         if opts["convert"] == "lower":
            value = value.lower()
         elif opts["convert"] == "upper":
            value = value.upper()
         elif opts["convert"] == "bool":
            true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
            if value.strip().lower() in true_values:
               if "true" in opts:
                  value = opts["true"]
               else:
                  value = "true"
            else:
               if "false" in opts:
                  value = opts["false"]
               else:
                  value = "false"
         elif opts["convert"] == "number":
            value = str(value).lower()
            if value.startswith("0x"):
               value = int(value[2:], 16)
            elif value.startswith("$"):
               value = int(value[1:], 16)
            else:
               if "radix" in opts:
                  radix = int(opts["radix"])
               else:
                  radix = 10

               try:
                  value = int(value, radix)
               except ValueError:
                  try:
                    value = float(value)
                  except:
                    value=0
         elif opts["convert"] == "float":
            value = float(value)
            # use "%g" instead of "%f" for very small values to avoid truncation to zero
            if "format" in opts:
               for m in re.finditer('%([-#0+hl ]*[0-9]*)(\.[0-9]*)?(f)',opts["format"],re.I):
                  if m and m.group(3)=="f" or m.group(3)=="F":
                     try:
                        if m.group(2) and len(m.group(2))>1:
                           p_d = int(m.group(2)[1:])
                        else:
                           p_d=6
                        if -math.log10(abs(value)) > p_d:
                           if m.group(3)=="f":
                              opts["format"]=re.sub("%.*f", "%" + m.group(1) + m.group(2) +"g",opts["format"])
                           else:
                              opts["format"]=re.sub("%.*F", "%" + m.group(1) + m.group(2) +"G",opts["format"])
                     except ValueError:
                        pass
      if "match" in opts:
         bfl = 0
         if "flags" in opts:
            flags = opts[flags].strip().upper()
            for ch in flags:
               if ch == 'I':
                  bfl = bfl | re.I
               elif ch == 'L':
                  bfl = bfl | re.L
               elif ch == 'M':
                  bfl = bfl | re.M
               elif ch == 'S':
                  bfl = bfl | re.S
               elif ch == 'U':
                  bfl = bfl | re.U
               elif ch == 'X':
                  bfl = bfl | re.X

         pat = re.compile(opts["match"], bfl)
         mat = re.match(pat, value)
         if mat:
            args = {}
            i = 0
            for g in list(mat.groups()):
               args[str(i)] = g
               i += 1
         else:
            args = None
      else:
         args = value

      if "format" in opts:
         if args is None:
            raise TemplateError("No match: match=%r" % opts["match"])

         try:
            value = opts["format"] % args
         except TypeError as ex:
            if "match" in opts:
               mtch = opts["match"]
            else:
               mtch = ""

            raise TemplateError(str(ex) + 
                  "; format=%r match=%r value=%r" % 
                  (opts["format"], mtch, value))
      elif "digits" in opts:
         v = abs(value)
         d = opts["digits"]
         r = len(d)
         if r <= 1:
            value = str(value)
         else:
            s = ""

            while v > 0:
               s = d[v % r] + s
               v = v // r

            if value < 0:
               s = "-" + s

            if len(s) == 0:
               s = d[0]

            value = s
      else:
         value = str(value)

      # Adds characters if the value is non-empty:
      #   if x='abc' => [% x asprefix=_ %]y = abc_y
      #   if x='' => [% x asprefix=_ %]y = y
      if "asprefix" in opts:
         if len(value.strip()) > 0:
            value = value.strip() + opts["asprefix"]
      if "assuffix" in opts:
         if len(value.strip()) > 0:
            value = opts["assuffix"] + value.strip()
      if "asstringlength" in opts:
         if len(value.strip()) > 0:
            value = opts["asstringlength"] + str(len(value.strip()))
      return value

   def debug_options(self, *args, **opts):
      for i in range(1, len(self._stack) + 1):
         conf = self._stack[-i]
         for name in conf:
            value = conf[name]

            props = Properties()
            props["name"] = name
            props["$_"] = value
            yield props

   def _lookup(self, *args, **opts):
      name = self._remembered_name

      if "suffix" in opts:
         self._remembered_name = opts["suffix"]
         suffix = self._lookup()
         name = name + suffix
      if "prefix" in opts:
         self._remembered_name = opts["prefix"]
         prefix = self._lookup()
         name = prefix + name

      props = None
      for i in range(1, len(self._stack) + 1):
         conf = self._stack[-i]
         if name in conf:
            props = conf
            break

      if props is not None:
         value = props.getProperty(name, "")
         value = self._format_value(value, *args, **opts)
         return value
      elif name in self._macros:
         return self._eval_macro_call(name, args, opts)
      elif "default" in opts:
         return opts["default"]
      else:
         raise TemplateError("UNDEFINED [%% %s %%]" % name)

   def _eval_macro_call(self, name, args, opts):
      m_args, m_opts, m_body = self._macros[name]

      props = Properties()

      for key, value in m_opts.items():
         props[key] = value

      for key, value in opts.items():
         props[key] = value

      if len(m_args) == len(args):
         for key, value in zip(m_args, args):
            props[key] = value
      else:
         raise TemplateError(
            "Number of arguments does not match in macro call to %s." % name)

      self._stack.append(props)

      result = [chunk for chunk in self._evaluate(m_body)]

      self._stack.pop()

      return "".join(result)

   def _setup_name(self, opt_name, default_name, opts):
      if opt_name in opts:
         return opts[opt_name]
      else:
         if default_name is None:
            return opt_name
         else:
            return default_name

   def _setup_filter(self, kw_list, args):
      """
      Scan for a list of keywords with the following semantics:

      If none of the arguments are given, all keywords are
      returned.

      If one or more of the keywords are present, only those
      are returned.

      PARAMETER
      kw_list -- the list of keywords to be scanned for.
      args   -- the keywords in the template file.

      RETURN
      a list of keywords according to the above semantics.
      """
      result = []
      for kw in kw_list:
         if kw in args:
               result.append(kw)
      if len(result) == 0:
            result = kw_list
      return result

   def __getattr__(self, name):
      self._remembered_name = name
      return self._lookup

   def banner(self, *args, **opts):

      if "width" in opts:
         WIDTH = int(opts["width"])
      else:
         WIDTH = 72

      if "prefix" in opts:
         PREFIX = opts["prefix"]
      else:
         PREFIX = ""

      if "suffix" in opts:
         SUFFIX = opts["suffix"]
      else:
         SUFFIX = ""

      props = Properties()

      for line in golem.util.tools.banner(
         WIDTH=WIDTH, PREFIX=PREFIX, SUFFIX=SUFFIX):
         props["$_"] = line
         yield props

   def include(self, *args, **opts):
      if len(args) != 1:
         raise TemplateError("[% include ... %] takes exactly one argument.")
      try:
         path = self.templates()
         template_file = open(os.path.join(path, args[0]), 'r')
         template = self.__class__(template_file)
         result = "".join(s for s in template(*self._stack))
         template_file.close()
      except TemplateError as ex:
         raise TemplateError("In included file '%s': %s" % (args[0], ex))

      return result

   def modules(self, *args, **opts):
      if len(args) != 1:
         raise TemplateError("[% modules ... %] takes exactly one argument.")
      else:
         props = Properties()
         if "path" in opts:
            p = os.path.expandvars(opts["path"]).strip().lower()

            if p == "process":
               path = self.process_path()
            elif p == "templates":
               path = self.templates()
            elif p == "golem":
               path = self.golem_path()
            else:
               path = None

            fname = os.path.join(path, args[0])
            fname = os.path.expandvars(fname)
         else:
            fname = args[0]
            fname = os.path.expandvars(fname)

         if "replace" in opts:
            rep = opts["replace"]
            if "by" not in opts:
               raise TemplateError(
                     ("[% modules replace=%r ... %]: " % rep) +
                     "option 'by' expected.")
            new_opts = opts.copy()
            for unexpected in ["path", "replace", "by"]:
               if unexpected in new_opts:
                  del new_opts[unexpected]
            by = self._evaluate_command(opts["by"], [], new_opts)

            fname = fname.replace(rep, by)

         
         substs = {}
         max = 0
         for name, value in opts.items():
            if name.startswith("$"):
               idx = int(name[1:])
               if idx > max:
                  max = idx
               substs[idx] = str(self._eval_string(value))

         result = []
         if max > 0:
            for i in range(1, max+1):
               if i in substs:
                  result.append(substs[i])
               else:
                  result.append("")
            fname = fname % tuple(result)
         
         try:
            if path is None:
               file = open(fname, 'r')
            else:
               file = open(os.path.join(path, fname), 'r')
         except IOError as ex:
            raise TemplateError("In [%% modules %%]: %s" % str(ex))
         current_chunk = None
         chunk_data = []
         separator = ""
         lsep = 0
         for line in file:
            if (lsep > 0) and line.startswith(separator):
               chopped = line[lsep:].strip()
               if current_chunk is not None:
                  props.setProperty(current_chunk, "".join(chunk_data))
                  chunk_data = []
               if chopped == "--":
                  file.close()
                  return props
               else:
                  options = chopped.split()
                  for sopt in options:
                     name, value = sopt.split("=", 2)
                     name = name.strip()
                     value = value.strip()
                     if name == "name":
                        current_chunk = value
                     else:
                        # ignore unknown options
                        pass
            else:
               if current_chunk is None:
                  chopped = line.strip()
                  if chopped.startswith("boundary"):
                     name, value = chopped.split("=", 2)
                     separator = "--" + value.strip()
                     lsep = len(separator)
                  else:
                     # Blank lines and random garbage are ignored.
                     pass
               else:
                  chunk_data.append(line)
         file.close()
         if current_chunk is not None:
            golem.util.tools.\
            warning("In file %r: %r generated." % (args[0], separator + "--"))
            props.setProperty(current_chunk, "".join(chunk_data))
      return props


   def env(self, *args, **opts):
      props = Properties()
      for key, value in opts.items():
         props.setProperty(key, value)

      return props

   def tab(self, *args, **opts):
      if "rep" in opts:
         factor = int(opts["rep"])
      else:
         factor = 1
      return "\t" * factor

   def indexof(self, *args, **opts):
      if "delimiter" in opts:
         delimiter = opts["delimiter"]
      else:
         delimiter = ","

      if "shift" in opts:
         shift = int(opts["shift"])
      else:
         shift = 0

      element = self._eval_string(args[0])
      lst = self._eval_string(args[1]).split(delimiter)
      if element in lst:
         idx = lst.indexof(element) + shift
      else:
         idx = -1

      return idx

   def subscript(self, *args, **opts):
      if "delimiter" in opts:
         delimiter = opts["delimiter"]
      else:
         delimiter = ","

      if "shift" in opts:
         shift = int(opts["shift"])
      else:
         shift = 0

      lst = self._eval_string(args[0]).split(delimiter)
      idx = self._eval_int(args[1]-shift)

      return lst[idx]

   def elements(self, *args, **opts):
      props = Properties()
      nopts = opts.copy()
      if "var" in opts:
         varname = opts["var"]
         del nopts["var"]
      else:
         varname = "$_"

      if "index" in opts:
         index_name = opts["index"]
         del nopts["index"]
      else:
         index_name = "index"

      if "first" in opts:
         first_name = opts["first"]
         del nopts["first"]
      else:
         first_name = "is_first"

      if "last" in opts:
         last_name = opts["last"]
         del nopts["last"]
      else:
         last_name = "is_last"

      if "delimiter" in opts:
         delimiter = opts["delimiter"]
         del nopts["delimiter"]
         if delimiter == "":
            delimiter = " "
      else:
         delimiter = ","

      if "shift" in opts:
         shift = int(opts["shift"])
         del nopts["shift"]
      else:
         shift = 0

      slst = self._eval_string(args[0], **nopts).strip()
      if slst:
         lst = slst.split(delimiter)

         i = 0
         n = len(lst)
         for arg in lst:
            props.setProperty(varname, arg)
            props.setProperty(index_name, i + shift)
            props.setProperty(first_name, i == 0)
            props.setProperty(last_name, i + 1 >= n)
            yield props
            i += 1

   def each(self, *args, **opts):
      props = Properties()
      if "var" in opts:
         varname = opts["var"]
      else:
         varname = "$_"

      if "first" in opts:
         first_name = opts["first"]
      else:
         first_name = "is_first"

      if "last" in opts:
         last_name = opts["last"]
      else:
         last_name = "is_last"

      i = 0
      n = len(args)
      for arg in args:
         props.setProperty(varname, arg)
         props.setProperty(first_name, i == 0)
         props.setProperty(last_name, i + 1 >= n)
         yield props
         i += 1

   def _eval_bool(self, string):
      true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
      false_values = ["0", "false", ".false.", "f", ".f.", "no", "n"]

      s = self._eval_string(str(string)).lower().strip()
      if s in true_values:
         return True
      elif s in false_values:
         return False
      else:
         raise TemplateError("Cannot evaluate %r as boolean." % s)

   def _eval_int(self, string):
      try:
         result = int(string)
      except ValueError:
            result = self._evaluate_command(string, [], {"convert": "number"})
            result = int(result)
      return result

   def _eval_string(self, string, **opts):
      try:
         result = self._evaluate_command(string, [], opts)
      except TemplateError:
         result = string
      return result

   def _fill_buckets(self, apples, buckets):
      assert buckets >= 1
      if buckets == 1:
         yield [apples]
      else:
         for apples0 in range(0, apples + 1):
            for tail in self._fill_buckets(apples - apples0, buckets - 1):
               yield [apples0] + tail

   def _expand_pattern(self, pat_array, max_len):

      n_pat = len(pat_array)
      n_fixed = n_pat
      astast = []
      for i in range(n_pat):
         if pat_array[i] == "**":
            astast.append(i)
            n_fixed -= 1

      n_loose = len(astast)
      assert n_pat == n_fixed + n_loose

      if n_fixed < max_len and n_loose > 0:
         result = set()
         for lengths in self._fill_buckets(max_len - n_fixed, n_loose):
            element = []

            ofs = 0
            for i in range(n_loose):
               i_loose = astast[i]
               for j in range(ofs, i_loose):
                  element.append(pat_array[j])
               ofs = i_loose + 1
               for j in range(lengths[i]):
                  element.append("*")
            for j in range(ofs, n_pat):
               element.append(pat_array[j])
            result.add(".".join(element))

         for element in result:
            yield element.split(".")
      elif max_len == n_fixed:
         yield pat_array

   def _name_matches_pattern(self, name, pattern, extensions,
         ignore_case=False):
      pat_array = pattern.split(".")
      name_array = name.split(".")
      l_name = len(name_array)

      for pat in self._expand_pattern(pat_array, len(name_array)):
         if len(pat) == l_name:
            cmp = True
            for i in range(l_name):
               if pat[i] == "*":
                  continue
               elif pat[i].lower() == "%extension%":
                  if name_array[i].lower() in extensions:
                     continue
                  else:
                     cmp = False
                     break
               elif ignore_case:
                  if pat[i].lower() == name_array[i].lower():
                     continue
                  else:
                     cmp = False
                     break
               else:
                  if pat[i] == name_array[i]:
                     continue
                  else:
                     cmp = False
                     break
            if cmp:
               return True
      return False

   def error(self, *args, **opts):
      raise TemplateError(" ".join(map(str, args)))

   def extension(self, *args, **opts):
      ext = []
      for i in range(1, len(self._stack) + 1):
         conf = self._stack[-i]
         lst = golem.properties.getExtensions(conf)
         if lst is not None:
            ext.extend(map(lambda x: x.lower(), lst))
         if ext and hasattr(conf,"final_extensions"):
               break

      presence = []
      for arg in args:
         if arg.startswith("!"):
            presence.append(arg[1:] not in ext)
         else:
            presence.append(arg in ext)

      if "require" in opts:
         mode = opts["require"].lower()
      else:
         mode = "all"

      if mode == "any" or mode == "some":
         return any(presence)
      elif mode == "all":
         return all(presence)
      elif mode == "no" or mode == "none":
         return not any(presence)
      else:
         golem.util.tools.\
         error("Unknown value for require=%r in [%extension%]" % mode)
            
   def options(self, *args, **opts):
      props = None
      names = []

      if "first" in opts:
         first_name = opts["first"]
      else:
         first_name = "is_first"

      if "last" in opts:
         last_name = opts["last"]
      else:
         last_name = "is_last"

      if "ignorecase" in opts:
         ignorecase = opts["ignorecase"].lower().strip() == "true"
      else:
         ignorecase = False

      if "var" in opts:
         varname = opts["var"]
      else:
         varname = "$_"

      if "name" in opts:
         namename = opts["name"]
      else:
         namename = "name"

      ext = []
      for i in range(1, len(self._stack) + 1):
         conf = self._stack[-i]
         lst = golem.properties.getExtensions(conf)
         if lst is not None:
            ext.extend(map(lambda x: x.lower(), lst))

      for the_ext in ext:
         for pattern in args:
            for i in range(1, len(self._stack) + 1):
               conf = self._stack[-i]
               for name in conf:
                  if self._name_matches_pattern(name, pattern,
                        [the_ext], ignorecase):
                     if name not in names:
                        names.append(name)

      for opt in ["ignorecase", "var", "name", "first", "last"]:
         if opt in opts:
            del opts[opt]

      count = len(names)
      is_first = True

      for name in names:
         count -= 1
         props = Properties()
         value = self._evaluate_command(name, args, opts)
         props.setProperty(namename, name)
         props.setProperty(varname, value)

         props.setProperty(first_name, str(is_first))
         is_first = False
         props.setProperty(last_name, str(count == 0))
         yield props

   def repeat(self, *args, **opts):
      props = Properties()
      if "var" in opts:
         varname = opts["var"]
      else:
         varname = "$_"

      if "first" in opts:
         first_name = opts["first"]
      else:
         first_name = "is_first"

      if "last" in opts:
         last_name = opts["last"]
      else:
         last_name = "is_last"

      if "shift" in opts:
         shift = self._eval_int(opts["shift"])
      else:
         shift = 0
         
      if "inclusive" in opts:
         true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
         is_inclusive = opts["inclusive"].lower() in true_values
      else:
         is_inclusive = False

      if len(args) == 0:
         raise TemplateError("repeat needs at least one argument.")
      elif len(args) == 1:
         loop_from = 0
         loop_to   = self._eval_int(args[0])
         loop_step = 1
      elif len(args) == 2:
         loop_from = self._eval_int(args[0])
         loop_to   = self._eval_int(args[1])
         loop_step = 1
      elif len(args) == 3:
         loop_from = self._eval_int(args[0])
         loop_to   = self._eval_int(args[1])
         loop_step = self._eval_int(args[2])

      if(is_inclusive):
         loop_to += loop_step

      for i in range(loop_from, loop_to, loop_step):
         props.setProperty(varname, i + shift)
         props.setProperty(first_name, i == loop_from)
         props.setProperty(last_name, i + loop_step >= loop_to)
         yield props

   def eval(self, *args, **opts):
      def sign(x):
         if x > 0:
            return 1
         elif x < 0:
            return -1
         else:
            return 0

      def gcd(a, b):
         while b != 0:
            a, b = b, a % b
         return a

      def lcm(a, b):
         return (a * b) // gcd(a, b)

      def push(arg):
         value = arg
         if value.startswith("'") or value.startswith("\""):
            value = value[1:]
            if value.endswith("'") or value.endswith("\""):
               value = value[:-1]
         elif value not in ["+", "-", ".",
               "0", "1", "2", "3", "4",
               "5", "6", "7", "8", "9"]:
            value = self._evaluate_command(value, [], nopts)
         try:
            value = int(value)
         except ValueError:
            try:
               value = float(value)
            except ValueError:
               pass
         stack.append(value)

      def execute(op, nargs):
         prec = op[0]
         if len(op_stack) > 0:
            other_prec, other_func, other_nargs = op_stack[-1]
         else:
            other_prec = -10000

         while other_prec >= prec:
            op_stack.pop()
            if other_nargs == 1:
               assert len(stack) > 0
               arg1 = stack.pop()
               if isinstance(arg1, list):
                  arg1 = arg1[0]
               res = other_func(arg1)
            else:
               assert other_nargs == 2
               assert len(stack) > 1
               arg2 = stack.pop()
               if isinstance(arg2, list):
                  arg2 = arg2[0]

               arg1 = stack.pop()
               if other_prec % 2 == 1:
                  # This is a comparison operator
                  if isinstance(arg1, list):
                     if arg1[0]:
                        arg1 = arg1[1]
                        res = other_func(arg1, arg2)
                     else:
                        res = [False, arg2]
                  else:
                     res = other_func(arg1, arg2)
               else:
                  if isinstance(arg1, list):
                     arg1 = arg1[0]
                  res = other_func(arg1, arg2)
            stack.append(res)
            if len(op_stack) > 0:
               other_prec, other_func, other_nargs = op_stack[-1]
            else:
               other_prec = -10000
         op_stack.append( (op[0], op[1], nargs) )

      def unwind():
         virtual_op = [-9999, lambda x: x]
         execute(virtual_op, 1)
         assert len(stack) == 1, "Stack: %s, Op-Stack: %s" % \
               (str(stack), str(op_stack))
         assert len(op_stack) == 1, "Stack: %s, Op-Stack: %s" % \
               (str(stack), str(op_stack))
         result = stack.pop()
         op_stack.pop()
         if isinstance(result, list):
            return result[0]
         else:
            return result

      operators = {
            " | ":      [100, lambda x, y: x or y],
            " || ":     [100, lambda x, y: x or y],
            " .or. ":   [100, lambda x, y: 
               self._eval_bool(x) or self._eval_bool(y)],

            " & ":      [150, lambda x, y: x and y],
            " && ":     [150, lambda x, y: x and y],
            " .and. ":  [150, lambda x, y:
               self._eval_bool(x) and self._eval_bool(y)],

            " !":       [200, lambda x: not x],
            " .not.":   [200, lambda x: not self._eval_bool(x)],

            " .eq. ":   [255, lambda x, y: [x == y, y]],
            " < ":      [255, lambda x, y: [x < y, y]],
            " .lt. ":   [255, lambda x, y: [x < y, y]],
            " > ":      [255, lambda x, y: [x > y, y]],
            " .gt. ":   [255, lambda x, y: [x > y, y]],
            " .ge. ":   [255, lambda x, y: [x >= y, y]],
            " .geq. ":  [255, lambda x, y: [x >= y, y]],
            " .le. ":   [255, lambda x, y: [x <= y, y]],
            " .leq. ":  [255, lambda x, y: [x <= y, y]],
            " .ne. ":   [255, lambda x, y: [x != y, y]],
            " .neq. ":  [255, lambda x, y: [x != y, y]],
            " <> ":     [255, lambda x, y: [x != y, y]],
            " ~< ":     [255, lambda x, y: str(x).startswith(str(y))],
            " ~> ":     [255, lambda x, y: str(x).endswith(str(y))],
            " ~ ":      [255, lambda x, y: str(y) in str(x)],
            " + ":      [300, lambda x, y: x + y],
            " . ":      [300, lambda x, y: str(x) + str(y)],
            " - ":      [300, lambda x, y: x - y],
            " .min. ":  [300, max],
            " .max. ":  [300, min],
            " :: ":     [300, lambda x, y: sqrt(x*x + y*y)],

            " * ":      [350, lambda x, y: x * y],
            " / ":      [350, lambda x, y: float(x) / float(y)],
            " // ":     [350, lambda x, y: x // y],
            " % ":      [350, lambda x, y: x % y],
            " .mod. ":  [350, lambda x, y: x % y],

            " -":       [400, lambda x: -x],
            " +":       [400, lambda x: +x],

            " ^ ":      [450, lambda x, y: x ** y],
            " ** ":     [450, lambda x, y: x ** y],
            " .rep. ":  [450, lambda x, y: str(x) * int(y)],

            " +:":      [500, lambda x: x + x],
            " -:":      [500, lambda x: x / 2],

            " .abs.":   [1000, lambda x: max(x, -x)],
            " .even.":  [1000, lambda x: x % 2 == 0],
            " .odd.":   [1000, lambda x: x % 2 != 0],
            " .sign.":  [1000, sign],
            " .lcm. ":  [1000, lcm],
            " *:":      [1000, lambda x: x * x],
            " /":       [1000, lambda x: 1/x],
            " .len.":   [1000, len],
            " .str.":   [1000, str],
            " .sqrt.":  [1000, math.sqrt],
            " .exp.":   [1000, math.exp],
            " .log.":   [1000, math.log],
            " .log. ":  [1000, lambda x, y: math.log(y) / math.log(x)],
            " .floor.": [1000, math.floor],
            " .ceil.":  [1000, math.ceil],
            " .sin.":   [1000, math.sin],
            " .cos.":   [1000, math.cos],
            " .tan.":   [1000, math.tan],
            " .sinh.":  [1000, math.sinh],
            " .cosh.":  [1000, math.cosh],
            " .tanh.":  [1000, math.tanh],
            " .asin.":  [1000, math.asin],
            " .acos.":  [1000, math.acos],
            " .atan.":  [1000, math.atan],
            " .atan. ": [1000, math.atan2],
            " `":       [2000, lambda x: self._eval_string(x)]
         }

      nopts = opts.copy()
      if "result" in opts:
         del nopts['result']

      stack = []
      op_stack = []
      brackets = []
      op_flag = True
      for arg in args:
         if op_flag:
            # we just had an operator, hence it must be
            # a prefix operator (if it is an operator at all)
            if (" %s" % arg) in operators:
               op = operators[" %s" % arg]
               execute(op, 1)
            elif arg == "(":
               brackets.append( (stack[:], op_stack[:]) )
               stack = []
               op_stack = []
               op_flag = True
            elif arg == ")":
               if len(brackets) == 0:
                  raise TemplateError("In eval: unexpected ')' encountered.")
               value = unwind()
               stack, op_stack = brackets.pop()
               stack.append(value)
               op_flag = False
            else:
               push(arg)
               op_flag = False
         else:
            if (" %s " % arg) in operators:
               op = operators[" %s " % arg]
               execute(op, 2)
               op_flag = True
            elif arg == ")":
               if len(brackets) == 0:
                  raise TemplateError("In eval: unexpected ')' encountered.")
               value = unwind()
               stack, op_stack = brackets.pop()
               stack.append(value)
               op_flag = False
            else:
               raise TemplateError(
                     "In eval: operator expected but %r found" % arg)

      if len(brackets) > 0:
         raise TemplateError("In eval: forgotten ')'.")
      else:
         result = str(unwind())
         if "result" in opts:
            name = opts["result"]
            props = golem.util.config.Properties()
            props[name] = result
            return props
         else:
            return result

   def cuts(self, *args, **opts):
      """
      Generates a list of all cuts in the requested format.

      [% @for cuts 3 %][% $_ %],[% @end @for %]

      would give (in some order)

      210,21,20,10,2,1,0,
      """

      nopts = opts.copy()
      for kw in ["first", "last", "cut", "uncut", "shift", "delim",
            "maxcut"]:
         if kw in nopts:
            del nopts[kw]

      N = self._eval_int(args[0], **nopts)

      first_name = self._setup_name("first", "is_first", opts)
      last_name = self._setup_name("last", "is_last", opts)
      cut_name = self._setup_name("cut", "$_", opts)
      uncut_name = self._setup_name("uncut", "uncut", opts)

      if "maxcut" in opts:
         maxcut = int(opts["maxcut"])
      else:
         maxcut = 4

      if "shift" in opts:
         shift = int(opts["shift"])
      else:
         shift = 0

      if "delim" in opts:
         delim = opts["delim"]
      else:
         delim = ""

      sel = [False] * N

      props = Properties()

      while not all(sel):
         cut = []
         uncut = []

         props.setProperty(first_name, not any(sel))
      
         carry = True
         for i in range(len(sel)):
            old_val = sel[i]
            new_val = carry ^ old_val
            carry = carry and old_val
            sel[i] = new_val

            if new_val:
               cut.append(i)
            else:
               uncut.append(i)

         if len(cut) > maxcut:
            continue

         cut.reverse()
         uncut.reverse()

         props.setProperty(last_name, all(sel))

         props.setProperty(cut_name, delim.join(map(str, cut)))
         props.setProperty(uncut_name, delim.join(map(str, uncut)))

         yield props

   def member(self, *args, **opts):
      """
      Checks is the content of a variable is contained in
      the value of another variable, which represents a list.
      If more than two arguments are given, all but the first
      argument are taken literally as the list of values.

         [% @if member diagram select.lo %] ... [% @end @if %]
         [% @if member diagram 1 2 4 6 7 %] ... [% @end @if %]

      
      """
      true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
      if "ignore_case" in opts:
         ignore_case = opts["ignore_case"].lower() in true_values
      else:
         ignore_case = False

      if "numeric" in opts:
         numeric = opts["numeric"].lower() in true_values
      else:
         numeric = False

      if len(args) > 2:
         lst = args[1:]
      else:
         slst = self._eval_string(args[1])
         lst = map(lambda s: s.strip(), slst.split(","))
         if ignore_case:
            lst = map(lambda s: s.lower(), lst)

      if numeric:
         src_lst = lst[:]
         lst = []
         for cur in src_lst:
            if ":" in cur:
               boundaries = cur.split(":")
               if len(boundaries) == 2:
                  a = self._eval_int(boundaries[0])
                  b = self._eval_int(boundaries[1])
                  lst.extend(range(a,b+1))
               elif len(boundaries) == 3:
                  a = self._eval_int(boundaries[0])
                  b = self._eval_int(boundaries[1])
                  c = self._eval_int(boundaries[2])
                  lst.extend(range(a,b+1,c))
               else:
                  raise TemplateError("Too many ':' in [% member %]")
            else:
               lst.append(self._eval_int(cur))

         element = self._eval_int(args[0])
      else:
         element = self._eval_string(args[0]).strip()
         if ignore_case:
            element = element.lower()

      return element in lst

   def anymember(self, *args, **opts):
      """
      Checks if any of the arguments (not interpreted as variable names)
      are members of the content of a variable given as the last argument.

         [% @if anymember nlo all debug %] ... [% @end @if %]
      
      """
      true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
      if "ignore_case" in opts:
         ignore_case = opts["ignore_case"].lower() in true_values
      else:
         ignore_case = False
      lst1 = args[:-1]
      lst2 = self._evaluate_command(args[-1], [], opts)

      if not isinstance(lst2, list):
         lst2 = map(lambda s: s.strip(), str(lst2).split(","))
         
      if ignore_case:
         lst1 = map(lambda s: s.lower(), lst1)
         lst2 = map(lambda s: s.lower(), lst2)

      return any(element in lst2 for element in lst1)


   def empty(self, *args, **opts):
      """
      Checks is the content of a variable represents
      an empty list.
      """

      if len(args) != 1:
         lst = args[:]
      else:
         slst = self._eval_string(args[0])
         lst = map(lambda s: s.strip(), slst.split(","))

      lst = filter(lambda s: len(s) > 0, lst)

      return len(lst) == 0

   def golem_path(self, *args, **opts):
      """
      Returns the installation path. If args is not empty
      each element in args is appended to the path as a subdirectory.
      """
      return golem.util.path.golem_path(*args)

   def time_stamp(self, *args, **opts):
      now = datetime.datetime.now()

      if "space" in opts:
         space_char = opts["space"]
      else:
         space_char = "~"

      if "format" in opts:
         format = opts["format"].replace(space_char, ' ')
         result = now.strftime(format)
      else:
         result = now.isoformat(' ')
      return result

   def user_name(self, *args, **opts):
      # return os.getlogin()
      ## os.getlogin() does not work with all terminals.
      ## according to a bug report (rather the answer to it)
      ## the one below is the preferred method to achieve
      ## the same result in a platform independent manner
      return pwd.getpwuid(os.geteuid())[0]

   def os(self, *args, **opts):
      if "prefix" in opts:
         prefix = opts["prefix"]
      else:
         prefix = ""
      props = Properties()
      for key, value in os.environ.items():
         props.setProperty(prefix + key, value)
      return props

   def nl(self, *args, **opts):
      if "dos" in args:
         nl = "\r\n"
      else:
         nl = "\n"

      if "rep" in opts:
         factor = int(opts["rep"])
      else:
         factor = 1
      return nl * factor

   def internal(self, *args, **opts):
      if len(args) == 0:
         raise TemplateError("[% internal %] requires an argument")
      
      iname = "__%s__" % (args[0].upper())
      if iname in self.__INTERNALS__().split(","):
         value = getattr(self, iname)
         return value(self, *(args[1:]), **opts)
      else:
         raise TemplateError(
               "In [%% internal %s %%]: unknown internal variable" % args[0])

   def tens_rec_info(self, *args, **opts):
      if len(args) == 0:
         raise TemplateError("[%% tens_rec_info %%] requires argument (rank)")

      R = self._eval_int(args[0])

      if "dim" in opts:
         d = int(opts["dim"])
      else:
         d = 4

      if "shift_args" in opts:
         shift_args = int(opts["shift_args"])
      else:
         shift_args = 0

      if "return_as_map" in opts: # internal usage only, may not be used in the template
         coeff_name = "coeff"
         args_name = "args"
         symmetry_name = "symmetry"
         sign_name = "sign"
         k_name = "k"
         i_name = "i"
         kmap_name = "kmap"
         imap_name = "imap"

         props = {}
         tworankhigher = {}

      else: # normal case
         coeff_name = self._setup_name("coeff", "coeff", opts)
         args_name = self._setup_name("args", "args", opts)
         symmetry_name = self._setup_name("symmetry", "symmetry", opts)
         sign_name = self._setup_name("sign", "sign", opts)
         k_name = self._setup_name("k", "k", opts)
         i_name = self._setup_name("i", "i", opts)

         # corresponding entries in rank+2 (used with the derive extension)
         kmap_name = self._setup_name("kmap", "kmap", opts)
         imap_name = self._setup_name("imap", "imap", opts)

         props = Properties()

         # get all k,i from rank+2
         new_opts = dict(opts) # copy
         new_opts["return_as_map"]=True
         tworankhigher = {}
         for x in self.tens_rec_info(str(R+2),*args[1:], **new_opts):
            tworankhigher[ tuple(x["args"]) ] = (x["k"],x["i"])

      props[coeff_name] = 0
      props[args_name] = []
      props[symmetry_name] = 1
      props[k_name] = 0
      props[i_name] = 0
      props[sign_name] = 1
      yield props

      for k in range(1,min(R,d)+1):
         lst, dic = generate_mapping(R, k)
         dim = len(lst)
         lab = 0
         for indices in select(range(d), k):
            lab += 1
            for i in range(dim):
               sign = 1
               args = []
               symm = 1
               for idx, mult in zip(indices, lst[i]):
                  args.extend([idx+shift_args]*mult)
                  symm *= fact(mult)
                  if idx > 0 and (mult % 2 == 1):
                     sign = -sign

               props[coeff_name] = k
               props[args_name] = args
               props[symmetry_name] = symm
               props[k_name] = lab
               props[i_name] = i+1
               props[sign_name] = sign
               if tuple(args) in tworankhigher:
                  props[kmap_name] = tworankhigher[tuple(args)][0]
                  props[imap_name] = tworankhigher[tuple(args)][1]
               yield props

def unescape_value(v):
   backslash = False
   result = ''
   for ch in v:
      if backslash:
         backslash = False
         if ch == '-':
            result += ' '
         elif ch == 'n':
            result += '\n'
         else:
            result += ch
      elif ch == '\\':
         backslash = True
      else:
         result += ch
   return result


def fact(N):
   """
   Compute the factorial of a non-negative integer number.
   """
   if N == 0:
      return 1
   elif N > 0:
      return N * fact(N-1)

def combinat(n, k):
   """
      Calculates the binomial coefficient (n atop k).
   """
   if k < 0 or k > n:
      return 0
   else:
      num = 1
      den = 1
      for i in range(1, k+1):
         num *= n-i+1
         den *= i
      return num/den

def select(items, k):
   """
   Iterator over all selections of k elements from a given list.

   PARAMETER

   items  --  list of elements to choose from (no repetitions)
   k      --  number of elements to select.
   """
   n = len(items)
   # We use the fact that
   # (n choose k) = (1 choose 1)(n-1 choose k-1)+(1 choose 0)(n-1 choose k)
   if k == n:
      yield items[:]
   elif k == 0:
      yield []
   elif 0 < k and k < n:
      head = items[0:1]
      tail = items[1:]
      for result in select(tail, k-1):
         yield head + result

      for result in select(tail, k):
         yield result

def generate_mapping(R, k):
   """
      Generates a mapping from tensor components \hat{C}(a_1, ..., a_k)
      into a one dimensional array.

      PARAMETER

      R  -- rank
      k  -- number of non-zero components of q

      RETURN

      (lst, dic)

      lst -- list of (a_1, ..., a_k)
      dic -- mapping from (a_1, ..., a_k) -> int

      lst[dic[X]] = X if X in dic
   """

   def rec_generator(k, R):
      if k == 0:
         yield []
      elif k <= R:
         for a_1 in range(1, R - (k - 1) + 1):
            if k > 1:
               for tail in rec_generator(k - 1, R - a_1):
                  yield [a_1] + tail
            else:
               yield [a_1]
   
   lst = []
   dic = {}
   i = 0
   for indices in rec_generator(k, R):
      t = tuple(indices)
      lst.append(t)
      dic[t] = i
      i += 1

   assert i == combinat(R, k), \
         "len(%s) != %d, R=%d,k=%d" % (lst,combinat(R, k),R,k)
   return lst, dic
