# vim: syntax=python:ts=3:sw=3

import math
import random

def A(i, F, R=None):
	if R is None:
		if F[i] == 0 or F[i] == i:
			return i
		else:
			return A(F[i], F)
	else:
		if F[i] == 0 or F[i] == i:
			return (i, z3chain())
		else:
			ip, rp = A(F[i], F, R)
			return (ip, rp + R[i])

class diagram:

	def __init__(self, in_legs, out_legs, vertices, propagators):
		self.ini = in_legs
		self.fin = out_legs
		self.vertices = vertices
		self.propagators = propagators

		for leg in self.ini.values():
			leg.setInitial()

	def layout(self, *args, **opts):
		height = opts['height']
		width  = opts['width']

		L = self.find_loops()
		assert len(L) <= 2
		props = set(self.propagators.keys())
		chords = set()
		bridges = set(props)

		loop_vertices = []
	
		if len(L) == 1:
			loop = L.copy().pop()
			chords.update(loop.keys())

		#print len (L),len(chords)
		#print loop
		#print L

		if len(chords) == 0:
			loop_vertices = [1]
		elif len(chords) == 1:
			loop_vertex = self.propagators[list(chords)[0]].vertex1
			loop_vertices = [loop_vertex]

		elif len(chords) == 2:
			loop_vertices = [
					self.propagators[list(chords)[0]].vertex1,
					self.propagators[list(chords)[0]].vertex2
				]
		else:
			loop_vertices = []
			while len(loop_vertices) < len(loop):
				for i, s in loop.items():
					if len(loop_vertices) >= len(loop):
						break

					if s == 1:
						p = [self.propagators[i].vertex1,
							self.propagators[i].vertex2]
					else:
						p = [self.propagators[i].vertex2,
							self.propagators[i].vertex1]

					if loop_vertices == []:
						loop_vertices = p
					elif loop_vertices[-1] == p[0]:
						loop_vertices.append(p[1])

		bridges.difference_update(chords)
		bridges = list(bridges)

		if len(chords) <= 2:
			df = 0.3
		elif len(chords) == 3:
			df = 0.5
		elif len(chords) == 4:
			df = 0.7
		else:
			df = 1.0

		for idx in chords:
			prop = self.propagators[idx]
			prop.setForce(prop.force() * df)

		leg_order = []
		for vertex in loop_vertices:
			leg_order.extend(self.visit_legs(vertex, bridges))

		# Place legs along an ellipse that fits in the diagram boundaries;
		# all angles in degrees
		phi = 45.0
		if len(loop_vertices) == 1:
			delta_phi = (360.0 - 45.0) / len(leg_order)
		else:
			delta_phi = 360.0 / len(leg_order)

		for lg in leg_order:
			x = width / 2.0 + width / 2.0 * math.sin(math.radians(phi))
			y = height / 2.0 + height / 2.0 * math.cos(math.radians(phi))
			lg.set_coord(x, y)
			phi += delta_phi

		if len(loop_vertices) == 1:
			# in the case of a tadpole diagram pull the tadpole towards 0 degree
			x = width / 2.0 + width / 2.0 * math.sin(0.0)
			y = height / 2.0 + height / 2.0 * math.cos(0.0)
			fld = field("null", "ZERO", 1, 0, 1)
			lg = leg(fld, 0, loop_vertices[0])
			lg.set_coord(x, y)
			lg.setInvisible()
			self.ref_point = (x, y)
			self.fin[-1] = lg
		else:
			self.ref_point = (width/2.0, height/2.0)
		for p in self.propagators.values():
				if p.field1.name == 'RENO':
					p.setInvisible()
				#print p.field1.linestyle()
	
		eqs = self.setup_equations()
		eqs.solve()

		for i, v in self.vertices.items():
			x, y = eqs.rhs[i - 1]
			v.set_coord(x, y)

		chords = list(chords)
		if len(chords) == 1:
			self.propagators[chords[0]].bend = 2
		elif len(chords) == 2:
			r = L.pop()
			p1 = self.propagators[chords[0]]
			p2 = self.propagators[chords[1]]
			if p1.vertex1 == p2.vertex1:
				p1.bend = 1
				p2.bend = -1
			else:
				p1.bend = 1
				p2.bend = 1




	def layout_2loop(self, *args, **opts):
		height = opts['height']
		width  = opts['width']

		L = self.find_loops()
		assert len(L) <= 2
		props = set(self.propagators.keys())
		#chords = set()
		chords2loop=[]
		bridges = set(props)

		loop_vertices = []
	
		#if len(L) == 2:
			#loop = L.copy().pop()
			#chords.update(loop.keys())
		for loop in L:
			chords2loop.append(set(loop.keys()))

		chords=chords2loop[0]
		if len(chords) == 0:
			loop_vertices = [1]
		elif len(chords) == 1:
			loop_vertex = self.propagators[list(chords)[0]].vertex1
			loop_vertices = [loop_vertex]

		elif len(chords) == 2:
			loop_vertices = [
					self.propagators[list(chords)[0]].vertex1,
					self.propagators[list(chords)[0]].vertex2
				]
		else:
			loop_vertices = []
			while len(loop_vertices) < len(loop):
				for i, s in loop.items():
					if len(loop_vertices) >= len(loop):
						break

					if s == 1:
						p = [self.propagators[i].vertex1,
							self.propagators[i].vertex2]
					else:
						p = [self.propagators[i].vertex2,
							self.propagators[i].vertex1]

					if loop_vertices == []:
						loop_vertices = p
					elif loop_vertices[-1] == p[0]:
						loop_vertices.append(p[1])

		bridges.difference_update(chords)
		bridges = list(bridges)

		if len(chords) <= 2:
			df = 0.3
		elif len(chords) == 3:
			df = 0.5
		elif len(chords) == 4:
			df = 0.7
		else:
			df = 1.0

		for idx in chords:
			prop = self.propagators[idx]
			prop.setForce(prop.force() * df)

		leg_order = []
		for vertex in loop_vertices:
			leg_order.extend(self.visit_legs(vertex, bridges))

		# Place legs along an ellipse that fits in the diagram boundaries;
		# all angles in degrees
		phi = 45.0
		if len(loop_vertices) == 1:
			delta_phi = (360.0 - 45.0) / len(leg_order)
		else:
			delta_phi = 360.0 / len(leg_order)

		for lg in leg_order:
			x = width / 2.0 + width / 2.0 * math.sin(math.radians(phi))
			y = height / 2.0 + height / 2.0 * math.cos(math.radians(phi))
			lg.set_coord(x, y)
			phi += delta_phi

		if len(loop_vertices) == 1:
			# in the case of a tadpole diagram pull the tadpole towards 0 degree
			x = width / 2.0 + width / 2.0 * math.sin(0.0)
			y = height / 2.0 + height / 2.0 * math.cos(0.0)
			fld = field("null", "ZERO", 1, 0, 1)
			lg = leg(fld, 0, loop_vertices[0])
			lg.set_coord(x, y)
			lg.setInvisible()
			self.ref_point = (x, y)
			self.fin[-1] = lg
		else:
			self.ref_point = (width/2.0, height/2.0)
		for p in self.propagators.values():
				if p.field1.name == 'RENO':
					p.setInvisible()
				#print p.field1.linestyle()
	
		eqs = self.setup_equations()
		eqs.solve()

		for i, v in self.vertices.items():
			x, y = eqs.rhs[i - 1]
			v.set_coord(x, y)

		chords = list(chords)
		if len(chords) == 1:
			self.propagators[chords[0]].bend = 2
		elif len(chords) == 2:
			r = L.pop()
			p1 = self.propagators[chords[0]]
			p2 = self.propagators[chords[1]]
			if p1.vertex1 == p2.vertex1:
				p1.bend = 1
				p2.bend = -1
			else:
				p1.bend = 1
				p2.bend = 1
		#sys.exit()



	def setup_equations(self, **opts):
		n = len(self.vertices)
		eqs = equationsystem(n)

		for prop in self.propagators.values():
			t = prop.force()
			i = prop.vertex1 - 1
			j = prop.vertex2 - 1
			if i != j:
				eqs[(i, j)] = eqs[(i, j)] - t
				eqs[(j, i)] = eqs[(j, i)] - t
				eqs[(i, i)] = eqs[(i, i)] + t
				eqs[(j, j)] = eqs[(j, j)] + t

		for legs in [self.ini, self.fin]:
			for leg in legs.values():
				l = leg.force()
				lx, ly = leg.get_coord()
				i = leg.vertex - 1
				eqs[(i, i)] = eqs[(i, i)] + l
				x, y = eqs.rhs[i]
				eqs.rhs[i] = (x + l * lx, y + l * ly)

		return eqs

	def visit_legs(self, vertex, bridges):
		"""
		Order the external legs such that the diagram can be
		drawn without line crossings.
		"""
		result = []
		direct_legs = []

		for leg in self.ini.values():
			if leg.vertex == vertex:
				direct_legs.append(leg)

		for leg in self.fin.values():
			if leg.vertex == vertex:
				direct_legs.append(leg)

		for i in range(len(bridges)):
			prop = self.propagators[bridges[i]]
			if prop.vertex1 == vertex:
				new_bridges = bridges[:]
				del new_bridges[i]
				more_legs = self.visit_legs(prop.vertex2, new_bridges)
				result.extend(more_legs)
			elif prop.vertex2 == vertex:
				new_bridges = bridges[:]
				del new_bridges[i]
				more_legs = self.visit_legs(prop.vertex1, new_bridges)
				result.extend(more_legs)

		n = len(direct_legs)
		m = n // 2

		result = direct_legs[0:m] + result + direct_legs[m:n]

		return result
	
	def find_loops(self):
		"""
		Algorithm 4 in my thesis (p. 43)
		"""

		# Initialization

		G = []
		L = set()
		F = {}
		R = {}

		for i, p in self.propagators.items():
			G.append( (p.vertex1, p.vertex2, i) )

		for i in self.vertices.keys():
			F[i] = i
			R[i] = z3chain()

		# The main algorithm

		for (i, j, p) in G:
			ai, pi = A(i, F, R)
			aj, pj = A(j, F, R)
			pij = pj - pi + z3chain({p: 1})

			if ai != aj:
				F[ai] = aj
				R[ai] = pij
			else:
				L.add(pij)

		return L

	def draw(self, f, lookup=None, *args, **opts):
		frame = 10
		f.write("\\begin{picture}(%d,%d)(%d,%d)\n" %
			(opts['width']+2*frame, opts['height']+2*frame,-frame,-frame))
		for dic in [self.ini, self.fin, self.vertices, self.propagators]:
			for obj in dic.values():
				obj.draw(f, self, lookup, *args, **opts)
		f.write("\\end{picture}\n")


class vertex:

	def __init__(self, degree, *fields):
		self.degree = degree
		assert len(fields) == degree
		self.rays = fields
		self.set_coord(0, 0)

	def set_coord(self, x, y):
		self.x = x
		self.y = y

	def get_coord(self):
		return (self.x, self.y)

	def draw(self, f, diag, lookup=None, *args, **opts):
		fields = []
		ctdiag = False
		for field in self.rays:
			if field.name == 'RENO':
				ctdiag=True
			fields.append(field.name)
		sfields = "%% %s vertex" % "-".join(fields)

		if "vsize" in opts:
			vsize = opts["vsize"]
		else:
			vsize = 2

		x, y = self.get_coord()

		if ctdiag== True:
			f.write("   \\Cross(%0.1f,%0.1f){%s}{1.0} " % (x, y, vsize))
		else:
			f.write("   \\Vertex(%0.1f,%0.1f){%s} " % (x, y, vsize))
		f.write(sfields + "\n")

class propagator:

	def __init__(self, field1, vertex1, field2, vertex2, momentum):
		self.vertex1 = vertex1
		self.vertex2 = vertex2
		self.field1 = field1
		self.field2 = field2
		self.momentum = momentum
		self.bend = 0
		self._force = 1.0
		self.is_invisible = False

	def setInvisible(self):
		self.is_invisible = True

	def draw(self, f, diag, lookup=None, *args, **opts):
		if self.is_invisible:
			return

		v1 = diag.vertices[self.vertex1]
		v2 = diag.vertices[self.vertex2]
		if "latex" in opts:
			latex_names = opts["latex"]
			name = self.field2.name
			if name in latex_names:
				label = "$%s$" % latex_names[name]
			else:
				label = "$%s$" % name
		f.write("   ")
		if self.bend == 0:
			self.field1.draw_line(f, v1.x, v1.y, v2.x, v2.y, lookup, 
					label=label, **opts)
		elif self.bend == 1:
			mx = (v1.x + v2.x) / 2.0
			my = (v1.y + v2.y) / 2.0
			dx = (v1.x - v2.x)
			dy = (v1.y - v2.y)
			r = math.sqrt(dx*dx + dy*dy) / 2.0
			phi = math.degrees(math.atan2(dy, dx))
			self.field1.draw_arc(f, mx, my, r, phi, phi + 180, lookup,
				label=label, **opts)
		elif self.bend == -1:
			mx = (v1.x + v2.x) / 2.0
			my = (v1.y + v2.y) / 2.0
			dx = (v1.x - v2.x)
			dy = (v1.y - v2.y)
			r = math.sqrt(dx*dx + dy*dy) / 2.0
			phi = math.degrees(math.atan2(dy, dx))
			#self.field1.draw_arcn(f, mx, my, r, phi - 180, phi, lookup,
			self.field1.draw_arcn(f, mx, my, r, phi, phi - 180, lookup,
				label=label, **opts)
		elif self.bend == 2:
			x1, y1 = diag.ref_point
			mx = (x1 + v2.x) / 2.0
			my = (y1 + v2.y) / 2.0
			dx = (x1 - v2.x)
			dy = (y1 - v2.y)
			r = math.sqrt(dx*dx + dy*dy) / 2.0
			phi = math.degrees(math.atan2(dy, dx))
			self.field1.draw_arc(f, mx, my, r,
					phi - 180.0, phi + 180.0,
					lookup, label=label, **opts)
		else:
			error("don't know what to do: " +
				"self.bend = %r (%s)" % (self.bend, self.bend))


	def setForce(self, value):
		self._force = value

	def force(self):
		return self._force

class leg:

	def __init__(self, field, momentum, vertex_index):
		self.field = field
		self.momentum = momentum
		self.vertex = vertex_index
		self.set_coord(0, 0)
		self.is_initial = False
		self.is_invisible = False

	def setInitial(self):
		self.is_initial = True

	def setInvisible(self):
		self.is_invisible = True

	def set_coord(self, x, y):
		self.x = x
		self.y = y

	def get_coord(self):
		return (self.x, self.y)

	def draw(self, f, diag, lookup=None, *args, **opts):
		if self.is_invisible:
			return

		v = diag.vertices[self.vertex]
		if "latex" in opts:
			latex_names = opts["latex"]
			name = self.field.name
			if self.momentum == "ZERO":
				mstr = ""
			elif self.momentum == "Q1":
				mstr = "(q)"
			elif self.momentum == "Q2":
				mstr = "(-q)"
			elif isinstance(self.momentum, int):
				assert self.momentum == 0
				mstr = ""
			else:
				mstr = "(k_{%s})" % self.momentum[1:]

			if name in latex_names:
				label = "$%s%s$" % (latex_names[name], mstr)
			else:
				label = "$%s%s$" % (name, mstr)
		f.write("   ")

		if self.field.is_conjugate:
			s1 = -1
		else:
			s1 = 1

		if self.is_initial:
			s2 = 1
		else:
			s2 = -1

		if s1 * s2 > 0:
			self.field.draw_line(f, self.x, self.y, v.x, v.y,
					lookup, label=label, labelpos="start", **opts)
		else:
			self.field.draw_line(f, v.x, v.y, self.x, self.y,
					lookup, label=label, labelpos="end", **opts)

	def __repr__(self):
		return "leg(%r, %r, %r)" % (self.field, self.momentum, self.vertex)

	def __str__(self):
		return "%s(%s)" % (self.field.name, self.momentum)

	def force(self, **opts):
		if "legforce" in opts:
			return opts["legforce"]
		else:
			return 1.0

class field:
	def __init__(self, name, mass, conjugate, twospin, color):
		self.name = name
		self.mass = mass
		self.is_conjugate = (conjugate < 0)
		self.two_spin = twospin
		self.color = color

	def linestyle(self, lookup=None):
		"""
		Selects an appropriate line style from the
		range of AxoDraw commands, depending on
		the spin and the color of the particle.

		RESULT
			A list of three or more entries. The first three elements
			are the commands for drawing a line, a counterclockwise arc
			and a clockwise arc respectively. If the list contains
			more than three elements the remaining values are the names
			of additional parameters.
		"""
		styles = {
				'fermion': ['\\ArrowLine', '\\ArrowArc', '\\ArrowArcn'],
				'majorana': ['\\Line', '\\CArc', '\\CArc'],
				'ghost': ['\\DashArrowLine', '\\DashArrowArc', '\\DashArrowArcn',
					'ghdashsize'],
				'scalar': ['\\DashLine', '\\DashCArc', '\\DashCArc',
					'sdashsize'],
				'gluon': ['\\Gluon', '\\GlueArc', '\\GlueArc',
					'gamplitude', 'windings'],
				'photon': ['\\Photon', '\\PhotonArc', '\\PhotonArc',
					'pamplitude', 'wiggles'],
				'chargedscalar' : ['\\DashArrowLine', '\\DashArrowArc', '\\DashArrowArcn',
					'sdashsize'],
				'invisible' : ['', '', '',
					'']
			}

		if lookup is not None:
			if self.name in lookup:
				return styles[lookup[self.name]]

		# if no preference for this particle is given use defaults:
		defaults = {
			0: {
					1: 'scalar',
					3: 'scalar',
					8: 'scalar'
				},
			1: {
					1: 'fermion',
					3: 'fermion',
					8: 'fermion'
				},
			2: {
					1: 'photon',
					3: 'photon',
					8: 'gluon'
				},
			3: {
					1: 'fermion',
					3: 'fermion',
					8: 'fermion'
				},
			4: {
					1: 'photon',
					3: 'photon',
					8: 'gluon'
				}
		}

		return styles[defaults[self.two_spin][self.color]]

	def draw_line(self, f, x1, y1, x2, y2, lookup=None, **opts):
		ls = self.linestyle(lookup)

		cmd = ls[0]
		args = ls[3:]
		st = "%s(%0.1f,%0.1f)(%0.1f,%0.1f)" % (cmd, x1, y1, x2, y2)
		dx = x1 - x2
		dy = y1 - y2
		l = math.sqrt(dx*dx+dy*dy)
		for arg in args:
			if arg in opts:
				value = opts[arg]
			else:
				value = 2

			if arg in ["wiggles", "windings"]:
				w = int(l * float(value) + 0.5)
				st = st + ("{%d}" % w)
			else:
				st = st + ("{%s}" % value)

		f.write(st)
		f.write(" %% %s-propagator\n" % self.name)

		if "label" in opts:
			# print a label
			mx = (x1 + x2) / 2.0
			my = (y1 + y2) / 2.0
			phi = math.atan2(dy, dx)

			dr =  3.0

			fx = mx + dr * math.sin(phi)
			fy = my - dr * math.cos(phi)
			if "labelpos" in opts:
				pos = opts["labelpos"].lower()
				if pos == "start":
					fx = x1 + dr * math.sin(phi)
					fy = y1 + dr * math.cos(phi)
				elif pos == "end":
					fx = x2 + dr * math.sin(phi)
					fy = y2 + dr * math.cos(phi)
			mode = ""
			if fx > mx:
				mode += "l"
			else:
				mode += "r"
			if fy > my:
				mode += "b"
			else:
				mode += "t"

			f.write("   \Text(%0.1f,%0.1f)[%s]{%s}\n" %
					(fx, fy, mode, opts["label"]))

	def draw_arc(self, f, x, y, r, phi1, phi2, lookup=None, **opts):
		ls = self.linestyle(lookup)
		cmd = ls[1]
		args = ls[3:]
		dphi = phi2 - phi1
		while dphi < 0:
			dphi += 360
		l = math.radians(dphi) * r
		st = "%s(%d,%d)(%d,%d,%d)" % (cmd, x, y, r, phi1, phi2)
		for arg in args:
			if arg in opts:
				value = opts[arg]
			else:
				value = 2

			if arg in ["wiggles", "windings"]:
				w = int(l * float(value) + 0.5)
				st = st + ("{%d}" % w)
			else:
				st = st + ("{%s}" % value)

		f.write(st)
		f.write(" %% %s-propagator\n" % self.name)

		if "label" in opts:
			# print a label

			phim = (phi1 + phi2) / 2.0
			while phim < 0.0:
				phim += 360.0
			while phim > 360.0:
				phim -= 360.0
			phim = math.radians(phim)

			dr =  3.0

			fx = x + (r + dr) * math.cos(phim)
			fy = y + (r + dr) * math.sin(phim)
			mode = ""
			if fx > x:
				mode += "l"
			else:
				mode += "r"
			if fy > y:
				mode += "b"
			else:
				mode += "t"

			f.write("   \Text(%0.1f,%0.1f)[%s]{%s}\n" %
					(fx, fy, mode, opts["label"]))

	def draw_arcn(self, f, x, y, r, phi1, phi2, lookup=None, **opts):
		ls = self.linestyle(lookup)

		invar = ls[2] == ls[1]
		cmd = ls[2]
		args = ls[3:]
		dphi = phi2 - phi1
		while dphi < 0:
			dphi += 360
		l = math.radians(dphi) * r
		if invar:
			st = "%s(%d,%d)(%d,%d, %d)" % (cmd, x, y, r, phi2, phi1)
		else:
			st = "%s(%d,%d)(%d,%d, %d)" % (cmd, x, y, r, phi1, phi2)
		for arg in args:
			if arg in opts:
				value = opts[arg]
			else:
				value = 2

			if arg in ["wiggles", "windings"]:
				w = int(l * float(value) + 0.5)
				st = st + ("{%d}" % w)
			else:
				st = st + ("{%s}" % value)
		f.write(st)
		f.write(" %% %s-propagator\n" % self.name)
		if "label" in opts:
			# print a label
			phim = (phi1 + phi2) / 2.0
			while phim < 0.0:
				phim += 360.0
			while phim > 360.0:
				phim -= 360.0
			phim = math.radians(phim)

			dr =  3.0

			fx = x + (r + dr) * math.cos(phim)
			fy = y + (r + dr) * math.sin(phim)
			mode = ""
			if fx > x:
				mode += "l"
			else:
				mode += "r"
			if fy > y:
				mode += "b"
			else:
				mode += "t"

			f.write("   \Text(%0.1f,%0.1f)[%s]{%s}\n" %
					(fx, fy, mode, opts["label"]))

	def __repr__(self):
		return "field(%r, %r, %r, %r, %r)" % (
				self.name, self.mass, self.is_conjugate,
				self.two_spin, self.color)

	def __str__(self):
		return "%s" % (self.name)

def sign(x):
	if x > 0:
		return 1
	else:
		return -1

class z3chain:

	def __init__(self, values={}):
		self._values = values.copy()
		self.canonical()


	def canonical(self):
		z = []
		for i, v in self.items():
			if v == 0:
				z.append(i)

		for i in z:
			del self[i]

	def __getattr__(self, name):
		return self._values.__getattribute__(name)

	def __add__(self, other):
		keys = set(self.keys()).union(set(other.keys()))
		result = z3chain()
		for i in keys:
			result[i] = self[i] + other[i]
		return result

	def __sub__(self, other):
		keys = set(self.keys()).union(set(other.keys()))
		result = z3chain()
		for i in keys:
			result[i] = self[i] - other[i]
		return result

	def __neg__(self):
		result = z3chain()
		for i in self.keys():
			result[i] = - self[i]
		return result

	def __getitem__(self, idx):
		if idx in self._values:
			return self._values[idx]
		else:
			return 0

	def __setitem__(self, idx, value):
		if value == 0:
			if idx in self._values:
				del self._values[idx]
		else:
			self._values[idx] = value

	def __nonzero__(self):
		self.canonical()
		return len(self._values) > 0

	def __eq__(self, other):
		return (self - other).__nonzero__()

	def __len__(self):
		return len(self._values)

	def __hash__(self):
		hash = "z3chain".__hash__()
		for i, s in self.items():
			hash += s * i
		return hash

	def __repr__(self):
		return "z3chain(%r)" % self._values

	def __str__(self):
		st = "<"
		flag = True
		for i, s in self.items():
			if s == 1:
				if flag:
					st += "%d" % i
				else:
					st += "+%d" % i
				flag = False
			elif s == -1:
				st += "-%d" % i
				flag = False
			elif s == 0:
				pass
			else:
				st += "(%d)%d" % (s, i)
				flag = False

		if flag:
			st += "0"
		st += ">"
		return st

	def copy(self):
		return z3chain(self._values.copy())

class equationsystem:
	"""
	Sets up a system of linear equations for calculating the
	positions of the vertices.
	"""
	def __init__(self, n):
		self._size = n
		self._matrix = [[0.0 for j in range(n)] for i in range(n)]
		self._x = [0.0 for i in range(n)]
		self._y = [0.0 for i in range(n)]
		self.rhs = rhs_pointer(self)

	def __getitem__(self, coord):
		i, j = coord
		return self._matrix[i][j]

	def __setitem__(self, coord, value):
		i, j = coord
		self._matrix[i][j] = value


	def __len__(self):
		return self._size

	def __str__(self):
		n = self._size
		result = "<equations>\n"
		for i in range(n):
			for j in range(n):
				result += "%6.1f " % self[(i, j)]
			result += "| %6.1f %6.1f <br/>\n" % self.rhs[i]
		result += "</equations>"

		return result

	def swap_rows(self, i, j):
		if i == j:
			return

		temp = self._matrix[i]
		self._matrix[i] = self._matrix[j]
		self._matrix[j] = temp

		self._x[i], self._x[j] = self._x[j], self._x[i]
		self._y[i], self._y[j] = self._y[j], self._y[i]

	def pivot(self, i):
		maxrow = i
		maxval = abs(self._matrix[maxrow][i])

		for j in range(i+1, self._size):
			if maxval < abs(self._matrix[j][i]):
				maxrow = j
				maxval = abs(self._matrix[maxrow][i])

		self.swap_rows(i, maxrow)

	def noise(self):
		return (random.random() - 0.5) * 1.0E-4

	def solve(self):
		random.seed()
		n = self._size

		for y in range(n):
			self.pivot(y)

			a = self._matrix[y][y]
			while abs(a) < 1.0E-10:
				a = self.noise()

			self._matrix[y][y] = a
			for y2 in range(y+1, n):
				c = self._matrix[y2][y] / a
				for x in range(y, n):
					self._matrix[y2][x] -= self._matrix[y][x] * c

				self._x[y2] -= self._x[y] * c
				self._y[y2] -= self._y[y] * c

		# Backsubstitution

		for y in range(n - 1, -1, -1):
			c = self._matrix[y][y]
			for y2 in range(y):
				a = self._matrix[y2][y]
				self._x[y2] -= self._x[y] * a / c
				self._y[y2] -= self._y[y] * a / c
				for x in range(n - 1, y - 1, -1):
					self._matrix[y2][x] -= self._matrix[y][x] * a / c
			self._matrix[y][y] = 1.0
			self._x[y] /= c
			self._y[y] /= c

class rhs_pointer:
	def __init__(self, les):
		self._les = les

	def __getitem__(self, idx):
		return (self._les._x[idx], self._les._y[idx])

	def __setitem__(self, idx, value):
		x, y = value
		self._les._x[idx] = x
		self._les._y[idx] = y

