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
*--#] include definitions and procedures:

*--#[ load result:
#Include- `COFILE'
.sort
*--#] load result:

*--#[ read integral name, lowest_prefactor_order, lowest_order:
Id INT(ReduzeF?$IntegralName,sDUMMY1?$LowestPrefactorOrder,sDUMMY2?$LowestOrder) = 1; 
.sort
#Write "IntegralName = `$IntegralName'"
#Write "LowestPrefactorOrder = `$LowestPrefactorOrder'"
#Write "LowestOrder = `$LowestOrder'"
*--#] read integral name, lowest_prefactor_order, lowest_order:

*--#[ unscreen coefficient:
Id SCREEN(sDUMMY1?) = sDUMMY1;
.sort
*--#] unscreen coefficient:

*--#[ series expand:
Multiply replace_(dimS,4-2*epsS);
.sort
#call seriesExpand(l`LOOPS', epsS, {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}) * Defines $highestPole
*--#] series expand:

*--#[ multiply coupling constants into coefficient:
Id PREFACTOR(sDUMMY1?) = prf(sDUMMY1,1);
.sort
PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:noprf;
*--#] multiply coupling constants into coefficient:

*--#[ write entry in coefficients.hpp:
#Append <coefficients.hpp>
#Write <coefficients.hpp> "std::vector<std::vector<secdecutil::Series<coeff_return_t>>> coefficient_of_`$IntegralName'"
#Write <coefficients.hpp> "{"
#Do ProjectorIndex = 1, `NUMPROJ'
  #Write <coefficients.hpp> "  {"
  #Do ColorSymbolIndex = 1, `NUMCS'
    #Write <coefficients.hpp> "     coefficient_of_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'"
    #If ( `ColorSymbolIndex' != `NUMCS')
      #Write <coefficients.hpp> "     ,"
    #EndIf
  #EndDo
  #Write <coefficients.hpp> "  }"
  #If ( `ProjectorIndex' != `NUMPROJ')
    #Write <coefficients.hpp> "  ,"
  #EndIf
#EndDo
#Write <coefficients.hpp> "};"
.sort
*--#] write entry in coefficients.hpp:

*--#[ write coefficient header:
#Do ProjectorIndex = 1, `NUMPROJ'
  #Do ColorSymbolIndex = 1, `NUMCS'
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "secdecutil::Series<coeff_return_t> coefficient_of_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'"
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "\{`$highestPole', // Minimum epsS order"
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> " {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}, // Maximum epsS order"
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "  {"
    #Do EpsOrder = `$highestPole', {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'}
* Since we are not allowed to have a "-" in c++ names
* replace the "-" by an "m" if required
      #If `EpsOrder' < 0
        #Redefine cppOrder "m{-`EpsOrder'}"
      #Else 
        #Redefine cppOrder "`EpsOrder'"
      #EndIf
      #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "coefficient_of_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'(invariants)"
      #If ( `EpsOrder' != {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'} )
        #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> ","
      #EndIf
    #EndDo
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "  },"
    #Write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'.hpp> "true}; // series is truncated"
  #EndDo
#EndDo
.sort
*--#]  write coefficient header:

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
      B epsS, ProjLabel, COLORFACTOR;
      .sort
      L [epsS^`EpsOrder'*ProjLabel(Proj`ProjectorIndex')*COLORFACTOR(c`ColorSymbolIndex')] = l`LOOPS'[epsS^`EpsOrder'*ProjLabel(Proj`ProjectorIndex')*COLORFACTOR(c`ColorSymbolIndex')];
      .sort
      Hide l`LOOPS';
      .sort
* TODO: Write i_ in a syntax acceptable to C++
      Format C;
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "/*\n"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "Coefficient:"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  IntegralName: `$IntegralName'"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  ProjectorLabel: Proj`ProjectorIndex'"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  ColorSymbol: c`ColorSymbolIndex'"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  EpsOrder: `EpsOrder'"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> ""
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "*/"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> ""
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "coeff_return_t coeff_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'(invariants_t invariants)"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "{\n"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  coeff_return_t coeff = %e", [epsS^`EpsOrder'*ProjLabel(Proj`ProjectorIndex')*COLORFACTOR(c`ColorSymbolIndex')]
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "  return coeff;"
      #write <coefficient_`$IntegralName'_Proj`ProjectorIndex'_c`ColorSymbolIndex'_ord`cppOrder'.cc> "}\n"
      Drop [epsS^`EpsOrder'*ProjLabel(Proj`ProjectorIndex')*COLORFACTOR(c`ColorSymbolIndex')];
      UnHide l`LOOPS'; 
      .sort
    #EndDo
  #EndDo
#EndDo
*--#] write coefficient files:

print+s;
.end
