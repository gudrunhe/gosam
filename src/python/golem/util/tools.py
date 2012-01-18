# vim: ts=3:sw=3:expandtab

import sys
import os.path
import imp
import traceback
import getopt
import re

import golem.model
import golem.properties
import golem.algorithms.helicity

from golem.util.path import golem_path
from golem.util.config import GolemConfigError
from golem.util.constants import MODEL_LOCAL

__logger__ = []

DEBUG   = 100
MESSAGE =  50
WARNING =  10
ERROR   =   0

DEFAULT_CMD_LINE_ARGS = [
      ('h', "help", "prints this help screen"),
      ('d', "debug", "prints out debug messages"),
      ('v', "verbose", "prints out status messages"),
      ('w', "warn", "prints out warnings and errors (default)"),
      ('q', "quiet", "suppresses warnings and messages"),
      ('l', "log-file=",
         "writes a log file with the current level of verbosity"),
   ]

def add_logger(file_name=None):
   if file_name is None:
      logger = Logger()
   else:
      logger = FileLogger(file_name)

   __logger__.append(logger)
   return logger

def add_logger_with_level(level, file_name=None):
   if file_name is None:
      logger = Logger(level)
   else:
      logger = FileLogger(file_name, level)

   __logger__.append(logger)
   return logger

def remove_logger(logger):
   if logger in __logger__:
      __logger__.remove(logger)
      return True
   return False

def debug(*messages):
   do_message(DEBUG, "DEB", "\n".join(messages))

def message(*messages):
   do_message(MESSAGE, "~~~", "\n".join(messages))

def warning(*messages):
   do_message(WARNING, "-->", "\n".join(messages))

def error(*messages):
   do_message(ERROR, "==>", "\n".join(messages))
   sys.exit("GoSam terminated due to an error")

def do_message(level, prefix, message):
   for logger in __logger__:
      logger.message(level, prefix, message)

class Logger:
   """
   A writer that outputs to the screen
   """
   def __init__(self, max_level=MESSAGE):
      self._max_level = max_level

   def format_lines(self, prefix, message):
      lines = message.splitlines()
      if len(lines) == 0:
         return prefix + " (No message given)"
      else:
         space = " " * (len(prefix) + 1)
         lines[0] = prefix + " " + lines[0]
         for i in range(1, len(lines)):
            lines[i] = space + lines[i]

      return "\n".join(lines)

   def write(self, aString):
      """
      This logger writes to the screen.
      """
      print(aString)

   def trace(self):
      lines = []
      count = 0
      for f, ln, fn, txt in traceback.extract_stack():
         count += 1

      for f, ln, fn, txt in traceback.extract_stack():
         count -= 1
         if count <= 3:
            break
         root, thefile = os.path.split(f)
         lines.append("%s[%d] (%s)" % (thefile, ln, fn))
      lines.append(">>> %s" % txt)
      return "\n".join(lines)


   def message(self, level, prefix, message):
      if level <= self._max_level:
         theString = self.format_lines(prefix, message)
         self.write(theString)
         #if self._max_level >= DEBUG:
         #   theString = self.format_lines("TRC", self.trace())
         #   self.write(theString)


class FileLogger(Logger):
   """
   A logger that writes to a file
   """

   def __init__(self, file_name, max_level=DEBUG):
      Logger.__init__(self, max_level)

      self._file = open(file_name, 'w')

   def __del__(self):
      self._file.close()
      self._file = None

   def write(self, aString):
      self._file.write(aString + "\n")

def copy_file(in_file, out_file):
   if not os.path.exists(in_file):
      raise GolemConfigError("File not found: %r" % in_file)

   f = open(in_file, 'r')
   lines = f.readlines()
   f.close()

   f = open(out_file, 'w')
   for line in lines:
      f.write(line)
   f.close()
   
def combinations(map):
   """
   This iterator lists all combinations of possible
   values for the elements of map.

   PARAMETER
      map -- a dictionary {key1: [value1_1, value1_2, ...], ...}

   RESULT
      yields all combinations as dictionaries {key1: value1_i, ...}
   """

   def rec_combinations(keys, map):
      if len(keys) == 0:
         yield {}
      else:
         key = keys[0]
         for new_map in rec_combinations(keys[1:], map):
            for heli in map[key]:
               result = new_map.copy()
               result[key] = heli
               yield result
   for c in rec_combinations(list(map.keys()), map):
      yield c


def enumerate_helicities(conf):
      """
      """
      zeroes = getZeroes(conf)
      in_particles, out_particles = generate_particle_lists(conf)
      fermion_filter = golem.algorithms.helicity.generate_symmetry_filter(
            conf, zeroes, in_particles, out_particles, error)

      in_particles.extend(out_particles)

      helic = {}
      for i in range(len(in_particles)):
         helic[i] = in_particles[i].getHelicityStates(zeroes)
         
      helicity_comb = [h for h in combinations(helic)]
      user_helis = conf.getProperty(golem.properties.helicities)
      if len(user_helis) > 0:
         ex_user_helis = expand_helicities(user_helis)

         new_helicity_comb = []
         for s in ex_user_helis:
            heli = golem.algorithms.helicity.parse_helicity(s)
            if heli in helicity_comb:
               new_helicity_comb.append(heli)
            else:
               raise golem.util.parser.TemplateError(
                  "Helicity %r is not valid for this process" % s)
         helicity_comb = new_helicity_comb

      for h in helicity_comb:
         if fermion_filter(h):
            yield h

def enumerate_and_reduce_helicities(conf):
   in_particles, out_particles = generate_particle_lists(conf)
   helicities = [h for h in enumerate_helicities(conf)]
   group = golem.algorithms.helicity.find_symmetry_group(helicities,
         conf, in_particles, out_particles, error)
   for g in group:
      yield g


def expand_helicities(patterns):
   anti = {"+": "-", "0": "0", "-": "+", "m": "k", "k": "m"}

   solutions = []
   while patterns:
      pat = patterns[0]
      patterns = patterns[1:]

      if "[" in pat:
         idx1 = pat.index("[")
         idx2 = pat.index("]")
         head = pat[:idx1]
         tail = pat[idx2+1:]
         chars = pat[idx1+1:idx2]
         if "=" in chars:
            eqidx = chars.index("=")
            if eqidx == 1:
               symbol =  chars[0]
               asymbol = " "
            elif eqidx == 2:
               symbol = chars[0]
               asymbol = chars[1]
            chars = chars[eqidx+1:]
         else:
            symbol = "%"
            asymbol = "~"

         for c in chars:
            ac = anti[c]
            patterns = [
               head.replace(symbol, c).replace(asymbol, ac) +
               c +
               tail.replace(symbol, c).replace(asymbol, ac) ] + patterns
      else:
         solutions.append(pat)
   return solutions


def encode_helicity(h, sym=golem.algorithms.helicity.heli_to_symbol):
   return dict([(k, sym[v]) for k, v in h.items()])

def prepare_model_files(conf, output_path=None):
   if output_path is None:
      path = process_path(conf)
   else:
      path = output_path

   model_lst = conf.getProperty(golem.properties.model)
   if "setup-file" in conf:
      rel_path = os.path.dirname(conf["setup-file"])
   else:
      rel_path = os.getcwd()

   if len(model_lst) == 0:
      model_lst = ['sm']

   if len(model_lst) == 1:
      model = model_lst[0]
      src_path = golem_path("models")
      for ext in ["", ".py", ".hh"]:
         copy_file(os.path.join(src_path, model + ext),
               os.path.join(path, MODEL_LOCAL + ext))
   elif len(model_lst) == 2:
      if model_lst[0].lower().strip() == "feynrules":
         model_path = model_lst[1]
         model_path = os.path.expandvars(model_path)
         model_path = os.path.expanduser(model_path)
         if not os.path.isabs(model_path):
            model_path = os.path.join(rel_path, model_path)
         message("Importing FeynRules model files ...")
         mdl = golem.model.feynrules.Model(model_path)
         mdl.store(path, MODEL_LOCAL)
         message("Done with model import.")
      else:
         model_path = model_lst[0]
         model_path = os.path.expandvars(model_path)
         model_path = os.path.expanduser(model_path)
         if not os.path.isabs(model_path):
            model_path = os.path.join(rel_path, model_path)
         model_name = model_lst[1]
         if model_name.isdigit():
            # This is a CalcHEP model, needs to be converted.
            message("Importing CalcHep model files ...")
            mdl = golem.model.calchep.Model(model_path, int(model_name))
            mdl.store(path, MODEL_LOCAL)
            message("Done with model import.")
         else:
            model = model_lst[1]
            for ext in ["", ".py", ".hh"]:
               copy_file(os.path.join(model_path, model + ext),
                     os.path.join(path, MODEL_LOCAL + ext))
   else:
      error("Parameter 'model' cannot have more than two entries.")

def getModel(conf, extra_path=None):
   MODEL_LOCAL = "model"

   if "model" in conf.cache:
         return conf.cache["model"]

   if extra_path is not None:
      path = extra_path
   else:
      path = process_path(conf)


   golem.model.MODEL_OPTIONS = {}
   for opt in conf.getListProperty(golem.properties.model_options):
      idx = -1
      for delim in [" ", ":", "="]:
         if delim in opt:
            didx = opt.index(delim)
            if idx < 0 or didx < idx:
               idx = didx
      if idx >= 0:
         golem.model.MODEL_OPTIONS[opt[:idx].strip()] = \
               opt[idx+1:].strip()
      else:
         golem.model.MODEL_OPTIONS[opt.strip()] = True

   fname = os.path.join(path, "%s.py" % MODEL_LOCAL)
   debug("Loading model file %r" % fname)
   mod = imp.load_source("model", fname)

   conf.cache["model"] = mod
   return mod

def expand_parameter_list(prop, conf):
   params = generate_parameter_list(conf)
   lst = conf.getProperty(prop, default=None)
   if lst is None:
      return

   new_values = set([])
   for value in lst:
      if "*" in value:
         pat = value.replace("*", r'(\w*)') + "$"
         cpat = re.compile(pat)
         count = 0
         for param in params:
            if cpat.match(param):
               count += 1
               new_values.add(param)
         if count == 0:
            warning("No known parameters match '%s' in property '%s'."
                  % (value, prop))
      elif value in params:
         new_values.add(value)
      else:
         warning("Property '%s' contains an unknown parameter name (%s)."
               % (prop, value),
               "The errorneous symbol has been removed from the list.")
   conf.setProperty(prop, list(new_values))

def generate_parameter_list(conf):
   from golem.util.constants import generate_gauge_var

   model = getModel(conf)
   result = list(model.types.keys())

   if generate_gauge_var and conf["__GAUGE_CHECK__"]:
      in_p, out_p = generate_particle_lists(conf)

      idx = 0
      for p in in_p:
         idx += 1
         twospin = abs(p.getSpin())
         if twospin == 2:
            result.append("gauge%dz" % idx)
      for p in out_p:
         idx += 1
         twospin = abs(p.getSpin())
         if twospin == 2:
            result.append("gauge%dz" % idx)

   return result




def generate_particle_lists(conf):
   """
   Generates a three-tuple of the form
      (in_particles, out_particles)
   where
      in_particles is the list of incoming particles.
      out_particles is the list of outgoing particles.
   """

   if "particle_lists" in conf.cache:
      inp, outp = conf.cache["particle_lists"]
      return inp[:], outp[:]

   ini = conf.getProperty(golem.properties.qgraf_in)
   fin = conf.getProperty(golem.properties.qgraf_out)

   mod = getModel(conf)

   in_particles = []
   for p in ini:
      particle = interpret_particle_name(p, mod)
      in_particles.append(particle)

   out_particles = []
   for p in fin:
      particle = interpret_particle_name(p, mod)
      out_particles.append(particle)

   conf.cache["particle_lists"] = (in_particles, out_particles)

   return (in_particles[:], out_particles[:])

__latex_particle_warnings__ = []

def interpret_particle_name(p, mod):
   """
   Translates a particle names into objects.
   """
   name = p.strip()
   if p in mod.particles:
      result = mod.particles[name]
   elif p in mod.mnemonics:
      result = mod.mnemonics[name]
      name = str(result)
   else:
      found = False
      try:
         pdg_code = int(name)
         for pname, p in mod.particles.items():
            if p.getPDGCode() == pdg_code:
               name = pname
               result = p
               found = True
               break
      except ValueError:
         pass
      if not found:
         raise GolemConfigError("Unknown particle: %r" % name)

   if name in mod.latex_names:
      result.setLaTeXName(mod.latex_names[name])
   else:
      if name not in __latex_particle_warnings__:
         __latex_particle_warnings__.append(name)
         warning("No LaTeX name for particle %r found." % name)


   return result

def diagram_count(path, suffix):
   """
   Analyzes the file diagrams-<suffix>.hh to
   infer the total number of diagrams in a
   process at the given loop order.

   PARAMETER

      path -- the path pointing to the file which contains
              the diagrams.
      suffix -- index which denotes the part of the amplitude


   This function looks for a line starting with
    '#define DIAGRAMCOUNT' and interprets the argument as the
    number of diagrams.
   """
   fname = os.path.join(path, "diagrams-%s.hh" % suffix)
   result = 0
   if os.path.exists(fname):
      f = open(fname, 'r')
      for line in f:
         if line.strip().startswith("#define DIAGRAMCOUNT"):
            words = line.strip().split()
            result = int(words[2].strip('"'))
            break
      f.close()
   else:
      pass
      # print "Warning: File %r not found." % fname
   return result

def setup_arguments(cmd_line_args, handler=None, extra_msg="", argv=sys.argv):
   """
   Use getopt to process command line arguments.

   PARAMETER

   cmd_line_args -- a list of tuples (s, l, h) where
            s = short form (one letter), e.g. 'x' for option '-x'
            l = long form; ends with a '=' if option takes an argument
            h = help message
   handler -- a function (name, value=None) -> True/False
            should return true if an argument is known, false otherwise
   """
   short_args = ""
   long_args = []
   long_width = 0
   for short_arg, long_arg, help_text in cmd_line_args:
      if short_arg != "":
         short_args += short_arg
         if long_arg.endswith("="):
            short_args += ":"
      if long_arg != "":
         long_args.append(long_arg)
         if long_arg.endswith("="):
            i = len("<ARG>")
         else:
            i = 0
         if len(long_arg) + i > long_width:
            long_width = len(long_arg) + i

   help_fmt = "-%s, --%-" + str(long_width) + "s -- %s"
   help_msgs = [
         "Usage: %s {options} %s" % (argv[0], extra_msg)
      ]

   for short_arg, long_arg, help_text in cmd_line_args:
      if long_arg.endswith("="):
         arg_opt = "<ARG>"
      else:
         arg_opt = ""
      help_msgs.append(help_fmt % (short_arg, long_arg + arg_opt, help_text))

   default_logger = add_logger_with_level(WARNING)

   try:
      opts, args = getopt.gnu_getopt(argv[1:], short_args, long_args)
   except getopt.GetoptError as err:
      # print help information and exit:
      error("Invalid command line argument:", str(err),
         "use %s --help for more information" % argv[0])

   verbosity = WARNING
   for o, a in opts:
      if o in ("-v", "--verbose"):
         verbosity = MESSAGE
      elif o in ("-d", "--debug"):
         verbosity = DEBUG
      elif o in ("-w", "--warn"):
         verbosity = WARNING
      elif o in ("-q", "--quiet"):
         verbosity = ERROR
      elif o in ("-l", "--log-file"):
         add_logger_with_level(verbosity, a)
      elif o in ("-h", "--help"):
         for msg in help_msgs:
            print(msg)
         sys.exit()
      else:
         if handler is None:
            error("Unhandled command line option: %s" % o)
         else:
            name = o.lstrip("-")
            if o.startswith("--"):
               pass
            else:
               for s, l, h in cmd_line_args:
                  if s == name:
                     name = l
                     break
            name = name.rstrip("=")

            success = handler(name, a)
            if not success:
               error("Unhandled command line option: %s" % o)

   remove_logger(default_logger)
   add_logger_with_level(verbosity)

   return args

def check_script_name(name):
   pname, sname = os.path.split(name)
   sbase, sext  = os.path.splitext(sname)
   flag = False
   if sbase.lower() == "golem-main":
      flag = True
      chunk1 = ""
      chunk2 = "It"
   elif sbase.lower() == "golem-init":
      flag = True
      chunk1 = "with the option --olp "
      chunk2 = "Apart from that, it"
     
   if flag:
      warning(
           "The use of the script %s is obsolete." % sname,
           "This script might be removed from any future version of GoSam.",
           "Please, use the script gosam.py %sinstead." % chunk1,
           "%s uses the same command line syntax as the old script." % chunk2)

def process_path(conf):
   setup_file = conf.getProperty("setup-file")
   setup_dir = os.path.dirname(setup_file)
   setup_dir = os.path.abspath(setup_dir)

   path = conf.getProperty(golem.properties.process_path)
   if path is None:
      error("Property %r must be set in %r!" %
            (str(golem.properties.process_path), setup_file))
   path = os.path.expandvars(path)
   if os.path.isabs(path):
      return path
   else:
      return os.path.join(setup_dir, path)

def banner(WIDTH=70, PREFIX="#", SUFFIX="#"):
   authors = golem.util.constants.AUTHORS
   asciiart = golem.util.constants.ASCIIART
   asciiwidth = max(map(len, asciiart))
   clines = golem.util.constants.CLINES

   llines = [
         "AUTHORS:"
   ]


   lauthor = max(map(len, authors.keys()))
   author_format = "* %" + str(-lauthor) + "s"
   for author in sorted(authors.keys(), key=lambda n: n.rsplit(" ", 1)[-1]):
      values = authors[author]
      if len(values) >= 1 and len(values[0]) > 0:
         email = " <" + values[0] + ">"
      else:
         email = ""
         
      llines.append((author_format % author) + email)
   maxauthorlen = max(map(len,llines))

   cl = WIDTH - len(PREFIX) - len(SUFFIX) - 1 - asciiwidth
   for lnr, line in enumerate(clines):
      if lnr < len(asciiart):
         asciiline = asciiart[lnr]
      else:
         asciiline = " " * asciiwidth
      outl = asciiline + line.center(cl)
      ll = len(outl) + 2
      if ll < WIDTH:
         yield PREFIX + " " + outl + (WIDTH-ll-1) * " " + SUFFIX
      else:
            yield PREFIX + " " + outl

   asciiline = " " * max(0, WIDTH - maxauthorlen - 4)

   for lnr, line in enumerate(llines):
      outl = asciiline + line
      ll = len(outl) + len(PREFIX) + len(SUFFIX)
      if ll < WIDTH:
         yield PREFIX + " " + outl + (WIDTH-ll-1) * " " + SUFFIX
      else:
         yield PREFIX + " " + outl

   for line in golem.util.constants.LICENSE:
      ll = len(line) + len(PREFIX) + len(SUFFIX)
      if ll < WIDTH:
         ws = " " * (WIDTH - ll)
      else:
         ws = ""
      yield PREFIX + line + ws + SUFFIX

class LimitedWidthOutputStream:
   def __init__(self, out, width, indent=0):
      self._out = out
      self._width = width
      self._indent = indent
      self._pos = indent

   def write(self, token):
      advance = len(str(token))
      if advance + self._pos > self._width:
         self._out.write("\n" + " " * self._indent)
         self._pos = self._indent
      self._out.write(str(token))
      self._pos += advance

   def nl(self):
      self._out.write("\n" + " " * self._indent)
      self._pos = self._indent

def getZeroes(conf):
   model_mod = getModel(conf)
   zeroes = list(filter(None, conf.getListProperty(golem.properties.zero)))
   for name, value in model_mod.parameters.items():
      if name in zeroes:
         continue
      t = model_mod.types[name]
      if t == 'RP':
         if float(value) == 0.0:
            zeroes.append(name)
      elif t == 'CP':
         if all(map(float, value)) == 0.0:
            zeroes.append(name)
   return zeroes

def product(lst):
   r = 1
   for i in lst:
      r *= i
   return r

def factorial(n):
   return product(range(2, n+1))
