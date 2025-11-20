from collections.abc import Mapping, Sequence

class Particle:
    pdg_code: int
    name: str
    antiname: str
    spin: int
    color: int
    mass: str
    width: str
    texname: str
    antitexname: str
    charge: str
    line: str
    propagating: bool
    CustomSpin2Prop: bool
    selfconjugate: bool

    def anti(self) -> Particle: ...

class Parameter:
    name: str
    nature: str
    type: str
    value: float | str
    texname: str
    lhablock: None | str
    lhacode: None | str

class CTParameter:
    name: str
    nature: str
    value: Mapping[int, str | float]
    texname: str

class Vertex:
    name: str
    particles: Sequence[Particle]
    color: Sequence[str]
    lorentz: Sequence[Lorentz]
    couplings: Mapping[tuple[int, int], Coupling]
    rank: set[int]

class CTVertex:
    name: str
    particles: Sequence[Particle]
    color: Sequence[str]
    lorentz: Sequence[Lorentz]
    couplings: Mapping[tuple[int, int, int], Coupling]
    type: str
    loop_particles: Sequence[Sequence[Sequence[Particle]]]
    rank: set[int]

class Coupling:
    name: str
    value: str | Mapping[int, str]
    order: Mapping[str, int]

class Lorentz:
    name: str
    spins: Sequence[int]
    structure: str
    rank: int
