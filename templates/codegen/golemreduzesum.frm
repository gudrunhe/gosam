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
.sort

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
   + diagram`i'
#EndIf
#EndDo
;
#EndIf

.sort:sum;

#Do i = {,[%@for elements loop.keep.diagrams%][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
#If x`i' != x
  Drop diagram`i';
#EndIf
#EndDo

.sort:drop;

[% @end @for %]


#call split(sum,list,INT,D,fDUMMY1)
.sort

#Do coeff = list
  #Ifdef `coeff'
    #call topolyratfun(`coeff',N,D,Den,0 , tmp1,tmp2)
  #EndIf
#EndDo

*
* Write amplitude
*
skip list;
#Do e = {`activeexprnames_'}
  #IfDef `e' 
    #Write <l`LOOPS'.txt>"L `e' = %e" `e'
  #EndIf
#EndDo
.sort

Drop; NDrop sum;
.sort

#call producelist(sum,list,INT)
.sort

Drop sum;
.sort

* Discard prefactors from INT function
Repeat Id INT(sDUMMY1?,?a,[],?b,[],?c) = INT(?a,[],?b,[],?c);
Id Once INT([],?a) = INT(?a);
.sort

* Bring INT to form expected by toreduze.py
Id INT(sDUMMY1?,?a) = INT(sDUMMY1,[],?a);
DropCoefficient;
.sort

*
* Write list of integrals
*
#Write <integralsl`LOOPS'.txt>, "+ %E", list
print+s;
.end




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


