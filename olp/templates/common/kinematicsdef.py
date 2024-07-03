kinematics={
[%@for mandelstam non-zero sym_prefix=es %]
	'[%symbol%]' : 'real',[%
@end @for mandelstam non-zero %][%
@for pairs ordered distinct %]
	'spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
	%]' : 'complex', 'spb[% 
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
        %]' : 'complex',[%
@end @for pairs ordered distinct %][%
@for particles %]
	'k[%index%]'[% @if is_lightlike%][% @else %] : 'vector', 'l[%index%]'[%
	   @end @if
	%] : 'vector',[%

	@select 2spin
	@case -2 2 %]
	'gauge[% index %]z' : 'complex',[%
	@end @select %][%
@end @for particles %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %]
	'e[% index %]' : 'cvector',[%
   @end @for %][%
   @for pairs ordered %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	'spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2
	    %]' : 'complex', 'spbe[% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
	 %]' : 'complex',[%
      @end @if %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %]
	'spae[%index1%][%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
	    %]' : 'complex', 'spb[%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]e[%
            index1 %]' : 'complex',[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	'spae[% index1
	    %]e[% index2 %]' : 'complex', 'spbe[% index2 %]e[% index1 %]' : 'complex',[%
      @end @if %][%
   @end @for %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	'spva[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
	    %]e[% index2 %]' : 'cvector', 'spvae[% index2 %][% 
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
	%]' : 'cvector',[%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
	'spvae[% index1
	    %]e[% index2 %]' : 'cvector', 'spvae[% index2 %]e[% index1 %]' : 'cvector',[%
      @end @if %][%
   @end @for %][%
@end @if NUMPOLVEC %][%
@for repeat num_colors shift=1 %]
	'c[% $_ %]' : 'color'[%@if is_last %][%@else%],[%
			@end @if%][%
@end @for repeat %]
}

dotproducts={
		'QspQ' : 'dotproduct(Q,Q)'[%
@for particles %],'Qspk[% index %]' : 'dotproduct(Q,k[%index%])'[%
	@if is_massive %], 'Qspl[% index %]' : 'dotproduct(Q,l[%index%])'[%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
	@for particles lightlike vector %],'Qspe[%index%]' : 'dotproduct(Q,e[%index%])'[%
   @end @for %][%
@end @if %][%
@for pairs distinct %],'Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]' : 'dotproduct(Q,spva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %])'[%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],'Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %]' : 'dotproduct(Q,spva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %])' ,'Qspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %]': 'dotproduct(Q,spvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %])'[%
	   @end @if %][%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
   is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],'Qspvae[%index1%]e[%index2%]' : 'dotproduct(Q,spvae[%index1%]e[%index2%])',
  'Qspvae[%index2%]e[%index1%]' : 'dotproduct(Q,spvae[%index2%]e[%index1%])'[%
      @end @if %][%
   @end @for %][%
@end @if%][%
@if extension tracify%][%
   @for pairs distinct %][%
      @for particles %],
		'Qeps[%@if is_lightlike1%]k[%@else%]l[%@end @if%][%index1%][%@if is_lightlike2%]k[%@else%]l[%@end @if%][%index2%][%@if is_lightlike%]k[%@else%]l[%@end @if%][%index%]' : 'epstensor(Q,[%@if is_lightlike1%]k[%@else%]l[%@end @if%][%index1%],[%@if is_lightlike2%]k[%@else%]l[%@end @if%][%index2%],[%@if is_lightlike%]k[%@else%]l[%@end @if%][%index%])'[%
      @end @for %][%
   @end @for %][%
@end @if %]}

