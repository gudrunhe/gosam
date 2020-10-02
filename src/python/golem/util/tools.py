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
import golem.installation

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
      ('r', "report", "generate post-mortem debug file"),
      ('', "olp", "switch to OLP mode. Use --olp --help for more options."),
      ('', "version", "prints the current version of GoSam")
   ]

POSTMORTEM_LOG = []
POSTMORTEM_CFG = None
POSTMORTEM_DO = False

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
   POSTMORTEM_LOG.extend(messages)
   do_message(MESSAGE, "~~~", "\n".join(messages))

def warning(*messages):
   POSTMORTEM_LOG.extend(messages)
   do_message(WARNING, "-->", "\n".join(messages))

def error(*messages):
   POSTMORTEM_LOG.extend(messages)
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
      user_helis = [i for i in user_helis if i]

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
   conf = golem.algorithms.helicity.filter_helicities(conf, in_particles, out_particles)
   helicities = [h for h in enumerate_helicities(conf)]
   group = golem.algorithms.helicity.find_gauge_invariant_symmetry_group(helicities,
         conf, in_particles, out_particles, error)
   return group


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
   return dict([(k, sym[v]) for k, v in list(h.items())])

def prepare_model_files(conf, output_path=None):
   if output_path is None:
      path = process_path(conf)
   else:
      path = output_path

   model_lst = conf.getProperty(golem.properties.model)

   # For BLHA2 standards: conversion to GoSam internal keywords of SM:
   if len(model_lst) == 1 and str(model_lst[0]).lower() == 'smdiag':
      model_lst[0] = 'smdiag'
      conf.setProperty("model","smdiag")
   if len(model_lst) == 1 and str(model_lst[0]).lower() == 'smnondiag':
      model_lst[0] = 'sm'
      conf.setProperty("model","sm")
   
  # new: if we generate UV counterterms we need extra files
   genUV = conf["generate_uv_counterterms"]

   if "setup-file" in conf:
      rel_path = os.path.dirname(conf["setup-file"])
   else:
      rel_path = os.getcwd()
   if len(model_lst) == 0:
      model_lst = ['sm']
      conf.setProperty("model","sm")
   if len(model_lst) == 1:
      model = model_lst[0]
      src_path = golem_path("models")
      # check for local file
      if os.path.sep in model and all([os.path.exists(os.path.join(rel_path,model + ext)) \
         for ext in ["", ".py", ".hh"]]):
         src_path=rel_path
      for ext in ["", ".py", ".hh"]:
         copy_file(os.path.join(src_path, model + ext),
               os.path.join(path, MODEL_LOCAL + ext))
      if genUV == 'true':
         print('Generating UV terms')
         for ext in [".py", ".hh"]:
            copy_file(os.path.join(src_path, model + 'ct' + ext),
                  os.path.join(path, MODEL_LOCAL + 'ct' + ext))
   elif len(model_lst) == 2:
      if model_lst[0].lower().strip() == "feynrules":
         model_path = model_lst[1]
         model_path = os.path.expandvars(model_path)
         model_path = os.path.expanduser(model_path)
         if not os.path.isabs(model_path):
            model_path = os.path.join(rel_path, model_path)
         message("Importing FeynRules model files ...")
         extract_model_options(conf)
         mdl = golem.model.feynrules.Model(model_path,golem.model.MODEL_OPTIONS)
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
            if genUV == 'true':
               for ext in [".hh", ".py"]:
                  copy_file(os.path.join(model_path, model + 'ct' + ext),
                        os.path.join(path, MODEL_LOCAL + 'ct' + ext))
   else:
      error("Parameter 'model' cannot have more than two entries.")


def extract_model_options(conf):
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

def getModel(conf, extra_path=None):
   MODEL_LOCAL = "model"

   if "model" in conf.cache:
         return conf.cache["model"]

   if extra_path is not None:
      path = extra_path
   else:
      path = process_path(conf)


   golem.model.MODEL_OPTIONS = {}
   golem.model.MODEL_ONES = conf.getListProperty(golem.properties.one)

   model_shortname = conf["model"]

   extract_model_options(conf)

   fname = os.path.join(path, "%s.py" % MODEL_LOCAL)
   debug("Loading model file %r" % fname)

   # --[ EW scheme management:

   # Check if there is a line with "#@modelproperty: supports ewchoose"
   # before the first line of code.

   ew_supp = False
   with open(fname, 'r') as modelfile:
      for line in modelfile:
         stripped_line = line.strip()
         if stripped_line != '' and not stripped_line.startswith("#"):
            # "#@modelproperty: supports ewchoose" not found
            debug('Model seems to not support "ewchoose".\n' +
                  'If it does, add the line\n' +
                  '"#@modelproperty: supports ewchoose" to\n' +
                  'the top of %s.' % fname)
            break
         elif stripped_line == "#@modelproperty: supports ewchoose":
            debug('Model supports "ewchoose".\n')
            ew_supp = True
            break
         # else: pass

   # Adapt EW scheme to order file request:
   if conf["olp.ewscheme"] is not None and ew_supp == True:
         select_olp_EWScheme(conf)
   elif ew_supp == True and ( ( conf["model.options"] is None) or \
         "ewchoose" in conf["model.options"] ):
      golem.model.MODEL_OPTIONS["ewchoose"]=True
   elif conf["olp.ewscheme"] is not None and ew_supp == False:
         error("EWScheme tag in orderfile incompatible with model.")

   # Modify EW setting for model file:
   if ew_supp and "ewchoose" in list(golem.model.MODEL_OPTIONS.keys()):
      if golem.model.MODEL_OPTIONS["ewchoose"] == True:
         golem.model.MODEL_OPTIONS["users_choice"] = '0'
      else:
         golem.model.MODEL_OPTIONS["users_choice"] = golem.model.MODEL_OPTIONS["ewchoose"]
         golem.model.MODEL_OPTIONS["ewchoose"] = True
   elif ew_supp and "ewchoose" not in list(golem.model.MODEL_OPTIONS.keys()):
      golem.model.MODEL_OPTIONS["ewchoose"] = False
      golem.model.MODEL_OPTIONS["users_choice"] = '0'
   elif ew_supp == False and "ewchoose" in list(golem.model.MODEL_OPTIONS.keys()):
      del golem.model.MODEL_OPTIONS["ewchoose"]
      #error("ewchoose option in model.options is not supported with the chosen model.")

   # --] EW scheme management

   mod = imp.load_source("model", fname)

   conf.cache["model"] = mod
   return mod

def select_olp_EWScheme(conf):
   ewparameters = ['mW','mZ','alpha','GF','sw','e','vev','ewchoose']
   ewscheme = conf["olp.ewscheme"]
   raisewarn = False
   for key, value in list(golem.model.MODEL_OPTIONS.items()):
      if any(item.startswith(str(key)) for item in ewparameters):
         raisewarn = True
#  possible values are: alphaGF, alpha0, alphaMZ, alphaRUN, alphaMSbar, OLPDefined
   if ewscheme == "alphaGF":
      golem.model.MODEL_OPTIONS["ewchoose"]='1'
      print("OLP EWScheme --> alphaGF (Gmu scheme)")

   if ewscheme == "alpha0":
      golem.model.MODEL_OPTIONS["ewchoose"]='2'
      golem.model.MODEL_OPTIONS["alpha"]='0.007297352536480967'
      print("OLP EWScheme --> alpha0")

   if ewscheme == "alphaMZ":
      golem.model.MODEL_OPTIONS["ewchoose"]='2'
      # Value of alpha(Mz)^-1=128.944 from Nucl.Phys.Proc.Suppl. 225-227 (2012) 282-287
      golem.model.MODEL_OPTIONS["alpha"]='0.007755305'
      print("OLP EWScheme --> alphaMZ")

   if ewscheme == "alphaRUN":
      print("OLP EWScheme --> alphaRUN")
      print("EW not supported yet!")
   if ewscheme == "alphaMSbar":
      print("OLP EWScheme --> alphaMSbar")
      print("EW not supported yet!")
   if ewscheme == "OLPDefined":
      print("OLP EWScheme --> OLPDefined: GoSam default taken")
      golem.model.MODEL_OPTIONS["ewchoose"]=2
      
   if raisewarn == True:
      warning("Warning: EWScheme setting from orderfile will override the model.options\n" + \
                 " setting from input card if incompatible!")
   # print golem.model.MODEL_OPTIONS
   return


def expand_parameter_list(prop, conf):
   params = generate_parameter_list(conf)
   lst = conf.getProperty(prop, default=None)
   if lst is None:
      return

   new_values = set([])
   for value in lst:
      if not value:
         continue
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
         if str(prop)=="zero" and value=="mU":
            warning("Property '%s' contains an unknown parameter name (%s)."
                 % (prop, value),
                 "You are probably using a different model than the built-in models",
                 "and therefore cannot use the default value list of the 'zero' input parameter.",
                 "To remove this warning add at least 'zero=' (or whatever is appropriate) to your input card.",
                 "The symbol has been removed from the list.")
         else:
            warning("Property '%s' contains an unknown parameter name (%s)."
                 % (prop, value),
                 "The symbol has been removed from the list.")
   conf.setProperty(prop, list(new_values))

def generate_parameter_list(conf):
   model = getModel(conf)
   result = list(model.types.keys())

   if conf["__GAUGE_CHECK__"]:
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
         for pname, p in list(mod.particles.items()):
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
   global POSTMORTEM_DO
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
   help_fmt_only_long = "--%-" + str(long_width+4) + "s -- %s"
   help_msgs = [
         "Usage: %s {options} %s" % (argv[0], extra_msg)
      ]

   for short_arg, long_arg, help_text in cmd_line_args:
      if long_arg.endswith("="):
         arg_opt = "<ARG>"
      else:
         arg_opt = ""
      if short_arg:
         help_msgs.append(help_fmt % (short_arg, long_arg + arg_opt, help_text))
      else:
         help_msgs.append(help_fmt_only_long % (long_arg + arg_opt, help_text))

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
      elif o in ("-r", "--report"):
         POSTMORTEM_DO = True
      elif o in ("--version"):
         print("GoSam %s (rev %s)" % (".".join(map(str, golem.installation.GOLEM_VERSION)), golem.installation.GOLEM_REVISION))
         print("Copyright (C) 2011-2017  The GoSam Collaboration")
         print("This is free software; see the source for copying conditions.  There is NO\n" +
               "warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
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
   if sbase.lower() == "gosam-main":
      flag = True
      chunk1 = ""
      chunk2 = "It"
   elif sbase.lower() == "gosam-init":
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
   former_authors = golem.util.constants.FORMER_AUTHORS
   asciiart = golem.util.constants.ASCIIART
   asciiwidth = max(list(map(len, asciiart)))
   clines = golem.util.constants.CLINES

   llines = [
         "AUTHORS:"
   ]


   lauthor = max(list(map(len, list(authors.keys()))))
   author_format = "* %" + str(-lauthor) + "s"
   for author in sorted(list(authors.keys()), key=lambda n: n.rsplit(" ", 1)[-1]):
      values = authors[author]
      if len(values) >= 1 and len(values[0]) > 0:
         email = " <" + values[0] + ">"
      else:
         email = ""
         
      llines.append((author_format % author) + email)

   llines.append("")
   llines.append("FORMER AUTHORS:")
   for author in sorted(list(former_authors.keys()), key=lambda n: n.rsplit(" ", 1)[-1]):
      values = former_authors[author]
      if len(values) >= 1 and len(values[0]) > 0:
         email = " <" + values[0] + ">"
      else:
         email = ""

      llines.append((author_format % author) + email)
   maxauthorlen = max(list(map(len,llines)))

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

   asciiline = " " * max(0, WIDTH - maxauthorlen - 7)

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
   zeroes = list([_f for _f in conf.getListProperty(golem.properties.zero) if _f])
   for name, value in list(model_mod.parameters.items()):
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

def getOnes(conf):
   model_mod = getModel(conf)
   ones = list([_f for _f in conf.getListProperty(golem.properties.one) if _f])
   for name, value in list(model_mod.parameters.items()):
      if name in ones:
         continue
      t = model_mod.types[name]
      if t == 'RP':
         if float(value) == 1.0:
            ones.append(name)
      elif t == 'CP':
         if float(value[0]) == 1.0 and float(value[1]) == 0.0:
            ones.append(name)
   return ones

def product(lst):
   r = 1
   for i in lst:
      r *= i
   return r

def factorial(n):
   return product(list(range(2, n+1)))

def derive_coupling_names(conf):
   """
   For a given configuration try to find out how the QCD and the QED
   couplings are called and if they are set to one.
   """

   result = {}

   candidates = {
         'QCD': ['gs', 'mdlG', 'mdlGG'],
         'QED': ['e', 'mdlee', 'mdlEE']
   }

   model = getModel(conf)
   symbols = list(model.types.keys())
   ones = getOnes(conf)
   zeroes = getZeroes(conf)

   for t, lst in list(candidates.items()):
      flag = False
      for c in lst:
         if c in symbols:
            if c in ones:
               result[t] = '1'
            elif c in zeroes:
               result[t] = '0'
            else:
               result[t] = c
            flag = True
            break
      if not flag:
         result[t] = '0'
   return result
