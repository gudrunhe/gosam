# vim: ts=3:sw=3

import golem.algorithms.helicity

class Particle:
	"""
	Store basic facts about particles.
	"""
	def __init__(self, field, twospin, mass, color, partner, width, pdg_code, charge):
		self._field = field
		self._twospin = twospin
		self._mass = mass
		self._color = color
		self._charge = charge
		if partner is None:
			self._partner = field
		else:
			self._partner = partner

		self._latex_name = field
		if width.strip(" +-\t\r\n") == '0':
			self._width = "0"
		else:
			self._width = width

		self._pdg_code = pdg_code

	def getPDGCode(self):
		return self._pdg_code

	def __int__(self):
		return self._pdg_code

	def setLaTeXName(self, name):
		"""
		Sets the LaTeX name, i.e. a character string
		which is used to type-set the particles name in LaTeX.
		"""
		self._latex_name = name

	def getLaTeXName(self):
		return self._latex_name

	def getSpin(self):
		"""
		Returns an integer number, two times the spin,
		negative for antiparticles, positive for particles
		"""
		return self._twospin

	def getColor(self):
		"""
		Returns an integer number, labeling the
		the SU(N)-color representation.
		Negative values correspond to conjugate
		representations.
		"""
		return self._color

	def getPartner(self):
		"""
		Returns the field name of its conjugate.
		If the particle is self-conjugate it returns its
		own field name.
		"""
		return self._partner

	def isMassive(self, zeroes={}):
		return self.getMass(zeroes) != "0"

	def getWidth(self, zeroes={}):
		if str(self._width) != "0":
			if self._width in zeroes:
				return "0"
		return str(self._width)

	def getMass(self, zeroes={}):
		if self._mass != 0:
			if self._mass in zeroes:
				return "0"
		return str(self._mass)

	def nullifyMass(self):
		self._mass = 0

	def nullifyWidth(self):
		self._width = 0

	def __str__(self):
		return self._field

	def __repr__(self):
		return "Particle(%r, %r, %r, %r, %r, %r, %r, %r)" % (
			self._field, self._twospin, self._mass,
			self._color, self._partner, self._width, self._pdg_code, self._charge)

	def getHelicityStates(self, zeroes={}):
		sp = abs(self.getSpin())
		if self.isMassive(zeroes):
			states = golem.algorithms.helicity.massive_states
		else:
			states = golem.algorithms.helicity.massless_states
		#if sp > 2:
		#	if sp % 2 == 0:
		#		ssp = "%d" % (sp // 2)
		#	else:
		#		ssp = "%d/2" % sp
		#	raise golem.util.config.GolemConfigError(
		#			"Spin %s particles currently not implemented" % ssp)
		return states[sp]
		

	def referenceRequired(self, zeroes={}):
		return self.getSpin() >= 2 or self.isMassive(zeroes)
	      
	def getCharge(self):
	  """
	  Return electric charge of the particle
	  """
	  return self._charge
	
	def getField(self):
	  return self._field

def simplify_model(particles, parameters, types, functions, masses, widths):
	for p in particles.values():
		m = p.getMass()
		w = p.getWidth()

		if masses is not None:
			if m != "0" \
					and abs(p.getPDGCode()) not in [23, 24] \
					and m not in masses:
				p.nullifyMass()
				parameters[m] = '0.0'
				types[m] = 'RP'
				if m in functions:
					del functions[m]
				m = "0"

		if w == "0":
			continue

		if m == 0 or (widths is not None and w not in widths):
				p.nullifyWidth()
				parameters[w] = '0.0'
				types[w] = 'RP'
				if w in functions:
					del functions[w]
