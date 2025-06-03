# Overview

This file contains a list of processes are used as additional regression tests for the GoSam code:

- ___dd_ttH_EFT___: $d\bar{d}\to t\bar{t}H$ with SMEFT operators $O_{t\phi}$ and $O_{\phi G}$
  		    Uses the `SMEFT_UFO_Otphi_OphiG` UFO model. Checks implementation of QCD counterterms for the EFT vertices and the different truncation options (loop-counting not fully included, yet.). 

- ___gH_tt_OLP___: $gH\to t\bar{t}$
  		   Checks functioning of GoSam when executed in OLP-mode with *.olp file as input. Quick check for quark mass and Yukawa counterterms (faster than `dd_ttH_EFT`).

- ___gH_ttg_EFT___: $gH\to t\bar{t}g$ with SMEFT operators $O_{t\phi}$ and $O_{\phi G}$
  		   Tree level test. Uses the `SMEFT_UFO_Otphi_OphiG` UFO model. Checks spin and colour correlated tree amplitudes used for the Whizard interface.

- ___pp_AAj_OLP___: $d\bar{d}\to\gamma\gamma g$ and $dg\to\gamma\gamma d$
  		   Checks functioning of GoSam when executed in OLP-mode with *.olp file as input. Tests in particular the BLHA amplitude types needed in the Whizard interface.    


# Running the Tests

Each test can be run by executing 
```console
make test
```
in the respective test folder. Additionally, a `Makefile` is provided to automatically run multiple tests. 
It defines the following commands:

- `make runtests`: \
   This command runs `make test` for all subdirectories.


- `make summarize`: \
   By running `make summarize`, the user obtains a printout of the status
   of all processes for which `make test` has been run earlier. \
   Note that 'make test' is not invoked by this script.


- `make runselected`: \
   This command runs a selection of tests, given by the `SELECTED_TEST` variable in the `Makefile`.



- `make check_selection`: \
   Print a list of the tests in the selection tests.
   Check if they exist or not.


- `make clean`:
   Run `make very-clean` in every test directory.


- `make <dirname>`:
   Run `make test` in the directory `<dirname>`.


# Possible Issues

In case you encounter failing tests, please, contact the authors. Bug reports,
including the corresponding `ntest/test.log` can be sent to

[The GoSam collaboration](https://github.com/gudrunhe/gosam)
