# vim: ts=3:sw=3

"""
This module contains all functions of the main program that are
concerned with the helicity projections of the process
"""

from golem.util.constants import generate_gauge_var

import golem.algorithms.helicity

def helicitylabel(h):
	if h == 0:
		return "0"
	elif h == 1:
		return "+"
	elif h == -1:
		return "-"
	else:
		return "."

def enumerate_helicities(keys, map):
	if len(keys) == 0:
		yield {}
	else:
		key = keys[0]
		for new_map in enumerate_helicities(keys[1:], map):
			for heli in map[key]:
				result = new_map.copy()
				result[key] = heli
				yield result 

def rewrite_helicity_legs(f, in_particles, out_particles, zeroes):
	#lc_args = []
	l_vectors = []
	ext_vectors = []
	light_vectors = []
	f.write("*---#[ procedure rewritelegs :\n")
	f.write("#procedure rewritelegs\n")
	k = 0
	i = 0
	for inp in  in_particles:
		k += 1
		i += 1
		mass = inp.getMass()
		if (mass == "0") or (mass in zeroes):
			massive = False
			ext_vectors.append("k%d" % k)
			light_vectors.append("k%d" % k)
			mass = "0"
		else:
			massive = True
			ext_vectors.append("k%d" % k)
			ext_vectors.append("l%d" % k)
			light_vectors.append("l%d" % k)
			l_vectors.append("l%d" % k)
			#lc_args.append("k%d, l%d, `REFk%d', %s" % (k, k, k, inp.getMass()))
		twospin = inp.getSpin()
		if (twospin == 1) or (twospin == -1):
			f.write("\tId inp(field1?, k%d) = " % k)
			f.write("inp(field1, k%d, `HELi%d');\n" % (k, i))
		elif twospin == 2:
			if massive:
				f.write("\tId inp(field1?, k%d) = " % k)
				f.write("inp(field1, k%d, `HELi%d', l%d, `REFk%d');\n" %
						(k, i, k, k))
			else:
				f.write("\tId inp(field1?, k%d) = " % k)
				f.write("inp(field1, k%d, `HELi%d', `REFk%d');\n" % (k, i, k))

			if generate_gauge_var:
				f.write("\t#If `GAUGEVAR'\n") 
				f.write("\t\tId inplorentz(%d, idx%dL2?, k%d, %s) =\n"
						% (twospin, k, k, mass))
				f.write("\t\t\t+inplorentz(%d, idx%dL2, k%d, %s)\n"
						% (twospin, k, k, mass))
				f.write("\t\t\t+gauge%dz * k%d(idx%dL2);\n" % (k, k, k))
				f.write("\t#EndIf\n") 

	o = 0
	for out in  out_particles:
		k += 1
		o += 1
		mass = out.getMass()
		if (mass == "0") or (mass in zeroes):
			massive = False
			ext_vectors.append("k%d" % k)
			light_vectors.append("k%d" % k)
		else:
			massive = True
			ext_vectors.append("k%d" % k)
			ext_vectors.append("l%d" % k)
			light_vectors.append("l%d" % k)
			l_vectors.append("l%d" % k)
			#lc_args.append("k%d, l%d, `REFk%d', %s" % (k, k, k, out.getMass()))
		twospin = out.getSpin()
		if (twospin == 1) or (twospin == -1):
			f.write("\tId out(field1?, k%d) = " % k)
			f.write("out(field1, k%d, `HELo%d');\n" % (k, o))
		elif twospin == 2 or twospin == -2:
			if massive:
				f.write("\tId out(field1?, k%d) = " % k)
				f.write("out(field1, k%d, `HELo%d', l%d, `REFk%d');\n" %
						(k, o, k, k))
			else:
				f.write("\tId out(field1?, k%d) = " % k)
				f.write("out(field1, k%d, `HELo%d', `REFk%d');\n" % (k, o, k))
			if generate_gauge_var:
				f.write("\t#If `GAUGEVAR'\n") 
				f.write("\t\tId outlorentz(%d, idx%dL2?, k%d, %s) =\n"
						% (twospin, k, k, mass))
				f.write("\t\t\t+outlorentz(%d, idx%dL2, k%d, %s)\n"
						% (twospin, k, k, mass))
				f.write("\t\t\t+gauge%dz * k%d(idx%dL2);\n" % (k, k, k))
				f.write("\t#EndIf\n") 

	f.write("#endprocedure\n")
	f.write("*---#] procedure rewritelegs :\n")

	if len(l_vectors) > 0:
		f.write("Vectors %s;\n" % ", ".join(l_vectors))
	f.write("#define LIGHTLIKE \"%s\"\n" % ",".join(light_vectors))
	f.write("#define EXTERNAL \"%s\"\n" % ",".join(ext_vectors))

