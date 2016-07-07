* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

***** WARNING THE FOLLOWING CODE DOES NOT WORK *****
* #IfDef `MASSCT'
* #Do i = `FIRST', `LAST'
* #include- d`i'h0l`LOOPS'mct.log
* #EndDo
* #Else
* #Do i = `FIRST', `LAST'
* #include- d`i'h0l`LOOPS'.log
* #EndDo
* #EndIf
***** END WARNING *****


[% @for loops_generated %]
* Process sum
* Load GoSam result
#IF (`LOOPS' == [%loop%])
#Do i = {,[%@for elements loop.keep.diagrams %][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
#If x`i' != x
#include- d`i'l`LOOPS'.txt;
#EndIf
#EndDo

G sum =
#Do i = {,[%@for elements loop.keep.diagrams%][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
#If x`i' != x
   + d`i'l`LOOPS'
#EndIf
#EndDo
;
#EndIf

[% @end @for %]

.sort:sum;

Drop;
NDrop sum;
.sort
* Simplify coefficients
PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:noprf;

B INT;
.sort:bracket;
Collect SCREEN;
.sort:collect;

#Write <l`LOOPS'.txt>, "L l`LOOPS' = %e", sum
.sort:writesum;

*
* Write list of integrals
*
Id INT(sDUMMY1?,?tail) = INT(sDUMMY1,[],?tail);
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
#Write <integralsl`LOOPS'.txt>, "+ %E", sum
print+s;
.end
