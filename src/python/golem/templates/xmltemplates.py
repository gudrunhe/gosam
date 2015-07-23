# vim: ts=3:sw=3:expandtab

import xml.parsers.expat
import os.path
import sys
import tempfile

import golem.util.main_misc
import golem.util.config

import golem.templates.filter
import golem.templates.factory

from golem.util.tools import debug, message, warning, error, \
      enumerate_helicities, encode_helicity, \
      enumerate_and_reduce_helicities, enumerate_qgraf_powers

def compare_version(version1, version2):
   """
   Returns
      -1 if version1 is older than version2
       0 if version1 and version2 are the same
       1 if version1 is newer than version2
   """

   l = min(len(version1), len(version2))

   for i in range(l):
      if version1[i] == version2[i]:
         continue
      elif version1[i] > version2[i]:
         return 1
      else:
         return -1

      if len(version1) > l:
         return 1
      elif len(version2) > l:
         return -1
      else:
         return 0

class TemplateXMLError(Exception):
   pass

class _TemplateState:
   def __init__(self, template_dir, output_dir, *props, **opts):
      self.props = list(props)
      self.opts = opts

      self._mode = "normal"

      ext = []
      for conf in props:
         lst = golem.properties.getExtensions(conf)
         if lst is not None:
            ext.extend(map(lambda x: x.lower(), lst))

      self.extensions = ext

      self.stack = [[{}]]
      self.produced_files = []

      self.template_dir = template_dir
      self.output_dir = output_dir

      self.cbuffer = None
      self.factory = golem.templates.factory.TemplateFactory()

      self.created_directories = []

   def setMode(self, mode):
      self._mode = mode

   def _getproperty(self, name):
      result = None
      for conf in self. props:
         if name in conf:
            result=conf.getProperty(name)
      return result

   def shuffle_push(self, lst):
      top = self.stack[-1]
      product = []
      for attrs1 in top:
         for attrs2 in lst:
            tmp = attrs1.copy()
            tmp.update(attrs2)
            #print "tmp " + str(tmp)
            product.append(tmp)
      self.stack.append(product)

   def create_directory(self, dest):
      if os.path.exists(dest):
         if not os.path.isdir(dest):
            error("Cannot create directory %r " % dest +
                  "because it exists and is not a directory.")
      else:
         message("Creating directory %r ..." % dest)
         os.mkdir(dest)
         self.created_directories.append(dest)

   def delete_dir_if_empty(self, dest):
      if not os.path.exists(dest):
         error("Cannot check if directory %r " % dest +
               "is empty because it does not exist.")

      elif not os.path.isdir(dest):
         error("Cannot check if %r " % dest +
               "is empty because it is not a directory.")
      else:
         if not os.listdir(dest):
            os.rmdir(dest)
            message("Removed empty directory %r." % dest)
         else:
            message("Keeping non-empty directory %r." % dest)

   def transform_template_file(self, in_file, out_file, class_name, filter, executable):
      if out_file in self.produced_files:
         warning("File %r has been overwritten while processing %r" % \
               (out_file, in_file))
      else:
         self.produced_files.append(out_file)

      self.factory.process(in_file, out_file, class_name,
            self.props, self.opts, self.opts, filter=filter, executable=executable)

   def start_template(self, attrs):
      for name in ["description", "version",
            "author", "author-email",
            "maintainer", "maintainer-email"]:
         if name in attrs:
            for entry in self.stack[0]:
               entry[name] = attrs[name]

      GOLEM_VERSION = golem.util.main_misc.GOLEM_VERSION

      if "golem-version-min" in attrs:
         golem_version_min = map(int,
               attrs["golem-version-min"].split("."))
         if compare_version(GOLEM_VERSION, golem_version_min) < 0:
            raise TemplateXMLError(
                  "GoSam too old: template requires version %s or above."
                  % attrs["golem-version-min"])

      if "golem-version-max" in attrs:
         golem_version_max = map(int,
               attrs["golem-version-max"].split("."))
         if compare_version(GOLEM_VERSION, golem_version_max) > 0:
            raise TemplateXMLError(
                  "GoSam too recent: template requires version %s or below." \
                  % attrs["golem-version-max"])

      for entry in self.stack[0]:
         entry["template-directory"] = self.template_dir
         entry["output-directory"] = self.output_dir

   def end_template(self):
      # delete empty directories
      for directory in self.created_directories:
         self.delete_dir_if_empty(directory)

   def expand_file(self, env, attrs):
      if "usedby" in attrs:
         usedby = attrs["usedby"]
      else:
         usedby = "main"

      if "user" in self.opts:
         user = self.opts["user"]
      else:
         user = "main"

      if user != usedby:
         return None

      if "src" not in attrs:
         raise TemplateXMLError("<file> without 'src' attribute encountered.")

      src = attrs["src"]
      if "dest" in attrs:
         dest = attrs["dest"]
      else:
         dest = src

      if "arguments" in attrs:
         arguments = attrs["arguments"].split(",")
         values = []
         for key in arguments:
            if key in env:
               values.append(env[key])
            else:
               raise TemplateXMLError(
                  "Undefined name in 'arguments': %r" % key)

         if "%" in dest:
            try:
               dest = dest % tuple(values)
            except TypeError:
               raise TemplateXMLError(
                  "In <file> attribute 'arguments' does not match 'dest'")

         if "%" in src:
            try:
               src = src % tuple(values)
            except TypeError:
               raise TemplateXMLError(
                  "In <file> attribute 'arguments' does not match 'src'")
      
      result = env.copy()

      result["output file name"] = dest
      result["template file name"] = src

      if "class" in attrs:
         result["class name"] = attrs["class"]
      else:
         result["class name"] = "Verbatim"

      result["executable"]= "executable" in attrs

      return result

   def start_file(self, attrs):
      top = self.stack[-1]
      new_top = []
      for env in top:
         exf = self.expand_file(env, attrs)
         if exf is not None:
            new_top.append(exf)

      self.stack.append(new_top)

   def end_file(self):
      envs = self.stack.pop()
      for env in envs:
         if "current output directory" in env:
            out_dir = env["current output directory"]
         else:
            out_dir = self.output_dir

         if "current template directory" in env:
            tpl_dir = env["current template directory"]
         else:
            tpl_dir = self.template_dir

         in_file = os.path.join(tpl_dir, env["template file name"].encode(sys.getfilesystemencoding()))
         out_file = os.path.join(out_dir, env["output file name"].encode(sys.getfilesystemencoding()))
         class_name = env["class name"]
         filter = env.get("filter", None)
         executable = env.get("executable", False)

         extra_props = golem.util.config.Properties()
         for name in env:
            extra_props.setProperty(name, env[name])

         self.props.append(extra_props)

         message("Generating file %s" % env["output file name"])
         self.transform_template_file(in_file, out_file, class_name, filter, executable)
         self.props.pop()

   def expand_directory(self, env, attrs):
      if "usedby" in attrs:
         usedby = attrs["usedby"]
      else:
         usedby = "main"

      if "user" in self.opts:
         user = self.opts["user"]
      else:
         user = "main"

      if user != usedby:
         return None

      if "src" not in attrs:
         raise TemplateXMLError(
               "<directory> without 'src' attribute encountered.")

      src = attrs["src"]
      if "dest" in attrs:
         dest = attrs["dest"]
      else:
         dest = src

      if "arguments" in attrs:
         arguments = attrs["arguments"].split(",")
         values = []
         for key in arguments:
            if key in env:
               values.append(env[key])
            else:
               raise TemplateXMLError(
                  "Undefined name in 'arguments': %r" % key)

         if "%" in dest:
            try:
               dest = dest % tuple(values)
            except TypeError:
               raise TemplateXMLError(
                  "In <directory> attribute 'arguments' does not match 'dest'")

         if "%" in src:
            try:
               src = src % tuple(values)
            except TypeError:
               raise TemplateXMLError(
                  "In <directory> attribute 'arguments' does not match 'src'")
      
      result = env.copy()

      if "current output directory" in env:
         out_dir = env["current output directory"]
      else:
         out_dir = self.output_dir

      if "current template directory" in env:
         tpl_dir = env["current template directory"]
      else:
         tpl_dir = self.template_dir

      result["current output directory"] = os.path.join(out_dir, dest.encode(sys.getfilesystemencoding()))
      result["current template directory"] = os.path.join(tpl_dir, src.encode(sys.getfilesystemencoding()))

      return result

   def start_directory(self, attrs):
      top = self.stack[-1]
      new_top = []
      for env in top:
         tmp = self.expand_directory(env, attrs)
         if tmp is not None:
            new_top.append(tmp)
            self.create_directory(tmp["current output directory"])
      self.stack.append(new_top)

   def end_directory(self):
      self.stack.pop()

   def evaluate_conditions(self, env, attrs):
      """
      Checks for the following attributes:
         <... if-file="exists" />
         <... if-file="generated" />
         <... if-extension="name,name,..." [require="all/some/none"] />
         <... if-option="name" value="value"/>
         <... if-option="name" list="value,value,value..."/>
         <... in-mode="scratch"/>
         <... if-internal="name,name,..." [require="all/some/none"] />
      """

      l = len(attrs)

      if "if-file" in attrs:
         if l != 1:
            raise TemplateXMLError(
                  "No other attributes allowed with 'if-file'")
         value = attrs["if-file"]

         if "current output directory" in env:
            out_dir = env["current output directory"]
         else:
            out_dir = self.output_dir

         out_file = os.path.join(out_dir, env["output file name"].encode(sys.getfilesystemencoding()))

         if value == "exists":
            return os.path.exists(out_file)
         elif value == "generated":
            return out_file in self.produced_files
         else:
            raise TemplateXMLError(
                  "Unknown value %r for attribute 'if-file'." % value +
                  "Must be 'exists' or 'generated'.")

      if "if-extension" in attrs:
         tmpext = attrs["if-extension"].split(",")
         extensions = map(lambda s: s.lower(), tmpext)

         if "required" in attrs:
            required = attrs["required"]
            rlen = 2
         elif len(tmpext) == 1:
            required = "all"
            rlen = 1
         else:
            raise TemlateXMLException(
               "Attribute 'required' is mandantory if more than one " +
               "extension is listed in 'if-extension'.")

         if l != rlen:
            raise TemplateXMLError(
                  "Unknown attributes encountered near 'if-extension'")

         if required == "all":
            for ex in extensions:
               if ex not in self.extensions:
                  return False
            return True
         elif required == "some":
            for ex in extensions:
               if ex in self.extensions:
                  return True
            return False
         elif required == "none":
            for ex in extensions:
               if ex in self.extensions:
                  return False
            return True
         else:
            raise TemplateXMLError(
                  "Unknown value %r for attribute 'required' " % required +
                  "near 'if-extension'. " +
                  "Must be one of: all, some, none.")

      if "if-option" in attrs:
         option_name = attrs["if-option"]
         option_value = self._getproperty(option_name)

         if "value" in attrs:
            values = [attrs["value"]]
         elif "list" in attrs:
            values = attrs["list"].split(",")
         else:
            raise TemplateXMLError(
               "Either 'value' or 'list' required with attribute 'if-option'")

         if len(attrs) != 2:
            raise TemplateXMLError(
               "Unknown attributes encountered near 'if-option'")

         if option_value is None:
            return False
         else:
            true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
            lvalues = map(lambda s: s.lower(), values)

            if "true" in lvalues:
               return option_value.strip().lower() in true_values \
                     or option_value in values
            elif "false" in lvalues:
               return option_value.strip().lower() not in true_values \
                     or option_value in values
            else:
               return option_value in values

      if "if-internal" in attrs:
         tmpinternals = attrs["if-internal"].split(",")
         tmpinternals = [ "__%s__" % (i.upper()) for i in tmpinternals ]

         internals = self._getproperty("__INTERNALS__")

         if "required" in attrs:
            required = attrs["required"]
            rlen = 2
         elif len(tmpinternals) == 1:
            required = "all"
            rlen = 1
         else:
            raise TemlateXMLException(
               "Attribute 'required' is mandantory if more than one " +
               "extension is listed in 'if-extension'.")

         if l != rlen:
            raise TemplateXMLError(
                  "Unknown attributes encountered near 'if-extension'")

         if required == "all":
            for i in tmpinternals:
               if i not in internals or str(self._getproperty(i)).lower() != 'true':
                  return False
            return True
         elif required == "some":
            for ex in extensions:
               if i in internals and str(self._getproperty(i)).lower() == 'true':
                  return True
            return False
         elif required == "none":
            for i in tmpinternals:
               if i in internals and str(self._getproperty(i)).lower() == 'true':
                  return False
            return True
         else:
            raise TemplateXMLError(
                  "Unknown value %r for attribute 'required' " % required +
                  "near 'if-internal'. " +
                  "Must be one of: all, some, none.")

   def start_except(self, attrs):
      envs = self.stack.pop()
      new_envs = []
      flag = True

      if "in-mode" in attrs:
         value = attrs["in-mode"]
         flag = (value == self._mode)
         del attrs["in-mode"]

      for env in envs:
         if (not flag) or (not self.evaluate_conditions(env, attrs)):
            new_envs.append(env)

      self.stack.append(new_envs)

   def end_except(self):
      pass

   def start_only(self, attrs):
      envs = self.stack.pop()
      new_envs = []
      flag = True

      if "in-mode" in attrs:
         value = attrs["in-mode"]
         flag = (value == self._mode)
         del attrs["in-mode"]

      for env in envs:
         if (not flag) or self.evaluate_conditions(env, attrs):
            new_envs.append(env)

      self.stack.append(new_envs)

   def end_only(self):
      pass

   def start_filter(self, attrs):
      envs = self.stack.pop()
      for env in envs:
         if "filter" in env:
            old_filter = env["filter"]
         else:
            old_filter = None

         if "name" in attrs:
            opts = attrs.copy()
            del opts["name"]

            opts = dict([(str(k), v) for k, v in opts.iteritems()])

            new_filter = golem.templates.filter.FilterFactory(
                  attrs["name"], old_filter, **opts)

            env["filter"] = new_filter
         else:
            env["filter"] = old_filter

      self.stack.append(envs)

   def end_filter(self):
      pass

   def start_foreach(self, attrs):
      if "iterator" in attrs:
         if "list" in attrs:
            raise TemplateXMLException(
               "<foreach> cannot have both atributes, 'iterator' and 'list'")

         itername = attrs["iterator"]
         if itername == "helicity":
            values = []
            mappings = [m for m in 
                  enumerate_and_reduce_helicities(self.opts["conf"])]

            if "conf" in self.opts:
               for i, heli in enumerate(
                     enumerate_helicities(self.opts["conf"])):
                  gi, mapping, color_basis = mappings[i]
                  if i == gi:
                     values.append({"helicity": i,
                        "helicitysymbol": encode_helicity(heli)})
            self.shuffle_push(values)
         elif itername == "crossings":
            values = []
            if "conf" in self.opts:
               conf = self.opts["conf"]
               crossings = conf.getProperty(golem.properties.crossings)
               for i, crossing in enumerate(crossings):
                  if ":" in crossing:
                     pos = crossing.index(":")
                     name = crossing[:pos].strip()
                     process = crossing[pos+1:]
                     if ">" in process:
                        ini, fin = map(lambda x: map(lambda y: y.strip(),
                           x.split()), process.split(">", 1))
                        values.append({"index": i, "name": name,
                           "initial": ini, "final": fin})
            self.shuffle_push(values)
         elif itername == "loops":
            values = []
            if "conf" in self.opts:
               for loop, power in enumerate_qgraf_powers(self.opts["conf"]):
                  values.append({"loop": loop, "power": power})
            self.shuffle_push(values)
         else:
            raise TemplateXMLError(
               "Unknown iterator at <foreach iterator=%r>" % itername)
      elif "list" in attrs:
         if "iterator" in attrs:
            raise TemplateXMLException(
               "<foreach> cannot have both attributes, 'iterator' and 'list'")

         lst = attrs["list"].split(",")
         if "name" in attrs:
            name = attrs["name"]
         else:
            name = "list"
            
         values = []
         for value in lst:
            values.append({name: value})

         self.shuffle_push(values)
      else:
         raise TemplateXMLException(
            "<foreach> must have one of the attributes 'iterator' or 'list'")

   def end_foreach(self):
      self.stack.pop()

   def character_data(self, cdata):
      if self.cbuffer is not None:
         self.cbuffer += cdata


def create_parser(template_dir, output_dir, *props, **opts):
   xmld = _TemplateState(template_dir, output_dir, *props, **opts)

   if "from_scratch" in opts:
      if opts["from_scratch"]:
         xmld.setMode("scratch")

   def evt_start_element(name, attrs):
      if name == "template":
         xmld.start_template(attrs)
      elif name == "file":
         xmld.start_file(attrs)
      elif name == "directory":
         xmld.start_directory(attrs)
      elif name == "except":
         xmld.start_except(attrs)
      elif name == "only":
         xmld.start_only(attrs)
      elif name == "filter":
         xmld.start_filter(attrs)
      elif name == "foreach":
         xmld.start_foreach(attrs)
      else:
         raise TemplateXMLError(
               "Unknown element <%s> in xml file." % name)

   def evt_end_element(name):
      if name == "template":
         xmld.end_template()
      elif name == "file":
         xmld.end_file()
      elif name == "directory":
         xmld.end_directory()
      elif name == "except":
         xmld.end_except()
      elif name == "only":
         xmld.end_only()
      elif name == "filter":
         xmld.end_filter()
      elif name == "foreach":
         xmld.end_foreach()
      else:
         raise TemplateXMLError(
               "Unknown element </%s> in xml file." % name)

   def evt_character_data(cdata):
      xmld.character_data(cdata)

   xmlp = xml.parsers.expat.ParserCreate()

   xmlp.StartElementHandler = evt_start_element
   xmlp.EndElementHandler = evt_end_element
   xmlp.CharacterDataHandler = evt_character_data

   return xmlp

def transform_templates(file_name, input_path, output_path, *props, **opts):
   abs_filename = os.path.abspath(file_name)
   abs_input_path = os.path.abspath(input_path)
   abs_outputpath = os.path.abspath(output_path)
   
#   print input_path

   if os.path.isdir(abs_filename):
      toks = [abs_filename, "template.xml"]
   else:
      toks = os.path.split(abs_filename)

   try:
      xmlp = create_parser(abs_input_path, abs_outputpath, *props, **opts)
      with open(os.path.join(*toks), 'r') as xmlf:
         xmlp.Parse(xmlf.read())
      message("All templates processed.")

   except IOError as ex:
      error("While processing templates of %r: %s" % (file_name, ex))
   except TemplateXMLError as ex:
      error("While processing templates of %r: %s" % (file_name, ex))
   except xml.parsers.expat.error as ex:
      error("While processing templates of %r: %s" % (file_name, ex))

