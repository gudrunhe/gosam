#Procedure OptimizeBorn()
#Create <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].txt>
#Create <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].dat>

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

#Call borndiag[% @if enable_truncation_orders %][% trnco %][% @end @if %]
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].txt> "#####Abbreviations"
#write <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].txt> "%O"
#write <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].txt> "#####Diagrams"
#write <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].txt> "amplitude = %e",diagrams;
#write <born[% @if enable_truncation_orders %]_[% trnco %][% @end @if %].dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
