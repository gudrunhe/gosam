[% ' vim: syntax=golem
	%]
	abb... : complex;

	TR : real;
	pi : real;
	sqrt2, Sqrt2 : real = "sqrt2";
	sqrt3, Sqrt3 : real = "sqrt3";
	i_ : complex;

	log, sqrt, sin, asin, cos, acos, tan, atan, exp : real -> real;
	pow : real, real -> real = "(%2$s)**(%3$s)";
	atan2 : real, real -> real = "atan2(%3$s, %2$s)";
	fabs : real -> real = "abs(%2$s)";
	sort4 : real, real, real, real, integer -> real;
	if : real, real, real -> real = "ifpos(%2$s, %3$s, %4$s)";
	#fhf2 : real, real, real, real, real, real,
	#	real, real, real, real, real, real, real -> real;

	[% @if internal CUSTOM_SPIN2_PROP
        %]customSpin2Prop : real, complex -> complex;[% @end @if %]


	complexconjugate : complex -> complex = "conjg(%2$s)";
	csqrt : complex -> complex = "sqrt(%2$s)";
