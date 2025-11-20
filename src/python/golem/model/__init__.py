from typing import cast

import feyngraph as fg

MODEL_OPTIONS: dict[str, str | int | bool] = {}
MODEL_ONES = []
UNITARY_GAUGE = False

feyngraph_model: fg.Model | None = None

__all__ = ["MODEL_OPTIONS"]

# Particle properties used in the diagram generation / processing.
# This property is defined in `golem.util.tools.prepare_model_files`
MODEL_DATA: dict[str, dict[str, str | int]] = dict()


def update_zero(zeroes: list[str]):
    for symbol in zeroes:
        keys = [k for k, v in MODEL_DATA["mass"].items() if v == symbol]
        for k in keys:
            MODEL_DATA["mass"][k] = "0"
        keys = [k for k, v in MODEL_DATA["width"].items() if v == symbol]
        for k in keys:
            MODEL_DATA["width"][k] = "0"


def mass(particle: str) -> str:
    return cast(str, MODEL_DATA["mass"][particle])


def width(particle: str) -> str:
    return cast(str, MODEL_DATA["width"][particle])


def aux(particle: str) -> int:
    return (
        cast(int, MODEL_DATA["aux"][particle]) if particle in MODEL_DATA["aux"] else 0
    )
