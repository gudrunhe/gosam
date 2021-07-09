#Procedure OptimizeBorn()
#Create <born_0.txt>
#Create <born_0.dat>

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

#Call borndiag0
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_0.txt> "#####Abbreviations"
#write <born_0.txt> "%O"
#write <born_0.txt> "#####Diagrams"
#write <born_0.txt> "amplitude = %e",diagrams;
#write <born_0.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
