#Procedure OptimizeBorn()
#Create <born_2.txt>
#Create <born_2.dat>

Symbol ,...,;

ExtraSymbols,vector,abb;

Local diagrams=;

#Call borndiag2
Format O2,stats=off;
Brackets c1,...,c1;
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_2.txt> "#####Abbreviations"
#write <born_2.txt> "%O"
#write <born_2.txt> "#####Diagrams"
#write <born_2.txt> "amplitude = %e",diagrams;
#write <born_2.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
