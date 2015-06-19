* Optimize multiple expressions in one go, see arXiv:1310.7007, section 4.2


* load the one loop diagram expressions to be optimized together[%
@for elements topolopy.keep.virt %]
#Include- d[%$_%]h[%helicity%]l1.exp[%
@end @for %]


#Define helicity "[%helicity%]"


#Define BracketLabelsAndQ "B R2SumLabel,[%
@for elements topolopy.keep.virt
   %]label[%$_%],[%
@end @for %]Qt2,QspQ[%
@for particles %],Qspk[%index%][%
   @if is_massive %],Qspl[%index%][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],Qspe[%index%][%
   @end @for %][%
@end @if %][%
@for pairs distinct %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %],Qspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%@end @if %][%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
            is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspvae[%index1%]e[%index2%],Qspvae[%index2%]e[%index1%][%
      @end @if %][%
   @end @for %][%
@end @if %];"


#Define BracketLabelsOnly "B R2SumLabel,[%
@for elements topolopy.keep.virt
   %]label[%$_%][%
   @if is_last
	%];[%
   @else
	%],[%
   @end @if %][%
@end @for %]"
.sort


#Define diagsum "[%
@for elements topolopy.keep.virt %][%
	@if is_first %]
		  label[%$_%] * diagram[%$_%]
		+ R2SumLabel  *     R2d[%$_%][% 
	@else %]
		+ label[%$_%] * diagram[%$_%]
		+ R2SumLabel  *     R2d[%$_%][%
	@end @if %][%
@end @for %]
;"


#Procedure writeDiagrams() [%
@for elements topolopy.keep.virt %]

L thisdiag = diagsum[label[%$_%]];
`BracketLabelsOnly'
.sort

#write <d[%$_%]h[%helicity%]l1.prc> "L diagram[%$_%]  = %e",thisdiag;[%
@end @for %]

#EndProcedure
