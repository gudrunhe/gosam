# vim: ts=3:sw=3
"""
This module allows to import model definitions from FeynRules using the
Python interface.
"""

import os
import os.path
import sys
import copy
import golem.model.expressions as ex

from golem.util.tools import error, warning, message, debug, \
		LimitedWidthOutputStream, load_source

LINE_STYLES = {
		'straight': 'fermion',
		'wavy': 'photon',
		'curly': 'gluon',
		'dashed': 'scalar',
		'dotted': 'ghost',
		'swavy' : 'majorana',
		'scurly' : 'majorana'
}



sym_cmath = ex.SymbolExpression("cmath")
sym_exp   = ex.SymbolExpression("exp")
sym_log   = ex.SymbolExpression("log")
sym_sqrt  = ex.SymbolExpression("sqrt")
sym_sin   = ex.SymbolExpression("sin")
sym_cos   = ex.SymbolExpression("cos")
sym_tan   = ex.SymbolExpression("tan")
sym_asin  = ex.SymbolExpression("asin")
sym_acos  = ex.SymbolExpression("acos")
sym_atan  = ex.SymbolExpression("atan")
sym_sinh  = ex.SymbolExpression("sinh")
sym_cosh  = ex.SymbolExpression("cosh")
sym_tanh  = ex.SymbolExpression("tanh")
sym_asinh = ex.SymbolExpression("asinh")
sym_acosh = ex.SymbolExpression("acosh")
sym_atanh = ex.SymbolExpression("atanh")
sym_pi    = ex.SymbolExpression("pi")
sym_e     = ex.SymbolExpression("e")

sym_re    = ex.SpecialExpression("re")
sym_im    = ex.SpecialExpression("im")
sym_sec   = ex.SpecialExpression("sec")
sym_csc   = ex.SpecialExpression("csc")
sym_asec  = ex.SpecialExpression("asec")
sym_acsc  = ex.SpecialExpression("acsc")
sym_conjg = ex.SpecialExpression("complexconjugate")
sym_cmplx = ex.SpecialExpression("complex")

sym_Nf    = ex.SpecialExpression("Nf")
sym_Nfgen = ex.SpecialExpression("Nfgen")
sym_Nfrat = ex.SpecialExpression("Nfrat")
sym_NC    = ex.SpecialExpression("NC")
sym_if    = ex.SpecialExpression("if")

i_ = ex.SpecialExpression("i_")

cmath_functions = [
		sym_exp, sym_log, sym_sqrt, sym_sin, sym_cos, sym_tan,
		sym_asin, sym_acos, sym_atan, sym_sinh, sym_cosh, sym_tanh,
		sym_asinh, sym_acosh, sym_atanh, sym_pi, sym_e
	]

shortcut_functions = [
		sym_re, sym_im, sym_sec, sym_csc, sym_asec, sym_acsc,
		sym_conjg, sym_cmplx, sym_if
	]

unprefixed_symbols = [
		sym_Nf, sym_Nfgen, sym_Nfrat
	]

class Model:
	def __init__(self, model_path, model_options=None):
		self.model_options = model_options or dict()

		sys.path.append(model_path)
		parent_path = os.path.normpath(os.path.join(model_path, os.pardir))
		norm_path = os.path.normpath(model_path)
		if norm_path.startswith(parent_path):
			mname = norm_path[len(parent_path):].replace(os.sep, "")
		else:
			mname = os.path.basename(model_path.rstrip(os.sep + (os.altsep if os.altsep else '')))
		if os.altsep is not None:
			mname = mname.replace(os.altsep, "")
		search_path = [ parent_path ]

		message("Trying to import FeynRules model '%s' from %s" %
				(mname, search_path[0]))
		mod = load_ufo_files(mname, search_path)

		self.all_particles  = mod.all_particles
		self.all_couplings  = mod.all_couplings
		self.all_parameters = mod.all_parameters
		self.all_vertices   = mod.all_vertices
		self.all_lorentz    = mod.all_lorentz
		self.model_orig = model_path
		self.model_name = mname
		self.prefix = "mdl"
		self.floats = []
		self.floatsd = {}
		self.floatsc = []

		try:
			self.all_CTparameters = mod.all_CTparameters
		except AttributeError:
			pass

		try:
			self.all_CTvertices = mod.all_CTvertices
		except AttributeError:
			pass

		self.useCT = False
		# the following code block splits all_couplings into
		# two separate lists of CT and non-CT couplings
		# also fills self.ctfunctions used write_python_file
		if hasattr(mod,"CT_vertices"):
			self.useCT = True
			self.all_CTcouplings = []
			self.ctfunctions = {}
			self.cttypes = {}
			for a in dir(mod.CT_vertices.C):
				b = getattr(mod.CT_vertices.C,a)
				if type(b).__name__ == "Coupling":
					self.all_CTcouplings.append(b)
					if b in self.all_couplings:
						self.all_couplings.remove(b)
		# construct the CT dictionary representing the Laurent expansion
			for c in self.all_CTcouplings:
				name = self.prefix + c.name.replace("_", "")
				self.ctfunctions[(name+'const')] = {}
				self.ctfunctions[(name+'log')] = {}
				self.cttypes[(name+'const')] = "C"
				self.cttypes[(name+'log')] = "C"
				if isinstance(c.value,dict):
					# the value of the coupling is a dictionary representing the Laurent expansion
					# => split const from log terms, if present
					for ctpart in ['const','log']:
						for ctpole in list(c.value.keys()):
							if isinstance(c.value[ctpole],dict):
								ctcoeff = c.value[ctpole][ctpart]
							else:
								if ctpart == 'const':
									ctcoeff = c.value[ctpole]
								else:
									ctcoeff = '0'
							self.ctfunctions[(name+ctpart)][ctpole] = ctcoeff
				elif isinstance(c.value,str):
					# the value of the coupling is a string and the Laurent expansion is only evident after evaluating CTParameter type objects

					CTparams = [ctp for ctp in self.all_CTparameters if ctp.name in c.value]
					CTpoles = set()

					for ctparam in CTparams:
						CTpoles = CTpoles.union(set(ctparam.value.keys()))

					for ctpart in ['const','log']:
						for ctpole in CTpoles:
							ctcoeff = c.value
							for ctparam in CTparams:
								if ctpole in ctparam.value:
									if isinstance(ctparam.value[ctpole],dict):
										ctcoeff = ctcoeff.replace(ctparam.name,ctparam.value[ctpole][ctpart])
									else:
										if ctpart == 'const':
											ctcoeff = ctcoeff.replace(ctparam.name,ctparam.value[ctpole])
										else:
											ctcoeff = ctcoeff.replace(ctparam.name,'0')
								else:
									ctcoeff = ctcoeff.replace(ctparam.name,'0')
							self.ctfunctions[(name+ctpart)][ctpole] = ctcoeff
				else:
					error("CT coupling %s is neither a dict nor str!" % c)

		parser = ex.ExpressionParser()
		ex.ExpressionParser.simple = ex.ExpressionParser.simple_old
		for l in self.all_lorentz:
			name = l.name
			structure = parser.compile(l.structure)
			l.rank = get_rank(structure)	

	def write_python_file(self, f):
		# Edit : GC- 16.11.12 now have the dictionaries
		# particlect and parameterct available
		# if non-empty the model.py file is modified
		f.write("# vim: ts=3:sw=3\n")
		f.write("# This file has been generated from the FeynRules model files\n")
		f.write("# in %s\n" % self.model_orig)
		f.write("from golem.model.particle import Particle\n")
		f.write("\nmodel_name = %r\n\n" % self.model_name)

		message("      Generating particle list ...")
		f.write("particles = {")

		is_first = True

		mnemonics = {}
		latex_names = {}
		line_types = {}
		particlect = {}

		for p in self.all_particles:
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			try:
				particlect[p] = p.counterterm
			except AttributeError:
				pass
			pmass = str(p.mass)
			pwidth = str(p.width)

			pdg_code = p.pdg_code
			canonical_name, canonical_anti = canonical_field_names(p)

			mnemonics[p.name] = canonical_name
			latex_names[canonical_name] = p.texname

			line_type = p.line.lower()
			# FIX- 15.08.12 GC # until FeynRules can accomodate charged scalars
			if line_type in LINE_STYLES:
				if (line_type == 'dashed') and (abs(p.color) == 3):
					line_types[canonical_name] = 'chargedscalar'
				else:
					line_types[canonical_name] = LINE_STYLES[line_type]
			else:
				line_types[canonical_name] = 'scalar'

			if pmass == "0" or pmass == "ZERO":
				mass = 0
			else:
				mass = self.prefix + pmass

			spin = abs(p.spin) - 1
			if canonical_name.startswith("anti"):
				spin = - spin

			if pwidth == "0" or pwidth == "ZERO":
				width = "0"
			else:
				width = self.prefix + pwidth

			f.write("\t%r: Particle(%r, %d, %r, %d, %r, %r, %d, %r)" %
					(canonical_name, canonical_name, spin, mass,
						p.color, canonical_anti, width, pdg_code, p.charge))

		f.write("\n}\n\n")

		is_first = True
		f.write("mnemonics = {")
		for key, value in list(mnemonics.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")

			f.write("\t%r: particles[%r]" % (key, value))
		f.write("\n}\n\n")

		is_first = True
		f.write("latex_names = {")
		for key, value in list(latex_names.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")

			f.write("\t%r: %r" % (key, value))
		f.write("\n}\n\n")

		is_first = True
		f.write("line_styles = {")
		for key, value in list(line_types.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")

			f.write("\t%r: %r" % (key, value))
		f.write("\n}\n\n")


		parameters = {}
		functions = {}
		types = {}
		parameterct={}
		slha_locations = {}
		for p in self.all_parameters:
			#  new: collect all the new counterterm pieces (if there are any)
			try:
			# use the name (p.name) or the object in the dictionary
				parameterct[p] = p.counterterm
			except AttributeError:
				pass
			name = self.prefix + p.name.replace("_","undrscr")
			if p.nature == 'external':
				parameters[name] = p.value
				slha_locations[name] = (p.lhablock, p.lhacode)
			elif p.nature == 'internal':
				functions[name] = p.value
			else:
				error("Parameter's nature ('%s') not implemented." % p.nature)

			if p.type == "real":
				types[name] = "R"
			elif p.type == "complex":
				types[name] = "C"
			else:
				error("Parameter's type ('%s') not implemented." % p.type)
		parameters['NC'] = '3.0'
		types['NC'] = 'R'
		parameters['Nf'] = '5.0'
		types['Nf'] = 'R'
		parameters['Nfgen'] = '-1.0'
		types['Nfgen'] = 'R'

		functions['Nfrat'] = 'if(Nfgen,Nf/Nfgen,1)'
		types['Nfrat'] = 'R'


		for key, value in list(self.model_options.items()):
			if key in parameters or self.prefix+key in parameters:
				if key in parameters:
					real_key=key
				else:
					real_key=self.prefix+key
				try:
					sval = str(value)
					fval = float(sval)
					parameters[real_key] = sval
				except ValueError:
					warning("Model option %s=%r not in allowed range." % (key, value),
							"Option ignored")
		specials = {}
		for expr in shortcut_functions:
			specials[str(expr)] = expr
		for expr in unprefixed_symbols:
			specials[str(expr)] = expr

		parser = ex.ExpressionParser(**specials)

		for c in self.all_couplings:
			name = self.prefix + c.name.replace("_", "")
			functions[name] = c.value
			types[name] = "C"

		message("      Generating function list ...")
		f.write("functions = {")
		fcounter = [0]
		fsubs = {}
		is_first = True
		for name, value in list(functions.items()):
			expr = parser.compile(value)
			for fn in cmath_functions:
				expr = expr.algsubs(ex.DotExpression(sym_cmath, fn),
						ex.SpecialExpression(str(fn)))
			expr = expr.prefixSymbolsWith(self.prefix)
			expr = expr.replaceFloats(self.prefix + "float", fsubs, fcounter)
			expr = expr.algsubs(sym_cmplx(
				ex.IntegerExpression(0), ex.IntegerExpression(1)), i_)

			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			f.write("\t%r: " % name)
			f.write("'")
			expr.write(f)
			f.write("'")
		f.write("\n}\n\n")

		if self.useCT:
			types.update(self.cttypes)

			message("      Generating counter term function list ...")
			f.write("ctfunctions = {")
			is_first = True
			for name, value in self.ctfunctions.items():
				if is_first:
					is_first = False
					f.write("\n")
				else:
					f.write(",\n")
				f.write("\t%r: " % name)
				is_firstcf = True
				for pl, cf in value.items():
					expr = parser.compile(cf)
					for fn in cmath_functions:
						expr = expr.algsubs(ex.DotExpression(sym_cmath, fn),
								ex.SpecialExpression(str(fn)))
					expr = expr.prefixSymbolsWith(self.prefix)
					expr = expr.replaceFloats(self.prefix + "float", fsubs, fcounter)
					expr = expr.algsubs(sym_cmplx(
						ex.IntegerExpression(0), ex.IntegerExpression(1)), i_)

					if is_firstcf:
						is_firstcf = False
						f.write("{\n")
					else:
						f.write(",\n")
					f.write("\t\t%r: " % pl)
					f.write("'")
					expr.write(f)
					f.write("'")
				f.write("\n\t}")
			f.write("\n}\n\n")

		# search for additional floats appearing in lorentz structures
		for l in self.all_lorentz:
			structure = parser.compile(l.structure)
			structure = structure.replaceFloats(self.prefix + "float", fsubs, fcounter)

		self.floats = list(fsubs.keys())
		self.floatsd = fsubs
		self.floatsc = fcounter

		f.write("parameters = {")
		is_first = True

		for name, value in list(fsubs.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			f.write("\t%r: %r" % (name, str(value)))

		for name, value in list(parameters.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			if isinstance(value, complex):
				f.write("\t%r: [%r, %r" % (name, str(value.real), str(value.imag)))
			else:
				f.write("\t%r: %r" % (name, str(value)))
		f.write("\n}\n\n")

		f.write("latex_parameters = {")
		is_first = True
		for p in self.all_parameters:
			name = self.prefix + p.name.replace("_","undrscr")
			if is_first:
				is_first = False
			else:
				f.write(",") 
			f.write("\n\t%r: %r" % (name, p.texname)) 
		f.write("\n}\n\n")

		f.write("types = {")
		is_first = True

		for name in list(fsubs.keys()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			f.write("\t%r: 'RP'" % name)

		for name, value in list(types.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			f.write("\t%r: %r" % (name, value))
		f.write("\n}\n\n")

		f.write("slha_locations = {")
		is_first = True

		for name, value in list(slha_locations.items()):
			if is_first:
				is_first = False
				f.write("\n")
			else:
				f.write(",\n")
			f.write("\t%r: %r" % (name, value))
		f.write("\n}\n\n")

		# new for modified UFO files
		for p in particlect:
			print(p.counterterm)
		for p in parameterct:
			print(p.counterterm)

	def write_qgraf_file(self, f, order_names):
		trunc_model = [self.model_orig]
		while len(trunc_model[-1]) > 70:
			s = trunc_model[-1]
			trunc_model[-1] = s[:69]
			trunc_model.append(s[69:])

		f.write("% vim: syntax=none\n\n")
		f.write("% This file has been generated from the FeynRule model files\n")
		f.write("%% in %s\n" % ("\\\n% ".join(trunc_model)))
		f.write("[ model = '%s' ]\n\n" % self.model_name)
		f.write("[ fmrules = '%s' ]\n\n" % self.model_name)

		f.write("%---#[ Propagators:\n")
		for p in self.all_particles:
			if p.pdg_code < 0:
				continue

			f.write("%% %s -- %s Propagator (PDG: %d)\n"
					% (p.name, p.antiname, p.pdg_code))

			field, afield = canonical_field_names(p)

			pmass = str(p.mass)
			pwidth = str(p.width)

			if pmass == "0" or pmass == "ZERO":
				mass = 0
			else:
				mass = self.prefix + pmass

			if p.spin % 2 == 1:
				try:
					if p.GhostNumber is not None:
						if p.GhostNumber == 1:
							sign = "-"
						else:
							sign = "+"
					else:
						sign = "+"
				except AttributeError:
					sign = "+"

				if mass == 0:
					options = ", notadpole"
				else:
					options = ""
			else:
				sign = "-"
				options = ""

			if pwidth == "0" or pwidth == "ZERO":
				width = "0"
			else:
				width = self.prefix + pwidth

			if not p.propagating:
				aux = "+1"
			else:
				aux = "+0"

			try:
				if p.CustomSpin2Prop:
					if not p.propagating:
						error("Particle %s with CustomSpin2Prop has to propagate." % p.name)
					aux = "+2"
			except AttributeError:
				pass

			if p.selfconjugate:
				conj = "('+')"
			elif p.pdg_code in [24,-24]:
				conj = "('+','+')"
			else:
				conj = "('+','-')"

			f.write("[%s,%s,%s%s;TWOSPIN='%d',COLOR='%d',\n"
				% (field, afield, sign, options, abs(p.spin)-1, abs(p.color)))
			f.write("    MASS='%s', WIDTH='%s',\n"
				% (mass, width))
			f.write("    AUX='%s', CONJ=%s]\n"
				% (aux, conj))
					
		f.write("%---#] Propagators:\n")
		f.write("%---#[ Vertices:\n")

		lwf = LimitedWidthOutputStream(f, 70)

		for c in self.all_couplings:
			keys = [key for key in list(c.order.keys()) if key[0:1].isdigit()]
			for k in keys:
				c.order["O%s" % k] = c.order[k]
				del c.order[k]
		orders = set()
		for c in self.all_couplings:
			orders.update(list(c.order.keys()))
		
		for el in order_names:
			if not(el in orders):
				warning(("Specified order name %s is not present in UFO model and, hence, has no effect." %  (el)))
		orders.update(order_names)

		for v in self.all_vertices:
			particles = v.particles
			names = []
			fields = []
			afields = []
			spins = []
			for p in particles:
				names.append(p.name)
				cn = canonical_field_names(p)
				fields.append(cn[0])
				afields.append(cn[1])
				spins.append(p.spin - 1)

			deg = len(fields)
			if deg >= 7:
			   warning(("Vertex %s is %d-point and therefore not supported by qgraf. It is skipped." %  (v.name, deg)))
			   continue
			   assert False

			flip = spins[0] == 1 and spins[2] == 1

			vfunctions = {}
			vertorders = []
			for coord, coupling in sorted(list(v.couplings.items()),key=lambda x: x[0]):
				for name in orders:
					if name in coupling.order:
						vfunctions[name] = coupling.order[name]
					else:
						vfunctions[name] = 0

				ic, il = coord
				vfunctions["RK"] = v.lorentz[il].rank

				if not vfunctions in vertorders:
					if len(vertorders) > 0:
						warning(("Vertex %s has ambiguous structure of powers:\n %s and %s.\n "
									% (v.name, vertorders, vfunctions))
										+ "I will split it up.")
					vfcp = copy.deepcopy(vfunctions)
					vertorders.append(vfcp)


			for ivo in range(len(vertorders)):
				f.write("%% %s: %s Vertex" % ( v.name+"_"+str(ivo), " -- ".join(names)))
				lwf.nl()
				lwf.write("[")
				is_first = True

				xfields = afields[:]
				if flip:
					xfields[0] = afields[1]
					xfields[1] = afields[0]

				for field in xfields:
					if is_first:
						is_first = False
					else:
						lwf.write(",")
					lwf.write(field)
				lwf.write(";")
				lwf.write("isCT='0',")
				if 'NP' in vertorders[ivo]:
					flagNP = 1 if vertorders[ivo]['NP']!=0 else 0
					lwf.write("isNP='%s'," % str(flagNP))
				is_first = True
				for name, power in list(vertorders[ivo].items()):
					if is_first:
						is_first = False
					else:
						lwf.write(",")
					lwf.write("%s='%-d'" % (name, power))
				lwf.write(",VL='%s'" % (v.name+"_"+str(ivo)))
				lwf.write("]")
				lwf.nl()

		f.write("%---#] Vertices:\n\n")
		if self.useCT:
			f.write("%---#[ CTVertices:\n")

			lwf = LimitedWidthOutputStream(f, 70)

			for c in self.all_CTcouplings:
				keys = [key for key in list(c.order.keys()) if key[0:1].isdigit()]
				for k in keys:
					c.order["O%s" % k] = c.order[k]
					del c.order[k]
			orders = set()
			for c in self.all_CTcouplings:
				orders.update(list(c.order.keys()))

			for el in order_names:
				if not(el in orders):
					warning(("Specified order name %s is not present in UFO model and, hence, has no effect." %  (el)))
			orders.update(order_names)

			for v in self.all_CTvertices:
				particles = v.particles
				names = []
				fields = []
				afields = []
				spins = []
				for p in particles:
					names.append(p.name)
					cn = canonical_field_names(p)
					fields.append(cn[0])
					afields.append(cn[1])
					spins.append(p.spin - 1)

				deg = len(fields)
				if deg >= 7:
					warning(("Vertex %s is %d-point and therefore not supported by qgraf. It is skipped." %  (v.name, deg)))
					continue
					assert False

				flip = spins[0] == 1 and spins[2] == 1

				vfunctions = {}
				vertorders = []
				for coord, coupling in sorted(list(v.couplings.items()),key=lambda x: x[0]):
					for name in orders:
						if name in coupling.order:
							vfunctions[name] = coupling.order[name]
						else:
							vfunctions[name] = 0

					ic, il, ip = coord
					vfunctions["RK"] = v.lorentz[il].rank

					if not vfunctions in vertorders:
						if len(vertorders) > 0:
							warning(("CTVertex %s has ambiguous structure of powers:\n %s and %s.\n "
										% (v.name, vertorders, vfunctions))
											+ "I will split it up.")
						vfcp = copy.deepcopy(vfunctions)
						vertorders.append(vfcp)


				for ivo in range(len(vertorders)):
					f.write("%% %s: %s CTVertex" % ( v.name+"_"+str(ivo), " -- ".join(names)))
					lwf.nl()
					lwf.write("[")
					is_first = True

					xfields = afields[:]
					if flip:
						xfields[0] = afields[1]
						xfields[1] = afields[0]

					for field in xfields:
						if is_first:
							is_first = False
						else:
							lwf.write(",")
						lwf.write(field)
					lwf.write(";")
					lwf.write("isCT='1',")
					if 'NP' in vertorders[ivo]:
						flagNP = 1 if vertorders[ivo]['NP']!=0 else 0
						lwf.write("isNP='%s'," % str(flagNP))
					is_first = True
					for name, power in list(vertorders[ivo].items()):
						if is_first:
							is_first = False
						else:
							lwf.write(",")
						lwf.write("%s='%-d'" % (name, power))
					lwf.write(",VL='%s'" % (v.name+"_"+str(ivo)))
					lwf.write("]")
					lwf.nl()

			f.write("%---#] CTVertices:\n\n")

	def write_form_file(self, f, order_names):
		parser = ex.ExpressionParser()
		lorex = {}
		lsubs = {}
		lcounter = [0]
		dummy_found = {}
		for l in self.all_lorentz:
			name = l.name
			structure = parser.compile(l.structure)
			structure = structure.replaceStrings(
					"ModelDummyIndex", lsubs, lcounter)
			structure = structure.replaceNegativeIndices(0, "MDLIndex%d",
					dummy_found)
			structure = structure.replaceFloats(self.prefix + "float", self.floatsd, self.floatsc)
			for i in [2]:
				structure = structure.algsubs(
					ex.FloatExpression("%d." % i),
					ex.IntegerExpression("%d" % i))
			lorex[name] = transform_lorentz(structure, l.spins)
		lwf = LimitedWidthOutputStream(f, 70, 6)
		f.write("* vim: syntax=form:ts=3:sw=3\n\n")
		f.write("* This file has been generated from the FeynRule model files\n")
		f.write("* in %s\n\n" % self.model_orig)

		f.write("*---#[ Symbol Definitions:\n")
		f.write("*---#[ Coupling Orders:\n")
		f.write("AutoDeclare Symbols RK")
		for el in order_names:
			f.write(",%s" % el)
		f.write(",isCT")
		if 'NP' in order_names:
			f.write(",isNP")
		f.write(";\n")
		f.write("Symbol Lambdam1,Lambdam2,Loopfac;")
		f.write("\n")
		f.write("*---#] Coupling Orders:\n")
		f.write("*---#[ Fields:\n")

		fields = []
		for p in self.all_particles:
			part, anti = canonical_field_names(p)
			field = "[field.%s]" % part
			if field not in fields:
				fields.append(field)
			if part != anti:
				field = "[field.%s]" % anti
				if field not in fields:
					fields.append(field)

		if len(fields) > 0:
			if len(fields) == 1:
				f.write("Symbol %s;" % fields[0])
			else:
				f.write("Symbols")
				lwf.nl()
				lwf.write(fields[0])
				for p in fields[1:]:
					lwf.write(",")
					lwf.write(p)
				lwf.write(";")
		f.write("\n")
		f.write("*---#] Fields:\n")
		f.write("*---#[ Parameters:\n")

		params = []
		for p in self.all_parameters:
			params.append(self.prefix + p.name.replace("_","undrscr"))

		for c in self.all_couplings:
			params.append(self.prefix + c.name.replace("_", ""))

		if len(params) > 0:
			if len(params) == 1:
				f.write("Symbol %s;" % params[0])
			else:
				f.write("Symbols")
				lwf.nl()
				lwf.write(params[0])
				for p in params[1:]:
					lwf.write(",")
					lwf.write(p)
				lwf.write(";")

		f.write("\n")

		if self.useCT:
			ctparams = [self.prefix + c.name.replace("_", "") for c in self.all_CTcouplings]
			if len(ctparams) > 0:
				if len(ctparams) == 1:
					f.write("Symbol %s;" % ctparams[0] + "eftctcpl")
				else:
					f.write("Symbols")
					lwf.nl()
					lwf.write(ctparams[0] + "eftctcpl")
					for ctp in ctparams[1:]:
						lwf.write(",")
						lwf.write(ctp + "eftctcpl")
					lwf.write(";")

			f.write("\n")

		if len(self.floats) == 1:
			f.write("Symbol %s;\n" % self.floats[0])
		elif len(self.floats) > 1:
			f.write("Symbols")
			lwf.nl()
			lwf.write(self.floats[0])
			for p in self.floats[1:]:
				lwf.write(",")
				lwf.write(p)
			lwf.write(";\n")

		f.write("AutoDeclare Indices ModelDummyIndex, MDLIndex;\n")
		f.write("*---#] Parameters:\n")
		max_deg = max([len(v.particles) for v in self.all_vertices])
		f.write("*---#[ Auxilliary Symbols:\n")
		f.write("Vectors vec1, ..., vec%d;\n" % max_deg)
		f.write("*---#] Auxilliary Symbols:\n")
		f.write("*---#] Symbol Definitions:\n")
		if self.containsMajoranaFermions():
			f.write("* Model contains Majorana Fermions:\n")
			debug("You are working with a model " +
					"that contains Majorana fermions.")
			f.write("#Define DISCARDQGRAFSIGN \"1\"\n")
		f.write("#Define USEVERTEXPROC \"1\"\n")
		f.write("*---#[ Procedure ReplaceVertices :\n")
		f.write("#Procedure ReplaceVertices\n")

		orders = set()
		orders.update(list(order_names))

		for v in self.all_vertices:
			particles = v.particles
			names = []
			fields = []
			afields = []
			spins = []
			for p in particles:
				names.append(p.name)
				cn = canonical_field_names(p)
				fields.append(cn[0])
				afields.append(cn[1])
				spins.append(p.spin - 1)

			vorders = {}
			vertorders = []
			cplnames = []
			for coord, coupling in list(v.couplings.items()):
				for name in orders:
					if name in coupling.order:
						vorders[name] = coupling.order[name]
					else:
						vorders[name] = 0

				ic, il = coord
				vorders["RK"] = v.lorentz[il].rank

				if vorders in vertorders:
					cplnames[vertorders.index(vorders)].append(coupling.name)
				else:
					if len(vertorders) > 0:
						warning(("Vertex %s has ambiguous structure of powers:\n %s and %s.\n "
									% (v.name, vertorders, vorders))
										+ "I will split it up.")
					vocp = copy.deepcopy(vorders)
					vertorders.append(vocp)
					cplnames.append([coupling.name])

			for ivo in range(len(vertorders)):

				flip = spins[0] == 1 and spins[2] == 1
				deg = len(particles)

				xidx = list(range(deg))
				if flip:
					xidx[0] = 1
					xidx[1] = 0

				fold_name = "(%s) %s Vertex" % ( v.name+"_"+str(ivo), " -- ".join(names))
				f.write("*---#[ %s:\n" % fold_name)
				if 'NP' in vertorders[ivo]:
					flagNP = 1 if vertorders[ivo]['NP']!=0 else 0
					f.write("Identify Once vertex(iv?, isCT0, isNP%s, RK%d" % (str(flagNP), vertorders[ivo]["RK"]))
				else:
					f.write("Identify Once vertex(iv?, isCT0, RK%d" % vertorders[ivo]["RK"])
				for el in order_names:
					f.write(", %s%d"
						% (el,vertorders[ivo][el]))
				colors = []
				for i in xidx:
					p = particles[i]
					field = afields[i]
					anti = fields[i]
					color = abs(p.color)
					spin = abs(p.spin) - 1
					if field.startswith("anti") and not p.pdg_code in [24,-24]:
						spin = - spin
						color = - color
					colors.append(color)

					f.write(",\n   [field.%s], idx%d?,%d,vec%d?,idx%dL%d?,%d,idx%dC%d?"
							% (field, i+1, spin, i+1, i+1, abs(spin), color, i+1,
								abs(color)))
				f.write(") =")
			
				if 'NP' in vertorders[ivo].keys():
					if 'QL' in vertorders[ivo].keys():
						f.write("\n  Lambdam2^%d * Loopfac^%d * (" % (vertorders[ivo]['NP'],vertorders[ivo]['QL']))
					else:
						f.write("\n  Lambdam2^%d * (" % (vertorders[ivo]['NP']))
				elif 'QL' in vertorders[ivo].keys():
					f.write("\n  Loopfac^%d * (" % (vertorders[ivo]['QL']))


				dummies = []

				brack_flag = False
				for i, s in enumerate(spins):
					if s == 3 or s == 4:
						brack_flag = True
						idx = "idx%dL%d" % (i+1, s)
						idxa = "idx%dL%da" % (i+1, s)
						idxb = "idx%dL%db" % (i+1, s)
						f.write("\n SplitLorentzIndex(%s, %s, %s) *" % (idx, idxa, idxb))
						dummies.append(idxa)
						dummies.append(idxb)

				if brack_flag:
					f.write(" (")


				for coord, coupling in sorted(list(v.couplings.items()),key=lambda x: x[0]):
					if not coupling.name in cplnames[ivo]:
						continue
					ic, il = coord
					lorentz = lorex[v.lorentz[il].name]
					scolor = v.color[ic]
					f.write("\n   + %s"
							% (self.prefix + coupling.name.replace("_", "")))
					if scolor != "1":
						color = parser.compile(scolor)
						color = color.replaceStrings("ModelDummyIndex", lsubs, lcounter)
						color = color.replaceNegativeIndices(0, "MDLIndex%d",
								dummy_found)
						color = transform_color(color, colors, xidx)
						if lorentz == ex.IntegerExpression(1):
							expr = color
						else:
							expr = color * lorentz
					else:
						expr = lorentz
					if not expr == ex.IntegerExpression(1):
						f.write(" * (")
						lwf.nl()
						expr.write(lwf)
						f.write("\n   )")
			
					for ind in list(lsubs.values()):
						s = str(ind)
						if expr.dependsOn(s):
							if s not in dummies:
								dummies.append(s)

				if brack_flag:
					f.write(")")
				if 'NP' in vertorders[ivo].keys() or 'QL' in vertorders[ivo].keys():
					f.write("\n)")
				f.write(";\n")

				for idx in list(dummy_found.values()):
					dummies.append(str(idx))

				if len(dummies) > 0:
					f.write("Sum %s;\n" % ", ".join(dummies))
				f.write("*---#] %s:\n" % fold_name)

		if self.useCT:

			for v in self.all_CTvertices:
				particles = v.particles
				names = []
				fields = []
				afields = []
				spins = []
				for p in particles:
					names.append(p.name)
					cn = canonical_field_names(p)
					fields.append(cn[0])
					afields.append(cn[1])
					spins.append(p.spin - 1)

				vorders = {}
				vertorders = []
				cplnames = []
				for coord, coupling in list(v.couplings.items()):
					for name in orders:
						if name in coupling.order:
							vorders[name] = coupling.order[name]
						else:
							vorders[name] = 0

					ic, il, ip = coord
					vorders["RK"] = v.lorentz[il].rank

					if vorders in vertorders:
						cplnames[vertorders.index(vorders)].append(coupling.name)
					else:
						if len(vertorders) > 0:
							warning(("Vertex %s has ambiguous structure of powers:\n %s and %s.\n "
										% (v.name, vertorders, vorders))
											+ "I will split it up.")
						vocp = copy.deepcopy(vorders)
						vertorders.append(vocp)
						cplnames.append([coupling.name])

				for ivo in range(len(vertorders)):

					flip = spins[0] == 1 and spins[2] == 1
					deg = len(particles)

					xidx = list(range(deg))
					if flip:
						xidx[0] = 1
						xidx[1] = 0

					fold_name = "(%s) %s CTVertex" % ( v.name+"_"+str(ivo), " -- ".join(names))
					f.write("*---#[ %s:\n" % fold_name)
					if 'NP' in vertorders[ivo]:
						flagNP = 1 if vertorders[ivo]['NP']!=0 else 0
						f.write("Identify Once vertex(iv?, isCT1, isNP%s, RK%d" % (str(flagNP), vertorders[ivo]["RK"]))
					else:
						f.write("Identify Once vertex(iv?, isCT1, RK%d" % vertorders[ivo]["RK"])
					for el in order_names:
						f.write(", %s%d"
							% (el,vertorders[ivo][el]))
					colors = []
					for i in xidx:
						p = particles[i]
						field = afields[i]
						anti = fields[i]
						color = abs(p.color)
						spin = abs(p.spin) - 1
						if field.startswith("anti") and not p.pdg_code in [24,-24]:
							spin = - spin
							color = - color
						colors.append(color)

						f.write(",\n   [field.%s], idx%d?,%d,vec%d?,idx%dL%d?,%d,idx%dC%d?"
								% (field, i+1, spin, i+1, i+1, abs(spin), color, i+1,
									abs(color)))
					f.write(") =")

					if 'NP' in vertorders[ivo].keys():
						if 'QL' in vertorders[ivo].keys():
							f.write("\n  Lambdam2^%d * Loopfac^%d * (" % (vertorders[ivo]['NP'],vertorders[ivo]['QL']))
						else:
							f.write("\n  Lambdam2^%d * (" % (vertorders[ivo]['NP']))
					elif 'QL' in vertorders[ivo].keys():
						f.write("\n  Loopfac^%d * (" % (vertorders[ivo]['QL']))


					dummies = []

					brack_flag = False
					for i, s in enumerate(spins):
						if s == 3 or s == 4:
							brack_flag = True
							idx = "idx%dL%d" % (i+1, s)
							idxa = "idx%dL%da" % (i+1, s)
							idxb = "idx%dL%db" % (i+1, s)
							f.write("\n SplitLorentzIndex(%s, %s, %s) *" % (idx, idxa, idxb))
							dummies.append(idxa)
							dummies.append(idxb)

					if brack_flag:
						f.write(" (")


					for coord, coupling in sorted(list(v.couplings.items()),key=lambda x: x[0]):
						if not coupling.name in cplnames[ivo]:
							continue
						ic, il, ip = coord
						lorentz = lorex[v.lorentz[il].name]
						scolor = v.color[ic]
						f.write("\n   + %s"
								% (self.prefix + coupling.name.replace("_", "") + "eftctcpl"))
						if scolor != "1":
							color = parser.compile(scolor)
							color = color.replaceStrings("ModelDummyIndex", lsubs, lcounter)
							color = color.replaceNegativeIndices(0, "MDLIndex%d",
									dummy_found)
							color = transform_color(color, colors, xidx)
							if lorentz == ex.IntegerExpression(1):
								expr = color
							else:
								expr = color * lorentz
						else:
							expr = lorentz
						if not expr == ex.IntegerExpression(1):
							f.write(" * (")
							lwf.nl()
							expr.write(lwf)
							f.write("\n   )")

						for ind in list(lsubs.values()):
							s = str(ind)
							if expr.dependsOn(s):
								if s not in dummies:
									dummies.append(s)

					if brack_flag:
						f.write(")")
					if 'NP' in vertorders[ivo].keys() or 'QL' in vertorders[ivo].keys():
						f.write("\n)")
					f.write(";\n")

					for idx in list(dummy_found.values()):
						dummies.append(str(idx))

					if len(dummies) > 0:
						f.write("Sum %s;\n" % ", ".join(dummies))
					f.write("*---#] %s:\n" % fold_name)

		f.write("#EndProcedure\n")
		f.write("*---#] Procedure ReplaceVertices :\n")

		f.write("*---#[ Dummy Indices:\n")
		for ind in list(lsubs.values()):
			f.write("Index %s;\n" % ind)
		f.write("*---#] Dummy Indices:\n")
		f.write("""\
*---#[ Procedure VertexConstants :
#Procedure VertexConstants
* Just a dummy, all vertex constants are already
* replaced in ReplaceVertices.
*
* This procedure might disappear in any future version of Golem
* so don't rely on it.
*
#EndProcedure
*---#] Procedure VertexConstants :
""")

	def write_formct_file(self, f):
		parser = ex.ExpressionParser()
		lorex = {}
		lsubs = {}
		lcounter = [0]
		dummy_found = {}
		for l in self.all_lorentz:
			name = l.name
			structure = parser.compile(l.structure)
			structure = structure.replaceStrings(
					"ModelDummyIndex", lsubs, lcounter)
			structure = structure.replaceNegativeIndices(0, "MDLIndex%d",
					dummy_found)
			for i in range(2,33):
				structure = structure.algsubs(
					ex.FloatExpression("%d." % i),
					ex.IntegerExpression("%d" % i))


		lwf = LimitedWidthOutputStream(f, 70, 6)
		f.write("* vim: syntax=form:ts=3:sw=3\n\n")
		f.write("* This file has been generated from the FeynRule model files\n")
		f.write("* in %s\n" % self.model_orig)
		f.write("* for Counter Term Vertices\n\n")

		f.write("*---#[ Symbol Definitions:\n")
		f.write("*---#[ Parameters:\n")

		params = []
		for c in self.all_CTcouplings:
			params.append(self.prefix + c.name.replace("_", ""))

		if len(params) > 0:
			if len(params) == 1:
				f.write("Symbol %s;" % params[0])
			else:
				f.write("Symbols")
				lwf.nl()
				lwf.write(params[0])
				for p in params[1:]:
					lwf.write(",")
					lwf.write(p)
				lwf.write(";")

		f.write("\n")

		if len(self.floats) == 1:
			f.write("Symbol %s;\n" % self.floats[0])
		elif len(self.floats) > 1:
			f.write("Symbols")
			lwf.nl()
			lwf.write(self.floats[0])
			for p in self.floats[1:]:
				lwf.write(",")
				lwf.write(p)
			lwf.write(";\n")

		f.write("AutoDeclare Indices ModelDummyIndex, MDLIndex;\n")
		f.write("*---#] Parameters:\n")
		f.write("*---#] Symbol Definitions:\n")
		f.write("*---#[ Procedure ReplaceCT :\n")
		f.write("#Procedure ReplaceCT\n")

		for v in self.all_CTvertices:
			particles = v.particles
			names = []
			fields = []
			afields = []
			for p in particles:
				names.append(p.name)
				cn = canonical_field_names(p)
				fields.append(cn[0])
				afields.append(cn[1])

			deg = len(particles)

			xidx = list(range(deg))

			fold_name = "(%s) %s CT" % ( v.name, " -- ".join(names))
			f.write("*---#[ %s:\n" % fold_name)
			f.write("Identify Once delta(mass")
			for i in xidx:
				p = particles[i]
				field = afields[i]
				f.write(",\n   [field.%s]" % field)
			f.write(") =")

			for coord, coupling in list(v.couplings.items()):
				ic, il = coord
				f.write("\n   + %s"
						% (self.prefix + coupling.name.replace("_", "")))
				for ind in list(lsubs.values()):
					s = str(ind)

			f.write(";\n")

			f.write("*---#] %s:\n" % fold_name)
		f.write("#EndProcedure\n")
		f.write("*---#] Procedure ReplaceCT :\n")




	def containsMajoranaFermions(self):
		for p in self.all_particles:
			if p.spin % 2 == 0 and p.selfconjugate:
				return True
		return False

	def store(self, path, local_name, order_names):
		message("  Writing Python file ...")
		with open(os.path.join(path, "%s.py" % local_name), 'w') as f:
			self.write_python_file(f)

		message("  Writing QGraf file ...")
		with open(os.path.join(path, local_name), 'w') as f:
			self.write_qgraf_file(f, order_names)

		message("  Writing Form file ...")
		with open(os.path.join(path, "%s.hh" % local_name), 'w') as f:
			self.write_form_file(f, order_names)

		#message("  Writing Form CT file ...")
		#with open(os.path.join(path, "%sct.hh" % local_name), 'w') as f:
			#self.write_formct_file(f)

def canonical_field_names(p):
	pdg_code = p.pdg_code
	if pdg_code < 0:
		canonical_name = "anti%d" % abs(pdg_code)
		if p.selfconjugate:
			canonical_anti = canonical_name
		else:
			canonical_anti = "part%d" % abs(pdg_code)
	else:
		canonical_name = "part%d" % pdg_code
		if p.selfconjugate:
			canonical_anti = canonical_name
		else:
			canonical_anti = "anti%d" % pdg_code

	return (canonical_name, canonical_anti)

lor_P = ex.SymbolExpression("P")
lor_Metric = ex.SymbolExpression("Metric")
lor_Epsilon = ex.SymbolExpression("Epsilon")
lor_Identity = ex.SymbolExpression("Identity")
lor_Gamma = ex.SymbolExpression("Gamma")
lor_ProjP = ex.SymbolExpression("ProjP")
lor_ProjM = ex.SymbolExpression("ProjM")

lor_ProjMinus = ex.SymbolExpression("ProjMinus")
lor_ProjPlus = ex.SymbolExpression("ProjPlus")
lor_Sm = ex.SymbolExpression("Sm")
lor_d = ex.SymbolExpression("d")
lor_d1 = ex.SymbolExpression("d_")
lor_NCContainer = ex.SymbolExpression("NCContainer")
lor_Gamma5 = ex.SymbolExpression("Gamma5")
lor_e = ex.SymbolExpression("e_")

def get_rank(expr):
	if isinstance(expr, ex.SumExpression):
		n = len(expr)
		lst = [get_rank(expr[i]) for i in range(n)]
		if len(lst) == 0:
			return 0
		else:
			return max(lst)


	elif isinstance(expr, ex.ProductExpression):
		n = len(expr)
		result = 0

		for i in range(n):
			sign, factor = expr[i]
			result += get_rank(factor)
		return result

	elif isinstance(expr, ex.PowerExpression):
		assert isinstance(expr.getExponent(), ex.IntegerExpression)
		return get_rank(expr.getBase())*(int(expr.getExponent()))

	elif isinstance(expr, ex.UnaryMinusExpression):
		return get_rank(expr.getTerm())

	elif isinstance(expr, ex.FunctionExpression):
		head = expr.getHead()
		args = expr.getArguments()
		if head == lor_P:
			return 1
		else:
			return 0
	else:
		return 0

def transform_lorentz(expr, spins):
	if isinstance(expr, ex.SumExpression):
		n = len(expr)
		return ex.SumExpression([transform_lorentz(expr[i], spins) 
			for i in range(n)])
	elif isinstance(expr, ex.ProductExpression):
		n = len(expr)
		new_factors = []

		for i in range(n):
			sign, factor = expr[i]
			new_factors.append( (sign, transform_lorentz(factor, spins)) )
		return ex.ProductExpression(new_factors)
	elif isinstance(expr, ex.PowerExpression):
		return ex.PowerExpression(
				transform_lorentz(expr.getBase(),spins),
				transform_lorentz(expr.getExponent(),spins)
				)
	elif isinstance(expr, ex.UnaryMinusExpression):
		return ex.UnaryMinusExpression(
				transform_lorentz(expr.getTerm(), spins)
			)
	elif isinstance(expr, ex.FunctionExpression):
		head = expr.getHead()
		args = expr.getArguments()
		if head == lor_P:
			# P(index, momentum)
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
			else:
				index = args[0]
			mom = ex.SymbolExpression("vec%d" % int(args[1]))
			# UFO files have all momenta outgoing:
			return -mom(index)
		elif head == lor_Metric or head == lor_Identity:
			my_spins = []
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
				my_spins.append(s)
			else:
				index1 = args[0]
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
				my_spins.append(s)
			else:
				index2 = args[1]

			if my_spins == [1, 1]:
				#return lor_d1(index1, index2)
				return lor_NCContainer(ex.IntegerExpression(1), index1, index2)
			else:
				return lor_d(index1, index2)
		elif head == lor_Gamma:
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
			else:
				index2 = args[1]
			if isinstance(args[2], ex.IntegerExpression):
				i = int(args[2])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index3 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
			else:
				index3 = args[2]
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				if i == 5:
					return lor_NCContainer(lor_Gamma5, index2, index3)
				else:
					i_particle = i % 1000
					i_index = i // 1000
					s = spins[i_particle-1] - 1
					if i_index == 1:
						suffix = "a"
					elif i_index == 2:
						suffix = "b"
					else:
						suffix = ""
					index1 = ex.SymbolExpression("idx%dL%d%s" %
							(i_particle, s, suffix))
			else:
				index1 = args[0]
			return lor_NCContainer(lor_Sm(index1), index2, index3)
		elif head == lor_Gamma5:
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
			else:
				index1 = args[0]
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				i_particle = i % 1000
				i_index = i // 1000
				s = spins[i_particle-1] - 1
				if i_index == 1:
					suffix = "a"
				elif i_index == 2:
					suffix = "b"
				else:
					suffix = ""
				index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
			else:
				index2 = args[2]
			return lor_NCContainer(lor_Gamma5, index1, index2)
		elif head == lor_ProjM:
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				s = spins[i-1] - 1
				index1 = ex.SymbolExpression("idx%dL%d" % (i, s))
			else:
				index1 = args[0]
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				s = spins[i-1] - 1
				index2 = ex.SymbolExpression("idx%dL%d" % (i, s))
			else:
				index2 = args[1]
			return lor_NCContainer(lor_ProjMinus, index1, index2)
		elif head == lor_ProjP:
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				s = spins[i-1] - 1
				index1 = ex.SymbolExpression("idx%dL%d" % (i, s))
			else:
				index1 = args[0]
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				s = spins[i-1] - 1
				index2 = ex.SymbolExpression("idx%dL%d" % (i, s))
			else:
				index2 = args[1]
			return lor_NCContainer(lor_ProjPlus, index1, index2)
		elif head == lor_Epsilon:
			arg_list=[]
			for ind in range(len(args)):
				if isinstance(args[ind], ex.IntegerExpression):
					i = int(args[ind])
					i_particle = i % 1000
					i_index = i // 1000
					s = spins[i_particle-1] - 1
					if i_index == 1:
						suffix = "a"
					elif i_index == 2:
						suffix = "b"
					else:
						suffix = ""
					index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
				else:
					index1 = args[ind]
				arg_list.append(index1)
			return lor_e(*arg_list)
		else:
			return expr
	else:
		return expr

col_T = ex.SymbolExpression("T")
col_f = ex.SymbolExpression("f")
col_Identity = ex.SymbolExpression("Identity")
col_d_ = ex.SymbolExpression("d_")
col_d8 = ex.SymbolExpression("dcolor8")
col_d3 = ex.SymbolExpression("dcolor")

def transform_color(expr, colors, xidx):
	if isinstance(expr, ex.SumExpression):
		n = len(expr)
		return ex.SumExpression([transform_color(expr[i], colors, xidx)
			for i in range(n)])
	elif isinstance(expr, ex.ProductExpression):
		n = len(expr)
		new_factors = []

		for i in range(n):
			sign, factor = expr[i]
			new_factors.append( (sign, transform_color(factor, colors, xidx)) )
		return ex.ProductExpression(new_factors)

	elif isinstance(expr, ex.UnaryMinusExpression):
		return ex.UnaryMinusExpression(
				transform_color(expr.getTerm(), colors, xidx)
			)
	elif isinstance(expr, ex.FunctionExpression):
		head = expr.getHead()
		args = expr.getArguments()
		if head == col_T or head == col_f:
			indices = []
			order = []
			xi = []
			for j in range(3):
				if isinstance(args[j], ex.IntegerExpression):
					i = int(args[j])
					x = xidx[i-1]
					c = abs(colors[x])
					order.append(colors[x])
					xi.append(x)
					indices.append(ex.SymbolExpression("idx%dC%d" % (x+1, c)))
				else:
					indices.append(args[j])
					order.append(0)
					xi.append(-1)
			if head == col_T:
				# Modification for Dirac-gluinos:
				if order[0]==-8:
					order[0]=8 # representation is real
				if order == [8, -3, 0]:
					order[2] = 3
				elif order == [8, 0, 3]:
					order[1] = -3
				elif order == [0, -3, 3]:
					order[0] = 8
				if order == [8, -3, 3]:
					return head(indices[0], indices[1], indices[2])
				elif order == [8, 3, -3]:
					return head(indices[0], indices[2], indices[1])
				else:
					error("Cannot recognize color assignment at vertex: %s" % order)
			else:
				return head(indices[0], indices[1], indices[2])
		if head == col_Identity:
			c = 0
			if isinstance(args[0], ex.IntegerExpression):
				i = int(args[0])
				c = abs(colors[i-1])
				index1 = ex.SymbolExpression("idx%dC%d" % (i, c))
			else:
				index1 = args[0]
			if isinstance(args[1], ex.IntegerExpression):
				i = int(args[1])
				c = abs(colors[i-1])
				index2 = ex.SymbolExpression("idx%dC%d" % (i, c))
			else:
				index2 = args[1]
			if c == 3:
				return col_d3(index1, index2)
			elif c == 8:
				return col_d8(index1, index2)
			else:
				return col_d_(index1, index2)
		else:
			return expr
	else:
		return expr

def load_ufo_files(mname, mpath):
	mfile = None
	try:
		if sys.version_info >= (3,6,):
			fpath = mpath[0]+'/'+mname+'/__init__.py'
			mod = load_source(mname,fpath)
		else:
			import imp
			mfile, mpath, mdesc = imp.find_module(mname, mpath)
			mod = imp.load_module(mname, mfile, mpath, mdesc)
	except ImportError as exc:
		error("Problem importing model file: %s" % exc)
	finally:
		if mfile is not None:
			mfile.close()
	return mod
