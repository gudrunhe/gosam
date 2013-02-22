#-
off statistics;
[% 
@if internal GENERATE_DERIVATIVES %]
Vectors Q[%
@for particles %],k[% index %][%
   @if is_massive %],l[% index %][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],e[%index%][%
   @end @for %][%
@end @if %];
Indices iDUMMY1, ..., iDUMMY5;
Vectors vDUMMY1, ..., vDUMMY4;
CFunctions fDUMMY1, ..., fDUMMY3;
CTensors d(symmetric);
CTensor ptens;
CTensor SUBSCRIPT;
AutoDeclare Vectors spva;
AutoDeclare Indices idx, iv;
CF dotproduct(symmetric);
CF Wrapper;[%
@end @if %][%
@if extension qshift%][%
@else %]
  CFunction j;                                                                                                                                               
  CTensor ptens;                                                                                                                                             
  Vector Q, p1;                                                                                                                                              
  Vector qshift;                                                                                                                                             
  CFunction fshift;
[%@end @if %]
V abb`DIAG';
Symbol Qt2,QspQ[%
@for particles %],Qspk[% index %][%
   @if is_massive %],Qspl[% index %][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],Qspe[%index%][%
   @end @for %][%
@end @if %][%
@for pairs distinct %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %],Qspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%@end @if %][%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
            is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspvae[%index1%]e[%index2%],Qspvae[%index2%]e[%index1%][%
      @end @if %][%
   @end @for %][%
@end @if %];

[%@if internal GENERATE_DERIVATIVES %]
#IfNDef `GENERATEDERIVATIVES'
[%@end @if %]

#append <`OUTFILE'.txt>
#append <`OUTFILE'.dat>
ExtraSymbols,vector,acc`DIAG';
#Include `OUTFILE'.prc
Local diag=diagram`DIAG';

Format O[%formopt.level%],stats=off;
.sort
#optimize diag;
#write <`OUTFILE'.txt> "#####Diagram"
#write <`OUTFILE'.txt> "%O"
#write <`OUTFILE'.txt> "brack = %e",diag(diagram`DIAG');
#write <`OUTFILE'.dat> "diagram_terms=`optimmaxvar_'";

#Close <`OUTFILE'.dat>
#Close <`OUTFILE'.txt>

.sort
[%@if internal GENERATE_DERIVATIVES %]
#Else
#Append <`OUTFILE'.dat>
#Append <`OUTFILE'd.txt>

#include- `OUTFILE'd.hh #d`RANK'diagram
.sort
ExtraSymbols,vector,acd`DIAG';
Format O[%formopt.level%],stats=off;
#Optimize d`RANK'diagram;
#write <`OUTFILE'd.txt> "#####Derive`RANK'"
#write <`OUTFILE'd.txt> "%O";
#write <`OUTFILE'd.txt> "brack = %e",d`RANK'diagram;
#write <`OUTFILE'.dat> "d`RANK'diagram_terms=`optimmaxvar_'";
#Close <`OUTFILE'd.txt>
#Close <`OUTFILE'.dat>
#EndIf
[%
@end @if %]
.end
