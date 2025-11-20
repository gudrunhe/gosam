# vim: ts=3:sw=3
from __future__ import annotations

import logging
import sys
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from typing import (
    TextIO,
    cast,
    final,
    override,
)

from golem.model.scanner import Scanner, TokenStream

logger = logging.getLogger(__name__)


@final
class ExpressionParser:
    """
    Recursive descent parser for mathematical expressions
    in 'standard' notation.
    """

    def __init__(self, **opts: Expression):
        self._specials = opts

    def compile(self, text: str) -> Expression:
        tokens = TokenStream(ExpressionScanner(), text)
        return self.expression(tokens)

    def expression(self, tokens: TokenStream) -> Expression:
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

    def product(self, tokens: TokenStream) -> Expression:
        factors: list[tuple[int, Expression]] = []
        o1 = self.factor(tokens)
        factors.append((1, o1))
        while tokens.name() == "mul_op":
            sign = cast(int, tokens.pop())
            o2 = self.factor(tokens)
            factors.append((sign, o2))

        if len(factors) == 1:
            return o1
        else:
            return ProductExpression(factors)

    def factor(self, tokens: TokenStream) -> Expression:
        _ = tokens.name()
        sign = 1
        while tokens.name() == "plus_op":
            sign *= cast(int, tokens.pop())
        o1 = self.simple(tokens)

        if tokens.name() == "power_op":
            _ = tokens.pop()
            ex_sign = 1
            while tokens.name() == "plus_op":
                ex_sign *= cast(int, tokens.pop())
            o2 = self.simple_power(tokens)
            if ex_sign == -1:
                o2 = UnaryMinusExpression(o2)
            o1 = PowerExpression(o1, o2)

        if sign == -1:
            o1 = UnaryMinusExpression(o1)
        return o1

    def simple(self, tokens: TokenStream) -> Expression:
        name = tokens.name()
        if name == "symbol":
            op1 = self.symbol(tokens)
            name = tokens.name()
            while name == "dot" or name == "lparen":
                if name == "dot":
                    _ = tokens.pop()
                    op2 = self.symbol(tokens)
                    op1 = DotExpression(op1, op2)
                elif name == "lparen":
                    op2 = self.argumentlist(tokens)
                    op1 = FunctionExpression(op1, op2)
                name = tokens.name()
            return op1
        elif name == "float":
            return FloatExpression(cast(float, tokens.pop()))
        elif name == "integer":
            # Change 27.08.13 any integer in an expression
            # that is not a power is treated as a float
            return FloatExpression(cast(float, tokens.pop()))
        elif name == "single_quoted":
            return StringExpression(cast(str, tokens.pop()))
        elif name == "lparen":
            _ = tokens.pop()
            result = self.expression(tokens)
            if tokens.name() == "rparen":
                _ = tokens.pop()
                return result
            elif tokens.name() != "":
                logger.critical(
                    "')' expected but %s (%r) found in '%s'."
                    % (tokens.name(), tokens.token(), tokens.source())
                )
                sys.exit("GoSam terminated due to an error")
            else:
                logger.critical(
                    "Unexpected end of expression: ')' expected in '%s'."
                    % tokens.source()
                )
                sys.exit("GoSam terminated due to an error")
        else:
            logger.critical(
                "%s (%r) encountered in %s." % (name, tokens.token(), tokens.source())
            )
            sys.exit("GoSam terminated due to an error")

    def simple_power(self, tokens: TokenStream) -> Expression:
        name = tokens.name()
        if name == "symbol":
            op1 = self.symbol(tokens)
            name = tokens.name()
            while name == "dot" or name == "lparen":
                if name == "dot":
                    _ = tokens.pop()
                    op2 = self.symbol(tokens)
                    op1 = DotExpression(op1, op2)
                elif name == "lparen":
                    op2 = self.argumentlist(tokens)
                    op1 = FunctionExpression(op1, op2)
                name = tokens.name()
            return op1
        elif name == "float":
            return FloatExpression(cast(float, tokens.pop()))
        elif name == "integer":
            return IntegerExpression(cast(int, tokens.pop()))
        elif name == "single_quoted":
            return StringExpression(cast(str, tokens.pop()))
        elif name == "lparen":
            _ = tokens.pop()
            result = self.expression(tokens)
            if tokens.name() == "rparen":
                _ = tokens.pop()
                return result
            elif tokens.name() != "":
                logger.critical(
                    "')' expected but %s (%r) found in '%s'."
                    % (tokens.name(), tokens.token(), tokens.source())
                )
                sys.exit("GoSam terminated due to an error")
            else:
                logger.critical(
                    "Unexpected end of expression: ')' expected in '%s'."
                    % tokens.source()
                )
                sys.exit("GoSam terminated due to an error")
        else:
            logger.critical(
                "%s (%r) encountered in %s." % (name, tokens.token(), tokens.source())
            )
            sys.exit("GoSam terminated due to an error")

    def simple_old(self, tokens: TokenStream) -> Expression:
        """
        Still needed in model.feynrules
        """
        name = tokens.name()
        if name == "symbol":
            op1 = self.symbol(tokens)
            name = tokens.name()
            while name == "dot" or name == "lparen":
                if name == "dot":
                    _ = tokens.pop()
                    op2 = self.symbol(tokens)
                    op1 = DotExpression(op1, op2)
                elif name == "lparen":
                    op2 = self.argumentlist(tokens)
                    op1 = FunctionExpression(op1, op2)
                name = tokens.name()
            return op1
        elif name == "integer":
            return IntegerExpression(cast(int, tokens.pop()))
        elif name == "float":
            return FloatExpression(cast(float, tokens.pop()))
        elif name == "single_quoted":
            return StringExpression(cast(str, tokens.pop()))
        elif name == "lparen":
            _ = tokens.pop()
            result = self.expression(tokens)
            if tokens.name() == "rparen":
                _ = tokens.pop()
                return result
            elif tokens.name() != "":
                logger.critical(
                    "')' expected but %s (%r) found in '%s'."
                    % (tokens.name(), tokens.token(), tokens.source())
                )
                sys.exit("GoSam terminated due to an error")
            else:
                logger.critical(
                    "Unexpected end of expression: ')' expected in '%s'."
                    % tokens.source()
                )
                sys.exit("GoSam terminated due to an error")
        else:
            logger.critical(
                "%s (%r) encountered in %s." % (name, tokens.token(), tokens.source())
            )
            sys.exit("GoSam terminated due to an error")

    def symbol(self, tokens: TokenStream) -> Expression:
        name = tokens.name()
        if name != "symbol":
            logger.critical(
                "Symbol expected but %s found in %s" % (name, tokens.source())
            )
            sys.exit("GoSam terminated due to an error")

        symbol = cast(str, tokens.pop())

        if symbol in self._specials:
            return self._specials[symbol]
        else:
            return SymbolExpression(symbol)

    def argumentlist(self, tokens: TokenStream):
        name = tokens.name()
        if name != "lparen":
            logger.critical("'(' expected but %s found in %s" % (name, tokens.source()))
            sys.exit("GoSam terminated due to an error")
        _ = tokens.pop()
        result: list[Expression] = []

        name = tokens.name()
        while name != "rparen":
            arg = self.expression(tokens)
            name = tokens.name()
            if name != "comma" and name != "rparen":
                logger.critical(
                    "Invalid argument list: ',' or ')' expected "
                    + (
                        "but %s ('%s') found in '%s'."
                        % (name, tokens.token(), tokens.source())
                    )
                )
                sys.exit("GoSam terminated due to an error")
            result.append(arg)

            if name == "comma":
                _ = tokens.pop()
                name = tokens.name()

        _ = tokens.pop()
        return result


class ExpressionScanner(Scanner):
    """
    Tokenizer for mathematical expressions. To be used together
    with ExpressionParser.
    """

    def __init__(self):
        super().__init__()
        pass

    def skip(self, image: str):
        r"@TOKEN /\s+/"
        pass

    def symbol(self, image: str) -> str:
        r"@TOKEN /[A-Za-z_][A-Za-z0-9_]*/"
        return image

    def float(self, image: str) -> str:
        "@TOKEN \
/([0-9]*\\.[0-9]+|[0-9]+\\.[0-9]*)([EeDd][-+]?[0-9]+)?|[0-9]+[EeDd][-+][0-9]+/"
        return image

    def integer(self, image: str) -> int:
        r"@TOKEN /[0-9]+(?![.0-9])/"
        return int(image)

    def plus_op(self, image: str) -> int:
        r"@TOKEN :\+|-:"
        if image == "+":
            return 1
        else:
            return -1

    def comma(self, image: str) -> str:
        "@TOKEN /,/"
        return image

    def mul_op(self, image: str) -> int:
        r"@TOKEN :\*(?!\*)|/:"
        if image == "*":
            return 1
        else:
            return -1

    def power_op(self, image: str) -> str:
        r"@TOKEN :\*\*|\^:"
        return image

    def lparen(self, image: str) -> str:
        r"@TOKEN :\(:"
        return image

    def rparen(self, image: str) -> str:
        r"@TOKEN :\):"
        return image

    def dot(self, image: str) -> str:
        r"@TOKEN /\./"
        return image

    def single_quoted(self, image: str) -> str:
        r"@TOKEN /'[^\n\r']*'/"
        return image


class Expression:
    def getPrecedence(self) -> int:
        raise NotImplementedError(
            "Expression.getPrecedence() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def dependsOn(self, _symbol: str) -> bool:
        raise NotImplementedError(
            "Expression.dependsOn() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def prefixSymbolsWith(self, _prefix: str) -> Expression:
        raise NotImplementedError(
            "Expression.prefixSymbolsWith() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def subs(self, _aDict: Mapping[str, Expression]) -> Expression:
        raise NotImplementedError(
            "Expression.subs() needs to be overwritten in %s." % self.__class__.__name__
        )

    def algsubs(self, _orig: Expression, _image: Expression) -> Expression:
        raise NotImplementedError(
            "Expression.algsubs() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def powerCounting(self, _powers: MutableMapping[str, int]) -> int:
        raise NotImplementedError(
            "Expression.powerCounting() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def countSymbolPowers(self) -> Mapping[str, int]:
        raise NotImplementedError(
            "Expression.countSymbolPowers() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def replaceNegativeIndices(
        self, _lvl: int, _pattern: str, _found: MutableMapping[int, Expression]
    ) -> Expression:
        raise NotImplementedError(
            "Expression.replaceNegativeIndices() "
            + "needs to be overwritten in %s." % self.__class__.__name__
        )

    def __int__(self) -> int:
        print(type(self.__class__.__name__), self.__class__.__name__)
        raise NotImplementedError(
            "Expression.__int__() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def replaceIntegerPowers(self, _pow_fun: Expression) -> Expression:
        raise NotImplementedError(
            "Expression.replaceIntegerPowers() "
            + "needs to be overwritten in %s." % self.__class__.__name__
        )

    def replaceFloats(
        self,
        _prefix: str,
        _subs: MutableMapping[str, Expression],
        _counter: list[int] = [0],
    ) -> Expression:
        raise NotImplementedError(
            "Expression.replaceFloats() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def replaceStrings(
        self,
        _prefix: str,
        _subs: MutableMapping[str, Expression],
        _counter: list[int] = [0],
    ) -> Expression:
        raise NotImplementedError(
            "Expression.replaceStrings() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def replaceDotProducts(
        self,
        _idx_prefixes: Sequence[str],
        _metric: Callable[[Expression, Expression], Expression],
        _dotproduct: None | Callable[[Expression, Expression], Expression] = None,
    ) -> Expression:
        raise NotImplementedError(
            "Expression.replaceDotProducts() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def write(self, _out: TextIO) -> None:
        raise NotImplementedError(
            "Expression.write() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    def write_fortran(self) -> str:
        raise NotImplementedError(
            "Expression.write_fortran() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    @override
    def __eq__(self, _other: object) -> bool:
        raise NotImplementedError(
            "Expression.__eq__() needs to be overwritten in %s."
            % self.__class__.__name__
        )

    @override
    def __ne__(self, other: object):
        return not (self == other)

    def __call__(self, *args: Expression) -> Expression:
        largs = list(args)
        return FunctionExpression(self, largs)

    def __mul__(self, other: Expression) -> Expression:
        return ProductExpression([(1, self), (1, other)])

    def __div__(self, other: Expression) -> Expression:
        return ProductExpression([(1, self), (-1, other)])

    def __pow__(self, other: Expression) -> Expression:
        return PowerExpression(self, other)

    def __add__(self, other: Expression) -> Expression:
        return SumExpression([self, other])

    def __sub__(self, other: Expression) -> Expression:
        return SumExpression([self, UnaryMinusExpression(other)])

    def __neg__(self):
        return UnaryMinusExpression(self)


class ConstantExpression(Expression):
    @override
    def getPrecedence(self):
        return 1000

    @override
    def dependsOn(self, _symbol: str):
        return False

    @override
    def prefixSymbolsWith(self, _prefix: str):
        return self

    @override
    def subs(self, _aDict: Mapping[str, Expression]):
        return self

    @override
    def powerCounting(self, _powers: MutableMapping[str, int]):
        return 0

    @override
    def replaceNegativeIndices(
        self, _lvl: int, _pattern: str, _found: MutableMapping[int, Expression]
    ) -> Expression:
        return self

    @override
    def countSymbolPowers(self) -> dict[str, int]:
        return {}

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self

    @override
    def replaceIntegerPowers(self, pow_fun: Expression) -> Expression:
        return self

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self

    @override
    def algsubs(self, orig: Expression, image: Expression) -> Expression:
        if self == orig:
            return image
        else:
            return self

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: None | Callable[[Expression, Expression], Expression] = None,
    ):
        return self


@final
class FloatExpression(ConstantExpression):
    def __init__(self, float: float):
        self._float = str(float)

    @override
    def write(self, out: TextIO):
        _ = out.write(str(self._float))

    @override
    def write_fortran(self):
        return str(self._float)

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        for name, value in subs.items():
            if str(value) == str(self._float):
                return SymbolExpression(name)

        counter[0] += 1
        name = "%s%d" % (prefix, counter[0])
        subs[name] = self
        return SymbolExpression(name)

    @override
    def __eq__(self, other: object):
        if isinstance(other, FloatExpression):
            return self._float == other._float
        else:
            return False

    @override
    def __str__(self):
        return str(self._float)


@final
class IntegerExpression(ConstantExpression):
    def __init__(self, integer: int):
        self._integer = integer

    @override
    def __int__(self):
        return self._integer

    @override
    def write(self, out: TextIO):
        _ = out.write(str(self._integer))

    @override
    def write_fortran(self):
        return str(self._integer)

    @override
    def __eq__(self, other: object):
        if isinstance(other, IntegerExpression):
            return self._integer == other._integer
        else:
            return False

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ) -> Expression:
        if lvl > 0 and self._integer < 0:
            idx = abs(self._integer)
            if idx in found:
                return found[idx]
            else:
                sidx = SymbolExpression(pattern % idx)
                found[idx] = sidx
                return sidx
        else:
            return self

    @override
    def __str__(self):
        return str(self._integer)


@final
class SymbolExpression(Expression):
    def __init__(self, symbol: str):
        self._symbol = symbol

    @override
    def countSymbolPowers(self):
        return {self._symbol: 1}

    @override
    def dependsOn(self, symbol: str) -> bool:
        return self._symbol == symbol

    @override
    def prefixSymbolsWith(self, prefix: str):
        return SymbolExpression(prefix + self._symbol)

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        if self._symbol in aDict:
            return aDict[self._symbol]
        else:
            return self

    @override
    def algsubs(self, orig: Expression, image: Expression) -> Expression:
        if self == orig:
            return image
        else:
            return self

    @override
    def getPrecedence(self) -> int:
        return 1000

    @override
    def write(self, out: TextIO):
        _ = out.write(self._symbol)

    @override
    def write_fortran(self):
        return self._symbol

    @override
    def replaceNegativeIndices(
        self, _lvl: int, pattern: str, found: Mapping[int, Expression]
    ):
        return self

    @override
    def powerCounting(self, powers: MutableMapping[str, int]) -> int:
        if self._symbol in powers:
            return powers[self._symbol]
        else:
            return 0

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self

    @override
    def replaceIntegerPowers(self, pow_fun: Expression) -> Expression:
        return self

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self

    @override
    def __str__(self):
        return self._symbol

    @override
    def __eq__(self, other: object):
        if isinstance(other, SymbolExpression):
            return self._symbol == other._symbol
        else:
            return False

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: None | Callable[[Expression, Expression], Expression] = None,
    ):
        return self


@final
class FunctionExpression(Expression):
    def __init__(self, head: Expression, args: Sequence[Expression]):
        self._deps: dict[str, bool] = {}
        self._head = head
        self._arguments = list(args)

    def getHead(self):
        return self._head

    def getArguments(self):
        return self._arguments[:]

    @override
    def powerCounting(self, powers: MutableMapping[str, int]):
        return self._head.powerCounting(powers)

    @override
    def countSymbolPowers(self):
        return self._head.countSymbolPowers()

    @override
    def getPrecedence(self):
        return 500

    @override
    def dependsOn(self, symbol: str) -> bool:
        if symbol in self._deps:
            return self._deps[symbol]
        else:
            dep = self._head.dependsOn(symbol) or any(
                arg.dependsOn(symbol) for arg in self._arguments
            )
            self._deps[symbol] = dep
            return dep

    @override
    def prefixSymbolsWith(self, prefix: str):
        return FunctionExpression(
            self._head.prefixSymbolsWith(prefix),
            [arg.prefixSymbolsWith(prefix) for arg in self._arguments],
        )

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ):
        return FunctionExpression(
            self._head.replaceNegativeIndices(lvl, pattern, found),
            [
                arg.replaceNegativeIndices(lvl + 1, pattern, found)
                for arg in self._arguments
            ],
        )

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        return FunctionExpression(
            self._head.subs(aDict), [arg.subs(aDict) for arg in self._arguments]
        )

    @override
    def algsubs(self, orig: Expression, image: Expression):
        if self == orig:
            return image
        else:
            return FunctionExpression(
                self._head.algsubs(orig, image),
                [arg.algsubs(orig, image) for arg in self._arguments],
            )

    @override
    def write(self, out: TextIO):
        if self._head.getPrecedence() >= self.getPrecedence():
            self._head.write(out)
        else:
            _ = out.write("(")
            self._head.write(out)
            _ = out.write(")")

        _ = out.write("(")
        first = True
        for arg in self._arguments:
            if first:
                first = False
            else:
                _ = out.write(",")
            arg.write(out)
        _ = out.write(")")

    @override
    def write_fortran(self) -> str:
        r_string = ""
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

    @override
    def __str__(self):
        return "[" + str(self._head) + "](" + ",".join(map(str, self._arguments)) + ")"

    @override
    def replaceIntegerPowers(self, pow_fun: Expression) -> Expression:
        if self._head == pow_fun:
            if len(self) == 2:
                if isinstance(self[1], IntegerExpression):
                    return self[0] ** self[1]
        new_head = self._head.replaceIntegerPowers(pow_fun)
        new_args = [x.replaceIntegerPowers(pow_fun) for x in self._arguments]
        return new_head(*new_args)

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_head = self._head.replaceFloats(prefix, subs, counter)
        new_args = [x.replaceFloats(prefix, subs, counter) for x in self._arguments]
        return FunctionExpression(new_head, new_args)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_head = self._head.replaceStrings(prefix, subs, counter)
        new_args = [x.replaceStrings(prefix, subs, counter) for x in self._arguments]
        return FunctionExpression(new_head, new_args)

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: None | Callable[[Expression, Expression], Expression] = None,
    ):
        new_head = self._head.replaceDotProducts(idx_prefixes, metric, dotproduct)
        new_args = [
            x.replaceDotProducts(idx_prefixes, metric, dotproduct)
            for x in self._arguments
        ]
        return FunctionExpression(new_head, new_args)

    def __len__(self):
        return len(self._arguments)

    def __getitem__(self, index: int) -> Expression:
        return self._arguments[index]

    @override
    def __eq__(self, other: object):
        if isinstance(other, FunctionExpression):
            if self._head == other._head and len(self) == len(other):
                for i in range(len(self)):
                    if self[i] != other[i]:
                        return False
                return True
            else:
                return False
        else:
            return False


@final
class DotExpression(Expression):
    def __init__(self, first: Expression, second: Expression):
        self._deps: dict[str, bool] = {}
        self._first = first
        self._second = second

    @override
    def __str__(self):
        return "(" + str(self._first) + "." + str(self._second) + ")"

    @override
    def replaceIntegerPowers(self, pow_fun: Expression):
        return DotExpression(
            self._first.replaceIntegerPowers(pow_fun),
            self._second.replaceIntegerPowers(pow_fun),
        )

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: None | Callable[[Expression, Expression], Expression] = None,
    ):
        if isinstance(self._first, SymbolExpression) or isinstance(
            self._first, SpecialExpression
        ):
            s1 = str(self._first)
            i1 = any(s1.startswith(prefix) for prefix in idx_prefixes)
        else:
            i1 = False

        if isinstance(self._second, SymbolExpression) or isinstance(
            self._second, SpecialExpression
        ):
            s2 = str(self._second)
            i2 = any(s2.startswith(prefix) for prefix in idx_prefixes)
        else:
            i2 = False

        if i1 and i2:
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

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ):
        s1 = self._first.replaceNegativeIndices(lvl, pattern, found)
        s2 = self._second.replaceNegativeIndices(lvl, pattern, found)
        return DotExpression(s1, s2)

    @override
    def __eq__(self, other: object):
        if isinstance(other, DotExpression):
            return (self._first == other._first and self._second == other._second) or (
                self._first == other._second and self._second == other._first
            )
        else:
            return False

    def getFirst(self):
        return self._first

    def getSecond(self):
        return self._second

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_first = self._first.replaceFloats(prefix, subs, counter)
        new_second = self._second.replaceFloats(prefix, subs, counter)
        return DotExpression(new_first, new_second)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_first = self._first.replaceStrings(prefix, subs, counter)
        new_second = self._second.replaceStrings(prefix, subs, counter)
        return DotExpression(new_first, new_second)

    @override
    def countSymbolPowers(self) -> Mapping[str, int]:
        p1 = self._first.countSymbolPowers()
        p2 = self._second.countSymbolPowers()
        return addSymbolPowers(p1, p2)

    @override
    def powerCounting(self, powers: MutableMapping[str, int]):
        return self._first.powerCounting(powers) + self._second.powerCounting(powers)

    @override
    def getPrecedence(self):
        return 500

    @override
    def dependsOn(self, symbol: str):
        if symbol in self._deps:
            return self._deps[symbol]
        else:
            dep = self._first.dependsOn(symbol) or self._second.dependsOn(symbol)
            self._deps[symbol] = dep
            return dep

    @override
    def prefixSymbolsWith(self, prefix: str):
        return DotExpression(
            self._first.prefixSymbolsWith(prefix),
            self._second.prefixSymbolsWith(prefix),
        )

    @override
    def subs(self, aDict: Mapping[str, Expression]) -> Expression:
        return DotExpression(self._first.subs(aDict), self._second.subs(aDict))

    @override
    def algsubs(self, orig: Expression, image: Expression) -> Expression:
        if self == orig:
            return image
        else:
            return DotExpression(
                self._first.algsubs(orig, image), self._second.algsubs(orig, image)
            )

    @override
    def write(self, out: TextIO):
        if self._first.getPrecedence() >= self.getPrecedence():
            self._first.write(out)
        else:
            _ = out.write("(")
            self._first.write(out)
            _ = out.write(")")

        _ = out.write(".")

        if self._second.getPrecedence() >= self.getPrecedence():
            self._second.write(out)
        else:
            _ = out.write("(")
            self._second.write(out)
            _ = out.write(")")

    @override
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


@final
class PowerExpression(Expression):
    def __init__(self, base: Expression, exponent: Expression):
        self._base = base
        self._exponent = exponent

    @override
    def __str__(self):
        return "(" + str(self._base) + ")^(" + str(self._exponent) + ")"

    @override
    def __eq__(self, other: object):
        if isinstance(other, PowerExpression):
            return self._base == other._base and self._exponent == other._exponent
        else:
            return False

    def getBase(self):
        return self._base

    def getExponent(self):
        return self._exponent

    @override
    def replaceIntegerPowers(self, pow_fun: Expression):
        return PowerExpression(
            self._base.replaceIntegerPowers(pow_fun),
            self._exponent.replaceIntegerPowers(pow_fun),
        )

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_base = self._base.replaceFloats(prefix, subs, counter)
        new_exponent = self._exponent.replaceFloats(prefix, subs, counter)
        return PowerExpression(new_base, new_exponent)

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ):
        new_base = self._base.replaceNegativeIndices(lvl, pattern, found)
        new_exponent = self._exponent.replaceNegativeIndices(lvl, pattern, found)
        return PowerExpression(new_base, new_exponent)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        new_base = self._base.replaceStrings(prefix, subs, counter)
        new_exponent = self._exponent.replaceStrings(prefix, subs, counter)
        return PowerExpression(new_base, new_exponent)

    @override
    def __int__(self) -> int:
        return cast(int, int(self._base) ** int(self._exponent))

    @override
    def countSymbolPowers(self) -> Mapping[str, int]:
        powers = self._base.countSymbolPowers()
        try:
            factor = int(self._exponent)
        except NotImplementedError:
            return {}

        return mulSymbolPowers(powers, factor)

    @override
    def powerCounting(self, powers: MutableMapping[str, int]):
        return int(self._exponent) * self._base.powerCounting(powers)

    @override
    def dependsOn(self, symbol: str):
        return self._base.dependsOn(symbol) or self._exponent.dependsOn(symbol)

    @override
    def prefixSymbolsWith(self, prefix: str):
        return PowerExpression(
            self._base.prefixSymbolsWith(prefix),
            self._exponent.prefixSymbolsWith(prefix),
        )

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: Callable[[Expression, Expression], Expression] | None = None,
    ):
        return PowerExpression(
            self._base.replaceDotProducts(idx_prefixes, metric, dotproduct),
            self._exponent.replaceDotProducts(idx_prefixes, metric, dotproduct),
        )

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        return PowerExpression(self._base.subs(aDict), self._exponent.subs(aDict))

    @override
    def algsubs(self, orig: Expression, image: Expression) -> Expression:
        if self == orig:
            return image
        else:
            return PowerExpression(
                self._base.algsubs(orig, image), self._exponent.algsubs(orig, image)
            )

    @override
    def getPrecedence(self):
        return 400

    @override
    def write(self, out: TextIO):
        if self._base.getPrecedence() >= self.getPrecedence():
            self._base.write(out)
        else:
            _ = out.write("(")
            self._base.write(out)
            _ = out.write(")")

        _ = out.write("^")

        if self._exponent.getPrecedence() >= self.getPrecedence():
            self._exponent.write(out)
        else:
            _ = out.write("(")
            self._exponent.write(out)
            _ = out.write(")")

    @override
    def write_fortran(self):
        r_string = ""
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


@final
class ProductExpression(Expression):
    def __init__(self, factors: Sequence[tuple[int, Expression]]):
        self._factors = factors[:]

    @override
    def __eq__(self, other: object):
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

    def __getitem__(self, index: int) -> tuple[int, Expression]:
        return self._factors[index]

    def getFactors(self):
        return self._factors[:]

    @override
    def countSymbolPowers(self):
        result = {}
        for sig, factor in self._factors:
            p = factor.countSymbolPowers()
            if sig == -1:  # TODO: Is this correct?
                p = mulSymbolPowers(p, -1)
            result = addSymbolPowers(p, result)
        return result

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        result: list[tuple[int, Expression]] = []
        for sig, factor in self._factors:
            p = factor.replaceFloats(prefix, subs, counter)
            result.append((sig, p))
        return ProductExpression(result)

    @override
    def replaceIntegerPowers(self, pow_fun: Expression):
        result: list[tuple[int, Expression]] = []
        for sig, factor in self._factors:
            p = factor.replaceIntegerPowers(pow_fun)
            result.append((sig, p))
        return ProductExpression(result)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        result: list[tuple[int, Expression]] = []
        for sig, factor in self._factors:
            p = factor.replaceStrings(prefix, subs, counter)
            result.append((sig, p))
        return ProductExpression(result)

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ):
        result: list[tuple[int, Expression]] = []
        for sig, factor in self._factors:
            p = factor.replaceNegativeIndices(lvl, pattern, found)
            result.append((sig, p))
        return ProductExpression(result)

    @override
    def powerCounting(self, powers: MutableMapping[str, int]):
        return sum([sig * term.powerCounting(powers) for sig, term in self._factors])

    @override
    def __int__(self) -> int:
        num = 1
        den = 1
        for sig, factor in self._factors:
            if sig == 1:
                num *= int(factor)
            else:
                den *= int(factor)
        return num / den

    @override
    def dependsOn(self, symbol: str):
        return any(factor.dependsOn(symbol) for _, factor in self._factors)

    @override
    def prefixSymbolsWith(self, prefix: str):
        new_factors: list[tuple[int, Expression]] = []
        for sign, factor in self._factors:
            new_factors.append((sign, factor.prefixSymbolsWith(prefix)))
        return ProductExpression(new_factors)

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: Callable[[Expression, Expression], Expression] | None = None,
    ):
        new_factors: list[tuple[int, Expression]] = []
        for sign, factor in self._factors:
            new_factors.append(
                (sign, factor.replaceDotProducts(idx_prefixes, metric, dotproduct))
            )
        return ProductExpression(new_factors)

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        new_factors: list[tuple[int, Expression]] = []
        for sign, factor in self._factors:
            new_factors.append((sign, factor.subs(aDict)))
        return ProductExpression(new_factors)

    @override
    def algsubs(self, orig: Expression, image: Expression):
        if self == orig:
            return image
        else:
            new_factors: list[tuple[int, Expression]] = []
            for sign, factor in self._factors:
                new_factors.append((sign, factor.algsubs(orig, image)))
            return ProductExpression(new_factors)

    @override
    def __str__(self):
        return "*".join(
            ["(" + str(term) + ")^" + str(sig) for sig, term in self._factors]
        )

    @override
    def write(self, out: TextIO):
        first_sig, first_term = self._factors[0]
        follow = self._factors[1:]
        if first_sig == -1:
            _ = out.write("1/")
        if first_term.getPrecedence() >= self.getPrecedence():
            first_term.write(out)
        else:
            _ = out.write("(")
            first_term.write(out)
            _ = out.write(")")

        for sig, term in follow:
            if sig == 1:
                _ = out.write("*")
            else:
                _ = out.write("/")
            if term.getPrecedence() > self.getPrecedence():
                term.write(out)
            else:
                _ = out.write("(")
                term.write(out)
                _ = out.write(")")

    @override
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

    @override
    def getPrecedence(self):
        return 200


@final
class SumExpression(Expression):
    def __init__(self, terms: Sequence[Expression]):
        self._deps: MutableMapping[str, bool] = {}
        self._terms = list(terms)

    @override
    def __eq__(self, other: object):
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

    def __getitem__(self, index: int) -> Expression:
        return self._terms[index]

    def getTerms(self):
        return self._terms[:]

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        result: list[Expression] = []
        for term in self._terms:
            p = term.replaceFloats(prefix, subs, counter)
            result.append(p)
        return SumExpression(result)

    @override
    def replaceIntegerPowers(self, pow_fun: Expression):
        result: list[Expression] = []
        for term in self._terms:
            p = term.replaceIntegerPowers(pow_fun)
            result.append(p)
        return SumExpression(result)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        result: list[Expression] = []
        for term in self._terms:
            p = term.replaceStrings(prefix, subs, counter)
            result.append(p)
        return SumExpression(result)

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ):
        result: list[Expression] = []
        for term in self._terms:
            p = term.replaceNegativeIndices(lvl, pattern, found)
            result.append(p)
        return SumExpression(result)

    @override
    def countSymbolPowers(self) -> Mapping[str, int]:
        all_p: list[Mapping[str, int]] = []
        names: set[str] = set([])
        for term in self._terms:
            p = term.countSymbolPowers()
            all_p.append(p)
            names.update(list(p.keys()))

        result: Mapping[str, int] = {}
        for name in names:
            if any(name not in p for p in all_p):
                continue
            pow = [p[name] for p in all_p]
            maxp = max(pow)
            minp = min(pow)
            if minp == maxp:
                result[name] = minp
        return result

    @override
    def __int__(self):
        return sum(map(int, self._terms))

    @override
    def dependsOn(self, symbol: str):
        if symbol in self._deps:
            return self._deps[symbol]
        else:
            dep = any(term.dependsOn(symbol) for term in self._terms)
            self._deps[symbol] = dep
            return dep

    @override
    def prefixSymbolsWith(self, prefix: str):
        return SumExpression([term.prefixSymbolsWith(prefix) for term in self._terms])

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: Callable[[Expression, Expression], Expression] | None = None,
    ):
        return SumExpression(
            [
                term.replaceDotProducts(idx_prefixes, metric, dotproduct)
                for term in self._terms
            ]
        )

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        return SumExpression([term.subs(aDict) for term in self._terms])

    @override
    def algsubs(self, orig: Expression, image: Expression):
        if self == orig:
            return image
        else:
            return SumExpression([term.algsubs(orig, image) for term in self._terms])

    @override
    def write(self, out: TextIO):
        first = self._terms[0]
        follow = self._terms[1:]
        if first.getPrecedence() >= self.getPrecedence():
            first.write(out)
        else:
            _ = out.write("(")
            first.write(out)
            _ = out.write(")")

        for term in follow:
            if isinstance(term, UnaryMinusExpression):
                term.write(out)
            else:
                _ = out.write("+")
                if term.getPrecedence() >= self.getPrecedence():
                    term.write(out)
                else:
                    _ = out.write("(")
                    term.write(out)
                    _ = out.write(")")

    @override
    def write_fortran(self) -> str:
        r_string = ""
        first = self._terms[0]
        follow = self._terms[1:]
        if first.getPrecedence() >= self.getPrecedence():
            r_string += first.write_fortran()
        else:
            r_string += "("
            r_string += first.write_fortran()
            r_string += ")"

        for term in follow:
            if isinstance(term, UnaryMinusExpression):
                r_string += term.write_fortran()
            else:
                r_string += "+"
                if term.getPrecedence() >= self.getPrecedence():
                    r_string += term.write_fortran()
                else:
                    r_string += "("
                    r_string += term.write_fortran()
                    r_string += ")"
        return r_string

    @override
    def getPrecedence(self):
        return 100

    @override
    def __str__(self):
        return "+".join(map(str, self._terms))


@final
class UnaryMinusExpression(Expression):
    def __init__(self, term: Expression):
        self._deps: MutableMapping[str, bool] = {}
        self._term = term

    @override
    def __str__(self):
        return "-(" + str(self._term) + ")"

    @override
    def __eq__(self, other: object):
        if isinstance(other, UnaryMinusExpression):
            return self._term == other._term
        else:
            return False

    def getTerm(self):
        return self._term

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        p = self._term.replaceFloats(prefix, subs, counter)
        return UnaryMinusExpression(p)

    @override
    def replaceIntegerPowers(self, pow_fun: Expression):
        p = self._term.replaceIntegerPowers(pow_fun)
        return UnaryMinusExpression(p)

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ):
        p = self._term.replaceStrings(prefix, subs, counter)
        return UnaryMinusExpression(p)

    @override
    def countSymbolPowers(self):
        return self._term.countSymbolPowers()

    @override
    def powerCounting(self, powers: MutableMapping[str, int]):
        return self._term.powerCounting(powers)

    @override
    def __int__(self):
        return -int(self._term)

    @override
    def dependsOn(self, symbol: str):
        if symbol in self._deps:
            return self._deps[symbol]
        else:
            dep = self._term.dependsOn(symbol)
            self._deps[symbol] = dep
            return dep

    @override
    def prefixSymbolsWith(self, prefix: str):
        return UnaryMinusExpression(self._term.prefixSymbolsWith(prefix))

    @override
    def replaceDotProducts(
        self,
        idx_prefixes: Sequence[str],
        metric: Callable[[Expression, Expression], Expression],
        dotproduct: Callable[[Expression, Expression], Expression] | None = None,
    ):
        return UnaryMinusExpression(
            self._term.replaceDotProducts(idx_prefixes, metric, dotproduct)
        )

    @override
    def replaceNegativeIndices(
        self, lvl: int, pattern: str, found: MutableMapping[int, Expression]
    ) -> Expression:
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
                self._term.replaceNegativeIndices(lvl, pattern, found)
            )

    @override
    def subs(self, aDict: Mapping[str, Expression]):
        return UnaryMinusExpression(self._term.subs(aDict))

    @override
    def algsubs(self, orig: Expression, image: Expression):
        if self == orig:
            return image
        else:
            return UnaryMinusExpression(self._term.algsubs(orig, image))

    @override
    def write(self, out: TextIO):
        _ = out.write("-")
        if self._term.getPrecedence() >= self.getPrecedence():
            self._term.write(out)
        else:
            _ = out.write("(")
            self._term.write(out)
            _ = out.write(")")

    @override
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

    @override
    def getPrecedence(self):
        return 150


@final
class SpecialExpression(ConstantExpression):
    def __init__(self, image: str):
        self._image = image

    @override
    def __eq__(self, other: object):
        if isinstance(other, SpecialExpression):
            return self._image == other._image
        else:
            return False

    @override
    def write(self, out: TextIO):
        _ = out.write(self._image)

    @override
    def write_fortran(self):
        return self._image

    @override
    def __str__(self):
        return self._image

    @override
    def replaceFloats(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        return self


@final
class StringExpression(ConstantExpression):
    def __init__(self, image: str):
        self._image = image

    @override
    def __eq__(self, other: object):
        if isinstance(other, SpecialExpression):
            return self._image == other._image
        else:
            return False

    @override
    def write(self, out: TextIO):
        _ = out.write("'" + self._image + "'")

    @override
    def write_fortran(self):
        return "'" + self._image + "'"

    @override
    def __str__(self):
        return "'" + self._image + "'"

    @override
    def replaceStrings(
        self,
        prefix: str,
        subs: MutableMapping[str, Expression],
        counter: list[int] = [0],
    ) -> Expression:
        if self._image in subs:
            return subs[self._image]

        counter[0] += 1
        name = "%s%d" % (prefix, counter[0])
        expr = SymbolExpression(name)
        subs[self._image] = expr
        return expr


def addSymbolPowers(p1: Mapping[str, int], p2: Mapping[str, int]):
    names = set(list(p1.keys()) + list(p2.keys()))
    result: Mapping[str, int] = {}
    for name in names:
        p = 0
        if name in p1:
            p += p1[name]
        if name in p2:
            p += p2[name]
        result[name] = p
    return result


def mulSymbolPowers(p1: Mapping[str, int], factor: int) -> Mapping[str, int]:
    result: Mapping[str, int] = {}
    for name, p in list(p1.items()):
        result[name] = factor * p
    return result


def resolve_dependencies(functions: Mapping[str, Expression]):
    """
    Bring a list of expressions into an order in which they
    can be computed
    """
    all_names = list(functions.keys())
    nfunctions = len(all_names)
    graph: dict[str, list[str]] = {}
    logger.info("      * Building call graph")
    i = 0
    for name, expr in list(functions.items()):
        i += 1
        if i % 100 == 0:
            logger.info("         (%5d/%5d)" % (i, nfunctions))
        edges: list[str] = []
        for other in all_names:
            if name == other:
                continue

            if expr.dependsOn(other):
                edges.append(other)
        graph[name] = edges

    logger.info("      * Traversing call graph")
    nedges = len(graph)
    logger.info("         %5d edges left" % nedges)

    program: list[str] = []
    name = ""
    while len(graph) > 0:
        found = None
        for name, edges in list(graph.items()):
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
                for name in list(graph.keys()):
                    bottom = True
                    for edges in list(graph.values()):
                        if name in edges:
                            bottom = False
                            break
                    if bottom:
                        bottom_expression = name
                        break
                if bottom_expression is not None:
                    flag = True
                    del graph[bottom_expression]

            problem_set = ", ".join(list(graph.keys()))

            logger.critical(
                "Cannot resolve dependencies between functions: %s." % problem_set
            )
            sys.exit("GoSam terminated due to an error")

        program.append(name)
        del graph[name]
        nedges -= 1
        if nedges % 100 == 0:
            logger.info("         %5d edges left" % nedges)

        for edges in list(graph.values()):
            if name in edges:
                edges.remove(name)

    return program
