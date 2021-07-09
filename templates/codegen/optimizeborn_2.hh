#Procedure OptimizeBorn()
#Create <born_2.txt>
#Create <born_2.dat>

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

#Call borndiag2
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <born_2.txt> "#####Abbreviations"
#write <born_2.txt> "%O"
#write <born_2.txt> "#####Diagrams"
#write <born_2.txt> "amplitude = %e",diagrams;
#write <born_2.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
