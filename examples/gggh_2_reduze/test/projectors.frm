#-
Off Statistics;
Format 255;

Symbols dimS;
Dimension dimS;

AutoDeclare Indices iDUMMY;
AutoDeclare Symbols sDUMMY;
AutoDeclare Symbols ProjLabel;
AutoDeclare Symbols ProjCoeff;
Vectors k1,k2,k3,k4;
Symbols mH,es12,es23;
CFunctions inplorentz, Dim, DenDim, ProjDen, ProjNum; 
CFunctions prf;

#Include- ../projectors.hh

L test = 
inplorentz(2,iDUMMY1,k1,0)*
inplorentz(2,iDUMMY2,k2,0)*
inplorentz(2,iDUMMY3,k3,0)*
inplorentz(0,iDUMMY4,k4,mH);

L T1 = test * d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3);
L T2 = test * d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2);
L T3 = test * d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1);
L T4 = test * k3(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3);

#Call ApplyProjectors()
#Call ExpandProjectors()

* Kinematics
Argument ProjNum;
   Id k1.k1 =;
   Id k1.k2 = 1/2 * es12;
   Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
   Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
   Id k2.k2 =;
   Id k2.k3 = 1/2 * es23;
   Id k2.k4 = - 1/2 * es12 - 1/2 * es23;
   Id k3.k3 =;
   Id k3.k4 = 1/2 * es12 - 1/2 * mH^2;
   Id k4.k4 = mH^2;
EndArgument;
.sort

Argument ProjDen;
   Id k1.k1 =;
   Id k1.k2 = 1/2 * es12;
   Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
   Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
   Id k2.k2 =;
   Id k2.k3 = 1/2 * es23;
   Id k2.k4 = - 1/2 * es12 - 1/2 * es23;
   Id k3.k3 =;
   Id k3.k4 = 1/2 * es12 - 1/2 * mH^2;
   Id k4.k4 = mH^2;
EndArgument;
.sort

Id k1.k1 =;
Id k1.k2 = 1/2 * es12;
Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k2 =;
Id k2.k3 = 1/2 * es23;
Id k2.k4 = - 1/2 * es12 - 1/2 * es23;
Id k3.k3 =;
Id k3.k4 = 1/2 * es12 - 1/2 * mH^2;
Id k4.k4 = mH^2;
.sort

Repeat Id ProjNum(sDUMMY1?) = prf(sDUMMY1,1);
Repeat Id ProjDen(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id Dim(sDUMMY1?) = prf(sDUMMY1,1);
Repeat Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id sDUMMY1? = prf(sDUMMY1,1);

.sort

PolyRatFun prf;
.sort
PolyRatFun;
.sort

Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1/sDUMMY2;

print+s T1,T2,T3,T4;
.end
