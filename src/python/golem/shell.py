# vim: ts=3:sw=3:expandtab

import os
import subprocess
try:
   import StringIO as io
except ImportError:
   import io
import signal
import sys

import golem
import golem.util.ishell
import golem.properties
import golem.util.constants
import golem.util.config

from golem.util.main_misc import find_config_files, write_template_file, \
      workflow, generate_process_files

class GolemShell(golem.util.ishell.InteractiveShell):
   def __init__(self,
         prompt="GoSam> "):

      self.golem_follow_set = {
            "": [],
            str(golem.properties.process_path): [" file"],
            str(golem.properties.template_path): [" file"],
            str(golem.properties.qgraf_power): ["QCD, ", "QED, ", "None, "],
            str(golem.properties.qgraf_options): [
               "onepi", "onepr", "onshell", "offshell",
               "nosigma", "sigma", "nosnail", "snail",
               "notadpole", "tadpole", "simple", "notsimple",
               "floop", "topol"
               ],
            str(golem.properties.model): [
               "sm", "smdiag", "FeynRules", " file"],
            str(golem.properties.qgraf_verbatim): [
               "true=", "false=",
               "iprop[", "chord[", "bridge[", "rbridge[", "bridge[",
               "vsum[", "psum["],
            str(golem.properties.qgraf_verbatim_lo): [
               "true=", "false=",
               "iprop[", "bridge[", "rbridge[", "bridge[",
               "vsum[", "psum["],
            str(golem.properties.qgraf_verbatim_nlo): [
               "true=", "false=",
               "iprop[", "chord[", "bridge[", "rbridge[", "bridge[",
               "vsum[", "psum["],
            str(golem.properties.qgraf_bin): [" file", "qgraf"],
            str(golem.properties.form_bin): [" file",
                  "form", "vorm", "tform", "tvorm",
                  "formi", "vormi", "tformi", "tvormi"],
            str(golem.properties.form_tmp): [" file"],
            str(golem.properties.fc_bin): [" file",
                  "gfortran", "g95", "ifort"],
            str(golem.properties.group_diagrams): ["true", "false"],
            str(golem.properties.extensions): [
                  "samurai", "golem95", "pjfry", "fr5", "dred",
                  "autotools", "qshift", "topolynomial",
                  "qcdloop", "avh_olo", "looptools", "gaugecheck", "derive",
                  "generate-all-helicities", "olp_daemon", "numpolvec",
                  "f77", "no-fr5","ninja","customspin2prop"],
            str(golem.properties.debug_flags): ["lo", "nlo", "all"],
            str(golem.properties.filter_lo_diagrams): ["lambda d:"],
            str(golem.properties.filter_nlo_diagrams): ["lambda d:"],
            str(golem.properties.abbrev_level): [
                  "diagram", "group", "helicity"],
            str(golem.properties.r2): [
               "implicit", "explicit", "only", "off"],
            str(golem.properties.symmetries): [
               "flavour", "family", "lepton", "generation", "parity"],
            str(golem.properties.config_renorm_gamma5): ["true", "false"],
            str(golem.properties.config_renorm_mqwf): ["true", "false"],
            str(golem.properties.config_renorm_decoupling): ["true", "false"],
            str(golem.properties.config_renorm_mqse): ["true", "false"],
            str(golem.properties.config_renorm_logs): ["true", "false"],
            str(golem.properties.config_renorm_beta): ["true", "false"],
            str(golem.properties.config_renorm_yukawa): ["true", "false"],
            str(golem.properties.config_nlo_prefactors): ["0", "1", "2"],
            str(golem.properties.pyxodraw): ["true", "false"],
            "!": [" file"]
         }
      self.golem_delims = " :=,"

      for cmd in COMMANDS:
         self.golem_follow_set[""].append(str(cmd) + " ")
         self.golem_follow_set[str(cmd)] = cmd.followset

      for prop in golem.properties.properties:
         self.golem_follow_set[""].append(str(prop) + " ")

      golem.util.ishell.InteractiveShell.__init__(self,
         prompt = prompt,
         history_file = ".gosam_history",
         completer_delims = self.golem_delims,
         follow_set = self.golem_follow_set)

      self.banner()
      self.reset()

   def reset(self):
      self.relative_path = os.getcwd()
      self.conf = find_config_files()
      self.update_model()
      self.session = []

   def banner(self):
      WIDTH = 80
      CMTCH = "#"

      print(CMTCH * WIDTH)
      for line in golem.util.tools.banner(
            WIDTH=WIDTH, PREFIX=CMTCH, SUFFIX=CMTCH):
         print(line)
      print(CMTCH * WIDTH)

   def update_model(self):
      rel_path = self.relative_path
      model_lst = self.conf.getProperty(golem.properties.model)

      if len(model_lst) == 0:
         model_lst = ['sm']

      python_file = io.StringIO()

      try:
         if len(model_lst) == 1:
            model = model_lst[0]
            src_path = golem.util.path.golem_path("models")
            fname = os.path.join(src_path, model + ".py")
            f = open(fname, 'r')
            for line in f:
               python_file.write(line)
            f.close()

         elif len(model_lst) == 2:
            if model_lst[0].lower().strip() == "feynrules":
               model_path = model_lst[1]
               model_path = os.path.expanduser(model_path)
               model_path = os.path.expandvars(model_path)
               if not os.path.isabs(model_path):
                  model_path = os.path.join(rel_path, model_path)
               mdl = golem.model.feynrules.Model(model_path)
               mdl.write_python_file(python_file)
            else:
               model_path = model_lst[0]
               model_path = os.path.expanduser(model_path)
               model_path = os.path.expandvars(model_path)
               if not os.path.isabs(model_path):
                  model_path = os.path.join(rel_path, model_path)
               model_name = model_lst[1]
               if model_name.isdigit():
                  # This is a CalcHEP model, needs to be converted.
                  mdl = golem.model.calchep.Model(model_path, int(model_name))
                  mdl.write_python_file(python_file)
               else:
                  model = model_lst[1]
                  src_path = model_lst[0]
                  fname = os.path.join(src_path, model + ".py")
                  f = open(fname, 'r')
                  for line in f:
                     python_file.write(line)
                  f.close()
         else:
            print("Parameter 'model' cannot have more than two entries.")
            return

         mdl_dict = {}
         mdl_dict.update(globals())
         exec(compile(python_file.getvalue(), 'model.py', 'exec'),
               mdl_dict, mdl_dict)
         self.model = mdl_dict

      except IOError as err:
         print("An error occurred when updating the model file:")
         print(err)
         self.recommendations[golem.properties.model] = "sm"
         return

      finally:
         python_file.close()

      particle_names = set([])
      
      particle_names.update(self.model["particles"].keys())
      particle_names.update(self.model["mnemonics"].keys())

      particle_names = list(particle_names)

      self.golem_follow_set[str(golem.properties.qgraf_in)] = particle_names
      self.golem_follow_set[str(golem.properties.qgraf_out)] = particle_names

      parameter_names = list(self.model["types"].keys())

      self.golem_follow_set[str(golem.properties.zero)] = parameter_names
      self.golem_follow_set[str(golem.properties.one)] = parameter_names
      self.golem_follow_set[str(golem.properties.model_options)] = \
            ["%s:" % name for name in parameter_names]

   def update(self, key, value):
      self.conf[key] = value

      if key == str(golem.properties.model):
         self.update_model()

      elif key == str(golem.properties.process_name):
         self.recommendations[golem.properties.process_path] = value

   def install_sigint_handler(self):
      def signal_handler(signal, frame):
         raise OSError("Interrupted by Ctrl+C.")
      signal.signal(signal.SIGINT, signal_handler)

   def uninstall_sigint_handler(self):
      signal.signal(signal.SIGINT, signal.SIG_DFL)

   def event(self, line):
      self.session.append(line)
      cmdline = line
      for commentchar in ["!", "#"]:
         if cmdline.strip().startswith(commentchar):
            return True

      tokens = [cmdline]
      for delim in ["=", " ", ":", ","]:
         new_tokens = []
         for token in tokens:
            t = token
            while delim in t:
               i = t.index(delim)
               if i > 0:
                  new_tokens.append(t[0:i])
               new_tokens.append(delim)
               t = t[i+1:]
            if len(t) > 0:
               new_tokens.append(t)
         tokens = new_tokens

      if len(tokens) == 0:
         return True

      keyword = tokens[0]
      args = tokens[1:]

      if keyword == ":":
         if all([arg == " " for arg in args]):
            # display history
            hist = self.get_history()
            lh = len(hist)
            digits = 0
            while lh > 0:
               digits += 1
               lh /= 10

            for i, h in enumerate(hist):
               print(("%" + str(digits) + "d: %s") % (i, h))
            return True
         else:
            sargs = ("".join(args)).strip()
            if sargs.startswith("!"):
               self.install_sigint_handler()
               try:
                  retcode = subprocess.call(sargs[1:], shell=True)
                  if retcode != 0:
                     print("Child process terminated with exit code %d."
                           % retcode)
               except OSError as e:
                  print("Child process terminated with an error: %s" % e)
               finally:
                  self.uninstall_sigint_handler()

               return True
            else:
               hist = self.get_history()
               try:
                  idx = int(sargs)
               except ValueError:
                  idx = -1
               if idx >= 0 and idx < len(hist):
                  print("Recalling %r ..." % hist[idx])
                  return self.event(hist[idx])
               else:
                  print("No such event in history.")
                  print("Type ':' for a list of history events.")
                  return True


      for cmd in COMMANDS:
         if str(cmd) == keyword:

            result = cmd.run(self, args)

            if len(self.recommendations) > 0:
               print("Your last command recommends the following settings:")
               for key,value in self.recommendations.items():
                  print("   %s: %s" % (key, value))

               print("Type 'accept' to accept the recommendations.")
               print("Any other command will ignore them.")

            self.golem_follow_set["accept"] = \
                list(self.recommendations.keys())

            self.afterevent()
            return result

      self.recommendations={}
      if any([arg != " " for arg in args]):
         # Set a parameter
         if args[0] in [" ", ":", "="]:
            args = args[1:]

         value = "".join(args)
         self.update(keyword, value)
         print(" %s=%s" % (keyword, value))

         self.afterevent()
         return True
      else:
         # Reading a parameter
         if keyword in self.conf:
            value = self.conf[keyword]
            print(" %s=%s" % (keyword, value))
            return True
         for prop in golem.properties.properties:
            if keyword == str(prop):
               print(" %s is currently not set." % keyword)
               if(prop.getType() == list):
                  pass
               elif prop.getDefault() is not None:
                  print(" Default: %s" % prop.getDefault())
               return True

      print("I don't know how to %r." % cmdline)
      print("Please, type 'help' for help.")
      return True

   def onexit(self):
      print("Thank you for using GoSam")

   def afterevent(self):
      if len(self.recommendations) > 0:
         print("Your last command recommends the following settings:")
         for key,value in self.recommendations.items():
            print("   %s: %s" % (key, value))

         print("Type 'accept' to accept the recommendations.")
         print("Any other command will ignore them.")

      self.golem_follow_set["accept"] = \
          list(self.recommendations.keys())


class Command:
   def __init__(self, name, help_text=None, followset=[]):

      self.name = name
      if help_text is None:
         self.help_text = [
               "No help available for command %r." % name
         ]
      else:
         self.help_text = help_text

      self.followset = followset

   def __str__(self):
      return self.name

   def help(self, *args):
      return self.help_text[:]

   def run(self, shell, args):
      print("Command '%s' has not been implemented yet." % self)
      shell.recommendations={}
      return True

class QUIT(Command):
   def __init__(self):
      Command.__init__(self, "quit",
            [
               "Quit the interactive session.",
               "",
               "This is equivalent to pressing CTRL+D (on UNIX)",
               "or CTRL+Z (on Windows)."
            ])

   def run(self, shell, args):
      shell.recommendations={}
      return False

class MAKE(Command):
   def __init__(self):
      Command.__init__(self, "make",
            [
               "Run make with the given target for the current process.",
               "Implemented targets are:",
               "  source          -- generate the sources for the process.",
               "  compile         -- compile the generated sources.",
               "  doc             -- generate documentation.",
               "  dist            -- generate a tar-ball.",
               "  clean           -- remove object files.",
               "  very-clean      -- remove objects and sources.",
               "",
               "Runs 'make compile' if no target has been given."
            ],
            
            followset=["source", "compile", "doc",
               "dist", "clean", "very-clean"])

   def run(self, shell, args):
      shell.recommendations = {}
      path = shell.conf[golem.properties.process_path]
      if path is None:
         path = ""

      if len(path.strip()) == 0:
         print("You need to set up the process path before you can run 'make'.")
         return True

      if(os.path.exists(os.path.join(path, "Makefile"))):
         target = "".join(args).strip()
         if len(target) == 0:
            target = "compile"

         shell.install_sigint_handler()
         try:
            retcode = subprocess.call("make -C %s " % path + target, shell=True)
            if retcode != 0:
               print("Make terminated with exit code %d." % retcode)
         except OSError as e:
            print("Make terminated with an error: %s" % e)
         finally:
            shell.uninstall_sigint_handler()
         return True
      else:
         print("There is no Makefile in your process path.")
         print("Did you run 'generate'?")
         return True

class RESET(Command):
   def __init__(self):
      Command.__init__(self, "reset",
            [
               "Set all parameters to their defaults and start a new session."
            ])

   def run(self, shell, args):
      shell.reset()
      print("Session has been cleared.")
      shell.recommendations={}
      return True

class WRITE(Command):
   def __init__(self):
      Command.__init__(self, "write",
            [
               "Write the current setup (variables only) to a process card.",
               "",
               "If no file name is given, the name of the card is derived",
               "from the variable process_name and is written to the current",
               "directory."
            ])

   def run(self, shell, args):
      conf = shell.conf
      shell.recommendations={}
      fname = "".join(args).strip()

      if len(fname) == 0:
         proc_name = conf[golem.properties.process_name].strip()
         if len(proc_name) > 0:
            fname = proc_name + ".in"
         else:
            fname = "golem.in"

      try:
         write_template_file(fname, conf)
         print("Process card stored in %r." % fname)
         return True
      except IOError as ex:
         print("Could not write to '%r':" % fname)
         print(str(ex))
         return True

class ACCEPT(Command):
   def __init__(self):
      Command.__init__(self, "accept",
            [
               "Accept the recommended settings suggested by the previous"
                + " command."
            ])

   def run(self, shell, args):
      accept_list = []
      for arg in args:
         if arg not in [" ", ":", "="]:
            accept_list.append(arg)
      if len(accept_list) == 0:
         accept_list.extend(shell.recommendations.keys())

      for key in accept_list:
         shell.update(key, shell.recommendations[key])
      shell.recommendations={}
      return True

class TOPDG(Command):
   def __init__(self):
      Command.__init__(self, "to.pdg",
            [
               "Converts the in and out states to PDG codes.",
            ])

   def run(self, shell, args):
      shell.recommendations={}
      
      pdgs = {}
      if "particles" in shell.model:
         particles = shell.model["particles"]

         for p in particles.values():
            pdgs[str(p)] = p.getPDGCode()

      if "mnemonics" in shell.model:
         mnemonics = shell.model["mnemonics"]

         for name, p in mnemonics.items():
            pdgs[name] = p.getPDGCode()

      lst = shell.conf.getProperty(golem.properties.qgraf_in)
      new_list = []
      for name in lst:
         if name in pdgs:
            new_list.append(str(pdgs[name]))
         else:
            new_list.append(name)
      shell.conf.setProperty(golem.properties.qgraf_in, ", ".join(new_list))
      lst = shell.conf.getProperty(golem.properties.qgraf_out)
      new_list = []
      for name in lst:
         if name in pdgs:
            new_list.append(str(pdgs[name]))
         else:
            new_list.append(name)
      shell.conf.setProperty(golem.properties.qgraf_out, ", ".join(new_list))

      return True

class SAVE(Command):
   def __init__(self):
      Command.__init__(self, "save",
            [
               "Saves the commands of this session into a file.",
               "See also: load, reset"
            ],
            followset = [" file"])

   def run(self, shell, args):
      shell.recommendations={}
      fname = "".join(args).strip()

      if len(fname) == 0:
         try:
            import Tkinter
            import tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            fname = tkFileDialog.asksaveasfilename(parent=root)
            root.destroy()
         except ImportError:
            print("Could not open dialog window.")
            print("File name required after 'save'")
            return True
         if len(fname) == 0:
            print("Nothing has been saved. User aborted action.")
            return True

      try:
         f = open(fname, 'w')
         for cmd in shell.session[:-1]:
            f.write(cmd + "\n")
         f.write("#" + shell.session[-1] + "\n")
         f.close()
         print("Current session stored in %r." % fname)
         return True
      except IOError as ex:
         print("Could not write to '%r':" % fname)
         print(str(ex))
         return True

class LOAD(Command):
   def __init__(self):
      Command.__init__(self, "load",
            [
               "Loads a previously saved session.",
               "See also: save, reset"
            ],
            followset = [" file"])

      self.stack = []

   def run(self, shell, args):
      shell.recommendations={}
      fname = "".join(args).strip()

      if len(fname) == 0:
         try:
            import Tkinter
            import tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            fname = tkFileDialog.askopenfilename(parent=root)
            root.destroy()
         except ImportError:
            print("Could not open dialog window.")
            print("File name required after 'load'")
            return True
         if len(fname) == 0:
            print("Nothing has been loaded. User aborted action.")
            return True

      if fname in self.stack:
         print("Prevented recursive loading of %r" % fname)
         return True

      rel_path = shell.relative_path
      try:
         self.stack.append(fname)
         shell.relative_path = os.path.dirname(fname)
         f = open(fname, 'r')
         lines = [line.rstrip() for line in f]
         result = shell.insert_text(*lines)
         print("Session restored from %r." % fname)
         return result
      except IOError as ex:
         print("Could not read session from '%r':" % fname)
         print(str(ex))
         return True
      finally:
         shell.relative_path = rel_path
         self.stack.pop()

class GENERATE(Command):
   def __init__(self):
      Command.__init__(self, "generate",
            [
               "Generates the files for the current process.",
               "",
               "This is equivalent to running gosam.py on",
               "the respective process card.",
               "",
               "If an argument is specified it must refer to the file name",
               "of an already generated process card."
            ],
            followset = [" file"])

   def prepare_process_card(self, defaults):
      result = golem.util.config.Properties()

      for prop in defaults:
         value=defaults[prop]
         if prop.startswith("+"):
            newkey=prop[1:]
            result[newkey] = value
         else:
            result[prop] = defaults[prop]

      result.decode()
      return result


   def run(self, shell, args):
      shell.recommendations={}
      fname = "".join(args).strip()
      conf = golem.util.config.Properties()

      if len(fname) == 0:
         conf.addAll(shell.conf)
         flag = False

         process_path = conf.getProperty(golem.properties.process_path, "") \
               .strip()
         process_name = conf.getProperty(golem.properties.process_name, "") \
               .strip()

         orders = golem.util.config.split_qgrafPower(",".join(map(str,conf.getListProperty(golem.properties.qgraf_power))))
         order = orders[0] if orders else []
         generate_lo = True
         generate_nlo = True
         if len(order) == 0:
            flag = True
         elif len(order) == 1:
            flag = True
         elif len(order) == 2:
            generate_nlo = False
         else:
            generate_lo = order[1].lower() != "none"

         extensions = [e.lower() for e in golem.properties.getExtensions(conf)]
         if generate_nlo:
            if not any([e in extensions for e in REDUCTION_EXTENSIONS]):
               shell.recommendations["+add.extensions"] = "samurai"
               flag=True

         if not conf["PSP_chk_method"] or conf["PSP_chk_method"].lower()=="automatic":
              conf["PSP_chk_method"] = "PoleRotation" if generate_lo_diagrams else "LoopInduced"

         if len(process_path) == 0:
            if len(process_name) == 0:
               rec = "."
            else:
               rec = process_name
            shell.recommendations[str(golem.properties.process_path)] = rec
            flag = True

         if flag:
            print("No output has been generated due to an insufficient setup.")
            return True

         ap = os.path.expandvars(process_path)
         ap = os.path.expanduser(process_path)
         ap = os.path.normpath(ap)
         if os.path.exists(ap):
            if not os.path.isdir(ap):
               print("Your specified process path %r is not a directory."
                     % process_path)
               return True
         else:
            print("Directory %r does not exist." % ap)
            ans = ""
            while not (ans.startswith("y") or ans.startswith("n")):
               ans = raw_input("Create it now (yes/no)? ").strip().lower()
            if ans.startswith("y"):
               try:
                  os.makedirs(ap)
               except OSError as ex:
                  print("Cannot create process directory: %s" % ex)
                  return True
         conf[golem.properties.process_path] = os.path.abspath(ap)
         fname = os.path.join(ap, "process.in")
         write_template_file(fname, conf)
         conf["setup-file"] = os.path.abspath(fname)
      else:
         if os.path.exists(fname):
            if not os.path.isfile(fname):
               # look for .golem.dir in that directory
               dir_info = read_golem_dir_file(fname)
               if "setup-file" in dir_info:
                  in_file = dir_info["setup-file"]
               else:
                  print("The argument %r seems not to refer to a" % fname
                        + "process file or directory.")
                  return True
            else:
               in_file = fname
         else:
            print("The file or directory %r does not exist." % arg)
            return True

         f = open(in_file, 'r')
         conf.load(f)
         f.close()
         conf["setup-file"] = os.path.abspath(in_file)

         orders = golem.util.config.split_qgrafPower(",".join(map(str,conf.getListProperty(golem.properties.qgraf_power))))
         order = orders[0] if orders else []

         generate_lo = True
         generate_nlo = True
         if len(order) == 0:
            flag = True
         elif len(order) == 1:
            flag = True
         elif len(order) == 2:
            generate_nlo = False
         else:
            generate_lo = order[1].lower() != "none"

      shell.install_sigint_handler()
      try:
         path = golem.util.tools.process_path(conf)
         proc_card = self.prepare_process_card(conf)
         workflow(proc_card)
         generate_process_files(proc_card, True)
      except golem.util.config.GolemConfigError as err:
         print("Code generation failed due to an error:")
         print(str(err))
         return True
      except OSError as err:
         print("Code generation failed due to an OS error:")
         print(str(err))
         return True
      finally:
         shell.uninstall_sigint_handler()

      info = proc_card["__info.count.tree__"]
      s = int(info)
      if info == 0:
         slo = "no tree diagrams"
      elif info == 1:
         slo = "one tree diagram"
      else:
         slo = "%s tree diagrams" % info

      info = proc_card["__info.count.virt__"]
      s += int(info)
      if info == 0:
         snlo = "no virt diagrams"
      elif info == 1:
         snlo = "one virt diagram"
      else:
         snlo = "%s loop diagrams" % info

      if s == 0:
         print("No diagrams were generated. Please, check your setup.")
      else:
         if generate_lo and generate_nlo:
            print("Generated %s and %s." % (slo, snlo))
         elif generate_lo:
            print("Generated %s." % (slo))
         else:
            print("Generated %s." % (snlo))
         print("Now you can run make")
      return True

class LIST(Command):
   def __init__(self):
      Command.__init__(self, "list",
            [
               "list variables: prints all currently defined variables.",
               "list commands:  prints all commands of the current session."
            ],
            followset = ["variables", "commands"])

   def list_commands(self, shell, WIDTH):
      for line in shell.session[:-1]:
         print(line)

   def list_variables(self, shell, WIDTH):
      def sortkey(s):
         if s.startswith("+"):
            return s[1:].lower()
         else:
            return s.lower()

      keys = [str(key) for key in shell.conf]
      keys.sort(key=sortkey)
      width = max(map(len, keys) + [0])
      fmt = "%-" + str(width) + "s %s"
      for key in keys:
         value = shell.conf[key]
         line = fmt % (key, value)
         while len(line) > 0:
            a = line[:WIDTH]
            b = line[WIDTH:]
            if len(b) > 0:
               print(a + "\\")
               line = "." * width + " " + b
            else:
               print(a)
               line = ""

   def run(self, shell, args):
      shell.recommendations = {}
      WIDTH=70
      listed = 0
      for arg in args:
         if arg.startswith("v"):
            self.list_variables(shell, WIDTH)
            listed += 1
            return True
         if arg.startswith("c"):
            self.list_commands(shell, WIDTH)
            listed += 1
            return True

      self.list_variables(shell, WIDTH)
      return True

class HELP(Command):
   def __init__(self):
      followset = []
      for cmd in COMMANDS:
         followset.append(str(cmd))

      for prop in golem.properties.properties:
         followset.append(str(prop))

      if "help" not in followset:
         followset.append("help")

      Command.__init__(self, "help",
            [
               "Prints a help screen for the given topic."
            ],
            followset=followset)

   def run(self, shell, args):
      shell.recommendations={}

      particle_dict = {}
      if "particles" in shell.model:
         particles = shell.model["particles"]

         for p in particles.values():
            particle_dict[str(p)] = p

      if "mnemonics" in shell.model:
         mnemonics = shell.model["mnemonics"]

         for name, p in mnemonics.items():
            particle_dict[name] = p

      if len(args) == 0:
         WIDTH = 70
         print("Add the name of one of the following topics")
         print("for more help.")

         print("")
         print("Commands:")
         line = ""
         lst = sorted(COMMANDS, key=str)
         for cmd in lst:
            if len(line) + len(str(cmd)) + 1 > WIDTH:
               print(line)
               line = ""
            line += " " + str(cmd)
         print(line)
         print("")

         print("Variables:")
         line = ""
         lst = sorted(golem.properties.properties, key=str)
         for prop in lst:
            if len(line) + len(str(prop)) + 1 > WIDTH:
               print(line)
               line = ""
            line += " " + str(prop)
         print(line)
         print("")

         print("Particles:")
         line = ""
         lst = sorted(particle_dict.keys())
         for prop in lst:
            if len(line) + len(str(prop)) + 1 > WIDTH:
               print(line)
               line = ""
            line += " " + str(prop)
         print(line)
         print("")
            
         print("Other Functionality:")
         print(" ':'    -- show command history.")
         print(" ':NN'  -- where NN is a number: recall history event.")
         print(" ':!'   -- run shell command, e.g. ':! ls'.")
         print("")
      else:
         hargs = []
         for arg in args:
            if arg in [":", "=", " "]:
               continue
            hargs.append(arg)

         help_topic = hargs[0]
      
         for cmd in COMMANDS:
            if help_topic == str(cmd):
               for line in cmd.help(hargs[1:]):
                  print(line)
               return True

         for prop in golem.properties.properties:
            if help_topic == str(prop):
               if prop.getType() != list:
                  print("Default: %r" % prop.getDefault())
                  print("")
               print(prop.getDescription())
               return True

         for name, particle in particle_dict.items():
            if help_topic == name:
               field = str(particle)
               if field in shell.model["latex_names"]:
                  print("LaTeX:                %s" 
                        % shell.model["latex_names"][field])
               print("PDG code:             %d" % particle.getPDGCode())
               spin2 = particle.getSpin()
               if spin2 % 2 == 0:
                  spin = str(spin2/2)
               else:
                  spin = str("%d/2" % spin2)
               print("Spin:                 %s" % spin)
               print("Color representation: %d" % particle.getColor())
               print("Mass:                 %s" % particle.getMass())
               print("Width:                %s" % particle.getWidth())
               print("QGraf name:           %s" % str(particle))
               print("Partner's QGraf name: %s" % particle.getPartner())
               return True

         print("No help available for %r." % help_topic)

      return True


COMMANDS = [
      QUIT(),
      MAKE(),
      RESET(),
      SAVE(),
      LOAD(),
      ACCEPT(),
      WRITE(),
      GENERATE(),
      LIST(),
      TOPDG()
      ]

COMMANDS.append(HELP())

