# vim: ts=3:sw=3

import StringIO
from golem.util.config import Properties
from golem.util.parser import Template
import golem.util.tools
import golem.model.expressions as ex
from golem.model.feynrules import cmath_functions, shortcut_functions, \
		unprefixed_symbols, sym_cmath, sym_cmplx, i_

class ModelTemplate(Template):
	"""
	Implements a template that knows the particle content
	and the parameters of a model.
	"""

	def init_model(self, conf):
		"""
		PARAMETER

		conf -- the configuration from which the model information is extracted.
		"""
		self._zeroes = golem.util.tools.getZeroes(conf)
		self._ones = conf.getProperty(golem.properties.one)
		self._mod = golem.util.tools.getModel(conf)
		self._model = self._mod.model_name
		self._modeltype =  conf.getProperty("modeltype")
		if not self._modeltype:
			self._modeltype = conf.getProperty("model")

		self._comment_chars = ['#', '!', ';']
		self._buffer_length = 80

		self._parameters = {}
		self._functions = {}
		self._ct_functions = {}
		name_length = 0
		self._floats = {}
		self._functions_fortran = {}
		
		for name, value in self._mod.parameters.items():
			t = self._mod.types[name]
			if len(name) > name_length:
				name_length = len(name)

			if name in self._zeroes:
				if not t.endswith('P'):
					t = t + 'P'
				param = (name, t, ["0.0", "0.0"])
			elif name in self._ones:
				if not t.endswith('P'):
					t = t + 'P'
				param = (name, t, ["1.0", "0.0"])
			else:
				if isinstance(value, list):
					param = (name, t, value)
				else:
					param = (name, t, [value, "0.0"])
			self._parameters[name] = param		
		
		for name, expression in self._mod.functions.items():
			t = self._mod.types[name]
			#if len(name) > name_length:
			#	name_length = len(name)

			self._functions[name] = t
			
		try:
		    for name, expression in self._mod.ct_functions.items():
			    t = self._mod.types[name]
			    self._ct_functions[name] = t
			    self._functions[name] = t
		except:
		     pass

		
		self._name_length = name_length

		props = Properties()

		props.setProperty("model", self._model)
		props.setProperty("modeltype", self._modeltype)
		props.setProperty("name_length", str(name_length))
		props.setProperty("len_comment_chars", str(len(self._comment_chars)))
		props.setProperty("buffer_length", str(self._buffer_length))

		self._globals = props

		self._slha_blocks = {}
		self._slha_locations = {}

		for name, value in self._mod.slha_locations.items():
			n, t, v = self._parameters[name]
			if t == "RP" or t == "CP":
				continue
			self._slha_locations[name] = value

			block, coords = value
			d = len(coords)
			if block in self._slha_blocks:
				if d != self._slha_blocks[block]:
					golem.util.tools.error("Incompatible entries for SLHA block %s"
							% block)
			else:
				self._slha_blocks[block] = d

		self._slha_entry_stack = []

		model_options = conf.getProperty(golem.properties.model_options)
		if "ewchoose" in golem.model.MODEL_OPTIONS:
			props.setProperty("ewchoose", str(golem.model.MODEL_OPTIONS["ewchoose"]))
		else:
			golem.model.MODEL_OPTIONS["ewchoose"] = False

		ones = conf.getProperty(golem.properties.one)

		props.setProperty("e_not_one", not "e" in ones)
		props.setProperty("gs_not_one", not "gs" in ones)
		props.setProperty("alpha_not_one", not "alpha" in ones)

	def add_kinematics_parameters(self, in_particles, out_particles):

		def add_param(name, value):
			if name in self._zeroes:
				self._parameters[name] = (name, "CP", ["0.0", "0.0"])
			elif name in self._ones:
				self._parameters[name] = (name, "CP", ["1.0", "0.0"])
			else:
				self._parameters[name] = (name, "C", [str(value), "0.0"])

			l = len(name)
			if l > self._name_length:
				self._name_length = l
				self._globals["name_length"] = str(l)
		############# END FUNCTION add_param #####################

		k = 0
		for inp in in_particles:
			k += 1
			twospin = inp.getSpin()

			if twospin == 2 or twospin == -2:
				add_param("gauge%dz" % k, 0.0)

		for out in out_particles:
			k += 1
			twospin = out.getSpin()

			if twospin == 2 or twospin == -2:
				add_param("gauge%dz" % k, 0.0)


	def __call__(self, *conf):
		for chunk in Template.__call__(self, self._globals, *conf):
			yield chunk

	def functions_resolved(self, *args, **opts):
		type_filter = self._setup_filter(["R", "C"], args)

		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		type_name  = self._setup_name("type", "type", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")


		parser = golem.model.expressions.ExpressionParser()
		functions = {}
		i = 0
		for name, value in model_mod.functions.items():
			i += 1
			if i % 100 == 0:
				golem.util.tools.message("  (%5d/%5d)" % (i, nfunctions))
			expr = parser.compile(value)
			functions[name] = expr
			
			
		golem.util.tools.message("Resolving dependencies between functions ...")
		program = golem.model.expressions.resolve_dependencies(functions)			

		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = functions[name]
			buf = StringIO.StringIO()
			try:
				ast.write(buf)

				type = self._functions[name]

				props.setProperty(name_name, name)
				props.setProperty(type_name, type)
				props.setProperty(expression_name, buf.getvalue())
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			finally:
				buf.close()
			yield props




	def functions_resolved_sum (self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")


		parser = golem.model.expressions.ExpressionParser()
		functions = {}
		i = 0
		for name, value in model_mod.functions.items():
			i += 1
			if i % 100 == 0:
				golem.util.tools.message("  (%5d/%5d)" % (i, nfunctions))
			expr = parser.compile(value)
			functions[name] = expr
			
		try:
		    for name, valuestr in model_mod.ct_functions.items():
			    content = valuestr[1:-1]
			    items = content.split(',')
			    pairs = [item.split(':',1) for item in items]
			    value = dict((k,str(v)) for (k,v) in pairs)
			    if '0' in value.keys():
			      expr0 = parser.compile(value['0'])
			    else:
			      expr0 = parser.compile('0')
			    if '-1' in value.keys():
			      expr1 = parser.compile(value['-1'])
			    else:
			      expr1 = parser.compile('0')
			    name0=name+'(0)'  
			    name1=name+'(1)'
			    functions[name0]= expr0
			    functions[name1]= expr1
		except:
		      pass
		
		
		golem.util.tools.message("Resolving dependencies between functions ...")
		program = golem.model.expressions.resolve_dependencies(functions)			

		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = functions[name]
			buf = StringIO.StringIO()
			try:
				ast.write(buf)

				props.setProperty(name_name, name)
				props.setProperty(expression_name, buf.getvalue())
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			finally:
				buf.close()
			yield props



	def ct_functions_resolved_name(self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")


		parser = golem.model.expressions.ExpressionParser()
		ct_functions = {}
		i = 0
		
		try:
		    for name, valuestr in model_mod.ct_functions.items():
			    content = valuestr[1:-1]
			    items = content.split(',')
			    pairs = [item.split(':',1) for item in items]
			    value = dict((k,str(v)) for (k,v) in pairs)
			    ct_functions[name]= parser.compile('0')
		except:
		    pass
			
		golem.util.tools.message("Resolving dependencies between ct_functions ...")
		program = golem.model.expressions.resolve_dependencies(ct_functions)			

		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = ct_functions[name]
			buf = StringIO.StringIO()
			try:
				ast.write(buf)

				props.setProperty(name_name, name)
				props.setProperty(expression_name, buf.getvalue())
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			finally:
				buf.close()
			yield props


	def ct_functions_resolved(self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")


		parser = golem.model.expressions.ExpressionParser()
		ct_functions = {}
		i = 0
		
		try:
		    for name, valuestr in model_mod.ct_functions.items():
			    content = valuestr[1:-1]
			    items = content.split(',')
			    pairs = [item.split(':',1) for item in items]
			    value = dict((k,str(v)) for (k,v) in pairs)
			    if '0' in value.keys():
			      expr0 = parser.compile(value['0'])
			    else:
			      expr0 = parser.compile('0')
			    if '-1' in value.keys():
			      expr1 = parser.compile(value['-1'])
			    else:
			      expr1 = parser.compile('0')
			    name0=name+'(0)'  
			    name1=name+'(1)'
			    ct_functions[name0]= expr0
			    ct_functions[name1]= expr1
		except:
		      pass
			
		golem.util.tools.message("Resolving dependencies between ct_functions ...")
		program = golem.model.expressions.resolve_dependencies(ct_functions)			

		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = ct_functions[name]
			buf = StringIO.StringIO()
			try:
				ast.write(buf)

				props.setProperty(name_name, name)
				props.setProperty(expression_name, buf.getvalue())
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			finally:
				buf.close()
			yield props


	def functions_resolved_reversed(self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")


		parser = golem.model.expressions.ExpressionParser()
		functions = {}
		i = 0
		for name, value in model_mod.functions.items():
			i += 1
			if i % 100 == 0:
				golem.util.tools.message("  (%5d/%5d)" % (i, nfunctions))
			expr = parser.compile(value)
			functions[name] = expr
			
		try:
		    for name, valuestr in model_mod.ct_functions.items():
			    content = valuestr[1:-1]
			    items = content.split(',')
			    pairs = [item.split(':',1) for item in items]
			    value = dict((k,str(v)) for (k,v) in pairs)
			    if '0' in value.keys():
			      expr0 = parser.compile(value['0'])
			    else:
			      expr0 = parser.compile('0')
			    if '-1' in value.keys():
			      expr1 = parser.compile(value['-1'])
			    else:
			      expr1 = parser.compile('0')
			    name0=name+'(0)'  
			    name1=name+'(1)'
			    functions[name0]= expr0
			    functions[name1]= expr1
		except:
		    pass
	
		golem.util.tools.message("Resolving dependencies between functions ...")
		program = golem.model.expressions.resolve_dependencies(functions)
		# the only difference
		program.reverse()

		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = functions[name]
			buf = StringIO.StringIO()
			try:
				ast.write(buf)

				props.setProperty(name_name, name)
				props.setProperty(expression_name, buf.getvalue())
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			finally:
				buf.close()
			yield props
		
	def has_slha_locations(self, *args, **opts):
		return len(self._slha_blocks) > 0

	def slha_blocks(self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)

		if "shift" in opts:
			i = int(opts["shift"])
		else:
			i = 0

		lst = []
		if "dimension" in opts:
			d = int(opts["dimension"])
			for name, value in self._slha_blocks.items():
				if value == d:
					lst.append( (i, name) )
				i += 1
		else:
			for name, value in self._slha_blocks.items():
				lst.append( (i, name) )
				i += 1

		if "reversed" in args:
			lst.reverse()

		to_upper = "upper" in args
		to_lower = "lower" in args

		if len(lst) > 0:
			last_index, last_block = lst[-1]
		props = Properties()
		is_first = True

		for index, name in lst:
			s = name
			if to_upper:
				s = s.upper()
			elif to_lower:
				s = s.lower()
			props.setProperty(first_name, is_first)
			props.setProperty(last_name, index == last_index)
			props.setProperty(name_name, s)
			props.setProperty(index_name, index)

			is_first = False

			entries = {}
			for varname, value in self._slha_locations.items():
				block, coords = value

				if block == name:
					entries[varname] = coords
					
			self._slha_entry_stack.append(entries)
			yield props
			self._slha_entry_stack.pop()

	def slha_entries(self, *args, **opts):
		entries = self._slha_entry_stack[-1]

		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		to_upper = "upper" in args
		to_lower = "lower" in args

		classes = {}
		yield_list = {}
		for varname, coords in entries.items():
			if len(coords) == 1:
				yield_list[coords[0]] = varname
			else:
				cls = coords[0]
				if cls not in classes:
					classes[cls] = {}
				classes[cls][varname] = coords[1:]

		if len(classes) > 0 and len(yield_list) > 0:
			golem.util.tools.error("Some SLHA block has an odd shape!")

		props = Properties()
		if len(classes) > 0:
			count = 0
			goal = len(classes)
			is_first = True
			for index, entries in classes.items():
				count += 1
				is_last = count == goal
				props.setProperty(first_name, is_first)
				props.setProperty(last_name, is_last)
				is_first = False

				props.setProperty(index_name, index)
				self._slha_entry_stack.append(entries)
				yield props
				self._slha_entry_stack.pop()
		elif len(yield_list) > 0:
			count = 0
			goal = len(yield_list)
			is_first = True
			for index, varname in yield_list.items():
				count += 1
				is_last = count == goal
				props.setProperty(first_name, is_first)
				props.setProperty(last_name, is_last)
				is_first = False

				s = varname
				if to_upper:
					s = s.upper()
				elif to_lower:
					s = s.lower()

				props.setProperty(index_name, index)
				props.setProperty(name_name, s)
				yield props

	def count(self, *args, **opts):
		type_filter = self._setup_filter(["R", "C", "RP", "CP"], args)
		counter = 0
		for name, param in self._parameters.items():
			(the_name, type, value) = param
			if type in type_filter:
				counter += 1
		return str(counter)

	def parameters(self, *args, **opts):
		type_filter = self._setup_filter(["R", "C", "RP", "CP"], args)

		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		alignment_name = self._setup_name("alignment", "alignment", opts)
		type_name  = self._setup_name("type", "type", opts)
		real_name  = self._setup_name("real", "real", opts)
		imag_name  = self._setup_name("imag", "imag", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name  = self._setup_name("last", "is_last", opts)

		if "base" in opts:
			base = int(opts["base"])
		else:
			base = 1

		lst = []
		names = sorted(self._parameters.keys(), key=lambda s: s.lower())
		for name in names:
			param = self._parameters[name]
			(the_name, type, value) = param
			if type in type_filter:
				lst.append(name)

		for i in range(len(lst)):
			props = Properties()
			if i == 0:
				props.setProperty(first_name, "true")
			else:
				props.setProperty(first_name, "false")
			if i == len(lst) - 1:
				props.setProperty(last_name, "true")
			else:
				props.setProperty(last_name, "false")

			name = lst[i]
			(name, type, value) = self._parameters[name]
			align = " " * (self._name_length - len(name))

			props.setProperty(index_name, str(i+base))
			props.setProperty(name_name, name)
			props.setProperty(alignment_name, align)
			props.setProperty(type_name, type)
			props.setProperty(real_name, value[0])
			props.setProperty(imag_name, value[1])

			yield props

	def functions(self, *args, **opts):
		type_filter = self._setup_filter(["R", "C", "CA"], args)

		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		type_name  = self._setup_name("type", "type", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name  = self._setup_name("last", "is_last", opts)

		if "base" in opts:
			base = int(opts["base"])
		else:
			base = 1

		lst = []
		for name, type in self._functions.items():
			if type in type_filter:
				lst.append(name)

		for i in range(len(lst)):
			props = Properties()
			if i == 0:
				props.setProperty(first_name, "true")
			else:
				props.setProperty(first_name, "false")
			if i == len(lst) - 1:
				props.setProperty(last_name, "true")
			else:
				props.setProperty(last_name, "false")

			name = lst[i]
			type = self._functions[name]

			props.setProperty(index_name, str(i+base))
			props.setProperty(name_name, name)
			props.setProperty(type_name, type)

			yield props

	def comment_chars(self, *args, **opts):
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		ord_name  = self._setup_name("ord", "ord", opts)
		unihex_name  = self._setup_name("unihex", "unihex", opts)
		hex_name  = self._setup_name("hex", "hex", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name  = self._setup_name("last", "is_last", opts)

		if "base" in opts:
			base = int(opts["base"])
		else:
			base = 1

		lst = self._comment_chars
		for i in range(len(lst)):
			props = Properties()
			if i == 0:
				props.setProperty(first_name, "true")
			else:
				props.setProperty(first_name, "false")
			if i == len(lst) - 1:
				props.setProperty(last_name, "true")
			else:
				props.setProperty(last_name, "false")

			name = lst[i]
			ascii = ord(name)
			hex_ascii = hex(ascii)
			while(len(hex_ascii) < 2):
				hex_ascii = '0' + hex_ascii
			uni_hex = hex_ascii
			while(len(uni_hex) < 4):
				uni_hex = '0' + uni_hex

			props.setProperty(index_name, str(i+base))
			props.setProperty(name_name, name)
			props.setProperty(ord_name, str(ascii))
			props.setProperty(unihex_name, uni_hex)
			props.setProperty(hex_name, hex_ascii)

			yield props

	def functions_resolved_fortran(self, *args, **opts):
		"""
		New method for writing the model file when GoSam is
		the OLP : writes directly into fortran
		"""
		index_name = self._setup_name("index", "index", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expression_name  = self._setup_name("expression", "expression", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)
		model_mod = self._mod
	
		nfunctions = len(model_mod.functions)

		golem.util.tools.message("Compiling functions ...")
		process_functions=False
		if self._functions_fortran == {}:
			process_functions=True
		if process_functions:
			specials={}
			for expr in shortcut_functions:
				specials[str(expr)] = expr
			for expr in unprefixed_symbols:
				specials[str(expr)] = expr
			parser = golem.model.expressions.ExpressionParser(**specials)
			functions = {}
			fcounter=[0]
			fsubs={}
			i = 0
			tmp=open('tmp','w')

			for name, value in model_mod.functions.items():
				i += 1
				if i % 100 == 0:
					golem.util.tools.message("  (%5d/%5d)" % (i, nfunctions))
				expr = parser.compile(value)
				prefix='mdl'
				for fn in cmath_functions:
					expr = expr.algsubs(ex.DotExpression(sym_cmath, fn),
							ex.SpecialExpression(str(fn)))
					expr = expr.replaceIntegerPowers(fn)
				expr = expr.algsubs(sym_cmplx(
					ex.IntegerExpression(0), ex.IntegerExpression(1)), i_)
				expr = expr.replaceFloats(prefix + "float", fsubs, fcounter)
				functions[name] = expr
			self._functions_fortran = functions
			self._floats = fsubs
			
		else:
			functions = self._functions_fortran
			


		golem.util.tools.message("Resolving dependencies between functions ...")
		program = golem.model.expressions.resolve_dependencies(functions)
		nlines = len(program)

		props = Properties()
		for i, name in enumerate(program):
			if i % 100 == 0:
				golem.util.tools.message("   (%5d/%5d) lines" % (i, nlines))

			ast = functions[name]
			buf =""
			try:
				buf += ast.write_fortran()

				props.setProperty(name_name, name)
				props.setProperty(expression_name, buf)
				props.setProperty(index_name, i)
				props.setProperty(first_name, i == 0)
				props.setProperty(last_name, i == nlines - 1)
			except:
				golem.util.tools.error("Could not set property in model file %s" % name)
			yield props

	def floats(self, *args, **opts):
		if self._floats == {}:
			list(self.functions_resolved_fortran(args,opts))
		float_name = self._setup_name("float", "$_", opts)
		value_name = self._setup_name("value", "value", opts)
		local_floats = self._floats
		props = Properties()
		for name in local_floats:
			try:
				props.setProperty(float_name, name)
				props.setProperty(value_name, local_floats[name])
			except:
				golem.util.tools.error("Floats not defined %s" % name)
			yield props


	def parameter_alias(self, *args, **opts):
		alias_name = self._setup_name("alias", "alias", opts)
		name_name  = self._setup_name("name", "$_", opts)
		expr_name  = self._setup_name("expr", "expr", opts)
		#only real variables implemented yet
		#type_name  = self._setup_name("type", "type", opts)

		re = str(opts.get("real","re"))
		im = str(opts.get("imag","im"))
		params = {}

		# params["model_param"]  = [ (alias_name , conversion_expression ) , ... ]
		params["mdlaEWM1"]= [("alpha",  "1._ki/{re}"),("alphaEW","1._ki/{re}")]
		params["mdlaS"] = [( "alphaS", "{re}"),("alphas", "{re}") ]
		params["mdlGf"] = [( "GF", "{re}")]

		props = Properties()
		for k in params.keys():
			if k in self._parameters and not "P" in self._parameters[k][1]:
				for (alias, expr_unf) in params[k]:
					expr = expr_unf.format(re=re,im=im)
					props.setProperty(name_name, k)
					props.setProperty(alias_name, alias)
					#props.setProperty(type_name, self._parameters[k][1])
					props.setProperty(expr_name, expr)
					yield props
