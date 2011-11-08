# vim: ts=3:sw=3
"""
This file contains the routines from the main program which
are concerned with color.
"""
import os.path

import golem.algorithms.color

def color_latex(f, in_particles, out_particles):
	error("DEPRECATED: golem.misc_color.color_latex")
	result = ""
	quarks = []
	aquarks = []
	gluons = []
	particles = []
	colored = []
	wf = []
	for i in range(len(in_particles)):
		p = in_particles[i]
		if p.getColor() == 3:
			color_index = "i_%d" % (i+1)
			quarks.append(color_index)
			colored.append(i+1)
			wf.append("q^{(%d)}_{%s}" % (i+1, color_index))
		elif p.getColor() == -3:
			color_index = "j_%d" % (i+1)
			aquarks.append(color_index)
			colored.append(i+1)
			wf.append("\\bar{q}^{(%d)}_{%s}" % (i+1, color_index))
		elif p.getColor() == 8 or p.getColor() == -8:
			color_index = "A_%d" % (i+1)
			gluons.append(color_index)
			colored.append(i+1)
			wf.append("g_{(%d)}^{%s}" % (i+1, color_index))
		else:
			continue
		particles.append(color_index)

	li = len(in_particles)
	for i in range(len(out_particles)):
		p = out_particles[i]
		if p.getColor() == 3:
			color_index = "j_%d" % (li+i+1)
			aquarks.append(color_index)
			colored.append(i+li+1)
			wf.append("\\bar{q}^{(%d)}_{%s}" % (li+i+1, color_index))
		elif p.getColor() == -3:
			color_index = "i_%d" % (li+i+1)
			quarks.append(color_index)
			colored.append(i+li+1)
			wf.append("q^{(%d)}_{%s}" % (li+i+1, color_index))
		elif p.getColor() == 8 or p.getColor() == -8:
			color_index = "A_%d" % (li+i+1)
			gluons.append(color_index)
			colored.append(i+li+1)
			wf.append("{g^\\ast_{(%d)}}^{%s}" % (li+i+1, color_index))
		else:
			continue
		particles.append(color_index)

	flag = False
	num_color = 0
	for lines, traces in golem.algorithms.color.colorbasis(
			quarks, aquarks, gluons):
		num_color += 1

		s_lines = wf[:]
		for line in lines:
			N = len(line)
			if N == 2:
				s_lines.append("\\delta_{%s%s}" % (line[0], line[1]))
			else:
				string = []
				for aidx in line[1:N-2]:
					string.append("T^{%s}" % (aidx))
				string.append("T^{%s}" % (line[N-2]))
				s_lines.append("(%s)_{%s%s}" % (
					"".join(string), line[0], line[N-1]))
			
		for tr in traces:
			N = len(tr)
			string = []
			for aidx in tr[1:N]:
				string.append("T^{%s}" % aidx)
			string.append("T^{%s}" % tr[0])
			s_lines.append("\\mathrm{tr}\\{%s\\}" % "".join(string))

		if flag:
			f.write("\\\\\n")
		else:
			flag = True

		f.write("\\vert c_{%d}\\rangle &= %s" % (num_color,
			"".join(s_lines) if len(s_lines) > 0 else "1"))

	if flag:
		f.write("\n")

def write_color_basis(f, in_particles, out_particles):
	"""
	Find all colored particles and build a color basis
	"""
	ini_fundamental = []
	fin_fundamental = []

	quarks = []
	aquarks = []
	gluons = []
	particles = []
	wf = []
	in_colors = []
	for i in range(len(in_particles)):
		p = in_particles[i]
		color_index = "idxi%dC%d?" % (i+1, abs(p.getColor()))

		wf.append("inpcolor(%d, %s)" % (i+1, color_index))
		if p.getColor() == 3:
			quarks.append(color_index)
			in_colors.append("NC")
		elif p.getColor() == -3:
			aquarks.append(color_index)
			in_colors.append("NC")
			ini_fundamental.append(i+1)
		elif p.getColor() == 8:
			gluons.append(color_index)
			in_colors.append("NA")

	for i in range(len(out_particles)):
		p = out_particles[i]
		color_index = "idxo%dC%d?" % (i+1, abs(p.getColor()))
		wf.append("outcolor(%d, %s)" % (i+1, color_index))
		if p.getColor() == 3:
			aquarks.append(color_index)
			fin_fundamental.append(i+1)
		elif p.getColor() == -3:
			quarks.append(color_index)
		elif p.getColor() == 8:
			gluons.append(color_index)

	f.write("*---#[ procedure colorbasis :\n")
	f.write("#procedure colorbasis\n")
	num_color = 0
	for lines, traces in golem.algorithms.color.colorbasis(
			quarks, aquarks, gluons):
		num_color += 1

		s_lines = wf[:]
		for line in lines:
			N = len(line)
			i = 0
			if N == 2:
				for i in range(len(s_lines)):
					s_lines[i] = s_lines[i].replace(line[0], line[1])
			else:
				string = []
				idx1 = line[0]
				idx2 = "idx%dC3?" % i
				i += 1
				for aidx in line[1:N-2]:
					string.append("T(%s, %s, %s)" % (aidx, idx1, idx2))
					idx1 = idx2
					idx2 = "idx%dC3?" % i
					i += 1
				string.append("T(%s, %s, %s)" % (line[N-2], idx1, line[N-1]))
				s_lines.extend(string)
			
		i = 0
		for tr in traces:
			N = len(tr)
			string = []
			idx0 = "idx%dC3?" % i
			i += 1
			idx1 = idx0
			for aidx in tr[1:N]:
				idx2 = "idx%dC3?" % i
				i += 1
				string.append("T(%s, %s, %s)" % (aidx, idx1, idx2))
				idx1 = idx2
			string.append("T(%s, %s, %s)" % (tr[0], idx1, idx0))
			s_lines.extend(string)
		pattern = "*\n\t\t".join(s_lines)

		f.write("\tId %s = c%d;\n" % (pattern, num_color))

	f.write("#endprocedure\n\n")
	f.write("*---#] procedure colorbasis :\n")

	if num_color > 0:
		f.write("Symbols c1, ..., c%d;\n" % num_color)
	f.write("#define NUMCS \"%d\"\n" % num_color)
	f.write("#define INCOLORS \"%s\"\n" % ",".join(in_colors))
	f.write("#define INIFUNDAMENTAL \"%s\"\n"
			% ",".join(map(str,ini_fundamental)))
	f.write("#define FINFUNDAMENTAL \"%s\"\n"
			% ",".join(map(str,fin_fundamental)))

	return num_color

def write_invcolor_basis(f, in_particles, out_particles):
	"""
	Find all colored particles and build a color basis
	"""
	quarks = []
	aquarks = []
	gluons = []
	particles = []
	colored = []
	wf = []
	wf1 = []
	wf2 = []
	for i in range(len(in_particles)):
		p = in_particles[i]
		color_index = "idxi%dC%d" % (i+1, abs(p.getColor()))
		wf.append("inpcolor(%d, %s`suffix', `num')" % (i+1, color_index))
		wf1.append("inpcolor(%d, %sa?, 1)" % (i+1, color_index))
		wf2.append("inpcolor(%d, %sb?, 2)" % (i+1, color_index))
		particles.append(color_index)
		if p.getColor() == 3:
			quarks.append(color_index)
			colored.append(i+1)
		elif p.getColor() == -3:
			aquarks.append(color_index)
			colored.append(i+1)
		elif p.getColor() == 8:
			gluons.append(color_index)
			colored.append(i+1)
	for i in range(len(out_particles)):
		p = out_particles[i]
		color_index = "idxo%dC%d" % (i+1, abs(p.getColor()))
		wf.append("outcolor(%d, %s`suffix', `num')" % (i+1, color_index))
		wf1.append("outcolor(%d, %sa?, 1)" % (i+1, color_index))
		wf2.append("outcolor(%d, %sb?, 2)" % (i+1, color_index))
		particles.append(color_index)
		if p.getColor() == 3:
			aquarks.append(color_index)
			colored.append(i+len(in_particles)+1)
		elif p.getColor() == -3:
			quarks.append(color_index)
			colored.append(i+len(in_particles)+1)
		elif p.getColor() == 8:
			gluons.append(color_index)
			colored.append(i+len(in_particles)+1)

	f.write("#define COLORED \"%s\"\n" % ",".join(map(str, colored)))

	f.write("*---#[ procedure invcolorbasis :\n")
	f.write("#procedure invcolorbasis(suffix,num)\n")
	num_color = 0
	for lines, traces in golem.algorithms.color.colorbasis(
			quarks, aquarks, gluons):
		num_color += 1

		s_lines = wf[:]
		s_lines2 = wf[:]
		for line in lines:
			N = len(line)
			i = 0
			if N == 2:
				string = []
				string.append("d_(%s`suffix', %s`suffix')" %
						(line[0], line[1]))
				s_lines.extend(string)
				s_lines2.extend(string)
			else:
				string = []
				string2 = []
				idx1 = line[0]
				idx2 = "idx%dC3" % i
				i += 1
				for aidx in line[1:N-2]:
					string.append("T(%s`suffix', %s`suffix', %s`suffix')" % 
							(aidx, idx1, idx2))
					string2.append("T(%s`suffix', %s`suffix', %s`suffix')" % 
							(aidx, idx2, idx1))
					idx1 = idx2
					idx2 = "idx%dC3" % i
					i += 1
				string.append("T(%s`suffix', %s`suffix', %s`suffix')" %
						(line[N-2], idx1, line[N-1]))
				string2.append("T(%s`suffix', %s`suffix', %s`suffix')" %
						(line[N-2], line[N-1], idx1))
				s_lines.extend(string)
				s_lines2.extend(string2)
			
		i = 0
		for tr in traces:
			N = len(tr)
			string = []
			string2 = []
			idx0 = "idx%dC3" % i
			i += 1
			idx1 = idx0
			for aidx in tr[1:N]:
				idx2 = "idx%dC3" % i
				i += 1
				string.append("T(%s`suffix', %s`suffix', %s`suffix')" %
						(aidx, idx1, idx2))
				string2.append("T(%s`suffix', %s`suffix', %s`suffix')" %
						(aidx, idx2, idx1))
				idx1 = idx2
			string.append("T(%s`suffix', %s`suffix', %s`suffix')" %
					(tr[0], idx1, idx0))
			string2.append("T(%s`suffix', %s`suffix', %s`suffix')" %
					(tr[0], idx0, idx1))
			s_lines.extend(string)
			s_lines2.extend(string2)
		pattern = "*\n\t\t\t".join(s_lines)
		pattern2 = "*\n\t\t\t".join(s_lines2)

		f.write("\t#if `num' == 1\n")
		f.write("\t\tId c(%d, m?) = c(%d, m) * (\n" % (num_color, num_color))
		f.write("\t\t\t%s);\n" % pattern)
		f.write("\t#else\n")
		f.write("\t\tId c(m?, %d) = c(m, %d) * (\n" % (num_color, num_color))
		f.write("\t\t\t%s);\n" % pattern2)
		f.write("\t#endif\n")
	f.write("#endprocedure\n")
	f.write("*---#] procedure invcolorbasis :\n")

	f.write("*---#[ procedure colorinsertion :\n")
	f.write("#procedure colorinsertion\n")
	for i in range(len(particles)):
		num = i + 1
		if (particles[i] in quarks) or (particles[i] in aquarks):
			rhs = "TR*(NC - 1/NC) * delta(%sa, %sb)" % (
					particles[i], particles[i])
		elif particles[i] in gluons:
			rhs = "NC * d_(%sa, %sb)" % (
					particles[i], particles[i])
		else:
			rhs = "1"
		f.write("\tId propcolor(%d, %d) * %s * %s =\n\t\t%s;\n" %
				(num, num, wf1[i], wf2[i], rhs))

		if (particles[i] in quarks):
			rhs = "T(idxIns, %sa, %sb)" % (
					particles[i], particles[i])
			rhs = [rhs, rhs]
		elif (particles[i] in aquarks):
			rhs = "(-1)*T(idxIns, %sb, %sa)" % (
					particles[i], particles[i])
			rhs = [rhs, rhs]
		elif particles[i] in gluons:
			rhs = "(-i_)*f(idxIns, %sa, %sb)" % (
					particles[i], particles[i])
			rhs = [rhs, rhs]
			#rhs = [("sig_(m-%d) * " % num) + rhs,
			#		 ("sig_(m-%d) * " % num) + rhs]
		else:
			rhs = ["0", "0"]
		f.write("\tId propcolor(%d, m?) * %s * %s =\n"
				% (num, wf1[i], wf2[i]))
		f.write("\t\tpropcolor(%d, m)*%s;\n" % (num, rhs[0]))
		f.write("\tId propcolor(m?, %d) * %s * %s =\n"
				% (num, wf1[i], wf2[i]))
		f.write("\t\tpropcolor(m, %d)*%s;\n" % (num, rhs[1]))

		if (particles[i] in quarks) or (particles[i] in aquarks):
			rhs = "delta(%sa, %sb)" % (particles[i], particles[i])
		elif particles[i] in gluons:
			rhs = "d_(%sa, %sb)" % (particles[i], particles[i])
		else:
			rhs = "1"
		f.write("\tId %s * %s =\n\t\t%s;\n" %
				(wf1[i], wf2[i], rhs))
	f.write("#endprocedure\n")
	f.write("*---#] procedure colorinsertion :\n")

	return num_color

def create_color_tex(conf, in_particles, out_particles):
	"""
	Creates the file color.tex which is included by
	process.tex
	"""
	error("DEPRECATED golem.util.main_color.create_color_tex")
	path = golem.util.tools.process_path(conf)

	file_name = os.path.join(path, "color.tex")
	f = open(file_name, 'w')
	f.write("% vi" + "m: ts=3:sw=3\n")
	color_latex(f, in_particles, out_particles)
	f.close()

