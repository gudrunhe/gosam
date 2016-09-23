#-
off statistics;
Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh
#include- seriesprocedures.hh

* Load GoSam result
#include- `COFILE'
.sort

Id INT(ReduzeF?$IntegralName,sDUMMY1?$LowestPrefactorOrder,sDUMMY2?$LowestOrder) = 1; * Get integral name, lowest_prefactor_order, lowest_order
.sort

Id SCREEN(sDUMMY1?) = sDUMMY1;

#write "IntegralName = `$IntegralName'"
#write "LowestPrefactorOrder = `$LowestPrefactorOrder'"
#write "LowestOrder = `$LowestOrder'"
.sort

Multiply replace_(dimS,4-2*epsS);
.sort

#call seriesExpand(l`LOOPS', epsS, {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'})

Multiply SCREEN(epsS,0);
.sort
Id epsS^sDUMMY1? * SCREEN(epsS,0) = SCREEN(epsS,sDUMMY1);
Id PREFACTOR(sDUMMY1?) = prf(sDUMMY1,1);
.sort:feed prf;
PolyRatFun prf;
.sort:prf;

* TODO use #append for coefficients.hpp and #create for coefficient_...
#write <coefficients.hpp> "/*"
#write <coefficients.hpp> "  MinimumEpsOrder: `$highestPole'"
#write <coefficients.hpp> "  MaximumEpsOrder: {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}"
#write <coefficients.hpp> "*/"
#write <coefficients.hpp> ""
#write <coefficients.hpp> "secdecutil::Series<coeff_return_t> coefficient_of_`$IntegralName' "
#write <coefficients.hpp> "{`$highestPole', {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'},{ "

* Tag each term with TermLabel ^ TermNumber
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
  Id ProjLabel(Proj1?$ProjectorLabel)*COLORFACTOR(c1?$ColorLabel)*SCREEN(epsS,sDUMMY1?$EpsOrder) = 1;
  print+s;
  .sort

* Since we are not allowed to have a "-" in c++ function names
* replace the "-" by an "m" if required
  #if `$EpsOrder' < 0
     #Redefine cppOrder "m{-`$EpsOrder'}"
  #else 
     #Redefine cppOrder "`$EpsOrder'"
  #endif
* TODO: Write i_ in a syntax acceptable to C++
  Format C;

  #write <coefficients.hpp> "coeff_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'(parameters)"
  #if ( `TermNumber' != `$NumberOfTerms')
    #write <coefficients.hpp> ","
  #endif

  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "/*\n"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "Coefficient:"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  IntegralName: `$IntegralName'"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  ProjectorLabel: `$ProjectorLabel'"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  ColorLabel: `$ColorLabel'"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  EpsOrder: `$EpsOrder'"
*  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  LowestPrefactorOrder: `$LowestPrefactorOrder'"
*  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  LowestOrder: `$LowestOrder'"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> ""
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "*/"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> ""
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "#include \"coefficients.hpp\""
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> ""
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "coeff_return_t coeff_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'(parameter_t parameters)"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "{\n"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  coeff_return_type coeff = %e", [`TermNumber']
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "  return coeff;"
  #write <coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorLabel'_ord`cppOrder'.cc> "}\n"
  Drop [`TermNumber'];
  Unhide l`LOOPS';
#EndDo

Id TermLabel = 1;
.sort

#write <coefficients.hpp> "},true};"


print+s;

.end