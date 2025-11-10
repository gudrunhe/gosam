from __future__ import annotations
from copy import deepcopy
import os
from math import copysign
from types import ModuleType
import itertools

import feyngraph as fg
import jinja2

from golem.pyxo.objects import (diagram as pyxo_diagram, leg as pyxo_leg, vertex as pyxo_vertex,
                                propagator as pyxo_propagator, field as pyxo_field)
from golem.topolopy.objects import Diagram, Leg, Propagator, Vertex
from golem.util.config import Properties, split_power
from golem.util.tools import golem_path, process_path, getModel
import golem

import logging
logger = logging.getLogger(__name__)

def run_feyngraph(in_particles: list[str], out_particles: list[str], conf: Properties) \
        -> tuple[dict[int, Diagram] | None, ...]:
    """
    Generate the diagrams and write the `diagrams-<i>.hh` files.
    """
    if hasattr(golem.model, "feyngraph_model"):
        model = golem.model.feyngraph_model
    else:
        if conf.getBooleanProperty("is_ufo"):
            model: fg.Model = fg.Model.from_ufo(conf["model_path"])
            model.merge_vertices()
        else:
            model: fg.Model = fg.Model.from_qgraf(conf["model_path"])

    powers: list[list[str]] = split_power(",".join(map(str, conf.getListProperty(golem.properties.coupling_power))))
    for power in powers:
        if len(power) == 2:
            power.append(power[1])
    with open(golem_path("templates/codegen/diagrams.hh.jinja"), "r") as file:
        diagram_template: jinja2.Template = jinja2.Template(file.read())

    selector: fg.DiagramSelector = fg.DiagramSelector()
    if "nosnail" in conf.getProperty(golem.properties.native_filters):
        selector.select_self_loops(0)
    if "notadpole" in conf.getProperty(golem.properties.native_filters):
        selector.select_tadpoles(0)
    if "onepi" in conf.getProperty(golem.properties.native_filters):
        selector.select_opi_components(1)
    if "onshell" in conf.getProperty(golem.properties.native_filters):
        selector.select_on_shell()
    particle_restrictions: dict[str, int] = {
        restriction.split(":")[0].strip(): int(restriction.split(":")[1].strip())
        for restriction in conf.getProperty("filter.particles").split(",")
    } if conf.getProperty("filter.particles") is not None else {}
    for particle, count in particle_restrictions.items():
        selector.select_propagator_count(particle, count)
    vertex_restrictions: dict[list[str], int] = {
        restriction.split(":")[0].strip()[1:-1].split(): int(restriction.split(":")[1].strip())
        for restriction in conf.getProperty("filter.vertices").split(",")
    } if conf.getProperty("filter.vertices") is not None else {}
    for particle_list, count in vertex_restrictions.items():
        selector.select_vertex_count(particle_list, count)

    model_module: ModuleType = getModel(conf)
    model_data: dict[str, dict[str, str | int]] = {
        "twospin": {name: p.getSpin() for name, p in model_module.particles.items()},
        "color": {name: int(copysign(p.getColor(), p.getPDGCode())) for name, p in model_module.particles.items()},
        "mass": {name: p.getMass() for name, p in model_module.particles.items()},
        "width": {name: p.getWidth() for name, p in model_module.particles.items()},
        "aux":  model_module.aux if hasattr(model_module, "aux") else {name: 0 for name, _ in model_module.particles.items()},
        "line_styles": model_module.line_styles,
        "latex_names": model_module.latex_names,
    }

    momentum_labels: list[str] = ["k" + str(i+1) for i in range(len(in_particles) + len(out_particles))] + ["p1"]

    # ----------- Born Diagrams -----------
    if conf.getBooleanProperty("generate_tree_diagrams") or conf.getBooleanProperty("generate_eft_loopind"):
        lo_selector: fg.DiagramSelector = deepcopy(selector)
        if conf.getBooleanProperty("generate_tree_diagrams"):
            for coupling, lo_power, _ in powers:
                lo_selector.select_coupling_power(coupling, int(lo_power))
        else:
            for coupling, _, nlo_power in powers:
                lo_selector.select_coupling_power(coupling, int(nlo_power))
        particle_restrictions: dict[str, int] = {
            restriction.split(":")[0].strip(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.lo.particles").split(",")
        } if conf.getProperty("filter.lo.particles") is not None else {}
        for particle, count in particle_restrictions.items():
            lo_selector.select_propagator_count(particle, count)
        vertex_restrictions: dict[list[str], int] = {
            restriction.split(":")[0].strip()[1:-1].split(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.lo.vertices").split(",")
        } if conf.getProperty("filter.lo.vertices") is not None else {}
        for particle_list, count in vertex_restrictions.items():
            lo_selector.select_vertex_count(particle_list, count)
        lo_selector.select_coupling_power("CT", 0)
        lo_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            0,
            model,
            lo_selector,
        )
        lo_generator.set_momentum_labels(momentum_labels)
        lo_diagrams: fg.DiagramContainer | None = lo_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-0.hh"), "w") as file:
            file.write(diagram_template.render(
                {"diagrams": lo_diagrams, "ufo": conf.getBooleanProperty("is_ufo")} | model_data
            ))
        draw_diagrams(lo_diagrams, model_data, os.path.join(process_path(conf), "pyxotree.tex"))
    else:
        lo_diagrams: fg.DiagramContainer | None = None

    # --------- one-loop Diagrams ---------
    if conf.getBooleanProperty("generate_loop_diagrams"):
        nlo_selector: fg.DiagramSelector = deepcopy(selector)
        for coupling, _, nlo_power in powers:
            nlo_selector.select_coupling_power(coupling, int(nlo_power))
        nlo_selector.select_coupling_power("CT", 0)
        particle_restrictions: dict[str, int] = {
            restriction.split(":")[0].strip(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.nlo.particles").split(",")
        } if conf.getProperty("filter.nlo.particles") is not None else {}
        for particle, count in particle_restrictions.items():
            nlo_selector.select_propagator_count(particle, count)
        vertex_restrictions: dict[list[str], int] = {
            restriction.split(":")[0].strip()[1:-1].split(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.nlo.vertices").split(",")
        } if conf.getProperty("filter.nlo.vertices") is not None else {}
        for particle_list, count in vertex_restrictions.items():
            nlo_selector.select_vertex_count(particle_list, count)
        nlo_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            1,
            model,
            nlo_selector,
        )
        nlo_generator.set_momentum_labels(momentum_labels)
        nlo_diagrams: fg.DiagramContainer | None = nlo_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-1.hh"), "w") as file:
            file.write(diagram_template.render(
                {"diagrams": nlo_diagrams, "ufo": conf.getBooleanProperty("is_ufo")} | model_data
            ))
        draw_diagrams(nlo_diagrams, model_data, os.path.join(process_path(conf), "pyxovirt.tex"))
    else:
        nlo_diagrams: fg.DiagramContainer | None = None

    # ----------- CT Diagrams -----------
    if conf.getBooleanProperty("generate_eft_counterterms"):
        ct_selector: fg.DiagramSelector = deepcopy(selector)
        for coupling, _, nlo_power in powers:
            ct_selector.select_coupling_power(coupling, int(nlo_power))
        ct_selector.select_coupling_power("CT", 1)
        particle_restrictions: dict[str, int] = {
            restriction.split(":")[0].strip(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.ct.particles").split(",")
        } if conf.getProperty("filter.ct.particles") is not None else {}
        for particle, count in particle_restrictions.items():
            ct_selector.select_propagator_count(particle, count)
        vertex_restrictions: dict[list[str], int] = {
            restriction.split(":")[0].strip()[1:-1].split(): int(restriction.split(":")[1].strip())
            for restriction in conf.getProperty("filter.ct.vertices").split(",")
        } if conf.getProperty("filter.ct.vertices") is not None else {}
        for particle_list, count in vertex_restrictions.items():
            ct_selector.select_vertex_count(particle_list, count)
        ct_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            0,
            model,
            ct_selector,
        )
        ct_generator.set_momentum_labels(momentum_labels)
        ct_diagrams: fg.DiagramContainer | None = ct_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-ct.hh"), "w") as file:
            file.write(diagram_template.render(
                {"diagrams": ct_diagrams, "ufo": conf.getBooleanProperty("is_ufo")} | model_data
            ))
        draw_diagrams(ct_diagrams, model_data, os.path.join(process_path(conf), "pyxoct.tex"))
    else:
        ct_diagrams: fg.DiagramContainer | None = None

    if conf.getBooleanProperty("generate_tree_diagrams") and len(lo_diagrams) == 0 \
        and conf.getBooleanProperty("generate_loop_diagrams"):
        logger.warning(
            "The current setup has no tree-level diagrams, the result will always be zero.\n" +
            "Use `order={},NONE,{}` instead of `order={}` to compute the |virtual|^2." .format(
                powers[0][0], powers[0][2], ",".join(map(str, list(itertools.chain(*powers))))
            )
        )

    return (convert_diagrams(lo_diagrams, model_data),
            convert_diagrams(nlo_diagrams, model_data),
            convert_diagrams(ct_diagrams, model_data))

def draw_diagrams(diagrams: fg.DiagramContainer, model_data: dict[str, dict[str, str | int]], outfile: str):
    """
    Draw the diagrams with `pyxodraw`.
    """
    opts: dict[str, int | float ] = {
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

    BOUNDARY: str = "NEXT DIAGRAM"

    with open(outfile, "w") as file:
        file.write("Diagrams generated by PyxoDraw\n\n")
        file.write("You will need the LaTeX package AxoDraw for drawing.\n")
        file.write(f"\n\nboundary={BOUNDARY}\n\n")
        diag_index: int = 1
        for diag in diagrams:
            pyxo_diag: pyxo_diagram = pyxo_diagram(
                {
                    i+1: pyxo_leg(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.momentum_str(),
                        p.vertex(1).id()+1
                    )
                    for i, p in enumerate(diag.incoming())
                },
                {
                    i+1: pyxo_leg(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.momentum_str(),
                        p.vertex(0).id()+1
                    ) for i, p in enumerate(diag.outgoing())
                },
                {
                    i+1: pyxo_vertex(
                        v.degree(),
                        *[
                            pyxo_field(
                                p.particle().name(),
                                model_data["mass"][p.particle().name()],
                                -1 if p.particle().is_anti() else 1,
                                model_data["twospin"][p.particle().name()],
                                model_data["color"][p.particle().name()],
                            ) for p in v.propagators()
                        ],
                        vtype = get_vertex_type(v)
                    ) for i, v in enumerate(diag.vertices())
                },
                {
                    i+1: pyxo_propagator(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.vertex(0).id()+1,
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.vertex(1).id()+1,
                        p.momentum_str()
                    )
                    for i, p in enumerate(diag.propagators())
                }
            )

            file.write(f"--{BOUNDARY} name=diagram{diag_index}\n")
            file.write(f"%% Diagram {diag_index}:\n")

            pyxo_diag.layout(**opts)
            pyxo_diag.draw(file, lookup=model_data["line_styles"], latex=model_data["latex_names"], **opts)
            diag_index += 1
        file.write(f"--{BOUNDARY}--\n")


def get_vertex_type(v):
    cpl = v.interaction().coupling_orders()
    if "CT" in cpl.keys() and cpl["CT"] > 0:
        return -1
    elif "NP" in cpl.keys() and cpl["NP"] > 0:
        return cpl["NP"]
    else:
        return 0


def convert_diagrams(diagrams: fg.DiagramContainer, model_data: dict[str, dict[str, str | int]]) \
        -> dict[int, Diagram] | None:
    if diagrams is None:
        return None
    return {
        i+1: Diagram(
            *[
                Leg(
                    j+1,
                    True,
                    incoming.particle().name(),
                    incoming.vertex(1).id()+1,
                    incoming.ray_index_ordered(1) + 1,
                    incoming.momentum_str(),
                    model_data["mass"][incoming.particle().name()],
                    model_data["twospin"][incoming.particle().name()],
                    model_data["color"][incoming.particle().name()],
                    incoming.particle().self_anti()
                ) for j, incoming in enumerate(diag.incoming())
            ],
            *[
                Leg(
                    j + 1,
                    False,
                    outgoing.particle().name(),
                    outgoing.vertex(0).id()+1,
                    outgoing.ray_index_ordered(1) + 1,
                    outgoing.momentum_str(),
                    model_data["mass"][outgoing.particle().name()],
                    model_data["twospin"][outgoing.particle().name()],
                    model_data["color"][outgoing.particle().name()],
                    outgoing.particle().self_anti()
                ) for j, outgoing in enumerate(diag.outgoing())
            ],
            *[
                Propagator(
                    j + 1,
                    (pn := p.normalize()).particle().name(),
                    pn.vertex(0).id()+1,
                    pn.ray_index_ordered(0) + 1,
                    pn.vertex(1).id()+1,
                    pn.ray_index_ordered(1) + 1,
                    pn.momentum_str(),
                    model_data["mass"][pn.particle().name()],
                    model_data["width"][pn.particle().name()],
                    model_data["aux"][pn.particle().name()],
                    model_data["twospin"][pn.particle().name()],
                    model_data["color"][pn.particle().name()],
                    pn.particle().self_anti(),
                    "-" if pn.particle().is_fermi() else "+"
                ) for j, p in enumerate(diag.propagators())
            ],
            *[
                Vertex(
                    j + 1,
                    v.interaction().coupling_orders()["RK"] if "RK" in v.interaction().coupling_orders() else 0,
                    v.interaction().coupling_orders(),
                    v.interaction().name(),
                    *[p.name() for p in v.particles_ordered()],
                ) for j, v in enumerate(diag.vertices())
            ]
        ) for i, diag in enumerate(diagrams)
    }
