* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

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
Id SCREEN(?head)=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;
#Write <`OUTFILE'integrals.txt>, "%E", sum
print+s;
.end