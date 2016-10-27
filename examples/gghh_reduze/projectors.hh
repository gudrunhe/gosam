* D dimensional Glover/ van der Bij projectors

#Define NUMPROJ "2"

#Procedure ApplyProjectors

Id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)*
inplorentz(0,iDUMMY3?,k3,mH)*
inplorentz(0,iDUMMY4?,k4,mH) =
    + d_(iDUMMY1,iDUMMY2)*ProjCoeff1
    + k1(iDUMMY2)*k2(iDUMMY1)*ProjCoeff2
    + k1(iDUMMY2)*k3(iDUMMY1)*ProjCoeff3
    + k2(iDUMMY1)*k3(iDUMMY2)*ProjCoeff4
    + k3(iDUMMY1)*k3(iDUMMY2)*ProjCoeff5
;

#EndProcedure

#Procedure ExpandProjectors

Id ProjCoeff1 =
(
 +1/4*Dim(-2+dimS)*DenDim(-3+dimS)*ProjLabel1
 -1/4*Dim(-4+dimS)*DenDim(-3+dimS)*ProjLabel1
 +1/4*Dim(-2+dimS)*DenDim(-3+dimS)*ProjLabel2
 -1/4*Dim(-4+dimS)*DenDim(-3+dimS)*ProjLabel2
);

Id ProjCoeff2 =
(
 -1/4*Dim(-2+dimS)*DenDim(-3+dimS)*ProjDen(k1.k2)*ProjLabel1
 +1/4*Dim(-4+dimS)*DenDim(-3+dimS)*ProjDen(k1.k2)*ProjLabel2
 -1/4*Dim(-4+dimS)*DenDim(-3+dimS)*ProjNum(k3.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel1
 +1/4*Dim(-2+dimS)*DenDim(-3+dimS)*ProjNum(k3.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel2
);

Id ProjCoeff3 =
(
 +1/2*Dim(-4+dimS)*DenDim(-3+dimS)*ProjNum(k2.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel1
 -1/2*Dim(-2+dimS)*DenDim(-3+dimS)*ProjNum(k2.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel2
);

Id ProjCoeff4 =
(
 +1/2*Dim(-4+dimS)*DenDim(-3+dimS)*ProjNum(k1.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel1
 -1/2*Dim(-2+dimS)*DenDim(-3+dimS)*ProjNum(k1.k3)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel2
);

Id ProjCoeff5 =
(
 -1/2*Dim(-4+dimS)*DenDim(-3+dimS)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel1
 +1/2*Dim(-2+dimS)*DenDim(-3+dimS)*ProjNum(k1.k1+2*k1.k2+k2.k2)*ProjDen(k1.k1*k2.k2+2*k1.k1*k2.k3+k1.k1*k3.k3+2*k1.k3*k2.k2+4*k1.k3*k2.k3+2*k1.k3*k3.k3+k2.k2*k3.k3+2*k2.k3*k3.k3)*ProjLabel2
);

#EndProcedure
