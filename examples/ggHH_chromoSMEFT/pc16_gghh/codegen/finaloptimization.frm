#-
off statistics;

Vectors Q,k1,k2,k3,l3,k4,l4,e1,e2;
Indices iDUMMY1, ..., iDUMMY5;
Vectors vDUMMY1, ..., vDUMMY4;
CFunctions fDUMMY1, ..., fDUMMY3;
CTensors d(symmetric);
CTensor ptens;
CTensor SUBSCRIPT;
AutoDeclare Vectors spva;
AutoDeclare Indices idx, iv;
CF dotproduct(symmetric);
CF Wrapper;
  CFunction j;
  CTensor ptens;
  Vector Q, p1;
  Vector qshift;
  CFunction fshift;

CF abb`DIAG';
Symbol Qt2,QspQ,Qspk1,Qspk2,Qspk3,Qspl3,Qspk4,Qspl4,Qspe1,Qspe2,Qspvak1k2,Qspvak1l3,Qspvak1l4,Qspvak2k1,Qspvak2l3,Qspvak2l4,Qspval3k1,Qspval3k2,Qspval3l4,Qspval4k1,Qspval4k2,Qspval4l3,Qspvak1e1,Qspvae1k1,Qspvak1e2,Qspvae2k1,Qspvak2e1,Qspvae1k2,Qspvak2e2,Qspvae2k2,Qspval3e1,Qspvae1l3,Qspval3e2,Qspvae2l3,Qspval4e1,Qspvae1l4,Qspval4e2,Qspvae2l4,Qspvae1e2,Qspvae2e1;


#IfNDef `GENERATEDERIVATIVES'



#append <`OUTFILE'.txt>
#append <`OUTFILE'.dat>
ExtraSymbols,vector,acc`DIAG';
#Include `OUTFILE'.prc
Local diag=diagram`DIAG';

Format O2,stats=off;
.sort
#optimize diag;
#write <`OUTFILE'.txt> "#####Diagram"
#write <`OUTFILE'.txt> "%O"
#write <`OUTFILE'.txt> "brack = %e",diag(diagram`DIAG');
#write <`OUTFILE'.dat> "diagram_terms=`optimmaxvar_'";

#Close <`OUTFILE'.dat>
#Close <`OUTFILE'.txt>

.sort



#Else
* GENERATEDERIVATIVES
#Append <`OUTFILE'.dat>
#Append <`OUTFILE'd.txt>

#include- `OUTFILE'd.hh #d`RANK'diagram
.sort
ExtraSymbols,vector,acd`DIAG';
Format O2,stats=off;
#Optimize d`RANK'diagram;
#write <`OUTFILE'd.txt> "#####Derive`RANK'"
#write <`OUTFILE'd.txt> "%O";
#write <`OUTFILE'd.txt> "brack = %e",d`RANK'diagram;
#write <`OUTFILE'.dat> "d`RANK'diagram_terms=`optimmaxvar_'";
#Close <`OUTFILE'd.txt>
#Close <`OUTFILE'.dat>
#EndIf

.end
