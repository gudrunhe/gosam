# Overview

This file contains a list of example processes available in GoSam:

## LO tests:

- ___ddzzdd___: $d(k_1) + \bar{d}(k_2) \rightarrow Z(k_3) + Z(k_4) + d(k_5) + \bar{d}(k_6)$ \
           Tree-Level only. \
           Demonstrates how the helicity symmetry finder can reduce the number of
           generated helicities

- ___eeZH_SMEFT___: $e^{+}(k_1) + e^{-}(k_2) \rightarrow Z(k_3) + H(k_4)$ @ $\alpha^2, \alpha_s^0$ \
           Tree-Level only. \
           Demonstrates the selection of different truncation options in SMEFT.

- ___gggg_tree___: $g(k_1)+g(k_2) \rightarrow g(k_3)+g(k_4)$ @ $\alpha_s^2$ \
           Tree-Level only. Includes helicities which are known to be zero.

- ___gguudd___: $g(k_1) + g(k_2) \rightarrow u(k_3) + \bar{u}(k_4) + d(k_5) + \bar{d}(k_6)$ \
           Tree-Level only. All particles massless. \
           (Test case only) Test calculation with many coloured final states.

- ___tttt___: $t(k_1) + \bar{t}(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ \
           Tree-Level only. \
           Test calculation with all external particles massive.

## NLO tests:

- ___bghb___: $b(k_1) + g(k_2) \rightarrow H(k_3) + b(k_4)$ @ $\alpha_s^3, \alpha$

- ___bghb_qp___: $b(k_1) + g(k_2) \rightarrow H(k_3) + b(k_4)$ @ $\alpha_s^3, \alpha$ \
  		 Same as previous, but also generates quadruple precision code.

- ___ddeeg___: $d(k_1) + \bar{d}(k_2) \rightarrow e^{-}(k_3) + e^{+}(k_4) + g(k_5)$ @ $\alpha_s^3, \alpha$

- ___ddhjj_olp___: $g(k_1) + g(k_2) \rightarrow H(k_3) + d(k_4) + \bar{d}(k_5)$ and $d(k_1) + \bar{d}(k_2) \rightarrow H(k_3) + u(k_4) + \bar{u}(k_5)$ @ $\alpha_s^4, \alpha$ \
           Calculation is done through the OLP-Interface using dimensional reduction with the `smehc` model (heavy-top limit)

- ___ddtt___: $d(k_1) + \bar{d}(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha_s^4$

- ___ddzg_crossing___: $d(k_1) + \bar{d}(k_2) \rightarrow Z(k_3) + g(k_4)$ and $d(k_1) + g(k_2) \rightarrow Z(k_3) + d(k_4)$ @ $\alpha_s^4, \alpha$ \
           Both crossings are calculated and compared

- ___dgdg___: $d(k_1)+g(k_2) \rightarrow d(k_3)+g(k_4)$ @ $\alpha_s^4, \alpha^0$ 

- ___eett___: $e^{+}(k_1) + e^{-}(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha^2, \alpha_s$

- ___eett_lhep___: $e^{+}(k_1) + e^{-}(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha^2, \alpha_s^2$ \
           Same as `eett`, but with a `LanHEP` model

- ___eeuu___: $e^{+}(k_1) + e^{-}(k_2) \rightarrow u(k_3) + \bar{u}(k_4)$ @ $\alpha^2, \alpha_s$

- ___gggg___: $g(k_1)+g(k_2) \rightarrow g(k_3)+g(k_4)$ @ $\alpha_s^4$ \
           Purely gluonic process without quark-loops, only one helicity. \
           Comparison with analytic formula.

- ___gggg_lhep___: $g(k_1)+g(k_2) \rightarrow g(k_3)+g(k_4)$ @ $\alpha_s^4$ \
           Same as `gggg`, but with a `LanHEP` model

- ___ggHg_HTL___: $g(k_1) + g(k_2) \rightarrow H(k_3) + g(k_4)$ @ $\alpha_s^4$ \
           Calculation is done in the `smehc` model (heavy-to limit)

- ___ggtt___: $g(k_1) + g(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha_s^3$

- ___ggtt_lhep___: $g(k_1) + g(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha_s^3$ \
           Same as `ggtt`, but with a `LanHEP` model

- ___ggtt_ufo___: $g(k_1) + g(k_2) \rightarrow t(k_3) + \bar{t}(k_4)$ @ $\alpha_s^3$ \
           Same as `ggtt`, but with a `UFO` model

- ___Hbb_SMEFT___: $H(k_1) \rightarrow b(k_2) + \bar{b}(k_3) @ $\alpha_s^2$ \
           Calculates NLO QCD corrections to Higgs decay to bottom quarks including two SMEFT operators ($O_{b\phi}$ and $O_{\phi G}$). Demonstrates how to implement and use counterterms for Wilson coefficients in the UFO model.

- ___Hbb_4F___: $H(k_1) \rightarrow b(k_2) + \bar{b}(k_3) \
           Calculates NLO QCD corrections to Higgs decay to bottom quarks including four-fermion operators.

- ___qqtth___: $d(k_1) + \bar{d}(k_2) \rightarrow H(k_3) + t(k_4) + \bar{t}(k_5)$ @ $\alpha_s^3, \alpha$

- ___s-channel_single_top___: $u(k_1) + \bar{d}(k_2) \rightarrow \nu_e(k_3) + e^{+}(k_4) + b(k_5) + \bar{b}(k_6)$ @ $\alpha^4, \alpha_s$ \
           Includes only one helicity. 

- ___tne___: $g(k_1) + b(k_2) \rightarrow e^{-}(k_3) + \nu_{\bar{e}}(k_4) + t(k_5)$ @ $\alpha_s^2, \alpha^2$

- ___udene___: $\bar{u}(k_1)+d(k_2) \rightarrow e-(k_3) + \nu_e~(k_4)$ @ $\alpha_s^2, \alpha^2$ \

- ___udene_lhep___: $\bar{u}(k_1)+d(k_2) \rightarrow e-(k_3) + \nu_e~(k_4)$ @ $\alpha_s^2, \alpha^2$ \
           Same as `udene`, but with a `LanHEP` model

- ___udene_ufo___: $\bar{u}(k_1)+d(k_2) \rightarrow e-(k_3) + \nu_e~(k_4)$ @ $\alpha_s^2, \alpha^2$ \
           Same as `udene`, but with a `UFO` model

- ___udeneg___: $\bar{u}(k_1)+d(k_2) \rightarrow e^{-}(k_3) + \nu_\bar{e}(k_4) + g(k_5)$ @ $\alpha_s^3, \alpha^2$ \

- ___udeneg_dred_vs_thv___: $\bar{u}(k_1)+d(k_2) \rightarrow e^{-}(k_3) + \nu_\bar{e}(k_4) + g(k_5)$ @ $\alpha_s^3, \alpha^2$ \
  	  Same as above, but calculates one in DRED and once in tHV; compares the results.

- ___udhud_unitary___: $u(k_1) + \bar{d}(k_2) \rightarrow H(k_3) + u(k_4) + \bar{d}(k_5)$ @ $\alpha^3, \alpha_s$ \
           Calculation is done in Feynman gauge and in unitary gauge and both results are compared

- ___uu_graviton_yy___: $u + \bar{u} \rightarrow \mathrm{Graviton} \rightarrow \gamma + \gamma$ \
           Calculation is done in the ADD model (model/LED_UFO) using
           dim. reduction. with a custom propagator for the spin-2 particle
           summing all KK modes.

- ___uudd___: $u(k_1)+\bar{u}(k_2) \rightarrow d(k_3)+\bar{d}(k_4)$ @ $\alpha_s^4, \alpha^0$ \

- ___WpWpjj___: $u(k_1)+\bar{d}(k_2) \rightarrow \bar{c}(k_3)+s(k_4)+e^{+}(k_5)+\nu_e(k_6)+\mu^{+}(k_7)+\nu_\mu(k_8)$ @ $\alpha_s^4, \alpha^4$ \
           Comparison with single phase space point of [arXiv:1007.5313](https://arxiv.org/abs/1007.5313) 

## Loop-induced tests

- ___gggz___: $g(k_1)+g(k_2) \rightarrow g(k_3)+Z(k_4)$ @ $\alpha_s^3, \alpha^1$ \
           This is a loop-induced process.

- ___ggHg_rescue___: $g(k_1) + g(k_2) \rightarrow H(k_3) + g(k_4)$ @ $\alpha_s^4$ \
           This example samples a instable PSP to trigger the rescue system.

- ___ggHg_SMEFT___: $g(k_1) + g(k_2) \rightarrow H(k_3) + g(k_4)$ @ $\alpha_s^4$ \
           Higgs plus jet production in the gluon-fusion channel, including two SMEFT operators ($O_{t\phi}$ and $O_{\phi G}$). Demonstrates the use of different SMEFT truncations for a loop-induced process, in the presence of a potentially loop-suppressed operator ($O_{\phi G}$).

- ___hyy___: $H(k_1) \rightarrow \gamma(k_2) + \gamma(k_3)$ @ $\alpha^3$ \
           This is a loop induced process, it also includes only one helicity. \
           Bosonic and fermionic contributions can be enabled separately, only fermionic contributions by default.

- ___hyy_all_helicities___: $H(k_1) \rightarrow \gamma(k_2) + \gamma(k_3)$ @ $\alpha^3$ \
           Same as `hyy`, but includes all helicities.

- ___hyy_olp___: $H(k_1) \rightarrow \gamma(k_2) + \gamma(k_3)$ @ $\alpha^3$ \
           Same as previous, but uses the BLHA2 interface.

- ___yyyy___: $\gamma(k_1)+\gamma(k_2) \rightarrow \gamma(k_3)+\gamma(k_4)$ \
           Comparison with analytic formulae from literature

# Running the Examples

One can also specify options (on top of the usual configuration files)
for all examples by creating a file `setup.in` from `setup.in.template`. **THIS IS NOT RECOMMENDED** \
Care has to be taken not to put process specific options into
this file.

If no such file exists, only the default values and the values
from config files are used.

Each example can be run by executing 
```console
make test
```
in the respective example folder. Additionally, a `Makefile` is provided to automatically run multiple tests. 
It defines the following commands:

- `make runtests`: \
   This command runs `make test` for all subdirectories.


- `make summarize`: \
   By running `make summarize`, the user obtains a printout of the status
   of all processes for which `make test` has been run earlier. \
   Note that 'make test' is not invoked by this script.


- `make runselected`: \
   This command runs a selection of tests to be specified in the Makefile.


- `make check_selection`: \
   Print a list of the tests in the selection tests.
   Check if they exist or not and if they ran successfully.
   
- `make run_failed`: \
   This command runs all tests which did not succeed previously.

- `make runlo`: \
   This command runs all LO tests.

- `make runnlo`: \
   This command runs all NLO tests.

- `make runloopinduced`: \
   This command runs all loop-induced tests.

- `make clean`:
   Run `make very-clean` in every test directory.


- `make <dirname>`:
   Run `make test` in the directory `<dirname>`.

Setting the variable `ENABLE_CODE_CHECK=true` will compile the examples with 
fortran runtime checks enabled and an increased compiler warning level.


# Possible Issues

In case you encounter failing tests, please, contact the authors. Bug reports,
including the corresponding `test/test.log` can be sent to

[The GoSam collaboration](gosam@lists.kit.edu)

or reported on [github](https://github.com/gudrunhe/gosam).
