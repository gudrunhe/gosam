# vim: syntax=python:ts=3:sw=3

import sys
import os
import os.path

import golem.util.main_qgraf
from golem.util.path import golem_path
from golem.util.tools import getModel, load_source

import logging

logger = logging.getLogger(__name__)


def convert_to_digits(number, digits):
    v = abs(number)
    r = len(digits)

    if r <= 1:
        return str(number)

    result = ""

    while v > 0:
        result = digits[v % r] + result
        v = v // r

    if number < 0:
        result = "-" + result

    if len(result) == "":
        result = digits[0]

    return result


def pyxodraw(*args, **opts):
    if "conf" in opts:
        conf = opts["conf"]
    else:
        conf = None

    for arg in args:
        arg_path = os.path.dirname(os.path.abspath(arg))
        if arg_path not in sys.path:
            sys.path.append(arg_path)

        short_name = os.path.split(arg)[-1]
        base_name = short_name[: short_name.rindex(".")]
        logger.debug("Pyxodraw is trying to load module %r\n" % base_name + "from directory: %r" % arg_path)
        mod = load_source(base_name, arg)

        model_name = mod.__model_name__
        diagrams = {}
        mod.get_diagrams(diagrams)

        if conf is None:
            model_mod = load_source(model_name, os.path.join(arg_path, "%s.py" % golem.util.main_qgraf.MODEL_LOCAL))
        else:
            model_mod = getModel(conf, arg_path)

        latex_names = model_mod.latex_names

        f = open(os.path.join(arg_path, base_name + ".tex"), "w")

        opts = {
            "gdashsize": 3,
            "sdashsize": 5,
            "gamplitude": 3,
            "windings": 0.2,
            "pamplitude": 3,
            "wiggles": 0.2,
            "vsize": 3,
            "height": 100,
            "width": 120,
        }

        BOUNDARY = "NEXT DIAGRAM"

        f.write("Diagrams generated by PyxoDraw\n\n")
        f.write("You will need the LaTeX package AxoDraw for drawing.\n")
        f.write("\n\nboundary=%s\n\n" % BOUNDARY)
        for idx, diag in list(diagrams.items()):
            f.write("--%s name=diagram%d\n" % (BOUNDARY, idx))
            f.write("%% Diagram %d:\n" % idx)

            diag.layout(**opts)
            diag.draw(f, lookup=model_mod.line_styles, latex=latex_names, **opts)
        f.write("--%s--\n" % BOUNDARY)
        f.close()


if __name__ == "__main__":
    print("This is PyxoDraw")
    pyxodraw(*sys.argv[1:])
