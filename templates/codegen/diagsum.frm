*[% 
@for elements var=grp diagram_sum %]
*--#[ diag[%grp%]:
Local diagram[%grp%] = [% 
	@for subdiagram_sum group=grp %]
	[% diagram_sign %] diag[%$_%][% 
	@if is_nf %] * Nfrat[% @end @if %][% 
	@end @for %];[%
	@for subdiagram_sum group=grp %]
#include- diagrams-1.hh #diagram[%$_%][%
      @end @for %];
*--#] diag[%grp%]:[% 
      @end @for %]
