*[% 
@for elements var=grp diagram_sum %]
*--#[ diag[%grp%]:
Local diagram[%grp%] = 
      [% @for elements diagram_sum group=grp %] + diag[%$_%][%
      @end @for %];[%
      @for elements diagram_sum group=grp %]
#include- diagrams-1.hh #diagram[%$_%][%
      @end @for %];
*--#] diag[%grp%]:
      [% @end @for %]
