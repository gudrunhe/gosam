[% ' # vim: ts=3:sw=3:syntax=golem
%]#procedure spva
* vim[% ' %]: syntax=form
[% @for pairs distinct %]
   Id Spab3([%
            @if is_lightlike1%]k[%index1%][% @else %]l[%index1%][%
            @end @if %], Q?, [%
            @if is_lightlike2%]k[%index2%][% @else %]l[%index2%][%
            @end @if %]) = spva[%
              @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
         %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %].Q;[%
   @end @for %]
#EndProcedure
