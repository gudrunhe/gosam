# vim: ts=3:sw=3
import sys
import os
import os.path
import imp

from time import gmtime, strftime

import golem.algorithms.mandelstam
import golem.algorithms.formfactors
import golem.util.config
import golem.util.tools
import golem.util.parser
import golem.properties
import golem.topolopy.functions
import golem.topolopy.objects
import golem.util.main_qgraf
import golem.util.constants as consts

import golem.templates.xmltemplates

from golem.util.path import golem_path
from golem.util.tools import copy_file, \
		debug, message, warning, \
		generate_particle_lists

from golem.util.config import GolemConfigError

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_qgraf import *
from golem.util.main_process import *
from golem.installation import GOLEM_VERSION

def create_ff_files(conf, in_particles, out_particles):
	legs = len(in_particles) + len(out_particles)
	path = golem.util.tools.process_path(conf)

	for n in range(1, legs + 1):
		f = open(os.path.join(path, "ff-%d.hh" % n), "w")
		p = golem.algorithms.formfactors.FormFactorPrinter(f)

		f.write("* vim: ts=3:sw=3\n")
		ffset = []
		for r in range(n + 1):
			f.write("*---#[ Procedure TI%dr%d :\n" % (n, r))
			ffs = p.generate(n, r)
			ffset.extend(ffs)
			f.write("*---#] Procedure TI%dr%d :\n" % (n, r))

		f.write("*---#[ Set of Form Factors :\n")
		if len(ffset) > 0:
			f.write("Set FormFactors%d : " % n)
			f.write(",\n\t".join(
					[", ".join(ffset[i:i+10]) for i in range(0, len(ffset), 8)]))
			f.write(";\n")
		f.write("*---#] Set of Form Factors :\n")
		f.close()

def generate_process_files(conf, from_scratch=False):
	"""
	This routine is a wrapper around anything that needs to be done
	for creating a new process.
	"""
	golem.properties.setInternals(conf)

	path = golem.util.tools.process_path(conf)

	templates = conf.getProperty(golem.properties.template_path)
	templates = os.path.expandvars(templates)

	if templates is None or len(templates) == 0:
		templates = golem_path("templates")

	extensions = golem.properties.getExtensions(conf)

	# properties will be filled later:
	props = golem.util.config.Properties()

	# This fills in the defaults where no option is given:
	for p in golem.properties.properties:
		props.setProperty(str(p), conf.getProperty(p))

	for name in conf:
		props[name] = conf[name]

	# OBSOLETE:
	## we only need the ff-<n>.hh files if we create the virtual amplitude
	## and if we use the extension 'golem95':
	##flag_create_ff_files = conf.getBooleanProperty("generate_nlo_virt") \
	##		and "golem95" in extensions
	flag_create_ff_files = False

	if not os.path.exists(path):
		raise GolemConfigError("Process path does not exist: %s" % path)

	in_particles, out_particles = \
			generate_particle_lists(conf)

	# Obtain the files required by QGraf from the template file.
	golem.templates.xmltemplates.transform_templates(templates, path, props,
			conf = conf,
			in_particles = in_particles,
			out_particles = out_particles,
			user = "qgraf",
			from_scratch=from_scratch)

	# First thing to be done because the Makefiles
	# Need to know the number of diagrams.
	run_qgraf(conf, in_particles, out_particles)

	# Run the new analyzer:
	message("Analyzing diagrams")
	# keep_tree, keep_virt, loopcache, tree_signs, tree_flows, flags = \
	keep_tree, keep_virt, loopcache, tree_signs, flags = \
			run_analyzer(path, conf, in_particles, out_particles)

	props.setProperty("topolopy.keep.tree", ",".join(map(str, keep_tree)))
	props.setProperty("topolopy.keep.virt", ",".join(map(str, keep_virt)))
	props.setProperty("topolopy.count.tree", len(keep_tree))
	props.setProperty("topolopy.count.virt", len(keep_virt))
	props.setProperty("templates", templates)
	props.setProperty("process_path", path)
	props.setProperty("max_rank", conf["__max_rank__"])

	conf["__info.count.tree__"] = len(keep_tree)
	conf["__info.count.virt__"] = len(keep_virt)

	for key, value in golem.util.tools.derive_coupling_names(conf).items():
		props.setProperty("%s_COUPLING_NAME" % key, value)

	# Create and populate subdirectories
	golem.templates.xmltemplates.transform_templates(templates, path, props,
			conf = conf,
			in_particles = in_particles,
			out_particles = out_particles,
			user = "main",
			from_scratch=from_scratch,
			loopcache=loopcache,
			tree_signs=tree_signs,
			# tree_flows=tree_flows,
			heavy_quarks=filter(lambda p: len(p.strip()) > 0,
				conf.getListProperty("__heavy_quarks__")),
			lo_flags = flags[0],
			nlo_flags = flags[1])

	create_process_hh(conf, in_particles, out_particles)
	generate_func_txt(conf)

	if flag_create_ff_files:
		create_ff_files(conf, in_particles, out_particles)

def find_config_files():
	"""
	Searches for configuration files in the default locations.
	These are used to fill the fields of newly created input
	files by preferred defaults.

	The procedure looks in the following locations:
		<golem path>
		<user's home>
		<working directory>
	
	The follwing file names are considered configuration files
		.gosam
		.golem
		gosam.in
		golem.in
		gosam.conf
		golem.conf
	"""
	props = golem.util.config.Properties()
	directories = [golem_path(), golem.util.path.get_homedir(), os.getcwd()]
	files = [".gosam", ".golem",
			"gosam.in", "golem.in",
			"gosam.conf", "golem.conf"]
	for dir in directories:
		for file in files:
			full_name = os.path.join(dir, file)
			if os.path.exists(full_name):
				f = open(full_name, 'r')
				props.load(f)
				f.close()
	return props

def write_template_file(fname, defaults, format=None):
	"""
	Creates a template file using the given default-configuration
	if present.

	fname --- name of the file to be created
	"""
	width = 70 # line width
	tw = 3     # tab width

	message("Writing template file %r" % fname)
	script = sys.argv[0]
	f = open(fname, "w")
	if format is None:
		f.write("#!/bin/env " + script + "\n")
	elif format == "LaTeX":
		f.write("\\begin{description}\n")
	else:
		raise GolemConfigError(
				"Unknown Format in write_template_file(..., %r)" % format)

	if format is None:
		for prop in defaults:
			if prop.startswith("$"):
				value=defaults[prop]
				f.write("%s=%s\n" % (prop, value))
	for prop in golem.properties.properties:
		if prop.isExperimental():
			continue

		if prop.getType() == str:
			stype = "text"
		elif prop.getType() == int:
			stype = "integer number"
		elif prop.getType() == bool:
			stype = "true/false"
		elif prop.getType() == list:
			stype = "comma separated list"
		else:
			stype = str(prop.getType())

		if format is None:
			text = "### %s (%s) " % (prop, stype)
			if len(text) < width:
				f.write("%s%s\n" % (text, "#" * (width-len(text))))
			else:
				f.write("%s\n" % text)
		elif format == "LaTeX":
			f.write("\\item[\\texttt{%s}] (\\textit{%s})\n" % 
					(str(prop).replace("_", "\\_"), stype.replace("_", "\\_")))

		if format is None:
			for line in prop.getDescription().splitlines(False):
				text = "# %s" % (line.expandtabs(tw))
				if len(text) < width - 2:
					f.write("%s%s #\n" % (text, " " * ((width-2)-len(text))))
				else:
					f.write("%s\n" % text)
			f.write("#" * width + "\n")
		elif format == "LaTeX":
			f.write("\\begin{verbatim}\n")
			first = True
			for line in prop.getDescription().splitlines(False):
				if first:
					indent = len(line) - len(line.lstrip())
					first = False
					prev_empty = False

				text = line[indent:].rstrip()

				if text.strip() == "":
					prev_empty = True
				else:
					if prev_empty:
						f.write("\n")
					f.write(line[indent:].rstrip() + "\n")
					prev_empty = False
			f.write("\\end{verbatim}\n")

		if format is None:
			if str(prop) in defaults.propertyNames():
				value = defaults.getProperty(prop)
				if isinstance(value, list):
					value=",".join(value)
				f.write("%s=%s\n" % (str(prop), value))
			elif prop.getDefault() is None:
				f.write("# %s=\n" % prop)
			else:
				f.write("# %s=%s\n" % (prop, prop.getDefault()))
			f.write("\n")
		elif format == "LaTeX":
			if prop.getDefault() is not None:
				value = str(prop.getDefault())
				if len(value) > 0:
					f.write("Default: \\verb|%s|\n" % value)

	if format is None:
		for prop in defaults:
			if prop.startswith("+"):
				value=defaults[prop]
				newkey=prop[1:]
				f.write("%s=%s\n" % (newkey, value))
			elif prop.endswith(".extensions"):
				value=defaults[prop]
				f.write("%s=%s\n" % (prop, value))
	elif format == "LaTeX":
		f.write("\\end{description}\n")
	f.close()

def read_golem_dir_file(path):
	"""
	Looks for the file .golem.dir under the given path.
	"""
	result = golem.util.config.Properties()

	dir_file = os.path.join(path, consts.GOLEM_DIR_FILE_NAME)
	if os.path.exists(dir_file):
		f = open(dir_file, 'r')
		result.load(f)
		f.close()

		ver = map(int,result["golem-version"].split("."))
		for gv, v in zip(GOLEM_VERSION + [0]*5, ver):
			if gv > v:
				raise GolemConfigError(
						"This directory has been generated with an older version "+
						"of golem (%s).\n" % result["golem-version"]+
						"Please, remove all files, including '.golem.dir' "+
						"and rerun golem-main.py.")
			elif gv < v:
				raise GolemConfigError(
						"This directory has been generated with a newer version "+
						"of golem (%s).\n" % result["golem-version"]+
						"Please, remove all files, including '.golem.dir' "+
						"and rerun golem-main.py.")

	return result

def write_golem_dir_file(path, fname, conf):
	"""
	Writes .golem.dir which will allow us later to identify
	this directory as a golem directory and to logically
	link it with the original setup file.

	PARAMETER

	path -- the path where the file should be located
	fname -- the name of the setup file used.
	"""
	dir_info = golem.util.config.Properties()
	dir_info["setup-file"] = os.path.abspath(fname)
	dir_info["golem-version"] = ".".join(map(str, GOLEM_VERSION))
	dir_info["process-name"] = conf.getProperty(golem.properties.process_name)
	dir_info["time-stamp"] = \
			strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

	f = open(os.path.join(path, consts.GOLEM_DIR_FILE_NAME), 'w')
	dir_info.store(f, "Do not remove this file!")
	f.close()

def check_dont_overwrite(conf):
	path = golem.util.tools.process_path(conf)

	dir_info = read_golem_dir_file(path)

	if("setup-file" in dir_info):
		setup_file_conf = conf["setup-file"]
		setup_file_dir = dir_info["setup-file"]

		if not os.path.exists(setup_file_dir):
			raise GolemConfigError(
					"The directory %r contains files created by %r, " %
						(path, setup_file_dir) +
					"which does no longer exist.\n" +
					"If you actually want to overwrite these files " +
					"you need to remove the file %r in that directory." % 
						consts.GOLEM_DIR_FILE_NAME)

		if not os.path.samefile(setup_file_conf, setup_file_dir):
			raise GolemConfigError(
					"The directory %r contains files created by %r, " %
						(path, setup_file_dir) +
					"which is not the same as %r.\n" % setup_file_conf +
					"If you actually want to overwrite these files " +
					"you need to remove the file %r in that directory." % 
						consts.GOLEM_DIR_FILE_NAME)

def workflow(conf):
	"""
	Creates additional properties which determine the workflow
	later in the program.

	Also does some checks whether the combination of properties
	makes sense.

	The additional properties are:

	generate_nlo_virt
	generate_lo_diagrams
	generate_uv_counterterms
	"""
	ini = conf.getProperty(golem.properties.qgraf_in)
	fin = conf.getProperty(golem.properties.qgraf_out)
	path = golem.util.tools.process_path(conf)

	powers = conf.getProperty(golem.properties.qgraf_power)
	renorm = conf.getProperty(golem.properties.renorm)
	templates = conf.getProperty(golem.properties.template_path)
	templates = os.path.expandvars(templates)
	qgraf_options = conf.getProperty(golem.properties.qgraf_options)

	r2only = conf.getProperty(golem.properties.r2).lower().strip() == "only"

	# Check if path exists. If it doesn't, raise an exception
	if not os.path.exists(path):
		raise GolemConfigError("The process path does not exist: %r" % path)

	check_dont_overwrite(conf)

	if len(powers) == 2:
		generate_lo_diagrams = True
		generate_nlo_virt = False
	elif len(powers) == 3:
		generate_lo_diagrams = powers[1].strip().lower() != "none"
		generate_nlo_virt = True
	else:
		raise GolemConfigError("The property %s must have 2 or 3 arguments." % \
				golem.properties.qgraf_power)

	conf["generate_lo_diagrams"] = generate_lo_diagrams
	conf["generate_nlo_virt"] = generate_nlo_virt
	conf["generate_uv_counterterms"] = False


	#if ("onshell" not in qgraf_options) and ("offshell" not in qgraf_options):
	#	qgraf_options.append("onshell")
	#	conf[golem.properties.qgraf_options] = ",".join(qgraf_options)


	if generate_nlo_virt and not r2only:
		# Check if a suitable extension for the reduction is available
		red_flag = False
		ext = golem.properties.getExtensions(conf)
		for red in golem.properties.REDUCTION_EXTENSIONS:
			if red in ext:
				red_flag = True
				break
		if not red_flag:
			golem.util.tools.warning(
					"Generating code for the virtual part without specifying",
					"a reduction library is useless.",
					"Please, make sure that at least one of the following",
					"is added to 'extensions':",
					", ".join(golem.properties.REDUCTION_EXTENSIONS),)
			conf["gosam-auto.extensions"] = "samurai"

	if len(ini) > 2:
		warning("You specified a process with %d incoming particles." %
					len(ini),
				"This software has not been fully tested for processes",
				"with more than two incoming particles."
				"We don't say this is impossible or wrong.",
				"",
				"====== BUT WE DON'T GUARANTEE FOR ANYTHING! =====")

	experimentals = map(str,
			filter(lambda p: p.isExperimental(), golem.properties.properties))
	for name in conf:
		if name in experimentals:
			warning(
				("Your configuration sets the property %r " % name) +
				"which is an undocumented and only partially tested feature.",
				"Please, feel free to test this feature but be aware that",
				"====== WE DON'T GUARANTEE FOR ANYTHING! =====")

	for prop in golem.properties.properties:
		lines = prop.check(conf)
		if len(lines) > 0:
			warning(*lines)


	# the following commands will need to import 'model.py'
	# here we create it:
	golem.util.tools.prepare_model_files(conf)

	for prop in [
			golem.properties.zero,
			golem.properties.one]:
		lst = conf.getProperty(prop)
		golem.util.tools.expand_parameter_list(prop, conf)
	
def run_analyzer(path, conf, in_particles, out_particles):
	generate_lo = conf.getBooleanProperty("generate_lo_diagrams")
	generate_virt = conf.getBooleanProperty("generate_nlo_virt")

	model = golem.util.tools.getModel(conf)
		
	lo_flags = {}
	virt_flags = {}

	if generate_lo:
		modname = consts.PATTERN_TOPOLOPY_LO
		fname = os.path.join(path, "%s.py" % modname)
		debug("Loading tree diagram file %r" % fname)
		mod_diag_lo = imp.load_source(modname, fname)
		# keep_tree, tree_signs, tree_flows =
		keep_tree, tree_signs = \
				golem.topolopy.functions.analyze_tree_diagrams(
					mod_diag_lo.diagrams, model, conf,
					filter_flags = lo_flags)
	else:
		keep_tree = []
		tree_signs = {}
		# tree_flows = {}

	quark_masses = []
	if generate_virt:
		zero = golem.util.tools.getZeroes(conf)
		onshell = {}
		i = 1
		for p in in_particles:
			m = p.getMass(zero)
			key = "es%d" % i
			if str(m) == "0":
				onshell[key] = "0"
			else:
				onshell[key] = "%s**2" % m

		modname = consts.PATTERN_TOPOLOPY_VIRT
		fname = os.path.join(path, "%s.py" % modname)
		debug("Loading one-loop diagram file %r" % fname)
		mod_diag_virt = imp.load_source(modname, fname)

		keep_virt, loopcache = golem.topolopy.functions.analyze_loop_diagrams(
				mod_diag_virt.diagrams, model, conf, onshell, quark_masses,
				filter_flags = virt_flags)
	else:
		keep_virt = []
		loopcache = golem.topolopy.objects.LoopCache()

	conf["__heavy_quarks__"] = quark_masses

	if not isinstance(lo_flags, dict):
		lo_flags = dict(enumerate(lo_flags))
	if not isinstance(virt_flags, dict):
		virt_flags = dict(enumerate(virt_flags))

	flags = (lo_flags, virt_flags)

	# return keep_tree, keep_virt, loopcache, tree_signs, tree_flows, flags
	return keep_tree, keep_virt, loopcache, tree_signs, flags
