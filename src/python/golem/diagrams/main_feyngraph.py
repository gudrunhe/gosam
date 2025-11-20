"""
This is the module containing the functions to perform the diagram generation using FeynGraph.
"""

from __future__ import annotations

import itertools
import logging
import os
from typing import cast

import feyngraph as fg
import jinja2

import golem
import golem.model
from golem.diagrams.filters import setup_selectors
from golem.pyxo.objects import (
    diagram as pyxo_diagram,
)
from golem.pyxo.objects import (
    field as pyxo_field,
)
from golem.pyxo.objects import (
    leg as pyxo_leg,
)
from golem.pyxo.objects import (
    propagator as pyxo_propagator,
)
from golem.pyxo.objects import (
    vertex as pyxo_vertex,
)
from golem.util.config import Properties, split_power
from golem.util.tools import golem_path, process_path

logger = logging.getLogger(__name__)


def run_feyngraph(
    in_particles: list[str], out_particles: list[str], conf: Properties
) -> tuple[fg.DiagramContainer | None, ...]:
    """
    Generate the diagrams and write the `diagrams-<i>.hh` files.
    """
    model: fg.Model
    if golem.model.feyngraph_model is not None:
        model = golem.model.feyngraph_model
    else:
        if conf.getBooleanProperty("is_ufo"):
            model = fg.Model.from_ufo(cast(str, conf["model_path"]))
            _ = model.merge_vertices()
        else:
            model = fg.Model.from_qgraf(cast(str, conf["model_path"]))

    powers: list[list[str | int]] = split_power(
        ",".join(map(str, conf.getListProperty("order")))
    )
    for power in powers:
        if len(power) == 2:
            power.append(power[1])
    with open(golem_path("templates/codegen/diagrams.hh.jinja"), "r") as file:
        diagram_template: jinja2.Template = cast(
            jinja2.Template, jinja2.Template(file.read())
        )

    lo_selector, nlo_selector, ct_selector = setup_selectors(conf, powers)

    momentum_labels: list[str] = [
        "k" + str(i + 1) for i in range(len(in_particles) + len(out_particles))
    ] + ["p1"]

    # ----------- Born Diagrams -----------
    lo_diagrams: fg.DiagramContainer | None
    if conf.getBooleanProperty("generate_tree_diagrams") or conf.getBooleanProperty(
        "generate_eft_loopind"
    ):
        lo_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            0,
            model,
            lo_selector,
        )
        lo_generator.set_momentum_labels(momentum_labels)
        lo_diagrams = lo_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-0.hh"), "w") as file:
            _ = file.write(
                diagram_template.render(
                    {"diagrams": lo_diagrams, "ufo": conf.getBooleanProperty("is_ufo")}
                    | golem.model.MODEL_DATA
                )
            )
        draw_diagrams(
            lo_diagrams,
            golem.model.MODEL_DATA,
            os.path.join(process_path(conf), "pyxotree.tex"),
        )
        logger.info(
            f"Found {len(lo_diagrams)} tree-level diagrams with the current configuration."
        )
    else:
        lo_diagrams = None

    # --------- one-loop Diagrams ---------
    nlo_diagrams: fg.DiagramContainer | None
    if conf.getBooleanProperty("generate_loop_diagrams"):
        nlo_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            1,
            model,
            nlo_selector,
        )
        nlo_generator.set_momentum_labels(momentum_labels)
        nlo_diagrams = nlo_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-1.hh"), "w") as file:
            _ = file.write(
                diagram_template.render(
                    {"diagrams": nlo_diagrams, "ufo": conf.getBooleanProperty("is_ufo")}
                    | golem.model.MODEL_DATA
                )
            )
        draw_diagrams(
            nlo_diagrams,
            golem.model.MODEL_DATA,
            os.path.join(process_path(conf), "pyxovirt.tex"),
        )
        logger.info(
            f"Found {len(nlo_diagrams)} one-loop diagrams with the current configuration."
        )
    else:
        nlo_diagrams = None

    # ----------- CT Diagrams -----------
    ct_diagrams: fg.DiagramContainer | None
    if conf.getBooleanProperty("generate_eft_counterterms"):
        ct_generator: fg.DiagramGenerator = fg.DiagramGenerator(
            in_particles,
            out_particles,
            0,
            model,
            ct_selector,
        )
        ct_generator.set_momentum_labels(momentum_labels)
        ct_diagrams = ct_generator.generate()
        with open(os.path.join(process_path(conf), "diagrams-ct.hh"), "w") as file:
            _ = file.write(
                diagram_template.render(
                    {"diagrams": ct_diagrams, "ufo": conf.getBooleanProperty("is_ufo")}
                    | golem.model.MODEL_DATA
                )
            )
        draw_diagrams(
            ct_diagrams,
            golem.model.MODEL_DATA,
            os.path.join(process_path(conf), "pyxoct.tex"),
        )
        logger.info(
            f"Found {len(ct_diagrams)} counterterm diagrams with the current configuration."
        )
    else:
        ct_diagrams = None

    if (
        lo_diagrams is not None
        and len(lo_diagrams) == 0
        and conf.getBooleanProperty("generate_loop_diagrams")
    ):
        logger.warning(
            """\
The current setup has no tree-level diagrams after applying the filters, the result will always be zero.
If the process is loop-induced, use `order={},NONE,{}` instead of `order={}` to compute the |virtual|^2.\
            """.format(
                powers[0][0],
                powers[0][2],
                ",".join(map(str, list(itertools.chain(*powers)))),
            )
        )

    return lo_diagrams, nlo_diagrams, ct_diagrams


def draw_diagrams(
    diagrams: fg.DiagramContainer,
    model_data: dict[str, dict[str, str | int]],
    outfile: str,
):
    """
    Draw the diagrams with `pyxodraw`.
    """
    opts: dict[str, int | float] = {
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
        _ = file.write(f"""\
Diagrams generated by PyxoDraw

You will need the LaTeX package AxoDraw for drawing.


boundary={BOUNDARY}

""")
        diag_index: int = 1
        for diag in diagrams:
            pyxo_diag: pyxo_diagram = pyxo_diagram(
                {
                    i + 1: pyxo_leg(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.momentum_str(),
                        p.vertex(1).id() + 1,
                    )
                    for i, p in enumerate(diag.incoming())
                },
                {
                    i + 1: pyxo_leg(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.momentum_str(),
                        p.vertex(0).id() + 1,
                    )
                    for i, p in enumerate(diag.outgoing())
                },
                {
                    i + 1: pyxo_vertex(
                        v.degree(),
                        *[
                            pyxo_field(
                                p.particle().name(),
                                model_data["mass"][p.particle().name()],
                                -1 if p.particle().is_anti() else 1,
                                model_data["twospin"][p.particle().name()],
                                model_data["color"][p.particle().name()],
                            )
                            for p in v.propagators()
                        ],
                        vtype=vertex_type(v),
                    )
                    for i, v in enumerate(diag.vertices())
                },
                {
                    i + 1: pyxo_propagator(
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.vertex(0).id() + 1,
                        pyxo_field(
                            p.particle().name(),
                            model_data["mass"][p.particle().name()],
                            -1 if p.particle().is_anti() else 1,
                            model_data["twospin"][p.particle().name()],
                            model_data["color"][p.particle().name()],
                        ),
                        p.vertex(1).id() + 1,
                        p.momentum_str(),
                    )
                    for i, p in enumerate(diag.propagators())
                },
            )

            _ = file.write(f"--{BOUNDARY} name=diagram{diag_index}\n")
            _ = file.write(f"%% Diagram {diag_index}:\n")

            pyxo_diag.layout(**opts)
            pyxo_diag.draw(
                file,
                lookup=model_data["line_styles"],
                latex=model_data["latex_names"],
                **opts,
            )
            diag_index += 1
        _ = file.write(f"--{BOUNDARY}--\n")


def vertex_type(v: fg.Vertex) -> int:
    if v.interaction().order("CT") > 0:
        return 0
    elif v.interaction().order("NP") > 0:
        return v.interaction().order("NP")
    else:
        return 0
