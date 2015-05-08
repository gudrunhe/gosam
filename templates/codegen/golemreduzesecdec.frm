Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Load GoSam result
#include- l`LOOPS'.log;

G l`LOOPS' = l`LOOPS';
.sort:sum;

#include- reduzereduction-`LOOPS'.hh
.sort:reduce;

#Call FactorDimSecDec
.sort:factor dim;

* Can not do this as you have Den^2*DenStore and you just add up their arguments!

*** WARNING NOT GENERALLY TRUE !!!!! ***
* SIMPLIFY A FEW THINGS *
*Multiply replace_(wH,0);
*.sort

Multiply prf(1,1);
Repeat Id Den(sDUMMY1?)*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY2,sDUMMY1*sDUMMY3);
Repeat Id sDUMMY1?*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY1*sDUMMY2,sDUMMY3);
.sort:feed prf;

Id SCREEN(sDUMMY1?) = sDUMMY1;
.sort:unscreen;

PolyRatFun prf;
.sort:prf;

Bracket ProjLabel,PREFACTOR,COLORFACTOR;
.sort
#Write <`OUTFILE'STUFF.txt>, "%E", l`LOOPS'
print+s;
.sort

* Compute the leading pole multiplying each integral
* Drop integrals which contribute to the amplitude at O(epsS^{`ORD+1})

#Call ExpandDimSecDec({`ORD'})

PolyRatFun;
.sort:no prf;

B INT,epsS;
.sort:bracket;
Collect SCREEN;
.sort:collect;
Id SCREEN(?head)=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;

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
Id INT(?head)*SCREEN(sDUMMY1?) = INT(?head,[],-sDUMMY1);

* Export Integrals to SecDec
#Call TagIntReduze
#Call TagToPropListSecDec
#Call IntToSecDec()
.sort:tosecdec;

#Write <`OUTFILE'secdec.txt>, "+ %E", l`LOOPS'
print+s;
.end
