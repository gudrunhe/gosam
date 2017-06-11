* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;

#Include- reduze.hh
#Include- symbols.hh
#Include- secdec.hh
#Include- projectors.hh
#Include- spinney.hh
#Include- model.hh
#Include- largeprf.hh

* Create list of ProjLabel1,...,ProjLabel`NUMPROJ'
#Define ProjectorLabels ""
#Do label = 1, `NUMPROJ'
  #Redefine ProjectorLabels "`ProjectorLabels',ProjLabel`label'"
#EndDo

* Load integral
#include- `INTEGRAL'.backsub

* Load SecDec integral naming and integral orders
#include- secdecnamesl`LOOPS'.hh;
#include- secdecordersl`LOOPS'.hh;
.sort

*
* Write each integral times coefficient into its own file
*
#If termsin(expr) != 0

  Id INTDIMLESS(ReduzeF?$IntegralName,?a) = INTDIMLESS(ReduzeF,?a); * Get integral name
  Id COLORFACTOR(sDUMMY1?$ColorSymbol) = COLORFACTOR(sDUMMY1);
  Id sDUMMY1?{`ProjectorLabels'}$ProjectorLabel = sDUMMY1;
  .sort
  #Define CoefficientFile "../../../coefficients/`LOOPS'loop/codegen/coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'.coeff"
  #Write <`CoefficientFile'> "* "
  #Write <`CoefficientFile'> "* Reduced integral times coefficient of integral `$IntegralName' "
  #Write <`CoefficientFile'> "* "
  #Do e = {`activeexprnames_'}
    #IfDef `e'
      #Write <`CoefficientFile'> "L `e' = %e" `e'
    #EndIf
  #EndDo

#EndIf
.end
