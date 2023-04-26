#-
off statistics;

Vectors Q,k1,k2,k3,l3,k4,l4,e1,e2;
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
  CFunction j;
  CTensor ptens;
  Vector Q, p1;
  Vector qshift;
  CFunction fshift;

CF abb`DIAG';
Symbol Qt2,QspQ,Qspk1,Qspk2,Qspk3,Qspl3,Qspk4,Qspl4,Qspe1,Qspe2,Qspvak1k2,Qspvak1l3,Qspvak1l4,Qspvak2k1,Qspvak2l3,Qspvak2l4,Qspval3k1,Qspval3k2,Qspval3l4,Qspval4k1,Qspval4k2,Qspval4l3,Qspvak1e1,Qspvae1k1,Qspvak1e2,Qspvae2k1,Qspvak2e1,Qspvae1k2,Qspvak2e2,Qspvae2k2,Qspval3e1,Qspvae1l3,Qspval3e2,Qspvae2l3,Qspval4e1,Qspvae1l4,Qspval4e2,Qspvae2l4,Qspvae1e2,Qspvae2e1;


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
Format O2,stats=off;
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
