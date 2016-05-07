
* D dimensional Glover/ van der Bij projectors
Id SCREEN(inplorentz(2,iDUMMY1?,k1,0))*
SCREEN(inplorentz(2,iDUMMY2?,k2,0))*
SCREEN(inplorentz(0,iDUMMY3?,k3,mH))*
SCREEN(inplorentz(0,iDUMMY4?,k4,mH)) =
ProjLabel(Proj1)*
Projector
(
   +1/4*(dimS-2)*DenDim(dimS-3)*
   (
      d_(iDUMMY1,iDUMMY2)-k2(iDUMMY1)*k1(iDUMMY2)*ProjDen(k1.k2)
   )
   -1/4*(dimS-4)*DenDim(dimS-3)*
   (
      d_(iDUMMY1,iDUMMY2)+
      (
         (
            + k3.k3*k2(iDUMMY1)*k1(iDUMMY2)
            - 2*k1.k3*k2(iDUMMY1)*k3(iDUMMY2)
            - 2*k2.k3*k3(iDUMMY1)*k1(iDUMMY2)
         )*ProjDen(k1.k2)
         + 2*k3(iDUMMY1)*k3(iDUMMY2)
      )*(k1.k1+k2.k2+2*k1.k2)*ProjDen((k1.k1+k3.k3+2*k1.k3)*(k2.k2+k3.k3+2*k2.k3)-k3.k3*k3.k3)
   )
)
+ ProjLabel(Proj2)*
Projector
(
   -1/4*(dimS-4)*DenDim(dimS-3)*
   (
      d_(iDUMMY1,iDUMMY2)-k2(iDUMMY1)*k1(iDUMMY2)*ProjDen(k1.k2)
   )
   +1/4*(dimS-2)*DenDim(dimS-3)*
   (
      d_(iDUMMY1,iDUMMY2)+
      (
         (
            + k3.k3*k2(iDUMMY1)*k1(iDUMMY2)
            - 2*k1.k3*k2(iDUMMY1)*k3(iDUMMY2)
            - 2*k2.k3*k3(iDUMMY1)*k1(iDUMMY2)
         )*ProjDen(k1.k2)
         + 2*k3(iDUMMY1)*k3(iDUMMY2)
      )*(k1.k1+k2.k2+2*k1.k2)*ProjDen((k1.k1+k3.k3+2*k1.k3)*(k2.k2+k3.k3+2*k2.k3)-k3.k3*k3.k3)
   )
);

