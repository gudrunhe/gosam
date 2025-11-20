# vim: ts=3:sw=3
import re
from collections.abc import Iterator
from re import Pattern
from typing import Callable, cast, final


class Scanner(object):
    """
    Implements a general purpose scanner (=tokenizer).
    """

    def __init__(self):
        patterns: list[str] = []
        actions = {}

        for name, func in cast(
            dict[str, Callable[[Scanner, str], str | None]], self.__class__.__dict__
        ).items():
            doc = func.__doc__
            if doc is not None:
                errmsg = (
                    "In doc-string of %s.%s: " % (self.__class__.__name__, name)
                ) + "Invalid pattern after '@TOKEN' (%s)."

                for line in doc.splitlines():
                    sline = line.strip()
                    if sline.startswith("@TOKEN"):
                        sline = sline[len("@TOKEN") :].strip()
                        delim = sline[0:1]
                        lasti = sline.rfind(delim, 1)
                        if lasti < 0:
                            raise SyntaxError(
                                errmsg % ("Missing closing delimiter '%s'" % delim)
                            )
                        pattern = sline[1:lasti]
                        flags = sline[lasti + 1 :].strip()
                        iflags = 0
                        for ch in flags.upper():
                            if ch == "I":
                                iflags += re.IGNORECASE
                            elif ch == "L":
                                iflags += re.LOCALE
                            elif ch == "S":
                                iflags += re.DOTALL
                            elif ch == "U":
                                iflags += re.UNICODE
                            elif ch in [" ", "\t"]:
                                pass
                            else:
                                raise SyntaxError(errmsg % ("Unknown flag '%s'" % ch))

                        gpattern = "(?P<%s>%s%s)" % (
                            name,
                            flags_to_string(iflags),
                            pattern,
                        )
                        try:
                            prog = re.compile(gpattern)
                        except BaseException as ex:
                            raise SyntaxError(errmsg % str(ex))
                        if prog.match(""):
                            raise SyntaxError(
                                errmsg % ("%r matches the empty string" % pattern)
                            )
                        patterns.append(gpattern)
                        actions[name] = func

                        break

        self._REGEX: Pattern[str] = re.compile("|".join(patterns), re.MULTILINE)
        self._ACTIONS: dict[str, Callable[[Scanner, str], str | int | float | None]] = (
            actions
        )

    def parse(self, text: str) -> Iterator[tuple[str, str | int | float]]:
        for match in self._REGEX.finditer(text):
            for name, image in match.groupdict().items():
                if image is None:
                    continue
                token = self._ACTIONS[name](self, image)
                if token is not None:
                    yield (name, token)


@final
class TokenStream:
    def __init__(self, scanner: Scanner, text: str):
        self._iter: Iterator[tuple[str, str | int | float]] = scanner.parse(text)
        self._stack: list[tuple[str, str | int | float]] = []
        self._text = text

    def source(self):
        return self._text

    def name(self) -> str:
        name, _ = self.top()
        return name

    def token(self):
        _, token = self.top()
        return token

    def top(self) -> tuple[str, str | int | float | None]:
        if len(self._stack) == 0:
            try:
                name, token = next(self._iter)
                self._stack.append((name, token))
                return (name, token)
            except StopIteration:
                return ("", None)
        else:
            return self._stack[-1]

    def pop(self):
        _, token = self.top()
        if len(self._stack) > 0:
            _ = self._stack.pop()
        return token

    def push(self, name: str, token: str):
        self._stack.append((name, token))


def flags_to_string(flags: int) -> str:
    FS = {
        re.IGNORECASE: "i",
        re.LOCALE: "L",
        re.MULTILINE: "m",
        re.DOTALL: "s",
        re.UNICODE: "u",
    }

    if flags == 0:
        return ""
    res = "(?"
    for num, ch in list(FS.items()):
        if flags & num == num:
            res += ch
    res += ")"
    return res
