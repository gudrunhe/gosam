[% @for mandelstam non-zero sym_prefix=es %]
	[%symbol%] : real;[%
   @end @for mandelstam non-zero %]
[% @for pairs ordered distinct %]
	spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
	%], spb[% 
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
        %] : complex;[%
   @end @for pairs ordered distinct %]
[% @for particles %]
	k[%index%][% @if is_lightlike%][% @else %], l[%index%][%
	   @end @if
	%] : vector;[%

	@select 2spin
	@case -2 2 %]
	gauge[% index %]z : complex;[%
	@end @select %][%

   @end @for particles %]
[% @for repeat num_colors shift=1 %]
	c[% $_ %] : color;[%
   @end @for repeat %]
