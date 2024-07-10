#!/usr/bin/env python
# From https://github.com/mesonbuild/meson/issues/5374
from os import environ, listdir, makedirs, walk
from os.path import join, isdir, exists
from sys import argv
from shutil import copy

all_modules = True

if len(argv) > 2:
    build_dir = argv[1]
else:
    build_dir = environ["MESON_BUILD_ROOT"]
if "MESON_INSTALL_DESTDIR_PREFIX" in environ:
    install_dir = environ["MESON_INSTALL_DESTDIR_PREFIX"]
else:
    install_dir = environ["MESON_INSTALL_PREFIX"]

if len(argv) == 2:
    include_dir = argv[1]
elif len(argv) > 2:
    include_dir = argv[2]
else:
    include_dir = "include"
module_dir = join(install_dir, include_dir)

modules = []
if all_modules:
    # finds $build_dir/**/*.mod
    for root, dirs, files in walk(build_dir):
        modules += [join(root, f) for f in files if f.endswith(".mod")]
else:
    # finds $build_dir/*/*.mod
    for d in listdir(build_dir):
        bd = join(build_dir, d)
        if isdir(bd):
            modules += [join(bd, f) for f in listdir(bd) if f.endswith(".mod")]

if not exists(module_dir):
    makedirs(module_dir)

for mod in modules:
    copy(mod, module_dir)