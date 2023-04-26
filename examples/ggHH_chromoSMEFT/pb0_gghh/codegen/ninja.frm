#-
* This file takes the input numerator from d*h*l1.txt as a
* function of abb(:)
* and outputs the file d*h*l1d.hh which has the
* expansion of the numerator d`p'diagram

off statistics;
Vectors Q,k1,k2,k3,l3,k4,l4,e1,e2;
Vectors vDUMMY1, vDUMMY2;
CTensors d(symmetric);
AutoDeclare Vectors spva;
AutoDeclare Indices idx, iv;
CF dotproduct(symmetric);
CF Wrapper;
S sDUMMY1;
CFunction j;
Vector Q, p1;
*  Vector qshift;
*  CFunction fshift;

CF abb`DIAG';
Symbol Qt2,QspQ,Qspk1,Qspk2,Qspk3,Qspl3,Qspk4,Qspl4,Qspe1,Qspe2,Qspvak1k2,Qspvak1l3,Qspvak1l4,Qspvak2k1,Qspvak2l3,Qspvak2l4,Qspval3k1,Qspval3k2,Qspval3l4,Qspval4k1,Qspval4k2,Qspval4l3,Qspvak1e1,Qspvae1k1,Qspvak1e2,Qspvae2k1,Qspvak2e1,Qspvae1k2,Qspvak2e2,Qspvae2k2,Qspval3e1,Qspvae1l3,Qspval3e2,Qspvae2l3,Qspval4e1,Qspvae1l4,Qspval4e2,Qspvae2l4,Qspvae1e2,Qspvae2e1;

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

Id QspQ = Q.Q;
Id Qspk1 = Q.k1;
Id Qspk2 = Q.k2;
Id Qspk3 = Q.k3;
Id Qspl3 = Q.l3;
Id Qspk4 = Q.k4;
Id Qspl4 = Q.l4;
Id Qspe1 = Q.e1;
Id Qspe2 = Q.e2;
Id Qspvak1k2 = Q.spvak1k2;
Id Qspvak1l3 = Q.spvak1l3;
Id Qspvak1l4 = Q.spvak1l4;
Id Qspvak2k1 = Q.spvak2k1;
Id Qspvak2l3 = Q.spvak2l3;
Id Qspvak2l4 = Q.spvak2l4;
Id Qspval3k1 = Q.spval3k1;
Id Qspval3k2 = Q.spval3k2;
Id Qspval3l4 = Q.spval3l4;
Id Qspval4k1 = Q.spval4k1;
Id Qspval4k2 = Q.spval4k2;
Id Qspval4l3 = Q.spval4l3;
Id Qspvak1e1 = Q.spvak1e1;
Id Qspvae1k1 = Q.spvae1k1;
Id Qspvak1e2 = Q.spvak1e2;
Id Qspvae2k1 = Q.spvae2k1;
Id Qspvak2e1 = Q.spvak2e1;
Id Qspvae1k2 = Q.spvae1k2;
Id Qspvak2e2 = Q.spvak2e2;
Id Qspvae2k2 = Q.spvae2k2;
Id Qspval3e1 = Q.spval3e1;
Id Qspvae1l3 = Q.spvae1l3;
Id Qspval3e2 = Q.spval3e2;
Id Qspvae2l3 = Q.spvae2l3;
Id Qspval4e1 = Q.spval4e1;
Id Qspvae1l4 = Q.spvae1l4;
Id Qspval4e2 = Q.spval4e2;
Id Qspvae2l4 = Q.spvae2l4;
Id Qspvae1e2 = Q.spvae1e2;
Id Qspvae2e1 = Q.spvae2e1;


* T.P. : this should be done numerically, e.g. a -> sign * a - qshift
*Id Q = p1;
*#Call shiftmomenta(`DIAG',1)
*Id fshift(0) = 0;
*Id fshift(?all) = 1;
*Id p1 = Q;



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
