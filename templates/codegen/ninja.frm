#-
* This file takes the input numerator from d*h*l1.txt as a 
* function of abb(:) 
* and outputs the file d*h*l1d.hh which has the 
* exansion of the numerator d`p'diagram

off statistics;
[% 
@if internal GENERATE_NINJA_TRIPLE %]
Vectors Q[%
@for particles %],k[% index %][%
   @if is_massive %],l[% index %][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],e[%index%][%
   @end @for %][%
@end @if %];
Vectors vDUMMY1, vDUMMY2;
CTensors d(symmetric);
AutoDeclare Vectors spva;
AutoDeclare Indices idx, iv;
CF dotproduct(symmetric);
CF Wrapper;
S sDUMMY1;[%
@end @if %][%
@if extension qshift%][%
@else %]
  CFunction j;
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


#Include `OUTFILE'.prc

* TP: Hide diagram`DIAG'
.sort
Hide;
.sort

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

* TP: store this expression for usage in triple and double ninja
.sort
Hide;
.sort

********************
* TP: triple ninja *
********************
Vectors vecA, vecB, vecC;
Symbol LaurentT, LaurentTi;

L nd3 = diag;

* TP: from old golem.frm
Id Q = vecA + vecC * LaurentTi + vecB * LaurentT;
Id LaurentT * LaurentTi = 1;
Id vecB.vecB = 0;
Id vecC.vecC = 0;

* TP: symplification
Id LaurentTi = 0;

Id abb`DIAG'(sDUMMY1?) = Wrapper(abb`DIAG',sDUMMY1);
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);

* TP: from old golem.frm
*#Define MINLaurentT "{{`LOOPSIZE'-3}-{`GLOOPSIZE'-`LOOPSIZE'}}"
* TP: CHECK!!!
#If `LOOPSIZE' > 3
   #Define MINLaurentT "{`LOOPSIZE'-3}"
#Else
   #Define MINLaurentT "0"
#Endif
#Define MAXLaurentT "`RANK'"

* TP: the following is taken from the old golem.frm, and modified by
* using only LaurentT instead of fDUMMY1
Brackets LaurentT;

.sort
Keep Brackets;
#Do pow=`MINLaurentT',`MAXLaurentT'
* TP: if pow < 0 then do-nothing!
*   #If `pow' < 0
*      Local nd3M{-`pow'} = 0;
*   #Else
*   #If `pow' >= 0
      Local nd3P`pow' = nd3[LaurentT^`pow'];
*   #EndIf
#EndDo

.sort
#Create <`OUTFILE'3.hh>
#Do pow=`MAXLaurentT',`MINLaurentT',-1
* TP: commented, because if pow < 0 then I don't need it
*   #If `pow' < 0
*      #$nd3M{-`pow'}terms = termsin_(nd3M{-`pow'});
*      #If `$nd3M{-`pow'}terms' > 0
*         #Write <`OUTFILE'3.hh> \
*              "nint{`MAXLaurentT'-`pow'}=%e",nd3M{-`pow'}
*      #Else
*         #Write <`OUTFILE'3.hh> \
*              "nint{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
*      #EndIf
*   #Else
**TP      #$nd3P{`pow'}terms = termsin_(nd3P{`pow'});
**TP      #If `$nd3P`pow'terms' > 0
         #write <`OUTFILE'3.hh> "*--#[ nint{`MAXLaurentT'-`pow'}diagram:"
         #Write <`OUTFILE'3.hh> \
              "L nint{`MAXLaurentT'-`pow'}=%e",nd3P{`pow'}
         #write <`OUTFILE'3.hh> "*--#] nint{`MAXLaurentT'-`pow'}diagram:"
**TP      #Else
**TP         #write <`OUTFILE'3.hh> "*--#[ nint{`MAXLaurentT'-`pow'}diagram:"
**TP         #Write <`OUTFILE'3.hh> \
**TP              "L nint{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
**TP         #write <`OUTFILE'3.hh> "*--#] nint{`MAXLaurentT'-`pow'}diagram:"
**TP      #EndIf
*   #EndIf
#EndDo
#Close <`OUTFILE'3.hh>

.sort
Hide;
.sort



********************
* TP: double ninja *
********************
#Create <`OUTFILE'2.hh>

* TP: only needed for LOOPSIZE == RANK
#If `LOOPSIZE' == `RANK'

Vector vecA;
Symbols LaurentT, beta;
L nd2 = diag;

Id Q = vecA * LaurentT;[%
@select r2 @case implicit %]
Id Qt2 = vecA.vecA * LaurentT^2;[%
@end @select %]
Id abb`DIAG'(sDUMMY1?) = Wrapper(abb`DIAG',sDUMMY1);
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);

#Define MINLaurentT "`LOOPSIZE'"
#Define  MAXLaurentT "`LOOPSIZE'"

Brackets LaurentT;
.sort
Keep Brackets;
#Do pow=`MINLaurentT',`MAXLaurentT'
   Local nd2P`pow' = nd2[LaurentT^`pow'];
#EndDo
.sort

#Do pow=`MAXLaurentT',`MINLaurentT',-1
**TP   #$nd2P`pow'terms = termsin_(nd2P`pow'); 
**TP   #If `$nd2P`pow'terms' > 0
      #write <`OUTFILE'2.hh> "*--#[ nind{`MAXLaurentT'-`pow'}diagram:"
      #Write <`OUTFILE'2.hh> "L nind{`MAXLaurentT'-`pow'}=%e", nd2P`pow'
      #write <`OUTFILE'2.hh> "*--#] nind{`MAXLaurentT'-`pow'}diagram:"
**TP   #Else
**TP      #write <`OUTFILE'2.hh> "*--#[ nind{`MAXLaurentT'-`pow'}diagram:"
**TP      #Write <`OUTFILE'2.hh> "L nind{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
**TP      #write <`OUTFILE'2.hh> "*--#] nind{`MAXLaurentT'-`pow'}diagram:"
**TP   #EndIf
#EndDo

* `LOOPSIZE' == `RANK'
#Else
   #write <`OUTFILE'2.hh> "*--#[ nind0diagram:"
   #Write <`OUTFILE'2.hh> "L nind0=0;"
   #write <`OUTFILE'2.hh> "*--#] nind0diagram:"
#EndIf

#Close <`OUTFILE'2.hh>

.end
