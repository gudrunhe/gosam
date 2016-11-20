[% @for parameters %]
[% @select type
@case R %]const real_parameter_t [% $_ %]=parameters.[% $_ %];[%
@case C %]const complex_parameter_t [% $_ %]=parameters.[% $_ %];[%
@case RP %]const real_parameter_t [% $_ %]=parameters.[% $_ %];[%
@case CP %]const complex_parameter_t [% $_ %]=parameters.[% $_ %];
[% @end @select type %][% @end @for parameters %]

[% @for functions_resolved language=cpp %]
[% @select type
@case R %]const real_parameter_t [% $_ %]=parameters.[% $_ %];[%
@case C %]const complex_parameter_t [% $_ %]=parameters.[% $_ %];
[% @end @select type %][% @end @for functions_resolved %]
