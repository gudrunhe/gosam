[% @for parameters R C RP CP %]
	'[%$_%]'[%alignment%] : [%
	@select type
	@case R RP %]'real'[%
	@else %]'complex'[%
	@end @select%],[%
   @end @for %]
[% @for functions R C CA %]
	'[%$_%]' : [%
	@select type
	@case R %]'real'[%
	@else %]'complex'[%
	@end @select%],[%
   @end @for %]
