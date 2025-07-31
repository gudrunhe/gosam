# vim: ts=3:sw=3:expandtab
import sys
import datetime
import re

try:
    import ast
except ImportError:
    ast = None

import logging

logger = logging.getLogger(__name__)


class GolemConfigError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)
        self._value = value

    def __str__(self):
        return "GoSam Configuration Error: %s" % self._value

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self._value)

    def value(self):
        return self._value


class Property:
    """
    This class is a wrapper for properties including their
    type and a description.

    The use of a wrapper allows for future changes of the syntax
    without affecting the source code in many places.
    """

    def __init__(
        self, name, description, type=str, default=None, experimental=False, options=None, sep=None, hidden=False
    ):
        """
        Note, in the case of type=list sep encodes the
        delimiter character (';' or ',') with if sep=None
        the comma is used.
        """
        self._name = name
        self._description = description
        self._type = type
        self._default = default
        self._experimental = experimental
        self._options = options
        self._sep = sep
        self._hidden = hidden

    def _guess_correct(self, options, *given):
        result = []
        for word in given:
            min_lev = len(word)
            min_opt = None
            for option in options:
                dist = levenshtein(word, option)
                if dist < min_lev:
                    min_opt = option
                    min_lev = dist
            if min_opt is not None and min_lev <= 5:
                result.append(("If you meant '%s' instead of '%s', " + "please correct and rerun!") % (min_opt, word))
        return result

    def check(self, conf):
        result = []

        if self._type == int:
            if self._options is not None:
                value = conf.getProperty(str(self))

                if value is not None:
                    try:
                        ivalue = int(value)
                        if value not in self._options:
                            result.append(
                                ("The value (%d) of option '%s'" + " is not in the valid range.") % (ivalue, self)
                            )
                    except ValueError:
                        result.append(("The value (%r) of option '%s'" + " is not an integer number.") % (value, self))

        elif self._type == bool:
            bool_values = [
                "1",
                "true",
                ".true.",
                "t",
                ".t.",
                "yes",
                "y",
                "0",
                "false",
                ".false.",
                "f",
                ".f.",
                "no",
                "n",
            ]
            value = conf.getProperty(str(self))

            if value is not None:
                if value.lower() not in bool_values:
                    result.append("The value (%r) of option '%s' is not a boolean literal." % (value, self))
                    result.extend(self._guess_correct(bool_values, value))

        elif self._type == list:
            if self._options is not None:
                odds = []
                default = self.getDefault()
                sep = self.getSep()
                sval = conf.getProperty(str(self))
                if sval is not None:
                    if sep is None:
                        values = sval.split(",")
                    else:
                        values = sval.split(sep)

                    for value in values:
                        vls = value.lower().strip()
                        if vls == "":
                            continue
                        if vls not in self._options:
                            odds.append(value)

                if len(odds) > 0:
                    result.append("The option '%s' contains unexpected values: %s" % (self, ", ".join(map(repr, odds))))
                    result.extend(self._guess_correct(self._options, *odds))
        else:
            if self._options is not None:
                value = conf.getProperty(str(self))
                if value is not None:
                    if value.lower() not in self._options:
                        result.append("Unexpected value (%r) for option '%s'." % (value, self))
                        result.extend(self._guess_correct(self._options, value))

        return result

    def isExperimental(self):
        return self._experimental

    def isHidden(self):
        return self._hidden

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getType(self):
        return self._type

    def getDefault(self):
        return self._default

    def getSep(self):
        return self._sep

    def __str__(self):
        return self.getName()

    def __repr__(self):
        return "Property(%r, %r, %r, %r)" % (self._name, self._description, self._type, self._default)


class Properties:
    """
    This class provides a simplistic replacement for
    the Java class java.util.Properties.

    It is simplistic with respect to the limited number
    of escape sequences which are implemented:
      '\\', '\n', '\r', '\f', '\t'.
    As in the Java implementation, a single backslash
    in front of any other character is removed.
    """

    def __init__(self, defaults=None, **values):
        self._defaults = defaults
        self._map = {}
        for key, value in list(values.items()):
            self.setProperty(key, str(value))

        self._decode = False

        self.cache = {}

    def decode(self):
        self._decode = True

    def nodecode(self):
        self._decode = False

    def getProperty(self, key, default=None):
        result = self._getProperty(key)
        if result is None:
            return default
        else:
            return result

    def _getProperty(self, key):
        if isinstance(key, Property):
            type = key.getType()
            name = str(key)
            default = key.getDefault()
            sep = key.getSep()
            if type == int:
                return self.getIntegerProperty(name, default)
            elif type == bool:
                return self.getBooleanProperty(name, default)
            elif type == list:
                if sep is None:
                    return self.getListProperty(name, default, ",")
                else:
                    return self.getListProperty(name, default, sep)
            else:
                return self.getProperty(name, default)
        else:
            if key in self._map:
                result = self._map[key]
            elif self._defaults is not None:
                if key in self._defaults:
                    result = self._defaults[key]
                else:
                    return None
            else:
                return None

            if self._decode and isinstance(result, str):
                # won't work in python3:
                # return result.decode("string_escape")
                # This is not 100% correct but should work reasonably well:
                if ast is not None:
                    return ast.literal_eval("'" + result + "'")
                else:
                    return result.decode("string_escape")
            else:
                return result

    def getListProperty(self, key, default=None, delimiter=","):
        name = str(key)
        if name in self:
            value = self[name].split(delimiter)
            return list([x.strip() for x in value])
        else:
            if default:
                return default.split(delimiter)
            else:
                return []

    def getBooleanProperty(self, key, default=False):
        true_values = ["1", "true", ".true.", "t", ".t.", "yes", "y"]
        name = str(key)
        if name in self:
            value = self.getProperty(name, default=default).strip().lower()
            return value in true_values
        else:
            return default

    def getIntegerProperty(self, key, default=None):
        name = str(key)
        if name in self:
            value = self.getProperty(name, default=default).strip()
            try:
                return int(value)
            except ValueError as ex:
                raise GolemConfigError("Property '%s' does not contain an integer value ('%s')." % (key, value))
        else:
            return default

    def copyProperties(self, other, *keys):
        for key in keys:
            self.setProperty(key, other.getProperty(key))

    def copy(self):
        result = Properties()
        for key in self.propertyNames():
            result.setProperty(key, self.getProperty(key))
        return result

    def setProperty(self, key, value):
        name = str(key)
        if name.startswith("+"):
            self.setProperty(name[1:], value)
        if value.__class__ == list:
            self._map[name] = ",".join(map(str, value))
        else:
            self._map[name] = str(value)

    def __contains__(self, key):
        name = str(key)
        if name in self._map:
            return True
        elif self._defaults is not None:
            return name in self._defaults
        else:
            return False

    def propertyNames(self):
        for key in list(self._map.keys()):
            yield key
        if self._defaults is not None:
            for key in self._defaults:
                if key not in self._map:
                    yield key

    def list(self, stream=sys.stdout):
        for key in self:
            stream.write("%s=%s\n" % (escape(key, True), escape(self[key])))

    def store(self, stream, comments=None, properties=None, info=[]):
        def format_comment(prop):
            if prop.getType() == str:
                stype = "text"
            elif prop.getType() == int:
                stype = "integer number"
            elif prop.getType() == bool:
                stype = "true/false"
            elif prop.getType() == list:
                stype = "comma separated list"
            else:
                stype = str(prop.getType())

            stream.write("### %s (%s)\n" % (prop, stype))
            for line in prop.getDescription().splitlines(False):
                text = "# %s" % (line.expandtabs(3))
                stream.write("%s\n" % text)

            if prop.isExperimental():
                stream.write("### This property is marked as EXPERIMENTAL !!!\n")

        if comments is not None:
            for cline in comments.splitlines():
                stream.write("# %s\n" % cline)
        stream.write("# %s\n" % datetime.datetime.now())

        keys = [key for key in self]

        for key in info:
            if key in keys:
                stream.write("# %s=%s\n" % (key, self[key]))
                keys.remove(key)
        stream.write("\n")

        if properties is not None:
            for propty in properties:
                key = str(propty)
                if propty.isHidden() and not (self[key] is propty.getDefault()):
                    continue
                format_comment(propty)

                if key in keys:
                    stream.write("%s=%s\n" % (escape(key, True), escape(self[key])))
                    keys.remove(key)
                else:
                    dflt = propty.getDefault()
                    if dflt is None:
                        dflt = ""
                    else:
                        dflt = str(dflt)
                    stream.write("### Default:\n")
                    stream.write("# %s=%s\n" % (escape(key, True), escape(dflt)))
                stream.write("\n")

        stream.write("### Further settings:\n")
        keys.sort()
        for key in keys:
            stream.write("%s=%s\n" % (escape(key, True), escape(self[key])))

    def load(self, stream, avail_props=[]):
        dollar_variables = []
        buf = ""
        raise_err = False
        err_str = ""
        for line in stream:
            buf += line.strip()
            if buf.startswith("!") or buf.startswith("#"):
                buf = ""
                continue
            elif buf == "":
                continue
            elif buf.endswith("\\"):
                bksl = ""
                while buf.endswith("\\\\"):
                    bksl += "\\\\"
                    buf = buf.rstrip("\\\\")
                if buf.endswith("\\"):
                    buf = buf.rstrip("\\")
                    buf += bksl
                    continue
                else:
                    buf += bksl
            # consider the line as terminated now

            # don't do replacements just look for '\\' or
            # one of '=', ':', ' ', '\t', '\f'
            preceeding_backslash = False
            separator_index = -1
            in_brackets = False
            for i in range(len(buf)):
                if (not preceeding_backslash and not in_brackets) and (buf[i] in ["=", ":", " ", "\f", "\t"]):
                    separator_index = i
                    break
                if buf[i] == "[":
                    in_brackets = True
                elif buf[i] == "]":
                    in_brackets = False
                elif buf[i] == "\\":
                    preceeding_backslash = not preceeding_backslash
                else:
                    preceeding_backslash = False

            if in_brackets:
                raise GolemConfigError("Invalid range specification in '%s'. Missing ']'?" % buf)

            if separator_index < 0:
                key = buf.strip()
                value = ""
            else:
                key = buf[0:separator_index].strip()
                value = buf[separator_index + 1 :].strip()

            for dkey, dvalue in reversed(dollar_variables):
                for fmt in ["${%s}", "$(%s)", "$%s"]:
                    key = key.replace(fmt % dkey, dvalue)
                    value = value.replace(fmt % dkey, dvalue)

            if key.startswith("$"):
                dollar_variables.append((key[1:], value))
            else:
                if "contrib_fc" in key:
                    buf = ""
                    continue
                if False if avail_props == [] else (key not in avail_props):
                    raise_err = True
                    err_str = err_str + ", " + str(key) if err_str else str(key)
                    buf = ""
                    continue
                self.setProperty(unescape(key), unescape(value))
            buf = ""
        if raise_err:
            raise GolemConfigError(
                "The properties '{0}'".format(err_str) + " which you set in your configuration file are unknown."
            )

    def __getitem__(self, key):
        return self._getProperty(key)

    def __setitem__(self, key, value):
        self.setProperty(key, value)

    def __iter__(self):
        return self.propertyNames()

    def addAll(self, other):
        for name in other:
            self[name] = other[name]
        return self

    def __iadd__(self, other):
        return self.addAll(other)

    def __str__(self):
        res = ""
        for key in self:
            res += "%s=%s\n" % (escape(key, True), escape(self[key]))
        return res

    def _del(self, name):
        del self._map[name]
        # keep plussed and unplussed entries consistent
        if name.startswith("+"):
            del self._map[name[1:]]
        else:
            try:
                del self._map["+" + name]
            except KeyError:
                pass

    def activate_subconfig(self, no):
        changed = {}
        for key in self:
            if "[" not in key:
                continue
            pos = key.index("[")
            if no in extractRange(key[pos + 1 : -1]):
                if key[:pos] in list(changed.keys()) and changed[key[:pos]] != self[key]:
                    raise GolemConfigError(
                        "multiple values for option '%s' in subprocess %s: '%s' or '%s'?"
                        % (key[:pos], no, changed[key[:pos]], self[key])
                    )
                self[key[:pos]] = self[key]
                changed[key[:pos]] = self[key]


def unescape(s):
    buf = [s[i] for i in range(len(s))]
    if "\\" in buf:
        idx_bk = buf.index("\\")
    else:
        idx_bk = -1
    while idx_bk >= 0:
        if idx_bk + 1 < len(buf):
            ch = buf[idx_bk + 1]
            if ch == "n":
                buf[idx_bk : idx_bk + 2] = "\n"
            elif ch == "r":
                buf[idx_bk : idx_bk + 2] = "\r"
            elif ch == "f":
                buf[idx_bk : idx_bk + 2] = "\f"
            elif ch == "t":
                buf[idx_bk : idx_bk + 2] = "\t"
            else:
                del buf[idx_bk : idx_bk + 1]
        if "\\" in buf[idx_bk + 1 :]:
            idx_bk = buf.index("\\", idx_bk + 1)
        else:
            idx_bk = -1
    return "".join(buf)


def escape(s, isKey=False):
    escapes = {"\n": "\\n", "\r": "\\r", "\f": "\\f", "\t": "\\t"}
    keyescapes = {"=": "\\=", ":": "\\:", " ": "\\ "}
    buf = s.replace("\\", "\\\\")
    for ch, esc in list(escapes.items()):
        buf = buf.replace(ch, esc)
    if isKey:
        for ch, esc in list(keyescapes.items()):
            buf = buf.replace(ch, esc)
        if buf[0] in ["#", "!"]:
            buf = "\\" + buf
    return buf

class ConfigurationException(Exception):
    pass

def version_compare(v1, v2):
   l1 = len(v1)
   l2 = len(v2)
   if l1 < l2:
      v1c = v1 + [0] * (l2-l1)
      v2c = v2[:]
   else:
      v1c = v1[:]
      v2c = v2 + [0] * (l1-l2)

   for p1, p2 in zip(v1c, v2c):
      if p1 > p2:
         return 1
      elif p1 < p2:
         return -1
   return 0

def levenshtein(str1, str2, case_sensitive=False):
    l1 = len(str1)
    l2 = len(str2)

    if case_sensitive:
        if l1 < l2:
            if l1 == 0:
                return l2
            s2 = str1
            s1 = str2
        else:
            if l2 == 0:
                return l1
            s1 = str1
            s2 = str2
    else:
        if l1 < l2:
            if l1 == 0:
                return l2
            s2 = str1.lower()
            s1 = str2.lower()
        else:
            if l2 == 0:
                return l1
            s1 = str1.lower()
            s2 = str2.lower()

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row
            # are one character longer
            insertions = previous_row[j + 1] + 1
            # than s2
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def extractRange(s, minval=0, maxval=999):
    """extract ranges from a string and returns a set
     Examples:

    >>> sorted(extractRange("2-3,5-8"))
    [2, 3, 5, 6, 7, 8]
    >>> sorted(extractRange("2-8,!4,!10"))
    [2, 3, 5, 6, 7, 8]
    >>> sorted(extractRange("2-8, !4-6"))
    [2, 3, 7, 8]
    >>> sorted(extractRange("1-10", maxval=5))
    [1, 2, 3, 4, 5]
    >>> sorted(extractRange("2-", 3, 5))
    [3, 4, 5]
    >>> sorted(extractRange("-2"))
    [0, 1, 2]
    >>> extractRange("!4")
    set([])
    >>> sorted(extractRange("-")) == range(0,1000)
    True

    """
    s = s.replace(" ", ",")
    ranges = [x.split("-") for x in s.split(",")]
    res = set()
    for r in ranges:
        if r == [""]:
            continue
        elif len(r) == 1:
            if r[0][0] in "^!":
                res.discard(int(r[0][1:]))
            else:
                res.add(int(r[0]))
        elif len(r) == 2:
            remove = r[0] and (r[0][0] in "^!")
            if remove:
                r[0] = r[0][1:]
            start = minval if r[0] == "" else int(r[0])
            end = maxval if r[1] == "" else int(r[1])
            if remove:
                res = set([x for x in res if x < start or x > end])
            else:
                res.update(list(range(start, end + 1)))
        else:  # len(r)>2
            raise ValueError("Invalid range: %s in '%s'" % (r, s))
    res = set([x for x in res if x >= minval and x <= maxval])
    return res


def split_qgrafPower(power):
    """
    >>> split_qgrafPower('QCD,2,0,QED,3,3')
    [['QCD', 2, 0], ['QED', 3, 3]]
    >>> split_qgrafPower('QCD,2,QED,3')
    [['QCD', 2], ['QED', 3]]
    >>> split_qgrafPower('QCD,2,3,QED,3')
    [['QCD', 2, 3], ['QED', 3, 3]]
    >>> split_qgrafPower('QCD,2')
    [['QCD', 2]]
    >>> split_qgrafPower('QED,3,4')
    [['QED', 3, 4]]
    >>> split_qgrafPower('QCD,2,3,4,QED,3,NP,1')
    [['QCD', 2, 3, 4], ['QED', 3, 3, 3], ['NP', 1, 1, 1]]
    >>> split_qgrafPower('QED,3,4,QED,3,4')
    Traceback (most recent call last):
     ...
    ConfigurationException: Coupling 'QED' repeated
    """
    if type(power) == list:
        return power
    assert type(power) == str
    min_length = 0
    orders = []
    couplings = set()
    l = re.split(",|;", power)
    current_coupling = []
    for i in l + [""]:
        if str(i).isdigit() or str(i).lower() == "none":
            assert current_coupling
            current_coupling.append(i)
        else:
            current_len = len(current_coupling) - 1
            if current_len < 0:
                current_len = 0
            if current_len < min_length and current_coupling:
                if current_len > 0:
                    current_coupling.extend([current_coupling[-1]] * (min_length - current_len))
                else:
                    current_coupling.extend([0] * (min_length - current_len))
            if current_len and current_coupling:
                orders.append(current_coupling)
            if min_length == 0:
                min_length = current_len
            if i:
                current_coupling = [i]
                if i in couplings:
                    raise ConfigurationException("Coupling '%s' repeated" % i)
                couplings.add(i)
            else:
                current_coupling = []
    return orders
