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

* Load result
#If (`LOOPS' == [%loop%])

  #Do i = {,[%@for elements loop.keep.diagrams %][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
    #If x`i' != x
      #include- d`i'l`LOOPS'.txt;
    #EndIf
  #EndDo
 
  G l`LOOPS' =
  #Do i = {,[%@for elements loop.keep.diagrams%][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
    #If x`i' != x
      + diagram`i'
    #EndIf
  #EndDo
  ;
  .sort:sum;

  #Do i = {,[%@for elements loop.keep.diagrams%][%@if is_last%][%$_%]}[% @else %][%$_%],[%@end @if%][%@end @for%]
    #If x`i' != x
      Drop diagram`i';
    #EndIf
  #EndDo
  .sort:drop;

#EndIf

[% @end @for %]

* Split expression into separate expressions
#call split(l`LOOPS',list,INT,D,fDUMMY1)
.sort

* Split numerators and denominators into separate expressions
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
    #Write <l`LOOPS'.txt> "L `e' = %e" `e'
  #EndIf
#EndDo
.sort

* Produce list of integrals
Drop; NDrop l`LOOPS';
.sort
#call producelist(l`LOOPS',list,INT)
.sort
Drop l`LOOPS';
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
.end
