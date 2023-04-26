#Procedure OptimizeBorn()
#Create <born_1.txt>
#Create <born_1.dat>

Symbol diag1,...,diag2;

ExtraSymbols,vector,abb;

Local diagrams=diag1
  +diag2;

#Call borndiag1
Format O2,stats=off;
Brackets c1,...,c1;
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_1.txt> "#####Abbreviations"
#write <born_1.txt> "%O"
#write <born_1.txt> "#####Diagrams"
#write <born_1.txt> "amplitude = %e",diagrams;
#write <born_1.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
