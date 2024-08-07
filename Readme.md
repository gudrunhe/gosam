    ################################################################################
    #   __   __   ___   __   __  __                      GoSam                     #
    #  / _) /  \ / __) (  ) (  \/  )             An Automated One-Loop             #
    # ( (/\( () )\__ \ /__\  )    (             Matrix Element Generator           #
    #  \__/ \__/ (___/(_)(_)(_/\/\_)             Version 3.x.x                     #
    #                                                                              #
    #                                    (c) The GoSam Collaboration 2011-2024     #
    #                                                                              #
    #        AUTHORS:      
    #        * Jens Braun                                 <jens.braun@student.kit.edu>       #
    #        * Benjamin Campillo  Aveleira      <benjamin.campillo@kit.edu>        #
    #        * Gudrun Heinrich                        <gudrun.heinrich@kit.edu>            # 
    #        * Marius Hoefer                            <marius.hoefer@kit.edu>              #
    #        * Stephen Jones                          <stephen.jones@durham.ac.uk>   #
    #        * Matthias Kerner                         <matthias.kerner@kit.edu>            #
    #        * Jannis Lang                               <jannis.lang@partner.kit.edu>       #
    #        * Vitaly Magerya                           <vitaly.magerya@tx97.net>           #
    #                                                                                                                    #
    #        FORMER AUTHORS:                                                                         #
    #          Gavin Cullen, Hans van Deurzen, Nicolas Greiner, Stephan Jahn,                      #
    #          Gionata Luisoni, Pierpaolo Mastrolia, Edoardo Mirabella, Giovanni Ossola,        #
    #          Tiziano Peraro, Joscha Reichel, Thomas Reiter,  Johannes Schlenk,                  #
    #          Ludovic Scyboz, Johann Felix von Soden-Fraunhofen, Francesco Tramontano  #
    #                                                                              #
    #  This program is free software: you can redistribute it and/or modify        #
    #  it under the terms of the GNU General Public License either                 #
    #  version 3, or (at your option) any later version.                           #
    #                                                                              #
    #  Scientific publications prepared using the present version of               #
    #  GoSam or any modified version of it or any code linking to GoSam            #
    #  or parts of it should make a clear reference to the publication:            #
    #                                                                              #
    #      G. Cullen et al.,                                                       #
    #      ``GoSam-2.0: a tool for automated one-loop calculations                 #
    #                        within the Standard Model and Beyond'',               #
    #      Eur. Phys. J. C 74 (2014) 8,  3001                                      #
    #      [arXiv:1404.7096 [hep-ph]].                                             #
    ################################################################################


# Synopsis

GoSam is a general one-loop evaluator for matrix elements.
The program produces Fortran 90 code from a given process
description by evaluating Feynman diagrams and translating
the associated one-loop diagrams into code suitable for the
evaluation with Ninja, Golem95 and/or Samurai.

# Prerequisites
* Installing GoSam and it's dependencies as well as building the generated Fortran code requires the 
  [Meson](https://mesonbuild.com/Getting-meson.html) build system.
* Running GoSam requires at least Python version 3.7, to run the Python code in parallel additionally the `multiprocess` 
package is required (available from [PyPI](https://pypi.org/project/multiprocess/)).
* To compile the dependencies and the generated code, a sufficiently modern Fortran compiler is required.
* Building GoSam with support for quadruple precision requires QuadNinja, which in turn requires `libquadmath`

# Installation

GoSam is available from the public [GitHub repository](https://github.com/gudrunhe/gosam) and can be downloaded by 
running 
```console
git clone
```

Then, in the cloned repository, running 
```console
meson setup build --prefix <prefix> [-Doption=value]
meson install -C build
```
will download, build and install 
[QGRAF](http://cfif.tecnico.ulisboa.pt/~paulo/qgraf.html), 
[Form](https://www.nikhef.nl/~form/), 
[ff](http://www.nikhef.nl/~t68/ff/), 
[OneLOop](https://helac-phegas.web.cern.ch/OneLOop.html), 
[QCDLoop](http://qcdloop.fnal.gov/), 
[Golem95](http://golem.hepforge.org/), 
[Samurai](https://samurai.hepforge.org/), 
[Ninja](https://ninja.hepforge.org/)
and GoSam. By optionally setting `-Doption=value`, the default build options can be altered. The full list of build
options is available by running `meson configure` in the `build` directory after running `meson setup`.
To avoid collisions with possible other installations of some of said programs, everything is installed into
a subfolder, e.g. `<prefix>/lib/GoSam/`. To set up the runtime environment for GoSam, a script
`<prefix>/bin/GoSam/gosam_setup_env.sh` is generated to update the required environment variables. It can be loaded with
```console
source <prefix>/bin/GoSam/gosam_setup_env.sh
```

> [!NOTE]
> Running `meson install -C build` will by default use all available processor cores. If this is undesired, the number 
> of jobs can be chosen by running 
> ```console
> meson compile -C build -j <jobs>
> meson install -C build
> ```
> instead.

> [!NOTE]
> By default, QuadNinja is built alongside Ninja. If this is undesired, QuadNinja can be disabled by setting 
> `-Dquadninja=false` during setup.

# Running GoSam
Running GoSam generally consists of two steps, the first one being the preparation of the process directory.
This is done by the Python program `gosam.py`. It supports two run modes, standalone mode and OLP
mode. In standalone mode, the process directory is generated by running 
```console
gosam.py <process_card>.in
```
with an appropriate process card. This will generate a folder `<process_dir>` containing all files required for
generating the source code. For details on the process card and running GoSam in OLP mode, please consult the full 
manual.

As a second step, the remaining source is generated and everything is compiled to a library. For this purpose, the
process directory contains a Meson build definition. In the process directory, running 
```console
meson setup build --prefix <prefix>
meson install -C build
```
will generate the remaining source, build the process libraries and install them to `<prefix>`. If GoSam is run in
OLP-mode, additionally a script `build_olp_library.sh` is generated to run all build commands.