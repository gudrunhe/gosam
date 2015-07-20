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


* Process sum
* Load GoSam result
#IF (`LOOPS' == 1)
#Do i = {[%@for elements topolopy.keep.virt%][%@if eval .not. is_last%][%$_%],[%@end @if%][%@if eval is_last%][%$_%]}[%@end @if%][%@end @for%]
#include- d`i'l`LOOPS'.log;
#EndDo

.sort:prefactors;

G sum =
#Do i = {[%@for elements topolopy.keep.virt%][%@if eval .not. is_last%][%$_%],[%@end @if%][%@if eval is_last%][%$_%]}[%@end @if%][%@end @for%]
   + d`i'l`LOOPS'
#EndDo
;
#EndIf

#IF (`LOOPS' == 2)
#Do i = {[%@for elements topolopy.keep.nnlo_virt%][%@if eval .not. is_last%][%$_%],[%@end @if%][%@if eval is_last%][%$_%]}[%@end @if%][%@end @for%]
#include- d`i'l`LOOPS'.log;
#EndDo

.sort:prefactors;

G sum =
#Do i = {[%@for elements topolopy.keep.nnlo_virt%][%@if eval .not. is_last%][%$_%],[%@end @if%][%@if eval is_last%][%$_%]}[%@end @if%][%@end @for%]
   + d`i'l`LOOPS'
#EndDo
;
#EndIf

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

#Write <`OUTFILE'.log>, "L l`LOOPS' = %e", sum
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
#Write <`OUTFILE'integrals.log>, "+ %E", sum
print+s;
.end

