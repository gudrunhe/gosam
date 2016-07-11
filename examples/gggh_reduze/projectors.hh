* D dimensional T. Gehrmann, M. Jaquier, E.W.N. Glover, A. Koukoutsakis (arXiv:1112.3554v1) Projectors
* Q: Do we need an extra minus sign here? Their projectors seem to project -coeff
Id SCREEN(inplorentz(2,iDUMMY1?,k1,0))*
SCREEN(inplorentz(2,iDUMMY2?,k2,0))*
SCREEN(inplorentz(2,iDUMMY3?,k3,0))*
SCREEN(inplorentz(0,iDUMMY4?,k4,mH)) =
ProjLabel(Proj1)*
Projector
(
 -(dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k1.k2)*(2*k2.k3)*(2*k1.k3))*
 (
  k2(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)-1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k2.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)*(2*k1.k2)*ProjDen(2*k1.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k2.k3)*(2*k1.k2)*ProjDen(2*k1.k3)
  )
 - (2*k2.k3)*(dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k1.k3)^2*(2*k1.k2)^2)*
 (
  k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)-k2(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 + (2*k2.k3)*dimS*DenDim(dimS - 3)*ProjDen((2*k1.k2)*(2*k1.k3)^3)*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k1.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 - (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k1.k3)^2*(2*k1.k2))*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)-k2(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k2)+1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k2.k3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k2.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k1.k3)-1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)-1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k1.k2)
  )
 )
+ ProjLabel(Proj2)*
Projector
(
 (2*k1.k3)*dimS*DenDim(dimS - 3)*ProjDen((2*k1.k2)*(2*k2.k3)^3)*
 (
  k2(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)-1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k2.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)*(2*k1.k2)*ProjDen(2*k1.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k2.k3)*(2*k1.k2)*ProjDen(2*k1.k3)
  )
 + (dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k2.k3)*(2*k1.k2)^2)*
 (
  k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)-k2(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 - (dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k1.k2)*(2*k2.k3)*(2*k1.k3))*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k1.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 + (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k2.k3)^2*(2*k1.k2))*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)-k2(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k2)+1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k2.k3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k2.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k1.k3)-1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)-1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k1.k2)
  )
 )
+ ProjLabel(Proj3)*
Projector
(
 (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k2.k3)^2*(2*k1.k2))*
 (
  k2(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)-1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k2.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)*(2*k1.k2)*ProjDen(2*k1.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k2.k3)*(2*k1.k2)*ProjDen(2*k1.k3)
  )
 + (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k1.k3)*(2*k1.k2)^2)*
 (
  k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)-k2(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 - (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k1.k3)^2*(2*k1.k2))*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k1.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 + dimS*DenDim(dimS - 3)*ProjDen((2*k1.k2)*(2*k2.k3)*(2*k1.k3))*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)-k2(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k2)+1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k2.k3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k2.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k1.k3)-1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)-1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k1.k2)
  )
 )
+ ProjLabel(Proj4)*
Projector
(
 (dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k2.k3)*(2*k1.k2)^2)*
 (
  k2(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)-1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k2.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k2(iDUMMY3)*(2*k1.k2)*ProjDen(2*k1.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k2.k3)*(2*k1.k2)*ProjDen(2*k1.k3)
  )
 + (2*k2.k3)*dimS*DenDim(dimS - 3)*ProjDen((2*k1.k3)*(2*k1.k2)^3)*
 (
  k2(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)-k2(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 - (2*k2.k3)*(dimS - 4)*DenDim(dimS - 3)*ProjDen((2*k1.k3)^2*(2*k1.k2)^2)*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k1.k3)-k3(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)*(2*k1.k2)*ProjDen(2*k2.k3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k3)*(2*k1.k2)*ProjDen(2*k2.k3)
  )
 + (dimS - 2)*DenDim(dimS - 3)*ProjDen((2*k1.k3)*(2*k1.k2)^2)*
 (
  k3(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)-k2(iDUMMY1)*k3(iDUMMY2)*k1(iDUMMY3)+1/2*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*(2*k1.k2)+1/2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*(2*k2.k3)-1/2*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*(2*k2.k3)+1/2*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*(2*k1.k3)-1/2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*(2*k1.k3)-1/2*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*(2*k1.k2)
  )
 );