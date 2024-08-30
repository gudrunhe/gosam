#!/usr/bin/python
# vim: ts=3:sw=3
import sys
import os
import os.path
import re
import argparse

import golem
import golem.util.tools

def main(argv=sys.argv):
	"""
	This is the golem OLP client of GoSam for the initialization phase
	of the Binoth Accord.
	"""
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
									 description="GoSam OLP - An Automated One-Lop Matrix Element Generator",
									 epilog="GoSam {} (rev {})\nCopyright (C) 2011-2024  The GoSam Collaboration\nThis is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.".format(
										 ".".join(map(str, golem.installation.GOLEM_VERSION)),
										 golem.installation.GOLEM_REVISION),
									 usage="%(prog)s [options] order_file [order_file ...]"
									 )
	parser.add_argument("-b", "--use-backslash", help="Allow the use of backslash escapes", action="store_true")
	parser.add_argument("-c", "--config",
						help="Overlay default config files by the specified file",
						dest="config_files",
						action="extend",
						nargs="*"
						)
	parser.add_argument("-C", "--no-defaults",
						help="Do not build default configuration",
						action="store_true",
						dest="skip_default"
						)
	parser.add_argument("-D", "--destination",
						help="Choose output directory [default: .]",
						dest="dest_dir",
						default="."
						)
	parser.add_argument("-e", "--use-single-quotes", help="Allow the use of single quotes", action="store_true")
	parser.add_argument("-E", "--use-double-quotes", help="Allow the use of double quotes", action="store_true")
	parser.add_argument("-f", "--format",
						help="Use specified format for template file",
						choices=["None", "LaTeX"],
						dest="template_format"
						)
	parser.add_argument("-i", "--ignore-case", help="Interpret the file case insensitive", action="store_true")
	parser.add_argument("-I", "--ignore-empty-subprocess",
						help="Write vanishing amplitude for subprocess with no remaining tree-level diagrams",
						action="store_true",
						dest="ignore_empty_subprocess"
						)
	parser.add_argument("-j", "--jobs",
						help="Maximum number of workers used (requires the multiprocess package) [default: os.cpu_count()]",
						action="store",
						type=int,
						default=os.cpu_count()
						)
	parser.add_argument("-l", "--log-file", help="Write to a log file with the current level of verbosity")
	parser.add_argument("--loglevel",
						choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
						default="WARNING",
						help="Set the logging level"
						)
	parser.add_argument("-M", "--mc", help="Set the name of the requesting MC program", default="any")
	parser.add_argument("-n", "--name", help="Add a name for this OLP", default="")
	parser.add_argument("-o", "--output-file", help="Specify the name of the contract file", default="%p%s.olc")
	parser.add_argument("-r", "--report", action="store_true")
	parser.add_argument("-t", "--templates", help="Set an alternative templates directory")
	parser.add_argument("--version",
						action="version",
						version="GoSam {} (rev {})\nCopyright (C) 2011-2024  The GoSam Collaboration\nThis is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.".format(
							".".join(map(str, golem.installation.GOLEM_VERSION)), golem.installation.GOLEM_REVISION)
						)
	parser.add_argument("-x", "--ignore-unknown", help="Ignore unknown/unsupported options", action="store_true")
	parser.add_argument("-X", "--no-crossings",
						help="Never generate crossings",
						action="store_false",
						dest="use_crossings"
						)
	parser.add_argument("-z", "--scratch",
						help="Overwrite all files including Makefile.conf, config.f90 etc",
						action="store_true",
						dest="from_scratch"
						)
	parser.add_argument("order_file", nargs="+")

	cmd_args = parser.parse_args(argv[1:])
	args = list(cmd_args.order_file)

	PAT_ASSIGN = re.compile(r'^[A-Za-z_.][-A-Za-z0-9_.]*[ \t]*=.*$',
			re.MULTILINE)
	#args = golem.util.tools.setup_arguments(CMD_LINE_ARGS, arg_handler,
	#		argv=argv)
	cmd_properties = []
	cmd_files = []
	for arg in args:
		if PAT_ASSIGN.match(arg) is not None:
			cmd_properties.append(arg)
		else:
			cmd_files.append(arg)
	args = cmd_files


	golem.util.tools.message("GoSam %s (OLP)" % ".".join(map(str,
		golem.util.main_misc.GOLEM_VERSION)))
	golem.util.tools.check_script_name(argv[0])
	golem.util.tools.debug("      path: %r" % golem.util.path.golem_path())
	
	defaults = []
	if not cmd_args.skip_default:
		defaults.append(golem.util.main_misc.find_config_files())

	for fname in cmd_args.config_files:
		golem.util.tools.message("Reading configuration file %s" % fname)
		try:
			cf = golem.util.config.Properties()
			with open(fname, 'r') as f:
				cf.load(f)
			defaults.append(cf)
		except golem.util.config.GolemConfigError as ex:
			golem.util.tools.error(
					"Configuration file %r could not be read: %s" % 
					(fname, str(ex)))

	if len(cmd_properties) > 0:
		cmd_defaults = golem.util.config.Properties()
		for assignment in cmd_properties:
			parts = assignment.split("=", 1)
			name  = parts[0].strip()
			value = parts[1].strip()
			cmd_defaults.setProperty(name, value)
		defaults.append(cmd_defaults)

	default_conf = golem.util.config.Properties()
	props = golem.util.config.Properties()

	## This fills in the defaults where no option is given:
	for p in golem.properties.properties:
		props.setProperty(str(p), default_conf.getProperty(p))

	# set default options (BLHA specific)
	default_conf["olp.include_color_average"] = True
	default_conf["olp.include_helicity_average"] = True
	default_conf["olp.include_symmetry_factor"] = True
	default_conf["nlo_prefactors"] = 2

	default_conf.setProperty("__OLP_MODE__","True")
	for c in defaults:
		default_conf += c

	if not default_conf["extensions"]:
		default_conf["extensions"]=props["extensions"]

	default_conf["ignore_empty_subprocess"] = cmd_args.ignore_empty_subprocess
	default_conf["veto_crossings"] = False
	default_conf["n_jobs"] = cmd_args.jobs

	skipped = 0
	for arg in args:
		path = golem.util.olp.derive_output_name(
				arg, cmd_args.dest_dir)
		path = os.path.expandvars(path)
		path = os.path.abspath(path)

		if cmd_args.output_file == "-":
			outp = sys.stdout
			close_outp = False
		else:
			outp_name = golem.util.olp.derive_output_name(
					arg, cmd_args.output_file)

			if os.path.exists(outp_name) and not cmd_args.force:
				golem.util.tools.error(
						"Output file %r already exists. Please, remove file." %
					outp_name)
			outp = open(outp_name, "w")
			close_outp = True

		try:
			skipped += golem.util.olp.process_order_file(
				arg, outp, path, default_conf, cmd_args.templates,
				double_quotes=cmd_args.use_double_quotes,
				single_quotes=cmd_args.use_single_quotes,
				backslash_escape=cmd_args.use_backslash,
				ignore_case=cmd_args.ignore_case,
				ignore_unknown=cmd_args.ignore_unknown,
				from_scratch=cmd_args.from_scratch,
				olp_process_name = cmd_args.name,
				use_crossings = cmd_args.use_crossings,
				mc_name = cmd_args.mc
			)
		except golem.util.olp_objects.OLPError as ex:
			golem.util.tools.warning(
					"Order file %r has been skipped because of errors: %s" %
					(arg, str(ex)))
			skipped += 1
		except IOError as ex:
			golem.util.tools.warning(
					"Order file %r could not be read." % arg)
			golem.util.tools.warning(
						"Error was: %s" % ex)
			skipped += 1
			continue
		finally:
			if close_outp:
				outp.close()

	if skipped > 0:
		golem.util.tools.error(
				"There were errors. %d file(s) skipped.\n" % skipped +
				"See .olc file for details.")
	if len(args) == 0:
		golem.util.tools.warning("No input files have been processed.")

	golem.util.tools.message("GoSam (OLP) is done.")
