# vim: ts=3:sw=3
import sys
import os
import os.path
import imp
import StringIO
import hashlib

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

from golem.util.find_libpaths import find_libraries

from golem.util.path import golem_path, gosam_contrib_path
from golem.util.tools import copy_file, \
		debug, message, warning, \
		generate_particle_lists

from golem.util.config import GolemConfigError, split_qgrafPower

# The following files contain routines which originally were
# part of golem-main itself:
from golem.util.main_qgraf import *
from golem.installation import GOLEM_VERSION, GOLEM_REVISION

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
	# properties will be filled later:
	props = golem.util.config.Properties()
    

	# This fills in the defaults where no option is given:
	for p in golem.properties.properties:
		props.setProperty(str(p), conf.getProperty(p))

	golem.properties.setInternals(conf)


	path = golem.util.tools.process_path(conf)

	templates = conf.getProperty(golem.properties.template_path)
	templates = os.path.expandvars(templates)

	if templates is None or len(templates) == 0:
		templates = golem_path("templates")

	for name in conf:
		props[name] = conf[name]

	# Special treatment for one loop due to old code
	higher_loops = []
	for loop in conf.getListProperty("loops_to_generate"):
		# special treatment for 1loop
		if int(loop) <= 1 :
			continue
		else:
			higher_loops.append(loop)
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
	golem.templates.xmltemplates.transform_templates(templates, templates, path, props,
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
	keep_tree, keep_virt, keep_vtot, keep_higher_virt, keep_higher_vtot, eprops, keep_ct,  loopcache, loopcache_tot, tree_signs, flags, massive_bubbles = \
			run_analyzer(path, conf, in_particles, out_particles, higher_loops)
#	keep_tree, keep_virt, keep_ct, loopcache, tree_signs, flags, massive_bubbles = \
#			run_analyzer(path, conf, in_particles, out_particles)

	props.setProperty("topolopy.keep.tree", ",".join(map(str, keep_tree)))
	props.setProperty("topolopy.keep.virt", ",".join(map(str, keep_virt)))
	props.setProperty("topolopy.keep.vtot", ",".join(map(str, keep_vtot)))
	assert len(higher_loops) == len(keep_higher_virt), "len(higher_loops) [%d] != len(keep_higher_virt) [%d]" % (len(higher_loops),len(keep_higher_virt))
	for looporder, diagrams in zip(higher_loops, keep_higher_virt):
		props.setProperty("topolopy.keep.n%slo_virt" % looporder,",".join(map(str, diagrams)))
		props.setProperty("topolopy.count.n%slo_virt" % looporder, len(diagrams))
	for looporder, diagrams in zip(higher_loops, keep_higher_vtot):
		props.setProperty("topolopy.count.n%slo_docu" % looporder, len(diagrams))
	props.setProperty("topolopy.keep.ct", ",".join(map(str, keep_ct)))
	props.setProperty("topolopy.count.tree", len(keep_tree))
	props.setProperty("topolopy.count.virt", len(keep_virt))
	props.setProperty("topolopy.count.docu", len(keep_vtot))
	props.setProperty("topolopy.count.ct", len(keep_ct))
	props.setProperty("templates", templates)
	props.setProperty("process_path", path)
	props.setProperty("max_rank", conf["__max_rank__"])

	conf["__info.count.tree__"] = len(keep_tree)
	conf["__info.count.virt__"] = len(keep_virt)
	conf["__info.count.docu__"] = len(keep_vtot)
	conf["__info.count.higher_virt__"] = [len(diag) for diag in keep_higher_virt]
	conf["__info.count.higher_docu__"] = [len(diag) for diag in keep_higher_vtot]
	conf["__info.count.ct__"] = len(keep_ct)

	for key, value in golem.util.tools.derive_coupling_names(conf).items():
		props.setProperty("%s_COUPLING_NAME" % key, value)
		

#	golem.templates.xmltemplates.transform_templates(templates, templates, path, props,
#			conf = conf,
#			in_particles = in_particles,
#			out_particles = out_particles,
#			user = "reduze",
#			from_scratch=from_scratch,
#			loopcache=loopcache,
#			loopcache_tot=loopcache_tot,
#			tree_signs=tree_signs,
#			# tree_flows=tree_flows,
#			heavy_quarks=filter(lambda p: len(p.strip()) > 0,
#				conf.getListProperty("__heavy_quarks__")),
#			lo_flags = flags[0],
#			nlo_flags = flags[1],
#			massive_bubbles = massive_bubbles,
#			diagram_sum = eprops)

	#if conf["__REDUZE__"]=='True':  
	    #copy_file(os.path.join(os.getcwd(),conf.getProperty("projectors")), os.path.join(conf.getProperty("process_path"),'codegen','projectors.hh'))
	    #copy_file(os.path.join(os.getcwd(),conf.getProperty("integral_families_1loop")), os.path.join(conf.getProperty("process_path"),'codegen','reduze','1loop','config','integral_families.yaml'))
	    #copy_file(os.path.join(os.getcwd(),conf.getProperty("integral_families_2loop")), os.path.join(conf.getProperty("process_path"),'codegen','reduze','2loop','config','integral_families.yaml'))

	# Create and populate subdirectories
	golem.templates.xmltemplates.transform_templates(templates, templates, path, props,
			conf = conf,
			in_particles = in_particles,
			out_particles = out_particles,
			user = "main",
			from_scratch=from_scratch,
			loopcache=loopcache,
			loopcache_tot=loopcache_tot,
			tree_signs=tree_signs,
			# tree_flows=tree_flows,
			heavy_quarks=filter(lambda p: len(p.strip()) > 0,
				conf.getListProperty("__heavy_quarks__")),
			lo_flags = flags[0],
			nlo_flags = flags[1],
			massive_bubbles = massive_bubbles,
			diagram_sum = eprops)

	if flag_create_ff_files:
		create_ff_files(conf, in_particles, out_particles)
		
# obsolete; should be done by template.xml
#	if conf["__REDUZE__"]=='True':
#          copy_file(os.path.join(os.getcwd(),conf.getProperty("projectors")), os.path.join(path,"projectors.hh"))
#	  copy_file(os.path.join(os.getcwd(),conf.getProperty("integral_families_1loop")), os.path.join(path,"integral_families_1loop.yaml"))
#	  if conf.getBooleanProperty("generate_nnlo_virt"):
#	    copy_file(os.path.join(os.getcwd(),conf.getProperty("integral_families_2loop")), os.path.join(path,"integral_families_2loop.yaml"))

	golem.templates.xmltemplates.transform_templates(templates, path, path, props,
			conf = conf,
			in_particles = in_particles,
			out_particles = out_particles,
			user = "reduze",
			from_scratch=from_scratch,
			loopcache=loopcache,
			loopcache_tot=loopcache_tot,
			tree_signs=tree_signs,
			# tree_flows=tree_flows,
			heavy_quarks=filter(lambda p: len(p.strip()) > 0,
				conf.getListProperty("__heavy_quarks__")),
			lo_flags = flags[0],
			nlo_flags = flags[1],
			massive_bubbles = massive_bubbles,
			diagram_sum = eprops)


	cleanup(path)

def cleanup(path):
	cleanup_files = []

	for ext in [".tex", ".log", ".py", ".pyc", ".pyo"]:
		for stub in ["pyxotree", "pyxovirt", "pyxo2virt", "topotree", "topovirt", "pyxoct", "topoct"]:
			cleanup_files.append(stub + ext)

#	if True:
#		for ext in ["", ".py", ".pyc", ".pyo"]:
#			cleanup_files.append("model" + ext)

	for filename in cleanup_files:
		full_name = os.path.join(path, filename)
		if os.path.exists(full_name):
			os.remove(full_name)

def find_config_files():
	"""
	Searches for configuration files in the default locations.
	These are used to fill the fields of newly created input
	files by preferred defaults.
	Use "golem.util.find_libpaths.find_libraries()"
	to find	external library paths.

	The procedure looks in the following locations:
		<golem path>
		<guessed share/gosam-contrib path>
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
	directories = [golem_path(), gosam_contrib_path(),
			golem.util.path.get_homedir(), os.getcwd()]
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
	libpaths = find_libraries()
	for flag in libpaths:
		props.setProperty(flag, libpaths[flag])
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
		changed = str(prop) in defaults.propertyNames()
		subprocess_specific_settings = False
		for k in defaults:
			if k.startswith(str(prop)+"["):
				subprocess_specific_settings=True
				changed=True
				break

		if prop.isExperimental() and not changed:
			continue
		if prop.isHidden() and not changed:
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
			if subprocess_specific_settings:
				for k in defaults:
					if k.startswith(str(prop)+"["):
						f.write("%s=%s\n" % (k, defaults.getProperty(k)))
			f.write("\n")
		elif format == "LaTeX":
			if prop.getDefault() is not None:
				value = str(prop.getDefault())
				if len(value) > 0:
					f.write("Default: \\verb|%s|\n" % value)

	if format is None:
		for prop in defaults:
			if prop.startswith("+") or prop.endswith(".extensions"):
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

		# be compatible between internal 1.99 releases and 2.0.*
		if ver==[1,99] and GOLEM_VERSION[:2] == [2,0]:
			warning("This directory has been generated with an older version "+
				"of GoSam (%s)." % result["golem-version"],
				"If you get compiler errors, you might need to remove all files",
				"including '.golem.dir' and rerun gosam.py.")
			return result

		# be compatible to older 2.0.* releases
		if ver[:2]==[2,0] and GOLEM_VERSION[:2] == [2,0] and ver[:3]<=(GOLEM_VERSION[:3]+[0]*5)[:3]:
			if ver[:3]!=(GOLEM_VERSION[:3]+[0]*5)[:3]:
				warning("This directory has been generated with an older version "+
					"of GoSam (%s)." % result["golem-version"],
					"If you get compiler errors, you might need to remove all files",
					"including '.golem.dir' and rerun gosam.py.")
			return result

		for gv, v in zip(GOLEM_VERSION + [0]*5, ver):
			if gv > v:
				raise GolemConfigError(
						"This directory has been generated with an older version "+
						"of GoSam (%s).\n" % result["golem-version"]+
						"Please, remove all files, including '.golem.dir' "+
						"and rerun gosam.py.")
			elif gv < v:
				raise GolemConfigError(
						"This directory has been generated with a newer version "+
						"of GoSam (%s).\n" % result["golem-version"]+
						"Please, remove all files, including '.golem.dir' "+
						"and rerun gosam.py.")

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
	if os.path.exists(os.path.abspath(fname)):
		dir_info["setup-file-sha1"] = hashlib.sha1(open(os.path.abspath(fname)).read()).hexdigest()
	dir_info["golem-version"] = ".".join(map(str, GOLEM_VERSION))
	dir_info["golem-revision"] =  str(GOLEM_REVISION)
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
	#conf["helsum"] = conf.getBooleanProperty(golem.properties.sum_helicities)
	

        if conf["__OLP_MODE__"]:
            correction_type = conf.getProperty("olp.correctiontype", default=None)
            if correction_type=="EW":
                correction_type="QED"

        orders = split_qgrafPower(",".join(map(str,conf.getProperty(golem.properties.qgraf_power))))
        powers = orders[0] if orders else []
            
	renorm = conf.getProperty(golem.properties.renorm)
	templates = conf.getProperty(golem.properties.template_path)
	templates = os.path.expandvars(templates)
	qgraf_options = conf.getProperty(golem.properties.qgraf_options)

	r2only = conf.getProperty(golem.properties.r2).lower().strip() == "only"
#	formopt = conf.getProperty(golem.properties.formopt)
	# Prepare a copy of the setup file in the property [% user.setup %]
	buf = StringIO.StringIO()
	conf.store(buf, properties=golem.properties.properties,
			info= [
            "golem.full-name", "golem.name", "golem.version",
            "golem.revision", "setup-file"])
	conf.setProperty("user.setup", buf.getvalue())
	buf.close()

	# properties will be filled later:
	props = golem.util.config.Properties()

	experimentals = map(str,
			filter(lambda p: p.isExperimental(), golem.properties.properties))
	for name in conf:
		if name in experimentals:
			warning(
				("Your configuration sets the property %r " % name) +
				"which is an undocumented and only partially tested feature.",
				"Please, feel free to test this feature but be aware that",
				"====== WE DON'T GUARANTEE ANYTHING! =====")


	# This fills in the defaults where no option is given:
	for p in golem.properties.properties:
		if conf.getProperty(p):
			conf.setProperty(str(p), conf.getProperty(p))

	if not conf["extensions"] and props["extensions"]:
		conf["extensions"]=props["extensions"]

	tmp_ext = golem.properties.getExtensions(conf)

	for p in conf["reduction_programs"].split(","):
		if not p in tmp_ext:
			if conf["gosam-auto-reduction.extensions"]:
				conf["gosam-auto-reduction.extensions"] = p + "," + conf["gosam-auto-reduction.extensions"]
			else:
				conf["gosam-auto-reduction.extensions"]  = p

	# Check if path exists. If it doesn't, try to create it
	if not os.path.exists(path):
		try:
			rp=os.path.relpath(path)
			if not os.path.sep in rp:
				os.mkdir(rp)
				warning("Process path %r created." % path)
		except OSError,err:
			raise GolemConfigError("Could not create process path: %r\r%s" % (path,err))

	if not os.path.exists(path):
		raise GolemConfigError("The process path does not exist: %r" % path)

	check_dont_overwrite(conf)

	if len(powers) < 2:
		raise GolemConfigError("The property %s must have 2 or more arguments." % \
				golem.properties.qgraf_power)
	if len(powers) == 2:
		generate_lo_diagrams = True
		generate_nlo_virt = False
		generate_nnlo_virt = False
	elif len(powers) == 3:
		generate_lo_diagrams = powers[1].strip().lower() != "none"
		generate_nlo_virt = powers[2].strip().lower() != "none"
		generate_nnlo_virt = False
	else:
		generate_lo_diagrams = powers[1].strip().lower() != "none"
		generate_nlo_virt = powers[2].strip().lower() != "none"
		generate_nnlo_virt = powers[3].strip().lower() != "none"
		warning("Your configuration sets a calculation to loop-order higher than 1 " +
              "which is an undocumented and only partially tested feature.",
              "Please, feel free to test this feature but be aware that",
              "====== WE DON'T GUARANTEE ANYTHING! =====")

	# loop orders that are to be calculated
	# parse the arument "order" of the run card
	loops_to_generate = []
	for i, power in enumerate(powers):
		# first element in powers is the type of the coupling
		# skip tree level (zero loops)
		if i == 0 or i == 1:
			continue
		if power.strip().lower() != "none":
			loops_to_generate.append(i - 1)
        if len(loops_to_generate)==0:
	  loops_to_generate.append(0)
	conf["loops_to_generate"] = loops_to_generate	  
	conf["generate_lo_diagrams"] = generate_lo_diagrams
	conf["generate_nlo_virt"] = generate_nlo_virt
	conf["generate_uv_counterterms"] = (len(conf.getProperty(golem.properties.model))>1 and conf.getProperty(golem.properties.model)[1]!='../model/Standard_Model_UFO')\
                    or conf["modeltype"]=="smdiag_complex_ct" or \
                    conf.getProperty(golem.properties.model)[0]=='smdiag_complex_ct'
        conf["generate_ct_internal"] = conf["modeltype"]=="smdiag_complex_ct" or \
            conf.getProperty(golem.properties.model)[0]=='smdiag_complex_ct'
        conf["qcd_in_ew"] = conf.getBooleanProperty("olp.qcd_in_ew")
	conf["generate_nnlo_virt"] = generate_nnlo_virt
	#generate_uv_counterterms
	#False

	if not conf["PSP_chk_method"] or conf["PSP_chk_method"].lower()=="automatic":
		conf["PSP_chk_method"] = "PoleRotation" if generate_lo_diagrams else "LoopInduced"

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
		if "pjfry" in ext and not "golem95" in ext:
			golem.util.tools.warning("The PJFRY interface needs Golem95 routines.",
					"Golem95 is automatically added to reduction_programs.")
			conf["gosam-auto-reduction.extensions"] = "golem95"
		if not red_flag:
			golem.util.tools.warning(
					"Generating code for the virtual part without specifying",
					"a reduction library is useless.",
					"Please, make sure that at least one of the following",
					"is added to 'extensions':",
					", ".join(golem.properties.REDUCTION_EXTENSIONS),)
			conf["gosam-auto-reduction.extensions"] = "ninja,golem95"
	if not generate_nlo_virt and conf["gosam-auto-reduction.extensions"]:
			conf["gosam-auto-reduction.extensions"]=""

	if not conf["reduction_interoperation"]:
		conf["reduction_interoperation"]=-1

	if not conf["reduction_interoperation_rescue"]:
		conf["reduction_interoperation_rescue"]=-1

	if len(ini) > 2:
		warning("You specified a process with %d incoming particles." %
					len(ini),
				"This software has not been fully tested for processes",
				"with more than two incoming particles.",
				"We don't say this is impossible or wrong.",
				"",
				"====== WE DON'T GUARANTEE ANYTHING! =====")

	# retrive final extensions from other options
	ext = golem.properties.getExtensions(conf)

	if "noformopt" not in ext:
		ext.append("formopt")
	if "noderive" not in ext:
		ext.append("derive")

	if "cdr" in ext and "dred" in ext:
		warning("Incompatible settings between regularisation_scheme and extensions. cdr is used.")

	if "no-fr5" in ext:
		warning("no-fr5 is not supported anymore.")

	if not "dred" in ext:
		ext.append("dred")
	if conf["regularisation_scheme"]=="cdr" or "cdr" in ext:
		conf["olp.irregularisation"]="CDR"



	# We need to put out an error if we specify formopt and some other extensions
	if 'formopt' in ext:
		if 'topolynomial' in ext:
			raise GolemConfigError(
						"Your configuration has select the extension 'topolynomial' \n"
						"and optimization by FORM 'formopt'. " +
						"The two options are not compatible. \nPlease change your input " +
						"card (remove topolynomial or add noformopt) and re-run.")
		if 'r2_only' in ext:
			raise GolemConfigError(
						"r2 only not supported with extension formopt. Add the 'noformopt' extension.\n")
		if conf["abbrev.level"] != "diagram" and conf["abbrev.level"] is not None:
			raise GolemConfigError(
						"formopt only supported with abbrev.level=diagram\n")
	if ('ninja' in ext) and ('formopt' not in ext):
		raise GolemConfigError(
			"The ninja reduction method is only supported with formopt.\n" +
			"Please either remove noformopt or ninja in the input card\n")

	conf["reduction_interoperation"]=conf["reduction_interoperation"].upper()
	conf["reduction_interoperation_rescue"]=conf["reduction_interoperation_rescue"].upper()

	if "shared" in ext:
		conf["shared.fcflags"]="-fPIC"
		conf["shared.ldflags"]="-fPIC"
		
		
	if conf.getBooleanProperty("helsum"):
		if not conf.getBooleanProperty("generate_lo_diagrams"):
			raise GolemConfigError(
				'The "helsum" feature is not implemented for loop-induced processes.\n' +
				'Set "helsum=false" for the selected process.\n')
		if "generate-all-helicities" not in ext:
			ext.append("generate-all-helicities")
		if conf.getProperty("polvec")=="numerical" or "numpolvec" in ext:
			raise GolemConfigError(
				'The "helsum" feature is only implemented for explicit\n' +
				'polarization vectors. Please either set "helsum=false"\n' +
				'or "polvec=explicit" in the input card."\n')
	else:
		if conf.getProperty("polvec")=="numerical" and not "numpolvec" in ext:
			ext.append("numpolvec")

	for prop in golem.properties.properties:
		lines = prop.check(conf)
		if len(lines) > 0:
			warning(*lines)

	conf["extensions"] = ext

	# the following commands will need to import 'model.py'
	# here we create it:
	golem.util.tools.prepare_model_files(conf)

	for prop in [
			golem.properties.zero,
			golem.properties.one]:
		lst = conf.getProperty(prop)
		golem.util.tools.expand_parameter_list(prop, conf)
	
def run_analyzer(path, conf, in_particles, out_particles, higher_loops):
	generate_lo = conf.getBooleanProperty("generate_lo_diagrams")
	generate_virt = conf.getBooleanProperty("generate_nlo_virt")
	generate_nnlo_virt = conf.getBooleanProperty("generate_nnlo_virt")
	generate_ct = conf.getBooleanProperty("generate_uv_counterterms")
	generate_ct_internal = conf.getBooleanProperty("generate_ct_internal")


	model = golem.util.tools.getModel(conf)
	flag_reduze = conf.getBooleanProperty("__REDUZE__")

		
	lo_flags = {}
	virt_flags = {}
	ct_flags = {}

	if generate_lo:
		modname = consts.PATTERN_TOPOLOPY_LO
		fname = os.path.join(path, "%s.py" % modname)
		debug("Loading tree diagram file %r" % fname)
		mod_diag_lo = imp.load_source(modname, fname)
		conf["ehc"]=False
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
	complex_masses = []
	massive_bubbles = {}
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

		keep_virt, keep_vtot, eprops, loopcache, loopcache_tot = golem.topolopy.functions.analyze_loop_diagrams(
			mod_diag_virt.diagrams, model, conf, onshell, quark_masses, complex_masses,
			filter_flags = virt_flags, massive_bubbles = massive_bubbles)
			
		if flag_reduze:
		  golem.topolopy.functions.analyze_yaml(path, conf,keep_vtot, consts.PATTERN_REDUZE_NLO_VIRT)
		  

	else:
		keep_virt = []
		keep_vtot = []
		eprops    = {}
		loopcache     = golem.topolopy.objects.LoopCache()
		loopcache_tot = golem.topolopy.objects.LoopCache()

	generate_higher_virt = False
	for l in conf.getListProperty("loops_to_generate"):
		if int(l) >= 2:
			generate_higher_virt = True
			break
	if generate_higher_virt:
		keep_higher_virt = []
		keep_higher_vtot = []
		for loop_order in higher_loops:
			zero = golem.util.tools.getZeroes(conf)
			onshell = {}
			i=1
			for p in in_particles:
				m = p.getMass(zero)
				key = "es%d" % i
				if str(m) == "0":
					onshell[key] = "0"
				else:
					onshell[key] = "%s**2" % m

			modname = consts.PATTERN_TOPOLOPY_HIGHER_VIRT % loop_order
			fname = os.path.join(path, "%s.py" % modname)
			debug("Loading %s-loop diagram file %r" % (loop_order,fname))
			mod_diag_higher_virt = imp.load_source(modname, fname)
		
			tmp_keep_higher_virt, tmp_keep_higher_vtot = golem.topolopy.functions.analyze_higher_loop_diagrams(
				mod_diag_higher_virt.diagrams, model, conf, onshell, loop_order, quark_masses, complex_masses,
				filter_flags = virt_flags, massive_bubbles = massive_bubbles)

			keep_higher_virt.append(tmp_keep_higher_virt)
			keep_higher_vtot.append(tmp_keep_higher_vtot)
			
			if flag_reduze:
			  golem.topolopy.functions.analyze_yaml(path, conf, tmp_keep_higher_vtot, consts.PATTERN_REDUZE_HIGHER_VIRT %loop_order)
	else:
		keep_higher_virt = []
		keep_higher_vtot = []

	keep_ct = []
	ct_signs = {}
	if generate_virt and generate_ct_internal:
		modname = consts.PATTERN_TOPOLOPY_CT
		modname_LO = consts.PATTERN_TOPOLOPY_LO
		fname = os.path.join(path, "%s.py" % modname)
		debug("Loading counter term diagram file %r" % fname)
		mod_diag_ct = imp.load_source(modname, fname)
		onshell={}
		#props.SetProperty("model","modelct")
		# keep_tree, tree_signs, tree_flows =
		keep_ct, ct_signs = \
				golem.topolopy.functions.analyze_ct_diagrams(
				mod_diag_ct.diagrams, model, conf, filter_flags = lo_flags)
	else:
		keep_ct = keep_tree
		ct_signs = tree_signs
	tree_flows = {}


	conf["__heavy_quarks__"] = quark_masses
	conf["complex_masses"] = complex_masses

	if not isinstance(lo_flags, dict):
		lo_flags = dict(enumerate(lo_flags))
	if not isinstance(virt_flags, dict):
		virt_flags = dict(enumerate(virt_flags))
	if not isinstance(ct_flags, dict):
		ct_flags = dict(enumerate(ct_flags))

	flags = (lo_flags, virt_flags, ct_flags)

	# return keep_tree, keep_virt, loopcache, tree_signs, tree_flows, flags
	return keep_tree, keep_virt, keep_vtot, keep_higher_virt, keep_higher_vtot, eprops, keep_ct, loopcache, loopcache_tot, tree_signs, flags, massive_bubbles



