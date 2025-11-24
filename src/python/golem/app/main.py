# vim: ts=3:sw=3:expandtab
import argparse
import cProfile
import logging
import os
import sys
import tempfile
from argparse import ArgumentParser
from collections.abc import Sequence
from typing import cast

import golem.installation
import golem.properties
import golem.util.config
import golem.util.constants
import golem.util.tools
from golem.util.config import GolemConfigError

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_misc import (
    find_config_files,
    generate_process_files,
    read_golem_dir_file,
    workflow,
    write_golem_dir_file,
    write_template_file,
)
from golem.util.path import golem_path

logger = logging.getLogger(__name__)


def main(argv: list[str] = sys.argv):
    """
    This is the main program of GoSam.
    """
    parser = argparse.ArgumentParser(
        formatter_class=golem.util.tools.NLRHelpFormatter,
        description="GoSam Standalone - An Automated One-Loop Matrix Element Generator",
        epilog="GoSam {} (rev {})\n".format(
            ".".join(map(str, golem.installation.GOLEM_VERSION)),
            golem.installation.GOLEM_REVISION,
        )
        + "Copyright (C) 2011-2025  The GoSam Collaboration\nThis is free software; see the "
        + "source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A "
        + "PARTICULAR PURPOSE.",
        usage="%(prog)s [options] config_file [config_file ...]",
    )
    _ = parser.add_argument(
        "-D",
        "--defaults",
        help="Include system specific paths when creating a new template",
        action="store_true",
        dest="use_default_files",
    )
    _ = parser.add_argument(
        "-f",
        "--format",
        help="Use specified format for template file",
        choices=["None", "LaTeX"],
        dest="template_format",
    )
    _ = parser.add_argument(
        "-I",
        "--ignore-empty-subprocess",
        help="Write vanishing amplitude for subprocess with no remaining tree-level diagrams",
        action="store_true",
        dest="ignore_empty_subprocess",
    )
    _ = parser.add_argument(
        "-l",
        "--log-file",
        help="Write to a log file with the current level of verbosity",
    )
    _ = parser.add_argument(
        "--loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level",
    )
    _ = parser.add_argument(
        "-m",
        "--merge",
        help="Merge files into template",
        action="extend",
        dest="merge_files",
        nargs="*",
        default=[],
    )
    _ = parser.add_argument(
        "--no-color", help="Disable colored terminal output", action="store_true"
    )
    _ = parser.add_argument(
        "--olp",
        help="Switch to OLP mode, use '--olp --help' for more options.",
        action="store_true",
    )
    _ = parser.add_argument(
        "-p",
        "--profile",
        help="Generate profiling information in the process directory's 'pstats'",
        action="store_true",
        dest="generate_profile",
    )
    _ = parser.add_argument("-r", "--report", action="store_true")
    _ = parser.add_argument(
        "-t",
        "--template",
        help="Writes configuration templates instead of processing them",
        action="store_true",
        dest="generate_templates",
    )
    _ = parser.add_argument(
        "--version",
        action="version",
        version="GoSam {} (rev {})\n".format(
            ".".join(map(str, golem.installation.GOLEM_VERSION)),
            golem.installation.GOLEM_REVISION,
        )
        + "Copyright (C) 2011-2025  The GoSam Collaboration\nThis is free software; see the "
        + "source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A "
        + "PARTICULAR PURPOSE.",
    )
    _ = parser.add_argument(
        "-z",
        "--scratch",
        help="Overwrite all files including Makefile.conf, config.f90 etc",
        action="store_true",
        dest="from_scratch",
    )
    _ = parser.add_argument("config_file", nargs="+")

    cmd_args = parser.parse_args(argv[1:])
    golem.util.tools.setup_logging(
        cast(str, cmd_args.loglevel),
        cast(str, cmd_args.log_file),
        not cast(bool, cmd_args.no_color),
    )
    args = list(cast(Sequence[str], cmd_args.config_file))

    if cast(bool, cmd_args.report):
        golem.util.tools.POSTMORTEM_DO = True

    GOLEM_FULL = "GoSam %s" % ".".join(map(str, golem.installation.GOLEM_VERSION))

    print(GOLEM_FULL + " running in standalone mode")

    logger.debug("      path: %r" % golem_path())

    if cast(bool, cmd_args.generate_templates):
        if cast(bool, cmd_args.use_default_files):
            defaults, _ = find_config_files()
        else:
            defaults = golem.util.config.Properties()
        if len(args) == 0:
            args = ["template.in"]

        for mfile in cast(Sequence[str], cmd_args.merge_files):
            if os.path.exists(mfile):
                with open(mfile, "r") as f:
                    defaults.load(f)

        for fname in args:
            if os.path.exists(fname) and os.path.isdir(fname):
                logger.critical("Cannot write to %r which denotes a directory." % fname)
                sys.exit("GoSam terminated due to an error")
            else:
                write_template_file(
                    fname, defaults, cast(str, cmd_args.template_format)
                )
    else:
        if len(args) == 0:
            dir_info = read_golem_dir_file(os.getcwd())
            if "setup-file" in dir_info:
                args.append(cast(str, dir_info["setup-file"]))
        if cast(bool, cmd_args.merge_files):
            logger.warning("Merge option only with --template usable.")
        for arg in args:
            # need the full system configuration
            # settings can be overridden in the input file
            c, _ = find_config_files()

            if os.path.exists(arg):
                if not os.path.isfile(arg):
                    # look for .golem.dir in that directory
                    dir_info = read_golem_dir_file(arg)
                    if "setup-file" in dir_info:
                        # args.append(dir_info["setup-file"])
                        in_file = cast(str, dir_info["setup-file"])
                    else:
                        logger.warning(
                            "The directory %r contains no file %r.\nThis directory has been skipped."
                            % (arg, golem.util.constants.GOLEM_DIR_FILE_NAME)
                        )
                        continue
                else:
                    in_file = arg
            else:
                logger.warning(
                    "The file or directory %r does not exist.\nThis file or directory has been skipped."
                    % arg
                )
                continue

            f = open(in_file, "r")

            temp_file_path = None

            try:
                # detect if the input file could be a double-escaped (*.rc) file
                if not f.readline().startswith("#!") and in_file.endswith(".rc"):
                    # merge into temporary template file
                    osfh, temp_file_path = tempfile.mkstemp(".gosam.in")
                    os.close(osfh)
                    _ = f.seek(0)
                    c.load(f)
                    write_template_file(
                        temp_file_path, c, cast(str, cmd_args.template_format)
                    )
                    f.close()
                    # use the temporary file as new input file
                    f = open(temp_file_path, "r")
                _ = f.seek(0)
                c.load(f)
                f.close()
            except GolemConfigError as err:
                logger.critical("Configuration file is not sound: {}".format(str(err)))
                sys.exit("GoSam terminated due to an error")
            finally:
                if temp_file_path:
                    os.unlink(temp_file_path)

            c.activate_subconfig(0)
            c["setup-file"] = os.path.abspath(in_file)
            c["golem.name"] = "GoSam"
            c["golem.version"] = ".".join(map(str, golem.installation.GOLEM_VERSION))
            c["golem.full-name"] = GOLEM_FULL
            c["golem.revision"] = golem.installation.GOLEM_REVISION
            c["ignore_empty_subprocess"] = cast(bool, cmd_args.ignore_empty_subprocess)

            logger.info("Processing %r" % arg)
            golem.util.tools.POSTMORTEM_CFG = c
            try:
                path = golem.util.tools.process_path(c)
                c.setProperty(golem.properties.process_path, path)
                if cast(bool, cmd_args.generate_profile):
                    stats_file = os.path.join(path, "pstats")
                    cProfile.run(
                        "workflow(c);generate_process_files(c, from_scratch)",
                        stats_file,
                    )
                else:
                    workflow(c)
                    generate_process_files(c, cast(bool, cmd_args.from_scratch))

                write_golem_dir_file(path, in_file, c)

            except GolemConfigError as err:
                logger.critical("Configuration file is not sound: {}".format(str(err)))
                sys.exit("GoSam terminated due to an error")
        if len(args) == 0:
            logger.warning("No input files have been processed.")
