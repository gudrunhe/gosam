#Define NUMPROJ "1"

#Procedure ApplyProjectors

Id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)*
inplorentz(0,iDUMMY3?,k3,mH) =
+ d_(iDUMMY1,iDUMMY2)     * ProjCoeff1
+ k2(iDUMMY1)*k1(iDUMMY2) * ProjCoeff2
;

#EndProcedure

#Procedure ExpandProjectors

* d_(iDUMMY1,iDUMMY2)
Id ProjCoeff1 =
(
 DenDim(dimS-2)*ProjLabel1
);

* k2(iDUMMY1)*k1(iDUMMY2)
Id ProjCoeff2 =
(
 - DenDim(dimS-2)*ProjDen(k1.k2)*ProjLabel1
);

#EndProcedure
