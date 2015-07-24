* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Load GoSam result
#include- l`LOOPS'.log;

G l`LOOPS' = l`LOOPS';
.sort:sum;

#include- reductionl`LOOPS'.hh
.sort:reduce;

Denominators Den;
** Check that 1/(a+Den(b)) terms from Reduze are handled correctly
Repeat Id Den(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id sDUMMY1? = prf(sDUMMY1,1);
.sort:feed prf;

Id SCREEN(sDUMMY1?) = sDUMMY1;
.sort:unscreen;

PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:noprf;

Bracket ProjLabel,PREFACTOR,COLORFACTOR;
.sort
#Write <`OUTFILE'reduced.log>, "L l`LOOPS' = %e", l`LOOPS'
print+s;
.sort

********* TESTING CODE ********
#Define OUTPUTREDUCED "0"
#If `OUTPUTREDUCED'
*
* Write list of integrals
*
PolyRatFun;
.sort:no prf;
B INT;
.sort:bracket;
Collect SCREEN;
.sort:collect;
Id SCREEN(?head)=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;

* Throw away information regarding which INT are crossed (for FIRE/LiteRed)
#Define UNCROSS "0"
#If `UNCROSS'
#Call UncrossIntReduze
Id Sector(sDUMMY1?)*INT(sDUMMY2?,?tail) = INT(sDUMMY1,[],?tail);
Id Crossing(?tail) = 1;
Id CrossingShift(?tail)=1;
Id CrossingInvariants(?tail)=1;
.sort:uncross;
DropCoefficient;
.sort:drop coeff;
#EndIf

#Write <`OUTFILE'integrals.log>, "+ %E", l`LOOPS'
print+s;
.end
#EndIf
********* TESTING CODE ********

* Compute the leading pole multiplying each integral
Multiply replace_(dimS,4-2*epsS);
.sort
Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1*Den(sDUMMY2);
.sort

* Note: room for optimisation here, we really just need the LOWEST pole not ALL the poles!
CFunction den; * den(x)=1/x, special function for series package
#include- series.h
* 2*`LOOPS'+`ORD'+1 is max possible # terms in expansion epsS^(-2*`LOOPS') + ... + 1 + ... + epsS^(`ORD')
#call init({2*`LOOPS'+`ORD'+1})
#call series(epsS,{2*`LOOPS'+`ORD'+1})
Id Den(sDUMMY1?) = den(sDUMMY1);
#call expand(den)
Id den(sDUMMY1?) = Den(sDUMMY1);
.sort

B INT,epsS;
.sort:bracket;
Collect SCREEN;
.sort:collect;
Id SCREEN(?head)=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;

********* TESTING CODE ********
* Throw away information regarding which INT are crossed (for FIRE/LiteRed)
#Define UNCROSS "0"
#If `UNCROSS'
#Call UncrossIntReduze
Id Sector(sDUMMY1?)*INT(sDUMMY2?,?tail) = INT(sDUMMY1,?tail);
Id Crossing(?tail) = 1;
Id CrossingShift(?tail)=1;
Id CrossingInvariants(?tail)=1;
.sort:uncross;
DropCoefficient;
.sort:drop coeff;
#EndIf
********* TESTING CODE ********

B INT;
.sort:bracket;
Collect SCREEN;
.sort:collect;
SplitArg;
Argument SCREEN;
Id epsS^sDUMMY1? = sDUMMY1;
EndArgument;

* Store the epsS order to which we must compute the integral
Id SCREEN(?head) = SCREEN(min_(?head));
Id INT(?head)*SCREEN(sDUMMY1?) = INT(?head,[],-sDUMMY1+`ORD');

* Export Integrals to SecDec
#Call TagIntReduze
#Call TagToPropListSecDec
#Call IntToSecDec
.sort:tosecdec;

#Write <`OUTFILE'secdec.txt>, "+ %E", l`LOOPS'
print+s;
.end
