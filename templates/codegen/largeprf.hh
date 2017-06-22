*
* A collection of convenience procedures for emulating prf
* without the limitation that the entire expression must fit into a single term
*

#procedure add(n1,d1,n2,d2 , gcd,lcm)

*
* Computes n1/d1 + n2/d2 = (n1*d2 + n2*d1) / (d1 * d2)
* Stores resulting numerator/denominator in n1/d1
*

* Step 1: Compute lcm(d1,d2)
	skip; nskip `gcd',`lcm';
	Local `lcm' = `d1'*`d2';
	Local `gcd' = gcd_(`d1',`d2');
	.sort
	skip; nskip `lcm';
	Local `lcm' = div_(`lcm',`gcd');
	.sort

* Step 2: Divide d1,d2 by gcd(d1,d2)
	drop `gcd';
	skip; nskip `d1',`d2';
	Local `d1' = div_(`d1', `gcd');
	Local `d2' = div_(`d2', `gcd');
	.sort

* Step 3: Build result as (n1*d2/gcd(d1,d2) + n2*d1/gcd(d1,d2))/lcm(d1,d2)
	drop `lcm';
	skip; nskip `n1',`d1';
	Local `n1' = `n1' * `d2' + `n2' * `d1';
	Local `d1' = `lcm';
	.sort

* Step 4: Divide numerator and denominator by their gcd
	skip; nskip `gcd';
	#If ( termsin(`n1') == 0)
		Local `gcd' = `d1';
	#Else
		Local `gcd' = gcd_(`d1',`n1');
	#EndIf
	.sort
	skip; nskip `n1',`d1';
	drop `gcd';
	Local `n1' = div_(`n1',`gcd');
	Local `d1' = div_(`d1',`gcd');

#endprocedure

#procedure multiply(n1,d1,n2,d2,nr,dr , gcd1,gcd2,ntmp,dtmp)
*
* Computes n1/d1 * n2/d2 stores result in nr,dr
* Stores resulting numerator/denominator in n1/d1
* Assumes gcd(n1,d1) = 1, gcd(n2,d2) = 1
*

* Step 1: Divide n1,d2 by their gcd, same for n2,d1
	skip; nskip `gcd1',`gcd2';
	L `gcd1' = gcd_(`n1',`d2');
	L `gcd2' = gcd_(`n2',`d1');
	.sort
	Drop `gcd1',`gcd2';
	skip; nskip `nr',`dr',`ntmp',`dtmp';
	L `nr' = div_(`n1',`gcd1');
	L `dr' = div_(`d2',`gcd1');
	L `ntmp' = div_(`n2',`gcd2');
	L `dtmp' = div_(`d1',`gcd2');
	.sort

* Step 2: Multiply
	Drop `ntmp', `dtmp';
	skip; nskip `nr',`dr';
	L `nr' = `nr'*`ntmp';
	L `dr' = `dtmp'*`dr';
	.sort

#endprocedure

#procedure producelist(expr,list,INT)

*
* Produces a list of `INT' appearing in `expr'
*
* Example:
*
*	expr = INT(i1)*COEFF1 + INT(i2)*COEFF2;
*
*	gives
*
*	list = INT(i1) + INT(i2);
*

	skip; nskip `list';
	L `list' = `expr';
	B `INT';
	.sort

	skip; nskip `list';
	collect fDUMMY1,fDUMMY1;
	Id fDUMMY1(?args) = 1;
	.sort

	skip; nskip `list';
	dropcoefficient;
	.sort

#endprocedure

#procedure simplifyproduct(expr,list,DINT , current,tmp1,tmp2,tmp3,tmp4)
*
* Takes expressions of the form
* expr = INT(...)*DINT(1,COEFF1) + ...
* where DINT(1,COEFF1) should be interpreted as
* DINT(1)*COEFF1
*
* Computes all products in the expression and
* saves results to [N`DINT'(x)], [D`DINT'(x)] where
* x is an index greater than any index
* currently appearing in `expr'
*

	#call producelist(`expr',`list',`DINT')

* Step 1: Get largest index used for `DINT'
	skip; nskip `list';
	Id `DINT'(sDUMMY1?,?a) = TermLabel^sDUMMY1*`DINT'(sDUMMY1,?a);
	.sort
	skip; nskip `list';
	#$index = 0;
	if ( count(TermLabel,1) > $index ) $index = count_(TermLabel,1);
	ModuleOption,maximum,$index;
	.sort

* Step 2: Drop term labels and terms from list that are not products
	skip; nskip `list';
	Id TermLabel = 1;
	Id `DINT'(sDUMMY1?) = 0;
	.sort

* Step 3: Iterate through list of products
	#Do term = `list'

* Step 3a) Increment index
		#$index = $index+1;

* Step 3b) Write current product to its own expression
		skip; nskip `current';
		L `current' = `term';
		Id `DINT'(sDUMMY1?$fac1,sDUMMY2?$fac2) = 0;
		.sort

* Step 3c) Perform multiplication
		Drop `current';
		#call multiply([N`DINT'(`$fac1')],[D`DINT'(`$fac1')],N`$fac2',D`$fac2',[N`DINT'(`$index')],[D`DINT'(`$index')],`tmp1',`tmp2',`tmp3',`tmp4')

* Step 3d) Insert new `DINT' into original expression
		Id `DINT'(`$fac1',`$fac2') = `DINT'(`$index');
		.sort

	#EndDo

#endprocedure

#procedure topolyratfun(coeff,N,D,den,separate , tmp1,tmp2)

*
* Processes coefficients of the form a/b + c/d
* splits them into a single numerator and a single denominator
*
* Example:
*
*	[D1INT(1)] = - den(z + x)*c*y*z + den(c + a)*a*b;
*
*	becomes
*
*	[ND1INT(1)] = - c^2*y*z - a*c*y*z + a*b*z + a*b*x;
*	[DD1INT(1)] = c*z + c*x + a*z + a*x;
*

	skip; nskip [`N'`coeff'], [`D'`coeff'];
	L [`N'`coeff'] = 0;
	L [`D'`coeff'] = 1;
	.sort

	#Do term = [`coeff']

		#If (`separate' != 0)
* Step 1: Put numerator of current term in `N'
			skip; nskip `N';
			L `N' = `term';
			Id `den'(?args) = 1;
			.sort

* Step 2: Put denominator of current term in `D'
			skip; nskip `D';
			L `D' = `term';
			dropsymbols;
			dropcoefficient;
			Id `den'(sDUMMY1?) = sDUMMY1;
			.sort

* Step 3: Add current numerator and denominator to previous result
			#call add([`N'`coeff'],[`D'`coeff'],`N',`D' , `tmp1',`tmp2')
			.sort

		#Else

* Step 3 (alt): Add current numerator and denominator to previous result
			#call add([`N'`coeff'],[`D'`coeff'],[N`term'],[D`term'] , `tmp1',`tmp2')
			.sort
			Drop [N`term'],[D`term'];

		#EndIf

	#EndDo

* Step 4: If numerator is zero drop term from all expressions
	drop [`coeff'],`N',`D';
	#If ( termsin([`N'`coeff']) == 0 )
		drop [`N'`coeff'], [`D'`coeff'];
		Id `coeff' = 0;
	#EndIf
	.sort

#endprocedure

#procedure split(expr,list,INT,PREFIX,collf)

*
* Splits large expressions
*
* Example:
*
*	expr = INT(i1)*COEFF1 + INT(i2)*COEFF2;
*
*	where COEFF can be of the form: a/b + c/d
*	is converted into the separate expressions
*
*	expr = INT(i1)*INTPREFIX(1) + INT(i2)*INTPREFIX(2);
*	[INTPREFIX(1)] = COEFF1;
*	[INTPREFIX(2)] = COEFF2;
*	list = INTPREFIX(1) + INTPREFIX(2);
*

* Step 1: Convert INT(i1) to INT(1)
	skip; nskip `expr';
	Id `INT'(?args) = `INT'(`INT'(?args));
	argtoextrasymbol tonumber `INT';
	.sort

* Step 2: Produce list = INTPREFIX(1) + INTPREFIX(2) + ...
	#call producelist(`expr',`list',`INT')

	skip; nskip `list',`expr';
	Id `INT'(sDUMMY1?) = `INT'`PREFIX'(sDUMMY1);
	.sort

* Step 3: Write [INTPREFIX(...)] for each INT(...) and build output expr
	skip `list';
	B `INT'`PREFIX';
	.sort

	skip list;
	#Do x = list
		L [`x'] = `expr'[`x'];
	#EndDo
	L `expr' = `list';

	Id `INT'`PREFIX'(sDUMMY1?) = `INT'`PREFIX'(sDUMMY1) * extrasymbol_(sDUMMY1);
	.sort

#endprocedure

#procedure series(N0,D0,numpow,denpow,eps,ORDER,PREFIX)

*
* Given N0/D0 computes the series expansion in eps
*

* Copy expressions so that names match what is internally expected
	L `PREFIX'N0 = `N0';
	L `PREFIX'D0 = `D0';
	.sort:copy;

*
* Step 1: Make leading term in numerator and denominator `eps'^0
*

* Count minimum power of `eps' in numerator and denominator

	Skip; NSkip `PREFIX'N0;
	#$minnum = maxpowerof_(`eps');
	if ( count(`eps',1) < $minnum ) $minnum = count_(`eps',1);
	ModuleOption,minimum,$minnum;
	.sort

	Skip; Nskip `PREFIX'D0;
	#$minden = maxpowerof_(`eps');
	if ( count(`eps',1) < $minden ) $minden = count_(`eps',1);
	ModuleOption,minimum,$minden;
	.sort

	Skip; NSkip `PREFIX'N0;
	Multiply `eps'^(-`$minnum');
	.sort

	Skip; NSkip `PREFIX'D0;
	Multiply `eps'^(-`$minden');
	.sort

*
* Step 2: Compute denominator
*
	Skip; NSkip numpow, denpow, `PREFIX'DF0d0;
	L numpow = `$minnum'; * Store power of `eps' in numerator (for returning)
	L denpow = `$minden'; * Store power of `eps' in denominator (for returning)
	.sort

	Hide;
	.sort:hide;

*
* Step 3: Compute denominator without repeated factors (`PREFIX'DF0)
*
	#$d0=`D0';
	#FactDollar $d0;
	#$previousterm=0;
	#$numfactors=0;
	.sort:fact;

	#Do i = 1, `$d0[0]'

		Skip;
		L `PREFIX'diff = (`$d0[`i']') - ($previousterm);
		.sort:DF0;
		
		#$previousterm=`$d0[`i']';
		#If termsin(`PREFIX'diff) != 0
* factor is new
			#$numfactors = $numfactors + 1;
			#$power`$numfactors' = 1;
			Skip;
			#If `i' == 1
				LF `PREFIX'DF0 = (`$d0[`i']');
			#Else
				LF `PREFIX'DF0 = `PREFIX'DF0*(`$d0[`i']');
			#EndIf
			.sort:DF0;
		#Else
			#$power`$numfactors' = $power`$numfactors' + 1;
		#EndIf

	#EndDo

	Drop `PREFIX'diff;
	Skip;
	L `PREFIX'DF0d = 0;
	.sort:drop;

	#Do i = 1, `$numfactors'

		Skip;
		L `PREFIX'cd = (`PREFIX'DF0[factor_^(`i')])*replace_(epsS,0);
		.sort:prod;

		Skip; NSkip `PREFIX'cd;
		L `PREFIX'cd = (`PREFIX'DF0[factor_^(`i')]) - (`PREFIX'cd);
		Id `eps'^sDUMMY1?pos_ = sDUMMY1*`eps'^(sDUMMY1-1);
		.sort:prod;

		Skip;
		L `PREFIX'prod = sDUMMY`i' * `PREFIX'cd;
		.sort:prod;

		Skip;
		#Do j = 1, `$numfactors'
			#If `i' != `j'
				L `PREFIX'prod = `PREFIX'prod * ( `PREFIX'DF0[factor_^(`j')]);
				.sort:prod;
			#EndIf
		#EndDo

		Skip;
		L `PREFIX'DF0d = `PREFIX'DF0d + `PREFIX'prod;
		.sort:prod;

	#EndDo
	
	Skip; 
	Drop `PREFIX'prod, `PREFIX'cd;
	LF `PREFIX'D0F = `PREFIX'DF0;
	.sort:drop;

	Skip; NSkip `PREFIX'DF0;
	Unfactorize `PREFIX'DF0;
	.sort:unfact;

*
* Step 4: Compute numerators
*

	#Do i = 1, {`ORDER'+`$minden'-`$minnum'+1}

*
* Step 4a): Generate derivative at 0
*
		Skip; NSkip `PREFIX'N{`i'-1}d0;
		L `PREFIX'N{`i'-1}d0 = `PREFIX'N{`i'-1}*replace_(`eps',0);
		.sort:zero;

* We have computed everything we need, can exit loop
		#If `i' == {`ORDER'+`$minden'-`$minnum'+1}
 			Drop `PREFIX'N{`i'-1};
			#BreakDo
		#EndIf

*
* Step 4b): Differentiate numerator (N`i')
*
		Hide;
		Skip; NSkip `PREFIX'N`i';
		L `PREFIX'N`i' = `PREFIX'N{`i'-1} - `PREFIX'N{`i'-1}d0;
		Id `eps'^sDUMMY1?pos_ = sDUMMY1*`eps'^(sDUMMY1-1);
		.sort:diff;

*
* Step 4c) Quotient Rule: Generate derivative of numerator
*
		Skip; NSkip `PREFIX'cd;
		L `PREFIX'cd = `PREFIX'DF0d;
		#Do j = 1, `$numfactors'
			Id sDUMMY`j' = `$power`j'' + `i' -1;
		#EndDo
		.sort;

		Drop `PREFIX'N{`i'-1}, `PREFIX'cd;
		Skip; NSkip `PREFIX'N`i';
		L `PREFIX'N`i'= `PREFIX'DF0*`PREFIX'N`i'/`i' - `PREFIX'N{`i'-1}*`PREFIX'cd/`i';
		.sort:quot;

	#EndDo

	Drop `PREFIX'DF0, `PREFIX'DF0d;
	.sort:drop;

*
* Step 5) Take `eps' = 0 in denominator
*
	Unhide;
	.sort:unhide;

	Skip; NSkip `PREFIX'D0F, `PREFIX'D0;
	Id epsS = 0;
	.sort:den;

#endprocedure
