
* Glover/ van der Bij projector A
*Id SCREEN(inplorentz(2,iDUMMY1?,k1,0))*
*   SCREEN(inplorentz(2,iDUMMY2?,k2,0))
*   =
*   d_(iDUMMY1,iDUMMY2)-k2(iDUMMY1)*k1(iDUMMY2)*ProjDen(k1.k2);

* Glover/ van der Bij projector B
Id SCREEN(inplorentz(2,iDUMMY1?,k1,0))*
   SCREEN(inplorentz(2,iDUMMY2?,k2,0))
   =
   d_(iDUMMY1,iDUMMY2)+
   (
      (
         + k3.k3*k2(iDUMMY1)*k1(iDUMMY2)
         - 2*k1.k3*k2(iDUMMY1)*k3(iDUMMY2)
         - 2*k2.k3*k3(iDUMMY1)*k1(iDUMMY2)
      )*ProjDen(k1.k2)
      + 2*k3(iDUMMY1)*k3(iDUMMY2)
   )*(k1.k1+k2.k2+2*k1.k2)*ProjDen((k1.k1+k3.k3+2*k1.k3)*(k2.k2+k3.k3+2*k2.k3)-k3.k3*k3.k3);
