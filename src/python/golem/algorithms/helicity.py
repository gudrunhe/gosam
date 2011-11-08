# vim: ts=3:sw=3
import golem.properties

symbol_to_heli = {'0': 0, '+': +1, '-': -1,
		'p': +2, 'm': -2, 'P': +3, 'M': -3}
heli_to_symbol = {0: '0', +1: '+', -1: '-',
		+2: 'p', -2: 'm', +3: 'P', -3: 'M'}

massless_states = [
		[0],          # spin 0
		[-1,1],       # spin 1/2
		[-1,1],       # spin 1
		[-2,2],       # spin 3/2
		[-2,2]        # spin 2
	]

massive_states = [
		[0],          # spin 0
		[-1,1],       # spin 1/2
		[-1,0,1],     # spin 1
		[-2,-1,1,2],  # spin 3/2
		[-2,-1,0,1,2] # spin 2
	]

def reference_vectors(conf, in_particles, out_particles):
	"""
	For a given process and a given helicity choose, heuristicly,
	a good set of reference momenta.

	PARAMETER
		conf          -- the configuration.
		in_particles  -- list of incoming particles.
		out_particles -- list of outgoing particles.

	The algorithms tries to avoid the situation where
	ref(k1)=l2 and ref(k2)=l1. This is only used when no
	external light-like momenta are available.
	In this case the function light_cone_split (kinematics.f90)
	needs to be called.

	In all other cases the algorithm imposes an order on the
	momenta such that ref(k_i)=l_j only if l_j can be computed
	without knowing l_i; in general, it produces a cycle free
	dependency graph whenever possible.

	"""
	zeroes = golem.util.tools.getZeroes(conf)
	suggstr = conf.getProperty(golem.properties.reference_vectors)
	suggestions = dict(map(lambda s: map(int, s.split(":")), suggstr))
	num_legs = len(in_particles) + len(out_particles)
	assert num_legs > 1, "Seriously, you need at least two particles!"

	external_massless = []
	reference_required = []
	gauge_vector_required = []
	references = {}
	not_favourable = set()
	ini_indices = set()

	by_index = {}

	def classify(particle, index, is_ini):
		mass = particle.getMass(zeroes)
		twospin = particle.getSpin()
		is_massive = particle.isMassive(zeroes)

		if is_massive:
			reference_required.insert(0, index)
			if abs(twospin) >= 2:
				not_favourable.update([index])

			by_index[index] = "l%d" % (index + 1)
		else:
			if abs(twospin) >= 2:
				gauge_vector_required.append(index)
			external_massless.append("k%d" % (index + 1))

			by_index[index] = "k%d" % (index + 1)
	#### END OF classify

	i = 0
	for ini in in_particles:
		classify(ini, i, True)
		ini_indices.update([i])
		i += 1

	for fin in out_particles:
		classify(fin, i, False)
		i += 1
	assert i == num_legs

	available_massless = external_massless[:]

	# Work through list of suggestions first
	for vec, ref in suggestions.items():
		kref = by_index[ref-1]
		kvec = by_index[vec-1]
		if vec - 1 in reference_required:
			i = reference_required.index(vec - 1)
			del reference_required[i]
		elif vec - 1 in gauge_vector_required:
			i = gauge_vector_required.index(vec - 1)
			del gauge_vector_required[i]
		references[vec-1] = kref
		if kvec not in available_massless:
			available_massless.append(kvec)

	while(len(reference_required) > 0):
		if len(available_massless) == 0:
			# No vectors available, hence we must split a pair
			assert len(reference_required) > 0
			preferred = set(reference_required)
			# Avoid vector bosons since we haven't implemented
			# the polarisation vectors for the case of symmetric splitting.
			preferred.difference_update(not_favourable)

			# Avoid initial state vectors, which have typically
			# large momenta but small masses (numerically not favourable).
			if len(preferred - ini_indices) >= 2:
				preferred.difference_update(ini_indices)
			elif len(preferred) < 2:
				raise golem.util.parser.TemplateError(
					"""Cannot produce correct code for your problem.\n\
				Please, see lorentz.pdf for more details.""")

			if len(preferred) > 0:
				particle = preferred.pop()
				reference_required.remove(particle)
			else:
				particle = reference_required.pop()

			if len(preferred) > 0:
				particle2 = preferred.pop()
				reference_required.remove(particle2)
			else:
				particle2 = reference_required.pop()
			l1 = "l%d" % (particle + 1)
			l2 = "l%d" % (particle2 + 1)
			references[particle] = l2
			references[particle2] = l1
			available_massless.append(l2)
		else:
			particle = reference_required.pop()
			l1 = "l%d" % (particle + 1)
			# Preferably choose k1 or k2, because they are
			# more likely to be IR-safe from experimental cuts
			if len(external_massless) > 0:
				if "k2" in external_massless:
					references[particle] = "k2"
				elif "k1" in external_massless:
					references[particle] = "k1"
				else:
					references[particle] = external_massless[0]
			else:
				references[particle] = available_massless[0]
		available_massless.append(l1)

	# Massive gauge bosons are already covered in the above case
	# hence gauge_vector_required only refers to massless particles.
	while len(gauge_vector_required) > 0:
		particle = gauge_vector_required.pop()
		k1 = "k%d" % (particle + 1)
		if len(gauge_vector_required) > 0:
			particle2 = gauge_vector_required.pop()
			k2 = "k%d" % (particle2 + 1)
			references[particle] = k2
			references[particle2] = k1
		else:
			my_externals = filter(lambda x: x != k1, external_massless)
			if len(my_externals) > 0:
				if "k2" in my_externals:
					references[particle] = "k2"
				elif "k1" in my_externals:
					references[particle] = "k1"
				else:
					references[particle] = my_externals[0]
			else:
				my_available = filter(lambda x: x != k1, available_massless)
				# If it's a proper process we will find another particle:
				assert len(my_available) > 0
				references[particle] = my_available[0]

	return references

def parse_helicity(string, symbols=symbol_to_heli):
	"""
	Parse a string representation of a helicity combination
	into a dictionary of helicities.

	PARAMETER

	string  -- the string representation
	symbols -- a dictionary of symbols

	EXAMPLE
	   >>> print parse_helicity("+-0p")
		{0: 1, 1: -1, 2: 0, 3: 2}
	"""
	result = {}
	i = 0
	for c in string:
		if c in symbols:
			result[i] = symbols[c]
			i += 1
		else:
			raise golem.util.parser.TemplateError(
				"Illegal helicity: %r" % string)
	return result

