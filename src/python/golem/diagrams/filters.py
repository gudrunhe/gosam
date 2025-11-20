"""
This module contains functions to setup FeynGraph `DiagramSelectors` according to the specified config.
"""

import logging
import os
import sys
from copy import deepcopy
from typing import Any, Callable, cast

import feyngraph as fg

from golem.util.config import Properties

logger = logging.getLogger(__name__)

###############################################################################
# Functions to setup `DiagramSelectors` according to the config
###############################################################################


def setup_selectors(
    conf: Properties, powers: list[list[str | int]]
) -> tuple[fg.DiagramSelector, ...]:
    """
    Setup the `feyngraph.DiagramSelector` objects as requested by the config `conf` and the coupling orders `powers`.
    Currently, 14 config options are used in this function:
       - `filter.options`: common baseline options
       - `filter[|.lo|.nlo|.ct].particles`: filters on the number of propagators of the respective particles
       - `filter[|.lo|.nlo|.ct]`: custom Python function added to the respective `DiagramSelector`
       - `diagram_selector[|.lo|.nlo|.ct]`: custom `DiagramSelector` used as a baseline for the respective component
       - `filter.module`: Python module which defines symbols for use in the other Python filters
    The `diagram_selector` objects act as baseline, so any other filter option will be applied on top of this, i.e.
    the `filter` function will be added to the selector specified in `diagram_selector`.

    Returns:
        A triple of `DiagramSelectors` for the leading-order diagrams, the next-to-leading-order diagrams and the counterterm diagrams.
    """
    filter_module = read_filter_module(conf)

    # ---------------------------- Base properties ----------------------------
    base_selector: fg.DiagramSelector
    if conf.getProperty("diagram_selector") is not None:
        if isinstance(
            s := eval(cast(str, conf.getProperty("diagram_selector")), filter_module),
            fg.DiagramSelector,
        ):
            base_selector = s
        else:
            logger.critical(
                f"Option 'diagram_selector' must be of type 'feyngraph.DiagramSelector', found {type(s)}"
            )
            sys.exit("GoSam terminated due to an error")
    else:
        base_selector = fg.DiagramSelector()

    apply_base(base_selector, conf, filter_module)

    # ---------------------------------- LO -----------------------------------
    if conf.getProperty("diagram_selector.lo") is not None:
        if isinstance(
            s := eval(
                cast(str, conf.getProperty("diagram_selector.lo")), filter_module
            ),
            fg.DiagramSelector,
        ):
            lo_selector = s
        else:
            logger.critical(
                f"Option 'diagram_selector.lo' must be of type 'feyngraph.DiagramSelector', found {type(s)}"
            )
            sys.exit("GoSam terminated due to an error")
        apply_base(lo_selector, conf)
    else:
        lo_selector: fg.DiagramSelector = deepcopy(base_selector)

    apply_particle_filters(lo_selector, conf, "filter.lo.particles")
    apply_custom_filter(lo_selector, conf, "filter.lo", filter_module)

    if conf.getBooleanProperty("generate_tree_diagrams"):
        for coupling, lo_power, _ in powers:
            lo_selector.select_coupling_power(cast(str, coupling), int(lo_power))
    else:  # Coupling order for loop-induced process
        for coupling, _, nlo_power in powers:
            lo_selector.select_coupling_power(cast(str, coupling), int(nlo_power))

    lo_selector.select_coupling_power("CT", 0)
    logger.debug(f"Selecting tree-level diagram with properties: {lo_selector}")

    # ---------------------------------- NLO ----------------------------------
    if conf.getProperty("diagram_selector.nlo") is not None:
        if isinstance(
            s := eval(
                cast(str, conf.getProperty("diagram_selector.nlo")), filter_module
            ),
            fg.DiagramSelector,
        ):
            nlo_selector = s
        else:
            logger.critical(
                f"Option 'diagram_selector.nlo' must be of type 'feyngraph.DiagramSelector', found {type(s)}"
            )
            sys.exit("GoSam terminated due to an error")
        apply_base(nlo_selector, conf)
    else:
        nlo_selector: fg.DiagramSelector = deepcopy(base_selector)

    apply_particle_filters(nlo_selector, conf, "filter.nlo.particles")
    apply_custom_filter(nlo_selector, conf, "filter.nlo", filter_module)
    # Color tadpoles are always zero and therefore discarded
    nlo_selector.add_custom_function(lambda d: not d.color_tadpole(0))

    for coupling, _, nlo_power in powers:
        nlo_selector.select_coupling_power(cast(str, coupling), int(nlo_power))

    nlo_selector.select_coupling_power("CT", 0)
    logger.debug(f"Selecting one-loop diagram with properties: {nlo_selector}")

    # ---------------------------------- CT -----------------------------------
    if conf.getProperty("diagram_selector.ct") is not None:
        if isinstance(
            s := eval(
                cast(str, conf.getProperty("diagram_selector.ct")), filter_module
            ),
            fg.DiagramSelector,
        ):
            ct_selector = s
        else:
            logger.critical(
                f"Option 'diagram_selector.ct' must be of type 'feyngraph.DiagramSelector', found {type(s)}"
            )
            sys.exit("GoSam terminated due to an error")
        apply_base(ct_selector, conf)
    else:
        ct_selector: fg.DiagramSelector = deepcopy(base_selector)

    apply_particle_filters(ct_selector, conf, "filter.ct.particles")
    apply_custom_filter(ct_selector, conf, "filter.ct", filter_module)

    for coupling, _, nlo_power in powers:
        ct_selector.select_coupling_power(cast(str, coupling), int(nlo_power))

    ct_selector.select_coupling_power("CT", 1)
    logger.debug(f"Selecting counterterm diagram with properties: {ct_selector}")

    return lo_selector, nlo_selector, ct_selector


def read_filter_module(conf: Properties) -> dict[str, Any]:
    """Read the Python file specified in `conf["filter.module"]` and return it's global/local dict."""
    globals: dict[str, Any] = {}
    if conf.getProperty("filter.module") is not None:
        module_file = os.path.expanduser(
            os.path.expandvars(cast(str, conf.getProperty("filter.module")))
        )
        try:
            with open(module_file, "r") as f:
                module_content = f.read()
            exec(module_content, globals, globals)
        except IOError as ex:
            logger.critical(f"Problems reading filter module {module_file}: {ex}")
            sys.exit("GoSam terminated due to an error")
        except SyntaxError as ex:
            logger.critical(
                f"Syntax error while reading filter module {ex.filename} [{ex.lineno}:{ex.offset}]: {ex.msg}",
                ex.text,
            )
            sys.exit("GoSam terminated due to an error")
    exec("from golem.diagrams.methods import *", globals, globals)
    return globals


def apply_base(
    s: fg.DiagramSelector, conf: Properties, filter_module: dict[str, Any] = {}
) -> None:
    """Apply `filter.options`, `filter.particles` and `filter` to the given `DiagramSelector`."""
    native_options: list[str] = cast(list[str], conf.getProperty("filter.options"))
    if "nosnail" in native_options:
        s.select_self_loops(0)
    if "notadpole" in native_options:
        s.select_tadpoles(0)
    if "onepi" in native_options:
        s.select_opi_components(1)
    if "onshell" in native_options:
        s.select_on_shell()

    apply_particle_filters(s, conf, "filter.particles")
    apply_custom_filter(s, conf, "filter", filter_module)


def apply_particle_filters(s: fg.DiagramSelector, conf: Properties, prop: str) -> None:
    """Apply the particle count filters from `prop` to `s`."""
    if conf.getProperty(prop) is not None:
        particles: dict[str, int] = {
            restriction.split(":")[0].strip(): int(restriction.split(":")[1].strip())
            for restriction in cast(str, conf.getProperty(prop)).split(",")
        }
    else:
        particles = {}

    for particle, count in particles.items():
        s.select_propagator_count(particle, count)


def apply_custom_filter(
    s: fg.DiagramSelector,
    conf: Properties,
    prop: str,
    filter_module: dict[str, Any] = {},
) -> None:
    if conf.getProperty(prop) is not None:
        f: Callable[[fg.Diagram], bool] = eval(
            cast(str, conf.getProperty(prop)), filter_module
        )
        s.add_custom_function(f)
