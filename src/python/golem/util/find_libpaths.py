# vim:ts=3:sw=3:expandtab

from golem.util.config import Configurator, OPTIONAL, REQUIRED

components = {
    "AVH_OneLoop": OPTIONAL,
    "Ninja": OPTIONAL,
    "Golem95": OPTIONAL,
    "Fortran": OPTIONAL,
    "Form": REQUIRED,
    "QGraf": REQUIRED,
    "Meson": REQUIRED,
    "Linker": OPTIONAL,
}


def find_libraries(hints={}, return_config=False):
    """
    Return a dict of linkage and include paths
    of the external libraries.

    """

    config = Configurator(hints, **components)

    cdict = {}
    config.store(cdict)

    if return_config:
        return cdict, config
    else:
        return cdict
