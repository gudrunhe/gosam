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
#include- `INTEGRAL'.out

* Insert dimS in terms of epsS
Id dimS=4-2*epsS;
.sort

print;
.end

* Count minimum power of epsS in numerator and denominator
#If termsin(expr) == 0

  #$minnum = 0;
  #$minden = 0;

#Else

  Skip; Nskip [NINTR(1)];
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

#message `$minnum'
#message `$minden'

Id INT(?head) = INT(?head,[],`$minden'-`$minnum'+`ORD')
.sort

* Discard prefactors from INT function
Repeat Id INT(sDUMMY1?,?a,[],?b,[],?c) = sDUMMY1*INT(?a,[],?b,[],?c);
Id Once INT([],?a) = INT(?a);
.sort













**** UP TO HERE
B INT;
print+s;
.end

Denominators Den;
.sort

* Simplify coefficients
Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);
Id Dim(sDUMMY1?) = prf(sDUMMY1,1);
** TODO: Check that 1/(a+Den(b)) terms from Reduze are handled correctly
#Call FeedPolyRatFun(`ProjectorLabels')
PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:noprf;

Bracket `ProjectorLabels',PREFACTOR,COLORFACTOR;
.sort
#Write <reducedl`LOOPS'.txt>, "L l`LOOPS' = %e", l`LOOPS'
*print+s;
.sort

* Compute the leading pole multiplying each integral
Multiply replace_(dimS,4-2*epsS);
.sort:dimS;
PolyRatFun prf(divergence,epsS);
.sort:prf;

* Drop everything except the INT and its required order
Id SCREEN?!{,INT,prf}(?head)=1;
Id sDUMMY1?=1;
.sort:drop screen;

PolyRatFun;
.sort:noprf;

* Store the epsS order to which we must compute the integral
Id prf(sDUMMY1?,sDUMMY2?) = SCREEN(sDUMMY1/sDUMMY2);
Id SCREEN(epsS^sDUMMY1?) = SCREEN(epsS^sDUMMY1,sDUMMY1);
Id SCREEN(epsS) = SCREEN(epsS,1);
Id SCREEN(1) = SCREEN(epsS,0);
Id INT(?head)*SCREEN(?a,sDUMMY1?) = INT(?head,[],-sDUMMY1+`ORD');
.sort:int order;

* Export Integrals to SecDec
#Call TagIntReduze
#Call TagToPropListSecDec
#Call IntToSecDec
.sort:tosecdec;

#Write <secdecintegralsl`LOOPS'.txt>, "+ %E", l`LOOPS'
*print+s;
.end