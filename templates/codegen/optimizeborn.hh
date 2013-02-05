#Procedure OptimizeBorn()
#Create <born.txt>

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

#Call borndiag
Format O2,stats=off;
Brackets c1,...,c[% num_colors %];
.sort
Format doublefortran;
#optimize diagrams;
#write <born.txt> "#####Abbreviations"
#write <born.txt> "%O"
#write <born.txt> "#####Diagrams"
#write <born.txt> "diagrams = %e",diagrams;
#EndProcedure
