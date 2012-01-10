# vim: ts=3:sw=3

import sys

def generate_mandelstam_set(num_in, num_out, prefix='s', suffix='', infix=''):
	"""
	Generates a set of Mandelstam variables for
	num_in incoming and num_out outgoing particles.
	The momenta obey momentum conservation, i.e.
	k1 + ... + k{num_in} = k{num_in+1} + ... + k{num_in+num_out}

	PARAMETER

	num_in  the number of incoming particles
	num_out the number of outgoing particles
	prefix  the prefix of the Mandelstam variables [Default: 's']
	suffix  see below [Default: '']
	infix   see below [Default: '']

	The parameters prefix, suffix and infix influence how Mandelstam
	variables are represented textually:
		(prefix='s', suffix='', infix='')     ---> s123
		(prefix='es(', suffix=')', infix=',') ---> es(1,2,3)
		(prefix='s_{', suffix='}', infix='')  ---> s_{123}

	RETURN

	Returns a pair (names, substitutions):

	names          a list of symbols which denote
	               the Mandelstam variables of the problem
	substitutions  a two dimensional array, represented by a list
	               of lists. the entries are dictionaries
						representing linear functions in the Mandelstam
						variables. The substitution for 2*k{i}.k{j}
						is stored in substitutions[i-1][j-1].
	EXAMPLE

	# 2->2 kinematics:
	>>> names, substitutions = generate_mandelstam_set(2, 2)

	# the Mandelstam variables are {s1, s2, s3, s4, s12, s23}
	# the replacement for 2*k1.k3 = s12 + s23 - s2 - s4
	>>> print substitutions[0][2] == {'s12': 1, 's23': 1, 's2': -1, 's4': -1}
	True

	"""
	num_legs = num_in + num_out
	cuts = sections(num_legs)
	dual_cuts = sections(num_legs, True)

	def normalize(i):
		if i < 1:
			return i + num_legs
		elif i > num_legs:
			return i - num_legs
		else:
			return i
		
	def find(i, j):
		i = normalize(i)
		j = normalize(j)

		if i < j:
			lst = list(range(i, j + 1))
		elif i == j:
			lst = [i]
		else:
			lst = list(range(i + 1, num_legs + 1)) + list(range(1, j))

		if lst in cuts:
			return lst
		elif lst in dual_cuts:
			return cuts[dual_cuts.index(lst)]
		elif (lst == list(range(i, num_legs + 1))
				+ list(range(1, i))) or (lst == []):
			return []
		else:
			sys.exit("Should never happen: Invalid cut: %r!" % lst)

	names = list(
			map(lambda l: mandelstam_name(prefix, suffix, infix, l), cuts))

	substitutions = []

	for i in range(1, num_legs + 1):
		row = []
		for j in range(1, num_legs + 1):
			if i > j:
				row.append(substitutions[j-1][i-1])
			elif i == j:
				row.append({mandelstam_name(prefix, suffix, infix, [i]): 2})
			else:
				# Use Equation (334) from my thesis.
				# This Equation is defined for ingoing kinematics
				# therefore we get an additional sign if one of
				# the momenta involved is ingoing and one is outgoing.
				if (i <= num_in) and (j > num_in):
					sign = -1
				else:
					sign = 1

				s_pp = mandelstam_name(prefix, suffix, infix, find(i, j))
				s_mm = mandelstam_name(prefix, suffix, infix, find(i+1, j-1))
				s_pm = mandelstam_name(prefix, suffix, infix, find(i, j-1))
				s_mp = mandelstam_name(prefix, suffix, infix, find(i+1, j))
				row.append({s_pp: sign, s_mm: sign, s_pm: -sign, s_mp: -sign})
		substitutions.append(row)

	return (names, substitutions)

def mandelstam_calc(num_in, num_out, prefix='s', suffix='', infix=''):
	"""
	This function returns a dictionary that contains for each
	Mandelstam variables the vectors that are used to calculate it.
	The parameters are as in generate_mandelstam_set.

		e.g. {'s123': [1, 2, -3]} = (k1+k2-k3)^2

	The sign represents the sign in front of the (outgoing) vector.
	"""

	def invert(x):
		if x > num_in:
			return -x
		else:
			return x

	result = {}
	num_legs = num_in + num_out
	cuts = sections(num_legs)
	for cut in cuts:
		name = mandelstam_name(prefix, suffix, infix, cut)
		if len(cut) > 1:
			vecs = list(map(invert, cut))
		else:
			vecs = cut
		result[name] = vecs
	return result


def sections(n, dual=False):
	"""
	Find all ways to cut a cycle of n nodes into two sets
	by cutting two of the edges.

	PARAMETER

	n the number of nodes

	RETURN

	a list of lists of indices from {1, ..., n}, where
	each sublist represents one of the two sets for each cut.

	"""
	result = []
	mom = list(range(1, n+1))
	if dual:
		i1 = 1
		i2 = 0
	else:
		i1 = 0
		i2 = 1
	for i in range(1, n):
		for j in range(0, i):
			sets = [mom[j:i], mom[i:n] + mom[0:j]]
			if len(sets[0]) <= len(sets[1]):
				result.append(sets[i1])
			else:
				result.append(sets[i2])
	return result

def mandelstam_name(prefix, suffix, infix, indices):
	if indices == []:
		return "0"
	else:
		return "%s%s%s" % (
			prefix,
			infix.join(map(number_to_letter, indices)),
			suffix)

def number_to_letter(d):
	"""
	Although it is not a problem of the near future the program
	should be safe for processes with more than 9 particles.
	We continue counting with 10='a', 11='b' through to 'z'.
	"""
	letters = [
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
			'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
			'u', 'v', 'w', 'x', 'y', 'z']
	if (d < 0) or (d >= len(letters)):
		sys.exit("Not enough letters in the alphabet.")
	return letters[d]
