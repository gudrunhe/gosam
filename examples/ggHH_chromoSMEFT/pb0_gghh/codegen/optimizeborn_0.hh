#Procedure OptimizeBorn()
#Create <born_0.txt>
#Create <born_0.dat>

Symbol diag1,...,diag2;

ExtraSymbols,vector,abb;

Local diagrams=diag1
  +diag2;

#Call borndiag0
Format O2,stats=off;
Brackets c1,...,c1;
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_0.txt> "#####Abbreviations"
#write <born_0.txt> "%O"
#write <born_0.txt> "#####Diagrams"
#write <born_0.txt> "amplitude = %e",diagrams;
#write <born_0.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
