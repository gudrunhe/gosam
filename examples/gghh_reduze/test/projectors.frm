Format 255;

AutoDeclare Indices iDUMMY;
AutoDeclare Symbols ProjLabel;
AutoDeclare Symbols ProjCoeff;
Vectors k1,k2,k3,k4;
Symbols mH,dimS;
CFunctions inplorentz, Dim, DenDim, ProjDen, ProjNum; 

#Include- ../projectors.hh

L test = 
inplorentz(2,iDUMMY1,k1,0)*
inplorentz(2,iDUMMY2,k2,0)*
inplorentz(0,iDUMMY3,k3,mH)*
inplorentz(0,iDUMMY4,k4,mH);

#Call ApplyProjectors()
#Call ExpandProjectors()

B ProjLabel1, ProjLabel2, Dim, DenDim;

print+s;
.end
