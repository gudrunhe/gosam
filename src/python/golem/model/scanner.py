# vim: ts=3:sw=3

import re

class Scanner(object):
	"""
	Implements a general purpose scanner (=tokenizer).
	"""
	def __new__(cls, *args, **opts):
		inst = object.__new__(cls)
		patterns = []
		actions = {}

		for name, func in cls.__dict__.items():
			doc = func.__doc__
			if doc is not None:
				errmsg = ("In doc-string of %s.%s: " % (cls.__name__, name)) + \
						"Invalid pattern after '@TOKEN' (%s)."

				for line in doc.splitlines():
					sline = line.strip()
					if sline.startswith("@TOKEN"):
						sline = sline[len("@TOKEN"):].strip()
						delim = sline[0:1]
						lasti = sline.rfind(delim, 1)
						if lasti < 0:
							raise SyntaxError(errmsg %
									("Missing closing delimiter '%s'" % delim))
						pattern = sline[1:lasti]
						flags = sline[lasti+1:].strip()
						iflags = 0
						for ch in flags.upper():
							if ch == 'I':
								iflags += re.IGNORECASE
							elif ch == 'L':
								iflags += re.LOCALE
							elif ch == 'S':
								iflags += re.DOTALL
							elif ch == 'U':
								iflags += re.UNICODE
							elif ch in [' ', '\t']:
								pass
							else:
								raise SyntaxError(errmsg % ("Unknown flag '%s'" % ch))

						gpattern = "(?P<%s>%s%s)" \
								% (name, flags_to_string(iflags), pattern)
						try:
							prog = re.compile(gpattern)
						except BaseException as ex:
							raise SyntaxError(errmsg % str(ex))
						if prog.match(""):
							raise SyntaxError(errmsg
									% ("%r matches the empty string" % pattern))
						patterns.append(gpattern)
						actions[name] = func

						break

		inst._REGEX   = re.compile("|".join(patterns), re.MULTILINE)
		inst._ACTIONS = actions

		return inst

	def __init__(self, *args, **opts):
		pass

	def parse(self, text):
		for match in self._REGEX.finditer(text):
			for name, image in match.groupdict().items():
				if image is None:
					continue
				token = self._ACTIONS[name].__call__(self, image)
				if token is not None:
					yield (name, token)

class TokenStream:
	def __init__(self, scanner, text):
		self._iter = scanner.parse(text)
		self._stack = []
		self._text = text

	def source(self):
		return self._text

	def name(self):
		name, token = self.top()
		return name

	def token(self):
		name, token = self.top()
		return token

	def top(self):
		if len(self._stack) == 0:
			try:
				name, token = next(self._iter)
				self._stack.append( (name, token) )
				return (name, token)
			except StopIteration:
				return ("", None)
		else:
			return self._stack[-1]

	def pop(self):
		name, token = self.top()
		if len(self._stack) > 0:
			self._stack.pop()
		return token

	def push(self, name, token):
		self._stack.append( (name, token) )

def flags_to_string(flags):
	FS = {
			re.IGNORECASE: 'i',
			re.LOCALE: 'L',
			re.MULTILINE: 'm',
			re.DOTALL: 's',
			re.UNICODE: 'u'
	}

	if flags == 0:
		return ""
	res = "(?"
	for num, ch in FS.items():
		if flags & num == num:
			res += ch
	res += ")"
	return res
