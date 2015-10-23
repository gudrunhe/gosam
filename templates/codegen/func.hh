#IfDef `optim'
[%
@for functions_resolved_sum index=index1%]
L x[% index1 %] = [% expression %];
#$name[%index1%] = [% $_ %];[%
   @if is_last %]
#$num = [%index1%];
[% @end @if %][%
@end @for %]
#Else[%
@for functions_resolved %][%
@if is_first %]
S [% @end @if%][% $_ %][% 
@if is_last %];[%@else%],[% @end @if %][%
@end @for %][%
@for parameters %][%
@if is_first %]
S [% @end @if%][% $_ %][% 
@if is_last %];[%@else%],[% @end @if %][%
@end @for %][%
@for ct_functions_resolved_name %][%
@if is_first %]
Vector [% @end @if%][% $_ %][% 
@if is_last %];[%@else%],[% @end @if %][%
@end @for %][%
@for functions_resolved_sum index=index1%]
L x[% index1 %] = [% expression %];
#$name[%index1%] = [% $_ %];[%
   @if is_last %]
#$num = [%index1%];
[% @end @if %][%
@end @for %]
#EndIf
#Procedure Simplify()
[%
@for functions_resolved_reversed index=index1%]
Id [% $_ %] = [% expression %];[% 
@end @for %]
#EndProcedure



