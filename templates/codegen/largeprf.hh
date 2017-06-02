*
* A collection of convenience procedures for emulating prf
* without the limitation that the entire expression must fit into a single term
*

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
