#!/usr/bin/python
# vim: ts=3:sw=3
import sys
import os
import os.path
import re

import golem
import golem.util.tools

CMD_LINE_ARGS = golem.util.tools.DEFAULT_CMD_LINE_ARGS + [
		('c', "config=", "Overlay default config files by the specified file"),
		('C', "no-defaults", "Do not build default configuration"),
		('f', "force", "Overwrite contract files without asking"),
		('e', "use-single-quotes", "Allow the use of single quotes"),
		('E', "use-double-quotes", "Allow the use of double quotes"),
		('b', "use-backslash", "Allow the use of backslash escapes"),
		('i', "ignore-case", "Interpret the file case insensitive"),
		('x', "ignore-unknown", "Ignore unknown/unsupported options"),
		('X', "no-crossings", "Never generate crossings [default]"),
		('Y', "crossings", "Do generate crossings"),
		('o', "output-file=", "Specify name of contract file."),
		('D', "destination=", "Choose output directory [default: .]"),
		('n', "name=", "Add a name for this OLP"),
		('t', "templates=", "Set an alternative templates directory"),
		('M', "mc=", "Set the name of the requesting MC program"),
		('z', "scratch",
			"Overwrites all existing files including Makefile.conf etc")
	]

cmd_templates = ""
cmd_dest_dir = "."
cmd_config_files = []
cmd_skip_default = False
cmd_extensions = {
			"double_quotes": False,
			"single_quotes": False,
			"backslash_escape": False
		}
cmd_ignore_case = False
cmd_ignore_unknown = False
cmd_force = False
cmd_from_scratch = False
cmd_name = ""
cmd_use_crossings = True

cmd_mc = "any"

# %f -- full input file name (foo/baz/order.in)
# %F -- file name (order.in)
# %p -- path of input file (foo/baz/)
# %s -- stem (order)
# %e -- extension (.in)
cmd_output_file = "%p%s.olc"

def arg_handler(name, value=None):
	global cmd_dest_dir, cmd_config_files, cmd_skip_default, \
			cmd_extensions, cmd_ignore_case, cmd_ignore_unknown, \
			cmd_output_file, cmd_templates, cmd_force, \
			cmd_from_scratch, cmd_name, cmd_use_crossings, cmd_mc

	if name == 'destination':
		cmd_dest_dir = value
		return True
	elif name == 'scratch':
		cmd_from_scratch = True
		return True
	elif name == 'config':
		cmd_config_files.append(value)
		return True
	elif name == 'no-defaults':
		cmd_skip_default = True
		return True
	elif name == 'no-crossings':
		cmd_use_crossings = False
		return True
	elif name == 'crossings':
		cmd_use_crossings = True
		return True
	elif name == 'use-single-quotes':
		cmd_extensions["single_quotes"] = True
		return True
	elif name == 'use-double-quotes':
		cmd_extensions["double_quotes"] = True
		return True
	elif name == 'use-backslash':
		cmd_extensions["backslash_escape"] = True
		return True
	elif name == 'ignore-case':
		cmd_ignore_case = True
		return True
	elif name == 'ignore-unknown':
		cmd_ignore_unknown = True
		return True
	elif name == 'output-file':
		cmd_output_file = value
		return True
	elif name == 'templates':
		cmd_templates = value
		return True
	elif name == 'force':
		cmd_force = True
		return True
	elif name == 'name':
		cmd_name = value
		return True
	elif name == 'mc':
		cmd_mc = value
		return True
	return False

def main(argv=sys.argv):
	"""
	This is the golem OLP client of GoSam for the initialization phase
	of the Binoth Accord.

	Usage: gosam-init.py {options} {file or directory} {name=value}
	-h, --help           -- prints this help screen
	-d, --debug          -- prints out debug messages
	-v, --verbose        -- prints out status messages
	-w, --warn           -- prints out warnings and errors (default)
	-q, --quiet          -- suppresses warnings and messages
	-l, --log-file=<ARG> -- writes a log file with the current level of
									verbosity

	-------------------------------------------------------------------
	Static variables:

		CMD_LINE_ARGS  -- A list of accepted command line arguments, where
								each entry is a triple of the form
								(<short>, <long>, <description>)
	"""

	PAT_ASSIGN = re.compile(r'^[A-Za-z_.][-A-Za-z0-9_.]*[ \t]*=.*$',
			re.MULTILINE)
	args = golem.util.tools.setup_arguments(CMD_LINE_ARGS, arg_handler,
			argv=argv)
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
	if not cmd_skip_default:
		defaults.append(golem.util.main_misc.find_config_files())

	for fname in cmd_config_files:
		golem.util.tools.message("Reading configuration file %s" % fname)
		try:
			cf = golem.util.config.Properties()
			f = open(fname, 'r')
			cf.load(f)
			f.close()
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

	skipped = 0
	for arg in args:
		path = golem.util.olp.derive_output_name(
				arg, cmd_dest_dir)
		path = os.path.expandvars(path)
		path = os.path.abspath(path)

		if cmd_output_file == "-":
			outp = sys.stdout
			close_outp = False
		else:
			outp_name = golem.util.olp.derive_output_name(
					arg, cmd_output_file)

			if os.path.exists(outp_name) and not cmd_force:
				golem.util.tools.error(
						"Output file %r already exists. Please, remove file." %
					outp_name)
			outp = open(outp_name, "w")
			close_outp = True

		try:
			skipped += golem.util.olp.process_order_file(
				arg, outp, path, default_conf, cmd_templates,
				double_quotes=cmd_extensions["double_quotes"],
				single_quotes=cmd_extensions["single_quotes"],
				backslash_escape=cmd_extensions["backslash_escape"],
				ignore_case=cmd_ignore_case,
				ignore_unknown=cmd_ignore_unknown,
				from_scratch=cmd_from_scratch,
				olp_process_name = cmd_name,
				use_crossings = cmd_use_crossings,
				mc_name = cmd_mc
			)
		except golem.util.olp_objects.OLPError as ex:
			golem.util.tools.warning(
					"Order file %r has been skipped because of errors: %s" %
					(arg, ex.message))
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
