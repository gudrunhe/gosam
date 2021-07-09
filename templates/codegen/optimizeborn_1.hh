#Procedure OptimizeBorn()
#Create <born_1.txt>
#Create <born_1.dat>

Symbol [% 
@for elements topolopy.keep.tree %][% 
   @if is_first %]diag[%$_%][% @else %][% 
   @end @if %][%
@end @for %],...,[% 
@for elements topolopy.keep.tree %][% 
   @if is_last %]diag[%$_%][% 
   @end @if %][%
@end @for %];

ExtraSymbols,vector,abb;

Local diagrams=[% 
@for elements topolopy.keep.tree %][% 
  @if is_first %][% @else %]
  +[% @end @if %]diag[%$_%][%
@end @for %];

#Call borndiag1
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_1.txt> "#####Abbreviations"
#write <born_1.txt> "%O"
#write <born_1.txt> "#####Diagrams"
#write <born_1.txt> "amplitude = %e",diagrams;
#write <born_1.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
