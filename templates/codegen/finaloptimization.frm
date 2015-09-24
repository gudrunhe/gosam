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
@else %][% 
@if extension ninja %]
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
CF dotproduct(symmetric);
CF Wrapper;[%
@end @if %][% @end @if %][%
@if extension qshift%][%
@else %]
  CFunction j;                                                                                                                                               
  CTensor ptens;                                                                                                                                             
  Vector Q, p1;                                                                                                                                              
  Vector qshift;                                                                                                                                             
  CFunction fshift;
[%@end @if %]
CF abb`DIAG';[%
@if extension tracify %]
AutoDeclare S Qeps;
CTensor epstensor;[%
@end @if %]
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
[%@if extension ninja %]
#IfNDef `GENERATENINJAMU'
#IfNDef `GENERATENINJAT2'
#IfNDef `GENERATENINJAT3'
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
[%@if extension ninja %]
** NINJA STUFF
#Else
* GENERATENINJAT3

Vector vecA, vecB, vecC;
Symbol LaurentMu2;
Symbol LaurentP;

#Append <`OUTFILE'.dat>
#Append <`OUTFILE'31.txt>

#include- `OUTFILE'31.hh #nint`LAURIDX'diagram
Id abb`DIAG'(LaurentP?) = Wrapper(abb`DIAG',LaurentP);
Id vecA?.vecB? = dotproduct(vecA,vecB);
Bracket LaurentMu2;

.sort
ExtraSymbols,vector,acd`DIAG';
Keep Brackets;
Format O[%formopt.level%],stats=off;
#Optimize nint`LAURIDX';
Bracket LaurentMu2;

.sort
#Define tpow "{`RANK'-`LAURIDX'}"
Keep Brackets;
Hide;
#Do mupow=0,`RANK'-`tpow',2
      Local nd3Pmu`mupow' = nint`LAURIDX'[LaurentMu2^{`mupow'/2}];
#EndDo
.sort

#write <`OUTFILE'31.txt> "#####NinjaTriangles`LAURIDX'"
#write <`OUTFILE'31.txt> "%O";
#Do mupow=0,`RANK'-`tpow',2
  #write <`OUTFILE'31.txt> "brack(jext`LAURIDX'mu`mupow') = %e",nd3Pmu`mupow';
#EndDo
#write <`OUTFILE'.dat> "nin3t`LAURIDX'diagram_terms=`optimmaxvar_'";
#Close <`OUTFILE'31.txt>
#Close <`OUTFILE'.dat>

#EndIf

#Else
* GENERATENINJAT2

Vector vecA, vecB, vecC, vecA0, vecA1;
Symbol LaurentX1, LaurentMu2;
Symbol LaurentP, LaurentP0, LaurentP1, LaurentP2;

#Append <`OUTFILE'.dat>
#Append <`OUTFILE'32.txt>

#include- `OUTFILE'31.hh #nint`LAURIDX'diagram

Id vecA = vecA0 + vecA1*LaurentX1;
Id LaurentP = LaurentP0 + LaurentP1*LaurentX1 + LaurentP2*LaurentX1^2;
Id vecA1.vecB = 0;
Id vecA1.vecC = 0;
Id abb`DIAG'(LaurentP?) = Wrapper(abb`DIAG',LaurentP);
Id vecA?.vecB? = dotproduct(vecA,vecB);
Bracket LaurentX1, LaurentMu2;

.sort
ExtraSymbols,vector,acd`DIAG';
Keep Brackets;
Format O[%formopt.level%],stats=off;
#Optimize nint`LAURIDX';
Bracket LaurentX1, LaurentMu2;

.sort
#Define tpow "{`RANK'-`LAURIDX'}"
Keep Brackets;
Hide;
#Do xpow=0,`RANK'-`tpow'
#Do mupow=0,`RANK'-`tpow'-`xpow',2
    Local nd3Px`xpow'Pmu`mupow' = nint`LAURIDX'[LaurentX1^{`xpow'}*LaurentMu2^{`mupow'/2}];
#EndDo
#EndDo
.sort

#write <`OUTFILE'32.txt> "#####NinjaBubbles`LAURIDX'"
#write <`OUTFILE'32.txt> "%O";
#Do xpow=0,`RANK'-`tpow'
#Do mupow=0,`RANK'-`tpow'-`xpow',2
  #write <`OUTFILE'32.txt> "brack(jext`LAURIDX'x`xpow'mu`mupow') = %e",nd3Px`xpow'Pmu`mupow';
#EndDo
#EndDo
#write <`OUTFILE'.dat> "nin2t`LAURIDX'diagram_terms=`optimmaxvar_'";
#Close <`OUTFILE'32.txt>
#Close <`OUTFILE'.dat>

#EndIf

#Else
* GENERATENINJAMU

Vector vecA;
Vector vecB;
Symbols LaurentT;

#Append <`OUTFILE'.dat>
#Append <`OUTFILE'21.txt>

#include- `OUTFILE'21.hh #ninddiagram
Bracket LaurentT;
.sort

ExtraSymbols,vector,acd`DIAG';
Format O[%formopt.level%],stats=off;
#Optimize nind;
Bracket LaurentT;
.sort

Keep Brackets;
Hide;
#Do pow=0,`RANK'-`LOOPSIZE', 1
    Local nind`pow' = nind[LaurentT^{`RANK'-`LOOPSIZE'-`pow'}];
#EndDo
.sort

#write <`OUTFILE'21.txt> "#####NinjaMusq"
#write <`OUTFILE'21.txt> "%O";
#Do pow=0,`RANK'-`LOOPSIZE', 1
  #write <`OUTFILE'21.txt> "brack(`pow') = %e",nind`pow';
#enddo
#write <`OUTFILE'.dat> "ninddiagram_terms=`optimmaxvar_'";
#Close <`OUTFILE'21.txt>
#Close <`OUTFILE'.dat>

#EndIf
** END NINJA STUFF
[% @end @if %]

[%@if internal GENERATE_DERIVATIVES %]
#Else
* GENERATEDERIVATIVES
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
