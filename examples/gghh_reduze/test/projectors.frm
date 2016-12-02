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
inplorentz(0,iDUMMY3,k3,mH)*
inplorentz(0,iDUMMY4,k4,mH);

L T1 = test * (d_(iDUMMY1,iDUMMY2) - k2(iDUMMY1)*k1(iDUMMY2)*ProjDen(k1.k2));

L T2 = test * 
(     + d_(iDUMMY1,iDUMMY2) 
      + k2(iDUMMY1)*k1(iDUMMY2)*ProjNum(k3.k3)*
        ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)
      - 2*k2(iDUMMY1)*k3(iDUMMY2)*ProjNum(k1.k3)*
        ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)
      - 2*k3(iDUMMY1)*k1(iDUMMY2)*ProjNum(k2.k3)*
        ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)
      + 2*k3(iDUMMY1)*k3(iDUMMY2)*
        ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)
);

#Call ApplyProjectors()
#Call ExpandProjectors()

* Kinematics
Argument ProjNum;
Id k1.k1 =;
Id k1.k2 = 1/2 * es12;
Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k2 =;
Id k2.k3 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k4 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k3.k3 = mH^2;
Id k3.k4 = 1/2 * es12 - 1/2 * mH^2 - 1/2 * mH^2;
Id k4.k4 = mH^2;
EndArgument;
.sort

Argument ProjDen;
Id k1.k1 =;
Id k1.k2 = 1/2 * es12;
Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k2 =;
Id k2.k3 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k4 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k3.k3 = mH^2;
Id k3.k4 = 1/2 * es12 - 1/2 * mH^2 - 1/2 * mH^2;
Id k4.k4 = mH^2;
EndArgument;
.sort

Id k1.k1 =;
Id k1.k2 = 1/2 * es12;
Id k1.k3 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k1.k4 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k2 =;
Id k2.k3 = - 1/2 * mH^2 + 1/2 * es23;
Id k2.k4 = - 1/2 * es12 + 1/2 * mH^2 - 1/2 * es23;
Id k3.k3 = mH^2;
Id k3.k4 = 1/2 * es12 - 1/2 * mH^2 - 1/2 * mH^2;
Id k4.k4 = mH^2;
.sort

Id ProjNum(sDUMMY1?) = prf(sDUMMY1,1);
Id ProjDen(sDUMMY1?) = prf(1,sDUMMY1);
Id Dim(sDUMMY1?) = prf(sDUMMY1,1);
Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id sDUMMY1? = prf(sDUMMY1,1);

.sort

PolyRatFun prf;
.sort
PolyRatFun;
.sort

Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1/sDUMMY2;

print+s T1,T2;
.end
