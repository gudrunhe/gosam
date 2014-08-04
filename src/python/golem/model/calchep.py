# vim: ts=3:sw=3

import os.path

from golem.model.expressions import ExpressionParser, \
		FunctionExpression, SymbolExpression, ProductExpression, \
		SumExpression, SpecialExpression, PowerExpression, \
		UnaryMinusExpression, DotExpression, IntegerExpression
from golem.util.config import GolemConfigError
from golem.util.tools import debug, message, error, warning, \
		LimitedWidthOutputStream

# Maximal number of M-functions added to the vertices
# in the qgraf file.
# If there are too many, qgraf will give up
MAX_VERTEX_PARAMETER = 10

MODEL_PREFIX = "mdl"
IGNORE_WIDTHS = True

Gamma5 = SpecialExpression("Gamma5")
ProjPlus = SpecialExpression("ProjPlus")
ProjMinus = SpecialExpression("ProjMinus")
Sm = SpecialExpression("Sm")
Sm4 = SpecialExpression("Sm4")
SmEps = SpecialExpression("SmEps")
NCContainer = SpecialExpression('NCContainer')
d_ = SpecialExpression("d_")
T  = SpecialExpression("T")
i_ = SpecialExpression("i_")
f  = SpecialExpression("f")
SplitLorentzIndex = SpecialExpression("SplitLorentzIndex")
PREFACTOR = SpecialExpression("PREFACTOR")
dMetric = SpecialExpression("d")
sqrt2 = SpecialExpression("Sqrt2")
sym_sin = SpecialExpression("sin")
sym_cos = SpecialExpression("cos")
sym_tan = SpecialExpression("tan")
sym_sqrt = SpecialExpression("sqrt")
sym_asin = SpecialExpression("asin")
sym_acos = SpecialExpression("acos")
sym_atan = SpecialExpression("atan")
sym_exp = SpecialExpression("exp")
sym_log = SpecialExpression("log")
sym_fabs = SpecialExpression("fabs")
sym_atan2 = SpecialExpression("atan2")
sym_if = SpecialExpression("if")
sym_sort4 = SpecialExpression("sort4")
sym_deltaaxial = SpecialExpression("deltaaxial")

idx = SymbolExpression('__IDX__')
adx = SymbolExpression('__ADJ_IDX__')

CANONICAL_HEADER_NAMES = {
   "full name": "fullname",
	"a": "name",
	"p": "name",
	"a+": "aname",
	"ap": "aname",
	"2*spin": "spin2",
	"latex(a)": "texname",
	"latex(a+)": "atexname",
	"number": "pdg",
	"id": "pdg"
}


class CalcHEPImportError(GolemConfigError):
	def __init__(self, msg):
		GolemConfigError.__init__(self, msg)

	def __str__(self):
		return "Error in LanHEP import: %s" % self.value()

	def __repr__(self):
		return "%s(%r)" % ( self.__class__, self.value())

class TableReader:
	"""
	Reader for CalcHEP/CompHEP model files (tables)

	I could not find a normative reference for the file format.
	It seems to be of the form:

	<Descriptive model name>
	<Table name, e.g. Particles, Lagrangian, Variables, Constraints>
	<Column head> "|" <Column head> "|" .... <Column head> "|"
	<Column data> "|" <Column data> "|" .... <Column data> 
	...
	An optional last line of commentary starting with "="
	The columns are fixed width
	"""

	def __init__(self, f):
		self.load(f)

	def load(self, f):
		model_name = f.readline().strip()
		table_name = f.readline().strip()

		format = f.readline()
		while format.endswith("\r") or format.endswith("\n"):
			format = format[:-1]

		if format.endswith("|"):
			format = format[:-1]
		else:
			raise CalcHEPImportError("Format line must end with a '|'.")

		column_names = format.split("|")
		widths = map(len, column_names)
		column_names = map(lambda s: s.strip(), column_names)
		table = []

		num_columns = len(column_names)

		if num_columns < 1:
			raise CalcHEPImportError(
				"Could not find sufficient number of columns.")

		num_rows = 0
		for line in f:
			if line.startswith("="):
				break

			while line.endswith("\r") or line.endswith("\n"):
				line = line[:-1]
			data = line.split("|")
			row = ["" for i in range(num_columns)]

			i = 0
			for cell in data:
				if i >= num_columns:
					if (i > num_columns) or len(cell.strip()) > 0:
						raise CalcHEPImportError(
							"Too many columns in entry #%d" % num_rows)
					else:
						continue

				if not IGNORE_WIDTHS:
					# don't care about the last cell
					if i < num_columns - 1:
						if len(cell) > widths[i]:
							raise CalcHEPImportError(
								("Column too wide (column #%d, entry #%d)." %
									(i+1,num_rows+1)) +
								("\nColumn was %r but width was %d" %
									(cell, widths[i])))
						elif len(cell) < widths[i]:
							raise CalcHEPImportError(
								("Column too narrow (column #%d, entry #%d)." %
									(i+1,num_rows+1)) +
								("\nColumn was %r but width was %d" %
									(cell, widths[i])))
				row[i] = cell.strip()
				i += 1
			table.append(row)
			num_rows += 1


		self.model_name = model_name
		self.table_name = table_name
		self.column_names = column_names
		self.widths = widths
		self.num_columns = num_columns
		self.num_rows = num_rows
		self.table = table

		self.column_indices = {}

		i = 0
		for name in self.column_names:
			header = self.normalize_name(name)
			self.column_indices[header] = i
			i += 1

		return True

	def normalize_name(self, name):
			words = name.lower().strip(" \t><").split()
			norm_name = " ".join(words)
			if norm_name in CANONICAL_HEADER_NAMES:
				norm_name = CANONICAL_HEADER_NAMES[norm_name]
			return norm_name

	def index(self, *names):
		for name in names:
			header = self.normalize_name(name)
			if header in self.column_indices:
				return self.column_indices[header]
		return -1

class Model:
	"""
	Describes a model from a CompHEP/CalcHEP table base.
	"""

	def __init__(self, path, idx):
		"""
		Creates a new model from a set of CalcHep/CompHep files.

		PARAMETER
			path -- directory where the .mdl files reside
			idx  -- index to be added to the file names
		"""
		self.load(path, idx)

	def load(self, path, idx):
		"""
		Loads the CalcHEP/CompHEP files for processing.

		PARAMETER
			path -- directory where the .mdl files reside
			idx  -- index to be added to the file names
		"""
		stubs = ["func", "lgrng", "prtcls", "vars"]
		tables = {}
		for stub in stubs:
			try:
				fname = os.path.join(path, "%s%d.mdl" % (stub, idx))
				f = open(fname, 'r')
				tables[stub] = TableReader(f)
				f.close()
			except CalcHEPImportError as exc:
				raise CalcHEPImportError("While reading %r: %s"
						% (fname, exc.value()))

		self.tables = tables

	def containsMajoranaFermions(self):
		prtcls = self.tables["prtcls"]
		i_A     = prtcls.index("name")
		i_A_p   = prtcls.index("aname")
		i_spin  = prtcls.index("spin2")

		for row in prtcls.table:
			if abs(int(row[i_spin])) == 1 and row[i_A] == row[i_A_p]:
				return True
		return False

	def store(self, path, stub):
		"""
		Writes the files required by golem to the specified directory.

		PARAMETER

			path -- directory to which the files should be written
			stub -- the prefix of the generated filenames
				<stub>.py, <stub>.hh, <stub>
		"""

		message("   Writing Python file ...")
		f = open(os.path.join(path, stub + ".py"), 'w')
		self.write_python_file(f)
		f.close()

		message("   Writing QGraf file ...")
		f = open(os.path.join(path, stub), 'w')
		self.write_qgraf_file(f, stub)
		f.close()

		message("   Writing Form file ...")
		f = open(os.path.join(path, stub + ".hh"), 'w')
		self.write_form_file(f)
		f.close()

	def _check_header_sane(self, tbl):
		required_headers = [
				"fullname", "name", "aname",
				"spin2", "mass", "width", "color", "aux", "texname", "atexname",
				"pdg"]

		missing = []
		for header in required_headers:
			idx = tbl.index(header)
			if idx < 0:
				missing.append(" or ".join(map(lambda s: "'%s'" % s, header)))

		if len(missing) > 0:
			raise CalcHEPImportError(
					"In particles: columns missing in table: %s" %
					", ".join(missing))

	def var_list(self, tbl, prtcls, prefix=""):
		i_name = tbl.index("Name")
		i_val  = tbl.index("Value")
		i_cmt  = tbl.index("Comment")

		if i_name < 0:
			raise CalcHEPImportError("In vars: column 'Name' missing.")
		if i_val < 0:
			raise CalcHEPImportError("In vars: column 'Value' missing.")

		seen = set()

		for row in tbl.table:
			name = row[i_name]
			if name == 'deltaaxial':
				continue

			if name.startswith("*"):
				name = name[1:]
			elif name.startswith("%"):
				continue

			seen.add(name)
			ltx_name = "\\text{%s}" % name
			name = prefix + name

			if i_cmt >= 0:
				yield [name, row[i_val], row[i_cmt], ltx_name]
			else:
				yield [name, row[i_val], "", ltx_name]

		self._check_header_sane(prtcls)

		i_name  = prtcls.index("fullname")
		i_mass  = prtcls.index("mass")
		i_width = prtcls.index("width")
		for row in prtcls.table:
			mass = row[i_mass]
			width = row[i_width]

			if mass.startswith("!"):
				name = mass[1:]
				if name not in seen:
					ltx_name = "\\text{%s}" % name
					name = prefix + name
					yield [name, "0.0", "Mass of %s" % row[i_name], ltx_name]
			if width.startswith("!"):
				name = width[1:]
				if name not in seen:
					ltx_name = "\\text{%s}" % name
					name = prefix + name
					yield [name, "0.0", "Width of %s" % row[i_name], ltx_name]

	def func_list(self, tbl, prefix=""):
		i_name = tbl.index("Name")
		i_expr = tbl.index("Expression")
		i_cmt  = tbl.index("Comment")
		parser = ExpressionParser(i=i_, Sqrt2=sqrt2,
				deltaaxial = sym_deltaaxial,
				sin = sym_sin,
				cos = sym_cos,
				tan = sym_tan,
				sqrt = sym_sqrt,
				asin = sym_asin,
				acos = sym_acos,
				atan = sym_atan,
				exp = sym_exp,
				log = sym_log,
				fabs = sym_fabs,
				atan2 = sym_atan2,
				sort4 = sym_sort4,
				**{'if': sym_if}
			)

		ExpressionParser.simple = ExpressionParser.simple_old

		if i_name < 0:
			raise CalcHEPImportError("In funcs: column 'Name' missing.")
		if i_expr < 0:
			raise CalcHEPImportError("In funcs: column 'Expression' missing.")
		for row in tbl.table:
			name = row[i_name]
			if name.startswith("*"):
				name = name[1:]
			elif name.startswith("%"):
				continue

			name = prefix + name

			expr = parser.compile(row[i_expr])
			expr = expr.prefixSymbolsWith(prefix)

			if i_cmt >= 0:
				yield [name, expr, row[i_cmt]]
			else:
				yield [name, expr]

	def expand_field_list(self, tbl, prefix=""):
		"""
		Expands the list of fields by automatically generating
		ghosts and Goldstone bosons.

		The generated list has the following order:
		    0: Full name
			 1: field name A
			 2: field name A+
			 3: 2*spin
			 4: mass
			 5: width
			 6: color
			 7: aux field
			 8: LaTeX(A)
			 9: LaTeX(A+)
			10: PDG code
		"""

		def pack(val):
			if val == '0':
				return val
			else:
				if val.startswith("!"):
					return prefix + val[1:]
				else:
					return prefix + val

		# Find the table columns:
		i_name  = tbl.index("fullname")
		i_A     = tbl.index("name")
		i_A_p   = tbl.index("aname")
		i_spin  = tbl.index("spin2")
		i_mass  = tbl.index("mass")
		i_width = tbl.index("width")
		i_color = tbl.index("color")
		i_aux   = tbl.index("aux")
		i_latex = tbl.index("texname")
		i_lat_p = tbl.index("atexname")
		i_pdg   = tbl.index("pdg")

		GHOSTS     = 9000000
		OTHERS     = 9100000
		GOLDSTONES = {
				 23: 250,
				 24: 251
			}

		if i_pdg < 0:
			raise CalcHEPImportError(
				"Old model files without PDG codes are not supported anymore.")
		self._check_header_sane(tbl)

		for row in tbl.table:
			aux = row[i_aux].strip().upper()
			pdg = row[i_pdg]

			if pdg == "":
				OTHERS += 1
				pdg = OTHERS
					
			new_row = [
				row[i_name],
				row[i_A],
				row[i_A_p],
				row[i_spin],
				pack(row[i_mass]),
				pack(row[i_width]),
				row[i_color],
				row[i_aux],
				row[i_latex],
				row[i_lat_p],
				pdg
			]
			yield new_row

			if aux == 'G':
				assert int(row[i_spin]) == 2, \
						"Cannot have aux=G for fields other than vectors"
				mass = row[i_mass].strip()
				color = int(row[i_color])
				OTHERS += 1
				if abs(color) != 1:
					new_row = [
							row[i_A] + " tensor ghost",
							row[i_A] + ".t",
							row[i_A_p] + ".t",
							"4",    # it's a tensor
							pack(row[i_mass]), # mass does not matter
							pack(row[i_width]), # width does not matter either
							row[i_color], # the color should remain the same
							"t",    # indicates that we have a tensor ghost here
							"{%s}_t" % row[i_latex],
							"{%s}_t" % row[i_lat_p],
							OTHERS	
					]
					yield new_row

				if mass != "0":
					if row[i_pdg] in GOLDSTONES:
						pdg = GOLDSTONES[i_pdg]
					else:
						OTHERS += 1
						pdg = OTHERS
					new_row = [
							row[i_A] + " goldstone boson",
							row[i_A] + ".f",
							row[i_A_p] + ".f",
							"0",    # it's a scalar boson
							pack(row[i_mass]), # same mass
							pack(row[i_width]), # same width
							row[i_color], # same color
							"f",    # indicates that we have a goldstone boson
							"\\chi_{%s}" % row[i_latex],
							"\\chi_{%s}" % row[i_lat_p],
							pdg
					]
					yield new_row

				GHOSTS += 1
				new_row = [
						row[i_A] + " faddeev popov ghost",
						row[i_A] + ".c",
						row[i_A] + ".C",
						"0",    # it's a scalar boson
						pack(row[i_mass]), # same mass
						pack(row[i_width]), # same width
						row[i_color], # same color
						"c",    # indicates that we have a ghost
						"c_{%s}" % row[i_latex],
						"\\bar{c}_{%s}" % row[i_latex],
						GHOSTS
				]
				yield new_row

				if row[i_A] != row[i_A_p]:
					GHOSTS += 1
					new_row = [
							row[i_A_p] + " faddeev popov ghost",
							row[i_A_p] + ".c",
							row[i_A_p] + ".C",
							"0",    # it's a scalar boson
							pack(row[i_mass]), # same mass
							pack(row[i_width]), # same width
							row[i_color], # same color
							"c",    # indicates that we have a ghost
							"c_{%s}" % row[i_lat_p],
							"\\bar{c}_{%s}" % row[i_lat_p],
							GHOSTS
					]

					yield new_row

	def write_qgraf_file(self, f, fmrules):
		WIDTH = 70
		INDENT = "      "
		prtcls = self.tables["prtcls"]
		lgrng  = self.tables["lgrng"]

		prefix = MODEL_PREFIX

		f.write("""\
% vim: syntax=none:sw=3:ts=3
%
% This model file has been created automatically
% from a source in CompHEP/CalcHEP format.

""")
		f.write("[ model = '%s']\n" % prtcls.model_name)
		f.write("[ fmrules = '%s']\n" % fmrules)

		f.write("\n%%%%%%%%%% PROPAGATORS %%%%%%%%%%%%%%%%%%%\n\n")

		#   0: Full name
		#   1: field name A
		#   2: field name A+
		#   3: 2*spin
		#   4: mass
		#   5: width
		#   6: color
		#   7: aux field
		#   8: LaTeX(A)
		#   9: LaTeX(A+)
		#  10: PDG code

		names = {}

		for row in self.expand_field_list(prtcls, prefix):

			row[3] = int(row[3])
			row[6] = int(row[6])
			mass = row[4].strip()

			options = []

			if row[3] % 2 == 1 or row[7] == 'c':
				commutation = "-"
			else:
				commutation = "+"
				if mass == "0":
					options.append("notadpole")

			#name = qgraf_escape(row[1])
			#anti_name = qgraf_escape(row[2])
			name = "part%d" % int(row[10])
			if row[1] == row[2]:
				anti_name = name
			else:
				anti_name = "anti%d" % int(row[10])

			names[row[1]] = name
			names[row[2]] = anti_name

			if row[1] != row[2]:
				conj = "CONJ=('+','-')"
			else:
				conj = "CONJ=('+')"

			aux = 0
			saux = row[7].lower()

			if saux == "t":
				aux = 1

			f.write("%% %s (PDG %s)\n" % (row[0], row[10]))
			line = "[%5s, %5s, %s;" % (name, anti_name,
					",".join([commutation] + options))
			comma = False
			for param in [
					"TWOSPIN=%d" %  row[3],
					"COLOR=%d" %  row[6],
					"MASS=%5r" % mass,
					"WIDTH=%5r" % row[5],
					"AUX='%+d'" % aux,
					conj]:
				if comma:
					line += ","
				else:
					comma = True

				if len(line) + 1 < WIDTH:
					line += " "
				else:
					f.write(line + "\n")
					line = INDENT

				if len(line) + len(param) < WIDTH:
					line += param
				else:
					f.write(line + "\n")
					line = INDENT + param

			f.write(line + "]\n")

		f.write("%%%%%%%%%% VERTICES %%%%%%%%%%%%%%%%%%%%%%\n")

		parser = ExpressionParser(i=i_, Sqrt2=sqrt2,
				deltaaxial = sym_deltaaxial,
				sin = sym_sin,
				cos = sym_cos,
				tan = sym_tan,
				sqrt = sym_sqrt,
				asin = sym_asin,
				acos = sym_acos,
				atan = sym_atan,
				exp = sym_exp,
				log = sym_log,
				fabs = sym_fabs,
				atan2 = sym_atan2,
				sort4 = sym_sort4,
				**{'if': sym_if}
				)

		# collect the names of the couplings
		coupl_freq = {}
		for row in lgrng.table:
			prefactor = parser.compile(row[4])
			powers = prefactor.countSymbolPowers()

			for name, expo in powers.iteritems():
				if expo != 0 or name in ['GG', 'EE']:
					if name in coupl_freq:
						coupl_freq[name] += 1
					else:
						coupl_freq[name] = 1

		coupl_list = list(coupl_freq.keys())
		coupl_list.sort(key=lambda X: coupl_freq[X], reverse=True)
		coupl_cut = min(len(coupl_list), MAX_VERTEX_PARAMETER)

		for row in lgrng.table:
			prefactor = parser.compile(row[4])
			lorentz = parser.compile(row[5])

			if row[3].strip() == "":
				field = [names[fld] for fld in row[0:3]]
				# map(qgraf_escape, row[0:3])
			else:
				field = [names[fld] for fld in row[0:4]]
				# map(qgraf_escape, row[0:4])

			if len(field) == 4:
				f.write("%%  %s  %s  %s  %s  Vertex\n" %
						(row[0], row[1], row[2], row[3]))
				line = "[%s, %s, %s, %s" % \
						(field[0], field[1], field[2], field[3])
			else:
				f.write("%%  %s  %s  %s  Vertex\n" %
						(row[0], row[1], row[2]))
				line = "[%s, %s, %s" % \
						(field[0], field[1], field[2])

			comma = False

			pwrs = {}
			for name in coupl_list[:coupl_cut]:
				pwrs[name] = prefactor.powerCounting({name: 1})

			pwrs['RK'] = get_rank(lorentz)

			if 'EE' in pwrs:
				pwrs['QED'] = pwrs['EE']

			if 'GG' in pwrs:
				pwrs['QCD'] = pwrs['GG']

			for name, expo in pwrs.iteritems():
				if comma:
					line += ","
					if len(line) > WIDTH:
						line += "\n"
						f.write(line)
						line = INDENT
					else:
						line += " "
				else:
					line += "; "
					comma = True
				chunk = "%s='%+d'" % (name, expo)
				if len(line) + len(chunk) < WIDTH:
					line += chunk
				else:
					f.write(line + "\n")
					line = INDENT + chunk
			f.write(line + "]\n")

		f.write("%%%%%%%%%%%%%%%% END % OF % FILE %%%%%%%%%\n")

	def write_python_file(self, f):
		prtcls = self.tables["prtcls"]
		vars   = self.tables["vars"]
		funcs  = self.tables["func"]
		extra_floats = {}

		prefix = MODEL_PREFIX

		f.write("""\
# vim: ts=3:sw=3
from golem.model.particle import Particle
from math import sqrt

""")
		f.write("model_name = %r\n\n" % prtcls.model_name)

		f.write("particles = {\n")
		comma = False
		# The fields are
		# 0            1   2   3       4     5      6     7
		# Full  name  |A  |A+ |2*spin| mass |width |color|aux|>
		#    8          9
		#    LaTex(A)<|>LaTeX(A+)   <|
		max_len = 0
		max_mlen = 0
		max_rlen = 0
		#   0: Full name
		#   1: field name A
		#   2: field name A+
		#   3: 2*spin
		#   4: mass
		#   5: width
		#   6: color
		#   7: aux field
		#   8: LaTeX(A)
		#   9: LaTeX(A+)
		#  10: PDG code
		names = {}
		for row in self.expand_field_list(prtcls, prefix):
			name = "part%d" % int(row[10])
			if row[1] == row[2]:
				anti_name = name
			else:
				anti_name = "anti%d" % int(row[10])

			names[row[1]] = name
			names[row[2]] = anti_name

			max_len = max(max_len, len(name), len(anti_name))
			max_mlen = max(max_mlen, len(row[4]))
			max_rlen = max(max_rlen, len(row[1]), len(row[2]))
		
		max_len = str(max_len+2)
		max_mlen = str(max_mlen+2)
		max_rlen = str(max_rlen+2)
		line_fmt = "\t\t%" + max_len + "r:" + \
			" Particle(%" + max_len + "r, %2d, %" + max_mlen + "r, %2d," + \
			" %" + max_len + "r, %r, %r, %r)"

		for row in self.expand_field_list(prtcls, prefix):
			row[3]  = int(row[3])
			row[6]  = int(row[6])
			row[10] = int(row[10])

			if comma:
				f.write(",\n")
			else:
				comma = True

			name = names[row[1]] # qgraf_escape(row[1])
			anti_name = names[row[2]] # qgraf_escape(row[2])
			charge = 0 #FIXME not yet implemented

			if(row[1] != row[2]):
				f.write(line_fmt %
					(anti_name, anti_name, -row[3], row[4], -row[6], name,
						row[5], -row[10], -charge))
				f.write(",\n")
			f.write(line_fmt %
				(name, name, row[3], row[4], row[6], anti_name, row[5], row[10], charge))
		f.write("\n}\n\n")

		f.write("""\
mnemonics = {
\t# Here, you can add entries like:
\t# 'mnemonic-name': particles['field-name']
""")

		fmt = "\t%" + max_rlen + "r: particles[%" + max_len + "r]"
		comma = False
		for row in self.expand_field_list(prtcls, prefix):
			name = names[row[1]] # qgraf_escape(row[1])
			anti_name = names[row[2]] # qgraf_escape(row[2])

			if name != row[1]:
				if comma:
					f.write(",\n")
				else:
					comma = True
				f.write(fmt % (row[1], name))
			
			if (anti_name != row[2]) and (row[1] != row[2]):
				if comma:
					f.write(",\n")
				else:
					comma = True
				f.write(fmt % (row[2], anti_name))

		if comma:
			f.write("\n}\n\n")
		else:
			f.write("}\n\n")

		counter = [0]
		self.fsubs = {}
		fprefix = prefix + "float"
		f.write("functions = {\n")
		f.write("\t'Nfrat': 'if(Nfgen,Nf/Nfgen,1)'")
		for row in self.func_list(funcs, prefix):
			name = row[0]
			expr = row[1].replaceFloats(fprefix, self.fsubs, counter)
			f.write(",\n")
			if len(row) > 2:
				f.write("\t\t# %s\n" % row[2])
			f.write("\t\t%r: " % name)
			f.write("'")
			expr.write(f)
			f.write("'")
		f.write("\n}\n\n")

		f.write("parameters = {\n")
		f.write("\t\t# Number of colours in SU(NC) group (QCD)\n")
		f.write("\t\t'NC': '3.0',\n")
		f.write("\t\t# Number of light flavours\n")
		f.write("\t\t'Nf': '5.0',")
		f.write("\t\t'Nfgen': '-1.0'")

		for name, value in self.fsubs.items():
			f.write(",\n")
			f.write("\t\t%r: " % name)
			f.write("'")
			value.write(f)
			f.write("'")
			
		for row in self.var_list(vars, prtcls, prefix):
			if len(row)  > 2:
				f.write(",\n\t\t# %s\n" % row[2])
			f.write("\t\t%r: %r" % (row[0], row[1]))
		f.write("\n}\n\n")

		f.write("latex_parameters = {\n")
		f.write("\t\t'NC': 'N_C',\n")
		f.write("\t\t'Nf': 'N_f',\n")
		f.write("\t\t'Nfgen': 'N_f^{gen}'")

		for name, value in self.fsubs.items():
			f.write(",\n")
			f.write("\t\t%r: %r" % (name, "\\text{" + name + "}"))
			
		for row in self.var_list(vars, prtcls, prefix):
			f.write(",\n\t\t%r: %r" % (row[0], row[3]))
		f.write("\n}\n\n")

		f.write("types = {\n")
		f.write("\t\t'NC': 'R', 'Nf': 'R', 'Nfgen': 'R', 'Nfrat': 'R'")
		for name in self.fsubs.iterkeys():
			f.write(",\n")
			f.write("\t\t%r: 'RP'" % name)
		for row in self.var_list(vars, prtcls, prefix):
			f.write(",\n\t\t%r: 'R'" % row[0])
		for row in self.func_list(funcs, prefix):
			f.write(",\n\t\t%r: 'R'" % row[0])
		f.write("\n}\n\n")

		f.write("latex_names = {\n")
		comma = False
		for row in self.expand_field_list(prtcls, prefix):

			if comma:
				f.write(",\n")
			else:
				comma = True
			if(row[1] != row[2]):
				f.write("\t\t%r: %r,\n" % (names[row[1]], row[8]))
			f.write("\t\t%r: %r" % (names[row[2]], row[9]))
		f.write("\n}\n\n")

		f.write("line_styles = {\n")
		comma = False
		for row in self.expand_field_list(prtcls, prefix):

			if comma:
				f.write(",\n")
			else:
				comma = True

			# choose line style
			tsp = abs(int(row[3]))
			color = int(row[6])
			aux = row[7]

			style = 'scalar'
			if aux == 'f':
				# goldstone boson
				style = 'scalar'
			elif aux == 'c':
				# faddeev popov ghost
				style = 'ghost'
			elif aux == 't':
				# tensor ghost
				style = 'scalar'
			elif tsp == 0:
				style = 'scalar'
			elif tsp % 2 == 1:
				style = 'fermion'
			else:
				if color > 1:
					style = 'gluon'
				else:
					style = 'photon'

			if(row[1] != row[2]):
				f.write("\t\t%r: %r,\n" % (names[row[1]], style))
			f.write("\t\t%r: %r" % (names[row[2]], style))
		f.write("\n}\n\n")

		f.write("slha_locations = {}\n\n")

	def write_form_file(self, f):
		WIDTH = 70
		prtcls = self.tables["prtcls"]
		vars   = self.tables["vars"]
		funcs  = self.tables["func"]
		lgrng  = self.tables["lgrng"]

		prefix = MODEL_PREFIX

		f.write("""\
* vim: ts=3:sw=3:syntax=form
* This file has been created automatically from a
* CompHEP/CalcHEP source.

*---#[ Symbol Definitions :
""")
		f.write("*---#[ Fields :\n")
		particles = {}
		names = {}
		for row in self.expand_field_list(prtcls, prefix):
			row[3] = int(row[3])
			row[6] = int(row[6])
			name = "part%d" % int(row[10])
			if row[1] == row[2]:
				anti_name = name
			else:
				anti_name = "anti%d" % int(row[10])

			names[row[1]] = name
			names[row[2]] = anti_name

			if(row[1] != row[2]):
				particles[anti_name] = \
					[row[0], anti_name, name, -row[3], row[4], \
					 row[5], -row[6], row[7]]
			particles[name] = \
				[row[0], name, anti_name, row[3], row[4], \
				 row[5], row[6], row[7]]

			name = "[field.%s]" % name
			anti_name = "[field.%s]" % anti_name

			if name == anti_name:
				f.write("Symbol %s;\n" % name)
			else:
				f.write("Symbols %s, %s;\n" % (name, anti_name))
		f.write("*---#] Fields :\n")

		f.write("*---#[ Parameters :\n")
		for row in self.var_list(vars, prtcls, prefix):
			if len(row) > 2:
				f.write("* %s\n" % row[2])
			f.write("Symbol %s;\n" % row[0])

		for row in self.func_list(funcs, prefix):
			if len(row) > 2:
				f.write("* %s\n" % row[2])
			f.write("Symbol %s;\n" % row[0])

		for row in self.fsubs:
			f.write("Symbol %s;\n" % row)

		f.write("*---#] Parameters :\n")
		f.write("*---#] Symbol Definitions :\n")

		if self.containsMajoranaFermions():
			f.write("* Model contains Majorana Fermions:\n")
			debug("You are working with a model " +
					"that contains Majorana fermions.")
			f.write("#Define DISCARDQGRAFSIGN \"1\"\n")
		f.write("#Define USEVERTEXPROC \"1\"\n")

		f.write("*---#[ Procedure ReplaceVertices :\n")
		f.write("#Procedure ReplaceVertices\n")

		parser = ExpressionParser(G5 = Gamma5, G  = Sm, Sqrt2 = sqrt2, i = i_,
				deltaaxial = sym_deltaaxial,
				sin = sym_sin,
				cos = sym_cos,
				tan = sym_tan,
				sqrt = sym_sqrt,
				asin = sym_asin,
				acos = sym_acos,
				atan = sym_atan,
				exp = sym_exp,
				log = sym_log,
				fabs = sym_fabs,
				atan2 = sym_atan2,
				sort4 = sym_sort4,
				**{'if': sym_if}
				)

		for row in lgrng.table:
			prefactor = parser.compile(row[4])
			lorentz = parser.compile(row[5])

			if row[3].strip() == "":
				field = [names[fld] for fld in row[0:3]]
			else:
				field = [names[fld] for fld in row[0:4]]

			if len(field) == 4:
				vtxname = "%s  %s  %s  %s  Vertex" % \
						(row[0], row[1], row[2], row[3])
			else:
				vtxname = "%s  %s  %s  Vertex" % \
						(row[0], row[1], row[2])
			#message(vtxname)

			fold = "*---#%%s  %s :\n" % vtxname

			f.write(fold % "[")
			f.write("Identify Once vertex(iv?,\n")
			i = 1
			subs = {}
			idx_splits = []
			sums = []
			reps = []

			Lidx = []
			Cidx = []
				
			idx_taken = False
			adj_idx_taken = False

			spins = []

			for fld in field:
				if i > 1:
					f.write(",\n")
				prt = particles[fld]

				Lidx.append("idx%dL%d" % (i, abs(int(prt[3]))))
				Cidx.append("idx%dC%d" % (i, abs(int(prt[6]))))
				f.write("      [field.%s], idx%d?, %d, k%d?, %s?, %d, %s?" %
						(fld, i, int(prt[3]), i, Lidx[-1], int(prt[6]), Cidx[-1]))

				subs["p%d" % i] = SpecialExpression("k%d" % i)
				reps.append(int(prt[6]))

				spin2      = int(prt[3])
				spins.append(abs(spin2))
				isselfconj = prt[1] == prt[2]
				isfermion  = spin2 % 2 == 1
				ismaiorana = isfermion and isselfconj

				if abs(spin2) == 1:
					if (spin2 < 0 and not adj_idx_taken) or idx_taken:
						subs[str(adx)] = SpecialExpression(Lidx[-1])
						adj_idx_taken = True
					else:
						subs[str(idx)] = SpecialExpression(Lidx[-1])
						idx_taken = True
				elif abs(spin2) == 2:
						subs["m%d" % i] = SpecialExpression(Lidx[-1])
				elif abs(spin2) == 3:
					if (spin2 < 0 and not adj_idx_taken) or idx_taken:
						subs[str(adx)] = SpecialExpression("%sL1" % Lidx[-1])
						adj_idx_taken = True
					else:
						subs[str(idx)] = SpecialExpression("%sL1" % Lidx[-1])
						idx_taken = True
					subs["m%d" % i] = SpecialExpression("%sL2" % Lidx[-1])
					idx_splits.append( (1, SplitLorentzIndex(
								SpecialExpression(Lidx[-1]), 
								SpecialExpression("%sL2" % Lidx[-1]),
								SpecialExpression("%sL1" % Lidx[-1]))) )
					sums.extend(["%sL2" % Lidx[-1], "%sL1" % Lidx[-1]])
				elif abs(spin2) == 4:
					subs["m%d" % i] = SpecialExpression("%sa" % Lidx[-1])
					subs["M%d" % i] = SpecialExpression("%sb" % Lidx[-1])
					idx_splits.append( (1, SplitLorentzIndex(
								SpecialExpression(Lidx[-1]),
								SpecialExpression("%sa" % Lidx[-1]),
								SpecialExpression("%sb" % Lidx[-1]))) )
					sums.extend(["%sa" % Lidx[-1], "%sb" % Lidx[-1]])
				elif spin2 == 0:
					pass
				else:
					raise CalcHEPImportError("Spin %d/2 not supported" % spin2)
				i += 1
			f.write(") =")

			if adj_idx_taken != idx_taken:
				raise CalcHEPImportError("Illegal vertex: %s" % vtxname)

			spins.sort()
			lorentz = translate_lorentz(lorentz, idx_taken, spins == [1,1,2])

			expression = PREFACTOR(i_ * prefactor) * lorentz

			try:
				c = self.color_generator(reps, Cidx)
			except CalcHEPImportError as exc:
				raise CalcHEPImportError(
					"While importing vertex %r: %s" % (field, exc))
			if c != 1:
				expression = expression * c

			if len(idx_splits) > 0:
				expression = expression * ProductExpression(idx_splits)


			expression = expression.subs(subs).prefixSymbolsWith(MODEL_PREFIX)
			lwf = LimitedWidthOutputStream(f, 70, 3)
			lwf.nl()
			expression.write(lwf)
			lwf.write(";")
			f.write("\n")

			if len(sums) > 0:
				f.write("Sum %s;\n" % ", ".join(sums))
			f.write(fold % "]")

		f.write("""\
	Repeat;
		Id once T(idx1?, idx2?) = T(idx1, idx3, idx4) * T(idx2, idx4, idx3) / TR;
		Sum idx3, idx4;
	EndRepeat;
""")
		f.write("#EndProcedure\n")
		f.write("*---#] Procedure ReplaceVertices :\n")

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

	def color_generator(self, reps, indices):
		"""
		Creates an expression for the color generator
		associated with a three particle vertex.

		reps -- a list of representations, i.e.
		        numbers of the set [1,-1,3,-3,8,-8]
		indices -- the color indices associated with the
		        fields.
		"""
		assert len(reps) == len(indices)

		for i in range(len(reps)):
			if abs(reps[i]) == 1:
				new_reps = reps[:]
				new_indices = indices[:]
				del new_reps[i]
				del new_indices[i]
				return self.color_generator(new_reps, new_indices)

		if len(reps) == 0:
			return 1
		elif len(reps) == 2:
			if abs(reps[0]) != 8:
				return d_(SpecialExpression(indices[0]),
						SpecialExpression(indices[1]))
			else:
				return T(SpecialExpression(indices[0]),
						SpecialExpression(indices[1]))

		elif len(reps) == 3:
			r = map(abs, reps)
			r.sort()

			if r == [3, 3, 8]:
				if  8 not in reps:
					ig = indices[reps.index(-8)]
				else:
					ig = indices[reps.index(8)]

				if (-3 not in reps) or (3 not in reps):
					raise CalcHEPImportError(
						"Cannot determine color flow in %r vector" % reps)

				iqbar = indices[reps.index(-3)]
				iq = indices[reps.index(3)]
					
				return T(SpecialExpression(ig),
						SpecialExpression(iqbar),
						SpecialExpression(iq))


			elif r == [8, 8, 8]:
				return -i_ * f(SpecialExpression(indices[0]),
						SpecialExpression(indices[1]),
						SpecialExpression(indices[2]))
			else:
				raise CalcHEPImportError(
						"Currently color generators for %r not supported" % reps)
		else:
			raise CalcHEPImportError(
					("Import of vertices with %d coloured" % len(reps)) +
					(" particles not supported. %r" % reps))

	
def translate_lorentz(expr, has_clifford, is_vff=False):
	if has_clifford:
		one = IntegerExpression(1)
		two = IntegerExpression(2)

		result = expr.algsubs(one + Gamma5, two * ProjPlus)
		result = result.algsubs(one - Gamma5, two * ProjMinus)
		result = grep_clifford(result, is_vff)
	else:
		result = expr

	result = result.replaceDotProducts(["m", "M"], dMetric)

	return result

def grep_clifford(expr, is_vff):
	if isinstance(expr, SumExpression):
		return grep_clifford_in_sum(expr, is_vff)
	elif isinstance(expr, ProductExpression):
		return grep_clifford_in_product(expr, is_vff)
	elif isinstance(expr, UnaryMinusExpression):
		return UnaryMinusExpression(grep_clifford(expr.getTerm(), is_vff))
	elif is_clifford(expr):
		return NCContainer(expr, adx, idx)
	else:
		return expr * d_(adx, idx)

def is_clifford(expr):
	if isinstance(expr, FunctionExpression):
		return expr._head == Sm or expr._head == Sm4 or expr._head == SmEps
	else:
		return expr == Gamma5 or expr == ProjPlus or expr == ProjMinus
		
def grep_clifford_in_sum(expr, is_vff):
	l = len(expr)
	new_terms = []
	for i in range(l):
		new_terms.append(grep_clifford(expr[i], is_vff))
	return SumExpression(new_terms)

def grep_clifford_in_product(expr, is_vff):
	l = len(expr)
	cliff_factors = []
	new_factors = []
	stack = []
	for i in range(l):
		stack.append( expr[i] )
	stack.reverse()

	while len(stack) > 0:
		sig, factor = stack.pop()
		if sig == -1:
			new_factors.append( (sig, factor) )
		elif isinstance(factor, ProductExpression):
			prod = []
			for i in range(len(factor)):
				prod.append( factor[i] )
			prod.reverse()
			stack.extend(prod)
		elif is_clifford(factor):
			cliff_factors.append( (sig, factor) )
		else:
			new_factors.append( (sig, factor) )

	if len(cliff_factors) > 0:
		new_factors.append( (1, NCContainer(ProductExpression(cliff_factors),
			adx, idx)) )
		return ProductExpression(new_factors)
	else:
		return d_(adx, idx) * expr


def qgraf_escape(s):
	"""
	Escape all characters which are not Qgraf-conform.

	Qgraf allows only [A-Za-z0-9_] in names and no digit
	as the first letter.
	
	Here, we make the following replacements:

	'_' -> '__'
	'+' -> '_0P_'
	'-' -> '_0M_'
	'.' + [^_A-Za-z] -> '_' + esc([^_0-7])
	[^_.A-Za-z0-9] -> '_' + oct([^_.A-Za-z0-9]) + '_'
	"""

	res = ""
	l = len(s)
	fmt = '_%03o_'
	for i in range(l):
		ch = s[i:i+1]
		if ch == '_':
			res += '__'
		elif ch == '+':
			res += "_0P_"
		elif ch == '-':
			res += "_0M_"
		elif ch == '.':
			if (i < l - 1) and not s[i+1:i+2].isalpha():
				res += fmt % ord(ch)
			else:
				res += '_'
		elif ch.isalnum():
			res += ch
		else:
			res += fmt % ord(ch)

	if not res[0:1].isalpha():
		res = "X_0_X_" + res
	return res

def get_rank(expr):
	if isinstance(expr, SumExpression):
		n = len(expr)
		lst = [get_rank(expr[i]) for i in range(n)]
		if len(lst) == 0:
			return 0
		else:
			return max(lst)

	elif isinstance(expr, ProductExpression):
		n = len(expr)
		result = 0

		for i in range(n):
			sign, factor = expr[i]
			result += get_rank(factor)
		return result

	elif isinstance(expr, UnaryMinusExpression):
		return get_rank(expr.getTerm())

	elif isinstance(expr, FunctionExpression):
		head = str(expr.getHead())
		args = expr.getArguments()
		if head == "G":
			if str(args[0]).startswith("p"):
				return 1
		return 0
	elif isinstance(expr, DotExpression):
		first = str(expr.getFirst())
		second = str(expr.getSecond())
		result = 0
		if first.startswith("p"):
			result += 1
		if second.startswith("p"):
			result += 1
		return result
	elif isinstance(expr, PowerExpression):
		expo = int(expr.getExponent())
		return expo * get_rank(expr.getBase())
	else:
		return 0
