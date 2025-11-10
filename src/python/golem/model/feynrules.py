# vim: ts=3:sw=3
"""
This module allows to import model definitions from FeynRules using the
Python interface.
"""
import sys
import os
import os.path
import sys
import copy
import re
import itertools

import golem.model
import golem.model.expressions as ex
from golem.topolopy.objects import Vertex

from golem.util.tools import LimitedWidthOutputStream, load_source

import logging

import feyngraph as fg

logger = logging.getLogger(__name__)

LINE_STYLES = {
    "straight": "fermion",
    "wavy": "photon",
    "curly": "gluon",
    "dashed": "scalar",
    "dotted": "ghost",
    "swavy": "majorana",
    "scurly": "majorana",
}


sym_cmath = ex.SymbolExpression("cmath")
sym_exp = ex.SymbolExpression("exp")
sym_log = ex.SymbolExpression("log")
sym_sqrt = ex.SymbolExpression("sqrt")
sym_sin = ex.SymbolExpression("sin")
sym_cos = ex.SymbolExpression("cos")
sym_tan = ex.SymbolExpression("tan")
sym_asin = ex.SymbolExpression("asin")
sym_acos = ex.SymbolExpression("acos")
sym_atan = ex.SymbolExpression("atan")
sym_sinh = ex.SymbolExpression("sinh")
sym_cosh = ex.SymbolExpression("cosh")
sym_tanh = ex.SymbolExpression("tanh")
sym_asinh = ex.SymbolExpression("asinh")
sym_acosh = ex.SymbolExpression("acosh")
sym_atanh = ex.SymbolExpression("atanh")
sym_pi = ex.SymbolExpression("pi")
sym_e = ex.SymbolExpression("e")

sym_re = ex.SpecialExpression("re")
sym_im = ex.SpecialExpression("im")
sym_sec = ex.SpecialExpression("sec")
sym_csc = ex.SpecialExpression("csc")
sym_asec = ex.SpecialExpression("asec")
sym_acsc = ex.SpecialExpression("acsc")
sym_conjg = ex.SpecialExpression("complexconjugate")
sym_cmplx = ex.SpecialExpression("complex")
sym_abs = ex.SpecialExpression("abs")

sym_Nf = ex.SpecialExpression("Nf")
sym_Nfgen = ex.SpecialExpression("Nfgen")
sym_Nfrat = ex.SpecialExpression("Nfrat")
sym_NC = ex.SpecialExpression("NC")
sym_if = ex.SpecialExpression("if")

i_ = ex.SpecialExpression("i_")
abs_ = ex.SpecialExpression("abs_")

cmath_functions = [
    sym_exp,
    sym_log,
    sym_sqrt,
    sym_sin,
    sym_cos,
    sym_tan,
    sym_asin,
    sym_acos,
    sym_atan,
    sym_sinh,
    sym_cosh,
    sym_tanh,
    sym_asinh,
    sym_acosh,
    sym_atanh,
    sym_pi,
    sym_e,
]

shortcut_functions = [sym_re, sym_im, sym_sec, sym_csc, sym_asec, sym_acsc, sym_conjg, sym_cmplx, sym_if, sym_abs]

unprefixed_symbols = [sym_Nf, sym_Nfgen, sym_Nfrat]


class Model:
    def __init__(self, model_path, model_options=None):
        self.model_options = model_options or dict()

        sys.path.append(model_path)
        parent_path = os.path.normpath(os.path.join(model_path, os.pardir))
        norm_path = os.path.normpath(model_path)
        if norm_path.startswith(parent_path):
            mname = norm_path[len(parent_path) :].replace(os.sep, "")
        else:
            mname = os.path.basename(model_path.rstrip(os.sep + (os.altsep if os.altsep else "")))
        if os.altsep is not None:
            mname = mname.replace(os.altsep, "")
        search_path = [parent_path]

        logger.info("Trying to import FeynRules model '%s' from %s" % (mname, search_path[0]))
        mod = load_ufo_files(mname, search_path)

        self.all_particles = mod.all_particles
        self.all_couplings = mod.all_couplings
        self.all_parameters = mod.all_parameters
        self.all_vertices = mod.all_vertices
        self.all_lorentz = mod.all_lorentz
        self.model_orig = model_path
        self.model_name = mname
        self.prefix = "mdl"
        self.floats = []
        self.floatsd = {}
        self.floatsc = []

        self.orders = set()
        for c in self.all_couplings:
            self.orders.update(list(c.order.keys()))

        parser = ex.ExpressionParser()
        ex.ExpressionParser.simple = ex.ExpressionParser.simple_old
        for l in self.all_lorentz:
            structure = parser.compile(l.structure)
            l.rank = get_rank(structure)

        self.useCT = False
        try:
            self.all_CTvertices = mod.all_CTvertices
            self.useCT = True
        except AttributeError:
            pass

        try:
            self.all_CTparameters = mod.all_CTparameters
        except AttributeError:
            if self.useCT:
                logger.critical("UFO model '%s' has CT_vertices but no CT_parameters!" % self.model_name)
                sys.exit("GoSam terminated due to an error")
            else:
                pass

        fg_model = fg.Model.from_ufo(model_path)

        # ################################################
        # Apply the vertex splitting of FeynGraph to self
        # ################################################
        new_vertices = []
        obsolete_vertices = []
        for i, v in enumerate(self.all_vertices):
            if (splitting := fg_model.splitting(v.name)) is not None:
                obsolete_vertices.append(i)
                for name, couplings in splitting.items():
                    newv = copy.deepcopy(v)
                    newv.name = name
                    newv.color = list(set(v.color[c] for c, _ in couplings))
                    newv.lorentz = list(set(v.lorentz[l] for _, l in couplings))
                    newv.couplings = {
                        (newv.color.index(v.color[c[0]]), newv.lorentz.index(v.lorentz[c[1]])): v.couplings[c]
                        for c in couplings
                    }
                    new_vertices.append(newv)
        for i in sorted(obsolete_vertices, reverse=True):
            self.all_vertices.pop(i)
        self.all_vertices.extend(new_vertices)

        if self.useCT:
            new_vertices = []
            obsolete_vertices = []
            for i, v in enumerate(self.all_CTvertices):
                if (splitting := fg_model.splitting(v.name)) is not None:
                    obsolete_vertices.append(i)
                    for name, couplings in splitting.items():
                        newv = copy.deepcopy(v)
                        newv.name = name
                        newv.color = list(set(v.color[c] for c, _ in couplings))
                        newv.lorentz = list(set(v.lorentz[l] for _, l in couplings))
                        newv.couplings = {
                            (newv.color.index(v.color[c[0]]), newv.lorentz.index(v.lorentz[c[1]])): v.couplings[c]
                            for c in couplings
                        }
                        new_vertices.append(newv)
            for i in sorted(obsolete_vertices, reverse=True):
                self.all_CTvertices.pop(i)
            self.all_CTvertices.extend(new_vertices)

        # ################################################################################
        # Add rank as coupling order to FeynGraph vertices and split vertices if necessary
        # ################################################################################
        new_vertices = []
        new_ct_vertices = []
        obsolete_vertices = []
        for v_index, ufo_vert in enumerate(self.all_vertices + self.all_CTvertices if self.useCT else self.all_vertices):
            ranks = set(ufo_vert.lorentz[l].rank for _, l, *_ in ufo_vert.couplings.keys())
            if len(ranks) > 1:
                logger.info(
                    "Ambiguous rank for vertex {}, splitting into {} vertices '{}_0' .. '{}_{}'".format(
                    ufo_vert.name,
                    len(ranks),
                    ufo_vert.name,
                    ufo_vert.name,
                    len(ranks) - 1
                ))
                fg_model.split_vertex(ufo_vert.name, [f"{ufo_vert.name}_{i}" for i in range(len(ranks))])
                for i, unique_rank in enumerate(ranks):
                    lorentz_indices = [i for i, l in enumerate(ufo_vert.lorentz) if l.rank == unique_rank]
                    newv = copy.deepcopy(ufo_vert)
                    newv.name = f"{ufo_vert.name}_{i}"
                    newv.lorentz = [ufo_vert.lorentz[j] for j in lorentz_indices]
                    newv.couplings = {
                        (c, newv.lorentz.index(ufo_vert.lorentz[l])): v
                        for (c, l), v in ufo_vert.couplings.items() if ufo_vert.lorentz[l].rank == unique_rank
                    }
                    newv.rank = {unique_rank}
                    fg_model.add_coupling(newv.name, "RK", unique_rank)
                    if hasattr(ufo_vert, "type"):
                        new_ct_vertices.append(newv)
                    else:
                        new_vertices.append(newv)
                obsolete_vertices.append(v_index)
            else:
                rank = ranks.pop()
                fg_model.add_coupling(ufo_vert.name, "RK", rank)
                ufo_vert.rank = {rank}
        for i in sorted(obsolete_vertices, reverse=True):
            if i <= len(self.all_vertices):
                self.all_vertices.pop(i)
            else:
                self.all_CTvertices.pop(i)
        self.all_vertices.extend(new_vertices)
        if self.useCT:
            self.all_CTvertices.extend(new_ct_vertices)

        # ######################################################################
        # Let FeynGraph merge the equivalent vertices and apply the same to self
        # ######################################################################
        mergings = fg_model.merge_vertices()

        new_vertices = []
        new_ct_vertices = []
        obsolete_vertices = []
        obsolete_ct_vertices = []
        k = 1
        for merged, original in mergings.items():
            logger.info(
                (
                    f"Vertices {original} have same external legs, coupling orders and spin map. Merging them internally into: {merged}."
                )
            )
            indices = [i for i, v in enumerate(self.all_vertices) if v.name in original]
            if len(indices) != 0:
                color = list(set([c for i in indices for c in self.all_vertices[i].color]))
                lorentz = list(set(l for i in indices for l in self.all_vertices[i].lorentz))
                couplings = {}
                for i in indices:
                    current_couplings =  {(
                             color.index(self.all_vertices[i].color[c]),
                             lorentz.index(self.all_vertices[i].lorentz[l])
                        ): value for (c, l), value in self.all_vertices[i].couplings.items()
                    }
                    for coord, coupling in current_couplings.items():
                        if coord in couplings:
                            couplings[coord].append(coupling)
                        else:
                            couplings[coord] = [coupling]
                # Merge couplings where necessary
                for coord, coupling_list in couplings.items():
                    if len(coupling_list) == 1:
                        couplings[coord] = coupling_list[0]
                    else:
                        newcoupling = copy.deepcopy(coupling_list[0])
                        newcoupling.name = f"GC_M_{k}"
                        newcoupling.value = "+".join(f"({c.value})" for c in coupling_list)
                        self.all_couplings.append(newcoupling)
                        couplings[coord] = newcoupling
                        k += 1
                # Create new, merged vertex
                newv = copy.deepcopy(self.all_vertices[indices[0]])
                newv.name = merged
                newv.color = color
                newv.lorentz = lorentz
                newv.couplings = couplings
                obsolete_vertices.extend(indices)
                new_vertices.append(newv)
            else:
                indices = [i for i, v in enumerate(self.all_CTvertices) if v.name in original]
                color = list(set([c for i in indices for c in self.all_CTvertices[i].color]))
                lorentz = list(set(l for i in indices for l in self.all_CTvertices[i].lorentz))
                couplings = {}
                for i in indices:
                    current_couplings = {(
                                             color.index(self.all_CTvertices[i].color[c]),
                                             lorentz.index(self.all_CTvertices[i].lorentz[l])
                                         ): value for (c, l), value in self.all_CTvertices[i].couplings.items()
                                         }
                    for coord, coupling in current_couplings.items():
                        if coord in couplings:
                            couplings[coord].append(coupling)
                        else:
                            couplings[coord] = [coupling]
                # Merge couplings where necessary
                for coord, coupling_list in couplings.items():
                    if len(coupling_list) == 1:
                        couplings[coord] = coupling_list[0]
                    else:
                        newcoupling = copy.deepcopy(coupling_list[0])
                        newcoupling.name = f"CTGC_M_{k}"
                        newcoupling.value = "+".join(f"({c.value})" for c in coupling_list)
                        self.all_couplings.append(newcoupling)
                        couplings[coord] = newcoupling
                        k += 1
                newv = copy.deepcopy(self.all_CTvertices[indices[0]])
                newv.name = merged
                newv.color = color
                newv.lorentz = lorentz
                newv.couplings = couplings
                obsolete_ct_vertices.extend(indices)
                new_ct_vertices.append(newv)

        for i in sorted(obsolete_vertices, reverse=True):
            self.all_vertices.pop(i)
        self.all_vertices.extend(new_vertices)
        if self.useCT:
            for i in sorted(obsolete_ct_vertices, reverse=True):
                self.all_CTvertices.pop(i)
            self.all_CTvertices.extend(new_ct_vertices)

        if self.useCT:
            self.labels = {v.name: i for i, v in enumerate(self.all_vertices + self.all_CTvertices)}
        else:
            self.labels = {v.name: i for i, v in enumerate(self.all_vertices)}

        # the following code block splits all_couplings into
        # two separate lists of CT and non-CT couplings
        # also fills self.ctfunctions used write_python_file
        if self.useCT:
            self.all_CTcouplings = []
            self.ctfunctions = {}
            self.cttypes = {}
            for a in dir(mod.CT_vertices.C):
                b = getattr(mod.CT_vertices.C, a)
                if type(b).__name__ == "Coupling":
                    self.all_CTcouplings.append(b)
                    if b in self.all_couplings:
                        self.all_couplings.remove(b)
            # construct the CT dictionary representing the Laurent expansion
            for c in self.all_CTcouplings:
                name = self.prefix + c.name.replace("_", "")
                self.ctfunctions[name] = {}
                self.cttypes[name] = "C"
                if isinstance(c.value, dict):
                    # the value of the coupling is a dictionary representing the Laurent expansion
                    # => split const from log terms, if present
                    for ctpole in list(c.value.keys()):
                        ctcoeff = c.value[ctpole]
                        self.ctfunctions[name][ctpole] = ctcoeff
                elif isinstance(c.value, str):
                    # the value of the coupling is a string and the Laurent expansion is only evident after evaluating CTParameter type objects
                    CTparams = [
                        ctp for ctp in self.all_CTparameters if ctp.name in re.split(r"\(|\)|\+|\*|-|/", c.value)
                    ]
                    CTpoles = set()

                    for ctparam in CTparams:
                        CTpoles = CTpoles.union(set(ctparam.value.keys()))

                    for ctpole in CTpoles:
                        ctcoeff = c.value
                        for ctparam in CTparams:
                            if ctpole in ctparam.value:
                                ctcoeff = ctcoeff.replace(ctparam.name, ctparam.value[ctpole])
                        self.ctfunctions[name][ctpole] = ctcoeff
                else:
                    logger.critical("CT coupling %s is neither a dict nor str!" % c)
                    sys.exit("GoSam terminated due to an error")

        golem.model.feyngraph_model = fg_model
        golem.model.global_model = self

    def write_python_file(self, f):
        # Edit : GC- 16.11.12 now have the dictionaries
        # particlect and parameterct available
        # if non-empty the model.py file is modified
        f.write("# vim: ts=3:sw=3\n")
        f.write("# This file has been generated from the FeynRules model files\n")
        f.write("# in %s\n" % self.model_orig)
        f.write("from golem.model.particle import Particle\n")
        f.write("\nmodel_name = %r\n\n" % self.model_name)

        logger.info("      Generating particle list ...")
        f.write("particles = {")

        is_first = True

        mnemonics = {}
        latex_names = {}
        line_types = {}
        particlect = {}

        for p in self.all_particles:
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            try:
                particlect[p] = p.counterterm
            except AttributeError:
                pass
            pmass = str(p.mass)
            pwidth = str(p.width)

            pdg_code = p.pdg_code

            mnemonics[p.name] = p.name
            latex_names[p.name] = p.texname

            line_type = p.line.lower()
            # FIX- 15.08.12 GC # until FeynRules can accomodate charged scalars
            if line_type in LINE_STYLES:
                if (line_type == "dashed") and (abs(p.color) == 3):
                    line_types[p.name] = "chargedscalar"
                else:
                    line_types[p.name] = LINE_STYLES[line_type]
            else:
                line_types[p.name] = "scalar"

            if pmass == "0" or pmass == "ZERO":
                mass = 0
            else:
                mass = self.prefix + pmass

            spin = abs(p.spin) - 1
            if p.pdg_code < 0:
                spin = -spin

            if pwidth == "0" or pwidth == "ZERO":
                width = "0"
            else:
                width = self.prefix + pwidth

            f.write(
                "\t%r: Particle(%r, %d, %r, %d, %r, %r, %d, %r)"
                % (p.name, p.name, spin, mass, p.color, p.antiname, width, pdg_code, p.charge)
            )

        f.write("\n}\n\n")

        is_first = True
        f.write("mnemonics = {")
        for key, value in list(mnemonics.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")

            f.write("\t%r: particles[%r]" % (key, value))
        f.write("\n}\n\n")

        is_first = True
        f.write("latex_names = {")
        for key, value in list(latex_names.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")

            f.write("\t%r: %r" % (key, value))
        f.write("\n}\n\n")

        is_first = True
        f.write("line_styles = {")
        for key, value in list(line_types.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")

            f.write("\t%r: %r" % (key, value))
        f.write("\n}\n\n")

        parameters = {}
        functions = {}
        types = {}
        parameterct = {}
        slha_locations = {}
        for p in self.all_parameters:
            #  new: collect all the new counterterm pieces (if there are any)
            try:
                # use the name (p.name) or the object in the dictionary
                parameterct[p] = p.counterterm
            except AttributeError:
                pass
            name = self.prefix + p.name.replace("_", "undrscr")
            if p.nature == "external":
                parameters[name] = p.value
                slha_locations[name] = (p.lhablock, p.lhacode)
            elif p.nature == "internal":
                functions[name] = p.value
            else:
                logger.critical("Parameter's nature ('%s') not implemented." % p.nature)
                sys.exit("GoSam terminated due to an error")

            if p.type == "real":
                types[name] = "R"
            elif p.type == "complex":
                types[name] = "C"
            else:
                logger.critical("Parameter's type ('%s') not implemented." % p.type)
                sys.exit("GoSam terminated due to an error")
        parameters["NC"] = "3.0"
        types["NC"] = "R"
        parameters["Nf"] = "5.0"
        types["Nf"] = "R"
        parameters["Nfgen"] = "-1.0"
        types["Nfgen"] = "R"

        functions["Nfrat"] = "if(Nfgen,Nf/Nfgen,1)"
        types["Nfrat"] = "R"

        for key, value in list(self.model_options.items()):
            if key in parameters or self.prefix + key in parameters:
                if key in parameters:
                    real_key = key
                else:
                    real_key = self.prefix + key
                try:
                    sval = str(value)
                    fval = float(sval)
                    parameters[real_key] = sval
                except ValueError:
                    logger.warning("Model option %s=%r not in allowed range.\n" % (key, value) + "Option ignored")
        specials = {}
        for expr in shortcut_functions:
            specials[str(expr)] = expr
        for expr in unprefixed_symbols:
            specials[str(expr)] = expr

        parser = ex.ExpressionParser(**specials)

        for c in self.all_couplings:
            name = self.prefix + c.name.replace("_", "")
            functions[name] = c.value
            types[name] = "C"

        logger.info("      Generating function list ...")
        f.write("functions = {")
        fcounter = [0]
        fsubs = {}
        is_first = True
        for name, value in list(functions.items()):
            expr = parser.compile(value)
            for fn in cmath_functions:
                expr = expr.algsubs(ex.DotExpression(sym_cmath, fn), ex.SpecialExpression(str(fn)))
            expr = expr.prefixSymbolsWith(self.prefix)
            expr = expr.replaceFloats(self.prefix + "float", fsubs, fcounter)
            expr = expr.algsubs(sym_cmplx(ex.IntegerExpression(0), ex.IntegerExpression(1)), i_)
            expr = expr.algsubs(sym_abs, abs_)

            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            f.write("\t%r: " % name)
            f.write("'")
            expr.write(f)
            f.write("'")
        f.write("\n}\n\n")

        if self.useCT:
            types.update(self.cttypes)

            logger.info("      Generating counter term function list ...")
            f.write("ctfunctions = {")
            is_first = True
            for name, value in self.ctfunctions.items():
                if is_first:
                    is_first = False
                    f.write("\n")
                else:
                    f.write(",\n")
                f.write("\t%r: " % name)
                is_firstcf = True
                for pl, cf in value.items():
                    expr = parser.compile(cf)
                    for fn in cmath_functions:
                        expr = expr.algsubs(ex.DotExpression(sym_cmath, fn), ex.SpecialExpression(str(fn)))
                    expr = expr.prefixSymbolsWith(self.prefix)
                    expr = expr.replaceFloats(self.prefix + "float", fsubs, fcounter)
                    expr = expr.algsubs(sym_cmplx(ex.IntegerExpression(0), ex.IntegerExpression(1)), i_)
                    expr = expr.algsubs(sym_abs, abs_)

                    if is_firstcf:
                        is_firstcf = False
                        f.write("{\n")
                    else:
                        f.write(",\n")
                    f.write("\t\t%r: " % pl)
                    f.write("'")
                    expr.write(f)
                    f.write("'")
                f.write("\n\t}")
            f.write("\n}\n\n")

        # search for additional floats appearing in lorentz structures
        for l in self.all_lorentz:
            structure = parser.compile(l.structure)
            structure = structure.replaceFloats(self.prefix + "float", fsubs, fcounter)

        self.floats = list(fsubs.keys())
        self.floatsd = fsubs
        self.floatsc = fcounter

        f.write("parameters = {")
        is_first = True

        for name, value in list(fsubs.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            f.write("\t%r: %r" % (name, str(value)))

        for name, value in list(parameters.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            if isinstance(value, complex):
                f.write("\t%r: [%r, %r" % (name, str(value.real), str(value.imag)))
            else:
                f.write("\t%r: %r" % (name, str(value)))
        f.write("\n}\n\n")

        f.write("latex_parameters = {")
        is_first = True
        for p in self.all_parameters:
            name = self.prefix + p.name.replace("_", "undrscr")
            if is_first:
                is_first = False
            else:
                f.write(",")
            f.write("\n\t%r: %r" % (name, p.texname))
        f.write("\n}\n\n")

        f.write("types = {")
        is_first = True

        for name in list(fsubs.keys()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            f.write("\t%r: 'RP'" % name)

        for name, value in list(types.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            f.write("\t%r: %r" % (name, value))
        f.write("\n}\n\n")

        f.write("slha_locations = {")
        is_first = True

        for name, value in list(slha_locations.items()):
            if is_first:
                is_first = False
                f.write("\n")
            else:
                f.write(",\n")
            f.write("\t%r: %r" % (name, value))
        f.write("\n}\n\n")

        f.write("aux = {\n")
        for p in self.all_particles:
            aux = 0 if p.propagating else 1
            if hasattr(p, "CustomSpin2Prop"):
                if p.CustomSpin2Prop:
                    if not p.propagating:
                        logger.critical(f"Particle {p.name} with CustomSpin2Prop has to propagate.")
                        sys.exit("GoSam terminated due to an error")
                    aux = 2
            f.write(f"    '{p.name}': {aux},\n")
        f.write("}")

        # new for modified UFO files
        for p in particlect:
            print(p.counterterm)
        for p in parameterct:
            print(p.counterterm)

    def write_form_file(self, f, order_names):
        parser = ex.ExpressionParser()
        lorex = {}
        lsubs = {}
        lcounter = [0]
        dummy_found = {}
        for l in self.all_lorentz:
            name = l.name
            structure = parser.compile(l.structure)
            structure = structure.replaceStrings("ModelDummyIndex", lsubs, lcounter)
            structure = structure.replaceNegativeIndices(0, "MDLIndex%d", dummy_found)
            structure = structure.replaceFloats(self.prefix + "float", self.floatsd, self.floatsc)
            for i in [2]:
                structure = structure.algsubs(ex.FloatExpression("%d." % i), ex.IntegerExpression("%d" % i))
            lorex[name] = transform_lorentz(structure, l.spins)
        lwf = LimitedWidthOutputStream(f, 70, 6)
        f.write("* vim: syntax=form:ts=3:sw=3\n\n")
        f.write("* This file has been generated from the FeynRule model files\n")
        f.write("* in %s\n\n" % self.model_orig)

        f.write("*---#[ Symbol Definitions:\n")
        f.write("*---#[ Coupling Orders:\n")
        f.write("AutoDeclare Symbols RK")
        f.write(",isNP")
        f.write(",V")
        f.write(",CTV")
        f.write(";\n")
        f.write("Symbol XNPorder,XQLorder,Xkeep;")
        f.write("\n")
        f.write("*---#] Coupling Orders:\n")
        f.write("*---#[ Parameters:\n")

        params = []
        for p in self.all_parameters:
            params.append(self.prefix + p.name.replace("_", "undrscr"))

        for c in self.all_couplings:
            params.append(self.prefix + c.name.replace("_", ""))

        if len(params) > 0:
            if len(params) == 1:
                f.write("Symbol %s;" % params[0])
            else:
                f.write("Symbols")
                lwf.nl()
                lwf.write(params[0])
                for p in params[1:]:
                    lwf.write(",")
                    lwf.write(p)
                lwf.write(";")

        f.write("\n")

        if self.useCT:
            ctparams = [self.prefix + c.name.replace("_", "") for c in self.all_CTcouplings]
            if len(ctparams) > 0:
                if len(ctparams) == 1:
                    f.write("Symbol %s;" % ctparams[0] + "eftctcpl")
                else:
                    f.write("Symbols")
                    lwf.nl()
                    lwf.write(ctparams[0] + "eftctcpl")
                    for ctp in ctparams[1:]:
                        lwf.write(",")
                        lwf.write(ctp + "eftctcpl")
                    lwf.write(";")

            f.write("\n")

        if len(self.floats) == 1:
            f.write("Symbol %s;\n" % self.floats[0])
        elif len(self.floats) > 1:
            f.write("Symbols")
            lwf.nl()
            lwf.write(self.floats[0])
            for p in self.floats[1:]:
                lwf.write(",")
                lwf.write(p)
            lwf.write(";\n")

        f.write("AutoDeclare Indices ModelDummyIndex, MDLIndex;\n")
        f.write("*---#] Parameters:\n")
        if hasattr(self, "all_CTvertices"):
            max_deg = max([len(v.particles) for v in (self.all_vertices + self.all_CTvertices)])
        else:
            max_deg = max([len(v.particles) for v in self.all_vertices])
        f.write("*---#[ Auxilliary Symbols:\n")
        f.write("Vectors vec1, ..., vec%d;\n" % max_deg)
        f.write("*---#] Auxilliary Symbols:\n")
        f.write("*---#] Symbol Definitions:\n")
        if self.containsMajoranaFermions():
            f.write("* Model contains Majorana Fermions:\n")
            logger.debug("You are working with a model " + "that contains Majorana fermions.")
            f.write('#Define DISCARDQGRAFSIGN "1"\n')
        f.write('#Define USEVERTEXPROC "1"\n')
        f.write("*---#[ Procedure ReplaceVertices :\n")
        f.write("#Procedure ReplaceVertices\n")

        orders = set()
        orders.update(list(order_names))

        for v in self.all_vertices:
            particles = v.particles
            names = []
            spins = []
            for p in particles:
                names.append(p.name)
                spins.append(p.spin - 1)

            vorders = {}
            cplnames = [c.name for c in v.couplings.values()]
            for coord, coupling in list(v.couplings.items()):
                for name in orders:
                    if name in coupling.order:
                        vorders[name] = coupling.order[name]
                    else:
                        vorders[name] = 0

                _, il, *_ = coord
                vorders["RK"] = v.lorentz[il].rank

            deg = len(particles)

            xidx = list(range(deg))

            fold_name = "(%s) %s Vertex" % (v.name, " -- ".join(names))
            f.write("*---#[ %s:\n" % fold_name)
            f.write(f"Identify Once vertex(iv?, {v.name}")
            colors = []
            for i in xidx:
                p = particles[i]
                color = abs(p.color)
                spin = abs(p.spin) - 1
                # N.B.: the particles of the vertex object are defined to be outgoing in the UFO convention, but we use
                # the convention where all particles are incoming. Therefore all particles must be inverted.
                if p.name != p.antiname and p.pdg_code > 0:
                    spin = -spin
                    color = -color
                colors.append(color)

                f.write(
                    ",\n   idx%d?,%d,vec%d?,idx%dL%d?,%d,idx%dC%d?"
                    % (i + 1, spin, i + 1, i + 1, abs(spin), color, i + 1, abs(color))
                )
            f.write(") =")

            # The following is used split the amplitude for the truncation options.
            # QL>0 always implies NP>0.
            NPQL_brack_flag = False
            if "QL" in vorders.keys() and vorders["QL"] > 0:
                f.write("\n  XQLorder^%d * (" % (vorders["QL"]))
                NPQL_brack_flag = True
            elif "NP" in vorders.keys() and vorders["NP"] > 0:
                f.write("\n  XNPorder^%d * (" % (vorders["NP"]))
                NPQL_brack_flag = True

            dummies = []

            brack_flag = False
            for i, s in enumerate(spins):
                if s == 3 or s == 4:
                    brack_flag = True
                    idx = "idx%dL%d" % (i + 1, s)
                    idxa = "idx%dL%da" % (i + 1, s)
                    idxb = "idx%dL%db" % (i + 1, s)
                    f.write("\n SplitLorentzIndex(%s, %s, %s) *" % (idx, idxa, idxb))
                    dummies.append(idxa)
                    dummies.append(idxb)

            if brack_flag:
                f.write(" (")

            for coord, coupling in sorted(list(v.couplings.items()), key=lambda x: x[0]):
                if not coupling.name in cplnames:
                    continue
                ic, il = coord
                lorentz = lorex[v.lorentz[il].name]
                scolor = v.color[ic]
                f.write("\n   + %s" % (self.prefix + coupling.name.replace("_", "")))
                if scolor != "1":
                    color = parser.compile(scolor)
                    color = color.replaceStrings("ModelDummyIndex", lsubs, lcounter)
                    color = color.replaceNegativeIndices(0, "MDLIndex%d", dummy_found)
                    color = transform_color(color, colors, xidx)
                    if lorentz == ex.IntegerExpression(1):
                        expr = color
                    else:
                        expr = color * lorentz
                else:
                    expr = lorentz
                if not expr == ex.IntegerExpression(1):
                    f.write(" * (")
                    lwf.nl()
                    expr.write(lwf)
                    f.write("\n   )")

                for ind in list(lsubs.values()):
                    s = str(ind)
                    if expr.dependsOn(s):
                        if s not in dummies:
                            dummies.append(s)

            if brack_flag:
                f.write(")")
            if NPQL_brack_flag:
                f.write("\n)")
            f.write(";\n")

            for idx in list(dummy_found.values()):
                dummies.append(str(idx))

            if len(dummies) > 0:
                f.write("Sum %s;\n" % ", ".join(dummies))
            f.write("*---#] %s:\n" % fold_name)

        if self.useCT:
            for v in self.all_CTvertices:
                particles = v.particles
                names = []
                spins = []
                for p in particles:
                    names.append(p.name)
                    spins.append(p.spin - 1)

                vorders = {}
                cplnames = [c.name for c in v.couplings.values()]
                for coord, coupling in list(v.couplings.items()):
                    for name in orders:
                        if name in coupling.order:
                            vorders[name] = coupling.order[name]
                        else:
                            vorders[name] = 0

                    _, il, *_ = coord
                    vorders["RK"] = v.lorentz[il].rank

                deg = len(particles)
                xidx = list(range(deg))

                fold_name = "(%s) %s CTVertex" % (v.name, " -- ".join(names))
                f.write("*---#[ %s:\n" % fold_name)
                f.write(f"Identify Once vertex(iv?, {v.name}")
                colors = []
                for i in xidx:
                    p = particles[i]
                    color = abs(p.color)
                    spin = abs(p.spin) - 1
                    # N.B.: the particles of the vertex object are defined to be outgoing in the UFO convention, but we use
                    # the convention where all particles are incoming. Therefore all particles must be inverted.
                    if p.name != p.antiname and p.pdg_code > 0:
                        spin = -spin
                        color = -color
                    colors.append(color)

                    f.write(
                        ",\n   idx%d?,%d,vec%d?,idx%dL%d?,%d,idx%dC%d?"
                        % (i + 1, spin, i + 1, i + 1, abs(spin), color, i + 1, abs(color))
                    )
                f.write(") =")

                # The following is used split the amplitude for the truncation options.
                # QL>0 always implies NP>0.
                NPQL_brack_flag = False
                if "QL" in vorders.keys() and vorders["QL"] > 0:
                    f.write("\n  XQLorder^%d * (" % (vorders["QL"]))
                    NPQL_brack_flag = True
                elif "NP" in vorders.keys() and vorders["NP"] > 0:
                    f.write("\n  XNPorder^%d * (" % (vorders["NP"]))
                    NPQL_brack_flag = True

                dummies = []

                brack_flag = False
                for i, s in enumerate(spins):
                    if s == 3 or s == 4:
                        brack_flag = True
                        idx = "idx%dL%d" % (i + 1, s)
                        idxa = "idx%dL%da" % (i + 1, s)
                        idxb = "idx%dL%db" % (i + 1, s)
                        f.write("\n SplitLorentzIndex(%s, %s, %s) *" % (idx, idxa, idxb))
                        dummies.append(idxa)
                        dummies.append(idxb)

                if brack_flag:
                    f.write(" (")

                for coord, coupling in sorted(list(v.couplings.items()), key=lambda x: x[0]):
                    if not coupling.name in cplnames:
                        continue
                    ic, il, ip = coord
                    lorentz = lorex[v.lorentz[il].name]
                    scolor = v.color[ic]
                    f.write("\n   + %s" % (self.prefix + coupling.name.replace("_", "") + "eftctcpl"))
                    if scolor != "1":
                        color = parser.compile(scolor)
                        color = color.replaceStrings("ModelDummyIndex", lsubs, lcounter)
                        color = color.replaceNegativeIndices(0, "MDLIndex%d", dummy_found)
                        color = transform_color(color, colors, xidx)
                        if lorentz == ex.IntegerExpression(1):
                            expr = color
                        else:
                            expr = color * lorentz
                    else:
                        expr = lorentz
                    if not expr == ex.IntegerExpression(1):
                        f.write(" * (")
                        lwf.nl()
                        expr.write(lwf)
                        f.write("\n   )")

                    for ind in list(lsubs.values()):
                        s = str(ind)
                        if expr.dependsOn(s):
                            if s not in dummies:
                                dummies.append(s)

                if brack_flag:
                    f.write(")")
                if NPQL_brack_flag:
                    f.write("\n)")
                f.write(";\n")

                for idx in list(dummy_found.values()):
                    dummies.append(str(idx))

                if len(dummies) > 0:
                    f.write("Sum %s;\n" % ", ".join(dummies))
                f.write("*---#] %s:\n" % fold_name)

        f.write("#EndProcedure\n")
        f.write("*---#] Procedure ReplaceVertices :\n")

        f.write("*---#[ Dummy Indices:\n")
        for ind in list(lsubs.values()):
            f.write("Index %s;\n" % ind)
        f.write("*---#] Dummy Indices:\n")
        f.write("""\
*---#[ Procedure VertexConstants :
#Procedure VertexConstants
* Just a dummy, all vertex constants are already
* replaced in ReplaceVertices.
*
* This procedure might disappear in any future version of Golem
* so don't rely on it.
*
#EndProcedure
*---#] Procedure VertexConstants :
""")

    def write_yukawa_ct_file(self, f) -> None:
        for v in self.all_vertices:
            # Identify Yukawa vertices we want to generate counterterms for:
            #   - Has two massive quarks (identified by PDG code <= 6)
            #   - Has one Higgs (identified by PDG code 25)
            #   - Has no new physics (order zero in coupling `NP`)
            pdg_codes = [abs(p.pdg_code) for p in v.particles]
            if len(v.particles) == 3 and any(pdg_codes.count(q) == 2 for q in range(7)) and pdg_codes.count(25) == 1:
                orders = next((c.order for c in v.couplings.values()), None)
                if orders is not None and "NP" in orders and orders["NP"] != 0:
                    continue
                quark_mass = next(p.mass for p in v.particles if abs(p.pdg_code) <= 6)
                if quark_mass == "0" or quark_mass == "ZERO":
                    continue
                f.write(f"""\
Id vertex(iv?, {v.name},
          idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
          idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
          idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
    vertex(iv, {v.name},
           idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
           idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
           idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
    (1+XCT*CYUKAWA*DELTAYUKOS{self.prefix + str(quark_mass)});

""")


    def containsMajoranaFermions(self):
        for p in self.all_particles:
            if p.spin % 2 == 0 and p.selfconjugate:
                return True
        return False

    def store(self, path, local_name, order_names):
        logger.info("  Writing Python file ...")
        with open(os.path.join(path, "%s.py" % local_name), "w") as f:
            self.write_python_file(f)

        logger.info("  Writing Form file ...")
        with open(os.path.join(path, "%s.hh" % local_name), "w") as f:
            self.write_form_file(f, order_names)

        logger.info("  Writing Form Yukawa counterterm file ...")
        if not os.path.isdir(os.path.join(path, "codegen")):
            os.mkdir(os.path.join(path, "codegen"))
        with open(os.path.join(path, "codegen", "ufo_yukawa_counterterms.hh"), "w") as f:
            self.write_yukawa_ct_file(f)

    def vertex(self, label: str) -> Vertex:
        if label[-1].isdigit() and label[-2] == "_":
            # During export into a QGRAF or FORM model file, a '_<digit>' is added. Since this only encodes splitting
            # into unambiguous coupling power pieces, it can be ignored here
            if self.useCT:
                return (self.all_vertices+self.all_CTvertices)[self.labels[label[:-2]]]
            else:
                return self.all_vertices[self.labels[label[:-2]]]
        else:
            if self.useCT:
                return (self.all_vertices+self.all_CTvertices)[self.labels[label]]
            else:
                return self.all_vertices[self.labels[label]]

lor_P = ex.SymbolExpression("P")
lor_Metric = ex.SymbolExpression("Metric")
lor_Epsilon = ex.SymbolExpression("Epsilon")
lor_Identity = ex.SymbolExpression("Identity")
lor_Gamma = ex.SymbolExpression("Gamma")
lor_ProjP = ex.SymbolExpression("ProjP")
lor_ProjM = ex.SymbolExpression("ProjM")

lor_ProjMinus = ex.SymbolExpression("ProjMinus")
lor_ProjPlus = ex.SymbolExpression("ProjPlus")
lor_Sm = ex.SymbolExpression("Sm")
lor_d = ex.SymbolExpression("d")
lor_d1 = ex.SymbolExpression("d_")
lor_NCContainer = ex.SymbolExpression("NCContainer")
lor_Gamma5 = ex.SymbolExpression("Gamma5")
lor_e = ex.SymbolExpression("e_")


def get_rank(expr):
    if isinstance(expr, ex.SumExpression):
        n = len(expr)
        lst = [get_rank(expr[i]) for i in range(n)]
        if len(lst) == 0:
            return 0
        else:
            return max(lst)

    elif isinstance(expr, ex.ProductExpression):
        n = len(expr)
        result = 0

        for i in range(n):
            sign, factor = expr[i]
            result += get_rank(factor)
        return result

    elif isinstance(expr, ex.PowerExpression):
        assert isinstance(expr.getExponent(), ex.IntegerExpression)
        return get_rank(expr.getBase()) * (int(expr.getExponent()))

    elif isinstance(expr, ex.UnaryMinusExpression):
        return get_rank(expr.getTerm())

    elif isinstance(expr, ex.FunctionExpression):
        head = expr.getHead()
        args = expr.getArguments()
        if head == lor_P:
            return 1
        else:
            return 0
    else:
        return 0


def transform_lorentz(expr, spins):
    if isinstance(expr, ex.SumExpression):
        n = len(expr)
        return ex.SumExpression([transform_lorentz(expr[i], spins) for i in range(n)])
    elif isinstance(expr, ex.ProductExpression):
        n = len(expr)
        new_factors = []

        for i in range(n):
            sign, factor = expr[i]
            new_factors.append((sign, transform_lorentz(factor, spins)))
        return ex.ProductExpression(new_factors)
    elif isinstance(expr, ex.PowerExpression):
        return ex.PowerExpression(
            transform_lorentz(expr.getBase(), spins), transform_lorentz(expr.getExponent(), spins)
        )
    elif isinstance(expr, ex.UnaryMinusExpression):
        return ex.UnaryMinusExpression(transform_lorentz(expr.getTerm(), spins))
    elif isinstance(expr, ex.FunctionExpression):
        head = expr.getHead()
        args = expr.getArguments()
        if head == lor_P:
            # P(index, momentum)
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index = args[0]
            mom = ex.SymbolExpression("vec%d" % int(args[1]))
            # UFO files have all momenta outgoing:
            return -mom(index)
        elif head == lor_Metric or head == lor_Identity:
            my_spins = []
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
                my_spins.append(s)
            else:
                index1 = args[0]
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
                my_spins.append(s)
            else:
                index2 = args[1]

            if my_spins == [1, 1]:
                # return lor_d1(index1, index2)
                return lor_NCContainer(ex.IntegerExpression(1), index1, index2)
            else:
                return lor_d(index1, index2)
        elif head == lor_Gamma:
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index2 = args[1]
            if isinstance(args[2], ex.IntegerExpression):
                i = int(args[2])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index3 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index3 = args[2]
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                if i == 5:
                    return lor_NCContainer(lor_Gamma5, index2, index3)
                else:
                    i_particle = i % 1000
                    i_index = i // 1000
                    s = spins[i_particle - 1] - 1
                    if i_index == 1:
                        suffix = "a"
                    elif i_index == 2:
                        suffix = "b"
                    else:
                        suffix = ""
                    index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index1 = args[0]
            return lor_NCContainer(lor_Sm(index1), index2, index3)
        elif head == lor_Gamma5:
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index1 = args[0]
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                i_particle = i % 1000
                i_index = i // 1000
                s = spins[i_particle - 1] - 1
                if i_index == 1:
                    suffix = "a"
                elif i_index == 2:
                    suffix = "b"
                else:
                    suffix = ""
                index2 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
            else:
                index2 = args[2]
            return lor_NCContainer(lor_Gamma5, index1, index2)
        elif head == lor_ProjM:
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                s = spins[i - 1] - 1
                index1 = ex.SymbolExpression("idx%dL%d" % (i, s))
            else:
                index1 = args[0]
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                s = spins[i - 1] - 1
                index2 = ex.SymbolExpression("idx%dL%d" % (i, s))
            else:
                index2 = args[1]
            return lor_NCContainer(lor_ProjMinus, index1, index2)
        elif head == lor_ProjP:
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                s = spins[i - 1] - 1
                index1 = ex.SymbolExpression("idx%dL%d" % (i, s))
            else:
                index1 = args[0]
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                s = spins[i - 1] - 1
                index2 = ex.SymbolExpression("idx%dL%d" % (i, s))
            else:
                index2 = args[1]
            return lor_NCContainer(lor_ProjPlus, index1, index2)
        elif head == lor_Epsilon:
            arg_list = []
            for ind in range(len(args)):
                if isinstance(args[ind], ex.IntegerExpression):
                    i = int(args[ind])
                    i_particle = i % 1000
                    i_index = i // 1000
                    s = spins[i_particle - 1] - 1
                    if i_index == 1:
                        suffix = "a"
                    elif i_index == 2:
                        suffix = "b"
                    else:
                        suffix = ""
                    index1 = ex.SymbolExpression("idx%dL%d%s" % (i_particle, s, suffix))
                else:
                    index1 = args[ind]
                arg_list.append(index1)
            return lor_e(*arg_list)
        else:
            return expr
    else:
        return expr


col_T = ex.SymbolExpression("T")
col_f = ex.SymbolExpression("f")
col_Identity = ex.SymbolExpression("Identity")
col_d_ = ex.SymbolExpression("d_")
col_d8 = ex.SymbolExpression("dcolor8")
col_d3 = ex.SymbolExpression("dcolor")


def transform_color(expr, colors, xidx):
    if isinstance(expr, ex.SumExpression):
        n = len(expr)
        return ex.SumExpression([transform_color(expr[i], colors, xidx) for i in range(n)])
    elif isinstance(expr, ex.ProductExpression):
        n = len(expr)
        new_factors = []

        for i in range(n):
            sign, factor = expr[i]
            new_factors.append((sign, transform_color(factor, colors, xidx)))
        return ex.ProductExpression(new_factors)

    elif isinstance(expr, ex.UnaryMinusExpression):
        return ex.UnaryMinusExpression(transform_color(expr.getTerm(), colors, xidx))
    elif isinstance(expr, ex.FunctionExpression):
        head = expr.getHead()
        args = expr.getArguments()
        if head == col_T or head == col_f:
            indices = []
            order = []
            xi = []
            for j in range(3):
                if isinstance(args[j], ex.IntegerExpression):
                    i = int(args[j])
                    x = xidx[i - 1]
                    c = abs(colors[x])
                    order.append(colors[x])
                    xi.append(x)
                    indices.append(ex.SymbolExpression("idx%dC%d" % (x + 1, c)))
                else:
                    indices.append(args[j])
                    order.append(0)
                    xi.append(-1)
            if head == col_T:
                # Modification for Dirac-gluinos:
                if order[0] == -8:
                    order[0] = 8  # representation is real
                if order == [8, -3, 0]:
                    order[2] = 3
                elif order == [8, 0, 3]:
                    order[1] = -3
                elif order == [0, -3, 3]:
                    order[0] = 8
                if order == [8, -3, 3]:
                    return head(indices[0], indices[1], indices[2])
                elif order == [8, 3, -3]:
                    return head(indices[0], indices[2], indices[1])
                else:
                    logger.critical("Cannot recognize color assignment at vertex: %s" % order)
                    sys.exit("GoSam terminated due to an error")
            else:
                return head(indices[0], indices[1], indices[2])
        if head == col_Identity:
            c = 0
            if isinstance(args[0], ex.IntegerExpression):
                i = int(args[0])
                c = abs(colors[i - 1])
                index1 = ex.SymbolExpression("idx%dC%d" % (i, c))
            else:
                index1 = args[0]
            if isinstance(args[1], ex.IntegerExpression):
                i = int(args[1])
                c = abs(colors[i - 1])
                index2 = ex.SymbolExpression("idx%dC%d" % (i, c))
            else:
                index2 = args[1]
            if c == 3:
                return col_d3(index1, index2)
            elif c == 8:
                return col_d8(index1, index2)
            else:
                return col_d_(index1, index2)
        else:
            return expr
    else:
        return expr

def load_ufo_files(mname, mpath):
    mfile = None
    try:
        if sys.version_info >= (
            3,
            6,
        ):
            fpath = mpath[0] + "/" + mname + "/__init__.py"
            mod = load_source(mname, fpath)
        else:
            import imp

            mfile, mpath, mdesc = imp.find_module(mname, mpath)
            mod = imp.load_module(mname, mfile, mpath, mdesc)
    except ImportError as exc:
        logger.critical("Problem importing model file: %s" % exc)
        sys.exit("GoSam terminated due to an error")
    finally:
        if mfile is not None:
            mfile.close()
    return mod
