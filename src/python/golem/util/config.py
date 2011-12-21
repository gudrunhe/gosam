# vim: ts=3:sw=3:expandtab
import sys
import datetime

import os
import os.path
import subprocess
import re
try:
   import ast
except ImportError:
   ast = None

import golem.util.path as gpath

class GolemConfigError(Exception):
   def __init__(self, value):
      Exception.__init__(self, value)
      self._value = value

   def __str__(self):
      return "Golem Configuration Error: %s" % self._value

   def __repr__(self):
      return "%s(%r)" % ( self.__class__, self._value)

   def value(self):
      return self._value

class Property:
   """
   This class is a wrapper for properties including their
   type and a description.

   The use of a wrapper allows for future changes of the syntax
   without affecting the source code in many places.
   """
   def __init__(self, name, description, type=str, default=None,
         experimental=False, options=None):
      """
      Note, in the case of type=list default encodes the
      delimiter character (';' or ',') with if default=None
      the comma is used.
      """
      self._name = name
      self._description = description
      self._type = type
      self._default = default
      self._experimental = experimental
      self._options = options

   def _guess_correct(self, options, *given):
      result = []
      for word in given:
         min_lev = len(word)
         min_opt = None
         for option in options:
            dist = levenshtein(word, option)
            if dist < min_lev:
               min_opt = option
               min_lev = dist
         if min_opt is not None and min_lev <= 5:
            result.append("Did you mean '%s' where you typed '%s'?"
                     % (min_opt, word))
      return result

   def check(self, conf):
      result = []
   
      if self._type == int:
         if self._options is not None:
            value = conf.getProperty(str(self))

            if value is not None:
               try:
                  ivalue = int(value)
                  if value not in self._options:
                     result.append(
                        "The value (%d) of option '%s'" +
                        " is not in the valid range."
                        % (ivalue, self))
               except ValueError:
                  result.append(
                        "The value (%r) of option '%s'" +
                        " is not an integer number."
                        % (value, self))
   
      elif self._type == bool:
         bool_values = [
               "1", "true", ".true.", "t", ".t.", "yes", "y",
         		"0", "false", ".false.", "f", ".f.", "no", "n"]
         value = conf.getProperty(str(self))

         if value is not None:
            if value.lower() not in bool_values:
               result.append(
                     "The value (%r) of option '%s' is not a boolean literal."
                     % (value, self))
               result.extend(self._guess_correct(bool_values, value))
   
      elif self._type == list:
         if self._options is not None:
            odds = []
            default = self.getDefault()
            sval = conf.getProperty(str(self))
            if sval is not None:
               if default is None:
                  values = sval.split(',')
               else:
                  values = sval.split(default)
   
               for value in values:
                  vls = value.lower().strip()
                  if vls == "":
                     continue
                  if vls not in self._options:
                     odds.append(value)
   
            if len(odds) > 0:
               result.append("The option '%s' contains unexpected values: %s"
                     % (self, ", ".join(map(repr, odds))))
               result.extend(self._guess_correct(self._options, *odds))
      else:
         if self._options is not None:
            value = conf.getProperty(str(self))
            if value is not None:
               if value.lower() not in self._options:
                  result.append("Unexpected value (%r) for option '%s'."
                        % (value, self))
                  result.extend(self._guess_correct(self._options, value))

      return result

   def isExperimental(self):
      return self._experimental

   def getName(self):
      return self._name

   def getDescription(self):
      return self._description

   def getType(self):
      return self._type

   def getDefault(self):
      return self._default

   def __str__(self):
      return self.getName()

   def __repr__(self):
      return "Property(%r, %r, %r, %r)" % (
            self._name, self._description,
            self._type, self._default)

class Properties:
   """
   This class provides a simplistic replacement for
   the Java class java.util.Properties.

   It is simplistic with respect to the limited number
   of escape sequences which are implemented:
     '\\', '\n', '\r', '\f', '\t'.
   As in the Java implementation, a single backslash
   in front of any other character is removed.
   """

   def __init__(self, defaults=None, **values):
      self._defaults = defaults
      self._map = {}
      for key, value in values.items():
         self.setProperty(key, str(value))

      self._decode = False

      self.cache = {}

   def decode(self):
      self._decode = True

   def nodecode(self):
      self._decode = False

   def getProperty(self, key, default=None):
      result = self._getProperty(key)
      if result is None:
         return default
      else:
         return result

   def _getProperty(self, key):
      if isinstance(key, Property):
         type = key.getType()
         name = str(key)
         default = key.getDefault()
         if(type == int):
            return self.getIntegerProperty(name, default)
         elif(type == bool):
            return self.getBooleanProperty(name, default)
         elif(type == list):
            if default is None:
               return self.getListProperty(name, ',')
            else:
               return self.getListProperty(name, default)
         else:
            return self.getProperty(name, default)
      else:
         if key in self._map:
            result = self._map[key]
         elif self._defaults is not None:
            if key in self._defaults:
               result = self._defaults[key]
            else:
               return None
         else:
            return None

         if self._decode and isinstance(result, str):
            # won't work in python3:
            # return result.decode("string_escape")
            # This is not 100% correct but should work reasonably well:
            if ast is not None:
               return ast.literal_eval("'"+result+"'")
            else:
               return result.decode("string_escape")
         else:
            return result
            

   def getListProperty(self, key, delimiter=','):
      name = str(key)
      if name in self:
         value = self[name].split(delimiter)
         return list(map(lambda x: x.strip(), value))
      else:
         return []

   def getBooleanProperty(self, key, default=False):
      true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
      name = str(key)
      if name in self:
         value = self[name].strip().lower()
         return value in true_values
      else:
         return default

   def getIntegerProperty(self, key, default=None):
      name = str(key)
      if name in self:
         value = self[name].strip()
         return int(value)
      else:
         return default

   def copyProperties(self, other, *keys):
      for key in keys:
         self.setProperty(key, other.getProperty(key))

   def copy(self, strip_plusses=False):
      result = Properties()
      for key in self.propertyNames():
         if key.startswith("+"):
            result.setProperty(key[1:], self.getProperty(key))
         else:
            result.setProperty(key, self.getProperty(key))
      return result

   def setProperty(self, key, value):
      name = str(key)
      if value.__class__ == list:
         self._map[name] = ",".join(map(str, value))
      else:
         self._map[name] = str(value)

   def __contains__(self, key):
      name = str(key)
      if name in self._map:
         return True
      elif self._defaults is not None:
         return name in self._defaults
      else:
         return False
         
   def propertyNames(self):
      for key in self._map.keys():
         yield key
      if self._defaults is not None:
         for key in self._defaults:
            if key not in self._map:
               yield key

   def list(self, stream=sys.stdout):
      for key in self:
         stream.write("%s=%s\n" % (escape(key, True), escape(self[key])))

   def store(self, stream, comments=None):
      if comments is not None:
         for cline in comments.splitlines():
            stream.write("# %s\n" % cline)
      stream.write("# %s\n" % datetime.datetime.now())
      for key in self:
         stream.write("%s=%s\n" % (escape(key, True), escape(self[key])))

   def load(self, stream):
      dollar_variables = []
      buf = ""
      for line in stream:
         buf += line.strip()
         if buf.startswith("!") or buf.startswith("#"):
            buf = ""
            continue
         elif buf == "":
            continue
         elif buf.endswith("\\"):
            bksl = ""
            while buf.endswith("\\\\"):
               bksl += "\\\\"
               buf = buf.rstrip("\\\\")
            if buf.endswith("\\"):
               buf = buf.rstrip("\\")
               buf += bksl
               continue
            else:
               buf += bksl
         # consider the line as terminated now

         # don't do replacements just look for '\\' or
         # one of '=', ':', ' ', '\t', '\f'
         preceeding_backslash = False
         separator_index = -1
         for i in range(len(buf)):
            if (not preceeding_backslash) and \
                  (buf[i] in ['=', ':', ' ', '\f', '\t']):
               separator_index = i
               break
            if buf[i] == '\\':
               preceeding_backslash = not preceeding_backslash
            else:
               preceeding_backslash = False

         if separator_index < 0:
            key = buf.strip()
            value = ""
         else:
            key = buf[0:separator_index].strip()
            value = buf[separator_index + 1:].strip()

         for dkey, dvalue in reversed(dollar_variables):
            for fmt in ["${%s}", "$(%s)", "$%s"]:
               key = key.replace(fmt % dkey, dvalue)
               value = value.replace(fmt % dkey, dvalue)

         if key.startswith("$"):
            dollar_variables.append( (key[1:], value) )
         else:
            self._map[unescape(key)] = unescape(value)
         buf = ""

   def __getitem__(self, key):
      return self._getProperty(key)

   def __setitem__(self, key, value):
      self.setProperty(key, value)
   
   def __iter__(self):
      return self.propertyNames()

   def addAll(self, other):
      for name in other:
         self[name] = other[name]
      return self

   def __iadd__(self, other):
      return self.addAll(other)

   def __str__(self):
      res = ""
      for key in self:
         res += "%s=%s\n" % (escape(key, True), escape(self[key]))
      return res

def unescape(s):
   buf = [s[i] for i in range(len(s))]
   if "\\" in buf:
      idx_bk = buf.index("\\")
   else:
      idx_bk = -1
   while idx_bk >= 0:
      if idx_bk + 1 < len(buf):
         ch = buf[idx_bk + 1]
         if ch == 'n':
            buf[idx_bk: idx_bk + 2] = "\n"
         elif ch == 'r':
            buf[idx_bk: idx_bk + 2] = "\r"
         elif ch == 'f':
            buf[idx_bk: idx_bk + 2] = "\f"
         elif ch == 't':
            buf[idx_bk: idx_bk + 2] = "\t"
         else:
            del buf[idx_bk: idx_bk + 1]
      if "\\" in buf[idx_bk + 1:]:
         idx_bk = buf.index("\\", idx_bk + 1)
      else:
         idx_bk = -1
   return "".join(buf)

def escape(s, isKey=False):
   escapes = {"\n": "\\n", "\r": "\\r", "\f": "\\f", "\t": "\\t"}
   keyescapes = {"=": "\\=", ":": "\\:", " ": "\\ "}
   buf = s.replace("\\", "\\\\")
   for ch, esc in escapes.items():
      buf = buf.replace(ch, esc)
   if isKey:
      for ch, esc in keyescapes.items():
         buf = buf.replace(ch, esc)
      if buf[0] in ['#', '!']:
         buf = "\\" + buf
   return buf

REQUIRED = 1
OPTIONAL = 0

class ConfigurationException(Exception):
   pass

class Component:
   def __init__(self):
      pass

   def examine(self, hints, **opts):
      pass

   def isInstalled(self):
      return False

   def getInstallationPath(self):
      return []

   def getInstance(self):
      pass

   def undohome(self, name):
      home = os.getenv("HOME")
      if home is not None:
         if name == home:
            return "${HOME}"
         if name.startswith(home):
            lh = len(home)
            return "${HOME}" + name[lh:]
      return name


   def store(self, conf):
      pass

   def generatePossibleDirs(self, suffix, **opts):
      user_home = gpath.get_homedir()
      golem_dir = gpath.golem_path()
      curdir = os.path.abspath(os.path.curdir)
      result = []

      if suffix == "lib" and "libdir" in opts:
         libdir = opts["libdir"]
         result.append(libdir)

      if suffix == "bin" and "bindir" in opts:
         bindir = opts["bindir"]
         result.append(bindir)

      if "prefix" in opts:
         prefix = opts["prefix"]
         d = os.path.join(prefix, suffix)
         if d not in result:
            result.append(d)

      for path in [
            os.path.join("/usr", suffix),
            os.path.join("/usr", "local", suffix),
            os.path.join(user_home, suffix),
            os.path.join(user_home, "local", suffix),
            os.path.join(golem_dir, suffix),
            os.path.join(curdir, suffix),
            os.path.join(curdir, "local", suffix)]:
         if path not in result:
            result.append(path)

      if suffix == "lib":
         ldp = os.getenv("LD_LIBRARY_PATH")
         if ldp:
            for path in ldp.split(os.path.pathsep):
               if path not in result:
                  result.append(path)

      if suffix == "bin":
         ldp = os.getenv("PATH")
         if ldp:
            for path in ldp.split(os.path.pathsep):
               if path not in result:
                  result.append(path)
      return result

class Library(Component):
   def __init__(self, cname, *names):
      self.locations = []
      self.libnames = list(names)
      self.extensions = [".so", ".a", ".dll"]
      self.name = cname

   def examine(self, hints, **opts):
      user_home = gpath.get_homedir()
      golem_dir = gpath.golem_path()
      curdir = os.path.abspath(os.path.curdir)
      dirs = self.generatePossibleDirs("lib")

      if self.name in hints:
         dirs = [hints[self.name]] + dirs

      for dir in dirs:
         found = False
         for libname in self.libnames:
            for ext in self.extensions:
               fname = os.path.join(dir, libname + ext)
               if os.path.exists(fname):
                  self.locations.append(dir)
                  found = True
                  break
            if found:
               break

   def findIncludeDir(self, subpath, incname, hints, *extensions):
      user_home = gpath.get_homedir()
      golem_dir = gpath.golem_path()
      curdir = os.path.abspath(os.path.curdir)
      dirs = self.generatePossibleDirs(os.path.join("include", subpath))

      locations = []

      if self.name in hints:
         dirs = [hints[self.name]] + dirs

      for dir in dirs:
         found = False
         for ext in extensions:
            fname = os.path.join(dir, incname + ext)
            if os.path.exists(fname):
               locations.append(dir)
               found = True
               break
            if found:
               break
      return locations

   def getInstance(self):
      dirs = self.getInstallationPath()
      for libname in self.libnames:
         for ext in self.extensions:
            fname = os.path.join(dirs[0], libname + ext)
            if os.path.exists(fname):
               return fname

   def isInstalled(self):
      return len(self.locations) > 0

   def getInstallationPath(self):
      return self.locations[:]

class Program(Component):
   def __init__(self, cname, *names):
      self.locations = []
      self.prognames = list(names)
      self.extensions = ["", ".exe", ".com"]
      self.name = cname


   def examine(self, hints):
      user_home = gpath.get_homedir()
      golem_dir = gpath.golem_path()
      curdir = os.path.abspath(os.path.curdir)
      dirs = self.generatePossibleDirs("bin")

      if self.name in hints:
         hint = hints[self.name]
         if os.path.exists(hint):
            self.locations.append(hint)

      for progname in self.prognames:
         for ext in self.extensions:
            for dir in dirs:
               fname = os.path.join(dir, progname + ext)
               if os.path.exists(fname):
                  if dir not in self.locations:
                     self.locations.append(fname)

   def getInstance(self):
      if len(self.locations) > 0:
         return self.locations[0]

   def isInstalled(self):
      return len(self.locations) > 0

   def getInstallationPath(self):
      return self.locations[:]

class LoopTools(Library):
   def __init__(self):
      Library.__init__(self, "LoopTools", "libooptools")

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])

      if "+zzz.extensions" in conf:
         conf["+zzz.extensions"] += ", looptools"
      else:
         conf["+zzz.extensions"] = "looptools"

      conf["+looptools.ldflags"] = "-L%s -looptools" % path

class AVH_OneLoop(Library):
   def __init__(self):
      Library.__init__(self, "avholo", "libavh_olo")

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])

      if "+zzz.extensions" in conf:
         conf["+zzz.extensions"] += ", avh_olo"
      else:
         conf["+zzz.extensions"] = "avh_olo"

      conf["+avh_olo.ldflags"] = "-L%s -lavh_olo" % path

class QCDLoop(Library):
   def __init__(self):
      Library.__init__(self, "QCDLoop", "libqcdloop")

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])

      if "+zzz.extensions" in conf:
         conf["+zzz.extensions"] += ", qcdloop"
      else:
         conf["+zzz.extensions"] = "qcdloop"

      conf["+qcdloop.ldflags"] = "-L%s -lqcdloop" % path


class Samurai(Library):
   def __init__(self):
      Library.__init__(self, "Samurai", "libsamurai")

   def examine(self, hints):
      Library.examine(self, hints)
      if len(self.locations) > 0:
         self.incdirs = self.findIncludeDir("samurai", "msamurai", hints,
               ".mod")
         if len(self.incdirs) == 0:
            self.locations = []

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])
      incd = self.undohome(self.incdirs[0])

      if "+installed.extensions" in conf:
         conf["+installed.extensions"] += ", samurai"
      else:
         conf["+installed.extensions"] = "samurai"

      conf["samurai.fcflags"] = "-I%s" % incd
      conf["samurai.ldflags"] = "-L%s -lsamurai" % path

class PJFry(Library):
   def __init__(self):
      Library.__init__(self, "PJFry", "libpjfry")

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])

      if "+installed.extensions" in conf:
         conf["+installed.extensions"] += ", pjfry"
      else:
         conf["+installed.extensions"] = "pjfry"

      conf["+pjfry.ldflags"] = "-L%s -lpjfry" % path

class Golem95(Library):
   def __init__(self):
      Library.__init__(self, "Golem", "libgolem")

   def examine(self, hints):
      Library.examine(self, hints)
      if len(self.locations) > 0:
         self.incdirs = self.findIncludeDir("golem95", "parametre", hints,
               ".mod")
         if len(self.incdirs) == 0:
            self.locations = []

   def store(self, conf):
      paths = self.getInstallationPath()
      if len(paths) == 0:
         return

      path = self.undohome(paths[0])
      incd = self.undohome(self.incdirs[0])

      if "+installed.extensions" in conf:
         conf["+installed.extensions"] += ", golem95"
      else:
         conf["+installed.extensions"] = "golem95"

      conf["golem95.fcflags"] = "-I%s" % incd
      conf["golem95.ldflags"] = "-L%s -lgolem" % path

class Form(Program):
   def __init__(self):
      Program.__init__(self, "Form",
            "tformi", "formi", "tvormi", "vormi",
            "tform", "form", "tvorm", "vorm",
            "tform3", "form3", "tvorm3", "vorm3")

   def examine(self, hints):
      Program.examine(self, hints)
      executable = self.getInstance()

      try:
         pipe = subprocess.Popen(executable,
               shell=True,
               bufsize=500, stdout=subprocess.PIPE).stdout

         for line in pipe.readlines():
            lline = line.lower().strip()
            if "version" in lline:
               i = lline.index("version")
               j = lline.index("(")
               lline = lline[i+len("version"):j]
               self.version = [int(re.sub("[^0-9]", "", s))
                     for s in lline.split(".")]
      except OSError:
         raise ConfigurationException(
               "Could not run FORM (%s) properly" % executable)

   def store(self, conf):
      conf["form.bin"] = self.undohome(self.getInstance())
      if version_compare(self.version, [4,0]) >= 0:
         conf["+form.extensions"] = "topolynomial"

class Fortran(Program):
   def __init__(self):
      Program.__init__(self, "Fortran",
            "ifort", "f95i",
            "f95", "f95n",
            "lfc", "lf95", "f95f",
            "xlf95", "xlf90", "xlf",
            "gfortran", "g95",
            "f95", "f90", "frt", "pgf", "pgf90", "pghpf",
            "fort90", "fl64", "fl32",
            "pgf77", "g77", "fort77", "f77", "af77", "f2c")

   def examine(self, hints):
      fc = os.getenv("FC")
      if fc is not None:
         path, prog = os.path.split(fc)
         if len(prog) > 0:
            self.prognames = [prog] + self.prognames
         if len(path) > 0 and self.name not in hints:
            hints = hints.copy()
            hints[self.name] = path

      Program.examine(self, hints)

   def store(self, conf):
      conf["fc.bin"] = self.undohome(self.getInstance())

class QGraf(Program):
   def __init__(self):
      Program.__init__(self, "QGraf", "qgraf")

   def store(self, conf):
      conf["qgraf.bin"] = self.undohome(self.getInstance())

class Java(Program):
   def __init__(self):
      Program.__init__(self, "Java", "java")

   def store(self, conf):
      haggies_jar = self.undohome(gpath.golem_path("haggies", "haggies.jar"))
      java = self.undohome(self.getInstance())
      conf["haggies.bin"] = "%s -jar %s" % \
            (java, haggies_jar)

class Configurator:
   def __init__(self, hints, **components):

      self.installed_components = []

      not_found = []

      for name, required in components.items():
         if name not in globals():
            raise ConfigurationException("Name '%s' not known" % name)

         cls = globals()[name]

         if type(cls) != type(Component):
            raise ConfigurationException(
                  "Name '%s' does not denote a class" % name)
         if not issubclass(cls, Component):
            raise ConfigurationException(
                  "Class '%s' is not a subclass of 'Component'" % name)
                  
         component = cls()

         self.message("Searching for %s ..." % name)
         component.examine(hints)

         if not component.isInstalled():
            if required == REQUIRED:
               not_found.append(name)
               self.message("Required component %s is not installed." % name)
            else:
               self.message("Component %s is not installed." % name)
         else:
            paths = component.getInstallationPath()
            l = len(paths)
            if l == 1:
               self.message("Component %s has been found." % name)
               self.message("     %s" % (paths[0]))
            else:
               self.message("Component %s has been found in %d places." %
                     (name, l))
               for i, path in enumerate(paths):
                  self.message("#%2d: %s" % (i+1, path))
            self.installed_components.append(component)

   def message(self, message):
      print("# ~~~ " + message)

   def fail(self, message):
      print("==> Configuration failed:")
      print("    " + message)
      sys.exit(1)

   def store(self, conf):
      for component in self.installed_components:
         component.store(conf)

def version_compare(v1, v2):
   l1 = len(v1)
   l2 = len(v2)
   if l1 < l2:
      v1c = v1 + [0] * (l2-l1)
      v2c = v2[:]
   else:
      v1c = v1[:]
      v2c = v2 + [0] * (l1-l2)

   for p1, p2 in zip(v1c, v2c):
      if p1 > p2:
         return 1
      elif p1 < p2:
         return -1
   return 0

def levenshtein(str1, str2, case_sensitive=False):
	l1 = len(str1)
	l2 = len(str2)

	if case_sensitive:
		if l1 < l2:
			if l1 == 0:
				return l2
			s2 = str1
			s1 = str2
		else:
			if l2 == 0:
				return l1
			s1 = str1
			s2 = str2
	else:
		if l1 < l2:
			if l1 == 0:
				return l2
			s2 = str1.lower()
			s1 = str2.lower()
		else:
			if l2 == 0:
				return l1
			s1 = str1.lower()
			s2 = str2.lower()


	previous_row = xrange(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			# j+1 instead of j since previous_row and current_row
			# are one character longer
			insertions = previous_row[j + 1] + 1
			# than s2
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row

	return previous_row[-1]
