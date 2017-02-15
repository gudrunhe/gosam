#Define NUMPROJ "3"

#Procedure ApplyProjectors


id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)* inplorentz(2,iDUMMY3?,k3,0)*
inplorentz(2,iDUMMY4?,k4,0) =  + DenDim( - 3 + dimS) * ( 3*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*ProjLabel3 - 
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*ProjLabel2 + 
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*ProjLabel3 - 
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*ProjLabel2 + 
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*ProjLabel3 + 
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*ProjLabel3 + 
         3*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*ProjLabel3
          + 3*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^-1*
         ProjLabel3 - k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*
         ProjLabel2 - k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*
         es23^-1*ProjLabel2 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-3*es23^-1*ProjLabel3 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*es23^-1*ProjLabel3 + k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23^-1*ProjLabel3 - k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^-1*ProjLabel2 + 3*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23^-1*
         ProjLabel3 - k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*
         es23^-1*ProjLabel2 - d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*ProjLabel3 + d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-2*ProjLabel2 - d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         es12^-3*ProjLabel3 - d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-3*ProjLabel3 + 5/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 - 1/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*
         ProjLabel2 + 5/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-4*es23*ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 + 5/(es23
          + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23
         *ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel2 + 3/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 3/(es23
          + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*
         ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*ProjLabel3 + 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         ProjLabel2 + 2/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-4*es23*ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 + 2/(es23
          + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*es23
         *ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel2 + 4/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 4/(es23
          + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel2 + 3/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*ProjLabel2 + 2/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-4*es23*ProjLabel3 + 4/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23
         *ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*ProjLabel2 + 3/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*ProjLabel3 - 1/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*
         ProjLabel2 + 4/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-4*es23*ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*ProjLabel3 - 1/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*ProjLabel2 + 3/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*
         ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-2*ProjLabel2 + 3/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 6/(es23
          + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*
         ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel2 + 1/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1
         *ProjLabel2 + 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-2*ProjLabel2 + 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel2 - 2/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         es23^-1*ProjLabel3 - 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel2 - 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel2 + 3/(
         es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 + 1/(
         es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*
         es23^-1*ProjLabel2 + 1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23^-1*
         ProjLabel2 + 1/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*es23^-1*ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23^-1*ProjLabel2 - 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23
         *ProjLabel3 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3
          + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*
         es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*ProjLabel2 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k1(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3
          + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-2*ProjLabel3 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k1(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3
          + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*
         es12^-2*ProjLabel3 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY1)*es12^-2*ProjLabel3 + 6/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23^2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^2*ProjLabel2 + 6/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-4*
         es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-3*es23^2*ProjLabel2 + 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         es23*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-2*es23*ProjLabel2 + 6/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-4*es23^2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY2)*es12^-3*es23^2*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*
         es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 4/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*
         k3(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*
         ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23^2*ProjLabel3 + 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*
         es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel3 + 
         2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel2 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*ProjLabel3 + 
         2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 
         2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 
         3/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*es12^-4*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-3*es23^2*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*es12^-4*es23^2*ProjLabel3 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel2 + 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*
         es23^2*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*
         ProjLabel2 + 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*
         es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23^2*ProjLabel3 + 2/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*ProjLabel3 - 
         2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 
         2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 
         4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-4*es23^2*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23^2*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*
         es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*es23*ProjLabel2 + 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY1)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*
         es23^2*ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-2*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*es23*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 - 2/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23^2*
         ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-2*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         ProjLabel2 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*ProjLabel3 - 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*
         es12^-3*es23*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*
         es12^-1*es23^-1*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel2 - 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1
         *ProjLabel3 + 3/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*ProjLabel3 - 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*
         es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel3 - 2/(es23 + es12)/(es23 + es12
         )*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23^-1*ProjLabel3 - 2/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel2 - 
         2/(es23 + es12)/(es23 + es12)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12
         )*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es23^-1*ProjLabel2
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-2*es23^2*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23
         *ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23
         *ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*ProjLabel2 - 1/(
         es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*
         k1(iDUMMY4)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*
         k1(iDUMMY3)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*
         k3(iDUMMY2)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*
         k1(iDUMMY4)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY3)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*
         k2(iDUMMY1)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY1)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*
         k3(iDUMMY1)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY3)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY2)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*
         k2(iDUMMY1)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*es12^-2*es23*ProjLabel3
          - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*
         k3(iDUMMY1)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*ProjLabel3 + 6/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*es12^-4*es23^3*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*es12^-3*es23^3*ProjLabel2 - 6/(es23 + es12)/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*
         es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^2*
         ProjLabel2 - 6/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23^2*ProjLabel3 + 1/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23^2*ProjLabel2 + 6/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         es23*ProjLabel2 - 6/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^2*ProjLabel2 + 6/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-1*es23*ProjLabel2 + 6/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23*
         ProjLabel2 - 6/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
         *k3(iDUMMY4)*ProjLabel2 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-4*es23^3*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-3*es23^2*ProjLabel3 + 1/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23^2*ProjLabel2 - 3/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-3*es23^2*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*
         es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*es23*
         ProjLabel2 - 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-3*es23^2*ProjLabel3 - 3/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-1*es23*ProjLabel2 + 3/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         es23*ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 + 
         1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*k3(iDUMMY4)*ProjLabel2 - 3/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-3*
         es23^2*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23*ProjLabel2 + 3/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 3/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*ProjLabel2
          + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 + 3/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         ProjLabel2 - 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 3/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
         *k3(iDUMMY4)*es23^-1*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-1
         *ProjLabel2 )

       + DenDim( - 1 + dimS)*DenDim( - 3 + dimS)*DenDim( - 4 + dimS) * (  - 2*
         k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*ProjLabel1 - 
         3*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*ProjLabel1
          + k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*dimS*
         ProjLabel1 - 3*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-2*ProjLabel1 + k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*ProjLabel1 + k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel1
          - 3*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel1 + k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         es23^-1*dimS*ProjLabel1 - 3*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel1 - 2*
         k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1*
         ProjLabel1 - 3*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         es12^-2*ProjLabel1 + k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         es12^-2*dimS*ProjLabel1 - 3*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-2*ProjLabel1 + k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*ProjLabel1 + k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*ProjLabel1 + 
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 3*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel1 - 3*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel1 + 
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 2*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         es12^-1*es23^-1*ProjLabel1 - 2*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-2*ProjLabel1 - 4*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*ProjLabel1 + k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-1*es23^-1*ProjLabel1 + 
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 2*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel1 - 3*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1*dimS*ProjLabel1 - 3*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23^-1*
         ProjLabel1 + k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*
         es23^-1*dimS*ProjLabel1 - 4*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*ProjLabel1 + k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*dimS*ProjLabel1 - 4*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel1
          - 2*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*
         ProjLabel1 - 3*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         es12^-1*es23^-1*ProjLabel1 + k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-1*es23^-1*dimS*ProjLabel1 - 3*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-1*es23^-1*ProjLabel1 + 
         k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 4*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-2*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-2*dimS*ProjLabel1 - 8*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-1*es23^-1*ProjLabel1 + 2*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel1 - 4*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es23^-2*ProjLabel1 + 
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es23^-2*dimS*
         ProjLabel1 - 4*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel1 - 4*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-2*ProjLabel1 + k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-2*dimS*ProjLabel1 - 4*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*
         ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*
         es23^-1*dimS*ProjLabel1 - 4*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es23^-2*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es23^-2*dimS*ProjLabel1 - 2*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es23^-2*ProjLabel1 - 4*k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1*ProjLabel1 + 
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 4*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*
         es23^-2*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*
         es23^-2*dimS*ProjLabel1 - 3*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es23^-2*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es23^-2*dimS*ProjLabel1 - 3*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es23^-2*ProjLabel1 + k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es23^-2*dimS*ProjLabel1 - 4*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23^-1*ProjLabel1 + 
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23^-1*dimS*
         ProjLabel1 - 4*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         es23^-2*ProjLabel1 + k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         es23^-2*dimS*ProjLabel1 - 3*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es23^-2*ProjLabel1 + k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es23^-2*dimS*ProjLabel1 - 3*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es23^-2*ProjLabel1 + k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es23^-2*dimS*ProjLabel1 - 2*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es23^-2*ProjLabel1 - 2*
         d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4)*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4)*dimS*ProjLabel1 + 2*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-1*ProjLabel1 - 
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-1*dimS*ProjLabel1
          + 2*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-1*ProjLabel1
          - d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-1*dimS*
         ProjLabel1 + 2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*
         ProjLabel1 - d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es23^-1*
         ProjLabel1 - d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es23^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-1*
         ProjLabel1 - d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es23^-1*
         ProjLabel1 - d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es23^-1*dimS
         *ProjLabel1 - d_(iDUMMY1,iDUMMY3)*d_(iDUMMY2,iDUMMY4)*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k2(iDUMMY4)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es23^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es23^-1*ProjLabel1 - 
         d_(iDUMMY1,iDUMMY4)*d_(iDUMMY2,iDUMMY3)*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY3)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY2)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es23^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es23^-1*ProjLabel1 + 
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k2(iDUMMY4)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY3)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY1)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es23^-1*ProjLabel1 + 
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es23^-1*ProjLabel1 + 2*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY2)*es12^-1*ProjLabel1 - 
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY2)*es12^-1*dimS*ProjLabel1
          + 2*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*es12^-1*ProjLabel1
          - d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*es12^-1*dimS*
         ProjLabel1 + 2*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-1*
         ProjLabel1 - d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es23^-1*
         ProjLabel1 - d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es23^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es23^-1*
         ProjLabel1 - d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es23^-1*dimS
         *ProjLabel1 + 2*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es23^-1*
         ProjLabel1 - d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es23^-1*dimS
         *ProjLabel1 - 4/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*es23*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*dimS*ProjLabel1 - 4
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*
         es12^-2*es23*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY3)*es12^-2*es23*dimS*ProjLabel1 - 8/(es23 + es12
         )*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-4*es23*dimS*ProjLabel3 + 2/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*
         ProjLabel2 - 2/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*es23*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*dimS*ProjLabel1 - 2
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*dimS*ProjLabel1 + 1/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*dimS*ProjLabel1 - 4/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-2*es23*ProjLabel1 + 1/(es23
          + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-2*es23
         *dimS*ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 2/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23*dimS*
         ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*dimS*ProjLabel2 - 
         1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         es12^-2*es23*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-1*ProjLabel1 + 2/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel1 - 
         1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*dimS*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*ProjLabel1 - 1/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*dimS*
         ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-4*es23*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23*dimS*ProjLabel3 + 3
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*dimS*ProjLabel2 - 1/(es23 + es12
         )*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-2*es23*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-1*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*dimS*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-1*dimS*ProjLabel1 - 12/(
         es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*
         es23*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)
         *k2(iDUMMY4)*es12^-4*es23*dimS*ProjLabel3 - 12/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*dimS*ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel2 + 4/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel2 - 8/(es23
          + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 8/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es23^-1*ProjLabel1 + 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-3*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*dimS*ProjLabel3 + 2/(es23
          + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         ProjLabel2 + 2/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*dimS*ProjLabel1 + 2/(es23
          + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es23^-1*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es23^-1*dimS*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es23^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es23^-1*dimS*ProjLabel1 - 4/(es23
          + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-2*es23
         *ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*es12^-2*es23*dimS*ProjLabel1 - 8/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-4*es23*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-4*es23*dimS*ProjLabel3 + 3/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-3*es23*dimS*ProjLabel2 - 1/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-2*es23*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-1*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*dimS*ProjLabel1 - 8/(es23
          + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*es23
         *ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-4*es23*dimS*ProjLabel3 + 3/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-3*es23*dimS*ProjLabel2 - 1/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-2*es23*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-1*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-1*dimS*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-1*dimS*ProjLabel1 - 12/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*
         es23*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)
         *k2(iDUMMY4)*es12^-4*es23*dimS*ProjLabel3 - 12/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*dimS*ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel2 + 4/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel2 - 8/(es23
          + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 8/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es23^-1*ProjLabel1 + 1/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*dimS*ProjLabel3 + 2/(es23
          + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*
         ProjLabel2 + 2/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*dimS*ProjLabel1 + 2/(es23
          + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es23^-1*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es23^-1*dimS*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*es23^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es23^-1*dimS*ProjLabel1 - 8/(es23
          + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-4*es23
         *ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-4*es23*dimS*ProjLabel3 + 2/(es23 + es12)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*
         ProjLabel2 - 2/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-2*es23*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*es23*dimS*ProjLabel1 - 2
         /(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-1*dimS*ProjLabel1 + 1/(es23 + es12)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-1*dimS*
         ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY1)*es12^-1*dimS*ProjLabel1 - 12/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 3/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23
         *dimS*ProjLabel3 - 12/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*ProjLabel3 + 3/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*dimS*
         ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*dimS*ProjLabel2 + 4
         /(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel2 - 8/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*ProjLabel3 + 
         2/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-3*dimS*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel2 + 2/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel1 - 
         1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*dimS*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 1/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-3*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*dimS*ProjLabel3 + 3/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*dimS*ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*ProjLabel1 + 1/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es23^-1*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*es23^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*dimS*ProjLabel1 - 8/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es23^-1*ProjLabel1 + 2/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY4)*es23^-1*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY4)*es23^-1*dimS*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es23^-1*dimS*ProjLabel1 - 12/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*
         es23*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)
         *k2(iDUMMY3)*es12^-4*es23*dimS*ProjLabel3 - 12/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-3*dimS*ProjLabel3 + 4/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*dimS*
         ProjLabel2 + 4/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-2*dimS*ProjLabel2 - 8/(es23
          + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-3*dimS*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel2 + 2/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*dimS*ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es23^-1*ProjLabel1 - 1/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es23^-1*dimS*
         ProjLabel1 - 8/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-3*ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*dimS*ProjLabel3 + 3/(es23
          + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         ProjLabel2 - 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-2*dimS*ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-1*ProjLabel1 + 1/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es23^-1*
         ProjLabel1 + 2/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*es23^-1*ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es23^-1*dimS*ProjLabel1 - 8/(es23
          + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*
         ProjLabel3 + 2/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-3*dimS*ProjLabel3 + 3/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*ProjLabel2 - 1/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*dimS*
         ProjLabel2 + 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-1*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es23^-1*ProjLabel1 + 2/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*es23^-1*
         ProjLabel1 - 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*es23^-1*dimS*ProjLabel1 + 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*es23^-1*dimS*ProjLabel1 - 12/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*
         es23*ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)
         *k2(iDUMMY4)*es12^-4*es23*dimS*ProjLabel3 - 24/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*ProjLabel3 + 
         6/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*dimS*ProjLabel3 + 4/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*ProjLabel2 - 1/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel2 - 12/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23^-1*dimS*ProjLabel3
          + 8/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-2*ProjLabel2 - 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel2 + 4/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel2 - 12/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-3*dimS*ProjLabel3 - 12/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 + 3/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^-1*dimS*
         ProjLabel3 + 4/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel2 + 4/(es23
          + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel2 - 12/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*dimS*ProjLabel3 - 12/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 + 3/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*
         es23^-1*dimS*ProjLabel3 + 4/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel2 - 1/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*dimS*
         ProjLabel2 + 4/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel2
          - 8/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*
         es12^-2*es23^-1*ProjLabel3 + 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^-1*dimS*ProjLabel3 + 2/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1
         *ProjLabel2 - 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es23^-1*ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*ProjLabel1 - 2/(es23
          + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-2
         *ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12*es23^-2*dimS*ProjLabel1 - 12/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*
         es12^-3*dimS*ProjLabel3 - 12/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^-1*ProjLabel3 + 3/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^-1*dimS*
         ProjLabel3 + 4/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*dimS*ProjLabel2 + 4/(es23
          + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*
         es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23^-1*dimS*ProjLabel2 - 8/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23^-1
         *ProjLabel3 + 2/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*es23^-1*dimS*ProjLabel3 + 3/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel2 - 1/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 
         1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12*
         es23^-2*ProjLabel1 - 8/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 + 2/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23^-1*dimS*
         ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel2
          - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*
         es23^-1*ProjLabel1 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12*es23^-2*ProjLabel1 - 4/(es23 + es12)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-2*
         ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12*es23^-2*dimS*ProjLabel1 - 12/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*ProjLabel3 + 
         3/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         es12^-3*dimS*ProjLabel3 - 12/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23^-1*ProjLabel3 + 3/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23^-1*dimS*
         ProjLabel3 + 4/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*dimS*ProjLabel2 + 4/(es23
          + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*
         es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23^-1*dimS*ProjLabel2 - 8/(es23 + 
         es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23^-1
         *ProjLabel3 + 2/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*es23^-1*dimS*ProjLabel3 + 3/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel2 - 1/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es23^-1*ProjLabel1 - 
         1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12*
         es23^-2*ProjLabel1 - 8/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 + 2/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23^-1*dimS*
         ProjLabel3 + 3/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel2 - 1/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel2
          - 1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*
         es23^-1*ProjLabel1 - 1/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12*es23^-2*ProjLabel1 - 4/(es23 + es12)*
         k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-2*
         ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12*es23^-2*dimS*ProjLabel1 - 8/(es23 + es12)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23^-1*
         ProjLabel3 + 2/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*es23^-1*dimS*ProjLabel3 + 2/(es23 + es12)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23^-1*
         ProjLabel2 - 2/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es23^-1*ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es23^-1*dimS*ProjLabel1 - 2/(es23
          + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12*es23^-2
         *ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12*es23^-2*dimS*ProjLabel1 - 4/(es23 + es12)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12*es23^-2*
         ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12*es23^-2*dimS*ProjLabel1 - 4/(es23 + es12)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12*es23^-2*
         ProjLabel1 + 1/(es23 + es12)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12*es23^-2*dimS*ProjLabel1 - 4/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4)*es12^-2*es23*ProjLabel3 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4)*es12^-2*es23*
         dimS*ProjLabel3 + 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         d_(iDUMMY3,iDUMMY4)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4)*es12^-1*es23*dimS*ProjLabel2
          + 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         es12^-1*es23*ProjLabel1 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*es12^-1*es23*dimS*ProjLabel1 + 4/(es23 + es12
         )*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*dimS*
         ProjLabel2 - 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*
         k3(iDUMMY4)*ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY4)*dimS*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*
         es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY3)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-2*es23*dimS*
         ProjLabel2 - 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*
         k3(iDUMMY3)*ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*dimS*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel3
          - 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*dimS*ProjLabel2 - 2/(es23 + es12
         )*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-1*
         dimS*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS
         *ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*dimS
         *ProjLabel2 + 2/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12*es23^-1*ProjLabel1 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-1*dimS*
         ProjLabel1 - 4/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*d_(iDUMMY2,iDUMMY4)*
         es12^-2*es23*ProjLabel3 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         d_(iDUMMY2,iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*d_(iDUMMY2,iDUMMY4)*es12^-1*es23*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k1(iDUMMY4)*es12^-1*es23
         *ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*
         k2(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY4)*ProjLabel1 + 4/(es23 + 
         es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*
         ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         es12^-1*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 4/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12*es23^-1
         *ProjLabel1 - 4/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*d_(iDUMMY2,iDUMMY3)
         *es12^-2*es23*ProjLabel3 + 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         d_(iDUMMY2,iDUMMY3)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*d_(iDUMMY2,iDUMMY3)*es12^-1*es23*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k1(iDUMMY3)*es12^-1*es23
         *ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*dimS*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY3)*ProjLabel1 + 4/(es23 + 
         es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY2)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*
         k2(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY2)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k3(iDUMMY2)*
         ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         es12^-1*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 4/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY1,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12*es23^-1
         *ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*
         k1(iDUMMY4)*es12^-1*es23*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k2(iDUMMY4)*
         es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY1)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY4)*ProjLabel1 + 4/(es23 + 
         es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*
         ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         es12^-1*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k2(iDUMMY1)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 4/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12*es23^-1
         *ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY3)*es12^-1*es23*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY3)*
         es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY1)*k2(iDUMMY3)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY3)*ProjLabel1 + 4/(es23 + 
         es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*
         k2(iDUMMY1)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k2(iDUMMY1)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k3(iDUMMY1)*
         ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-2*es23*ProjLabel2
          - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         es12^-1*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 4/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY2,iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12*es23^-1
         *ProjLabel1 + 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY2)*es12^-1*es23*ProjLabel1 - 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k1(iDUMMY2)*es12^-1*es23*dimS*
         ProjLabel1 + 4/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k2(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*dimS*
         ProjLabel3 - 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k2(iDUMMY2)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k2(iDUMMY2)*es12^-2*es23*dimS*
         ProjLabel2 - 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k3(iDUMMY2)*ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY1)*k3(iDUMMY2)*dimS*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*
         es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY2)*k2(iDUMMY1)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k2(iDUMMY1)*es12^-2*es23*dimS*
         ProjLabel2 - 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*
         k3(iDUMMY1)*ProjLabel1 + 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY2)*k3(iDUMMY1)*dimS*ProjLabel1 + 4/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3
          - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*dimS*ProjLabel3
          - 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         es12^-2*es23*ProjLabel2 + 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*es23*dimS*ProjLabel2 - 2/(es23 + es12
         )*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-1*
         dimS*ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY2)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-1*dimS
         *ProjLabel2 + 4/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY1)*es12^-2*ProjLabel3 - 1/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY1)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es12^-1*ProjLabel2 + 1/(
         es23 + es12)*d_(iDUMMY3,iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es12^-1*dimS
         *ProjLabel2 + 2/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12*es23^-1*ProjLabel1 - 1/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12*es23^-1*dimS*
         ProjLabel1 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*es12^-2*es23^2*ProjLabel1 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-2*
         es23^2*dimS*ProjLabel1 - 12/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23^2*ProjLabel3 + 3/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY4)*es12^-4*es23^2*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^2*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^2*dimS*ProjLabel2 + 4/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*
         es12^-1*es23*ProjLabel1 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23*dimS*ProjLabel1 - 12
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY3)*es12^-4*es23^2*ProjLabel3 + 3/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-4*es23^2*dimS*
         ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY3)*es12^-3*es23^2*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-3*
         es23^2*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23*ProjLabel1 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*es23*dimS*ProjLabel1 - 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23^2*dimS*ProjLabel3 - 4/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 + 2
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*es12^-3*es23^2*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^2*dimS*
         ProjLabel2 + 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-2*
         es23*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*
         dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23*
         dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*ProjLabel1 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*dimS*
         ProjLabel1 - 12/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY2)*es12^-4*es23^2*ProjLabel3 + 3/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-4*
         es23^2*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*es12^-3*es23^2*ProjLabel2 - 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY2)*es12^-3*es23^2*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23*
         ProjLabel1 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23*dimS*ProjLabel1 - 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)
         *k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23^2*dimS*ProjLabel3
          - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23*dimS*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*es23^2*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-2*
         es23*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*
         k3(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel2 + 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*
         es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 - 2
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23*dimS*
         ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*ProjLabel1 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*dimS*ProjLabel1 - 4/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23^2*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*
         es23*dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*es23^2*ProjLabel2 + 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-2*es23*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*
         es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*dimS*ProjLabel2 + 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*es23*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         es23*dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*ProjLabel1 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*dimS*
         ProjLabel1 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*
         es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 
         4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 + 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*
         es23*dimS*ProjLabel2 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*
         es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*
         es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*
         es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-1*ProjLabel1 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12*es23^-1*dimS*ProjLabel1 - 12/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-4*es23^2*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*es12^-4*es23^2*dimS*ProjLabel3 + 4/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         es12^-3*es23^2*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)
         *k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-3*es23^2*dimS*ProjLabel2
          + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         k3(iDUMMY1)*es12^-1*es23*ProjLabel1 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23*dimS*
         ProjLabel1 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-4*
         es23^2*dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23^2*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*es12^-2*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-3*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 - 2
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         es23*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23*ProjLabel2 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*es23*dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*ProjLabel1 + 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*dimS*ProjLabel1 - 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*es23^2*dimS*ProjLabel3 - 4/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-3*es23*dimS*ProjLabel3 + 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-3*es23^2*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-2*es23*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-3*
         es23*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel2 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY3)*es12^-2*es23*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*dimS*ProjLabel3 - 2/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*
         es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*es23*dimS*ProjLabel2 - 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*ProjLabel1 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*dimS*ProjLabel1 + 4/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*
         es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 + 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*
         es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-1*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23*ProjLabel2 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*es23*dimS*ProjLabel2 - 2/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12*
         es23^-1*ProjLabel1 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-1*dimS*ProjLabel1 - 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-4*es23^2*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*
         es23*dimS*ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*es23^2*ProjLabel2 - 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*es12^-3*es23^2*dimS*ProjLabel2 + 2/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*es23*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-2*es23*dimS*ProjLabel2 + 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*
         es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*es23*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY2)*k3(iDUMMY1)*es12^-3*es23*dimS*ProjLabel3 - 1/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*
         es12^-2*es23*dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*ProjLabel1 + 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*dimS*ProjLabel1 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 2/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*dimS*
         ProjLabel2 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*
         es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-1*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-2*dimS*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-2*es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-1*ProjLabel2 + 
         4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12*
         es23^-1*ProjLabel1 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12*es23^-1*dimS*ProjLabel1 + 4
         /(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-3*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*
         es23*dimS*ProjLabel2 - 2/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-3*es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*
         es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-1*ProjLabel2 + 4/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 2/(es23
          + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*
         es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-2*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-1*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-1*dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*dimS*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*dimS*
         ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12*es23^-1*ProjLabel1 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12*
         es23^-1*dimS*ProjLabel1 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*
         es12^-2*dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*ProjLabel3 + 1/(
         es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel3 + 2/(es23 + es12)/(es23
          + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel2 + 2/(es23 + es12)/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*dimS*ProjLabel3 - 4/(es23 + es12)/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*
         es23^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*ProjLabel2 - 
         4/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*
         es12^-1*es23^-1*dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es23^-1*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel3 + 4/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*
         es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*ProjLabel2 - 4/(es23
          + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*
         es12^-1*es23^-1*dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*ProjLabel2 + 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es23^-1*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*ProjLabel3 + 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-2*dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23^-1*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23^-1*dimS*ProjLabel3 + 1/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*
         es12^-1*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es23^-1*ProjLabel2 - 12/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel3 + 3/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*dimS*
         ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*dimS*
         ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*
         es12^-1*es23^-1*dimS*ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*ProjLabel2 - 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12^-1*dimS*ProjLabel2 + 2/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es23^-1*ProjLabel2 - 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es23^-1*dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1*dimS*ProjLabel3 + 4/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*
         es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es23^-1*dimS*ProjLabel2 - 12/(
         es23 + es12)/(es23 + es12)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*es23^-1*ProjLabel3 + 3/(es23 + es12)/(es23 + es12
         )*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*
         dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es23^-1*ProjLabel2 - 1/(es23 + 
         es12)/(es23 + es12)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         es23^-1*dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*k3(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^2*es23^-2*ProjLabel1 + 1/(
         es23 + es12)/(es23 + es12)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^2*es23^-2*dimS*ProjLabel1 + 4/(es23 + es12)/(es23 + 
         es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-3*es23^2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*es12^-3*es23^2*dimS*ProjLabel3 - 2/(es23 + 
         es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         es12^-2*es23^2*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-2*es23^2*dimS*
         ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23
         *dimS*ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23
         *dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23
         *dimS*ProjLabel3 + 2/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-1*es23
         *dimS*ProjLabel2 + 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY1,iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*dimS*ProjLabel2 + 4/(es23
          + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k1(iDUMMY4)*
         es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k1(iDUMMY4)*es12^-3*es23^2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k1(iDUMMY2)*k1(iDUMMY4)*es12^-2*es23^2*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k1(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY2)*k3(iDUMMY4)*es12^-1*
         es23*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23
         *dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY2)*es12^-1*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*ProjLabel2
          + 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*
         k1(iDUMMY3)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k1(iDUMMY3)*es12^-3*es23^2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k1(iDUMMY2)*k1(iDUMMY3)*es12^-2*es23^2*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k1(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         es23*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k1(iDUMMY3)*k3(iDUMMY2)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k1(iDUMMY3)*k3(iDUMMY2)*es12^-2*es23
         *dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k1(iDUMMY3)*k3(iDUMMY2)*es12^-1*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY1,iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*dimS*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY1,iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*ProjLabel2
          + 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*
         k1(iDUMMY4)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k1(iDUMMY4)*es12^-3*es23^2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY1)*k1(iDUMMY4)*es12^-2*es23^2*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY1)*k3(iDUMMY4)*es12^-1*
         es23*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23
         *dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*es12^-1*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*ProjLabel2
          + 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY3)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k1(iDUMMY3)*es12^-3*es23^2*dimS*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY1)*k1(iDUMMY3)*es12^-2*es23^2*ProjLabel2 - 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*dimS*ProjLabel3 + 1/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY3)*es12^-1*
         es23*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY3)*k3(iDUMMY1)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k1(iDUMMY3)*k3(iDUMMY1)*es12^-2*es23
         *dimS*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k1(iDUMMY3)*k3(iDUMMY1)*es12^-1*es23*ProjLabel2 + 4/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY2,iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*dimS*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY2,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*ProjLabel2
          + 4/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k1(iDUMMY2)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)
         *d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k1(iDUMMY2)*es12^-3*es23^2*dimS*
         ProjLabel3 - 2/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY1)*k1(iDUMMY2)*es12^-2*es23^2*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k1(iDUMMY2)*es12^-2*
         es23^2*dimS*ProjLabel2 - 4/(es23 + es12)/(es23 + es12)*
         d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*ProjLabel3
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*
         k3(iDUMMY2)*es12^-2*es23*dimS*ProjLabel3 + 2/(es23 + es12)/(es23 + 
         es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23*
         ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23*dimS*ProjLabel2 - 4/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY1)*es12^-2*
         es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY2)*k3(iDUMMY1)*es12^-2*es23*dimS*ProjLabel3 + 2/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k1(iDUMMY2)*k3(iDUMMY1)*es12^-1*
         es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k1(iDUMMY2)*k3(iDUMMY1)*es12^-1*es23*dimS*ProjLabel2 + 4/(es23 + es12
         )/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*dimS*ProjLabel3 - 2/(es23 + es12)/(
         es23 + es12)*d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*ProjLabel2
          + 1/(es23 + es12)/(es23 + es12)*d_(iDUMMY3,iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-4*es23^3*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-4*es23^3*dimS*ProjLabel3 + 
         4/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*es12^-3*es23^3*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*es12^-3*es23^3*dimS*ProjLabel2 + 12/(es23 + es12)/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*es23^2*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*
         es12^-3*es23^2*dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         es23^2*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^2*dimS*
         ProjLabel2 + 12/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)
         *k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23^2*ProjLabel3 - 3/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23^2*dimS*ProjLabel3 - 4/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)
         *k3(iDUMMY3)*es12^-2*es23^2*ProjLabel2 + 1/(es23 + es12)/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY3)*
         es12^-2*es23^2*dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23
         *ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)
         *k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 4
         /(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*es23*dimS*ProjLabel2 + 12/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*
         es12^-3*es23^2*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23^2*
         dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^2*
         ProjLabel2 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-2*es23^2*dimS*ProjLabel2 - 
         12/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 3/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)*
         k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23*dimS*
         ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)
         *k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 + 3/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*dimS*ProjLabel3 + 4/(es23 + es12
         )/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k3(iDUMMY2)*
         k3(iDUMMY3)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         es23*dimS*ProjLabel2 + 12/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 
         3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS*ProjLabel3 - 4/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*dimS*ProjLabel2 + 12
         /(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23^2*ProjLabel3 - 3/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*es23^2*dimS*ProjLabel3 - 4/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*
         es12^-2*es23^2*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*es12^-2*es23^2*
         dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23*dimS*ProjLabel3 + 4
         /(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-1*es23*dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*
         es12^-2*es23*ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY2)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*dimS*
         ProjLabel3 + 4/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23*ProjLabel2 - 1/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-1*es23*dimS*ProjLabel2 + 12/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)
         *k3(iDUMMY4)*es12^-1*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*dimS
         *ProjLabel3 - 4/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)
         *k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k3(iDUMMY1)*k3(iDUMMY3)*
         k3(iDUMMY4)*dimS*ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*
         ProjLabel3 + 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*dimS*ProjLabel3 + 4
         /(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-1*es23*ProjLabel2 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*es12^-1*es23*dimS*ProjLabel2 + 12/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*ProjLabel3 - 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*dimS*
         ProjLabel3 - 4/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*ProjLabel2 + 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*
         k3(iDUMMY4)*dimS*ProjLabel2 + 12/(es23 + es12)/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*
         ProjLabel3 - 3/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*dimS*ProjLabel3 - 4/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*ProjLabel2 + 1/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*dimS*
         ProjLabel2 - 12/(es23 + es12)/(es23 + es12)/(es23 + es12)*k3(iDUMMY1)
         *k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel3 + 3/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
         *k3(iDUMMY4)*es23^-1*dimS*ProjLabel3 + 4/(es23 + es12)/(es23 + es12)
         /(es23 + es12)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*
         es23^-1*ProjLabel2 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12*es23^-1*dimS*
         ProjLabel2 )

       + k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*ProjLabel3 + 
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*ProjLabel3 + 
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*es23^-1*
         ProjLabel3 + k2(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         es23^-1*ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 1/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k2(iDUMMY3)*es12^-4*es23*ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*ProjLabel3 - 1/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*
         ProjLabel3 - 1/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-3*ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY2)*
         k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 1/(es23
          + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-4*es23*ProjLabel3 + 1/(es23
          + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY1)*es12^-3*ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-4*es23*ProjLabel3 + 1/(es23
          + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*es12^-3*
         ProjLabel3 + 1/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*es12^-3*ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*ProjLabel3 - 1/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*es23^-1
         *ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k2(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY1)*
         k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*es23^-1*ProjLabel3 - 1/(
         es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*
         ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-2*es23^-1*ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY2)*
         k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*es23^-1*ProjLabel3 - 1/(
         es23 + es12)*k2(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*
         es23^-1*ProjLabel3 - 1/(es23 + es12)*k2(iDUMMY3)*k2(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23^-1*ProjLabel3 + 1/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*
         es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)
         *k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*es12^-4*es23^2*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY2)*es12^-4*es23^2*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY1)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-3*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY1)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-3*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*es12^-4*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY1)*k2(iDUMMY4)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*es12^-3*
         es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*es12^-4*es23^2*ProjLabel3 + 1/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*
         k2(iDUMMY3)*es12^-3*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*es12^-3*es23*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY4)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*
         k2(iDUMMY4)*k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY3)*es12^-2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY3)*
         k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + 
         es12)*k1(iDUMMY2)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*
         k2(iDUMMY1)*k2(iDUMMY2)*es12^-4*es23^2*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*es12^-3*
         es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*es12^-3*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY4)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY3)*k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*
         k3(iDUMMY3)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*es12^-3*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*es12^-2*ProjLabel3 - 
         1/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*es12^-2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*ProjLabel3 + 
         1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY1)*k2(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY3)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*es23^-1
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*k2(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)*k2(iDUMMY1)*k2(iDUMMY4)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1
         *ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*k2(iDUMMY2)*k3(iDUMMY1)*
         k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)
         /(es23 + es12)*k2(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*es23^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)*
         k2(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*es23^-1*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*es12^-4*es23^3*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*
         k1(iDUMMY3)*k3(iDUMMY4)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k1(iDUMMY4)*
         k3(iDUMMY3)*es12^-3*es23^2*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)
         /(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*
         es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY1)*k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY2)*es12^-3*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*
         k1(iDUMMY3)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k1(iDUMMY4)*
         k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-4*
         es23^3*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*es12^-3*es23^2*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*es12^-3*es23^2*ProjLabel3 - 1/(
         es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*
         k2(iDUMMY1)*k3(iDUMMY4)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY4)*es12^-2*
         es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY2)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-3*es23^2*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 - 1/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k1(iDUMMY4)*
         k3(iDUMMY1)*k3(iDUMMY3)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(
         es23 + es12)/(es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*
         k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(
         es23 + es12)*k1(iDUMMY2)*k2(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY2)*
         k3(iDUMMY1)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)
         *k3(iDUMMY2)*es12^-3*es23^2*ProjLabel3 - 1/(es23 + es12)/(es23 + es12
         )/(es23 + es12)*k1(iDUMMY3)*k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*
         es12^-2*es23*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)
         *k1(iDUMMY3)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)*es12^-2*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*es12^-2*es23*ProjLabel3 + 1/(es23
          + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY3)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY4)*es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + 
         es12)/(es23 + es12)*k1(iDUMMY3)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY4)*
         es12^-1*ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*
         k1(iDUMMY4)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-2*es23*
         ProjLabel3 + 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*
         k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*es12^-1*ProjLabel3 + 1/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k1(iDUMMY4)*k3(iDUMMY1)*k3(iDUMMY2)
         *k3(iDUMMY3)*es12^-1*ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23
          + es12)*k2(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es12^-1*
         ProjLabel3 - 1/(es23 + es12)/(es23 + es12)/(es23 + es12)*k2(iDUMMY1)*
         k3(iDUMMY2)*k3(iDUMMY3)*k3(iDUMMY4)*es23^-1*ProjLabel3 - 1/(es23 + 
         es12)/(es23 + es12)/(es23 + es12)*k3(iDUMMY1)*k3(iDUMMY2)*k3(iDUMMY3)
         *k3(iDUMMY4)*es23^-1*ProjLabel3;

#EndProcedure


#Procedure ExpandProjectors

#EndProcedure         

