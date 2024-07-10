    ################################################################################
    #   __   __   ___   __   __  __                      GoSam                     #
    #  / _) /  \ / __) (  ) (  \/  )             An Automated One-Loop             #
    # ( (/\( () )\__ \ /__\  )    (             Matrix Element Generator           #
    #  \__/ \__/ (___/(_)(_)(_/\/\_)             Version 3.x.x                     #
    #                                                                              #
    #                                    (c) The GoSam Collaboration 2011-2024     #
    #                                                                              #
    #        AUTHORS:                                                              #
    #        * Gudrun Heinrich                   <gudrun.heinrich@kit.edu>         #
    #        * Stephen Jones                     <s.jones@cern.ch>                 #
    #        * Matthias Kerner                   <mkerner@physik.uzh.ch>           #
    #        * Jannis Lang                       <jannis.lang@kit.edu>             #
    #        * Vitaly Magerya                    <vitaly.magerya@tx97.net>         #
    #        * Pierpaolo Mastrolia               <Pierpaolo.Mastrolia@cern.ch>     #
    #        * Giovanni Ossola                   <gossola@citytech.cuny.edu>       #
    #        * Tiziano Peraro                    <tiziano.peraro@unibo.it>         #
    #        * Johannes Schlenk                  <johannes.schlenk@psi.ch>         #
    #        * Ludovic Scyboz                    <ludovic.scyboz@physics.ox.ac.uk> #
    #        * Francesco Tramontano              <Francesco.Tramontano@cern.ch>    #
    #                                                                              #
    #        FORMER AUTHORS:                                                       #
    #        * Gavin Cullen, Hans van Deurzen, Nicolas Greiner, Stephan Jahn,      #
    #          Gionata Luisoni, Edoardo Mirabella, Joscha Reichel, Thomas Reiter,  #
    #          Johann Felix von Soden-Fraunhofen                                   #
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
  [Meson](https://mesonbuild.com/Getting-meson.html) build system
* Running GoSam requires at least Python version 3.7, to run the Python code in parallel additionally the `multiprocess` 
package is required (available from [PyPI](https://pypi.org/project/multiprocess/)).
* To compile the dependencies and the generated code, a sufficiently modern Fortran compiler is required.

# Installation

GoSam is available from the public [GitHub repository](https://github.com/gudrunhe/gosam) and can be downloaded by 
running 
```console
git clone
```

Then, in the cloned repository, running 
```console
meson setup build --prefix <prefix>
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
and GoSam. To avoid collisions with possible other installations of some of said programs, everything is installed into
a subfolder, e.g. `<prefix>/lib/GoSam/`. To setup the runtime enviroment for GoSam, a script
`<prefix>/bin/GoSam/gosam_setup_env.sh` is generated to update the required enviroment variables. It can be loaded with
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
