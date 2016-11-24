CFunctions den;

#include- series.hh

#Procedure getHighestPole(expression, regulator)
* Extract the highest pole of a regulator in an expression consisting of terms prf(...,...)*INT(...)
* Result is stored in $highestPole
* Requires:
*   CFunction prf,SCREEN;
*   Symbols sDUMMY1, sDUMMY2;

  Hide;
  Nhide localExpression;
  L localExpression = `expression';
  .sort

  PolyRatFun prf(divergence,`regulator');
  .sort

  Id SCREEN?!{,prf}(?a)=1;
  Id sDUMMY1?=1;
  .sort

  PolyRatFun;
  Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1/sDUMMY2;
  Id `regulator'^sDUMMY1?$highestPole = sDUMMY1;
  .sort

  Drop localExpression;
  Unhide;
  .sort

#EndProcedure

#Procedure seriesExpand(expression, regulator, order)
* Series expand an expression consisting of terms prf(...,...)*INT(...) in a regulator to a given order
* WARNING: Should only be called once per FORM session
* Requires:
*   CFunction prf,den;
*   Symbols sDUMMY1;
*   Procedure: getHighestPole
*   Include Package: series.hh (Andreas Maier)

  Hide;
  Nhide `expression';
  .sort

* Ensure series starts A + B*regulator + ...
  #call getHighestPole(`expression', `regulator'); * Defines $highestPole
  Multiply prf(1,`regulator'^$highestPole);
  .sort

* Simplify
  PolyRatFun prf;
  .sort
  PolyRatFun;
  .sort

  Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1*den(sDUMMY2);

  #$highestRegulatorPowerInDenominator = 0;
  Argument den;
    if ( count(`regulator',1) > $highestRegulatorPowerInDenominator ) $highestRegulatorPowerInDenominator = count_(`regulator',1);
* Print "      >> <%w> After %t the maximum power of regulator is %$",$highestRegulatorPowerInDenominator;
  EndArgument;
  ModuleOption,maximum,$highestRegulatorPowerInDenominator;
  .sort

*  #Write "$highestPole = `$highestPole'"
*  #Write "$highestRegulatorPowerInDenominator = `$highestRegulatorPowerInDenominator'"

  #define SERIESTERMS "{-`$highestPole'+ 1 + `order'}"
  #if ( `SERIESTERMS' > `$highestRegulatorPowerInDenominator' )
    #call init(`SERIESTERMS')
  #else
    #call init(`$highestRegulatorPowerInDenominator')
  #endif

  #call series(`regulator',{`SERIESTERMS'-1})
  #call expand(den)
  .sort

* Restore correct dependence on regulator
  Multiply `regulator'^$highestPole;
  .sort

#EndProcedure
