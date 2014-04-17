# vim: ts=3:sw=3

import golem

try:
	from bytes import maketrans
except ImportError:
	from string import maketrans

from golem.util.config import GolemConfigError

WHITESPACE = \
	b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0b\x0c\x0d\x0e\x0f" + \
	b"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1b\x1c\x1d\x1e\x1f" + \
	b"\x20"

PROBLEM_TO_SPACE = maketrans(
		WHITESPACE + b"\\\"\'#|&",
		b" " * (len(WHITESPACE) + 6))

class OLPOrderFile:
	"""
	The syntax of an order file is described in

	T. Binoth et al., ``A proposal for a standard
	interface between Monte-Carlo tools and one-loop programs,''
	[aXiv:1001.1307].

	The document is, however, not clear about some details of the
	language. Therefore we add a description here of how we interpret
	the specification.

	A physical line consists of all characters up to (including)
	a "\n", "\r" or "\r\n", where "\r" denotes the ASCII character 13
	(CR) and "\n" denotes the ASCII character 10 (LF).

	As blank characters all characters in the range ASCII 0 - ASCII 32
	(including) are counted, whereas the characters "\n" and "\r" have
	a special meaning, as described above.

	A logical line consists of the concatenation of physical lines:
	a line which has a "&" (ASCII 38) as its last non-blank character
	is called a continued line. A physical line following a continued
	line is called a continuation line. In the concatenation everything
	following the last "&" including the "&" character is skipped.
	If a continuation line has a "&" as the first non-blank character
	everything to the left of the first "&" is skipped in the continuation
	including the "&" itself. If the first non-blank character of a
	continuation line is not a "&" then everyting left of this character
	(not including the first non-blank character) is skipped in the
	continuation line. If the only non-blank character in a continuation
	line is a single "&" then this line is not counted as a continued line.

	In a logical line, every character following a "#" (ASCII 35) including
	the "#" character itself is considered commentary and therefore
	skipped in the parsing process. Everything else is parsed into tokens,
	whereas tokens are separated by blank characters. The tokens "|" and
	"->" do not have to be separated by blank characters.

	EXTENSION: Considering that in some cases, like for file names,
	it might be necessary to include literal blank characters, two
	extensions are proposed:

	1. The use of single quotes: In a logical line, everything between
	   a pair of single quotes (ASCII 39) is considered a single token.
		The quotes are removed by the parser from the input but are not
		considered part of the token. There is no (Pascal like)
		escaping by doubling (as in: 'Tom''s example').

	2. The use of double quotes: In a logical line, everything between
	   a pair of double quotes (ASCII 34) is considered a single token.
		The quotes are removed by the parser from the input but are not
		considered part of the token. Characters can be escaped by the
		escape sequences established in C-like languages. These are in
		particular:
		- "\\n" (ASCII 10), "\\r" (ASCII 13), "\\f" (ASCII 12), "\\t" (ASCII 9)
		- "\\x" followed by two hexadecimal digits representing
		  the ASCII code of a character
		- any other character following a backslash is taken literally,
		  in particular "\\\\" and "\\\"".

	3. In a logical line a backslash in front of any character switches
	   off its special meaning, in particular in front of a white space
		character or the combinations \\" \\| \\' \\# \\->

	Interpretation of the tokens:

	If a logical line contains the token "->" [aka arrow]
	(to the left of "|", if both are present),
	the line describes a subprocess. There must be one or two integer
	numbers to the left of the arrow and one or more integer numbers
	to the right of the arrow. The interpretation of the subprocess
	stops at "|" character or the end of the line, whatever is encountered
	first.

	All other, non-blank lines describe parameter settings. The first
	token of the line is interpeted as the name of a setting, the remaining
	tokens (up to a possible "|") are taken as a list of values.

	If a logical line contains the token "|" this file is considered
	a contract file rather than an order file. If an order file is
	expected the appearance of a "|" character should produce an
	error message or a warning. Everything after the "|" character
	is the response of the OLP.
	
	In a parameter setting the first token after "|" must be
	"OK" or "Error:". If it is "OK" there must not be any further tokens;
	if it is "Error:" the remaining tokens build up an error message.

	In a subprocess description the "|" must be followed either by
	a list of integer numbers or by an error message starting with the
	token "Error:", as descibed in the previous paragraph.

	It is not clear from the proposal if the interpretation of the names
	etc should be case sensitive. Our strategy is to accept keywords
	independent of their letter case but to keep values, such as file names,
	in their original writing.
	"""

	def __init__(self, source, extensions={
			"double_quotes": False,
			"single_quotes": False,
			"backslash_escape": False
		}):
		"""
		Generates an order-file objects from
		a given source.

		PARAMETER

		source -- If source is a string it is interpreted
		   as a file name; the file of that name is opened
		   and read. Otherwise source is expected to be a
		   (opened) file object or a list of strings 
		   representing the lines of an order file.

		extensions -- a dictionary which allows to switch
		   on certain proposed extensions to the original
			proposal. See syntax description above.
		"""
		if "single_quotes" in extensions:
			self._single_quotes = extensions["single_quotes"]
		else:
			self._single_quotes = False
		if "double_quotes" in extensions:
			self._double_quotes = extensions["double_quotes"]
		else:
			self._double_quotes = False
		if "backslash_escape" in extensions:
			self._backslash_escape = extensions["backslash_escape"]
		else:
			self._backslash_escape = False

		self._options = {}
		self._options_ordered = []
		self._opt_res = {}
		self._opt_res_ordered = []
		self._processes = []
		self._processes_opt_until = []
		self._proc_res = []
		self._processing_instructions = []

		if isinstance(source, str):
			f = open(source)
			try:
				self.__init__(f, extensions)
			finally:
				f.close()
		else:
			parseStatus = None
			line_number = 0
			for line in source:
				line_number += 1
				try:
					parseStatus = self._parseLine(line, line_number, parseStatus)
				except OLPError as ex:
					raise OLPError("While parsing line #%d: %s" %
							(line_number, str(ex)))

	def _parseLine(self, line, line_number, parseStatus):
		if parseStatus is not None:
			# This is a continuation line:
			s = line.lstrip(WHITESPACE)
			if s.startswith("&"):
				s = s[1:]

			s = s.rstrip(WHITESPACE)
			if s.endswith("&"):
				s = s[:-1]
				return parseStatus + s
			else:
				s = parseStatus + s
		else:
			s = line.rstrip(WHITESPACE)
			if s.endswith("&"):
				s = s[:-1]
				return s
	
		# Continuation business is finished.
		# Now tokenize the line

		elements = [[], [], []]
		sp = 0
		is_subprocess = False
		is_contract = False
		is_blank = True
		for tok in self._tokens(s):
			is_blank = False
			if tok == 1:
				sp = 1
				is_subprocess = True
			elif tok == 2:
				sp = 2
				is_contract = True
			else:
				elements[sp].append(tok)

		if not is_blank:
			if is_subprocess:
				if is_contract:
					self._handle_subprocess(line_number, elements[0], elements[1], elements[2])
				else:
					self._handle_subprocess(line_number, elements[0], elements[1])
			else:
				if is_contract:
					self._handle_option(line_number, elements[0][0], elements[0][1:],
							elements[2])
				else:
					self._handle_option(line_number, elements[0][0], elements[0][1:])
		return None

	def _handle_option(self, line_number, name, value, response = None):
		#if name in self._options:
		#	raise OLPError("Option %s has been specified more than once" % name)

		if response is not None:
			if isinstance(self, OLPContractFile):
				self._options[name] = value
				self._options_ordered.append((line_number,name,value))

				if len(response) < 1:
					raise OLPError("Empty response encountered in contract file")

				tmp = response[0].lower()
				if tmp == "ok":
					if len(response) > 1:
						raise OLPError("There is something extra in the response")
				elif tmp != "error:":
					raise OLPError("Invalid response (neither 'OK' nor 'Error:')")

				self._opt_res[name] = response
				self._opt_res_ordered.append( (line_number,name,value,response) )
			else:
				raise OLPError("No response expected in order file")
		else:
			if isinstance(self, OLPContractFile):
				raise OLPError("Response expected in contract file")
			else:
				self._options[name] = value
				self._options_ordered.append((line_number,name,value))
				self._opt_res_ordered.append( (line_number,name, None) )


	def _handle_subprocess(self, line_number, inp, out, response = None):
		if response is not None:
			if isinstance(self, OLPContractFile):
				self._processes.append( (line_number, inp, out) )
				self._processes_opt_until.append(len(self._options_ordered))

				if len(response) < 1:
					raise OLPError("Empty response encountered in contract file")

				tmp = response[0].lower()

				if tmp != "error:":
					values = []
					for token in response:
						try:
							val = int(token)
							values.append(val)
						except ValueError:
							raise OLPError("Invalid integer literal %r in response"
									% token)
					if len(values) != values[0] + 1:
						raise OLPError("Wrong number of channels in response")

				self._proc_res.append(response)
			else:
				raise OLPError("No response expected in order file")
		else:
			if isinstance(self, OLPContractFile):
				raise OLPError("Response expected in contract file")
			else:
				self._processes.append( (line_number, inp, out) )
				self._processes_opt_until.append(len(self._options_ordered))
				self._proc_res.append([])
		pass

	def _tokens(self, line):
		token = ""
		state = 0
		col = 0
		digits = 0
		for ch in line:
			col += 1
			if state == 4:
				if ch == ">":
					if len(token) > 0:
						yield token
						token = ""
					yield 1
					state = 0
					continue
				else:
					token += "-"
					state = 0

			if state == 0:
				if ch in WHITESPACE:
					if len(token) > 0:
						yield token
						token = ""
				elif ch == "\\" and self._backslash_escape:
					state = 1
				elif ch == "\"" and self._double_quotes:
					if len(token) > 0:
						yield token
						token = ""
					state = 2
				elif ch == "\'" and self._single_quotes:
					if len(token) > 0:
						yield token
						token = ""
					state = 3
				elif ch == "|":
					if len(token) > 0:
						yield token
						token = ""
					yield 2
				elif ch == "-":
					state = 4
				elif ch == "#":
					commentary = line[col:]
					if commentary.startswith("@"):
						self._processing_instructions.append(commentary[1:])
					break
				else:
					token += ch
			elif state == 1:
				# backslash extension
				token += ch
				state = 0
			elif state == 2:
				# double quote extension
				if ch == "\"":
					yield token
					token = ""
					state = 0
				elif ch == "\\":
					state = 5
				else:
					token += ch
			elif state == 3:
				# single quote extension
				if ch == "'":
					yield token
					token = ""
					state = 0
				else:
					token += ch
			elif state == 5:
				# after backslash inside double qoutes
				if ch == "n":
					token += "\n"
					state = 2
				elif ch == "t":
					token += "\t"
					state = 2
				elif ch == "r":
					token += "\r"
					state = 2
				elif ch == "f":
					state = 2
					token += "\f"
					state = 2
				elif ch == "x":
					state = 6
				else:
					token += ch
					state = 2
			elif state == 6:
				# expect a hex digit
				if ch in "0123456789":
					digits = ord(ch) - ord("0")
				elif ch in "abcdef":
					digits = ord(ch) - ord("a") + 10
				elif ch in "ABCDEF":
					digits = ord(ch) - ord("A") + 10
				state = 7
			elif state == 7:
				# expect a hex digit
				if ch in "0123456789":
					digits = 16 * digits + ord(ch) - ord("0")
				elif ch in "abcdef":
					digits = 16 * digits + ord(ch) - ord("a") + 10
				elif ch in "ABCDEF":
					digits = 16 * digits + ord(ch) - ord("A") + 10
				token += chr(digits)
				state = 2

		if state == 4:
			token += "-"
			state = 0

		if state != 0:
			raise OLPError("Syntax error at %r [%d]." % (line, col))

		if len(token) > 0:
			yield token

	def options(self):
		for name, value in self._options.iteritems():
			yield (name, value)

	def options_ordered(self):
		for line_number, name, value in self._options_ordered:
			yield (line_number, name, value)


	def processes(self):
		i = 0
		for process in self._processes:
			inp, out = process[1:]
			yield (i, inp, out)
			i += 1

	def processes_ordered(self):
		i = 0
		for process in self._processes:
			line_number, inp, out = process
			yield (line_number, i, inp, out)
			i += 1

	def processing_instructions(self):
		return self._processing_instructions[:]

class OLPContractFile(OLPOrderFile):

	def __init__(self, source, extensions={
			"double_quotes": False,
			"single_quotes": False,
			"backslash_escape": False
		}):
		if isinstance(source, OLPOrderFile):
			self._options = source._options.copy()
			self._options_ordered = source._options_ordered[:]
			self._opt_res = source._opt_res.copy()
			self._opt_res_ordered = source._opt_res_ordered[:]
			self._processes = source._processes[:]
			self._processes_opt_until = source._processes_opt_until[:]
			self._proc_res = source._proc_res[:]
			self._single_quotes = source._single_quotes
			self._double_quotes = source._double_quotes
			self._backslash_escape = source._backslash_escape
		else:
			OLPOrderFile.__init__(self, source, extensions)


	def getProperty(self, name, default=None):
		if name in self._options:
			return (self._options[name])[:]
		else:
			return default

	def getPropertyResponse(self, name):
		if name in self._opt_res:
			return " ".join(self._opt_res[name])
		else:
			return None

	def getProcessResponse(self, idx):
		return self._proc_res[idx]

	def setProcessResponse(self, idx, lst):
		self._proc_res[idx] = lst
	
	def setProcessError(self, idx, msg):
		self._proc_res[idx] = msg

	def setPropertyResponse(self, name, value):
		i=0
		for l,n,_ in self.options_ordered():
			if n==name: break
			i=i+1
		if n!=self._options_ordered[i][1]:
			assert False
		line_number=self._options_ordered[i][0]
		if isinstance(value, str):
			self._opt_res[name] = value.split(" ")
			self._opt_res_ordered[i] = line_number,name, value.split(" ")
		else:
			self._opt_res[name] = value
			self._opt_res_ordered[i] = line_number,name, value

		assert isinstance(self._opt_res[name], list), \
				"self._opt_res[%r] == %r" % (name, self._opt_res[name])

	def setPropertyResponseOrdered(self, name, value, line_number):
		i=0
		for l,n,_ in self.options_ordered():
			if line_number==l and n==name:
				break
			i=i+1
		if line_number!=self._options_ordered[i][0] or n!=self._options_ordered[i][1]:
			assert False

		if isinstance(value, str):
			self._opt_res[name] = value.split(" ")
			self._opt_res_ordered[i] = line_number,name, value.split(" ")
		else:
			self._opt_res[name] = value
			self._opt_res_ordered[i] = line_number,name, value

		assert isinstance(self._opt_res[name], list), \
				"self._opt_res[%r] == %r" % (name, self._opt_res[name])




	def isPropertyOk(self, name):
		r = self.getPropertyResponse(name).lower()
		if r is None:
			return False
		else:
			return r == "ok"

	def escape(self, value):
		return value

	def _escape(self, value):
		spaced = value.translate(PROBLEM_TO_SPACE)
		needs_escape = " " in spaced

		if needs_escape:
			if self._double_quotes:
				idx = spaced.rfind(" ")
				while idx >= 0:
					ch = value[idx:idx+1]
					if ch == "\n":
						spaced = spaced[0:idx] + "\\n" + spaced[idx+1:]
					elif ch == "\r":
						spaced = spaced[0:idx] + "\\r" + spaced[idx+1:]
					elif ch == "\t":
						spaced = spaced[0:idx] + "\\t" + spaced[idx+1:]
					elif ch == "\f":
						spaced = spaced[0:idx] + "\\f" + spaced[idx+1:]
					elif ch in ["\"", "\\"]:
						spaced = spaced[0:idx] + "\\" + ch + spaced[idx+1:]
					elif ch in [" ", "#", "|", "&", "'"]:
						spaced = spaced[0:idx] + ch + spaced[idx+1:]
					else:
						XX = "\\x%02x" % ord(ch)
						spaced = spaced[0:idx] + XX + spaced[idx+1:]
					idx = spaced.rfind(" ", 0, idx)
				return "\"%s\"" % spaced
			elif self._backslash_escape:
				idx = spaced.rfind(" ")
				while idx >= 0:
					ch = value[idx:idx+1]
					spaced = spaced[0:idx] + "\\" + ch + spaced[idx+1:]
					idx = spaced.rfind(" ", 0, idx)
				return "\"%s\"" % spaced
			elif self._single_quotes:
				idx = spaced.rfind(" ")
				while idx >= 0:
					ch = value[idx:idx+1]
					if ch == "'":
						spaced = spaced[0:idx] + "''" + spaced[idx+1:]
					else:
						spaced = spaced[0:idx] + ch + spaced[idx+1:]
					idx = spaced.rfind(" ", 0, idx)
				return "\'%s\'" % spaced
			else:
				return value
		else:
			return value

	def store(self, f):
		start_pos=0
		end_pos=0
		for i, inp, out in self.processes():
			end_pos=self._processes_opt_until[i]

			for j in range(start_pos,end_pos):
				_,name, value = self._options_ordered[j]
				# response = self.getPropertyResponse(name)
				response = self._opt_res_ordered[j] if (len(self._opt_res_ordered)>j) else None
				if response is None:
					response = "OK # Option has been ignored."
				else:
					response = " ".join(response[2])
				f.write("%s %s | %s\n" % (name,
					" ".join(map(lambda s: self._escape(s), value)), response))

			try:
				response = self.getProcessResponse(i)
			except IndexError:
				golem.util.tools.error("Response Code for process has not been set properly.")
			if isinstance(response, list):
				f.write("%s -> %s | %d %s\n" % (" ".join(map(str, inp)), 
					" ".join(map(str, out)), len(response),
					" ".join(map(str, response))))
			else:
				f.write("%s -> %s | %s\n" % (" ".join(map(str, inp)), 
					" ".join(map(str, out)), response))
			start_pos=end_pos
		


class OLPError(GolemConfigError):
	pass

if __name__ == "__main__":
	import sys

	expect_contract = False

	for arg in sys.argv[1:]:
		if arg == "-c":
			expect_contract = True
			continue
		elif arg == "-o":
			expect_contrac = False
			continue

		if expect_contract:
			cf = OLPContractFile(arg)
		else:
			of = OLPOrderFile(arg)
			cf = OLPContractFile(of)

		for key, value in cf.options():
			# print("%r = %r" % (key, value))
			cf.setPropertyResponse(key, ["ok"])


class SUSYLesHouchesFile:
	"""
	This class allows to read a SUSY Les Houches accord
	parameter file.
	"""

	def __init__(self, *files):
		self.blocks = {}
		for f in files:
			if isinstance(f, file):
				self.load(f)
			else:
				the_file = open(f, "r")
				self.load(the_file)
				the_file.close()

	def load(self, f):
		block = {}
		line_number = 0

		for line in f:
			line_number += 1
			if "#" in line:
				idx = line.find("#")
				line = line[:idx]
			if line.strip() == "":
				continue

			if line[0] == "B" or line[0] == "b":
				uline = line.upper().strip()
				if uline.startswith("BLOCK "):
					name = uline[6:].strip()
					if hasattr(self, name):
						block = getattr(self, name)
					else:
						block = {}
						setattr(self, name, block)
						self.blocks[name] = block
				else:
					golem.util.tools.warning(
							"Skipping line %d and remainder of this BLOCK" %
							line_number)
					block = {}
			elif line[0] == " " or line[0] == "\t":
				tokens = []
				s = line.replace("\t", " ").strip()
				while s != "":
					values = s.split(" ", 1)
					tokens.append(values[0].strip())
					if len(values) == 2:
						s = values[1].strip()
					else:
						s = ""

				try:
					value = float(tokens.pop())
					id = tuple(map(int, tokens))
					block[id] = value
				except ValueError:
					golem.util.tools.warning(
							"Skipped line %d: illegal format" % line_number)
			else:
				golem.util.tools.warning(
						"Skipped line %d: missing value" % line_number)

	def __getitem__(self, id):
		if id in self.blocks:
			return self.blocks[id]
		else:
			return {}
