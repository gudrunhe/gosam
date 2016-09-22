Dim=%(dim)s-2*eps;
prefactor=1;

momlist=ToExpression["p" <> ToString[#]] & /@ Range[[% loop %]];
GosamIncoming = {[% @for particles initial %]k[%index%][% @if eval index .lt. num_in %], [% @end @if %][%@end @for %]};
GosamOutgoing = {[% @for particles final %]k[%index%][% @if eval index .lt. num_out %], [% @end @if %][%@end @for %]};

ExternalMomenta=Join[GosamIncoming,GosamOutgoing];
KinematicInvariants={[% @for mandelstam sym_prefix=es non-zero non-mass %][% @if eval .not. is_first %],[% @end @if %][% symbol %][% @end @for %]};
Masses={[% @for all_masses %][% @if eval .not. is_first %],[% @end @if %][% mass %][% @end @for %]};
ScalarProductRules = {[%@for mandelstam_subs diagonal upper %]
  SP[k[% index1 %],k[% index2 %]]->0[%
@for mandelstam_subs_rhs %][%
      @select coeff
      @case -1 %] - 1/2 * [%
      @case 1 %] + 1/2 * [%
      @case -2 %] - [%
      @case 2 %] + [%
      @else %][%
         @if eval coeff .gt. 0 %][%
            @if is_first %] [%
            @else %] +[%
            @end @if %] [%coeff%] * [%
         @else %] - [%eval .abs. coeff%]/2 * [%
         @end @if %][%
      @end @select %][%$_%][%
      @if eval exponent .gt. 1 %]^[%exponent%][%
      @end @if %][%
   @end @for %][% @if eval .not. is_last %],[% @end @if %][%
@end @for %]
};
numerator={1};

(* these lines are replaced by tosecdec.py *)
proplist={%(proplist)s};
powerlist={%(powerlist)s};
