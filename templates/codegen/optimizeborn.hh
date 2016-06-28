#Procedure OptimizeBorn()
#Create <born.txt>
#Create <born.dat>

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
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <born.txt> "#####Abbreviations"
#write <born.txt> "%O"
#write <born.txt> "#####Diagrams"
#write <born.txt> "amplitude = %e",diagrams;
#write <born.dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure


#Procedure OptimizeCT()
#Create <ct.txt>
#Create <ct.dat>

Symbol [% 
@for elements topolopy.keep.ct %][% 
   @if is_first %]ctdiag[%$_%][% @else %][% 
   @end @if %][%
@end @for %],...,[% 
@for elements topolopy.keep.ct %][% 
   @if is_last %]ctdiag[%$_%][% 
   @end @if %][%
@end @for %];

ExtraSymbols,vector,ctabb;

Local ctdiagrams=[% 
@for elements topolopy.keep.ct %][% 
  @if is_first %][% @else %]
  +[% @end @if %]ctdiag[%$_%][%
@end @for %];

#Call ctdiag
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize ctdiagrams;
#write <ct.txt> "#####Abbreviations"
#write <ct.txt> "%O"
#write <ct.txt> "#####Diagrams"
#write <ct.txt> "ctamplitude = %e",ctdiagrams;
#write <ct.dat> "ctabbrev_terms=`optimmaxvar_'"


#EndProcedure
