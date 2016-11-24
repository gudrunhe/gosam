* vim: syntax=form:ts=3:sw=3:expandtab
#-
Off Statistics;

*--#[ include definitions and procedures: 
#Include- symbols.hh
#Include- spinney.hh
#Include- model.hh
#Include- reduze.hh
#Include- secdec.hh
#Include- seriesprocedures.hh
#Include- projectors.hh

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

*--#[ read integral name, lowest_prefactor_order, lowest_order:
Id INT(ReduzeF?$IntegralName,sDUMMY1?$LowestPrefactorOrder,sDUMMY2?$LowestOrder) = 1; 
.sort
*#Write "IntegralName = `$IntegralName'"
*#Write "LowestPrefactorOrder = `$LowestPrefactorOrder'"
*#Write "LowestOrder = `$LowestOrder'"
*--#] read integral name, lowest_prefactor_order, lowest_order:

*--#[ unscreen coefficient:
Id SCREEN(sDUMMY1?) = sDUMMY1;
.sort
*--#] unscreen coefficient:

*--#[ series expand:
Multiply replace_(dimS,4-2*epsS);
.sort
#call seriesExpand(l`LOOPS', epsS, {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}) * Defines $highestPole
* Simplify
Repeat Id sDUMMY1?!{,epsS,`ProjectorLabels'}^sDUMMY2?pos_ = prf(sDUMMY1^sDUMMY2,1);
Repeat Id sDUMMY1?!{,epsS,`ProjectorLabels'}^sDUMMY2?neg_ = prf(1,sDUMMY1^(-sDUMMY2));
Repeat Id sDUMMY1?!{,epsS,`ProjectorLabels'} = prf(sDUMMY1,1);
Repeat Id den(sDUMMY1?) = prf(1,sDUMMY1);
.sort
PolyRatFun prf;
.sort
PolyRatFun;
Unhide;
.sort
*--#] series expand:

*--#[ multiply coupling constants into coefficient:
Id PREFACTOR(sDUMMY1?) = prf(sDUMMY1,1);
.sort
PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:noprf;
*--#] multiply coupling constants into coefficient:

*--#[ write header:
#Define HeaderFile "coefficient_`$IntegralName'.hpp.tmp"
#Write <`HeaderFile'> "#ifndef coefficient_`$IntegralName'_hpp_included#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "#define coefficient_`$IntegralName'_hpp_included#@GoSamInternalNewline@#"

#Write <`HeaderFile'> "#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "#include #@GoSamInternalDblquote@#typedef.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"

#Write <`HeaderFile'> "#@GoSamInternalNewline@#"
#Do ProjectorIndex = 1, `NUMPROJ'
  #Do ColorSymbolIndex = 1, `NUMCS'
    #Write <`HeaderFile'> "#include #@GoSamInternalDblquote@#coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
  #EndDo
#EndDo

#Write <`HeaderFile'> "#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "namespace integral_coefficients {#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "#@GoSamInternalNewline@#"

#Write <`HeaderFile'> "integral_coeffs_t `$IntegralName'#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "{#@GoSamInternalNewline@#"
#Do ProjectorIndex = 1, `NUMPROJ'
  #Write <`HeaderFile'> "{"
  #Do ColorSymbolIndex = 1, `NUMCS'
    #Write <`HeaderFile'> "`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'"
    #If ( `ColorSymbolIndex' != `NUMCS')
      #Write <`HeaderFile'> ",#@GoSamInternalNewline@#"
    #EndIf
  #EndDo
  #Write <`HeaderFile'> "}"
  #If ( `ProjectorIndex' != `NUMPROJ')
    #Write <`HeaderFile'> ",#@GoSamInternalNewline@#"
  #Else
     #Write <`HeaderFile'> "#@GoSamInternalNewline@#"
  #EndIf
#EndDo
#Write <`HeaderFile'> "};#@GoSamInternalNewline@#"

#Write <`HeaderFile'> "#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "};#@GoSamInternalNewline@#"

#Write <`HeaderFile'> "#@GoSamInternalNewline@#"
#Write <`HeaderFile'> "#endif#@GoSamInternalNewline@#"

.sort
*--#] write header:

*--#[ write coefficient header:
#Do ProjectorIndex = 1, `NUMPROJ'
  #Do ColorSymbolIndex = 1, `NUMCS'
    #Define CoefficientHeaderFile "coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp.tmp"
    #Write <`CoefficientHeaderFile'> "#ifndef coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_hpp_included#@GoSamInternalNewline@#"
    #Write <`CoefficientHeaderFile'> "#define coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_hpp_included#@GoSamInternalNewline@#"
    #Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"
    #Write <`CoefficientHeaderFile'> "#include #@GoSamInternalDblquote@#typedef.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
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
    #Write <`CoefficientHeaderFile'> "coeff_return_t `$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'(invariants_t invariants, parameters_t parameters);#@GoSamInternalNewline@#"
    #EndDo
    #Write <`CoefficientHeaderFile'> "#@GoSamInternalNewline@#"

    #Write <`CoefficientHeaderFile'> "coeff_return_t `$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'#@GoSamInternalNewline@#"
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
      #Write <`CoefficientHeaderFile'> "`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'"
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
  #EndDo
#EndDo
.sort
*--#] write coefficient header:

*--#[ write coefficient files:
#Do ProjectorIndex = 1, `NUMPROJ'
  #Do ColorSymbolIndex = 1, `NUMCS'
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
      L [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(c`ColorSymbolIndex')] = l`LOOPS'[epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(c`ColorSymbolIndex')];
      .sort
      Hide l`LOOPS';
      .sort
* TODO: Write i_ in a syntax acceptable to C++
* TODO: COLORFACTOR should contain only colorsymbols i.e... c1,c2,c3,... but not Nc,TF etc...
      Format C;
      #Define CoefficientFile "coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc.tmp"
      #Write <`CoefficientFile'> "/*#@GoSamInternalNewline@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "Coefficient:#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  IntegralName: `$IntegralName'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  ProjectorLabel: Proj`ProjectorIndex'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  ColorSymbol: c`ColorSymbolIndex'#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  EpsOrder: `EpsOrder'#@GoSamInternalNewline@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "*/#@GoSamInternalNewline@#"
      
      #Write <`CoefficientFile'>"#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#include #@GoSamInternalDblquote@#typedef.hpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"

      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "namespace integral_coefficients {#@GoSamInternalNewline@#"

      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "coeff_return_t `$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'(invariants_t invariants, parameters_t parameters)#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "{#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#include #@GoSamInternalDblquote@#invariants_hunk.cpp#@GoSamInternalDblquote@##@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "  coeff_return_t coeff = %e#@GoSamInternalNewline@##@GoSamInternalNewline@#", [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(c`ColorSymbolIndex')](#@no_split_expression@#)
      #Write <`CoefficientFile'> "  return coeff;#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "};#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "#@GoSamInternalNewline@#"
      #Write <`CoefficientFile'> "};#@GoSamInternalNewline@#"
      Drop [epsS^`EpsOrder'*ProjLabel`ProjectorIndex'*COLORFACTOR(c`ColorSymbolIndex')];
      UnHide l`LOOPS'; 
      .sort
    #EndDo
  #EndDo
#EndDo
*--#] write coefficient files:

*print+s;
.end
