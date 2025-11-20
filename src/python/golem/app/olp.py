#!/usr/bin/python
# vim: ts=3:sw=3
import argparse
import logging
import os
import os.path
import re
import sys
from collections.abc import Sequence
from typing import TextIO, cast

import golem
import golem.installation
import golem.properties
import golem.util.tools
from golem.util.config import GolemConfigError, Properties, PropValue
from golem.util.main_misc import (
    find_config_files,
    generate_process_files,
    read_golem_dir_file,
    workflow,
    write_golem_dir_file,
    write_template_file,
)
from golem.util.olp import derive_output_name, process_order_file
from golem.util.olp_objects import OLPError
from golem.util.path import golem_path

logger = logging.getLogger(__name__)


def main(argv: list[str] = sys.argv):
    """
    This is the golem OLP client of GoSam for the initialization phase
    of the Binoth Accord.
    """
    parser = argparse.ArgumentParser(
        formatter_class=golem.util.tools.NLRHelpFormatter,
        description="GoSam OLP - An Automated One-Loop Matrix Element Generator",
        epilog="GoSam {} (rev {})\n".format(
            ".".join(map(str, golem.installation.GOLEM_VERSION)),
            golem.installation.GOLEM_REVISION,
        )
        + "Copyright (C) 2011-2025  The GoSam Collaboration\nThis is free software; see the "
        + "source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A "
        + "PARTICULAR PURPOSE.",
        usage="%(prog)s [options] order_file [order_file ...]",
    )
    _ = parser.add_argument(
        "-b",
        "--use-backslash",
        help="Allow the use of backslash escapes",
        action="store_true",
    )
    _ = parser.add_argument(
        "-c",
        "--config",
        help="Overlay default config files by the specified file",
        dest="config_files",
        action="extend",
        nargs="*",
        default=[],
    )
    _ = parser.add_argument(
        "-C",
        "--no-defaults",
        help="Do not build default configuration",
        action="store_true",
        dest="skip_default",
    )
    _ = parser.add_argument(
        "-D",
        "--destination",
        help="Choose output directory [default: .]",
        dest="dest_dir",
        default=".",
    )
    _ = parser.add_argument(
        "-e",
        "--use-single-quotes",
        help="Allow the use of single quotes",
        action="store_true",
    )
    _ = parser.add_argument(
        "-E",
        "--use-double-quotes",
        help="Allow the use of double quotes",
        action="store_true",
    )
    _ = parser.add_argument(
        "-f",
        "--force",
        help="Overwrite contract files without asking",
        action="store_true",
    )
    _ = parser.add_argument(
        "-i",
        "--ignore-case",
        help="Interpret the file case insensitive",
        action="store_true",
    )
    _ = parser.add_argument(
        "-I",
        "--ignore-empty-subprocess",
        help="Write vanishing amplitude for subprocess with no remaining tree-level diagrams",
        action="store_true",
        dest="ignore_empty_subprocess",
    )
    _ = parser.add_argument(
        "-j",
        "--jobs",
        help="Maximum number of workers used (requires the multiprocess package) [default: os.cpu_count()]",
        action="store",
        type=int,
        default=os.cpu_count(),
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
        "-M", "--mc", help="Set the name of the requesting MC program", default="any"
    )
    _ = parser.add_argument("-n", "--name", help="Add a name for this OLP", default="")
    _ = parser.add_argument(
        "--no-color", help="Disable colored terminal output", action="store_true"
    )
    _ = parser.add_argument(
        "-o",
        "--output-file",
        help="Specify the name of the contract file",
        default="%p%s.olc",
    )
    _ = parser.add_argument("-r", "--report", action="store_true")
    _ = parser.add_argument(
        "-t", "--templates", help="Set an alternative templates directory"
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
        "-x",
        "--ignore-unknown",
        help="Ignore unknown/unsupported options",
        action="store_true",
    )
    _ = parser.add_argument(
        "-X",
        "--no-crossings",
        help="Never generate crossings",
        action="store_false",
        dest="use_crossings",
    )
    _ = parser.add_argument(
        "-z",
        "--scratch",
        help="Overwrite all files including Makefile.conf, config.f90 etc",
        action="store_true",
        dest="from_scratch",
    )
    _ = parser.add_argument("order_file", nargs="+")

    cmd_args = parser.parse_args(argv[1:])
    golem.util.tools.setup_logging(
        cast(str, cmd_args.loglevel),
        cast(str, cmd_args.log_file),
        not cast(bool, cmd_args.no_color),
    )
    args = list(cast(Sequence[str], cmd_args.order_file))

    PAT_ASSIGN = re.compile(r"^[A-Za-z_.][-A-Za-z0-9_.]*[ \t]*=.*$", re.MULTILINE)
    cmd_properties: list[str] = []
    cmd_files: list[str] = []
    for arg in args:
        if PAT_ASSIGN.match(arg) is not None:
            cmd_properties.append(arg)
        else:
            cmd_files.append(arg)
    args = cmd_files

    print(
        "GoSam %s" % ".".join(map(str, golem.installation.GOLEM_VERSION))
        + " running in OLP mode"
    )

    logger.debug("      path: %r" % golem_path())

    defaults: list[Properties] = []
    default_files: list[str]
    if not cast(bool, cmd_args.skip_default):
        default_c, default_files = find_config_files()
        defaults.append(default_c)
    else:
        default_files = []

    for fname in cast(list[str], cmd_args.config_files):
        logger.info("Reading configuration file %s" % fname)
        try:
            cf = Properties()
            with open(fname, "r") as f:
                cf.load(f)
            defaults.append(cf)
            default_files.append(os.path.abspath(fname))
        except IOError:
            logger.critical("Configuration file %r could not be found." % (fname))
            sys.exit("GoSam terminated due to an error")
        except GolemConfigError as ex:
            logger.critical(
                "Configuration file %r could not be read: %s" % (fname, str(ex))
            )
            sys.exit("GoSam terminated due to an error")

    if len(cmd_properties) > 0:
        cmd_defaults = Properties()
        for assignment in cmd_properties:
            parts = assignment.split("=", 1)
            name = parts[0].strip()
            value = parts[1].strip()
            cmd_defaults.setProperty(name, value)
        defaults.append(cmd_defaults)

    default_conf = Properties()
    props = Properties()

    default_conf["extra_setup_file"] = default_files

    ## This fills in the defaults where no option is given:
    for p in golem.properties.properties:
        props.setProperty(str(p), cast(PropValue, default_conf.getProperty(p)))

    # set default options (BLHA specific)
    default_conf["olp.include_color_average"] = True
    default_conf["olp.include_helicity_average"] = True
    default_conf["olp.include_symmetry_factor"] = True
    default_conf["nlo_prefactors"] = 2

    default_conf.setProperty("__OLP_MODE__", "True")
    for c in defaults:
        default_conf += c

    if not default_conf["extensions"]:
        default_conf["extensions"] = cast(PropValue, props["extensions"])

    default_conf["ignore_empty_subprocess"] = cast(
        bool, cmd_args.ignore_empty_subprocess
    )
    default_conf["veto_crossings"] = False
    default_conf["n_jobs"] = cast(int, cmd_args.jobs)

    skipped = 0
    for arg in args:
        path = derive_output_name(arg, cast(str, cmd_args.dest_dir))
        path = os.path.expandvars(path)
        path = os.path.abspath(path)

        outp: TextIO
        if cmd_args.output_file == "-":
            outp = sys.stdout
            close_outp = False
        else:
            outp_name = derive_output_name(arg, cast(str, cmd_args.output_file))

            if os.path.exists(outp_name) and not cast(bool, cmd_args.force):
                logger.critical(
                    "Output file %r already exists. Please, remove file." % outp_name
                )
                sys.exit("GoSam terminated due to an error")
            outp = open(outp_name, "w")
            close_outp = True

        try:
            skipped += process_order_file(
                arg,
                outp,
                path,
                default_conf,
                cast(list[str], cmd_args.templates),
                double_quotes=cast(bool, cmd_args.use_double_quotes),
                single_quotes=cast(bool, cmd_args.use_single_quotes),
                backslash_escape=cast(bool, cmd_args.use_backslash),
                ignore_case=cast(bool, cmd_args.ignore_case),
                ignore_unknown=cast(bool, cmd_args.ignore_unknown),
                from_scratch=cast(bool, cmd_args.from_scratch),
                olp_process_name=cast(str, cmd_args.name),
                use_crossings=cast(bool, cmd_args.use_crossings),
                mc_name=cast(str, cmd_args.mc),
            )
        except GolemConfigError as ex:
            logger.warning(
                "Order file %r has been skipped because of errors: %s" % (arg, str(ex))
            )
            skipped += 1
        except IOError as ex:
            logger.warning("Order file %r could not be read." % arg)
            logger.warning("Error was: %s" % ex)
            skipped += 1
            continue
        finally:
            if close_outp:
                outp.close()

    if skipped > 0:
        logger.critical(
            "There were errors. %d file(s) skipped.\n" % skipped
            + "See .olc file for details."
        )
        sys.exit("GoSam terminated due to an error")
    if len(args) == 0:
        logger.warning("No input files have been processed.")

    logger.info("GoSam (OLP) is done.")
