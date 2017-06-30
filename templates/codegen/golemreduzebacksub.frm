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
#include- `INTEGRAL'.in
#include- coefficients.txt
#include- coefficientsl`LOOPS'.hh

Id INTD(sDUMMY1?)*sDUMMY2? = INTD(sDUMMY1,sDUMMY2);
.sort

#call simplifyproduct(expr,list,INTD,tmp1,tmp2,tmp3,tmp4,tmp5)

* Split expression into separate expressions
#call split(expr,list,INT,R,fDUMMY1)
.sort

* Split numerators and denominators into separate expressions
#Do coeff = list
  #Ifdef `coeff'
    #call topolyratfun(`coeff',N,D,ProjNum,Den,0 , tmp1,tmp2)
  #EndIf
#EndDo

* Drop unnecessary expressions
Drop; 
NDrop expr, list;
#Do coeff = list
  NDrop [N`coeff'], [D`coeff'] ;
#EndDo

* Insert dimS in terms of epsS
Id dimS=4-2*epsS;
.sort

* Count minimum power of epsS in numerator and denominator
#If termsin(expr) == 0

  #$minnum = 0;
  #$minden = 0;

#Else

  Skip; NSkip [NINTR(1)];
  #$minnum = maxpowerof_(epsS);
  if ( count(epsS,1) < $minnum ) $minnum = count_(epsS,1);
  ModuleOption,minimum,$minnum;
  .sort

  Skip; Nskip [DINTR(1)];
  #$minden = maxpowerof_(epsS);
  if ( count(epsS,1) < $minden ) $minden = count_(epsS,1);
  ModuleOption,minimum,$minden;
  .sort

#EndIf

Id INT(?head) = INT(?head,[],`$minden'-`$minnum'+`ORD');
.sort

* Pull prefactors from INT function
Skip; NSkip expr;
Repeat Id INT(sDUMMY1?,?a,[],?b,[],?c,[],?d) = sDUMMY1*INT(?a,[],?b,[],?c,[],?d);
Id Once INT([],?a) = INT(?a);
.sort

*
* Write amplitude
*
#Do e = {`activeexprnames_'}
  #IfDef `e' 
    #Write <`INTEGRAL'.backsub> "L `e' = %e" `e'
  #EndIf
#EndDo
.sort



Drop;
NDrop expr;
.sort

*
* Write integrals prepared for SecDec
*
#call producelist(expr,list,INT)

Drop expr;
.sort

* Export Integrals to SecDec
#Call TagIntReduze
#Call TagToPropListSecDec
#Call IntToSecDec
.sort:tosecdec;

#Write <secdec_`INTEGRAL'.hh> "%E", list
.end

