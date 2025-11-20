"""
This module contains functions to check the generated diagrams for various properties required during post-processing.
"""

import logging
import sys
from typing import cast

import feyngraph as fg

from golem.diagrams.methods import (
    complex_quark_bubble_masses,
    contains_ehc,
    loopsize,
    massive_quark_self_energy,
    onshell,
    prop_str,
    quark_bubble_masses,
    rank,
)
from golem.diagrams.objects import LoopCache
from golem.model import aux
from golem.util.config import Properties

logger = logging.getLogger(__name__)


def check_tree(diags: fg.DiagramContainer, conf: Properties) -> None:
    """
    Check the tree-level diagrams in the `DiagramContainer` and set flags in `conf` accordingly.

    Currently considered properties:
        - `ehc`: `diags` contains an effective gluon-Higgs coupling
    """

    # Effective Higgs Couplings
    if diags.query_function(lambda d: contains_ehc(d)) is not None:
        conf["ehc"] = True

    if len(diags) == 0 and not conf.getBooleanProperty("generate_eft_loopind"):
        if conf.getBooleanProperty("ignore_empty_subprocess"):
            conf.setProperty("write_vanishing_amplitude", "true")
        else:
            logger.critical(
                "No remaining diagrams in subprocess {} after applying filters, use --ignore-empty-subprocess to continue anyway.".format(
                    cast(str, conf["process_name"])
                )
            )
            sys.exit("GoSam terminated due to an error")


def analyze_loop(
    diags: fg.DiagramContainer, conf: Properties
) -> tuple[
    LoopCache,
    LoopCache,
    dict[str, set[str] | list[str] | int | str | list[int] | dict[int, list[int]]],
]:
    """
    Analyze the loop diagrams in the `DiagramContainer` and process them. Diagrams are discarded if they are on-shell.
    Otherwise, the properties
        - `quark_masses`: set of quark masses which appear in massive quark loops
        - `complex_quark_masses`: same as `quark_masses`, but only for quarks with a non-zero width
        - `max_rank`: maximum rank of any loop diagram
        - `keep_indices`: indices of the kept diagrams
        - `eprops`: dict containing the diagrams `j` with identical loop propagators to diagram `i` at key `i`
    """
    quark_masses: set[str] = set()
    complex_quark_masses: list[str] = []
    max_rank: int = 0
    keep_indices: list[int] = []
    eprops: dict[int, list[int]] = {}
    seen_propagators: dict[int, str] = {}
    cache_tot = LoopCache()

    for i, d in enumerate(diags):
        quark_masses |= set(quark_bubble_masses(d))
        for complex_mass in complex_quark_bubble_masses(d):
            if complex_mass not in complex_quark_masses:
                complex_quark_masses.append(complex_mass)
            if (
                complex_mass == "0"
                and complex_quark_masses[len(complex_quark_masses) - 1] != "0"
                and (len(complex_quark_masses) % 2) == 1
            ):
                complex_quark_masses.append(complex_mass)

        if onshell(d):
            continue

        if rank(d) > loopsize(d) + 1:
            logger.critical(
                f"Diagram {i} has rank {rank(d)} and loopsize {d.loopsize(0)}, but GoSam only supports diagrams with 'rank - loopsize <= 1'."
            )
            sys.exit("GoSam terminated due to an error")

        cache_tot.add(d, i + 1)

        if (rk := rank(d)) > max_rank:
            max_rank = rk

        s: str = "({}),{}".format(
            ",".join(
                prop_str(p.normalize())
                for p in d.chord(0)
                if aux(p.particle().name()) != 1
            ),
            rk,
        )
        if conf.getBooleanProperty("use_MQSE"):
            s += f",{str(massive_quark_self_energy(d))}"
        seen_propagators[i + 1] = s

    loose: list[int] = []
    if conf.getBooleanProperty("diagsum"):
        for i, s in seen_propagators.items():
            for j in range(i + 1, len(diags) + 1):
                if (
                    s == seen_propagators[j]
                    and j in seen_propagators.keys()
                    and j not in loose
                ):
                    loose.append(j)
                    if i in eprops.keys():
                        eprops[i].append(j)
                    else:
                        eprops[i] = [j]

    cache = LoopCache()
    for i in seen_propagators.keys():
        if i in loose:
            continue
        if i not in eprops.keys():
            eprops[i] = [i]
        else:
            eprops[i].append(i)
        keep_indices.append(i)
        cache.add(diags[i - 1], i)
    return (
        cache,
        cache_tot,
        {
            "quark_masses": quark_masses,
            "complex_quark_masses": complex_quark_masses,
            "max_rank": max_rank,
            "keep_indices": keep_indices,
            "eprops": eprops,
        },
    )
