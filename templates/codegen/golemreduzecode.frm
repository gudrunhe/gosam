* vim: syntax=form:ts=3:sw=3:expandtab
#-
Off Statistics;

*--#[ include definitions and procedures: 
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
.sort
*--#] include definitions and procedures:


*--#[ load result:
#Include- `COFILE'
.sort
*--#] load result:

*--#[ read integral information:
Id INTDIMLESS(ReduzeF?$IntegralName,sDUMMY1?$LowestPrefactorOrder,sDUMMY2?$LowestOrder) = 1;
Id sDUMMY1?{,`ProjectorLabels'}$ProjectorLabel = 1;
Id COLORFACTOR(sDUMMY1?$ColorSymbol) = 1;
.sort
#Message `$IntegralName'
#Message `$LowestPrefactorOrder'
#Message `$LowestOrder'
#Message `$ProjectorLabel'
#Message `$ColorSymbol'
#Message ExpansionOrder: {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}
print;
.sort
*--#] read integral information:

*--#[ series expand:
Multiply replace_(dimS,4-2*epsS);
.sort
#call series([NINTR(1)],[DINTR(1)],numpow,denpow,epsS,{`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'},p)
#$highestPole = denpow - numpow;
print;
.sort
#Message `$highestPole'
.sort
*--#] series expand:

*--#[ hide functions for code generation:
Id PREFACTOR(sDUMMY1?) = dum_(sDUMMY1); * Hide PREFACTOR from code
Id COLORINTERNAL(sDUMMY1?) = dum_(sDUMMY1); * Hide COLORINTERNAL function from code
*--#] hide functions for code generation:

*--#[ write coefficient header:
#Define CoefficientHeaderFile "coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'.hpp.tmp"
#Write <`CoefficientHeaderFile'> "#ifndef coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_hpp_included#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#define coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_hpp_included#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#include #@GoSamInternalDblquote@#../../../typedef.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "namespace integral_coefficients {#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Do EpsOrder = `$highestPole', {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}
* Since we are not allowed to have a "-" in c++ names
* replace the "-" by an "m" if required   
  #If `EpsOrder' < 0
    #Redefine cppOrder "m{-`EpsOrder'}"
  #Else 
    #Redefine cppOrder "`EpsOrder'"
  #EndIf
  #Write <`CoefficientHeaderFile'> "coeff_return_t `$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_ord`cppOrder'(invariants_t invariants, parameters_t parameters);#@GoSamInternalNewline@#"
#EndDo
#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"

#Write <`CoefficientHeaderFile'> "coeff_func_series_t `$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "\{#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "`$highestPole', // Minimum epsS order#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "{`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}, // Maximum epsS order#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "  {#@GoSamInternalNewline@#"
#Do EpsOrder = `$highestPole', {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}
* Since we are not allowed to have a "-" in c++ names
* replace the "-" by an "m" if required
  #If `EpsOrder' < 0
    #Redefine cppOrder "m{-`EpsOrder'}"
  #Else 
    #Redefine cppOrder "`EpsOrder'"
  #EndIf
  #Write <`CoefficientHeaderFile'> "`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_ord`cppOrder'"
  #If ( `EpsOrder' != {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'} )
    #Write <`CoefficientHeaderFile'> ",#@GoSamInternalNewline@#"
  #EndIf
#EndDo
#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "},#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "true, // series is truncated#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#@GoSamInternalDblquote@#eps#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "};#@GoSamInternalNewline@#"

#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "};#@GoSamInternalNewline@#"

#Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
#Write <`CoefficientHeaderFile'> "#endif#@GoSamInternalNewline@#"
#Close <`CoefficientHeaderFile'>
.sort
*--#] write coefficient header:

*--#[ write coefficient files:
    #Do EpsOrder = `$highestPole', {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}
* Since we are not allowed to have a "-" in c++ names
* replace the "-" by an "m" if required
      #If `EpsOrder' < 0
        #Redefine cppOrder "m{-`EpsOrder'}"
      #Else 
        #Redefine cppOrder "`EpsOrder'"
      #EndIf
      B epsS, `ProjectorLabels', COLORFACTOR;
      .sort
      L [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(`$ColorSymbol')] = l`LOOPS'[epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(`$ColorSymbol')];
      .sort
      Hide l`LOOPS';
      .sort
* TODO: Write i_ in a syntax acceptable to C++
      Format C;
      #Define CoefficientFile "coefficient_`$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_ord`cppOrder'.cc.tmp"
      #Write <`CoefficientFile'> "/*#@GoSamInternalNewline@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "Coefficient:#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  IntegralName: `$IntegralName'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  ProjectorLabel: `$ProjectorLabel'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  ColorSymbol: `$ColorSymbol'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  EpsOrder: `EpsOrder'#@GoSamInternalNewline@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "*/#@GoSamInternalNewline@#"
      
      #Write <`CoefficientFile'>"#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#include #@GoSamInternalDblquote@#../../../typedef.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"

      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "namespace integral_coefficients {#@GoSamInternalNewline@#"

      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "coeff_return_t `$IntegralName'_`$ProjectorLabel'_`$ColorSymbol'_ord`cppOrder'(invariants_t invariants, parameters_t parameters)#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "{#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#include #@GoSamInternalDblquote@#invariants_hunk.cpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#include #@GoSamInternalDblquote@#parameters_hunk.cpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  coeff_return_t coeff = %e#@GoSamInternalNewline@##@GoSamInternalNewline@#", [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(`$ColorSymbol')](#@no_split_expression@#)
      #Write <`CoefficientFile'> "  return coeff;#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "};#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "};#@GoSamInternalNewline@#"
      #Close <`CoefficientFile'>
      Drop [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(`$ColorSymbol')];
      UnHide l`LOOPS'; 
      .sort
    #EndDo
  #EndDo
#EndDo
*--#] write coefficient files:

*print+s;
.end
