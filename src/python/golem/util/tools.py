# vim: ts=3:sw=3:expandtab
import argparse
import sys
import os.path
import traceback
import re
from copy import copy
import textwrap
import shutil

import golem.model
import golem.properties
import golem.algorithms.helicity
import golem.installation
from golem.installation import LIB_DIR, BIN_DIR

from golem.util.path import golem_path
from golem.util.config import GolemConfigError
from golem.util.constants import MODEL_LOCAL

import logging

logger = logging.getLogger(__name__)

POSTMORTEM_LOG = []
POSTMORTEM_CFG = None
POSTMORTEM_DO = False


class NLRHelpFormatter(argparse.HelpFormatter):
    """
    Newline respecting help formatter: same as default formatter, except that each line is wrapped separately.
    """

    def _split_lines(self, text, width):
        wrapped_lines = []
        for line in text.splitlines():
            line = self._whitespace_matcher.sub(" ", line).strip()
            wrapped_lines += textwrap.wrap(line, width)
        return wrapped_lines

    def _fill_text(self, text, width, indent):
        wrapped_lines = []
        for line in text.splitlines():
            line = self._whitespace_matcher.sub(" ", line).strip()
            wrapped_lines.append(textwrap.fill(line, width, initial_indent=indent, subsequent_indent=indent))
        return "\n".join(wrapped_lines)


class CustomWrapper(textwrap.TextWrapper):
    def wrap(self, text):
        lines = text.splitlines()
        wrapped_lines = [wrapped_line for line in lines for wrapped_line in super(CustomWrapper, self).wrap(line)]
        if len(wrapped_lines) == 1:
            wrapped_lines[0] = "- " + wrapped_lines[0]
        else:
            for i in range(len(wrapped_lines)):
                if i == 0:
                    wrapped_lines[i] = "┌ " + wrapped_lines[i]
                elif i == len(wrapped_lines) - 1:
                    wrapped_lines[i] = "           └ " + wrapped_lines[i]
                else:
                    wrapped_lines[i] = "           │ " + wrapped_lines[i]
        return wrapped_lines


class DuplicationFilter(logging.Filter):
    def __init__(self):
        self.previous_logs = None

    def filter(self, record):
        current_log = (record.module, record.levelno, record.getMessage())
        if not self.previous_logs:
            self.previous_logs = [current_log]
        else:
            if current_log in self.previous_logs:
                return False
            else:
                self.previous_logs.append(current_log)
        return True

class ColorFormatter(logging.Formatter):
    def __init__(self, message, use_color=True, **kwargs):
        super().__init__(message, **kwargs)
        self.use_color = use_color
        self.wrapper = CustomWrapper(width=shutil.get_terminal_size().columns - 13, tabsize=4)

    def format(self, record):
        if self.use_color:
            colored_record = copy(record)
            colored_record.msg = self.wrapper.fill(colored_record.msg)
            if record.levelname == "DEBUG":
                colored_record.levelname = ansi_style("[DEBUG]   ", fg_8bit("8"))
            elif record.levelname == "INFO":
                colored_record.levelname = ansi_style("[INFO]    ", fg_8bit("6"))
            elif record.levelname == "WARNING":
                colored_record.levelname = ansi_style("[WARNING] ", fg_8bit("3"))
            elif record.levelname == "ERROR":
                colored_record.levelname = ansi_style("[ERROR]   ", fg_8bit("208"))
            elif record.levelname == "CRITICAL":
                colored_record.levelname = ansi_style("[CRITICAL]", fg_8bit(1))
                colored_record.msg = ansi_style(colored_record.msg, fg_8bit(1))
            return super().format(colored_record)
        else:
            record.msg = textwrap.fill(record.msg, width=1000)
            if record.levelname == "DEBUG":
                record.levelname = "[DEBUG]    -"
            elif record.levelname == "INFO":
                record.levelname = "[INFO]     -"
            elif record.levelname == "WARNING":
                record.levelname = "[WARNING]  -"
            elif record.levelname == "ERROR":
                record.levelname = "[ERROR]    -"
            elif record.levelname == "CRITICAL":
                record.levelname = "[CRITICAL] -"
            return super().format(record)


def setup_logging(loglevel, logfile=None, use_color=True):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)

    if loglevel != "DEBUG":
        console_formatter = ColorFormatter("{levelname} {message}", style="{", use_color=use_color)
    else:
        console_formatter = ColorFormatter("{levelname} {message} ({funcName} in {filename}:{lineno})", style="{")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(DuplicationFilter())
    root_logger.addHandler(console_handler)
    if logfile is not None:
        if loglevel != "DEBUG":
            file_formatter = ColorFormatter(
                "{asctime} - {levelname} {message}", style="{", datefmt="%H:%M:%S", use_color=False
            )
        else:
            file_formatter = ColorFormatter(
                "{asctime} - {levelname} {message} ({funcName} in {filename}:{lineno})",
                style="{",
                datefmt="%H:%M:%S",
                use_color=False,
            )
        file_handler = logging.FileHandler(logfile, mode="w")
        file_handler.setLevel(loglevel if loglevel == "DEBUG" else "INFO")
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(DuplicationFilter())
        root_logger.addHandler(file_handler)


def fg_24bit(r, g, b):
    return "38;2;{};{};{}".format(r, g, b)


def bg_24bit(r, g, b):
    return "48;2;{};{};{}".format(r, g, b)


def fg_8bit(n):
    return "38;5;{}".format(n)


def bg_8bit(n):
    return "48;5;{}".format(n)


def ansi_style(text, codes):
    if isinstance(codes, (list, tuple)):
        return "\033[{}m".format(";".join(codes)) + text + "\033[0m"
    else:
        return "\033[{}m".format(codes) + text + "\033[0m"


def copy_file(in_file, out_file):
    if not os.path.exists(in_file):
        raise GolemConfigError("File not found: %r" % in_file)

    with open(in_file, "r") as f:
        lines = f.readlines()

    with open(out_file, "w") as f:
        for line in lines:
            f.write(line)

def setup_env():
    env = os.environ.copy()
    if "PATH" in env:
        env["PATH"] = f"{BIN_DIR}:{env['PATH']}"
    else:
        env["PATH"] = BIN_DIR
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{LIB_DIR}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = LIB_DIR
    return env


def combinations(map):
    """
    This iterator lists all combinations of possible
    values for the elements of map.

    PARAMETER
       map -- a dictionary {key1: [value1_1, value1_2, ...], ...}

    RESULT
       yields all combinations as dictionaries {key1: value1_i, ...}
    """

    def rec_combinations(keys, map):
        if len(keys) == 0:
            yield {}
        else:
            key = keys[0]
            for new_map in rec_combinations(keys[1:], map):
                for heli in map[key]:
                    result = new_map.copy()
                    result[key] = heli
                    yield result

    for c in rec_combinations(list(map.keys()), map):
        yield c


def enumerate_helicities(conf):
    """ """
    zeroes = getZeroes(conf)
    in_particles, out_particles = generate_particle_lists(conf)
    fermion_filter = golem.algorithms.helicity.generate_symmetry_filter(conf, zeroes, in_particles, out_particles)

    in_particles.extend(out_particles)

    helic = {}
    for i in range(len(in_particles)):
        helic[i] = in_particles[i].getHelicityStates(zeroes)

    helicity_comb = [h for h in combinations(helic)]
    user_helis = conf.getProperty(golem.properties.helicities)
    user_helis = [i for i in user_helis if i]

    if len(user_helis) > 0:
        ex_user_helis = expand_helicities(user_helis)

        new_helicity_comb = []
        for s in ex_user_helis:
            heli = golem.algorithms.helicity.parse_helicity(s)
            if heli in helicity_comb:
                new_helicity_comb.append(heli)
            else:
                raise golem.util.parser.TemplateError("Helicity %r is not valid for this process" % s)
        helicity_comb = new_helicity_comb

    for h in helicity_comb:
        if fermion_filter(h):
            yield h


def enumerate_and_reduce_helicities(conf):
    in_particles, out_particles = generate_particle_lists(conf)
    conf = golem.algorithms.helicity.filter_helicities(conf, in_particles, out_particles)
    helicities = [h for h in enumerate_helicities(conf)]
    group = golem.algorithms.helicity.find_gauge_invariant_symmetry_group(helicities, conf, in_particles, out_particles)
    return group


def expand_helicities(patterns):
    anti = {"+": "-", "0": "0", "-": "+", "m": "k", "k": "m"}

    solutions = []
    while patterns:
        pat = patterns[0]
        patterns = patterns[1:]

        if "[" in pat:
            idx1 = pat.index("[")
            idx2 = pat.index("]")
            head = pat[:idx1]
            tail = pat[idx2 + 1 :]
            chars = pat[idx1 + 1 : idx2]
            if "=" in chars:
                eqidx = chars.index("=")
                if eqidx == 1:
                    symbol = chars[0]
                    asymbol = " "
                elif eqidx == 2:
                    symbol = chars[0]
                    asymbol = chars[1]
                chars = chars[eqidx + 1 :]
            else:
                symbol = "%"
                asymbol = "~"

            for c in chars:
                ac = anti[c]
                patterns = [
                    head.replace(symbol, c).replace(asymbol, ac) + c + tail.replace(symbol, c).replace(asymbol, ac)
                ] + patterns
        else:
            solutions.append(pat)
    return solutions


def encode_helicity(h, sym=golem.algorithms.helicity.heli_to_symbol):
    return dict([(k, sym[v]) for k, v in list(h.items())])


def prepare_model_files(conf, output_path=None):
    if output_path is None:
        path = process_path(conf)
    else:
        path = output_path

    model_lst = conf.getProperty(golem.properties.model)

    # For BLHA2 standards: conversion to GoSam internal keywords of SM:
    if len(model_lst) == 1 and str(model_lst[0]).lower() == "smdiag":
        model_lst[0] = "smdiag"
        conf.setProperty("model", "smdiag")
    if len(model_lst) == 1 and str(model_lst[0]).lower() == "smnondiag":
        model_lst[0] = "sm"
        conf.setProperty("model", "sm")

    # Some options only work with ufo models.
    # For OLP mode: check if property is set already.
    if conf["is_ufo"] is not None:
        isufo = conf["is_ufo"]
    else:
        isufo = False
        conf["is_ufo"] = isufo

    conf["enable_truncation_orders"] = conf.getProperty(golem.properties.enable_truncation_orders)

    if "setup-file" in conf:
        rel_path = os.path.dirname(conf["setup-file"])
    else:
        rel_path = os.getcwd()
    if len(model_lst) == 0:
        model_lst = ["sm"]
        conf.setProperty("model", "sm")
    if len(model_lst) == 1:
        model = model_lst[0]
        src_path = golem_path("models")
        # check for local file
        if os.path.sep in model and all(
            [os.path.exists(os.path.join(rel_path, model + ext)) for ext in ["", ".py", ".hh"]]
        ):
            src_path = rel_path
        for ext in ["", ".py", ".hh"]:
            copy_file(os.path.join(src_path, model + ext), os.path.join(path, MODEL_LOCAL + ext))
    elif len(model_lst) == 2:
        if model_lst[0].lower().strip() == "feynrules":
            isufo = True
            conf["is_ufo"] = isufo
            model_path = model_lst[1]
            model_path = os.path.expandvars(model_path)
            model_path = os.path.expanduser(model_path)
            if not os.path.isabs(model_path):
                model_path = os.path.join(rel_path, model_path)
            logger.info("Importing FeynRules model files ...")
            extract_model_options(conf)
            mdl = golem.model.feynrules.Model(model_path, golem.model.MODEL_OPTIONS)
            order_names = sorted(conf.getProperty(golem.properties.order_names))
            if order_names == [""]:
                order_names = []
            mdl.store(path, MODEL_LOCAL, order_names)
            logger.info("Done with model import.")
        else:
            model_path = model_lst[0]
            model_path = os.path.expandvars(model_path)
            model_path = os.path.expanduser(model_path)
            if not os.path.isabs(model_path):
                model_path = os.path.join(rel_path, model_path)
            model_name = model_lst[1]
            if model_name.isdigit():
                # This is a CalcHEP model, needs to be converted.
                logger.info("Importing CalcHep model files ...")
                mdl = golem.model.calchep.Model(model_path, int(model_name))
                mdl.store(path, MODEL_LOCAL)
                logger.info("Done with model import.")
            else:
                model = model_lst[1]
                for ext in ["", ".py", ".hh"]:
                    copy_file(os.path.join(model_path, model + ext), os.path.join(path, MODEL_LOCAL + ext))
    else:
        logger.critical("Parameter 'model' cannot have more than two entries.")
        sys.exit("GoSam terminated due to an error")


def extract_model_options(conf):
    for opt in conf.getListProperty(golem.properties.model_options):
        idx = -1
        for delim in [" ", ":", "="]:
            if delim in opt:
                didx = opt.index(delim)
                if idx < 0 or didx < idx:
                    idx = didx
        if idx >= 0:
            golem.model.MODEL_OPTIONS[opt[:idx].strip()] = opt[idx + 1 :].strip()
        else:
            golem.model.MODEL_OPTIONS[opt.strip()] = True


def getModel(conf, extra_path=None):
    MODEL_LOCAL = "model"

    if "model" in conf.cache:
        return conf.cache["model"]

    if extra_path is not None:
        path = extra_path
    else:
        path = process_path(conf)

    golem.model.MODEL_OPTIONS = {}
    golem.model.MODEL_ONES = conf.getListProperty(golem.properties.one)

    model_shortname = conf["model"]

    extract_model_options(conf)

    fname = os.path.join(path, "%s.py" % MODEL_LOCAL)
    logger.debug("Loading model file %r" % fname)

    # --[ EW scheme management:

    # Check if there is a line with "#@modelproperty: supports ewchoose"
    # before the first line of code.

    ew_supp = False
    with open(fname, "r") as modelfile:
        for line in modelfile:
            stripped_line = line.strip()
            if stripped_line != "" and not stripped_line.startswith("#"):
                # "#@modelproperty: supports ewchoose" not found
                logger.debug(
                    'Model seems to not support "ewchoose".\n'
                    + "If it does, add the line\n"
                    + '"#@modelproperty: supports ewchoose" to\n'
                    + "the top of %s." % fname
                )
                break
            elif stripped_line == "#@modelproperty: supports ewchoose":
                logger.debug('Model supports "ewchoose".')
                ew_supp = True
                break
            # else: pass

    # Adapt EW scheme to order file request:
    if conf["olp.ewscheme"] is not None and ew_supp == True:
        select_olp_EWScheme(conf)
    elif ew_supp == True and ((conf["model.options"] is None) or "ewchoose" in conf["model.options"]):
        golem.model.MODEL_OPTIONS["ewchoose"] = True
    elif conf["olp.ewscheme"] is not None and ew_supp == False:
        logger.critical("EWScheme tag in orderfile incompatible with model.")
        sys.exit("GoSam terminated due to an error")

    # Modify EW setting for model file:
    if ew_supp and "ewchoose" in list(golem.model.MODEL_OPTIONS.keys()):
        if golem.model.MODEL_OPTIONS["ewchoose"] == True:
            golem.model.MODEL_OPTIONS["users_choice"] = "0"
        else:
            golem.model.MODEL_OPTIONS["users_choice"] = golem.model.MODEL_OPTIONS["ewchoose"]
            golem.model.MODEL_OPTIONS["ewchoose"] = True
    elif ew_supp and "ewchoose" not in list(golem.model.MODEL_OPTIONS.keys()):
        golem.model.MODEL_OPTIONS["ewchoose"] = False
        golem.model.MODEL_OPTIONS["users_choice"] = "0"
    elif ew_supp == False and "ewchoose" in list(golem.model.MODEL_OPTIONS.keys()):
        del golem.model.MODEL_OPTIONS["ewchoose"]
        # error("ewchoose option in model.options is not supported with the chosen model.")

    # --] EW scheme management

    mod = load_source("model", fname)
    conf.cache["model"] = mod
    return mod


def select_olp_EWScheme(conf):
    ewparameters = ["mW", "mZ", "alpha", "GF", "sw", "e", "vev", "ewchoose"]
    ewscheme = conf["olp.ewscheme"]
    raisewarn = False
    for key, value in list(golem.model.MODEL_OPTIONS.items()):
        if any(item.startswith(str(key)) for item in ewparameters):
            raisewarn = True
    #  possible values are: alphaGF, alpha0, alphaMZ, alphaRUN, alphaMSbar, OLPDefined
    if ewscheme == "alphaGF":
        golem.model.MODEL_OPTIONS["ewchoose"] = "1"
        print("OLP EWScheme --> alphaGF (Gmu scheme)")

    if ewscheme == "alpha0":
        golem.model.MODEL_OPTIONS["ewchoose"] = "2"
        golem.model.MODEL_OPTIONS["alpha"] = "0.007297352536480967"
        print("OLP EWScheme --> alpha0")

    if ewscheme == "alphaMZ":
        golem.model.MODEL_OPTIONS["ewchoose"] = "2"
        # Value of alpha(Mz)^-1=128.944 from Nucl.Phys.Proc.Suppl. 225-227 (2012) 282-287
        golem.model.MODEL_OPTIONS["alpha"] = "0.007755305"
        print("OLP EWScheme --> alphaMZ")

    if ewscheme == "alphaRUN":
        print("OLP EWScheme --> alphaRUN")
        print("EW not supported yet!")
    if ewscheme == "alphaMSbar":
        print("OLP EWScheme --> alphaMSbar")
        print("EW not supported yet!")
    if ewscheme == "OLPDefined":
        print("OLP EWScheme --> OLPDefined: GoSam default taken")
        golem.model.MODEL_OPTIONS["ewchoose"] = 2

    if raisewarn == True:
        logger.warning(
            "EWScheme setting from orderfile will override the model.options\n"
            + " setting from input card if incompatible!"
        )
    # print golem.model.MODEL_OPTIONS
    return


def expand_parameter_list(prop, conf):
    params = generate_parameter_list(conf)
    lst = conf.getProperty(prop, default=None)
    if lst is None:
        return

    new_values = set([])
    for value in lst:
        if not value:
            continue
        if "*" in value:
            pat = value.replace("*", r"(\w*)") + "$"
            cpat = re.compile(pat)
            count = 0
            for param in params:
                if cpat.match(param):
                    count += 1
                    new_values.add(param)
            if count == 0:
                logger.warning("No known parameters match '%s' in property '%s'." % (value, prop))
        elif value in params:
            new_values.add(value)
        else:
            logger.warning(
                "Property '%s' contains an unknown parameter name (%s)\n" % (prop, value)
                + "The symbol has been removed from the list."
            )
    conf.setProperty(prop, list(new_values))


def generate_parameter_list(conf):
    model = getModel(conf)
    result = list(model.types.keys())

    if conf["__GAUGE_CHECK__"]:
        in_p, out_p = generate_particle_lists(conf)

        idx = 0
        for p in in_p:
            idx += 1
            twospin = abs(p.getSpin())
            if twospin == 2:
                result.append("gauge%dz" % idx)
        for p in out_p:
            idx += 1
            twospin = abs(p.getSpin())
            if twospin == 2:
                result.append("gauge%dz" % idx)

    return result


def generate_particle_lists(conf):
    """
    Generates a three-tuple of the form
       (in_particles, out_particles)
    where
       in_particles is the list of incoming particles.
       out_particles is the list of outgoing particles.
    """

    if "particle_lists" in conf.cache:
        inp, outp = conf.cache["particle_lists"]
        return inp[:], outp[:]

    ini = conf.getProperty(golem.properties.qgraf_in)
    fin = conf.getProperty(golem.properties.qgraf_out)

    mod = getModel(conf)

    in_particles = []
    for p in ini:
        particle = interpret_particle_name(p, mod)
        in_particles.append(particle)

    out_particles = []
    for p in fin:
        particle = interpret_particle_name(p, mod)
        out_particles.append(particle)

    conf.cache["particle_lists"] = (in_particles, out_particles)

    return (in_particles[:], out_particles[:])


__latex_particle_warnings__ = []


def interpret_particle_name(p, mod):
    """
    Translates a particle names into objects.
    """
    name = p.strip()
    if p in mod.particles:
        result = mod.particles[name]
    elif p in mod.mnemonics:
        result = mod.mnemonics[name]
        name = str(result)
    else:
        found = False
        try:
            pdg_code = int(name)
            for pname, p in list(mod.particles.items()):
                if p.getPDGCode() == pdg_code:
                    name = pname
                    result = p
                    found = True
                    break
        except ValueError:
            pass
        if not found:
            raise GolemConfigError("Unknown particle: %r" % name)

    if name in mod.latex_names:
        result.setLaTeXName(mod.latex_names[name])
    else:
        if name not in __latex_particle_warnings__:
            __latex_particle_warnings__.append(name)
            logger.warning("No LaTeX name for particle %r found." % name)

    return result


def diagram_count(path, suffix):
    """
    Analyzes the file diagrams-<suffix>.hh to
    infer the total number of diagrams in a
    process at the given loop order.

    PARAMETER

       path -- the path pointing to the file which contains
               the diagrams.
       suffix -- index which denotes the part of the amplitude


    This function looks for a line starting with
     '#define DIAGRAMCOUNT' and interprets the argument as the
     number of diagrams.
    """
    fname = os.path.join(path, "diagrams-%s.hh" % suffix)
    result = 0
    if os.path.exists(fname):
        with open(fname, "r") as f:
            for line in f:
                if line.strip().startswith("#define DIAGRAMCOUNT"):
                    words = line.strip().split()
                    result = int(words[2].strip('"'))
                    break
    else:
        pass
        # print "Warning: File %r not found." % fname
    return result


def process_path(conf):
    setup_file = conf.getProperty("setup-file")
    setup_dir = os.path.dirname(setup_file)
    setup_dir = os.path.abspath(setup_dir)

    path = conf.getProperty(golem.properties.process_path)
    if path is None:
        logger.critical("Property %r must be set in %r!" % (str(golem.properties.process_path), setup_file))
        sys.exit("GoSam terminated due to an error")
    path = os.path.expandvars(path)
    if os.path.isabs(path):
        return path
    else:
        return os.path.join(setup_dir, path)


def banner(WIDTH=70, PREFIX="#", SUFFIX="#"):
    authors = golem.util.constants.AUTHORS
    former_authors = golem.util.constants.FORMER_AUTHORS
    asciiart = golem.util.constants.ASCIIART
    asciiwidth = max(list(map(len, asciiart)))
    clines = golem.util.constants.CLINES

    llines = ["AUTHORS:"]

    lauthor = max(list(map(len, list(authors.keys()))))
    author_format = "* %" + str(-lauthor) + "s"
    for author in sorted(list(authors.keys()), key=lambda n: n.rsplit(" ", 1)[-1]):
        values = authors[author]
        if len(values) >= 1 and len(values[0]) > 0:
            email = " <" + values[0] + ">"
        else:
            email = ""

        llines.append((author_format % author) + email)

    llines.append("")
    llines.append("FORMER AUTHORS:")
    for author in sorted(list(former_authors.keys()), key=lambda n: n.rsplit(" ", 1)[-1]):
        values = former_authors[author]
        if len(values) >= 1 and len(values[0]) > 0:
            email = " <" + values[0] + ">"
        else:
            email = ""

        llines.append((author_format % author) + email)
    maxauthorlen = max(list(map(len, llines)))

    cl = WIDTH - len(PREFIX) - len(SUFFIX) - 1 - asciiwidth
    for lnr, line in enumerate(clines):
        if lnr < len(asciiart):
            asciiline = asciiart[lnr]
        else:
            asciiline = " " * asciiwidth
        outl = asciiline + line.center(cl)
        ll = len(outl) + 2
        if ll < WIDTH:
            yield PREFIX + " " + outl + (WIDTH - ll - 1) * " " + SUFFIX
        else:
            yield PREFIX + " " + outl

    asciiline = " " * max(0, WIDTH - maxauthorlen - 7)

    for lnr, line in enumerate(llines):
        outl = asciiline + line
        ll = len(outl) + len(PREFIX) + len(SUFFIX)
        if ll < WIDTH:
            yield PREFIX + " " + outl + (WIDTH - ll - 1) * " " + SUFFIX
        else:
            yield PREFIX + " " + outl

    for line in golem.util.constants.LICENSE:
        ll = len(line) + len(PREFIX) + len(SUFFIX)
        if ll < WIDTH:
            ws = " " * (WIDTH - ll)
        else:
            ws = ""
        yield PREFIX + line + ws + SUFFIX


class LimitedWidthOutputStream:
    def __init__(self, out, width, indent=0):
        self._out = out
        self._width = width
        self._indent = indent
        self._pos = indent

    def write(self, token):
        advance = len(str(token))
        if advance + self._pos > self._width:
            self._out.write("\n" + " " * self._indent)
            self._pos = self._indent
        self._out.write(str(token))
        self._pos += advance

    def nl(self):
        self._out.write("\n" + " " * self._indent)
        self._pos = self._indent


def getZeroes(conf):
    model_mod = getModel(conf)
    zeroes = list([_f for _f in conf.getListProperty(golem.properties.zero) if _f])
    for name, value in list(model_mod.parameters.items()):
        if name in zeroes:
            continue
        t = model_mod.types[name]
        if t == "RP":
            if float(value) == 0.0:
                zeroes.append(name)
        elif t == "CP":
            if all(map(float, value)) == 0.0:
                zeroes.append(name)
    return zeroes


def getOnes(conf):
    model_mod = getModel(conf)
    ones = list([_f for _f in conf.getListProperty(golem.properties.one) if _f])
    for name, value in list(model_mod.parameters.items()):
        if name in ones:
            continue
        t = model_mod.types[name]
        if t == "RP":
            if float(value) == 1.0:
                ones.append(name)
        elif t == "CP":
            if float(value[0]) == 1.0 and float(value[1]) == 0.0:
                ones.append(name)
    return ones


def product(lst):
    r = 1
    for i in lst:
        r *= i
    return r


def factorial(n):
    return product(list(range(2, n + 1)))


def derive_coupling_names(conf):
    """
    For a given configuration try to find out how the QCD and the QED
    couplings are called and if they are set to one.
    """

    result = {}

    candidates = {"QCD": ["gs", "mdlG", "mdlGG", "mdlGS"], "QED": ["e", "mdlee", "mdlEE", "mdlE"]}

    model = getModel(conf)
    symbols = list(model.types.keys())
    ones = getOnes(conf)
    zeroes = getZeroes(conf)

    for t, lst in list(candidates.items()):
        flag = False
        for c in lst:
            if c in symbols:
                if c in ones:
                    result[t] = "1"
                elif c in zeroes:
                    result[t] = "0"
                else:
                    result[t] = c
                flag = True
                break
        if not flag:
            result[t] = "0"
    return result


def load_source(mname, mpath):
    if sys.version_info >= (
        3,
        6,
    ):
        # see https://docs.python.org/dev/whatsnew/3.12.html#imp
        import importlib.util
        import importlib.machinery

        loader = importlib.machinery.SourceFileLoader(mname, mpath)
        spec = importlib.util.spec_from_file_location(mname, mpath, loader=loader)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mname] = mod
        loader.exec_module(mod)
    else:
        import imp

        mod = imp.load_source(mname, mpath)
    return mod
