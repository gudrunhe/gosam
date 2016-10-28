* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

#Include- reduze.hh
#Include- secdec.hh
#Include- projectors.hh
#Include- symbols.hh
#Include- spinney.hh
#Include- model.hh

* Create list of ProjLabel1,...,ProjLabel`NUMPROJ'
#Define ProjectorLabels ""
#Do label = 1, `NUMPROJ'
#Redefine ProjectorLabels "`ProjectorLabels',ProjLabel`label'"
#EndDo
.sort

* Load GoSam result
#include- l`LOOPS'.txt;

G l`LOOPS' = l`LOOPS';
.sort:sum;

#include- reductionl`LOOPS'.hh
.sort:reduce;

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
PolyRatFun;
.sort:noprf;

* Drop everything except the INT and its required order
Id SCREEN?!{,INT,prf}(?head)=1;
Id sDUMMY1?=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;

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