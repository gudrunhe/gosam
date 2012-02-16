[%
@for mandelstam non-zero sym_prefix=es %]
	[%symbol%] : real;[%
@end @for mandelstam non-zero %][%
@for pairs ordered distinct %]
	spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
	%], spb[% 
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
        %] : complex;[%
@end @for pairs ordered distinct %][%
@for particles %]
	k[%index%][% @if is_lightlike%][% @else %], l[%index%][%
	   @end @if
	%] : vector;[%

	@select 2spin
	@case -2 2 %]
	gauge[% index %]z : complex;[%
	@end @select %][%
@end @for particles %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	e[% index %] : cvector;[%
   @end @for %][%
   @for pairs ordered %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2
            %], spbe[% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
	 %] : complex;[%
      @end @if %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %]
	spae[%index1%][%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %], spb[%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]e[%
            index1 %] : complex;[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	spae[% index1
            %]e[% index2 %], spbe[% index2 %]e[% index1 %] : complex;[%
      @end @if %][%
   @end @for %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	spva[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %], spvae[% index2 %][% 
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
	%] : cvector;[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	spvae[% index1
            %]e[% index2 %], spvae[% index2 %]e[% index1 %] : cvector;[%
      @end @if %][%
   @end @for %][%
@end @if NUMPOLVEC %][%
@for repeat num_colors shift=1 %]
	c[% $_ %] : color;[%
@end @for repeat %]
