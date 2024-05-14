#Procedure OptimizeEFTCT()
#Create <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].txt>
#Create <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].dat>

Symbol [% 
@for elements topolopy.keep.ct %][%
   @if is_first %]diag[%$_%][% @else %][% 
   @end @if %][%
@end @for %],...,[% 
@for elements topolopy.keep.ct %][%
   @if is_last %]diag[%$_%][% 
   @end @if %][%
@end @for %];

ExtraSymbols,vector,abb;

Local diagrams=[% 
@for elements topolopy.keep.ct %][%
  @if is_first %][% @else %]
  +[% @end @if %]diag[%$_%][%
@end @for %];

#Call eftctdiag[% @if use_order_names %][% trnco %][% @end @if %]
Format O[%formopt.level%],stats=off;
Brackets c1,...,c[% num_colors %];
.sort
*Format doublefortran;
#optimize diagrams;
#write <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].txt> "#####Abbreviations"
#write <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].txt> "%O"
#write <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].txt> "#####Diagrams"
#write <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].txt> "amplitude = %e",diagrams;
#write <eft_ct[% @if use_order_names %]_[% trnco %][% @end @if %].dat> "abbrev_terms=`optimmaxvar_'"


#EndProcedure
