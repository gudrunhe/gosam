*     Copyright 2010-2013 Andreas Maier <a.maier@tum.de>
* 
*     This program is free software: you can redistribute it and/or modify
*     it under the terms of the GNU General Public License as published by
*     the Free Software Foundation, either version 3 of the License, or
*     (at your option) any later version.
* 
*     This program is distributed in the hope that it will be useful,
*     but WITHOUT ANY WARRANTY; without even the implied warranty of
*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*     GNU General Public License for more details.
* 
*     You should have received a copy of the GNU General Public License
*     along with this program.  If not, see <http://www.gnu.org/licenses/>.

*Header file for the series package - contains all procedures

#ifndef `SERIESPACKAGE'
#define SERIESPACKAGE

*global definitions
#ifndef `NAMESPACE'
#define NAMESPACE ""
#endif
#procedure `NAMESPACE'series(VAR,CUT)
*defines the active expressions to be series in `VAR' up to power `CUT'
* the only thing this procedure does is define variables
* for the "real" functions that do all the work

   #$seriesvar=`VAR';
   #$seriescut=`CUT';

#endprocedure
#procedure `NAMESPACE'invert(SOURCE,TARGET)
*inverts `SOURCE' (interpreting it as a series in `$seriesvar', up to `$seriesvar'^`$seriescut')
* the result is saved in `TARGET'

   #call `NAMESPACE'toseries(`SOURCE',ta)
   #define CUT "{`$seriescut'+{`$seriesminpowerta'}}"
*  coefficients of inverted series
   #call `NAMESPACE'createtable(tb,`CUT')
   fill [series::tb](0)=1/[series::ta](0);
   skip;
*  now higher order terms
   #do power=1,`CUT'
      L [series::tmp]= -[series::tb](0)*(
      #do j=1,`power'
	 +([series::ta](`j'))*([series::tb]({`power'-`j'}))
      #enddo
      );
      if(count([series::ta],1)>0)discard;
      .sort
      #$seriestmp=[series::tmp];
      fill [series::tb](`power') = `$seriestmp';
      skip;
   #enddo
   .sort
   drop [series::tmp];
   skip;
   L `TARGET'= (`$seriesvar')^-(`$seriesminpowerta')*(
   #do i=0,`CUT'
      +[series::tb](`i')*`$seriesvar'^(`i')
   #enddo
   );
   .sort
   cleartable [series::ta];
   cleartable [series::tb];

#endprocedure

#procedure `NAMESPACE'exp(SOURCE,TARGET)
*computes e^SOURCE,
*  treating SOURCE as a series as specified by the procedure series
* the result is saved in TARGET

   #call `NAMESPACE'toseries(`SOURCE',ta)
   #define CUT "{`$seriescut'}"
   #call `NAMESPACE'createtable(tb,`CUT')
*  coefficients of result series
   fill [series::tb](0)=1;
   skip;
*  now higher order terms
   #do power=1,`CUT'
      L [series::tmp]= (
      #do j=1,`power'
	 +(`j')/(`power')*([series::ta]({`j'-{`$seriesminpowerta'}}))*([series::tb]({`power'-`j'}))
      #enddo
      );
      if(count([series::ta],1)>0)discard;
      .sort
      #$seriestmp=[series::tmp];
      fill [series::tb](`power') = `$seriestmp';
      skip;
   #enddo
   .sort
   drop [series::tmp];
   skip;
   L `TARGET'=
   #do i=0,`CUT'
      +[series::tb](`i')*`$seriesvar'^(`i')
   #enddo
   ;
   .sort
   cleartable [series::tb];

*  if the series starts from a power that is smaller than one,
*  these parts cannot be expanded and we keep them
   #if `$seriesminpowerta'<1
      #if `$seriesminpowerta'<0
	 #message WARNING: expression in exponent is not analytic
	 #message some parts will not be expanded
      #endif
      S [series::x];
      CF exp;
      skip;
      nskip `TARGET';
      multiply exp( sum_(
         [series::x],0,-(`$seriesminpowerta'),
         [series::ta]([series::x])*`$seriesvar'^([series::x]+(`$seriesminpowerta'))
      ) );
      argument exp;
	 if(count([series::ta],1)>0)discard;
      endargument;
      .sort
   #endif
   cleartable [series::ta];

#endprocedure
#procedure `NAMESPACE'log(SOURCE,TARGET)
*computes the logarithm of SOURCE,
* treating SOURCE as a series as specified by the procedure series
* the result is saved in TARGET

   #call `NAMESPACE'toseries(`SOURCE',ta)
   #define CUT "`$seriescut'"
   #call `NAMESPACE'createtable(tb,`CUT')
   CF log;
   skip;
*  coefficients of inverted series
   #do power=1,`CUT'
      L [series::tmp]=([series::ta](`power'))/([series::ta](0))
      #do j=1,{`power'-1}
	 -(`j')/(`power')*([series::ta]({`power'-`j'}))/([series::ta](0))*([series::tb](`j'))
      #enddo
      ;
      if(count([series::ta],1)>0)discard;
      .sort
      #$seriestmp=[series::tmp];
      fill [series::tb](`power') = `$seriestmp';
      skip;
   #enddo
   .sort
   drop [series::tmp];
   skip;
   L `TARGET'= log([series::ta](0)*(`$seriesvar')^(`$seriesminpowerta'))
   #do i=1,`CUT'
      +[series::tb](`i')*`$seriesvar'^(`i')
   #enddo
   ;
*  throw away trivial logs -- this is a bit a waste of resources,
*  we already know that at most one term will be affected
   id once log(1)=0;

   .sort
   cleartable [series::ta];
   cleartable [series::tb];

#endprocedure
#procedure `NAMESPACE'power(BASE,EXP,TARGET)
*computes BASE^EXP, treating both as series (as specified by the procedure series)
* the result is saved in `TARGET'

*uses TARGET=exp(EXP*log(BASE))

   #call `NAMESPACE'log(`BASE',[series::tmp_pow])
   skip;
*  #call `NAMESPACE'multiply(`EXP',[series::tmp_pow],[series::tmp_pow_2])
*  skip;
   drop [series::tmp_pow];
   L [series::tmp_pow_2]=`EXP'*[series::tmp_pow];
   #call `NAMESPACE'exp([series::tmp_pow_2],`TARGET')
   skip;
   drop [series::tmp_pow_2];
   .sort

#endprocedure


#procedure `NAMESPACE'Gamma(SOURCE,TARGET)
*computes the Gamma function with argument SOURCE,
* treating SOURCE as a series as specified by the procedure series
* the result is saved in TARGET

   #call `NAMESPACE'toseries(`SOURCE',ta)
   #define CUT "`$seriescut'"
   #call `NAMESPACE'createtable(tb,`CUT')
   fill [series::tb](0) = 1;
   CF Gamma;
   hide `SOURCE';
*  coefficients of inverted series
   #do power=1,`CUT'
      #$seriesPARTSIZE = 0;
*     sum over partitions of `power''
      #do i = 0,0,0
	 #call `NAMESPACE'nextPartition(`power',PART)
	 #call `NAMESPACE'computeMultiplicities(PART,MULTIPLICITY)
	 #if `$seriesPARTSIZE' == 0
*	    after last partition
	    #breakdo
	    #elseif `$seriesPARTSIZE' == 1
*           trivial partition
	    skip;
	    l [series::tmp] = + psi(0,[series::ta](0))*[series::ta](`power');
	    .sort
	    
	    #else
	    skip;
	    l [series::tmp] = [series::tmp] + psi({`$seriesPARTSIZE'-1},[series::ta](0))
	    #do j=1,`$seriesPARTSIZE',1
	       #redefine l "`$seriesPART`j''"
	       * [series::ta](`l')^`$seriesMULTIPLICITY`l''/{`$seriesMULTIPLICITY`l''!}
	       #redefine j "{`j'+`$seriesMULTIPLICITY`l''-1}"
	    #enddo
	    + {{`$seriesPARTSIZE'-1}!}
	    #do j=1,`$seriesPARTSIZE',1
	       #redefine l "`$seriesPART`j''"
	       * (-[series::tb](`l'))^`$seriesMULTIPLICITY`l''/{`$seriesMULTIPLICITY`l''!}
	       #redefine j "{`j'+`$seriesMULTIPLICITY`l''-1}"
	    #enddo
	    ;
	    if(count([series::ta],1)>0)discard;
	    .sort
	 #endif
      #enddo
      #$seriestmp=[series::tmp];
      fill [series::tb](`power') = `$seriestmp';
      skip;
   #enddo
   .sort
   drop [series::tmp];
   skip;
   L `TARGET'= Gamma([series::ta](0))*(1
   #do i=1,`CUT'
      +[series::tb](`i')*`$seriesvar'^(`i')
   #enddo
   );
   .sort
   cleartable [series::ta];
   cleartable [series::tb];
   unhide `SOURCE';

#endprocedure
#procedure `NAMESPACE'wrap(SOURCE,FUN,TARGET)
*computes FUN(SOURCE), treating SOURCE as a series
* as specified by the procedure series
* the result is saved in TARGET

   #call `NAMESPACE'toseries(`SOURCE',ta)
   #if `$seriesminpowerta'<0
      #message Argument `SOURCE' of `FUN' contains negative powers of  `$seriesvar'
      #terminate
      #elseif `$seriesminpowerta'==0
      #define FUNARG "[series::ta](0)"
      #else
      #define FUNARG "0"
   #endif
   #call `NAMESPACE'createtable(tb,`$seriescut')

*  coefficients of result series
   S [series::d],[series::x];
   CF D;
   fill [series::tb](0)=`FUN'(`FUNARG');
   skip;
*  now higher order terms
   #do power=1,`$seriescut'
      L [series::tmp]=
      #do j=1,`power'
	 + [series::d]*(`j')/(`power')
	   *([series::ta]({`j'-`$seriesminpowerta'}))
	   *([series::tb]({`power'-`j'}))
      #enddo
      ;
      if(count([series::ta],1)>0)discard;
      .sort
      #$seriestmp=[series::tmp];
      fill [series::tb](`power') = `$seriestmp';
      skip;
   #enddo
   .sort
   drop [series::tmp];
   skip;
   L `TARGET'=
   #do i=0,`$seriescut'
      +[series::tb](`i')*`$seriesvar'^(`i')
   #enddo
   ;
   id [series::d]^[series::x]?{>0}*`FUN'(?a) = D(`FUN'(?a),[series::x]);
   .sort
   cleartable [series::tb];

#endprocedure
#procedure `NAMESPACE'createtable(tab,SIZE)
*creates a new table [series::`tab'] with size *at least* `SIZE'

   #ifndef `$seriessize`tab''
*  table is unused, create it
      table,sparse [series::`tab'](1);
      #else
      cleartable [series::`tab'];
   #endif
   #$seriessize`tab'=`SIZE';

#endprocedure
#procedure `NAMESPACE'toseries(source,tab)
*transforms `source' into a series (read the coefficients into the table `tab')

   #ifndef `$seriesvar'
      #message no series found
      #message (please call series(var,cut) first)
      #terminate
   #endif

   .sort
   skip;
   nskip `source';
*  find lowest & highest power of $seriesvariable
   #$seriesminpower`tab'=maxpowerof_(`$seriesvar');
*  #$seriesmaxpower`tab'=minpowerof_(`$seriesvar');
   #$seriesmaxpower`tab'=-maxpowerof_(`$seriesvar');
   if(count(`$seriesvar',1)<$seriesminpower`tab') $seriesminpower`tab'=count_(`$seriesvar',1);
   if(count(`$seriesvar',1)>$seriesmaxpower`tab') $seriesmaxpower`tab'=count_(`$seriesvar',1);
   moduleoption minimum $seriesminpower`tab';
   moduleoption maximum $seriesmaxpower`tab';
   .sort
   #define SIZE "{`$seriesmaxpower`tab''-{`$seriesminpower`tab''}}"
   S [series::x];
   skip;
   nskip `source';
*  make the expansion start from `$seriesvar'^0
*  replace the expansion variable by some auxiliary variable
*  in order to circumvent global cuts
*  (i.e. from 'Symbol `$seriesvar'(:`cut'))
   multiply [series::x]^-(`$seriesminpower`tab'');
*replace_(`$seriesvar',[series::x]);
   id `$seriesvar'=[series::x];
   id `$seriesvar'^-1=[series::x]^-1;
   b+ [series::x];
   .sort
*  fill coefficients into table
   #call `NAMESPACE'createtable(`tab',`SIZE')

   fillexpression [series::`tab']=`source'([series::x]);
   skip;
   nskip `source';
   multiply [series::x]^(`$seriesminpower`tab'');
   multiply replace_([series::x],`$seriesvar');
   .sort

#endprocedure
#procedure `NAMESPACE'init(CUT)

   #ifndef `$serieslabelnum'
      #$seriesmaxtermnum=`CUT';
      #$serieslabelnum=0;
      S [series::x],[series::y],[series::i];
      cf [series::log],[series::den],[series::Gamma],[series::LOG],[series::EXP];
      cf exp,log,D,psi,[series::f];

      table [series::b](0:`CUT');
      #do n=0,`CUT'
	 #$seriesa`n'=0;
	 #$seriesb`n'=0;
	 fill [series::b](`n')=$seriesb`n';
      #enddo

*     just for convenience and to suppress warnings
      #$seriesminterm=0;
      #$seriesinvminterm=0;
      #$seriesminpow=0;
      #$seriesc=0;
      #$serieslim=0;
      #$seriesx=0;
      #$seriest=0;
      #$seriessum=0;
      #$seriesorigcut=0;
      #$seriesvarstore=0;
      #$seriescutstore=0;

      #else
      #ifndef `$seriesIWarnedYou'
	 #message WARNING: init called more than once
	 #message init was first called with argument `$seriesmaxtermnum'
	 #message all further calls will be ignored
	 #$seriesIWarnedYou = 1;
      #endif
   #endif

#endprocedure
#procedure `NAMESPACE'expand(FUN,?a)
*wrapper which calls the corresponding expansion procedure

   #if "`FUN'"=="exp"
      #call `NAMESPACE'expandExp(`FUN',`?a')
      #elseif ( ("`FUN'"=="log") || ("`FUN'"=="ln") )
      #call `NAMESPACE'expandLog(`FUN',`?a')
      #elseif ( ("`FUN'"=="pow") || ("`FUN'"=="power") )
      #call `NAMESPACE'expandPower(`FUN',`?a')
      #elseif ( ("`FUN'"=="den") || ("`FUN'"=="deno") )
      #call `NAMESPACE'expandDenominator(`FUN',`?a')
      #elseif "`FUN'"=="Gamma"
      #call `NAMESPACE'expandGamma(`FUN',`?a')
      #else
      #call `NAMESPACE'expandFunction(`FUN',`?a')
   #endif

#endprocedure
#procedure `NAMESPACE'expandDenominator(DENO,?SERIESSPEC)
*replaces the argument of `DENO' by its inverse
*(the argument is considered as a series in $seriesvar up to power $seriescut)

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

*  increase label number to make sure it's unique
   #$serieslabelnum=`$serieslabelnum'+1;

   while(match(`DENO'([series::x]?)));
      $seriesminpow=maxpowerof_([series::x]);
      $seriesminterm=0;

      once `DENO'([series::x]?$seriesx)=1;

*     determine leading term
      inside $seriesx;
	 $seriesc = count_($seriesvar,1);
	 if($seriesc<$seriesminpow);
	    $seriesminpow=count_($seriesvar,1);
	    $seriesminterm=term_();
	    elseif($seriesc==$seriesminpow);
	    $seriesminterm=$seriesminterm+term_();
	 endif;
      endinside;

      $seriesminterm = ($seriesminterm)*($seriesvar)^(-($seriesminpow));

      $seriest = termsin_($seriesminterm);
      if($seriest==1);
	 $seriesinvminterm = 1/$seriesminterm;
	 else;
	 $seriesinvminterm = [series::den]($seriesminterm);
      endif;

*     normalise denominator
      $seriesx =  1 + ($seriesinvminterm)*(($seriesx)*($seriesvar)^(-($seriesminpow)) - $seriesminterm);

      multiply $seriesinvminterm*$seriesvar^-$seriesminpow;

      #call `NAMESPACE'getCoefficients(x,$seriesvar,`$seriesmaxtermnum',a)

*     multiply by expanded inverse of normalised denominator
      $serieslim = $seriescut - count_($seriesvar,1);
      $seriesb0=1;
      #do n=1,`$seriesmaxtermnum'
	 if(`n'>$serieslim) goto afterloop`$serieslabelnum';
	 $seriesb`n' =
	 #do i=0,{`n'-1}
	    - $seriesa{`n'-`i'}*$seriesb`i'
	 #enddo
	 ;
      #enddo
      label afterloop`$serieslabelnum';

      $seriessum=sum_([series::i],0,$serieslim,[series::b]([series::i]));
      multiply $seriessum;

   endwhile;

*  restore original notion of denominators
   multiply replace_([series::den],`DENO');

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure
#procedure `NAMESPACE'expandLog(LOG,?SERIESSPEC)
*replaces the argument of `LOG' by its inverse
*(the argument is considered as a series in $seriesvar up to power $seriescut)

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

*  increase label number to make sure it's unique
   #$serieslabelnum=`$serieslabelnum'+1;

   while(match(`LOG'([series::x]?)));
      $seriesminpow=maxpowerof_([series::x]);
      $seriesminterm=0;

      once `LOG'([series::x]?$seriesx)=1;

*     determine leading term
      inside $seriesx;
	 $seriesc = count_($seriesvar,1);
	 if($seriesc<$seriesminpow);
	    $seriesminpow=count_($seriesvar,1);
	    $seriesminterm=term_();
	    elseif($seriesc==$seriesminpow);
	    $seriesminterm=$seriesminterm+term_();
	 endif;
      endinside;

      $seriesminterm = $seriesminterm*$seriesvar^-$seriesminpow;

*     normalise log argument
      $seriesx =  1 + (($seriesx)*($seriesvar)^(-($seriesminpow)) - $seriesminterm)/($seriesminterm);

      #call `NAMESPACE'getCoefficients(x,$seriesvar,`$seriesmaxtermnum',a)

*     multiply by expanded logarithm
      $serieslim = $seriescut - count_($seriesvar,1);

      #do n=1,`$seriesmaxtermnum'
	 if(`n'>$serieslim) goto afterloop`$serieslabelnum';
	 $seriesb`n' = $seriesa`n'
	 #do i=1,{`n'-1}
	    - `i'/`n'*$seriesa{`n'-`i'}*$seriesb`i'
	 #enddo
	 ;
      #enddo
      label afterloop`$serieslabelnum';

      $seriessum=sum_([series::i],1,$serieslim,[series::b]([series::i]));
      $seriessum = $seriessum + [series::log](($seriesminterm) * ($seriesvar)^($seriesminpow));
      multiply $seriessum;
   endwhile;

*  restore original notion of logs
   multiply replace_([series::log],`LOG');

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure
#procedure `NAMESPACE'expandExp(EXP,?SERIESSPEC)
*replaces the argument arg of `EXP' by exp(arg)
*(the argument is considered as a series in $seriesvar up to power $seriescut)

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

*  increment label number to make sure it's unique
   #$serieslabelnum=`$serieslabelnum'+1;

   repeat id `EXP'([series::x]?)*`EXP'([series::y]?) = `EXP'([series::x]+[series::y]);
   if(match(`EXP'([series::x]?$seriesx)));

*     extract negative powers (not expandable)
      $seriesminterm = 0;
      inside $seriesx;
	 $seriesc = count_($seriesvar,1);
	 if($seriesc<0);
	    $seriesminterm = $seriesminterm+term_();
	 endif;
      endinside;
      $seriest = termsin_($seriesminterm);
      if($seriest>0);
	 print "WARNING: `EXP'(%$)" $seriesx;
	 print "   contains negative powers of %$ ,%"  $seriesvar;
	 print "which cannot be expanded";
      endif;

      #call `NAMESPACE'getCoefficients(x,$seriesvar,`$seriesmaxtermnum',a)

*     determine coefficients of expanded function
      $serieslim = $seriescut - count_($seriesvar,1);

      $seriesb0 = 1;
      #do n=1,`$seriesmaxtermnum'
	 if(`n'>$serieslim) goto afterloop`$serieslabelnum';
	 $seriesb`n' =
	 #do i=1,`n'
	    + `i'/`n'*$seriesa`i'*$seriesb{`n'-`i'}
	 #enddo
	 ;
      #enddo
      label afterloop`$serieslabelnum';

*     multiply by expanded function
      $seriessum=sum_([series::i],0,$serieslim,[series::b]([series::i]));
      once `EXP'($seriesx) = $seriessum;

      $seriest=termsin_($seriesa0);
      if($seriest>0) multiply `EXP'($seriesa0);

   endif;

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure
#procedure `NAMESPACE'expandPower(POW,?SERIESSPEC)
*replaces `POW'(x,y) by x^y, treating both x and y as series (as specified by the procedure series)

*uses `POW'(x,y)=exp(y*log(x))

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

   $seriesorigcut = $seriescut;
   $seriescut = $seriesorigcut - count_($seriesvar,1);
   id `POW'([series::x]?,[series::y]?)=[series::EXP]([series::y]*[series::LOG]([series::x]));

   argument [series::EXP];
      #call `NAMESPACE'expandLog([series::LOG]);
      multiply replace_([series::LOG],log);
   endargument;

*  restore original cut
   $seriescut=$seriesorigcut;
   #call `NAMESPACE'expandExp([series::EXP]);

   multiply replace_([series::EXP],exp);

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure

#procedure `NAMESPACE'expandGamma(GAMMA,?SERIESSPEC)
* expand Gamma functions in $seriesvar up to power $seriescut

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

   #define l

*  increase label number to make sure it's unique
   #$serieslabelnum=`$serieslabelnum'+1;

   while(match(`GAMMA'([series::x]?$seriesx)));

      #call `NAMESPACE'getCoefficients(x,$seriesvar,`$seriesmaxtermnum',a)

*     determine coefficients of expanded function
      $serieslim = $seriescut - count_($seriesvar,1);

      $seriesb0 = 1;
      #do n=1,`$seriesmaxtermnum'
	 if(`n'>$serieslim) goto afterloop`$serieslabelnum';
	 #$seriesPARTSIZE = 0;
*        sum over partitions of `n'
	 #do i = 0,0,0
	    #call `NAMESPACE'nextPartition(`n',PART)
	    #call `NAMESPACE'computeMultiplicities(PART,MULTIPLICITY)
	    #if `$seriesPARTSIZE' == 0
*	       after last partition
	       #breakdo

	       #elseif `$seriesPARTSIZE' == 1
*              trivial partition
	       $seriesb`n' = psi(0,$seriesa0)*$seriesa`n';

	       #else
	       $seriesb`n' =
	       + $seriesb`n'
	       + psi({`$seriesPARTSIZE'-1},$seriesa0)
	       #do j=1,`$seriesPARTSIZE',1
		  #redefine l "`$seriesPART`j''"
		  * $seriesa`l'^`$seriesMULTIPLICITY`l''/{`$seriesMULTIPLICITY`l''!}
		  #redefine j "{`j'+`$seriesMULTIPLICITY`l''-1}"
	       #enddo
	       + {{`$seriesPARTSIZE'-1}!}
	       #do j=1,`$seriesPARTSIZE',1
		  #redefine l "`$seriesPART`j''"
		  * (-$seriesb`l')^`$seriesMULTIPLICITY`l''/{`$seriesMULTIPLICITY`l''!}
		  #redefine j "{`j'+`$seriesMULTIPLICITY`l''-1}"
	       #enddo
	       ;
	    #endif
	 #enddo
      #enddo
      label afterloop`$serieslabelnum';

*     multiply by expanded function
      $seriessum= sum_([series::i],0,$serieslim,[series::b]([series::i]));
      once `GAMMA'($seriesx) = [series::Gamma]($seriesa0) * $seriessum;

   endwhile;

   multiply replace_([series::Gamma],`GAMMA');

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure
#procedure `NAMESPACE'expandFunction(FUN,?SERIESSPEC)
*expands function FUN
*(the argument is considered as a series in $seriesvar up to power $seriescut)

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'localSeries(`?SERIESSPEC')
   #endif

*  increase label number to make sure it's unique
   #$serieslabelnum=`$serieslabelnum'+1;

   while(match(`FUN'([series::x]?)));

      once `FUN'([series::x]?$seriesx)=1;

      #call `NAMESPACE'getCoefficients(x,$seriesvar,`$seriesmaxtermnum',a)

*     multiply by expanded function

      $serieslim = $seriescut - count_($seriesvar,1);
      $seriesb0=D([series::f]($seriesa0),0);
      #do n=1,`$seriesmaxtermnum'
	 if(`n'>$serieslim) goto afterloop`$serieslabelnum';
	 $seriesb`n' =
	 #do i=1,`n'
	    + `i'/`n'*$seriesa`i'*$seriesb{`n'-`i'}
	 #enddo
	 ;
	 inside $seriesb`n';
	    id D([series::x]?,[series::y]?)=D([series::x],[series::y]+1);
	 endinside;
      #enddo
      label afterloop`$serieslabelnum';
      $seriesb0=[series::f]($seriesa0);

      $seriessum=sum_([series::i],0,$serieslim,[series::b]([series::i]));
      multiply $seriessum;

   endwhile;

   multiply replace_([series::f],`FUN');

   #ifdef `?SERIESSPEC'
      #call `NAMESPACE'restoreSeries
   #endif

#endprocedure
#procedure `NAMESPACE'getCoefficients(X,VAR,CUT,C)
*   extract the coefficients of `VAR' to some power in $series`X'
*   the powers can range from 0 to `CUT'
*   the resulting coefficients are saved to $series`C'0,...,$series`C'`CUT'

   #do i=0,`CUT'
      $series`C'`i' = 0;
   #enddo

*  this is O(`CUT'*termsin_($series`X')), but should be O(termsin_($series`X'))
*  O(log(`CUT')*termsin_($series`X')) could be achieved with a binary search,
*  but this does not appear to be a performance bottleneck
   inside $series`X';
      $seriesc=count_(`VAR',1);
      if($seriesc==0);
         $series`C'0 = $series`C'0 + term_();
	 #do n=1,`CUT'
	    elseif($seriesc==`n');
	    $series`C'`n'=$series`C'`n'+term_();
	 #enddo
	 else;
	 print "power %$ out of range [0,`CUT']" $seriesc;
	 print "   in term %t";
	 setexitflag;
      endif;
   endinside;
   
#endprocedure
#procedure `NAMESPACE'parallel
*contains the instructions that are necessary for
* parallel execution of a module when the *function
* procedures are used

   moduleoption local $seriesvar,$seriescut,$seriesvarstore,$seriescutstore;
   moduleoption local <$seriesa0>,...,<$seriesa`$seriesmaxtermnum'>;
   moduleoption local <$seriesb0>,...,<$seriesb`$seriesmaxtermnum'>;
   moduleoption local $seriesminterm,$seriesinvminterm,$seriesminpow,$seriesc,$serieslim,$seriesx,$seriest,$seriessum,$seriesorigcut;

#endprocedure
#procedure `NAMESPACE'nextPartition(N,PART)
*   compute the next integer partition for N
*   the current partition is given by ($series`PART'1,...,$series`PART`$series`PART'SIZE'')
*   initially $series`PART'SIZE should be set to 0
*   the new partition will again be saved to
*   ($series`PART'1,...,$series`PART`$series`PART'SIZE'')

   #if `$series`PART'SIZE' == 0
*     first partition
      #call `NAMESPACE'nextLongerPartition(`N',`PART')

      #elseif `$series`PART'1' == 1
*     last partition
      #$series`PART'SIZE = 0;
      #$series`PART'1 = 0;

      #elseif `$series`PART'1' == 2
      #call `NAMESPACE'nextLongerPartition(`N',`PART')

      #else
*     next partition
*     try tro find a pair of elements which differ by more than 1
      #do i=2,{`$series`PART'SIZE'+1}
	 #if `$series`PART'`i'' < {`$series`PART'1'-1}
	    #if `i' > `$series`PART'SIZE'
	       #$series`PART'SIZE = {`$series`PART'SIZE'+1};
	       #$series`PART'{`$series`PART'SIZE'+1} = 0;
	    #endif
	    #define DIFF "1"
	    #$series`PART'`i' = {`$series`PART'`i''+1};
	    #do j=2,{`i'-1}
	       #redefine DIFF "{`DIFF'+`$series`PART'`i''-`$series`PART'`j''}"
	       #$series`PART'`j' = `$series`PART'`i'';
	    #enddo
	    #$series`PART'1 = {`$series`PART'1'-`DIFF'};
	    #breakdo
	 #endif
      #enddo
   #endif

#endprocedure

#procedure `NAMESPACE'nextLongerPartition(N,PART)

   #define LENGTH "{`$series`PART'SIZE'+1}"
   #$series`PART'SIZE = `LENGTH';
   #$series`PART'1 = {`N'-`LENGTH'+1};
   #do i=2,`LENGTH'
      #$series`PART'`i' = 1;
   #enddo
   #$series`PART'{`LENGTH'+1} = 0;

#endprocedure

#procedure `NAMESPACE'computeMultiplicities(PART,MUL)

*   the multiplicity of any element e of the partition
*   ($series`PART'1,...,$series`PART`$series`PART'SIZE'') will be saved to $series`MUL'`i'

   #define N

   #do i=1,`$series`PART'SIZE'
      #redefine N "`$series`PART'`i''"
      #$series`MUL'`N'=0;
   #enddo

   #do i=1,`$series`PART'SIZE'
      #redefine N "`$series`PART'`i''"
      #$series`MUL'`N'= {`$series`MUL'`N''+1};
   #enddo

#endprocedure

#procedure `NAMESPACE'localSeries(VAR,CUT)
* set $seriesvar and $seriescut to local values

   #ifdef `$seriesvar'
      $seriesvarstore = $seriesvar;
      $seriescutstore = $seriescut;
      #else
      $seriesvarstore = `VAR';
      $seriescutstore = `CUT';
   #endif
   $seriesvar = `VAR';
   $seriescut = `CUT';

#endprocedure

#procedure `NAMESPACE'restoreSeries()
* restore global values of $seriesvar and $seriescut

   $seriesvar = $seriesvarstore;
   $seriescut = $seriescutstore;

#endprocedure
#endif
