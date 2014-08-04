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


* What follows are contents of the file ninja_opt.frm which comes with
* the Ninja library, slightly modified for GoSam. (T.P.)
S ninjaT, ninjaTi, ninjaX;
S ninjaP, ninjaP0, ninjaP1, ninjaP2;
V ninjaA, ninjaA0, ninjaA1, ninjaE3, ninjaE4; 
S ninjaMu2;
V ninjaQ;


#define EXPANSIONFILE "`OUTFILE'.hh"
#define DIAGN "`LOOPSIZE'"
#define DIAGRANK "`RANK'" 

#Append <`OUTFILE'.dat>
#Append <`OUTFILE'`EXPANSIONCUT'.txt>

#include `EXPANSIONFILE' #ninjaDiag`EXPANSIONID'
Id abb`DIAG'(ninjaP?) = Wrapper(abb`DIAG',ninjaP);
Id ninjaA0?.ninjaA1? = dotproduct(ninjaA0,ninjaA1);
Bracket ninjaT, ninjaX, ninjaMu2;
.sort

ExtraSymbols,vector,acd`DIAG';
Keep Brackets;
Format O[%formopt.level%],stats=off;
#optimize ninjaDiag`EXPANSIONID';
Bracket ninjaT, ninjaX, ninjaMu2;
.sort



#if `EXPANSIONID' == 31

#do tpow={3+`DIAGRANK'-`DIAGN'},2,-1
 #do mupow=0,{3+`DIAGRANK'-`DIAGN'}-`tpow',2
     Local ninjaDiagt`tpow'mu`mupow' = ninjaDiag`EXPANSIONID'[ninjaT^`tpow'*ninjaMu2^{`mupow'/2}];
 #enddo
#enddo
.sort
#write <`OUTFILE'.dat> "nin`EXPANSIONID'diagram_terms=`optimmaxvar_'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "#####Ninja`EXPANSIONID'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "%O";
#do tpow={3+`DIAGRANK'-`DIAGN'},2,-1
 #do mupow=0,{3+`DIAGRANK'-`DIAGN'}-`tpow',2
	 #write <`OUTFILE'`EXPANSIONCUT'.txt> "brack(ninjaidxt`tpow'mu`mupow') =  %e",ninjaDiagt`tpow'mu`mupow';
 #enddo
#enddo

#endif


#if (`EXPANSIONID' == 32) && (`DIAGN' >= 3)

#do tpow=1,0,-1
	#do mupow=0,{3+`DIAGRANK'-`DIAGN'}-`tpow',2
		Local ninjaDiagt`tpow'mu`mupow' = ninjaDiag`EXPANSIONID'[ninjaT^`tpow'*ninjaMu2^{`mupow'/2}];
	#enddo
#enddo
.sort
#write <`OUTFILE'.dat> "nin`EXPANSIONID'diagram_terms=`optimmaxvar_'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "#####Ninja`EXPANSIONID'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "%O";
#do tpow=1,0,-1
	#do mupow=0,{3+`DIAGRANK'-`DIAGN'}-`tpow',2
	 #write <`OUTFILE'`EXPANSIONCUT'.txt> "brack(ninjaidxt`tpow'mu`mupow') =  %e",ninjaDiagt`tpow'mu`mupow';
	#enddo
#enddo

#endif


#if `EXPANSIONID' == 21

#do tpow={2+`DIAGRANK'-`DIAGN'},1,-1
	#do xpow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'
		#do mupow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'-`xpow',2
			Local ninjaDiagt`tpow'x`xpow'mu`mupow' = ninjaDiag`EXPANSIONID'[ninjaT^`tpow'*ninjaX^`xpow'*ninjaMu2^{`mupow'/2}];
		#enddo
	#enddo
#enddo
.sort
#write <`OUTFILE'.dat> "nin`EXPANSIONID'diagram_terms=`optimmaxvar_'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "#####Ninja`EXPANSIONID'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "%O";
#do tpow={2+`DIAGRANK'-`DIAGN'},1,-1
	#do xpow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'
		#do mupow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'-`xpow',2
			#write <`OUTFILE'`EXPANSIONCUT'.txt> "brack(ninjaidxt`tpow'x`xpow'mu`mupow') = %e",ninjaDiagt`tpow'x`xpow'mu`mupow';
		#enddo
	#enddo
#enddo

#endif


#if `EXPANSIONID' == 22

#do tpow=0,0,-1
	#do xpow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'
		#do mupow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'-`xpow',2
			Local ninjaDiagt`tpow'x`xpow'mu`mupow' = ninjaDiag`EXPANSIONID'[ninjaT^`tpow'*ninjaX^`xpow'*ninjaMu2^{`mupow'/2}];
		#enddo
	#enddo
#enddo
.sort
#write <`OUTFILE'.dat> "nin`EXPANSIONID'diagram_terms=`optimmaxvar_'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "#####Ninja`EXPANSIONID'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "%O";
#do tpow=0,0,-1
	#do xpow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'
		#do mupow=0,{2+`DIAGRANK'-`DIAGN'}-`tpow'-`xpow',2
			#write <`OUTFILE'`EXPANSIONCUT'.txt> "brack(ninjaidxt`tpow'x`xpow'mu`mupow') = %e",ninjaDiagt`tpow'x`xpow'mu`mupow';
		#enddo
	#enddo
#enddo

#endif


#if (`EXPANSIONID' == Mu2)

#do tpow=`DIAGRANK'-`DIAGN',0,-1
	Local ninjaDiagt`tpow' = ninjaDiag`EXPANSIONID'[ninjaT^`tpow'];
#enddo
.sort
#write <`OUTFILE'.dat> "nin`EXPANSIONID'diagram_terms=`optimmaxvar_'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "#####Ninja`EXPANSIONID'";
#write <`OUTFILE'`EXPANSIONCUT'.txt> "%O";
#do tpow=`DIAGRANK'-`DIAGN',0,-1
	#write <`OUTFILE'`EXPANSIONCUT'.txt> "brack(ninjaidxt`tpow') = %e",ninjaDiagt`tpow'(ninjaC[ninjaidxt`tpow']);
#enddo

#endif


#Close <`OUTFILE'`EXPANSIONCUT'.txt>
#Close <`OUTFILE'.dat>

.end
