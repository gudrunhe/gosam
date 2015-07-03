#-
#define LOOPS "1"
#include- model.hh
off statistics;

* Symbols for bracketing the diagram (CC) and R2 during optimization
S CC, R2;

  CFunction j;
  CTensor ptens;
  Vector Q, p1;
  Vector qshift;
  CFunction fshift;
#include ../codegen/symbols.hh

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

AutoDeclare Symbol c;
AutoDeclare Vector spva;
S Nfrat;
Indices iDUMMY1, ..., iDUMMY5;
Vectors vDUMMY1, ..., vDUMMY4;
CFunctions fDUMMY1, ..., fDUMMY3;
CTensors d(symmetric);
CTensor ptens;
CTensor SUBSCRIPT;
AutoDeclare Vectors spva;
AutoDeclare Indices idx, iv;
CF dotproduct(symmetric);
CF Wrapper;
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
CF Wrapper;

[%@end @if%]

#define HELS "[% @for helicities generated %][%helicity%][%@if is_last %][%@else%],[%@end @if%][%
@end @for%]"

.sort
#Include abbreviate.hh
#Include ../codegen/replace.hh

#do i={`HELS'}
#Include ../helicity`i'/d`DIAG'h`i'l1.prc
Id c1 = c1h`i';
.sort
Local dh`i'd`DIAG' = diagram`DIAG';[%
@select r2 @case explicit %]
Local R2dh`i'd`DIAG' = R2d`DIAG';[%
@end @select%]
.sort
*drop diagram`DIAG';
#EndDo
.sort
[%@if internal GENERATE_DERIVATIVES %]
#do i={`HELS'}
#Include ../helicity`i'/d`DIAG'h`i'l1d.prc
Id c1 = c1h`i';
.sort
#do irank=0,`RANK'
Local d`irank'h`i'd`DIAG' = d`irank'diagram;
.sort
#EndDo
#EndDo
[%@end @if %]

.sort

Local diagram`DIAG' = 
#do i={`HELS'}
+ dh`i'd`DIAG'
#EndDo
;[%
@select r2 @case explicit %]
Local d`DIAG'R2 =
#Do i={`HELS'}
+ R2dh`i'd`DIAG'*R2
#EndDo
;[%
@end @select%]
.sort


#Create <`OUTFILE'.txt>
#Create <`OUTFILE'.dat>
#Call  OptimizeCode(1) * R2Prefactor already processed at helicity level
#Close <`OUTFILE'.txt>
#Close <`OUTFILE'.dat>


.end
