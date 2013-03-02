#-
* This file takes the input numerator from d*h*l1.txt as a 
* function of abb(:) 
* and outputs the file d*h*l1d.hh which has the 
* exansion of the numerator d`p'diagram

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
Symbols sDUMMY1;
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
CF abb`DIAG';
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


#Create<`OUTFILE'd.hh>
#append <`OUTFILE'.dat>

#Include `OUTFILE'.prc
Local diag=diagram`DIAG';

Id QspQ = Q.Q;[%
@for particles %]
Id Qspk[%index%] = Q.k[%index%];[%
@if is_massive %]
Id Qspl[%index%] = Q.l[%index%];[%
@end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for particles lightlike vector %]
Id Qspe[%index%] = Q.e[%index%];[%
@end @for %][%
@end @if %][%
@for pairs distinct %]
Id Qspva[%
            @if is_lightlike1%]k[%index1%][% @else %]l[%index1%][%
            @end @if %][%
            @if is_lightlike2%]k[%index2%][% @else %]l[%index2%][%
            @end @if %] = Q.spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %];[%
   @end @for %][%
@if internal NUMPOLVEC %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Id Qspva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]e[%
         index2 %] = Q.spva[%
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %];
Id Qspvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][%
          index1 %] = Q.spvae[% index2 %][% 
        @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %];[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
Id Qspvae[%index1%]e[%index2%] = Q.spvae[%index1%]e[%index2%];
Id Qspvae[%index2%]e[%index1%] = Q.spvae[%index2%]e[%index1%];[%
      @end @if %][%
   @end @for %][%
@end @if %]

[%
@if extension qshift %][%
@else %]
Id Q = p1;
#Call shiftmomenta(`DIAG',1)
Id fshift(0) = 0;
Id fshift(?all) = 1;
Id p1 = Q;[%
@end @if %]


.sort
Local d0diagram = diag;
#Do p=1,`RANK'
   Local d`p'diagram = <d(iv1)> *...* <d(iv`p')> * diag;
#EndDo
.sort
Hide diag;
.sort
ToTensor, Functions, Q, ptens;
Repeat;
   Id Once d(iDUMMY1?) * ptens(?indices) =
      fDUMMY1(iDUMMY1) * distrib_(1,1, fDUMMY2, ptens, ?indices);
   Id fDUMMY1(iDUMMY1?) * fDUMMY2(iDUMMY2?) = d_(iDUMMY1, iDUMMY2);
EndRepeat;
.sort
ToVector ptens, Q;
Id d(iDUMMY1?) = 0;
#IfDef `DERIVATIVESATZERO'
   Id Q = 0;
#EndIf
Id d_(iDUMMY1?,iDUMMY2?) = d(iDUMMY1,iDUMMY2);
Id abb`DIAG'(sDUMMY1?) = Wrapper(abb`DIAG',sDUMMY1);
Id vDUMMY1?(iDUMMY1?) = SUBSCRIPT(vDUMMY1, iDUMMY1);
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);
.sort
#Do p=0,`RANK'
   #write <`OUTFILE'd.hh> "*--#[ d`p'diagram:"
   #write <`OUTFILE'd.hh> "L d`p'diagram = %e",d`p'diagram;
   #write <`OUTFILE'd.hh> "*--#] d`p'diagram:"
#EndDo
#Close <`OUTFILE'd.hh>
#Close <`OUTFILE'.dat>
.end
