"""
This module contains functions to query properties of diagrams which are not directly available through FeynGraph.
These were previously available as methods on GoSam's `Diagram` class.
"""

import itertools

import feyngraph as fg

import golem.model
from golem.diagrams.objects import LoopIntegral, Momentum
from golem.model import aux, mass, width

###############################################################################
# Functions for additional properties of the diagrams
###############################################################################


def rank(d: fg.Diagram) -> int:
    """Get the diagram's rank, i.e. the momentum power in the loop-integral's numerator."""
    rank = sum(
        abs(p.particle().spin())
        for p in d.chord(0)
        if abs(p.particle().spin()) != 2
        and aux(p.particle().name()) != 1
        or (golem.model.UNITARY_GAUGE and mass(p.particle().name()) != "0")
    )
    rank += sum(v.interaction().order("RK") for v in d.loop_vertices(0))
    return rank


def massive_quark_self_energy(d: fg.Diagram) -> bool:
    """
    Check whether the diagram's loop is a QCD self-energy insertion on a massive quark propagator. Self-energy
    insertions with new physics vertices are ignored.
    """
    if len(d.chord(0)) != 2:
        return False

    if sum(v.interaction().order("NP") for v in d.loop_vertices(0)) != 0:
        return False

    if not any(
        abs(p.particle().spin()) == 1
        and abs(p.particle().color()) == 3
        and mass(p.particle().name()) != "0"
        for p in d.chord(0)
    ):
        return False

    if not any(
        abs(p.particle().spin()) == 2
        and abs(p.particle().color()) == 8
        and mass(p.particle().name()) == "0"
        for p in d.chord(0)
    ):
        return False

    if any(v.degree() != 3 for v in d.loop_vertices(0)):
        return False

    return True


def is_massive_bubble(d: fg.Diagram) -> bool:
    """Check whether the diagram's loop is a bubble with at least one massive propagator."""
    if len(d.chord(0)) != 2:
        return False
    if not any(mass(p.particle().name()) != "0" for p in d.chord(0)):
        return False
    # Number of propagators which are attached to the loop vertices, but not part of the loop
    if (
        not sum(
            p.momentum()[-1] == 0 for v in d.loop_vertices(0) for p in v.propagators()
        )
        == 2
    ):
        return False
    return True


def is_scaleless(d: fg.Diagram) -> bool:
    """Check whether the diagram's loop integral is scaleless, i.e. the $S$-matrix has only zero-entries."""
    onshell: dict[str, str] = {}

    for leg in [*d.incoming(), *d.outgoing()]:
        m = mass(leg.particle().name())
        if m != "0":
            onshell[f"s{leg.id() + 1}"] = f"{mass}**2"
        else:
            onshell[f"s{leg.id() + 1}"] = "0"

    li = LoopIntegral.from_diagram(d)
    return li.is_scaleless(onshell, "%s**%d", "s")


def contains_ehc(d: fg.Diagram) -> bool:
    """
    Check whether the diagram contains an effective gluon-Higgs coupling. The particles are identified by some
    standard names or their PDG IDs.
    """
    return any(
        v.match_particle_combinations(
            [["g", "G", "part21"], ["g", "G", "part21"], ["H", "part25"]]
        )
        or (
            v.degree() == 3
            and sum(p.particle().pdg() == 21 for p in v.propagators()) == 2
            and sum(p.particle().pdg() == 25 for p in v.propagators()) == 1
        )
        for v in d.vertices()
    )


def quark_bubble_masses(d: fg.Diagram) -> list[str]:
    """Get a list of quark masses which are part of a bubble-loop."""
    if len(d.chord(0)) != 2 or any(
        abs(p.particle().spin()) != 1 or abs(p.particle().color()) != 3
        for p in d.chord(0)
    ):
        return []
    else:
        return [
            mass(p.particle().name())
            for p in d.chord(0)
            if mass(p.particle().name()) != "0"
        ]


def complex_quark_bubble_masses(d: fg.Diagram) -> list[str]:
    """
    Get a list of complex quark masses which are part of a bubble-loop, i.e. only masses of quarks with a non-zero width.
    """
    if len(d.chord(0)) != 2 or any(
        abs(p.particle().spin()) != 1
        or abs(p.particle().color()) != 3
        or mass(p.particle().name()) == "0"
        for p in d.chord(0)
    ):
        return []
    else:
        return list(
            itertools.chain.from_iterable(
                [mass(p.particle().name()), width(p.particle().name())]
                for p in d.chord(0)
                if len(mass(p.particle().name())) > 0
                and len(width(p.particle().name())) > 0
            )
        )


def is_nf(d: fg.Diagram) -> bool:
    """Check whether the diagram's loop contains only light fermions."""
    return all(
        abs(p.particle().spin()) == 1
        and abs(p.particle().color()) == 3
        and mass(p.particle().name()) == "0"
        for p in d.chord(0)
    )


def prop_str(p: fg.Propagator) -> str:
    """Get a string representation of a propagator containing only the particle name, mass and width."""
    name = p.particle().name()
    if p.momentum()[-1] < 0:
        p = p.invert()
    if mass(name) == "0":
        return f"P({p.momentum_str()})"
    else:
        if width(name) == "0":
            return f"P({p.momentum_str()}, {mass(name)})"
        else:
            return f"P({p.momentum_str()}, {mass(name)}, {width(name)})"


def onshell(d: fg.Diagram) -> bool:
    """Check whether the diagram has an on-shell propagator."""
    zerosum = {
        **{leg.momentum_str(): 1 for leg in d.incoming()},
        **{leg.momentum_str(): -1 for leg in d.outgoing()},
    }
    for p in d.propagators():
        if p.momentum()[-1] != 0:
            continue
        if Momentum(p.momentum_str(), zerosum).onshell():
            return True
    return False


def loopsize(d: fg.Diagram) -> int:
    """Get number of propagators in the diagram's loop, not counting non-propagating particles."""
    return d.loopsize(0) - sum(aux(p.particle().name()) == 1 for p in d.chord(0))
