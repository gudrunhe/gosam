# vim: ts=3:sw=3

from golem.util.config import Properties
from golem.util.parser import Template, TemplateError
import golem.util.path
import golem.util.config

class LightConeTemplate(Template):
	"""
	Implements a template that can generate information
	about the light cone projections for the given
	helicity.
	"""

	def setup(self, ref, onshell):
		"""
		PARAMETER

		ref -- a dictionary of reference momenta 
		"""

		self._ref = ref
		self._onshell = {}
		bindex = len("es")
		for s, m in onshell.iteritems():
			i = int(s[bindex:])
			if m.endswith("**2"):
				self._onshell[i] = m[:-3]
			else:
				assert m == "0", "m should be '0' but is %r" % m
				self._onshell[i] = m

	def references(self, *args, **opts):
		"""
		Returns a list of reference momenta
		"""
		lst = list(self._ref.keys())
		lst.sort()

		name_name = self._setup_name("name", "name", opts)
		vector_name = self._setup_name("vector", "vector", opts)
		mass_name = self._setup_name("mass", "mass", opts)
		massive_name = self._setup_name("massive", "is_massive", opts)
		index_name = self._setup_name("index", "index", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)

		if "shift" in opts:
			base = int(opts["shift"])
		else:
			base = 0
		
		props = golem.util.config.Properties()
		for i in range(len(lst)):
			name = lst[i]
			mass = self._onshell[name]
			is_massive = mass != "0"
			props.setProperty(index_name, base + i)
			props.setProperty(first_name, i == 0)
			props.setProperty(last_name, i == len(lst) - 1)
			props.setProperty(name_name, name)
			props.setProperty(mass_name, mass)
			props.setProperty(massive_name, is_massive)
			props.setProperty(vector_name, self._ref[name])

			yield props

	def _compute_program(self):
		# Calculate dependencies between auxiliary vectors
		lst = list(self._ref.keys())
		lst.sort()

		# Example: self._ref = {1: 'l2', 2: 'l1', 3: 'l2', 4: 'l2'}
		#          self._onshell = {1: 'm', 2: 'm', 3: 'm', 4: '0'}
		dependencies = {}
		for i in lst:
			vector = self._ref[i]
			mass = self._onshell[i]
			if mass == "0":
				continue
			if vector.startswith("l"):
				idx = int(vector[1:])
				dependencies[i] = set([idx])
			else:
				dependencies[i] = set()
		# Now: dependencies = {
		#  1: set(['l2']),
		#  2: set(['l1']),
		#  3: set(['l2'])}

		for i in dependencies.iterkeys():
			d = dependencies[i]
			new_d = set(d)
			flag = True
			while flag:
				d = frozenset(new_d)
				for j in d:
					new_d.update(dependencies[j])
					
				flag = (new_d != d)
			dependencies[i] = new_d
		# Now: dependencies = {
		#  1: set(['l1', 'l2']),
		#  2: set(['l1', 'l2']),
		#  3: set(['l1', 'l2'])}

		# Program: a list of instructions encoded as:
		#   [i]    == ligt_cone_decomposition(k_i, ref_i)
		#   [i, j] == symmetric splitting of k_i and k_j
		program = []
		available = set()
		while len(dependencies) > 0:
			success = False
			indep = filter(lambda i: dependencies[i] == set(),
					dependencies.keys())
			for i in indep:
				program.append([i])
				success = True

			if success:
				available.update(indep)
			else:
				# try splittings
				for i, depi in dependencies.iteritems():
					li = "l%d" % i
					for j, depj in dependencies.iteritems():
						if j <= i:
							continue
						lj = "l%d" % j
						if self._ref[i] == lj and self._ref[j] == li:
							success = True
							program.append([i, j])
							available.update([i, j])
							break
			if success:
				for i in available:
					if i in dependencies:
						del dependencies[i]
				for i in dependencies.iterkeys():
					dependencies[i].difference_update(available)
			else:
				raise "Cannot create initialization for kinematics"

		self._program = program
		return program

	def instructions(self, *args, **opts):
		"""
		Enumerates a sequence of instructions to initialize
		the l-momenta.

		[% @for instructions opcode=<name>
			index1=<name> mass1=<name>
			index2=<name> mass2=<name>
		%]
			[%opcode%] -- either 1 or 2
			[%index%]  -- the number of the leg.
			[%mass%]  -- the mass of the corresponding external vector
		"""
		opcode_name = self._setup_name("opcode", "opcode", opts)
		index1_name = self._setup_name("index1", "index1", opts)
		index2_name = self._setup_name("index2", "index2", opts)
		mass1_name = self._setup_name("mass1", "mass1", opts)
		mass2_name = self._setup_name("mass2", "mass2", opts)
		first_name = self._setup_name("first", "is_first", opts)
		last_name = self._setup_name("last", "is_last", opts)

		self._compute_program()
		index = 0
		l = len(self._program) - 1
		for inst in self._program:
			props = Properties()
			props.setProperty(first_name, index == 0)
			props.setProperty(last_name, index == l)
			props.setProperty(opcode_name, len(inst))

			props.setProperty(index1_name, inst[0])
			props.setProperty(mass1_name, self._onshell[inst[0]])
			if len(inst) == 1:
				ref = self._ref[inst[0]]
				j = int(ref[1:])
				mass = self._onshell[j]
				props.setProperty(index2_name, j)
				props.setProperty(mass2_name, mass)
			else:
				props.setProperty(index2_name, inst[1])
				props.setProperty(mass2_name, self._onshell[inst[1]])

			index += 1
			yield props
