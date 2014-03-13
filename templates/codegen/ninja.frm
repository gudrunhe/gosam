#-
* This file takes the input numerator from d*h*l1.txt as a 
* function of abb(:) 
* and outputs the file d*h*l1d.hh which has the 
* expansion of the numerator d`p'diagram

off statistics;
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
@if extension qshift%][%
@else %]
CFunction j;
Vector Q, p1;
*  Vector qshift;
*  CFunction fshift;
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

S ninjaMu2;
V ninjaQ;
CF ninjaMP;
S ninjaT, ninjaTi, ninjaX;
S ninjaP, ninjaP0, ninjaP1, ninjaP2;
V ninjaA, ninjaA0, ninjaA1, ninjaE3, ninjaE4; 


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
* T.P. : this should be done numerically, e.g. a -> sign * a - qshift
*Id Q = p1;
*#Call shiftmomenta(`DIAG',1)
*Id fshift(0) = 0;
*Id fshift(?all) = 1;
*Id p1 = Q;[%
@end @if %]



* What follows are contents of the file ninja_laurent.frm which comes
* with the Ninja library, slightly modified for GoSam. (T.P.)
*
* Changes w.r.t. ninja_laurent.frm:
* -   `OUTFILE' --> `OUTFILE'.hh

.sort
Hide;
.sort

* Some conversions
#define QVAR "Q"
#define MU2VAR "Qt2"
#define DIAGNAME "diag"
#define DIAGN "`LOOPSIZE'"
#define DIAGRANK "`RANK'" 

S ninjaT, ninjaTi, ninjaX;
S ninjaP, ninjaP0, ninjaP1, ninjaP2;
V ninjaA, ninjaA0, ninjaA1, ninjaE3, ninjaE4; 
S ninjaMu2;
V ninjaQ;

L ninjaDiag = `DIAGNAME';

multiply, replace_(`QVAR',ninjaQ,`MU2VAR',ninjaMu2);

.sort
Hide;
.sort

L ninjaDiag3 = ninjaDiag;

#if `DIAGN' >= 3
multiply, ninjaTi^{`DIAGN'-3};
#else
multiply, ninjaT^{3-`DIAGN'};
#endif

id ninjaQ = ninjaA + ninjaE3*ninjaT + (ninjaP+ninjaMu2)*ninjaTi*ninjaE4;

id ninjaT * ninjaTi = 1;
id ninjaTi = 0;

id ninjaE3.ninjaE3 = 0;
id ninjaE4.ninjaE4 = 0;
id ninjaE3.ninjaE4 = 1/2;

Bracket ninjaT;
.sort

L ninjaDiag31 = 0
#if `DIAGRANK' >= `DIAGN'
+ ninjaDiag3[ninjaT^4]*ninjaT^4
#endif
+ ninjaDiag3[ninjaT^3]*ninjaT^3
+ ninjaDiag3[ninjaT^2]*ninjaT^2;

#if `DIAGN' >= 3
L ninjaDiag32 = ninjaDiag3[ninjaT^1]*ninjaT^1 + ninjaDiag3[ninjaT^0];
#endif

.sort

#write <`OUTFILE'.hh> "*--#[ ninjaDiag31:"
#write <`OUTFILE'.hh> "L ninjaDiag31 = %e", ninjaDiag31;
#write <`OUTFILE'.hh> "*--#] ninjaDiag31:"

#if `DIAGN' >= 3
#write <`OUTFILE'.hh> "*--#[ ninjaDiag32:"
#write <`OUTFILE'.hh> "L ninjaDiag32 = %e", ninjaDiag32;
#write <`OUTFILE'.hh> "*--#] ninjaDiag32:"
#else
#write <`OUTFILE'.hh> "*--#[ ninjaDiag32:"
#write <`OUTFILE'.hh> "L ninjaDiag32 = 0;"
#write <`OUTFILE'.hh> "*--#] ninjaDiag32:"
#endif

.sort
Hide;
.sort

L ninjaDiag2 = ninjaDiag3;

multiply, ninjaTi;
id ninjaT * ninjaTi = 1;
id ninjaTi = 0;

id ninjaA = ninjaA0 + ninjaA1*ninjaX;
id ninjaP = ninjaP0 + ninjaP1*ninjaX + ninjaP2*ninjaX^2;
id ninjaA1.ninjaE3 = 0;
id ninjaA1.ninjaE4 = 0;

Bracket ninjaT;
.sort

L ninjaDiag21 = 0
#if `DIAGRANK' >= `DIAGN'
+ ninjaDiag2[ninjaT^3]*ninjaT^3
#endif
+ ninjaDiag2[ninjaT^2]*ninjaT^2
+ ninjaDiag2[ninjaT]*ninjaT;

L ninjaDiag22 = ninjaDiag2[ninjaT^0];

.sort

#write <`OUTFILE'.hh> "*--#[ ninjaDiag21:"
#write <`OUTFILE'.hh> "L ninjaDiag21 = %e", ninjaDiag21;
#write <`OUTFILE'.hh> "*--#] ninjaDiag21:"

#write <`OUTFILE'.hh> "*--#[ ninjaDiag22:"
#write <`OUTFILE'.hh> "L ninjaDiag22 = %e", ninjaDiag22;
#write <`OUTFILE'.hh> "*--#] ninjaDiag22:"

.sort

#if (`DIAGRANK' >= `DIAGN') && (`DIAGN' >= 4)

Hide;
.sort

L ninjaDiagMu2 = ninjaDiag * ninjaTi^{`DIAGN'};

id ninjaQ = ninjaA0 * ninjaT
#if (`DIAGRANK' > `DIAGN')
 + ninjaA1
#endif
;
id ninjaMu2 = ninjaA0.ninjaA0 * ninjaT^2;
id ninjaT * ninjaTi = 1;
id ninjaTi = 0;

.sort

#write <`OUTFILE'.hh> "*--#[ ninjaDiagMu2:"
#write <`OUTFILE'.hh> "L ninjaDiagMu2 = %e", ninjaDiagMu2;
#write <`OUTFILE'.hh> "*--#] ninjaDiagMu2:"

#else

#write <`OUTFILE'.hh> "*--#[ ninjaDiagMu2:"
#write <`OUTFILE'.hh> "L ninjaDiagMu2 = 0;"
#write <`OUTFILE'.hh> "*--#] ninjaDiagMu2:"

#endif

.end
