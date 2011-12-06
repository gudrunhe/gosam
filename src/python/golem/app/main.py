# vim: ts=3:sw=3:expandtab

import sys
import os
import os.path
import getopt
import cProfile

import golem.shell
import golem.util.config
import golem.util.tools
from golem.util.config import GolemConfigError
import golem.installation

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_misc import *

CMD_LINE_ARGS = golem.util.tools.DEFAULT_CMD_LINE_ARGS + [
      ('z', "scratch",
         "overwrites all files including Makefile.conf, config.f90 etc"),
      ('t', "template",
         "writes configuration templates instead of processing them"),
      ('p', "profile",
         "generates profiling information in the process directory's 'pstats'"),
      ('N', "no-defaults",
         "do not try to find configuration files in the default locations"),
      ('f', "format=",
         "use specified format for template file"),
      ('m', "merge=",
         "merge file into template"),
      ('i', "interactive",
         "run an interactive session")
   ]

generate_templates = False
use_default_files = True
template_format = None
generate_profile = False
from_scratch = False
merge_files = []
interactive_session = None

def arg_handler(name, value=None):
   global generate_templates, use_default_files, template_format, \
         generate_profile, from_scratch, merge_files, \
         interactive_session, draw_diagrams
   if name == "scratch":
      from_scratch = True
      return True
   if name == "template":
      generate_templates = True
      return True
   if name == "merge":
      merge_files.append(value)
      return True
   if name == "profile":
      generate_profile = True
      return True
   if name == "no-defaults":
      use_default_files = False
      return True
   if name == "format":
      if value in ["LaTeX"]:
         template_format = value
         return True
      else:
         return False
   if name == "interactive":
      interactive_session = golem.shell.GolemShell()
      return True

def main(argv=sys.argv):
   """
   This is the main program of GoSam.

   Usage: golem-main.py {options} [--template] {file or directory}
   -h, --help           -- prints this help screen
   -d, --debug          -- prints out debug messages
   -p, --profile        -- generates profiling information
   -v, --verbose        -- prints out status messages
   -w, --warn           -- prints out warnings and errors (default)
   -q, --quiet          -- suppresses warnings and messages
   -l, --log-file=<ARG> -- writes a log file with the current level of
                           verbosity
   -t, --template       -- writes configuration templates
                           instead of processing them
   -m, --merge=<ARG>    -- when producing template files, merges the contents
                           of that file into the template
   -N, --no-defaults    -- do not use a default configuration file
                           when creating a new template
   -f, --format=<ARG>   -- use specified format when writing template files
   -z, --scratch        -- overwrite all files
   -i, --interactive    -- start an interactive interface
   -y, --no-pyxodraw    -- do not attempt to draw diagrams.

   -------------------------------------------------------------------
   Static variables:

      CMD_LINE_ARGS  -- A list of accepted command line arguments, where
                        each entry is a triple of the form
                        (<short>, <long>, <description>)
   """

   args = golem.util.tools.setup_arguments(CMD_LINE_ARGS, arg_handler,
         argv=argv)

   GOLEM_FULL = "GoSam %s" % ".".join(map(str,
      golem.installation.GOLEM_VERSION))

   message(GOLEM_FULL)

   golem.util.tools.check_script_name(argv[0])

   debug("      path: %r" % golem_path())

   if generate_templates:
      if use_default_files:
         defaults = find_config_files()
      else:
         defaults = golem.util.config.Properties()
      if len(args) == 0:
         args = ["template.in"]

      for mfile in merge_files:
         if os.path.exists(mfile):
            f = open(mfile, 'r')
            defaults.load(f)
            f.close()

      for fname in args:
         if os.path.exists(fname) and os.path.isdir(fname):
            error("Cannot write to %r which denotes a directory." % fname)
         else:
            write_template_file(fname, defaults, template_format)
   elif interactive_session is not None:
      flag = True
      for arg in args:
         flag = interactive_session.event("load %s" % arg)
         if not flag:
            interactive_session.reset()
      if flag:
         interactive_session.run()
   else:
      if len(args) == 0:
         dir_info = read_golem_dir_file(os.getcwd())
         if "setup-file" in dir_info:
            args.append(dir_info["setup-file"])
      for arg in args:
         c = golem.util.config.Properties()

         if os.path.exists(arg):
            if not os.path.isfile(arg):
               # look for .golem.dir in that directory
               dir_info = read_golem_dir_file(arg)
               if "setup-file" in dir_info:
                  # args.append(dir_info["setup-file"])
                  in_file = dir_info["setup-file"]
               else:
                  warning("The directory %r contains no file %r." % (
                     arg, GOLEM_DIR_FILE_NAME),
                        "This directory has been skipped.")
                  continue
            else:
               in_file = arg
         else:
            warning("The file or directory %r does not exist." % arg,
               "This file or directory has been skipped.")
            continue

         f = open(in_file, 'r')
         c.load(f)
         f.close()
         c["setup-file"] = os.path.abspath(in_file)
         c["golem.name"] = "GoSam"
         c["golem.version"] = ".".join(map(str, 
            golem.installation.GOLEM_VERSION))
         c["golem.full-name"] = GOLEM_FULL

         message("Processing %r" % arg)
         try:
            path = golem.util.tools.process_path(c)
            c.setProperty(golem.properties.process_path, path)
            if generate_profile:
               stats_file = os.path.join(path, "pstats")
               cProfile.run(
                     "workflow(c);generate_process_files(c, from_scratch)",
                     stats_file)
            else:
               workflow(c)
               generate_process_files(c, from_scratch)

            write_golem_dir_file(path, in_file, c)

         except GolemConfigError as err:
            golem.util.tools.error("Configuration file is not sound:", str(err))
      if len(args) == 0:
         golem.util.tools.warning("No input files have been processed.")

