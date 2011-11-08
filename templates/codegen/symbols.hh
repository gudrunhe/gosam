
CFunctions out, outlorentz, outcolor;
CFunctions inp, inplorentz, inpcolor;
CFunctions proplorentz, propcolor;
CFunction vertex;
CFunction abbr;
CFunction SplitLorentzIndex;
CFunction SCREEN;
Function NCSIGN(antisymmetric);

* Used in the output to keep eps and form factors together
CFunction mulfirst;

CTensors f(antisymmetric), f4, T;

CFunctions C(symmetric), CL(symmetric), CR(symmetric);

CFunctions inv, PREFACTOR, COLORFACTOR, delta(symmetric);
CFunction QGRAFSIGN;
NFunction NCOrder;

* formfactor(A, B) = A + B/eps
CFunction formfactor, log;

Symbols field1, ..., field5;
Symbols m, TR, NC, NA, eps(-2:2), sign1, ..., sign4;
Symbol sqrt2, Sqrt2, sqrt3, Sqrt3, scale2;
Symbol deltaaxial, deltaOS, deltaHV;

Vector ZERO, vDUMMYA;

#If `LOOPS' == 1
	CFunction j;
	CTensor ptens;
	Vector Q;
#EndIf

AutoDeclare Indices idx, iv;
AutoDeclare CFunctions Lor;
