# vim: ts=3:sw=3

# This is a re-implementation of my earlier 'FormFactory.java'
# program.
#
# The following assumptions have been made:
# - No q_a have been used, instead we only deal with powers of the
#   integration momentum (in form of the tensor ptens).
# - r_n = 0

__author__ = "Thomas Reiter <thomasr@nikhef.nl>"

import sys
import os
import os.path
import golem.util.path

from golem.algorithms.color import permutations

class FormFactorPrinter:
	def __init__(self, aFile):
		self.f = aFile
		self.g_format = "d(%s, %s)"
		self.i_format = "idx%d"
		self.p_format = "j(%d)"
		self.a_format = "a%s%s"
		self.b_format = "b%s%s"
		self.c_format = "c%s%s"
		self.arg_format = "(%s)"

	def set_format_p(self, fmt):
		self.p_format = fmt

	def set_format_a(self, fmt):
		self.a_format = fmt

	def set_format_b(self, fmt):
		self.b_format = fmt

	def set_format_c(self, fmt):
		self.c_format = fmt

	def set_format_arg(self, fmt):
		self.arg_format = fmt

	def a(self, n, r, *args):
		sargs = ", ".join(map(lambda i: self.p_format % i, args))
		return (self.a_format % (n, r)) + (self.arg_format % sargs)

	def b(self, n, r, *args):
		sargs = ", ".join(map(lambda i: self.p_format % i, args))
		return (self.b_format % (n, r)) + (self.arg_format % sargs)

	def c(self, n, r, *args):
		sargs = ", ".join(map(lambda i: self.p_format % i, args))
		return (self.c_format % (n, r)) + (self.arg_format % sargs)

	def set_format_g(self, fmt):
		self.g_format = fmt

	def set_format_i(self, fmt):
		self.i_format = fmt

	def i(self, k, isPattern = False):
		if isPattern:
			return (self.i_format % k) + "?"
		else:
			return self.i_format % k

	def g(self, i, j):
		return self.g_format % (i, j)

	def r(self, k, idx):
		return "d_(`r%d', %s)" % (k, idx)

	def generate(self, n, r):
		"""
		Generates the substitution rule for an n-point rank-r
		tensor integral.
		"""
		symmetries = {}
		symmetries[self.a_format % (n, r)] = r;
		if n < 6:
			if r >= 2:
				symmetries[self.b_format % (n, r)] = r - 2;

			if r >= 4:
				symmetries[self.c_format % (n, r)] = r - 4;

		self.f.write("#Procedure TI%dr%d(%s)\n" %
				(n, r, ",".join(map(lambda i: "r%d" % i, range(1, n + 1)))))
		self.f.write("\tId ptens(%s) = \n" %
				", ".join(map(lambda i: self.i(i, True), range(1, r + 1))))
		self.generateFF(n, r, 0)
		if n < 6:
			self.generateFF(n, r, 2)
			self.generateFF(n, r, 4)

		self.f.write("\t;\n")
		for name, args in symmetries.iteritems():
			if args > 0:
				self.f.write("\tSymmetrize %s 1, ..., %d;\n" % (name, args))
		self.f.write("#EndProcedure\n\n")

		for name in symmetries.keys():
			self.f.write("CFunction %s;\n" % name)

		return symmetries.keys()

	def generateFF(self, n, r, g):
		for gset, rset in selections(r, g):
			g_indices = map(lambda i: self.i(i), gset)
			r_indices = map(lambda i: self.i(i), rset)


			for args in combinations(n-1, r - g):
				r_tensor = [self.r(k, i) for k, i in zip(args, r_indices)]
				if g == 0:
					ff = self.a(n, r, *args)
				elif g == 2:
					ff = self.b(n, r, *args)
				elif g == 4:
					ff = self.c(n, r, *args)
				else:
					ff = "ERROR(g = %d)" % g

				for term in symmetric_tensor(*g_indices):
					g_tensor = [self.g(i1, i2) for i1, i2 in term]
					factors = g_tensor + r_tensor + [ff]
					self.f.write("+ %s\n" % "*".join(factors))

def symmetric_tensor(*indices):
	"""
	Generate the symmetric tensor constructed from all
	possible pairings of the indices into products of metric tensors.

	Yields the terms in form of a list of pairs of indices.
	"""
	assert len(indices) % 2 == 0
	if indices == []:
		yield []
		return

	N = len(indices) // 2
	for s1, s2 in selections(2*N, N):
		if s1 != []:
			if s1[0] != 1:
				break
		for p in permutations(s2):
			result = []
			skipThis = False
			for a, b in zip(s1, p):
				if a > b:
					skipThis = True
					break
				else:
					result.append( (indices[a-1], indices[b-1]) )
			if not skipThis:
				yield result

def selections(n, m):
	"""
	Generates all subsets of length m from the set {1, ..., n}.

	Yields pairs, where the first element contains the subset
	of size m and the second element contains the dual subset
	of size (n - m)
	"""
	if n < m:
		return

	marker = range(1, m + 1)
	dual = range(m + 1, n + 1)

	yield (marker[:], dual[:])
	hasMoreElements = True

	while hasMoreElements:
		hasMoreElements = False
		for i in range(m - 1, -1, -1):
			if marker[i] <= n - (m - i):
				for j in range(m - 1, i - 1, -1):
					marker[j] = marker[i] + 1 + (j - i)
				hasMoreElements = True
				j = 0
				k = 1
				for p in marker:
					for l in range(k, p):
						dual[j] = l
						j += 1
					k = p + 1
				for l in range(k, n + 1):
					dual[j] = l
					j += 1

				assert len(set(marker) & set(dual)) == 0, \
						"marker = %r, dual = %r" % (marker, dual)
				assert len(marker) == m, \
						"marker = %r, len(marker) != %d" % (marker, m)
				assert len(dual) == n - m, \
						"dual = %r, len(dual) != %d" % (dual, n - m)
				yield (marker[:], dual[:])
				break

def combinations(n, m):
	"""
	Creates all elements of the set {1, ..., n}^.

	The result is in form of a list [i_1, ..., i_r].
	"""

	marker = [1 for i in range(m)]
	hasMoreElements = True
	yield marker[:]

	if m == 0:
		return

	while hasMoreElements:
		hasMoreElements = False
		marker[m - 1] += 1
		for i in range(m - 1, -1, -1):
			if marker[i] > n:
				marker[i] = 1
				if i > 0:
					marker[i-1] += 1
			else:
				hasMoreElements = True
				yield marker[:]
				break

if __name__ == "__main__":

	print("GOLEM 2.0: Form Factor Generator")
	path = golem.util.path.golem_path("src", "form")
	print("Installing files into [%s]" % path)

	for arg in sys.argv[1:]:
		n = int(arg)
		f = open(os.path.join(path, "ff-%d.hh" % n), "w")
		p = FormFactorPrinter(f)

		f.write("* vim: ts=3:sw=3\n")
		f.write("* This file has been automatically generated\n")
		f.write("* using the program %s\n" % sys.argv[0])
		for r in range(n + 1):
			f.write("*---#[ Procedure TI%dr%d :\n" % (n, r))
			p.generate(n, r)
			f.write("*---#] Procedure TI%dr%d :\n" % (n, r))
		f.close()
