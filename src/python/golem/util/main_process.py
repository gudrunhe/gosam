# vim: ts=3:sw=3
import os.path
import imp
import string

import golem.properties
import golem.model.feynrules

import golem.model.expressions

import golem.util.tools

from golem.util.main_color import *
from golem.util.main_helicity import rewrite_helicity_legs, generate_gauge_var


def create_process_hh(conf, in_particles, out_particles):
	"""
	Creates the file 'process.hh' that contains the
	process specific (but diagram independent)
	declarations and definitions, such as
	the color basis.

	The file 'process.hh' is created in the directory
	that has been specified in the configuration
	as 'process_path'.
	"""
	path = golem.util.tools.process_path(conf)

	zeroes = golem.util.tools.getZeroes(conf)
	ones = conf.getProperty(golem.properties.one)
	extensions = golem.properties.getExtensions(conf)

	if path is None:
		sys.exit("Option %s is required." % golem.properties.process_path)

	num_in = len(in_particles)
	num_out = len(out_particles)
	num_legs = num_in + num_out

	mandelstam_vars, mandelstam_subs = \
		golem.algorithms.mandelstam.generate_mandelstam_set(num_in, num_out,
				prefix="es", infix="", suffix="")

	indices = []
	zerovec = []
	lv = []
	for i in range(num_in):
		p = in_particles[i]
		m = p.getMass()
		if m in zeroes:
			m = "0"
		if m != "0":
			lv.append("l%d" % (i+1))
		else:
			lv.append("k%d" % (i+1))
		color_index = "i%dC%d" % (i+1, abs(p.getColor()))
		lorentz_index = "i%dL%d" % (i+1, abs(p.getSpin()))
		indices.append(color_index)
		indices.append(lorentz_index)
		zerovec.append("+k%d" % (i+1))
	for i in range(num_out):
		p = out_particles[i]
		m = p.getMass()
		if m in zeroes:
			m = "0"
		if m != "0":
			lv.append("l%d" % (i+num_in+1))
		else:
			lv.append("k%d" % (i+num_in+1))
		color_index = "o%dC%d" % (i+1, abs(p.getColor()))
		lorentz_index = "o%dL%d" % (i+1, abs(p.getSpin()))
		indices.append(color_index)
		indices.append(lorentz_index)
		zerovec.append("-k%d" % (len(in_particles) + i+1))
	
	file_name = os.path.join(path, "process.hh")
	f = open(file_name, 'w')
	f.write("* vim: ts=3:sw=3\n")
	f.write("#define LEGS \"%d\"\n" % num_legs)
	
	if generate_gauge_var:
		f.write("* Flag: Rewrite gauge boson legs as " +
			"eps(k) -> eps(k) + gaugeXz * k\n")

		if "gaugecheck" in extensions:
			GAUGEVAR = 1
		else:
			GAUGEVAR = 0

		f.write("#define GAUGEVAR \"%d\"\n" % GAUGEVAR)

	# define symbols
	f.write("*---#[ symbol definitions :\n")
	spsymbols = []
	for i in range(num_legs):
		for j in range(i+1,num_legs):
			spsymbols.append("spa%s%s" % (lv[i], lv[j]))
			spsymbols.append("spb%s%s" % (lv[j], lv[i]))

	for i in range(0, len(spsymbols), 7):
		f.write("Symbols %s;\n" % ",".join(spsymbols[i:i+7]))
	for i in range(0, len(mandelstam_vars), 10):
		stop = min(i+10, len(mandelstam_vars))
		lst = ", ".join(mandelstam_vars[i:i+stop])
		f.write("Symbols %s;\n" % lst)
	# define vectors
	f.write("Vectors k1, ..., k`LEGS';\n")
	f.write("#If `LOOPS' == 1\n")
	f.write("\tVector p1;\n")
	f.write("\tVectors r1, ..., r`LEGS';\n")
	f.write("#EndIf\n\n")

	k = 0
	flag = False
	for inp in  in_particles:
		k += 1
		twospin = inp.getSpin()
		if twospin == 2:
			if not flag:
				f.write("#If `GAUGEVAR'\n")
				flag = True
			f.write("\tSymbol gauge%dz;\n" % (k))
	for out in  out_particles:
		k += 1
		twospin = out.getSpin()
		if twospin == 2:
			if not flag:
				f.write("#If `GAUGEVAR'\n")
				flag = True
			f.write("\tSymbol gauge%dz;\n" % (k))

	if flag:
		f.write("#EndIf\n\n")

	# define indices
	for i in range(0, len(indices), 10):
		stop = min(i+10, len(indices))
		lst = ", ".join(indices[i:i+stop])
		f.write("Indices %s;\n" % lst)
	f.write("*---#] symbol definitions :\n")

	# Write out the set which can be used for abbreviations:
	kinvariants = spsymbols + mandelstam_vars
	lines = [",".join(kinvariants[i:i+7]) for i in range(0, len(spsymbols), 7)]

	f.write("*---#[ set of kinematic invariants :\n")
	f.write("#Define KinInvariants \"%s\"\n" % ",\\\n   ".join(lines))
	f.write("*---#] set of kinematic invariants :\n")

	# procedure zeroes: replace symbols that should be treated
	# as zero
	zeroes = list(filter(lambda x: x.strip() != "", zeroes))
	f.write("*---#[ procedure zeroes :\n")
	f.write("#procedure zeroes\n")
	for i in range(0, len(zeroes), 8):
		stop = min(i+8, len(zeroes))
		if stop > 0:
			f.write("\tMultiply replace_(%s);\n" %
					", ".join(map(lambda x: "%s, 0" % x, zeroes[i:i+stop])))
	f.write("#endprocedure\n")
	f.write("*---#] procedure zeroes :\n")

	# procedure ones: replace symbols that should be treated
	# as one
	ones = list(filter(lambda x: x.strip() != "", ones))
	f.write("*---#[ procedure ones :\n")
	f.write("#procedure ones\n")
	for i in range(0, len(ones), 8):
		stop = min(i+8, len(ones))
		if stop > 0:
			f.write("\tMultiply replace_(%s);\n" %
					", ".join(map(lambda x: "%s, 1" % x, ones[i:i+stop])))
	f.write("#endprocedure\n")
	f.write("*---#] procedure ones :\n")


	# write procedure abbrevlist
	#f.write(generate_abbrev_proc(conf, in_particles, out_particles))

	# procedure kinematics: replace dot products by Mandelstam variables
	# and use on-shell conditions

	# First create a list of onshell conditions:
	onshell = {}
	onshell2 = {}
	for i in range(1, num_legs + 1):
		if i <= num_in:
			p = in_particles[i - 1]
		else:
			p = out_particles[i - num_in - 1]
		mass = p.getMass()
		if mass in zeroes:
			mass = "0"
		if str(mass) == "0":
			onshell["es%d" % i] = "0"
			onshell2["es%d" % i] = "0"
		else:
			onshell["es%d" % i] = "(%s^2)" % mass
			onshell2["es%d" % i] = "%s**2" % mass

	f.write("*---#[ procedure conservation :\n")
	f.write("#procedure conservation\n")
	if num_out > 0:
		sign = 1
	else:
		sign = -1
	line = "Id k%d = " % num_legs
	for i in range(1, num_legs):
		if i <= num_in:
			s = sign
		else:
			s = -sign
		if s == 1:
			line += "+k%d" % i
		else:
			line += "-k%d" % i
	f.write("\t%s;\n" % line)
	f.write("#endprocedure\n")
	f.write("*---#] procedure conservation :\n")

	f.write("*---#[ procedure kinematics :\n")
	f.write("#procedure kinematics\n")
	for i in range(1, num_legs + 1):
		for j in range(i, num_legs + 1):
			subs = mandelstam_subs[i-1][j-1]
			rhs = ""
			terms = 0
			for v, c in subs.items():
				if v in onshell:
					symb = onshell[v]
				else:
					symb = v

				if symb != "0":
					if c == 1:
						if terms > 0:
							rhs += "+%s" % symb
						else:
							rhs = symb
					elif c == -1:
						rhs += "-%s" % symb
					elif (c > 0) and (terms > 0):
						rhs += "+%d*%s" % (c, symb)
					else:
						rhs += "%d*%s" % (c, symb)
					terms += 1
			if terms == 0:
				f.write("\tId k%d.k%d = 0;\n" % (i, j))
			else:
				f.write("\tId k%d.k%d = 1/2 * (%s);\n" % (i, j, rhs))
				if i == j:
					f.write("\tId l%d.l%d = 0;\n" % (i, j))

	f.write("#endprocedure\n")
	f.write("*---#] procedure kinematics :\n")

	f.write("*---#[ procedure spsymbols :\n")
	f.write("#procedure spsymbols\n")
	for i in range(num_legs):
		for j in range(i+1,num_legs):
			f.write("Id Spa2(%s, %s) = spa%s%s;\n"
					% (lv[i], lv[j], lv[i], lv[j]))
			f.write("Id Spb2(%s, %s) = spb%s%s;\n"
					% (lv[j], lv[i], lv[j], lv[i]))

	f.write("#endprocedure\n")
	f.write("*---#] procedure spsymbols :\n")

	rewrite_helicity_legs(f, in_particles, out_particles, zeroes)

	fermions = []
	idx = 0
	for p in in_particles:
		idx += 1
		if abs(p.getSpin()) != 1:
			continue
		fermions.append(str(idx))
	for p in out_particles:
		idx += 1
		if abs(p.getSpin()) != 1:
			continue
		fermions.append(str(idx))
	f.write("#define FERMIONS \"%s\"\n" % ",".join(fermions))

	f.write("*---#[ color :\n")
	write_color_basis(f, in_particles, out_particles)
	write_invcolor_basis(f, in_particles, out_particles)

	f.write("*---#] color :\n")

	f.close()

	if False:
		file_name = os.path.join(path, "process.dat")
		f = open(file_name, 'w')

		pr_dat = golem.util.config.Properties()
		pr_dat["zero"] = "".join(zerovec)
		pr_dat["num_in"] = num_in
		pr_dat.copyProperties(conf,
				golem.properties.process_name)
		for symbol, value in onshell2.items():
			pr_dat[symbol] = value


		pr_dat["generate_lo_diagrams"] = conf["generate_lo_diagrams"]
		pr_dat["generate_nlo_virt"] = conf["generate_nlo_virt"]
		pr_dat["extensions"] = golem.properties.getExtensions(conf)

		pr_dat.store(f)
		f.close()

def generate_abbrev_proc(conf, in_particles, out_particles, max_power=-1):
	"""
	Generate a list of abbreviations for products of spinor brackets up to a
	certain power.

	PARAMETER
		max_power -- maximum number of vectors inserted; if max_power < 0
		             or if the argument is omitted the function chooses
						 a value which is reasonable for a gauge theory.
	"""
	zeroes = golem.util.tools.getZeroes(conf)
	path = golem.util.tools.process_path(conf)

	# Calculate the number of vectors in the numerator
	power = max_power
	if power < 0:
		count = 0
		for p in in_particles + out_particles:
			twospin = int(p.getSpin())
			count += twospin % 2

		power = count / 2
		if power < 0:
			power = 0
	assert power >= 0

	# Emulate QGrafs in- and out-loops (no colour info needed):
	# <in_loop><back> *
	#    inp([[field.<field>]], idx<vertex_index>r<ray_index>, <momentum>) *
	#    inplorentz([CONJ][TWOSPIN], iv<vertex_index>r<ray_index>L[TWOSPIN],
	# <back> <momentum>, [MASS]) *
	# <end><back>
	# <out_loop><back> *
	#    out([[field.<field>]], idx<vertex_index>r<ray_index>, <momentum>) *
	#    outlorentz([CONJ][TWOSPIN], iv<vertex_index>r<ray_index>L[TWOSPIN],
	# <back> <momentum>, [MASS]) *
	# <end><back>
	#
	# These lines are stored in 'output'
	output = []


	# 'vectors' contains a list of vectors that appear in the problem
	vectors = []
	idx = 0
	for p in in_particles:
		idx += 1
		twospin = p.getSpin()
		if twospin < 0:
			twospin = -twospin
			conj = "-"
		else:
			conj = ""

		if p.isMassive(zeroes):
			vector = ("l%d" % idx)
		else:
			vector = ("k%d" % idx)
		vectors.append(vector)
	
		output.append("inp([field.%s], k%d)" % (p, idx))
		output.append("inplorentz(%s%d, iv0, k%d, %s)" %
				(conj, twospin, idx, p.getMass(zeroes)))

	for p in out_particles:
		idx += 1
		twospin = p.getSpin()
		if twospin < 0:
			twospin = -twospin
			conj = "-"
		else:
			conj = ""

		if p.isMassive(zeroes):
			vector = ("l%d" % idx)
		else:
			vector = ("k%d" % idx)
		vectors.append(vector)
	
		output.append("out([field.%s], k%d)" % (p, idx))
		output.append("outlorentz(%s%d, iv0, k%d, %s)" %
				(conj, twospin, idx, p.getMass(zeroes)))
	output.append("(1+VLIST(%s))^%d" % (",".join(vectors), power))

	output = [
			"*--#[ procedure abbrevlist:",
			"#procedure abbrevlist()",
			" *\n".join(output),
			"#endprocedure",
			"*--#] procedure abbrevlist:",
			""
			]

	return "\n".join(output)

def resolve_dependencies(functions):
	"""
	Bring a list of expressions into an order in which they
	can be computed
	"""
	all_names = functions.keys()
	graph = {}
	for name, expr in functions.items():
		edges = []
		for other in all_names:
			if name == other:
				continue

			if expr.dependsOn(other):
				edges.append(other)
		graph[name] = edges

	program = []
	while len(graph) > 0:
		found = None
		for name, edges in graph.items():
			if len(edges) == 0:
				found = name
				break
		if found is None:
			# Before we generate an error message we minimize the set of problematic
			# functions. In order to do so we drop all functions on which no other
			# function depends.
			flag = True
			while flag:
				flag = False
				bottom_expression = None
				for name in graph.keys():
					bottom = True
					for edges in graph.values():
						if name in edges:
							bottom = False
							break
					if bottom:
						bottom_expression = name
						break
				if bottom_expression is not None:
					flag = True
					del graph[bottom_expression]

			problem_set = ", ".join(graph.keys())

			golem.util.tools.error(
					"Cannot resolve dependencies between functions: %s." %
					problem_set)

		program.append(name)
		del graph[name]

		for edges in graph.values():
			if name in edges:
				edges.remove(name)

	return program

def generate_func_txt(conf):
	"""
	Creates the file func.txt which contains the functions
	defined in the model file. The format of this file is such
	that it can later be processed with haggies.
	"""

	path = golem.util.tools.process_path(conf)
	model_mod = golem.util.tools.getModel(conf)

	golem.util.tools.message("Generating func.txt ...")
	golem.util.tools.message("   - Compiling functions ...")
	parser = golem.model.expressions.ExpressionParser()
	functions = {}
	for name, value in model_mod.functions.items():
		expr = parser.compile(value)
		functions[name] = expr
	
	golem.util.tools.message("   - Resolving dependencies between functions ...")
	program = resolve_dependencies(functions)
	golem.util.tools.message("   - Writing func.txt ...")

	fname = os.path.join(path, "func.txt")
	f = open(fname, "w")
	for name in program:
		ast = functions[name]
		f.write(name)
		f.write("=");
		ast.write(f)
		f.write(";\n")
	f.close()

	golem.util.tools.message("   - Done")
