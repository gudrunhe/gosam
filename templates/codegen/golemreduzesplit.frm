#-
off statistics;
*Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Load GoSam result
#include- reducedl`LOOPS'.txt;

* Load SecDec integral naming and integral orders
#include- secdecnamesl`LOOPS'.hh;
#include- secdecordersl`LOOPS'.hh;
.sort

*
* Write each integral times coefficient into its own file
*

B INT;
.sort:bracket;
Collect SCREEN;
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
  Id INT(ReduzeF?$IntegralName,?a) = INT(ReduzeF,?a); * Get integral name
  .sort
* Write coefficient to file
  #write <coefficient_`$IntegralName'.txt> "* "
  #write <coefficient_`$IntegralName'.txt> "* Reduced integral times coefficient of integral `$IntegralName' "
  #write <coefficient_`$IntegralName'.txt> "* "
  #write <coefficient_`$IntegralName'.txt> "L l`LOOPS' = %e", [`TermNumber']
* Write log of coefficient files
*  #write <coefficient_log.yaml> "---"
*  #write <coefficient_log.yaml> "integral:"
*  #write <coefficient_log.yaml> "  name: `$IntegralName'"
*  #write <coefficient_log.yaml> "  file: coefficient_`$IntegralName'.txt"
  Drop [`TermNumber'];
  Unhide l`LOOPS';
 #EndDo

Id TermLabel = 1;
.sort

print+s;
.end
