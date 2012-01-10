[% ' vim: syntax=golem
 %][%
@for mandelstam non-zero %]
@polynomial [%symbol%];[%
@end @for mandelstam non-zero %][%

@for pairs ordered distinct %]
@polynomial spa[%
   @if is_lightlike1 %]k[% @else %]l[%
   @end @if %][% index1 %][%
   @if is_lightlike2 %]k[% @else %]l[%
   @end @if %][% index2
   %], spb[% 
   @if is_lightlike1 %]k[% @else %]l[%
   @end @if %][% index1 %][%
   @if is_lightlike2 %]k[% @else %]l[%
   @end @if %][% index2 %];[%
@end @for pairs ordered distinct %]
@polynomial [%
@for repeat num_colors shift=1
	%]c[% $_ %][%
   @if is_last %];[% @else %], [% @end @if %][%
@end @for repeat %][%

@for particles %][%
   @select 2spin
   @case -2 2 %]
@polynomial gauge[% index %]z;[%
   @end @select %][%
@end @for particles %]
