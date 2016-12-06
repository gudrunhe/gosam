#Define NUMPROJ "4"

#Procedure ApplyProjectors

Id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)*
inplorentz(2,iDUMMY3?,k3,0)*
inplorentz(0,iDUMMY4?,k4,mH) =
+ k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3) * ProjCoeff1
+ k2(iDUMMY1)*k2(iDUMMY2)*k1(iDUMMY3) * ProjCoeff2
+ k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3) * ProjCoeff3
+ k2(iDUMMY1)*k2(iDUMMY3)*k1(iDUMMY2) * ProjCoeff4
+ k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2) * ProjCoeff5
+ k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3) * ProjCoeff6
+ k2(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3) * ProjCoeff7
+ k2(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2) * ProjCoeff8
+ k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3) * ProjCoeff9
+ k2(iDUMMY2)*k2(iDUMMY3)*k1(iDUMMY1) * ProjCoeff10
+ k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1) * ProjCoeff11
+ k2(iDUMMY2)*k1(iDUMMY1)*k1(iDUMMY3) * ProjCoeff12
+ k2(iDUMMY2)*k1(iDUMMY1)*k3(iDUMMY3) * ProjCoeff13
+ k2(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1) * ProjCoeff14
+ k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3) * ProjCoeff15
+ k2(iDUMMY3)*k1(iDUMMY1)*k1(iDUMMY2) * ProjCoeff16
+ k2(iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY2) * ProjCoeff17
+ k2(iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY1) * ProjCoeff18
+ k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2) * ProjCoeff19
+ k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3) * ProjCoeff20
+ k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3) * ProjCoeff21
+ k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2) * ProjCoeff22
+ k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3) * ProjCoeff23
+ k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1) * ProjCoeff24
+ k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3) * ProjCoeff25
+ k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2) * ProjCoeff26
+ k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3) * ProjCoeff27
+ d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)     * ProjCoeff28
+ d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)     * ProjCoeff29
+ d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)     * ProjCoeff30
+ d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)     * ProjCoeff31
+ d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)     * ProjCoeff32
+ d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)     * ProjCoeff33
+ d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)     * ProjCoeff34
+ d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)     * ProjCoeff35
+ d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)     * ProjCoeff36
;

#EndProcedure

#Procedure ExpandProjectors

* k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)
Id ProjCoeff1 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3^2)*ProjDen(k2.k1^2*k2.k3^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1^2*k2.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1*k2.k3^2)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1^2*k2.k3^2)*ProjLabel4
);

* k2(iDUMMY1)*k2(iDUMMY2)*k1(iDUMMY3)
Id ProjCoeff2 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1^2*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k2.k3)*ProjLabel4
);

* k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff3 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1*k2.k3^2)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3^2)*ProjLabel4
);

* k2(iDUMMY1)*k2(iDUMMY3)*k1(iDUMMY2)
Id ProjCoeff4 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1^2*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel3
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel2
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k2.k3)*ProjLabel4
);

* k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)
Id ProjCoeff5 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1*k2.k3^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3^2)*ProjLabel4
);

* k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)
Id ProjCoeff6 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1^2*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k1.k3)*ProjLabel4
);

* k2(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff7 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/8*Dim( 4 -dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)
Id ProjCoeff8 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/8*Dim(dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff9 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3^2*k1.k3)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3^2*k1.k3)*ProjLabel4
);

* k2(iDUMMY2)*k2(iDUMMY3)*k1(iDUMMY1)
Id ProjCoeff10 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1^2*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k2.k3)*ProjLabel4
);

* k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)
Id ProjCoeff11 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1*k2.k3^2)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3^2)*ProjLabel4
);

* k2(iDUMMY2)*k1(iDUMMY1)*k1(iDUMMY3)
Id ProjCoeff12 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1^2*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k1.k3)*ProjLabel4
);

* k2(iDUMMY2)*k1(iDUMMY1)*k3(iDUMMY3)
Id ProjCoeff13 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/8*Dim(dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)
Id ProjCoeff14 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/8*Dim(4 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)
Id ProjCoeff15 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3^2*k1.k3)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3^2*k1.k3)*ProjLabel4
);

* k2(iDUMMY3)*k1(iDUMMY1)*k1(iDUMMY2)
Id ProjCoeff16 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1^2)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1^2*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1^2*k1.k3)*ProjLabel4
);

* k2(iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY2)
Id ProjCoeff17 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/8*Dim(4 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY1)
Id ProjCoeff18 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 - 1/8*Dim(dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3*k1.k3)*ProjLabel4
);

* k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)
Id ProjCoeff19 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3^2*k1.k3)*ProjLabel3
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3^2)*ProjLabel1
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3^2*k1.k3)*ProjLabel4
);

* k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)
Id ProjCoeff20 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3^2)*ProjDen(k2.k1^2*k1.k3^2)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1*k1.k3^2)*ProjLabel3
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1^2*k1.k3)*ProjLabel1
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1^2*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff21 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1*k1.k3^2)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)
Id ProjCoeff22 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1*k1.k3^2)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff23 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3*k1.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)
Id ProjCoeff24 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1*k1.k3^2)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)
Id ProjCoeff25 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3*k1.k3^2)*ProjLabel3
 - 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3^2)*ProjLabel4
);

* k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)
Id ProjCoeff26 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel1
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k1.k3^2)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3*k1.k3^2)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3^2)*ProjLabel4
);

* k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff27 =
(
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3^2*k1.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3*k1.k3^2)*ProjLabel2
 - 1/4*DenDim( - 3 + dimS)*ProjNum(k2.k1^2)*ProjDen(k2.k3^2*k1.k3^2)*ProjLabel3
 + 1/8*Dim( 2 - dimS)*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3^2*k1.k3^2)*ProjLabel4
);

* d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)
Id ProjCoeff28 =
(
 - 1/2*DenDim( - 3 + dimS)*ProjNum(k1.k3)*ProjDen(k2.k1*k2.k3)*ProjLabel1
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel4
);

* d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)
Id ProjCoeff29 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k2.k1)*ProjLabel1
);

* d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)
Id ProjCoeff30 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k2.k3)*ProjLabel1
);

* d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)
Id ProjCoeff31 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k2.k1)*ProjLabel2
);

* d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)
Id ProjCoeff32 =
(
 - 1/2*DenDim( - 3 + dimS)*ProjNum(k2.k3)*ProjDen(k2.k1*k1.k3)*ProjLabel2
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel4
);

* d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)
Id ProjCoeff33 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k1.k3)*ProjLabel2
);

* d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)
Id ProjCoeff34 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k2.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k2.k3)*ProjLabel3
);

* d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)
Id ProjCoeff35 =
(
 - 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k1*k1.k3)*ProjLabel4
 + 1/2*DenDim( - 3 + dimS)*ProjDen(k1.k3)*ProjLabel3
);

* d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)
Id ProjCoeff36 =
(
 - 1/2*DenDim( - 3 + dimS)*ProjNum(k2.k1)*ProjDen(k2.k3*k1.k3)*ProjLabel3
 + 1/4*DenDim( - 3 + dimS)*ProjDen(k2.k3*k1.k3)*ProjLabel4
);

#EndProcedure
