[% ' vim: syntax=golem
%]* vim[%
   ' %]: syntax=form:expandtab:ts=3:sw=3
CFunctions out, outlorentz, outcolor;
CFunctions inp, inplorentz, inpcolor;
CFunctions proplorentz, propcolor;
CFunction vertex;
CFunction abbr;
CTensor SplitLorentzIndex;
CFunction SCREEN;
Function NCSIGN(antisymmetric);
CFunction csqrt;

* Used in the output to keep eps and form factors together
CFunction mulfirst;

CTensors f(antisymmetric), f4, T;

CFunctions C(symmetric), CL(symmetric), CR(symmetric);

CFunctions inv, PREFACTOR, COLORFACTOR, delta(symmetric);
CFunction customSpin2Prop;
CFunction QGRAFSIGN;
CTensor SUBSCRIPT;
NFunction NCOrder;[%
@if extension tracify %]
CFunction antisymm, Qeps;
AutoDeclare S Qeps;[%
@end @if %]
* formfactor(A, B) = A + B/eps
CFunction formfactor, log;

Symbols field1, ..., field5;
Symbols m, TR, NC, NA, eps(-2:2), sign1, ..., sign4;
Symbol sqrt2, Sqrt2, sqrt3, Sqrt3, scale2;
Symbol deltaaxial, deltaOS, deltaHV;

Symbol CYUKAWA, CYUKAWA2, RENLOG;
AutoDeclare Symbol LOGYUK;

Vector ZERO, vDUMMYA;

#If `LOOPS' == 1
   CFunction j;
   CTensor ptens;
   Vector Q, p1;
   Vector qshift;
   CFunction fshift;
#EndIf
[%
@if extension formopt %]
CF dotproduct;
[% @end @if %]
