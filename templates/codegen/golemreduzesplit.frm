#-
off statistics;
*Format 255; * Number of characters per line

#Include- reduze.hh
#Include- symbols.hh
#Include- secdec.hh
#Include- projectors.hh
#Include- spinney.hh
#Include- model.hh

* Create list of ProjLabel1,...,ProjLabel`NUMPROJ'
#Define ProjectorLabels ""
#Do label = 1, `NUMPROJ'
#Redefine ProjectorLabels "`ProjectorLabels',ProjLabel`label'"
#EndDo
.sort

* Load GoSam result
#include- reducedl`LOOPS'.txt;

* Load SecDec integral naming and integral orders
#include- secdecnamesl`LOOPS'.hh;
#include- secdecordersl`LOOPS'.hh;
.sort

*
* Write each integral times coefficient into its own file
*

B INTDIMLESS;
.sort:bracket;
Collect SCREEN; * Error - collect statement could overflow!
.sort:collect;

* Tag each term ( integral * coefficient ) with TermLabel ^ TermNumber
#$NumberOfTerms = 0;
.sort
$NumberOfTerms = $NumberOfTerms + 1;
Multiply TermLabel ^ $NumberOfTerms;
.sort

#Do TermNumber = 1, `$NumberOfTerms'
  B TermLabel;
  .sort
  L [`TermNumber'] = l`LOOPS'[TermLabel ^ `TermNumber'];
  .sort
  Hide l`LOOPS';
  .sort
  Id INTDIMLESS(ReduzeF?$IntegralName,?a) = INTDIMLESS(ReduzeF,?a); * Get integral name
  .sort
* Write coefficient to file
  #Define CoefficientFile "coefficients/`LOOPS'loop/codegen/coefficient_`$IntegralName'.coeff"
  #Write <`CoefficientFile'> "* "
  #Write <`CoefficientFile'> "* Reduced integral times coefficient of integral `$IntegralName' "
  #Write <`CoefficientFile'> "* "
  #Write <`CoefficientFile'> "L l`LOOPS' = %e", [`TermNumber']
*  #Close <`CoefficientFile'>
* Write log of coefficient files
*  #write <coefficient_log.yaml> "---"
*  #write <coefficient_log.yaml> "integral:"
*  #write <coefficient_log.yaml> "  name: `$IntegralName'"
*  #write <coefficient_log.yaml> "  file: coefficient_`$IntegralName'.coeff"
  Drop [`TermNumber'];
  Unhide l`LOOPS';
 #EndDo

Id TermLabel = 1;
.sort

*print+s;
.end
