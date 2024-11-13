# vim: ts=3:sw=3:expandtab

import os.path
import sys

import golem.properties

from golem.topolopy.objects import Diagram, Propagator, Leg, LoopCache, TreeCache, CTCache
import golem.topolopy.userlib
from golem.util.config import GolemConfigError

import logging

logger = logging.getLogger(__name__)


def setup_list(prop, conf):
    result = []
    for r in conf.getListProperty(prop):
        if r == "":
            continue
        if ":" in r:
            boundaries = r.split(":")
            if len(boundaries) == 1:
                a = int(boundaries[0])
                b = a + 1
                c = 1
            elif len(boundaries) == 2:
                a = int(boundaries[0])
                b = int(boundaries[1]) + 1
                c = 1
            elif len(boundaries) == 3:
                a = int(boundaries[0])
                b = int(boundaries[1]) + 1
                c = int(boundaries[2])
            else:
                logger.critical("Invalid range: %r" % r)
                sys.exit("GoSam terminated due to an error")
            result.extend(list(range(a, b, c)))
        else:
            result.append(int(r))
    return result


def setup_filter(prop, conf, model):
    locs = {}
    globs = globals().copy()

    globs.update(model.particles)
    globs["_"] = None

    quarks = []
    leptons = []
    fermions = []
    bosons = []

    for name, prtcl in list(model.particles.items()):
        tsp = prtcl.getSpin()
        clr = prtcl.getColor()

        if tsp % 2 == 1:
            fermions.append(name)
        else:
            bosons.append(name)
        if abs(tsp) == 1 and abs(clr) == 3:
            quarks.append(name)
        if abs(tsp) == 1 and abs(clr) == 1:
            leptons.append(name)

    golem.topolopy.userlib.QUARKS = quarks
    golem.topolopy.userlib.LEPTONS = leptons
    golem.topolopy.userlib.FERMIONS = fermions
    golem.topolopy.userlib.BOSONS = bosons

    for name in dir(golem.topolopy.userlib):
        if name.startswith("_"):
            continue
        globs[name] = getattr(golem.topolopy.userlib, name)

    fltr_mod_file = conf.getProperty(golem.properties.filter_module).strip()
    if fltr_mod_file:
        try:
            fltr_mod_file = os.path.expanduser(os.path.expandvars(fltr_mod_file))
            exec(compile(open(fltr_mod_file, "rb").read(), fltr_mod_file, "exec"), globs, globs)
        except IOError as ex:
            logger.critical("Problems reading filter module %r: %s" % (fltr_mod_file, str(ex)))
            sys.exit("GoSam terminated due to an error")
        except SyntaxError as ex:
            logger.critical(
                "Syntax error while reading filter module %r [%d:%d]: %s" % (ex.filename, ex.lineno, ex.offset, ex.msg),
                ex.text,
            )
            sys.exit("GoSam terminated due to an error")

    fltr = conf.getProperty(prop)
    if len(fltr.strip()):
        try:
            return eval(fltr, globs)
        except SyntaxError as ex:
            logger.critical("Option %s is not a valid expression" % prop)
            sys.exit("GoSam terminated due to an error")
    else:
        return lambda d: True


def analyze_tree_diagrams(diagrams, model, conf, filter_flags=None):
    zero = golem.util.tools.getZeroes(conf)
    lst = setup_list(golem.properties.select_lo_diagrams, conf)
    fltr = setup_filter(golem.properties.filter_lo_diagrams, conf, model)
    keep = []
    lose = []
    signs = {}
    # flows = {}

    treecache = TreeCache()

    for idx, diagram in list(diagrams.items()):
        if lst:
            if idx not in lst:
                lose.append(idx)
                continue

        if diagram.EHCfound():
            conf["ehc"] = True

        if analyze_diagram(diagram, zero, fltr):
            keep.append(idx)

            if filter_flags is not None:
                for flag in diagram.filter_flags:
                    if flag not in filter_flags:
                        filter_flags[flag] = [idx]
                    else:
                        filter_flags[flag].append(idx)
        else:
            lose.append(idx)
            conf["veto_crossings"] = diagram.filtered_by_momentum

        signs[idx] = diagram.sign()
    #   flows[idx] = diagram.fermion_flow()

    logger.debug("After analyzing tree diagrams: keeping %d, purging %d" % (len(keep), len(lose)))

    for idx in keep:
        treecache.add(diagrams[idx], idx)

    return keep, signs, treecache  # , flows


def analyze_loop_diagrams(
    diagrams, model, conf, onshell, quark_masses=None, complex_masses=None, filter_flags=None, massive_bubbles={}
):
    zero = golem.util.tools.getZeroes(conf)
    lst = setup_list(golem.properties.select_nlo_diagrams, conf)
    fltr = setup_filter(golem.properties.filter_nlo_diagrams, conf, model)
    keep = []
    keep_tot = []
    lose = []
    max_rank = 0

    loopcache = LoopCache()
    loopcache_tot = LoopCache()

    for idx, diagram in list(diagrams.items()):
        if lst:
            if idx not in lst:
                lose.append(idx)
                continue
        if analyze_diagram(diagram, zero, fltr):
            # check for massive quarks first. Even though the
            # diagram might fail the next test it contributes
            # to the renormalization of the gluon wave function.
            if quark_masses is not None:
                for qm in diagram.QuarkBubbleMasses():
                    if qm not in quark_masses:
                        quark_masses.append(qm)
            if complex_masses is not None:
                for cqm in diagram.ComplexQuarkBubbleMasses():
                    if cqm not in complex_masses:
                        complex_masses.append(cqm)
                    if cqm == "0" and complex_masses[len(complex_masses) - 1] != "0" and (len(complex_masses) % 2) == 1:
                        complex_masses.append(cqm)

            if diagram.onshell() > 0:
                lose.append(idx)
            else:
                keep.append(idx)
                keep_tot.append(idx)
                loopcache_tot.add(diagram, idx)

                diagram.isMassiveBubble(idx, massive_bubbles)

                if filter_flags is not None:
                    for flag in diagram.filter_flags:
                        if flag not in filter_flags:
                            filter_flags[flag] = [idx]
                        else:
                            filter_flags[flag].append(idx)
                rk = diagram.rank()
                if rk > max_rank:
                    max_rank = rk
        else:
            lose.append(idx)
            conf["veto_crossings"] = diagram.filtered_by_momentum

    logger.debug("After analyzing loop diagrams: keeping %d, purging %d" % (len(keep_tot), len(lose)))

    # --- new start

    props = []
    eprops = {}
    for idx in keep:
        props_str = str(diagrams[idx].getLoopIntegral()) \
                    + "," \
                    + str(diagrams[idx].rank()) 
        if conf.getBooleanProperty("use_MQSE"):
            props_str = props_str \
                        + "," \
                        + str(diagrams[idx].isMassiveQuarkSE())
        props.append(
            [
                idx,
                props_str,
            ]
        )

    if conf.getProperty(golem.properties.sum_diagrams):
        for i, item in props:
            for j, jtem in props:
                if item == jtem and j > i:
                    if j not in lose:
                        lose.append(j)
                        keep.remove(j)
                        if i not in eprops:
                            eprops[i] = [j]
                        else:
                            eprops[i].append(j)
    for idx in keep:
        loopcache.add(diagrams[idx], idx)
        if idx not in list(eprops.keys()):
            eprops[idx] = [idx]
        else:
            eprops[idx].append(idx)
    # --- new end

    logger.debug("After analyzing loop diagrams and diagram sum: keeping %d, purging %d" % (len(keep), len(lose)))

    conf["__max_rank__"] = max_rank

    return keep, keep_tot, eprops, loopcache, loopcache_tot


def analyze_ct_diagrams(diagrams, model, conf, filter_flags=None):
    zero = golem.util.tools.getZeroes(conf)
    lst = setup_list(golem.properties.select_ct_diagrams, conf)
    fltr = setup_filter(golem.properties.filter_ct_diagrams, conf, model)
    keep = []
    lose = []
    signs = {}

    ctcache = CTCache()

    for idx, diagram in list(diagrams.items()):
        if lst:
            if idx not in lst:
                lose.append(idx)
                continue

        if analyze_diagram(diagram, zero, fltr):
            keep.append(idx)

            if filter_flags is not None:
                for flag in diagram.filter_flags:
                    if flag not in filter_flags:
                        filter_flags[flag] = [idx]
                    else:
                        filter_flags[flag].append(idx)
        else:
            lose.append(idx)
            conf["veto_crossings"] = diagram.filtered_by_momentum

        signs[idx] = diagram.sign()

    logger.debug("After analyzing CT diagrams: keeping %d, purging %d" % (len(keep), len(lose)))

    for idx in keep:
        ctcache.add(diagrams[idx], idx)

    return keep, signs, ctcache


def analyze_diagram(diagram, zero, fltr):
    if diagram.colorforbidden():
        return False
    diagram.substituteZero(zero)

    if isinstance(fltr, list):
        result = False
        flags = []
        for key, predicate in enumerate(fltr):
            if predicate(diagram):
                flags.append(str(key))
                result = True
        diagram.filter_flags = flags
        return result
    elif isinstance(fltr, dict):
        flags = []
        result = False
        for key, predicate in list(fltr.items()):
            if predicate(diagram):
                flags.append(key)
                result = True
        diagram.filter_flags = flags
        return result
    else:
        if fltr(diagram):
            diagram.filter_flags = [""]
            return True
