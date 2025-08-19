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

- ___uu_uu_4F___: $u\bar{u}\to u\bar{u}$
  		   Checks GoSam's functionalities related to four-fermion operators.

Setting the variable `ENABLE_CODE_CHECK=true` will compile the examples with 
fortran runtime checks enabled and an increased compiler warning level.