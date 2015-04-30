Dim=4-2*eps;
prefactor=Gamma[1+eps]^2;

momlist=ToExpression[Table[StringJoin["p", ToString[i]], {i, 1, [% loop %]}]];
gosam_incoming = {[% @for particles initial %]k[%index%][% @if eval index .lt. num_in %], [% @end @if %][%@end @for %]};
gosam_outgoing = {[% @for particles final %]k[%index%][% @if eval index .lt. num_out %], [% @end @if %][%@end @for %]};

ExternalMomenta=Join[gosam_incoming,gosam_outgoing];
KinematicInvariants={[% @for mandelstam non-zero non-mass %][% @if eval .not. is_first %],[% @end @if %][% symbol %][% @end @for %]};
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

(* proplist *)
(* numerator *)
(* powerlist *)