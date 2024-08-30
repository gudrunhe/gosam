# vim: ts=3:sw=3:expandtab
import argparse
import sys
import os
import os.path
import getopt
import cProfile
import tempfile

import golem.shell
import golem.util.config
import golem.util.tools
from golem.util.config import GolemConfigError, Form
import golem.installation
import golem.util.constants
from golem.util.tools import error

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_misc import *

def main(parser, argv=sys.argv):
   """
   This is the main program of GoSam.
   """
   parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                    description="GoSam Standalone - An Automated One-Lop Matrix Element Generator",
                                    epilog="GoSam {} (rev {})\nCopyright (C) 2011-2024  The GoSam Collaboration\nThis is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.".format(
                                        ".".join(map(str, golem.installation.GOLEM_VERSION)),
                                        golem.installation.GOLEM_REVISION),
                                    usage="%(prog)s [options] config_file [config_file ...]"
                                    )
   parser.add_argument("-D", "--defaults",
                       help="Include system specific paths when creating a new template",
                       action="store_true",
                       dest="use_default_files"
                       )
   parser.add_argument("-f", "--format",
                       help="Use specified format for template file",
                       choices=["None", "LaTeX"],
                       dest="template_format"
                       )
   parser.add_argument("-i", "--interactive",
                       help="Start an interactive session (not supported anymore)",
                       action="store_true",
                       dest="interactive"
                       )
   parser.add_argument("-I", "--ignore-empty-subprocess",
                       help="Write vanishing amplitude for subprocess with no remaining tree-level diagrams",
                       action="store_true",
                       dest="ignore_empty_subprocess"
                       )
   parser.add_argument("-l", "--log-file", help="Write to a log file with the current level of verbosity")
   parser.add_argument("--loglevel",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                       default="WARNING",
                       help="Set the logging level"
                       )
   parser.add_argument("-m", "--merge",
                       help="Merge files into template",
                       action="extend",
                       dest="merge_files",
                       nargs="*"
                       )
   parser.add_argument("--olp", help="Switch to OLP mode, use '--olp --help' for more options.", action="store_true")
   parser.add_argument("-p", "--profile",
                       help="Generate profiling information in the process directory's 'pstats'",
                       action="store_true",
                       dest="generate_profile"
                       )
   parser.add_argument("-r", "--report", action="store_true")
   parser.add_argument("-t", "--template",
                       help="Writes configuration templates instead of processing them",
                       action="store_true",
                       dest="generate_templates"
                       )
   parser.add_argument("--version",
                       action="version",
                       version="GoSam {} (rev {})\nCopyright (C) 2011-2024  The GoSam Collaboration\nThis is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.".format(
                           ".".join(map(str, golem.installation.GOLEM_VERSION)), golem.installation.GOLEM_REVISION)
                       )
   parser.add_argument("-z", "--scratch",
                       help="Overwrite all files including Makefile.conf, config.f90 etc",
                       action="store_true",
                       dest="from_scratch"
                       )
   parser.add_argument("config_file", nargs="+")

   cmd_args = parser.parse_args(argv[1:])
   args = list(cmd_args.config_file)

   if cmd_args.report:
      golem.util.tools.POSTMORTEM_DO = True

   if cmd_args.interactive:
      interactive_session = golem.shell.GolemShell()
   else:
      interactive_session = None

   GOLEM_FULL = "GoSam %s" % ".".join(map(str,
      golem.installation.GOLEM_VERSION))

   message(GOLEM_FULL)

   golem.util.tools.check_script_name(argv[0])

   debug("      path: %r" % golem_path())

   if cmd_args.generate_templates:
      if cmd_args.use_default_files:
         defaults = find_config_files()
      else:
         defaults = golem.util.config.Properties()
      if len(args) == 0:
         args = ["template.in"]

      for mfile in cmd_args.merge_files:
         if os.path.exists(mfile):
            with open(mfile, 'r') as f:
               defaults.load(f)

      for fname in args:
         if os.path.exists(fname) and os.path.isdir(fname):
            error("Cannot write to %r which denotes a directory." % fname)
         else:
            write_template_file(fname, defaults, cmd_args.template_format)
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
      if cmd_args.merge_files:
         golem.util.tools.warning("Merge option only with --template usable.")
      for arg in args:
         # need the full system configuration
         # settings can be overridden in the input file
         c = find_config_files()

         if os.path.exists(arg):
            if not os.path.isfile(arg):
               # look for .golem.dir in that directory
               dir_info = read_golem_dir_file(arg)
               if "setup-file" in dir_info:
                  # args.append(dir_info["setup-file"])
                  in_file = dir_info["setup-file"]
               else:
                  warning("The directory %r contains no file %r." % (
                     arg, golem.util.constants.GOLEM_DIR_FILE_NAME),
                        "This directory has been skipped.")
                  continue
            else:
               in_file = arg
         else:
            warning("The file or directory %r does not exist." % arg,
               "This file or directory has been skipped.")
            continue

         f = open(in_file, 'r')

         temp_file_path=None

         try:
            # detect if the input file could be a double-escaped (*.rc) file
            if not f.readline().startswith("#!") and in_file.endswith(".rc"):
                 # merge into temporary template file
                 osfh, temp_file_path = tempfile.mkstemp(".gosam.in")
                 os.close(osfh)
                 f.seek(0)
                 c.load(f)
                 write_template_file(temp_file_path, c, cmd_args.template_format)
                 f.close()
                 # use the temporary file as new input file
                 f = open(temp_file_path,'r')
            f.seek(0)
            c.load(f)
            f.close()
         except GolemConfigError as err:
            golem.util.tools.error("Configuration file is not sound:", str(err))
         finally:
            if temp_file_path:
               os.unlink(temp_file_path)

         c.activate_subconfig(0)
         c["setup-file"] = os.path.abspath(in_file)
         c["golem.name"] = "GoSam"
         c["golem.version"] = ".".join(map(str, 
            golem.installation.GOLEM_VERSION))
         c["golem.full-name"] = GOLEM_FULL
         c["golem.revision"] = \
            golem.installation.GOLEM_REVISION
         c["ignore_empty_subprocess"] = cmd_args.ignore_empty_subprocess

         message("Processing %r" % arg)
         golem.util.tools.POSTMORTEM_CFG = c
         try:
            path = golem.util.tools.process_path(c)
            c.setProperty(golem.properties.process_path, path)
            if cmd_args.generate_profile:
               stats_file = os.path.join(path, "pstats")
               cProfile.run(
                     "workflow(c);generate_process_files(c, from_scratch)",
                     stats_file)
            else:
               workflow(c)
               generate_process_files(c, cmd_args.from_scratch)

            write_golem_dir_file(path, in_file, c)

         except GolemConfigError as err:
            golem.util.tools.error("Configuration file is not sound:", str(err))
      if len(args) == 0:
         golem.util.tools.warning("No input files have been processed.")

