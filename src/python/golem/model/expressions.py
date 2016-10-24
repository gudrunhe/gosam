# vim: ts=3:sw=3

import golem.model.scanner
import golem.util.tools
from golem.util.tools import error
from golem.properties import zero
from golem.util.config import Property

class ExpressionParser:
	"""
	Recursive descent parser for mathematical expressions
	in 'standard' notation.
	"""

	def __init__(self, **opts):
		self._specials = opts

	def compile(self, text):
		tokens = golem.model.scanner.TokenStream(ExpressionScanner(), text)
		return self.expression(tokens)
	      
	def check_mass(self, text, masses):
	  text=text.replace("_","")
	  text=text.replace("reglog","log")
	  if text.find("if ") >0:
	    mass=text.split("if")[1].split("else")[0].strip()
	    if masses["masses"].lower().find(mass.lower())>=0:
	      #return "("+text.split("else")[1].strip()
	      text_split=text.split()
	      while text_split[text_split.index(mass) -3]!='(':
		del text_split[text_split.index(mass) -3]
	      del text_split[text_split.index(mass) -2]
	      del text_split[text_split.index(mass) -1]
	      del text_split[text_split.index(mass) +1]
	      del text_split[text_split.index(mass)]
	      return ''.join(text_split)
	    else:
	      text_split=text.split()
	      while text_split[text_split.index(mass) +3]!=')':
		del text_split[text_split.index(mass) +3]	      
	      del text_split[text_split.index(mass) +2]
	      del text_split[text_split.index(mass) -1]
	      del text_split[text_split.index(mass) +1]
	      del text_split[text_split.index(mass)]
	      return ''.join(text_split)
	      #return text.split("if")[0].strip() +")"
	  else:
	    return text

	def expression(self, tokens):
		terms = [self.product(tokens)]
		while tokens.name() == "plus_op":
			sign = tokens.pop()
			o2 = self.product(tokens)
			if sign == -1:
				o2 = UnaryMinusExpression(o2)
			terms.append(o2)
		if len(terms) > 1:
			return SumExpression(terms)
		else:
			return terms[0]

	def product(self, tokens):
		factors = []
		o1 = self.factor(tokens)
		factors.append( (1, o1) )
		while tokens.name() == "mul_op":
			sign = tokens.pop()
			o2 = self.factor(tokens)
			factors.append( (sign, o2) )

		if len(factors) == 1:
			return o1
		else:
			return ProductExpression(factors)
                    
        def log(self, tokens):
            name=tokens.name()
            term = self.product(tokens)
            if tokens.name() == "log":
                return LogExpression(term)
            else:
                return term

	def factor(self, tokens):
		name = tokens.name()
		sign = 1
		while tokens.name() == "plus_op":
			sign *= tokens.pop()
		o1 = self.simple(tokens)

		if tokens.name() == "power_op":
			tokens.pop()
			ex_sign = 1
			while tokens.name() == "plus_op":
				ex_sign *= tokens.pop()
			o2 = self.simple_power(tokens)
			if ex_sign == -1:
				o2 = UnaryMinusExpression(o2)
			o1 = PowerExpression(o1, o2)

		if sign == -1:
			o1 = UnaryMinusExpression(o1)
		return o1

	def simple(self, tokens):
		name = tokens.name()
		if name == "symbol":
			op1 = self.symbol(tokens)
			name = tokens.name()
			while name == "dot" or name == "lparen":
				if name == "dot":
					tokens.pop()
					op2 = self.symbol(tokens)
					op1 = DotExpression(op1, op2)
				elif name == "lparen":
					op2 = self.argumentlist(tokens)
					op1 = FunctionExpression(op1, op2)
				name = tokens.name()
			return op1
		elif name == "float":
			return FloatExpression(tokens.pop())
		elif name == "integer":
			# Change 27.08.13 any integer in an expression
			# that is not a power is treated as a float
			return FloatExpression(tokens.pop())
		elif name == "single_quoted":
			return StringExpression(tokens.pop())
		elif name == "lparen":
			tokens.pop()
			result = self.expression(tokens)
			if tokens.name() == "rparen":
				tokens.pop()
				return result
			elif tokens.name() != "":
				error("')' expected but %s (%r) found in '%s'." %
						(tokens.name(), tokens.token(), tokens.source()))
			else:
				error("Unexpected end of expression: ')' expected in '%s'." %
						tokens.source())
		else:
			error("%s (%r) encountered in %s." %
					(name, tokens.token(), tokens.source()))

	def simple_power(self, tokens):
		name = tokens.name()
		if name == "symbol":
			op1 = self.symbol(tokens)
			name = tokens.name()
			while name == "dot" or name == "lparen":
				if name == "dot":
					tokens.pop()
					op2 = self.symbol(tokens)
					op1 = DotExpression(op1, op2)
				elif name == "lparen":
					op2 = self.argumentlist(tokens)
					op1 = FunctionExpression(op1, op2)
				name = tokens.name()
			return op1
		elif name == "float":
			return FloatExpression(tokens.pop())
		elif name == "integer":
			return IntegerExpression(tokens.pop())
		elif name == "single_quoted":
			return StringExpression(tokens.pop())
		elif name == "lparen":
			tokens.pop()
			result = self.expression(tokens)
			if tokens.name() == "rparen":
				tokens.pop()
				return result
			elif tokens.name() != "":
				error("')' expected but %s (%r) found in '%s'." %
						(tokens.name(), tokens.token(), tokens.source()))
			else:
				error("Unexpected end of expression: ')' expected in '%s'." %
						tokens.source())
		else:
			error("%s (%r) encountered in %s." %
					(name, tokens.token(), tokens.source()))

	def simple_old(self, tokens):
		"""
		Still needed in model.feynrules
		"""
		name = tokens.name()
		if name == "symbol":
			op1 = self.symbol(tokens)
			name = tokens.name()
			while name == "dot" or name == "lparen":
				if name == "dot":
					tokens.pop()
					op2 = self.symbol(tokens)
					op1 = DotExpression(op1, op2)
				elif name == "lparen":
					op2 = self.argumentlist(tokens)
					op1 = FunctionExpression(op1, op2)
				name = tokens.name()
			return op1
		elif name == "integer":
			return IntegerExpression(tokens.pop())
		elif name == "float":
			return FloatExpression(tokens.pop())
		elif name == "single_quoted":
			return StringExpression(tokens.pop())
		elif name == "lparen":
			tokens.pop()
			result = self.expression(tokens)
			if tokens.name() == "rparen":
				tokens.pop()
				return result
			elif tokens.name() != "":
				error("')' expected but %s (%r) found in '%s'." %
						(tokens.name(), tokens.token(), tokens.source()))
			else:
				error("Unexpected end of expression: ')' expected in '%s'." %
						tokens.source())
		else:
			error("%s (%r) encountered in %s." %
					(name, tokens.token(), tokens.source()))



	def symbol(self, tokens):
		name = tokens.name()
		if name != "symbol":
			error("Symbol expected but %s found in %s" % (name, tokens.source()))

		symbol = tokens.pop()

		if symbol in self._specials:
			return self._specials[symbol]
		else:
			return SymbolExpression(symbol)

	def argumentlist(self, tokens):
		name = tokens.name()
		if name != "lparen":
			error("'(' expected but %s found in %s" % (name, tokens.source()))
		tokens.pop()
		result = []

		name = tokens.name()
		while name != "rparen":
			arg = self.expression(tokens)
			name = tokens.name()
			if name != "comma" and name != "rparen":
				error("Invalid argument list: ',' or ')' expected " +
						("but %s ('%s') found in '%s'." %
							(name, tokens.token(), tokens.source())))
			result.append(arg)

			if name == "comma":
				tokens.pop()
				name = tokens.name()
				
		tokens.pop()
		return result

class ExpressionScanner(golem.model.scanner.Scanner):
	"""
	Tokenizer for mathematical expressions. To be used together
	with ExpressionParser.
	"""
	def __init__(self):
		pass

	def skip(self, image):
		r'@TOKEN /\s+/'
		pass

	def symbol(self, image):
		r'@TOKEN /[A-Za-z_][A-Za-z0-9_]*/'
		return image

	def integer(self, image):
		r'@TOKEN /[0-9]+/'
		return int(image)

	def float(self, image):
		'@TOKEN \
/([0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)([EeDd][-+]?[0-9]+)?|[0-9]+[EeDd][-+][0-9]+/'
		return image

	def plus_op(self, image):
		'@TOKEN :\+|-:'
		if image == '+':
			return 1
		else:
			return -1

	def comma(self, image):
		'@TOKEN /,/'
		return image

	def mul_op(self, image):
		'@TOKEN :\*(?!\*)|/:'
		if image == '*':
			return 1
		else:
			return -1

	def power_op(self, image):
		r'@TOKEN :\*\*|\^:'
		return image

	def lparen(self, image):
		r'@TOKEN :\(:'
		return image

	def rparen(self, image):
		r'@TOKEN :\):'
		return image

	def dot(self, image):
		r'@TOKEN /\./'
		return image

	def single_quoted(self, image):
		r"@TOKEN /'[^\n\r']*'/"
		return image

class Expression:
	def getPrecedence(self):
		raise NotImplementedError(
				"Expression.getPrecedence() needs to be overwritten in %s."
				% self.__class__.__name__)

	def dependsOn(self, symbol):
		raise NotImplementedError(
				"Expression.dependsOn() needs to be overwritten in %s."
				% self.__class__.__name__)

	def prefixSymbolsWith(self, prefix):
		raise NotImplementedError(
				"Expression.prefixSymbolsWith() needs to be overwritten in %s."
				% self.__class__.__name__)

	def subs(self, aDict):
		raise NotImplementedError(
				"Expression.subs() needs to be overwritten in %s."
				% self.__class__.__name__)

	def algsubs(self, orig, image):
		raise NotImplementedError(
				"Expression.algsubs() needs to be overwritten in %s."
				% self.__class__.__name__)

	def powerCounting(self, powers):
		raise NotImplementedError(
				"Expression.powerCounting() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def countSymbolPowers(self):
		raise NotImplementedError(
				"Expression.countSymbolPowers() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def replaceNegativeIndices(self, lvl, pattern, found):
		raise NotImplementedError(
				"Expression.replaceNegativeIndices() " + \
				"needs to be overwritten in %s." % \
				self.__class__.__name__)

	def __int__(self):
		print type(self.__class__.__name__),self.__class__.__name__ 
		raise NotImplementedError(
				"Expression.__int__() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def replaceIntegerPowers(self, pow_fun):
		raise NotImplementedError(
				"Expression.replaceIntegerPowers() " + \
				"needs to be overwritten in %s." % \
				self.__class__.__name__)

	def replaceFloats(self, prefix, subs, counter=[0]):
		raise NotImplementedError(
				"Expression.replaceFloats() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def replaceStrings(self, prefix, subs, counter=[0]):
		raise NotImplementedError(
				"Expression.replaceStrings() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		raise NotImplementedError(
				"Expression.replaceDotProducts() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def __eq__(self, other):
		raise NotImplementedError(
				"Expression.__eq__() needs to be overwritten in %s." % \
				self.__class__.__name__)

	def __ne__(self, other):
		return not (self == other)

	def __call__(self, *args):
		if isinstance(args, tuple):
			largs = list(args)
		else:
			largs = [args]
			dir(args)
		return FunctionExpression(self, largs)

	def __mul__(self, other):
		return ProductExpression([ (1, self), (1, other)])

	def __div__(self, other):
		return ProductExpression([ (1, self), (-1, other)])

	def __pow__(self, other):
		return PowerExpression(self, other)

	def __add__(self, other):
		return SumExpression([self, other])

	def __sub__(self, other):
		return SumExpression([self, UnaryMinusExpression(other)])

	def __neg__(self):
		return UnaryMinusExpression(self)
            
        def __log__(self):
                return LogExpression(self)

class ConstantExpression(Expression):
	def getPrecedence(self):
		return 1000

	def dependsOn(self, symbol):
		return False

	def prefixSymbolsWith(self, prefix):
		return self

	def subs(self, aDict):
		return self

	def powerCounting(self, powers):
		return 0

	def replaceNegativeIndices(self, lvl, pattern, found):
		return self
	
	def countSymbolPowers(self):
		return {}

	def replaceFloats(self, prefix, subs, counter=[0]):
		return self

	def replaceIntegerPowers(self, pow_fun):
		return self

	def replaceStrings(self, prefix, subs, counter=[0]):
		return self

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return self

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		return self
	
class FloatExpression(ConstantExpression):
	def __init__(self, float):
		self._float = str(float)

	def write(self, out):
		out.write(str(self._float))

	def write_fortran(self ):
		return str(self._float) 

	def replaceFloats(self, prefix, subs, counter=[0]):
		for name, value in subs.items():
			if str(value) == str(self._float):
				return SymbolExpression(name)

		counter[0] += 1
		name = "%s%d" % (prefix, counter[0])
		subs[name] = self
		return SymbolExpression(name)

	def __eq__(self, other):
		if isinstance(other, FloatExpression):
			return self._float == other._float
		else:
			return False

	def __str__(self):
		return str(self._float)

class IntegerExpression(ConstantExpression):
	def __init__(self, integer):
		self._integer = integer

	def __int__(self):
		return self._integer

	def write(self, out):
		out.write(str(self._integer))

	def write_fortran(self):
		return str(self._integer)

	def __eq__(self, other):
		if isinstance(other, IntegerExpression):
			return self._integer == other._integer
		else:
			return False

	def replaceNegativeIndices(self, lvl, pattern, found):
		if lvl > 0 and self._integer < 0:
			idx = abs(idx)
			if idx in found:
				return found[idx]
			else:
				sidx = SymbolExpression(pattern % idx)
				found[idx] = sidx
				return sidx
		else:
			return self
	
	def __str__(self):
		return str(self._integer)
		
class SymbolExpression(Expression):
	def __init__(self, symbol):
		self._symbol = symbol

	def countSymbolPowers(self):
		return {self._symbol: 1}

	def dependsOn(self, symbol):
		return self._symbol == symbol

	def prefixSymbolsWith(self, prefix):
		return SymbolExpression(prefix + self._symbol)

	def subs(self, aDict):
		if self._symbol in aDict:
			return aDict[self._symbol]
		else:
			return self

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return self

	def getPrecedence(self):
		return 1000

	def write(self, out):
		out.write(self._symbol)

	def write_fortran(self):
		return self._symbol

	def replaceNegativeIndices(self, lvl, pattern, found):
		return self

	def powerCounting(self, powers):
		if self._symbol in powers:
			return powers[self._symbol]
		else:
			return 0
		
	def replaceFloats(self, prefix, subs, counter=[0]):
		return self

	def replaceStrings(self, prefix, subs, counter=[0]):
		return self

	def replaceIntegerPowers(self, pow_fun):
		return self

	def __str__(self):
		return self._symbol

	def __eq__(self, other):
		if isinstance(other, SymbolExpression):
			return self._symbol == other._symbol
		else:
			return False

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		return self



class FunctionExpression(Expression):
	def __init__(self, head, args):
		self._deps = {}
		self._head = head
		self._arguments = list(args)

	def getHead(self):
		return self._head

	def getArguments(self):
		return self._arguments[:]

	def powerCounting(self, powers):
		return self._head.powerCounting(powers)

	def countSymbolPowers(self):
		return self._head.countSymbolPowers()

	def getPrecedence(self):
		return 500

	def dependsOn(self, symbol):
		if symbol in self._deps:
			return self._deps[symbol]
		else:
			dep = self._head.dependsOn(symbol) or \
				any(arg.dependsOn(symbol) for arg in self._arguments)
			self._deps[symbol] = dep
			return dep

	def prefixSymbolsWith(self, prefix):
		return FunctionExpression(self._head.prefixSymbolsWith(prefix),
				map(lambda arg: arg.prefixSymbolsWith(prefix), self._arguments))

	def replaceNegativeIndices(self, lvl, pattern, found):
		return FunctionExpression(
				self._head.replaceNegativeIndices(lvl, pattern, found),
				map(lambda arg: arg.replaceNegativeIndices(lvl+1, pattern, found),
					self._arguments))
		return self


	def subs(self, aDict):
		return FunctionExpression(self._head.subs(aDict),
				map(lambda arg: arg.subs(aDict), self._arguments))

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return FunctionExpression(self._head.algsubs(orig, image),
				map(lambda arg: arg.algsubs(orig, image), self._arguments))

	def write(self, out):
		if self._head.getPrecedence() >= self.getPrecedence():
			self._head.write(out)
		else:
			out.write("(")
			self._head.write(out)
			out.write(")")
		out.write("(")
		first = True
		for arg in self._arguments:
			if first:
				first = False
			else:
				out.write(",")
			arg.write(out)
		out.write(")")


	def write_fortran(self):
		r_string=''
		if self._head.getPrecedence() >= self.getPrecedence():
			r_string += self._head.write_fortran()
		else:
			r_string += "("
			r_string += self._head.write_fortran()
			r_string += ")"

		r_string += "("
		first = True
		for arg in self._arguments:
			if first:
				first = False
			else:
				r_string += ","
			r_string += arg.write_fortran()
		r_string += ")"
		return r_string


	def __str__(self):
		return "[" + str(self._head) + "](" + \
			",".join(map(str,self._arguments)) + ")"

	def replaceIntegerPowers(self, pow_fun):
		if self._head == pow_fun:
			if len(self) == 2:
				if isinstance(self[1], IntegerExpression):
					return self[0]**self[1]
		new_head = self._head.replaceIntegerPowers(pow_fun)
		new_args = map(lambda x: x.replaceIntegerPowers(pow_fun),
			self._arguments)
		return new_head(*new_args)

	def replaceFloats(self, prefix, subs, counter=[0]):
		new_head = self._head.replaceFloats(prefix, subs, counter)
		new_args = map(lambda x: x.replaceFloats(prefix, subs, counter),
				self._arguments)
		return FunctionExpression(new_head, new_args)

	def replaceStrings(self, prefix, subs, counter=[0]):
		new_head = self._head.replaceStrings(prefix, subs, counter)
		new_args = map(lambda x: x.replaceStrings(prefix, subs, counter),
				self._arguments)
		return FunctionExpression(new_head, new_args)

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		new_head = self._head.replaceDotProducts(idx_prefixes, metric, dotproduct)
		new_args = map(lambda x:
				x.replaceDotProducts(idx_prefixes, metric, dotproduct),
				self._arguments)
		return FunctionExpression(new_head, new_args)

	def __len__(self):
		return len(self._arguments)

	def __getitem__(self, index):
		return self._arguments[index]

	def __eq__(self, other):
		if isinstance(other, FunctionExpression):
			if self._head == other._head and \
					len(self) == len(other):
				for i in range(len(self)):
					if self[i] != other[i]:
						return False
				return True
			else:
				return False
		else:
			return False
                    


class DotExpression(Expression):
	def __init__(self, first, second):
		self._deps = {}
		self._first = first
		self._second = second

	def __str__(self):
		return "(" + str(self._first) + "." + str(self._second) + ")"

	def replaceIntegerPowers(self, pow_fun):
		return DotExpression(
				self._first.replaceIntegerPowers(pow_fun),
				self._second.replaceIntegerPowers(pow_fun))
	
	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		if isinstance(self._first, SymbolExpression) or \
				isinstance(self._first, SpecialExpression):
			s1 = str(self._first)
			i1 = any(s1.startswith(prefix) for prefix in idx_prefixes)
		else:
			i1 = False

		if isinstance(self._second, SymbolExpression) or \
				isinstance(self._second, SpecialExpression):
			s2 = str(self._second)
			i2 = any(s2.startswith(prefix) for prefix in idx_prefixes)
		else:
			i2 = False

		if (i1 and i2):
			return metric(self._first, self._second)
		elif i1:
			return self._second(self._first)
		elif i2:
			return self._first(self._second)
		else:
			if dotproduct is not None:
				return dotproduct(self._first, self._second)
			else:
				return self

	def replaceNegativeIndices(self, lvl, pattern, found):
		s1 = self._first.replaceNegativeIndices(lvl, pattern, found)
		s2 = self._second.replaceNegativeIndices(lvl, pattern, found)
		return DotExpression(self._first, self._second)

	def __eq__(self, other):
		if isinstance(other, DotExpression):
			return (self._first == other._first
					and self._second == other._second) or \
				(self._first == other._second
					and self._second == other._first)
		else:
			return False

	def getFirst(self):
		return self._first

	def getSecond(self):
		return self._second

	def replaceFloats(self, prefix, subs, counter=[0]):
		new_first = self._first.replaceFloats(prefix, subs, counter)
		new_second = self._second.replaceFloats(prefix, subs, counter)
		return DotExpression(new_first, new_second)

	def replaceStrings(self, prefix, subs, counter=[0]):
		new_first = self._first.replaceStrings(prefix, subs, counter)
		new_second = self._second.replaceStrings(prefix, subs, counter)
		return DotExpression(new_first, new_second)

	def countSymbolPowers(self):
		p1 = self._first.countSymbolPowers()
		p2 = self._second.countSymbolPowers()
		return addSymbolPowers(p1, p2)

	def powerCounting(self, powers):
		return self._first.powerCounting(powers) \
				+ self._second.powerCounting(powers)

	def getPrecedence(self):
		return 500

	def dependsOn(self, symbol):
		if symbol in self._deps:
			return self._deps[symbol]
		else:
			dep = self._first.dependsOn(symbol) or \
				self._second.dependsOn(symbol)
			self._deps[symbol] = dep
			return dep

	def prefixSymbolsWith(self, prefix):
		return DotExpression(self._first.prefixSymbolsWith(prefix),
				self._second.prefixSymbolsWith(prefix))

	def subs(self, aDict):
		return DotExpression(self._first.subs(aDict), self._second.subs(aDict))

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return DotExpression(self._first.algsubs(orig, image),
					self._second.algsubs(orig, image))

	def write(self, out):

		if self._first.getPrecedence() >= self.getPrecedence():
			self._first.write(out)
		else:
			out.write("(")
			self._first.write(out)
			out.write(")")

		out.write(".")

		if self._second.getPrecedence() >= self.getPrecedence():
			self._second.write(out)
		else:
			out.write("(")
			self._second.write(out)
			out.write(")")

	def write_fortran(self):
		r_string = "dotproduct"
		if self._first.getPrecedence() >= self.getPrecedence():
			r_string += self._first.write_fortran()
		else:
			r_string += "("
			r_string += self._first.write_fortran()
			r_string += ")"

		r_string += ","

		if self._second.getPrecedence() >= self.getPrecedence():
			r_string += self._second.write_fortran()
		else:
			r_string += "("
			r_string += self._second.write_fortran()
			r_string += ")"
		return r_string


class PowerExpression(Expression):
	def __init__(self, base, exponent):
		self._base = base
		self._exponent = exponent

	def __str__(self):
		return "(" + str(self._base) + ")^(" + str(self._exponent) + ")"

	def __eq__(self, other):
		if isinstance(other, PowerExpression):
			return self._base == other._base \
					and self._exponent == other._exponent
		else:
			return False

	def getBase(self):
		return self._base

	def getExponent(self):
		return self._exponent

	def replaceIntegerPowers(self, pow_fun):
		return PowerExpression(
				self._base.replaceIntegerPowers(pow_fun),
				self._exponent.replaceIntegerPowers(pow_fun))

	def replaceFloats(self, prefix, subs, counter=[0]):
		new_base = self._base.replaceFloats(prefix, subs, counter)
		new_exponent = self._exponent.replaceFloats(prefix, subs, counter)
		return PowerExpression(new_base, new_exponent)

	def replaceNegativeIndices(self, lvl, pattern, found):
		new_base = self._base.replaceNegativeIndices(lvl, pattern, found)
		new_exponent = self._exponent.replaceNegativeIndices(lvl, pattern, found)
		return PowerExpression(new_base, new_exponent)

	def replaceStrings(self, prefix, subs, counter=[0]):
		new_base = self._base.replaceStrings(prefix, subs, counter)
		new_exponent = self._exponent.replaceStrings(prefix, subs, counter)
		return PowerExpression(new_base, new_exponent)

	def __int__(self):
		return int(self._base) ** int(self._exponent)

	def countSymbolPowers(self):
		powers = self._base.countSymbolPowers()
		try:
			factor = int(self._exponent)
		except NotImplementedError:
			return {}

		return mulSymbolPowers(powers, factor)

	def powerCounting(self, powers):
		return int(self._exponent) * self._base.powerCounting(powers)

	def dependsOn(self, symbol):
		return self._base.dependsOn(symbol) or \
				self._exponent.dependsOn(symbol)

	def prefixSymbolsWith(self, prefix):
		return PowerExpression(self._base.prefixSymbolsWith(prefix),
				self._exponent.prefixSymbolsWith(prefix))

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		return PowerExpression(
			self._base.replaceDotProducts(idx_prefixes, metric, dotproduct),
			self._exponent.replaceDotProducts(idx_prefixes, metric, dotproduct))

	def subs(self, aDict):
		return PowerExpression(self._base.subs(aDict), self._exponent.subs(aDict))

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return PowerExpression(
					self._base.algsubs(orig, image),
					self._exponent.algsubs(orig, image))

	def getPrecedence(self):
		return 400

	def write(self, out):

		if self._base.getPrecedence() >= self.getPrecedence():
			self._base.write(out)
		else:
			out.write("(")
			self._base.write(out)
			out.write(")")

		out.write("^")

		if self._exponent.getPrecedence() >= self.getPrecedence():
			self._exponent.write(out)
		else:
			out.write("(")
			self._exponent.write(out)
			out.write(")")

	def write_fortran(self):
		r_string = ''
		if self._base.getPrecedence() >= self.getPrecedence():
			r_string += self._base.write_fortran()
		else:
			r_string += "("
			r_string += self._base.write_fortran()
			r_string += ")"

		r_string += "**"

		if self._exponent.getPrecedence() >= self.getPrecedence():
			r_string += self._exponent.write_fortran()
		else:
			r_string += "("
			r_string += self._exponent.write_fortran()
			r_string += ")"
		return r_string



class ProductExpression(Expression):
    
        logexpression = False
    
	def __init__(self, factors):
		self._factors = factors[:]

	def __eq__(self, other):
		if isinstance(other, ProductExpression):
			if len(self) == len(other):
				for i in range(len(self)):
					s1, f1 = self[i]
					s2, f2 = other[i]
					if not (s1 == s2 and f1 == f2):
						return False
				return True
			else:
				return False
		else:
			return False

	def __len__(self):
		return len(self._factors)

	def __getitem__(self, index):
		return self._factors[index]

	def getFactors(self):
		return self._factors[:]

	def countSymbolPowers(self):
		result = {}
		for sig, factor in self._factors:
			p = factor.countSymbolPowers()
			if p == -1:
				p = mulSymbolPowers(p, -1)
			result = addSymbolPowers(p, result)
		return result

	def replaceFloats(self, prefix, subs, counter=[0]):
		result = []
		for sig, factor in self._factors:
			p = factor.replaceFloats(prefix, subs, counter)
			result.append( (sig, p) )
		return ProductExpression(result)

	def replaceIntegerPowers(self, pow_fun):
		result = []
		for sig, factor in self._factors:
			p = factor.replaceIntegerPowers(pow_fun)
			result.append( (sig, p) )
		return ProductExpression(result)

	def replaceStrings(self, prefix, subs, counter=[0]):
		result = []
		for sig, factor in self._factors:
			p = factor.replaceStrings(prefix, subs, counter)
			result.append( (sig, p) )
		return ProductExpression(result)

	def replaceNegativeIndices(self, lvl, pattern, found):
		result = []
		for sig, factor in self._factors:
			p = factor.replaceNegativeIndices(lvl, pattern, found)
			result.append( (sig, p) )
		return ProductExpression(result)

	def powerCounting(self, powers):
		return sum([sig * term.powerCounting(powers)
			for sig, term in self._factors])

	def __int__(self):
		num = 1
		den = 1
		for sig, factor in self._factors:
			if sig == 1:
				num *= int(factor)
			else:
				den *= int(factor)
		return num / den

	def dependsOn(self, symbol):
		return any(factor.dependsOn(symbol) for sign, factor in self._factors)

	def prefixSymbolsWith(self, prefix):
		new_factors = []
		for sign, factor in self._factors:
			new_factors.append( (sign, factor.prefixSymbolsWith(prefix)) )
		return ProductExpression(new_factors)

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		new_factors = []
		for sign, factor in self._factors:
			new_factors.append( (sign,
				factor.replaceDotProducts(idx_prefixes, metric, dotproduct)) )
		return ProductExpression(new_factors)

	def subs(self, aDict):
		new_factors = []
		for sign, factor in self._factors:
			new_factors.append( (sign, factor.subs(aDict)) )
		return ProductExpression(new_factors)

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			new_factors = []
			for sign, factor in self._factors:
				new_factors.append( (sign, factor.algsubs(orig, image)) )
			return ProductExpression(new_factors)

	def __str__(self):
		return "*".join(
				["(" + str(term) + ")^" + str(sig) for sig, term in self._factors])

	def write(self, out):
		first_sig, first_term = self._factors[0]

			
                if str(self._factors[0][1])=="log":
                    first_term.write(out)
                    out.write("(")
                    second_sig, second_term = self._factors[1]
                    if second_term.getPrecedence() > self.getPrecedence():
                            second_term.write(out)
                    else:
                            out.write("(")
                            second_term.write(out)
                            out.write(")")                                        
                    follow = self._factors[2:]
                    for sig, term in follow:
                            if sig == 1:
                                    out.write("*")
                            else:
                                    out.write("/")
                            if term.getPrecedence() > self.getPrecedence():
                                    term.write(out)
                            else:
                                    out.write("(")
                                    term.write(out)
                                    out.write(")")                    
                    out.write(")")
                    
                else:
                    follow = self._factors[1:]
                    if first_sig == -1:
                            out.write("1/")
                    if first_term.getPrecedence() >= self.getPrecedence():
                            first_term.write(out)
                    else:
                            out.write("(")
                            first_term.write(out)
                            out.write(")")                    

                    for sig, term in follow:
                            if sig == 1:
                                    out.write("*")
                            else:
                                    out.write("/")
                            if term.getPrecedence() > self.getPrecedence():
                                    term.write(out)
                            else:
                                    out.write("(")
                                    term.write(out)
                                    out.write(")")

	def write_fortran(self):
		first_sig, first_term = self._factors[0]
		follow = self._factors[1:]
		r_string = ""
		if first_sig == -1:
			r_string += "1.0_ki/"
		if first_term.getPrecedence() >= self.getPrecedence():
			r_string += first_term.write_fortran()
		else:
			r_string += "("
			r_string += first_term.write_fortran()
			r_string += ")"
		
		for sig, term in follow:
			if sig == 1:
				r_string += "*"
			else:
				r_string += "/"
			if term.getPrecedence() > self.getPrecedence():
				r_string += term.write_fortran()
			else:
				r_string += "("
				r_string += term.write_fortran()
				r_string += ")"
		return r_string

	def getPrecedence(self):
		return 200

class SumExpression(Expression):
	def __init__(self, terms):
		self._deps = {}
		self._terms = list(terms)

	def __eq__(self, other):
		if isinstance(other, SumExpression):
			if len(self) == len(other):
				iterms = set(range(len(other)))
				for i in range(len(self)):
					t1 = self[i]
					found = -1
					for j in iterms:
						t2 = other[j]
						if t1 == t2:
							found = j
							break
					if found >= 0:
						iterms.remove(found)
					else:
						return False
				return True
			else:
				return False
		else:
			return False

	def __len__(self):
		return len(self._terms)

	def __getitem__(self, index):
		return self._terms[index]

	def getTerms(self):
		return self._terms[:]

	def replaceFloats(self, prefix, subs, counter=[0]):
		result = []
		for term in self._terms:
			p = term.replaceFloats(prefix, subs, counter)
			result.append(p)
		return SumExpression(result)

	def replaceIntegerPowers(self, pow_fun):
		result = []
		for term in self._terms:
			p = term.replaceIntegerPowers(pow_fun)
			result.append(p)
		return SumExpression(result)

	def replaceStrings(self, prefix, subs, counter=[0]):
		result = []
		for term in self._terms:
			p = term.replaceStrings(prefix, subs, counter)
			result.append(p)
		return SumExpression(result)

	def replaceNegativeIndices(self, lvl, pattern, found):
		result = []
		for term in self._terms:
			p = term.replaceNegativeIndices(lvl, pattern, found)
			result.append(p)
		return SumExpression(result)

	def countSymbolPowers(self):
		all_p = []
		name = set([])
		for term in self._terms:
			p = term.countSymbolPowers()
			all_p.append(p)
			names.update(p.keys())

		result = {}
		for name in names:
			if any(name not in p for p in all_p):
				continue
			pow = [p[name] for p in all_p]
			maxp = max(pow)
			minp = min(pow)
			if minp == maxp:
				result[name] = minp
		return result

	def __int__(self):
		return sum(map(int, self._terms))

	def dependsOn(self, symbol):
		if symbol in self._deps:
			return self._deps[symbol]
		else:
			dep = any(term.dependsOn(symbol) for term in self._terms)
			self._deps[symbol] = dep
			return dep

	def prefixSymbolsWith(self, prefix):
		return SumExpression( map(lambda term: term.prefixSymbolsWith(prefix),
			self._terms))

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		return SumExpression( map(lambda term:
			term.replaceDotProducts(idx_prefixes, metric, dotproduct),
			self._terms))

	def subs(self, aDict):
		return SumExpression( map(lambda term: term.subs(aDict), self._terms))

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return SumExpression(
					map(lambda term: term.algsubs(orig, image), self._terms))

	def write(self, out):
		first = self._terms[0]
		follow = self._terms[1:]
		if first.getPrecedence() >= self.getPrecedence():
			first.write(out)
		else:
			out.write("(")
			first.write(out)
			out.write(")")

		for term in follow:
			if isinstance(term, UnaryMinusExpression):
				term.write(out)
			else:
				out.write("+")
				if term.getPrecedence() >= self.getPrecedence():
					term.write(out)
				else:
					out.write("(")
					term.write(out)
					out.write(")")


	def write_fortran(self):
		r_string = ""
		first = self._terms[0]
		follow = self._terms[1:]
		if first.getPrecedence() >= self.getPrecedence():
			r_string += first.write_fortran()
		else:
			r_string +="("
			r_string +=first.write_fortran(out)
			r_string +=")"

		for term in follow:
			if isinstance(term, UnaryMinusExpression):
				r_string +=term.write_fortran()
			else:
				r_string +="+"
				if term.getPrecedence() >= self.getPrecedence():
					r_string +=term.write_fortran()
				else:
					r_string +="("
					r_string +=term.write_fortran()
					r_string +=")"
		return r_string

	def getPrecedence(self):
		return 100

	def __str__(self):
		return "+".join(map(str,self._terms))

class UnaryMinusExpression(Expression):
	def __init__(self, term):
		self._deps = {}
		self._term = term

	def __str__(self):
		return "-(" + str(self._term) + ")"

	def __eq__(self, other):
		if isinstance(other, UnaryMinusExpression):
			return self._term == other._term
		else:
			return False

	def getTerm(self):
		return self._term

	def replaceFloats(self, prefix, subs, counter=[0]):
		p = self._term.replaceFloats(prefix, subs, counter)
		return UnaryMinusExpression(p)

	def replaceIntegerPowers(self, pow_fun):
		p = self._term.replaceIntegerPowers(pow_fun)
		return UnaryMinusExpression(p)

	def replaceStrings(self, prefix, subs, counter=[0]):
		p = self._term.replaceStrings(prefix, subs, counter)
		return UnaryMinusExpression(p)

	def countSymbolPowers(self):
		return self._term.countSymbolPowers()

	def powerCounting(self, powers):
		return self._term.powerCounting(powers)

	def __int__(self):
		return - int(self._term)

	def dependsOn(self, symbol):
		if symbol in self._deps:
			return self._deps[symbol]
		else:
			dep = self._term.dependsOn(symbol)
			self._deps[symbol] = dep
			return dep

	def prefixSymbolsWith(self, prefix):
		return UnaryMinusExpression(self._term.prefixSymbolsWith(prefix))

	def replaceDotProducts(self, idx_prefixes, metric, dotproduct=None):
		return UnaryMinusExpression(
			self._term.replaceDotProducts(idx_prefixes, metric, dotproduct))

	def replaceNegativeIndices(self, lvl, pattern, found):
		if isinstance(self._term, IntegerExpression) and lvl > 0:
			idx = int(self._term)
			if idx > 0:
				if idx in found:
					return found[idx]
				else:
					sidx = SymbolExpression(pattern % idx)
					found[idx] = sidx
					return sidx
			else:
				return self
		else:
			return UnaryMinusExpression(
				self._term.replaceNegativeIndices(lvl, pattern, found))

	def subs(self, aDict):
		return UnaryMinusExpression(self._term.subs(aDict))

	def algsubs(self, orig, image):
		if self == orig:
			return image
		else:
			return UnaryMinusExpression(self._term.algsubs(orig, image))

	def write(self, out):
		out.write("-")
		if self._term.getPrecedence() >= self.getPrecedence():
			self._term.write(out)
		else:
			out.write("(")
			self._term.write(out)
			out.write(")")


	def write_fortran(self):
		r_string = ""
		r_string += "-"
		if self._term.getPrecedence() >= self.getPrecedence():
			r_string += self._term.write_fortran()
		else:
			r_string += "("
			r_string += self._term.write_fortran()
			r_string += ")"
		return r_string

	def getPrecedence(self):
		return 100


class SpecialExpression(ConstantExpression):
	def __init__(self, image):
		self._image = image

	def __eq__(self, other):
		if isinstance(other, SpecialExpression):
			return self._image == other._image
		else:
			return False

	def write(self, out):
		out.write(self._image)

	def write_fortran(self):
		return self._image

	def __str__(self):
		return self._image

	def replaceFloats(self, prefix, subs, counter=[0]):
		return self

	def replaceStrings(self, prefix, subs, counter=[0]):
		return self

class StringExpression(ConstantExpression):
	def __init__(self, image):
		self._image = image

	def __eq__(self, other):
		if isinstance(other, SpecialExpression):
			return self._image == other._image
		else:
			return False

	def write(self, out):
		out.write("'" + self._image + "'")

	def write_fortran(self):
		return "'" + self._image + "'"


	def __str__(self):
		return "'" + self._image + "'"

	def replaceStrings(self, prefix, subs, counter=[0]):
		if self._image in subs:
			return subs[self._image]

		counter[0] += 1
		name = "%s%d" % (prefix, counter[0])
		expr = SymbolExpression(name)
		subs[self._image] = expr
		return expr

def addSymbolPowers(p1, p2):
	names = set(p1.keys() + p2.keys())
	result = {}
	for name in names:
		p = 0
		if name in p1:
			p += p1[name]
		if name in p2:
			p += p2[name]
		result[name] = p
	return result

def mulSymbolPowers(p1, factor):
	result = {}
	for name, p in p1.items():
		result[name] = factor * p
	return result

def resolve_dependencies(functions):
	"""
	Bring a list of expressions into an order in which they
	can be computed
	"""
	all_names = functions.keys()
	nfunctions = len(all_names)
	graph = {}
	golem.util.tools.message("      * Building call graph")
	i = 0
	for name, expr in functions.items():
		i += 1
		if i % 100 == 0:
			golem.util.tools.message("         (%5d/%5d)" % (i, nfunctions))
		edges = []
		for other in all_names:
			if name == other:
				continue

			if expr.dependsOn(other):
				edges.append(other)
		graph[name] = edges

	golem.util.tools.message("      * Traversing call graph")
	nedges = len(graph)
	golem.util.tools.message("         %5d edges left" % nedges)

	program = []
	while len(graph) > 0:
		found = None
		for name, edges in graph.items():
			if len(edges) == 0:
				found = name
				break
		if found is None:
			# Before we generate an error message we minimize the set of problematic
			# functions. In order to do so we drop all functions on which no other
			# function depends.
			flag = True
			while flag:
				flag = False
				bottom_expression = None
				for name in graph.keys():
					bottom = True
					for edges in graph.values():
						if name in edges:
							bottom = False
							break
					if bottom:
						bottom_expression = name
						break
				if bottom_expression is not None:
					flag = True
					del graph[bottom_expression]

			problem_set = ", ".join(graph.keys())

			golem.util.tools.error(
					"Cannot resolve dependencies between functions: %s." %
					problem_set)

		program.append(name)
		del graph[name]
		nedges -= 1
		if nedges % 100 == 0:
			golem.util.tools.message("         %5d edges left" % nedges)

		for edges in graph.values():
			if name in edges:
				edges.remove(name)

	return program
