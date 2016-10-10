* vim: syntax=form:ts=3:sw=3:expandtab
*
* This version of golem.frm generates expressions for the numerator
* only.
*
#-
*on shortstatistics;
off statistics;
*on statistics;

* The reference vectors are determined by the global setting
* 'reference-vectors' in the configuration file.
* Changing them here might lead to inconsistent results.[%
@for particles %][%
   @if is_massive
      %]
#define REFk[%index%] "[%
      @if eval reference > 0 %]k[%reference %][%
      @else %]l[% eval - reference %][%
      @end @if %]"[%
   @else %][%
      @select 2spin @case 2 3 4 %]
#define REFk[%index%] "[%
         @if eval reference > 0 %]k[%reference %][%
         @else %]l[% eval - reference %][%
         @end @if %]"[%
      @end @select %][%
   @end @if %][% 
@end @for %][%
@if extension dred %]
#Define DRED "defined"[%
@end @if %][%
@if internal REQUIRE_FR5 %]
#Define FR5 "defined"[%
@end @if %]

#Define EXTRAPAT "EXSYM"[%
@if extension topolynomial %]
#If (`VERSION_' >= 4) && (`SUBVERSION_' >= 0)
   #Define USETOPOLYNOMIAL "1"
#Else
   #Define USETOPOLYNOMIAL "0"
#EndIf[%
@else %]
#Define USETOPOLYNOMIAL "0"[%
@end @if %]

[%
@if extension tracify %]
AutoDeclare S Qeps;
CTensor epstensor;[%
@end @if %]

[%
@if extension formopt %]
#If `LOOPS' == 1
   #Define abb`DIAG' "0"
   Autodeclare Symbol Qsp;
   #Include- abbreviate.hh
   Symbol CC, R2;
#Else
   #Include- optimizeborn.hh
#EndIf[%
@else %]
#If `LOOPS' == 1
   #Include- abbreviate.hh
   #Create <`OUTFILE'.abb>
#EndIf[%
@end @if %]

#include- spinney.hh
#redefine SPCANCEL "0"

#include- symbols.hh

#ifndef `USEVERTEXPROC'
   #include- vertices.hh
#endif

CFunctions Spab3, Spba3;
CFunction epspow;
AutoDeclare Vectors spva;

*
* We introduce the additional symbols
* - Qt2 = \tilde{Q}^2
*
Symbol Qt2;
Function SmQt;
[% @if diagsum %]Symbol Nfrat;[%
@end @if %]


#If `USETOPOLYNOMIAL'
   ExtraSymbols,underscore,`EXTRAPAT';
#EndIf

#include- color.hh
.global

[%
@if generate_uv_counterterms %]
#IfDef `CTFLG'
#If `CTFLG' == 1
  #include- diagrams-`LOOPS'ct.hh #global[%
  @if generate_ct_internal %]
  #include- model.hh[%
  @else %]
  #include- modelct.hh[%
  @end @if %]
#Else 
  #include- diagrams-`LOOPS'.hh #global
  #include- model.hh  
#EndIf
#Else
  #include- diagrams-`LOOPS'.hh #global
  #include- model.hh  
#Endif[%
@else %]
#include- diagrams-`LOOPS'.hh #global
#include- model.hh[%
@end @if %][%
@if diagsum %]
#If `LOOPS' == 0[%
@if generate_uv_counterterms %]
#If `CTFLG' == 1
#include- diagrams-`LOOPS'ct.hh #diagram`DIAG'
#Else 
#include- diagrams-`LOOPS'.hh #diagram`DIAG'
#EndIf[%
@else %]
#include- diagrams-`LOOPS'.hh #diagram`DIAG'[%
@end @if %]
#Else
F diag1,...,diag`DIAGRAMCOUNT';
#include- diagsum.frm #diag`DIAG'
#EndIf[%
@else %]
#include- diagrams-`LOOPS'.hh #diagram`DIAG'[%
@end @if %][%
@select r2
@case explicit only %]
#If `LOOPS' == 1
   #include- r2.hh
   #include- r2integrals.hh
#EndIf[%
@end @select %]

#ifdef `ISDUMMY'
   Multiply 0;
#endif

Id QGRAFSIGN(sDUMMY1?) = 1;

#call zeroes


* models that implement their own vertex replacements
* must define the preprocessor variable USEVERTEXPROC
* in the (Form-)model file and, in the same file,
* define the procedure ReplaceVertices
#ifndef `USEVERTEXPROC'
   #Call ExpandVertices
#else
   Repeat;
      #call ReplaceVertices
   EndRepeat;
#endif

#call VertexConstants
#call ones
#call zeroes

#if `LOOPS' > 0
   Id deltaaxial = 0;
#else
   #ifdef `FR5'
      Id deltaaxial^2 = 0;
   #else
      Id deltaaxial = 0;
   #endif
#endif

*---#[ Process Propagators:
* If the mass is zero the width becomes irrelevant:
Id proplorentz(sDUMMY1?, vDUMMY1?, 0, sDUMMY3?, ?tail) =
   proplorentz(sDUMMY1, vDUMMY1, 0, 0, ?tail);

*#IfDef `MASSIVEBUBBLE'
*
* NOTE: If you plan to insert your own renormalization code here
*       check if you need to undefine MQSE:
*
* #Undefine MQSE
*
*   #$MASSIVEBUBBLESIZE = nargs_(`MASSIVEBUBBLE') / 3;
*   #If `$MASSIVEBUBBLESIZE' == 1
*      #Message This is a massive tadpole: `MASSIVEBUBBLE'
*   #Else
*      #Message This is a massive two-point function: `MASSIVEBUBBLE'
*   #EndIf
*#EndIf

[% @if generate_uv_counterterms %][%
@else %]
#IfDef `MQSE'
  SplitArg (p1), proplorentz;

  Id proplorentz(1, vDUMMY1?, vDUMMY2?, sDUMMY1?, sDUMMY2?, 0, iDUMMY1?, iDUMMY2?) *
     proplorentz(2, vDUMMY3?, vDUMMY4?,        0,        0, 0, iDUMMY3?, iDUMMY4?) =

     + proplorentz(1, vDUMMY1 + vDUMMY2, sDUMMY1, sDUMMY2, 0, iDUMMY1, iDUMMY2) *
       proplorentz(2, vDUMMY3 + vDUMMY4,       0,       0, 0, iDUMMY3, iDUMMY4)
     + fDUMMY1(vDUMMY1, vDUMMY2, vDUMMY3, vDUMMY4, sDUMMY1, sDUMMY2,
               iDUMMY1, iDUMMY2, iDUMMY3, iDUMMY4);
  .sort:MQSE 1.0;
  Id fDUMMY1(?head, ZERO, -p1, ?tail) =
     fDUMMY1(?head, ZERO,  p1, ?tail);

  Id fDUMMY1(?head,  vDUMMY1?, -p1, ?tail) =
     fDUMMY1(?head, -vDUMMY1,   p1, ?tail);

 Id fDUMMY1(vDUMMY1?, p1, ZERO, p1, sDUMMY1?, sDUMMY2?,
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = + deltaOS * csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)) / 4 *
       (
      + (6*p1.vDUMMY1 + 3*(vDUMMY1.vDUMMY1-csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))))*
        inv(csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)))
      + 3*(4-2*deltaHV)*Qt2*inv(vDUMMY1.vDUMMY1-3*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)))
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);
  Id fDUMMY1(ZERO, p1, vDUMMY2?, p1, sDUMMY1?, sDUMMY2?,
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = - deltaOS * csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)) / 4 *
       (
      + (6*p1.vDUMMY2 + 3*(vDUMMY2.vDUMMY2+csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))))*
        inv(csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)))
      - 3*(4-2*deltaHV)*Qt2*inv(vDUMMY2.vDUMMY2-3*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2))*csqrt(sDUMMY1*(sDUMMY1-i_*sDUMMY2)))
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);

 Id fDUMMY1(vDUMMY1?, p1, ZERO, p1, sDUMMY1?, ZERO,
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = + deltaOS * sDUMMY1 / 4 *
       (
      + (6*p1.vDUMMY1 + 3*(vDUMMY1.vDUMMY1-sDUMMY1*sDUMMY1))*
        inv(sDUMMY1*sDUMMY1)
      + 3*(4-2*deltaHV)*Qt2*inv(vDUMMY1.vDUMMY1-3*sDUMMY1*sDUMMY1)
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);
  Id fDUMMY1(ZERO, p1, vDUMMY2?, p1, sDUMMY1?, ZERO,
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = - deltaOS * sDUMMY1 / 4 *
       (
      + (6*p1.vDUMMY2 + 3*(vDUMMY2.vDUMMY2+sDUMMY1*sDUMMY1))*
        inv(sDUMMY1*sDUMMY1)
      - 3*(4-2*deltaHV)*Qt2*inv(vDUMMY2.vDUMMY2-3*sDUMMY1*sDUMMY1)
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);

   #IfDef `DRED'
      Id deltaHV = 0;
   #Else
      Id deltaHV = -1/2;
   #EndIf
   .sort:MQSE 1.1;
#EndIf[%
@end @if %]

#include- propagators.hh

#if `LOOPS' == 1
    SplitArg (p1), inv, 1;
   Id inv(k1?, p1, ?tail) = 1;
   Id inv(k1?, -p1, ?tail) = 1;
   Id inv(-p1, ?tail) = 1;
   Id inv(p1, ?tail) = 1;
#endif
Id inv(k1?, m?, sDUMMY1?) = inv(k1.k1 - m^2 + i_ * m * sDUMMY1);
Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id inv(0, m?) = - inv(m^2);
Id inv(0, m?, sDUMMY1?) = + inv(-m^2 + i_ * m * sDUMMY1);

Argument inv;
   Id ZERO = 0;
   #call kinematics
EndArgument;
Id inv(sDUMMY1?symbol_) = 1/sDUMMY1;
Argument log;
   Id ZERO = 0;
   #call kinematics
EndArgument;

[% @if internal CUSTOM_SPIN2_PROP %]
Id customSpin2Prop(k1?, m?, sDUMMY1?) = customSpin2Prop(k1.k1,m^2 - i_ * m * sDUMMY1);

Argument customSpin2Prop;
    Id ZERO = 0;
    #call kinematics
EndArgument;[% @end @if %]


*Brackets SplitLorentzIndex;
.sort:part 0.9.0;
*Keep Brackets;

Repeat Id SplitLorentzIndex(iDUMMY1?, iDUMMY2?, ?tail1) *
          SplitLorentzIndex(iDUMMY1?, iDUMMY4?, ?tail2) =
   SplitLorentzIndex(iDUMMY1, ?tail1) *
   SplitLorentzIndex(iDUMMY1, ?tail2) * d_(iDUMMY2, iDUMMY4);
Id SplitLorentzIndex(iDUMMY1?) * SplitLorentzIndex(iDUMMY1?) = 1;
*---#] Process Propagators:

#call coloralgebra(0)

*---#[ Process Legs:
*#if `LOOPS' == 1
*   #call loopflow(`DIAG')
*#else
*   #call treeflow(`DIAG')
*#endif

#call rewritelegs

Id fDUMMY1?{inplorentz,outlorentz}(sDUMMY1?!{-1,1}, ?tail) =
   SCREEN(fDUMMY1(sDUMMY1, ?tail));
#include- legs.hh

#IfNDef `USEVERTEXPROC'
   Repeat;
        #Call ExpandLorentzStructures
      Id ZERO = 0;
      Id d(ZERO, iDUMMY1?) = 0;
      Id d(vDUMMY1?{`EXTERNAL'}, iDUMMY1?) = vDUMMY1(iDUMMY1);
      Repeat Id vDUMMY1?{`EXTERNAL'}(iDUMMY1?) * d(iDUMMY1?, iDUMMY2?) =
         vDUMMY1(iDUMMY2);
      #Call kinematics
   EndRepeat;
#Else
   #Call kinematics
   Id ZERO = 0;
#EndIf

Argument;
  Id ZERO = 0;
EndArgument;

.sort:subst. vertices and fermion legs;

repeat id d(iv1L?, iv2L?) * d(iv2L?, iv3L?) = d(iv1L, iv3L);

#Call RemoveNCContainer

#Do f = {`FERMIONS',}
   #If "`f'" != ""
      Id fDUMMY1?{UbarSpa,UbarSpb}(k`f', ?tail) =
         NCSIGN(`f') * fDUMMY1(k`f', ?tail);
      Id fDUMMY1?{USpa,USpb}(k`f', ?tail) =
         fDUMMY1(k`f', ?tail) * NCSIGN(`f');
   #EndIf
#EndDo
.sort:process fermions;

Id SCREEN(sDUMMY1?) = sDUMMY1;[%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector initial %]
Id inplorentz(2, ivL2?, k[% index %], 0) *
   inp(field1?, k[% index %], sDUMMY1?{-1,1}, vDUMMY1?) = e[%index%](ivL2);[%
   @end @for %][%
   @for particles lightlike vector final %]
Id outlorentz(2, ivL2?, k[% index %], 0) *
   out(field1?, k[% index %], sDUMMY1?{-1,1}, vDUMMY1?) = e[%index%](ivL2);[%
   @end @for %][%
@end @if %]
#include- legs.hh

* The rules of legs.hh do not restore all inp() and out()
* functions after we introduce the gauge check.
#if `GAUGEVAR'
   Id fDUMMY1?{inp,out}(sDUMMY1?, iDUMMY1?, vDUMMY1?, ?tail) =
      fDUMMY1(sDUMMY1, iDUMMY1, vDUMMY1);
#endif

Id inp(?all) = 1;
Id out(?all) = 1;

Id ZERO = 0;

#call zeroes
Id csqrt(0) = 0;
*---#] Process Legs:

Repeat Id SplitLorentzIndex(iDUMMY1?, iDUMMY2?, ?tail1) *
          SplitLorentzIndex(iDUMMY1?, iDUMMY4?, ?tail2) =
   SplitLorentzIndex(iDUMMY1, ?tail1) *
   SplitLorentzIndex(iDUMMY1, ?tail2) * d_(iDUMMY2, iDUMMY4);
Id SplitLorentzIndex(iDUMMY1?) * SplitLorentzIndex(iDUMMY1?) = 1;
.sort:part 1;

Multiply replace_(Sqrt2, sqrt2);
Id sqrt2^2  = 2;
Id sqrt2^-2 = 1/2;

Multiply replace_(Sqrt3, sqrt3);
Id sqrt3^2  = 3;
Id sqrt3^-2 = 1/3;

#if `LOOPS' == 1
* Discrepancy between loop-integral libraries' convention 1/(i\pi^(n/2))
* and 1/(2\pi)^n leaving out the pre-factors as described
* in the manual.
   Multiply PREFACTOR(i_/2);
#endif

Repeat Id PREFACTOR(sDUMMY1?) * PREFACTOR(sDUMMY2?) =
   PREFACTOR(sDUMMY1 * sDUMMY2);

Id PREFACTOR(sDUMMY1?) = sDUMMY1;

Argument SpDenominator;
   #Call spsymbols
EndArgument;

Argument inv;
   #Call kinematics
EndArgument;

[% @if internal CUSTOM_SPIN2_PROP
%]Argument customSpin2Prop;
   #Call kinematics
EndArgument;[% @end @if %]


#IfDef `FR5'
   #If `LOOPS'==0
      Brackets deltaaxial;
.sort:split fin ren 1;
      Local diagram`DIAG'fr = diagram`DIAG'[deltaaxial];
      Id deltaaxial = 0;
   #EndIf
#EndIf

#Call lightconedecomp
Argument SpDenominator;
   #Call spsymbols
EndArgument;

* tHooftAlgebra will split all Dirac matrices Sm
* into Sm4 + SmEps. That would generate 2^n
* terms for n matrices, many of which become zero
* later on. To avoid this as far as possible we
* replace here all matrices contracted to external momenta.
#If `LOOPS' == 1
   #IfDef `DRED'
      Id d(iDUMMY1?, iDUMMY2?) = d4(iDUMMY1, iDUMMY2);
      Id Sm(iDUMMY1?) = Sm4(iDUMMY1);
   #Else
      Id Sm(vDUMMY1?{`EXTERNAL'}) = Sm4(vDUMMY1);
      Id d(vDUMMY1?{`EXTERNAL'}, iDUMMY1?) = d4(vDUMMY1, iDUMMY1);
* If there are any p1's in the first place we better protect them
* in order not to lose dimensionality information:
      Id p1.p1 = d(p1, p1);
      Id p1.vDUMMY1?{`EXTERNAL'} = d4(p1, vDUMMY1);
      Id p1(iDUMMY1?) = d(p1, iDUMMY1);
   #EndIf
#Else
   Id Sm(iDUMMY1?) = Sm4(iDUMMY1);
   Id d(iDUMMY1?, iDUMMY2?) = d4(iDUMMY1, iDUMMY2);
#EndIf

.sort:part 3.5;

#Call tHooftAlgebra

[% @if extension better_num %]



#If `LOOPS' == 1
   
   #IfDef `DRED'
    Id d4(p1,p1) = d4(p1,p1) - Qt2;
    Id Sm4(p1) = Sm4(p1) + SmQt;
    Repeat;
        Repeat Id Sm4(p1)*Sm4(p1) = d4(p1,p1);
        
            Id SmQt * Sm4(iDUMMY1?) = - Sm4(iDUMMY1) * SmQt;
    Endrepeat
        Id p1.p1 = p1.p1 - Qt2;
        Id d4(p1, p1) = p1.p1;
        Id SmQt * SmQt = -Qt2;
        Id SmQt = 0;
   #Else
      Id dEps(iDUMMY1?, iDUMMY1?) = -2*eps;
      Id dEps(p1, p1) = -Qt2;
      Id dEps(vDUMMY1?{`EXTERNAL'}, iDUMMY2?) = 0;
   #EndIf

* Qt2 terms only contribute to finite part
* Therefore Qt2 * eps cannot contribute to the result
   Id Qt2 * eps = 0;
   Id eps^sDUMMY1?{>2} = 0;

   #If `LOOPSIZE' > 6
      Id Qt2 = 0;


   #ElseIf `LOOPSIZE' == 5
      ToTensor, Functions, p1, ptens;
      If(count(ptens,1)==0) Multiply ptens;
* For pentagons we need to consider integrals of rank 6 only
      Id Only ptens * Qt2 = 0;
      Id Only ptens * Qt2^2 = 0;
      Id Only ptens(iDUMMY1?) * Qt2 = 0;
      Id Only ptens(iDUMMY1?,iDUMMY2?) * Qt2 = 0;
      Id Only ptens(iDUMMY1?,iDUMMY2?,iDUMMY3?) * Qt2 = 0;
      ToVector, ptens, p1;
   #ElseIf `LOOPSIZE' == 4
      ToTensor, Functions, p1, ptens;
      If(count(ptens,1)==0) Multiply ptens;
* For boxes we need to consider integrals of type mu2*ptens(mu,nu),
* mu2^2 and the one with rank 5
      Id Only ptens * Qt2 = 0;
      Id Only ptens(iDUMMY1?) * Qt2 = 0;
      ToVector, ptens, p1;
   #EndIf

#Else
   Id dEps(iDUMMY1?, iDUMMY1?) = 0;
#EndIf

[% @else %]

#If `LOOPS' == 1
   
   #IfDef `DRED'
      Repeat;
         Repeat Id Sm4(p1)*Sm4(p1) = d4(p1,p1);
         Id Sm4(p1) * Sm4(iDUMMY1?) =
            - Sm4(iDUMMY1) * Sm4(p1) + 2 * d4(p1, iDUMMY1);
      EndRepeat;
      Id d4(p1, p1) = p1.p1;
      Id p1.p1 = p1.p1 - Qt2;
   #Else
      Id dEps(iDUMMY1?, iDUMMY1?) = -2*eps;
      Id dEps(p1, p1) = -Qt2;
      Id dEps(vDUMMY1?{`EXTERNAL'}, iDUMMY2?) = 0;
   #EndIf

* Qt2 terms only contribute to finite part
* Therefore Qt2 * eps cannot contribute to the result
   Id Qt2 * eps = 0;
   Id eps^sDUMMY1?{>2} = 0;

   #If `LOOPSIZE' > 6
      Id Qt2 = 0;


   #ElseIf `LOOPSIZE' == 5
      ToTensor, Functions, p1, ptens;
      If(count(ptens,1)==0) Multiply ptens;
* For pentagons we need to consider integrals of rank 6 only
      Id Only ptens * Qt2 = 0;
      Id Only ptens * Qt2^2 = 0;
      Id Only ptens(iDUMMY1?) * Qt2 = 0;
      Id Only ptens(iDUMMY1?,iDUMMY2?) * Qt2 = 0;
      Id Only ptens(iDUMMY1?,iDUMMY2?,iDUMMY3?) * Qt2 = 0;
      ToVector, ptens, p1;
   #ElseIf `LOOPSIZE' == 4
      ToTensor, Functions, p1, ptens;
      If(count(ptens,1)==0) Multiply ptens;
* For boxes we need to consider integrals of type mu2*ptens(mu,nu),
* mu2^2 and the one with rank 5
      Id Only ptens * Qt2 = 0;
      Id Only ptens(iDUMMY1?) * Qt2 = 0;
      ToVector, ptens, p1;
   #EndIf

#Else
   Id dEps(iDUMMY1?, iDUMMY1?) = 0;
#EndIf[%
@end @if %]

#Call SpCollect
#Call SpClear()

#call SpContractMetrics
#call SpTrace4(`LIGHTLIKE')
.sort:part 4;

ChainIn NCSIGN;
Id NCSIGN(`FERMIONS') = 1;

#call SpContractLeviCivita(`LIGHTLIKE')
#call SpContractMetrics
#call SpClear()

Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, vDUMMY1?, ?tail) = 0;
Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(?head, vDUMMY1?, vDUMMY1?) = 0;

#call SpContract
#call SpOpen(`LIGHTLIKE')

#If `LOOPS' == 1[%
@select r2
@case implicit %]
* Implicit reduction of R2 term:
* All terms in the numerator which come with a \epsilon or \mu^2
* are reduced with the reduction library (Samurai/Golem95/PJFry etc.)
.sort 5.3;
Local d`DIAG'R2 = 0;[%
@case explicit %]
* Explicit reduction of R2 term:
* All terms in the numerator which come with a \epsilon or \mu^2
* are replaced by explicit expressions.
   Brackets eps, Qt2;
.sort 5.3;
   Local d`DIAG'R2 = 
      + diagram`DIAG'[eps] * fDUMMY1(eps)
      + diagram`DIAG'[Qt2] * fDUMMY1(Qt2)
      + diagram`DIAG'[Qt2^2] * fDUMMY1(Qt2^2)
      + diagram`DIAG'[Qt2^3] * fDUMMY1(Qt2^3);
   Id eps = 0;
   Id Qt2 = 0;
   Id fDUMMY1(eps?) = eps;
.sort 5.4;
   Hide diagram`DIAG';
   #call ReduceDiagramR2(`DIAG')
.sort 5.5;
   UnHide diagram`DIAG';[%
@case off %]
* R2 term is discarded:
* All terms in the numerator which come with a \epsilon or \mu^2
* are set to zero.
   Brackets eps, Qt2;
.sort 5.3;
   Id eps = 0;
   Id Qt2 = 0;
.sort 5.3;[%
@case only %]
* R2 term only:
* All terms in the numerator which come with a \epsilon or \mu^2
* are replaced by explicit expressions. Everything else is discarded.
   Brackets eps, Qt2;
.sort 5.3;
   Local d`DIAG'R2 = 
      + diagram`DIAG'[eps] * fDUMMY1(eps)
      + diagram`DIAG'[Qt2] * fDUMMY1(Qt2)
      + diagram`DIAG'[Qt2^2] * fDUMMY1(Qt2^2)
      + diagram`DIAG'[Qt2^3] * fDUMMY1(Qt2^3);
   Id eps = 0;
   Id Qt2 = 0;
   Id fDUMMY1(eps?) = eps;

   If(count(eps,1,Qt2,1)==0) Discard;
.sort 5.4;
   Hide diagram`DIAG';
   #call ReduceDiagramR2(`DIAG')
.sort 5.5;
   UnHide diagram`DIAG';[%
@else %]
   #message Undefined value for r2: "[% r2 %]"
   #terminate[%
@end @select %]
#EndIf


#if `LOOPS' == 1[%
@if extension tracify%]
* Combine multiple spinor lines to one spinor line.
* As a consequence, at most rank-l (where l is the
* number of loops) tensor integrals appear.

Hide d`DIAG'R2;

#call SpClose()

#Do left={`LIGHTLIKE'}
  #Do right={`LIGHTLIKE'}
    #if `right' != `left'
      #Do X={a,b}
        #Do Z={a,b}
          Id Sp`X'a(?head,`left')*Spa`Z'(`right',?tail) = Sp`X'a(?head,`left')*SpDenominator(Spbb(`left',`right'))*Spbb(`left',`right')*Spa`Z'(`right',?tail);
          #call SpClose()
          Id Sp`X'b(?head,`left')*Spb`Z'(`right',?tail) = Sp`X'b(?head,`left')*SpDenominator(Spaa(`left',`right'))*Spaa(`left',`right')*Spb`Z'(`right',?tail);
          #call SpClose()
        #EndDo
      #EndDo
    #EndIf
  #EndDo
#EndDo

#Do left={`LIGHTLIKE'}
  #Do right={`LIGHTLIKE'}
    #Do aux={`LIGHTLIKE'}
       #if `left' != `aux'
          #if `right' != `aux'
             #if `right' != `left'
                #call SpTracify(`left',`right',`aux',p1)
             #Else
*               If `right' == `left', we need two auxilary vectors for Spaa/Spbb
                #Do aux2={`LIGHTLIKE'}
                   #If `right' != `aux2'
                      #If `aux' != `aux2'
                         Id Spaa(`left',?chain,`right') = SpDenominator(Spbb(`right',`aux',`aux2',`left')) * trL * ProjMinus * Sm4(`left',?chain,`right',`aux',`aux2') * trR;
                         Id Spbb(`left',?chain,`right') = SpDenominator(Spaa(`right',`aux',`aux2',`left')) * trL * ProjPlus * Sm4(`left',?chain,`right',`aux',`aux2') * trR;

*                        But Spab/Spba can be closed to a trace without auxilary vectors if `left' == `right'
                         Id Spab(`left',?chain,`right') = trL * ProjMinus * Sm4(`left',?chain) * trR;
                         Id Spba(`left',?chain,`right') = trL * ProjPlus * Sm4(`left',?chain) * trR;
                      #EndIf
                   #EndIf
                #EndDo
             #EndIf
          #EndIf
       #EndIf
     #EndDo
  #EndDo
#EndDo
#call SpTrace4
.sort:tracify;
UnHide d`DIAG'R2;[%
@end @if extension tracify%][%
@if extension qshift %]
   #Call shiftmomenta(`DIAG',0)
   Argument Spab, Spaa, Spbb, Spba;
      #Call shiftmomenta(`DIAG',0)
   EndArgument;[%
@else %]
   Id p1 = Q;
   Argument Spab, Spaa, Spbb, Spba;
      Id p1 = Q;   
   EndArgument;[%
@end @if %]
   Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, iDUMMY2?, vDUMMY3?) = 
      fDUMMY1(vDUMMY1, iDUMMY2, vDUMMY3);
   #call SpOpen(`LIGHTLIKE')
#endif

Id d4(vDUMMY1?, iDUMMY1?) = vDUMMY1(iDUMMY1);

#If `LOOPS' == 1
   Id Spab(vDUMMY1?, Q?, vDUMMY2?) = Spab3(vDUMMY1, Q, vDUMMY2);
   Id Spba(vDUMMY1?, Q?, vDUMMY2?) = Spba3(vDUMMY1, Q, vDUMMY2);
* slight optimisation:
   Id Spba3(vDUMMY1?, iDUMMY1?, vDUMMY2?) = Spab3(vDUMMY2, iDUMMY1, vDUMMY1);
   Id Spab3(vDUMMY1?, iDUMMY1?, vDUMMY1?) = 2*vDUMMY1(iDUMMY1);
* better optimisation:
   #call spva
.sort:part 5.1;
#EndIf

[% @if generate_ct_internal %]
Id Spab(vDUMMY1?, kx, vDUMMY2?) = 0;
Id Spba(vDUMMY1?, kx, vDUMMY2?) = 0;[%
@end @if %]

Id Spa2(vDUMMY1?{`EXTERNAL'}, vDUMMY2?{`EXTERNAL'}) *
   Spb2(vDUMMY2?, vDUMMY1?) = 2 * fDUMMY1(vDUMMY1.vDUMMY2);

Id vDUMMY1?{`EXTERNAL'}.vDUMMY2?{`EXTERNAL'} = fDUMMY1(vDUMMY1.vDUMMY2);

Id SpDenominator(Spa2(vDUMMY1?{k1,...,k`LEGS'}, vDUMMY2?{k1,...,k`LEGS'})) *
   SpDenominator(Spb2(vDUMMY1?, vDUMMY2?)) = -1/2 * inv(vDUMMY1.vDUMMY2);

Argument inv, fDUMMY1;
#call kinematics
EndArgument;

[% @if internal CUSTOM_SPIN2_PROP
%]Argument customSpin2Prop, fDUMMY1;
#call kinematics
EndArgument;[% @end @if %]


Id fDUMMY1(sDUMMY1?) * inv(sDUMMY1?) = 1;
Id fDUMMY1(sDUMMY1?) = sDUMMY1;
Id inv(sDUMMY1?symbol_) = (1/sDUMMY1);

#call kinematics
Id vDUMMY1?{`LIGHTLIKE'}.vDUMMY2?{`LIGHTLIKE'} =
   1/2 * Spa2(vDUMMY1, vDUMMY2) * Spb2(vDUMMY2, vDUMMY1);

#call spsymbols[%
@if extension tracify%]
Argument;
  #call spsymbols
EndArgument;
#If `LOOPS' == 1
   Id e_(Q,vDUMMY1?,vDUMMY2?,vDUMMY3?) =  Qeps(vDUMMY1,vDUMMY2,vDUMMY3);
   Id e_(vDUMMY1?,Q,vDUMMY2?,vDUMMY3?) = -Qeps(vDUMMY1,vDUMMY2,vDUMMY3);
   Id e_(vDUMMY1?,vDUMMY2?,Q,vDUMMY3?) =  Qeps(vDUMMY1,vDUMMY2,vDUMMY3);
   Id e_(vDUMMY1?,vDUMMY2?,vDUMMY3?,Q) = -Qeps(vDUMMY1,vDUMMY2,vDUMMY3);

   Id e_(vDUMMY1?,vDUMMY2?,vDUMMY3?,vDUMMY4?) = epstensor(vDUMMY1,vDUMMY2,vDUMMY3,vDUMMY4);
#EndIf[%
@end @if %]

Id SpDenominator(sDUMMY1?) = (1/sDUMMY1);
Id inv(sDUMMY1?) = (1/sDUMMY1);

.sort:5.2;

[%
@if extension formopt %][%
@select r2 
@case explicit %]
#If `LOOPS' == 1
   #Create <`OUTFILE'.txt>
   #Create <`OUTFILE'.dat>[%
@if helsum %]
   #Call WriteUnoptimized(`R2PREFACTOR')[%
@else %]
   #Call  OptimizeCode(`R2PREFACTOR')[%
@end @if %]
   #Close <`OUTFILE'.txt>
   #Close <`OUTFILE'.dat>
#Else
   #If `BORNFLG' == 1
   #Create <`OUTFILE'.txt>
        #write <`OUTFILE'.txt> "#Procedure borndiag"
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == 0
        #Create <`OUTFILE'.txt>
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == -1
        #Append <borndiag.prc>
	#write <borndiag.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #ElseIf `BORNFLG' == 2
	#Create <borndiag.prc>
        #write <borndiag.prc> "#Procedure borndiag"
	#write <borndiag.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #ElseIf `BORNFLG' == 3[% 
@if eval .not. generate_ct_internal %]   
        repeat id UVSET?UV[UVNR]*UVSET1?UV[UVNR1] =0;
        repeat id UVSET?UV[UVNR]^2 =0;
        if (match(UVSET?UV[UVNR]) );
        else;
          id UVSET?NONUV[UVNR] = 0;
        endif;
        .sort;[%
@end @if %]        
	#Create <`OUTFILE'.txt>
        #write <`OUTFILE'.txt> "#Procedure ctdiag"
	#write <`OUTFILE'.txt> "Id ctdiag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == 4[% 
@if eval .not. generate_ct_internal %]   
        repeat id UVSET?UV[UVNR]*UVSET1?UV[UVNR1] =0;
        repeat id UVSET?UV[UVNR]^2 =0;
        if (match(UVSET?UV[UVNR]) );
        else;
          id UVSET?NONUV[UVNR] = 0;
        endif;
        .sort;[%
@end @if %]         
        #Create <`OUTFILE'.txt>
	#write <`OUTFILE'.txt> "Id ctdiag`DIAG'  = %e",diagram`DIAG'	
   #ElseIf `BORNFLG' == -3[% 
@if eval .not. generate_ct_internal %]   
        repeat id UVSET?UV[UVNR]*UVSET1?UV[UVNR1] =0;
        repeat id UVSET?UV[UVNR]^2 =0;
        if (match(UVSET?UV[UVNR]) );
        else;
          id UVSET?NONUV[UVNR] = 0;
        endif;
        .sort; [%
@end @if %]           
        #Append <ctdiag.prc>
	#write <ctdiag.prc> "Id ctdiag`DIAG'  = %e",diagram`DIAG'
        #write <ctdiag.prc> "#EndProcedure"
        #Call OptimizeCT()	
   #ElseIf `BORNFLG' == 5[% 
@if eval .not. generate_ct_internal %]   
        repeat id UVSET?UV[UVNR]*UVSET1?UV[UVNR1] =0;
        repeat id UVSET?UV[UVNR]^2 =0;
        if (match(UVSET?UV[UVNR]) );
        else;
          id UVSET?NONUV[UVNR] = 0;
        endif;
        .sort;[%
@end @if %]               
	#Create <ctdiag.prc>
        #write <ctdiag.prc> "#Procedure ctdiag"
	#write <ctdiag.prc> "Id ctdiag`DIAG'  = %e",diagram`DIAG'
        #write <ctdiag.prc> "#EndProcedure"
        #Call OptimizeCT()	
   #EndIf
#EndIf
.end[%
@case implicit %]
#If `LOOPS' == 1
   #Create <`OUTFILE'.txt>
   #Create <`OUTFILE'.dat>[%
@if helsum %]
   #Call WriteUnoptimized(0)[%
@else %]
   #Call  OptimizeCode(0)[%
@end @if %]
   #Close <`OUTFILE'.txt>
   #Close <`OUTFILE'.dat>
#Else
   #If `BORNFLG' == 1
   #Create <`OUTFILE'.txt>
        #write <`OUTFILE'.txt> "#Procedure borndiag"
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == 0
        #Create <`OUTFILE'.txt>
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == -1
        #Append <borndiag.prc>
	#write <borndiag.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #ElseIf `BORNFLG' == 2
	#Create <borndiag.prc>
        #write <borndiag.prc> "#Procedure borndiag"
	#write <borndiag.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #EndIf
#EndIf
.end[%
@case only off %]
# message 'FORM optimization implemented only with r2=explicit/implicit!!'
.end[%
@end @select %][%
@else %]

#If `LOOPS' == 1
   #Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
         Q[%
@select r2 @case implicit %],Qt2,eps[%
@end @select %])
#EndIf

.sort:5.9;

#If `LOOPS' == 1
   #$terms=termsin_(diagram`DIAG')[%
@select r2 @case explicit only %]+ termsin_(d`DIAG'R2)[%
@end @select%];
#Else
   #$terms=termsin_(diagram`DIAG');
#EndIf
#Define TERMS "`$terms'"
.sort:part 7;

#If `LOOPS' == 1[%
@select r2 @case explicit only %]
   #If "`R2PREFACTOR'" != "1"
      #Write <`OUTFILE'.abb> "rat2d`DIAG' = `R2PREFACTOR' *(%E);", d`DIAG'R2
   #Else
      #Write <`OUTFILE'.abb> "rat2d`DIAG' = %e", d`DIAG'R2
   #EndIf[%
@end @select %]
   #Close <`OUTFILE'.abb>
#EndIf

#If (`GROUP' == 0) && (`USETOPOLYNOMIAL')
   ToPolynomial;
.sort:part 8;
#EndIf

#Create <`OUTFILE'.dat>
#If (`GROUP' == 0) && (`USETOPOLYNOMIAL')
   #Write <`OUTFILE'.dat> "extrasymbols=%"
   #Do i=1,`EXTRASYMBOLS_'
      #Write <`OUTFILE'.dat> " `EXTRAPAT'`i'_%"
   #EndDo
   #Write <`OUTFILE'.dat> ""
#Else
   #Write <`OUTFILE'.dat> "extrasymbols="
#EndIf

#Write <`OUTFILE'.dat> "terms=`TERMS'"
#Write <`OUTFILE'.dat> "time=`time_'"
#Close <`OUTFILE'.dat>[%

@select r2 @case implicit explicit %]
#If `LOOPS' > 0
   Multiply epspow(0);
   Id epspow(0) * eps^sDUMMY2? = epspow(sDUMMY2);
#EndIf[%
@end @select %]
.sort:part 9.1;[%

@select r2
@case only %]
#If `LOOPS' == 0[%
@end @select %]
   #Create <`OUTFILE'.txt>
   #If `GROUP' == 0
      #If `TERMS' != 0
         #If `USETOPOLYNOMIAL' == "1"
            #Do x=1,`EXTRASYMBOLS_'
                #Write <`OUTFILE'.txt> "`EXTRAPAT'`x'_ = %`x'x;"
            #EndDo
         #EndIf
      #EndIf
   #EndIf

   #If `TERMS' > 0
      #Write <`OUTFILE'.txt> "d`DIAG' = %e", diagram`DIAG'
   #EndIf
   #Close <`OUTFILE'.txt>[%
@select r2
@case only %]
#EndIf[%
@end @select %]

#IfDef `FR5'
   #If `LOOPS' == 0
      #Create <`OUTFILE'-fr.txt>
      #Write <`OUTFILE'-fr.txt> "d`DIAG' = %e", diagram`DIAG'fr
      #Close <`OUTFILE'-fr.txt>
   #EndIf
#EndIf

#If (`GROUP' == 0) && (`USETOPOLYNOMIAL')
   FromPolynomial;
#EndIf
.sort:output;
Global diagram`DIAG'x = diagram`DIAG';
.store

*---#[ GENERATEDERIVATIVES:
#IfDef `GENERATEDERIVATIVES'
#Append <`OUTFILE'.abb>

Global diagram = diagram`DIAG'x;[%
@if extension qshift %][%
@else %]
   Id Q = p1;
   #Call shiftmomenta(`DIAG',1)
   Id fshift(0) = 0;
   Id fshift(?all) = 1;
   Id p1 = Q;
   #Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
         Q,qshift,[%
     @select r2 @case implicit explicit %],Qt2,eps,epspow[%
     @end @select %])[%
@end @if %]
.store:start derivatives;

   Local d0diagram = diagram;
#Do p=1,`RANK'
   Local d`p'diagram = <d(iv1)> *...* <d(iv`p')> * diagram;
#EndDo
ToTensor, Functions, Q, ptens;
Repeat;
   Id Once d(iDUMMY1?) * ptens(?indices) =
      fDUMMY1(iDUMMY1) * distrib_(1,1, fDUMMY2, ptens, ?indices);
   Id fDUMMY1(iDUMMY1?) * fDUMMY2(iDUMMY2?) = d_(iDUMMY1, iDUMMY2);
EndRepeat;
ToVector ptens, Q;
Id d(iDUMMY1?) = 0;
#IfDef `DERIVATIVESATZERO'
   Id Q = 0;
#EndIf
Id d_(iDUMMY1?,iDUMMY2?) = d(iDUMMY1,iDUMMY2);

Id vDUMMY1?(iDUMMY1?) = SUBSCRIPT(vDUMMY1, iDUMMY1);
.sort
#Do p=0,`RANK'
   #$d`p'terms = termsin_(d`p'diagram);
   #If `$d`p'terms' > 0
      #Write <`OUTFILE'd.txt> "d`p'diagram = %e", d`p'diagram
   #Else
      #Write <`OUTFILE'd.txt> "d`p'diagram = NULL*epspow(0);"
   #EndIf
#EndDo
#Close <`OUTFILE'.abb>
.store:end-of-derive;
#EndIf
*---#] GENERATEDERIVATIVES:
*---#[ GENERATENINJATRIPLE:
#IfDef `GENERATENINJATRIPLE'
Vectors vecA, vecB, vecC;
Symbol LaurentT, LaurentTi;

#Append <`OUTFILE'.abb>
Global nd3 = diagram`DIAG'x;[%
@if extension qshift %][%
@else %]
Id Q = p1;
#Call shiftmomenta(`DIAG',1)
Id fshift(0) = 0;
Id fshift(?all) = 1;
Id p1 = Q;[%
@end @if %]
Id Q = vecA + vecC * LaurentTi + vecB * LaurentT;

Id LaurentT * LaurentTi = 1;
Id vecB.vecB = 0;
Id vecC.vecC = 0;

#Define MINLaurentT "{{`LOOPSIZE'-3}-{`GLOOPSIZE'-`LOOPSIZE'}}"
*#If `RANK' > `LOOPSIZE'
#Define MAXLaurentT "`RANK'"
*#Else
*   #Define  MAXLaurentT "`LOOPSIZE'"
*#EndIf
  
#Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
      vecA,vecB,vecC,LaurentT,LaurentTi,qshift,[%
  @select r2 @case implicit explicit %],Qt2,eps,epspow[%
     @end @select %])
.sort
Multiply fDUMMY1(0);
Id fDUMMY1(sDUMMY1?) * LaurentT^sDUMMY2? = fDUMMY1(sDUMMY1+sDUMMY2);
Id fDUMMY1(sDUMMY1?) * LaurentTi^sDUMMY2? = fDUMMY1(sDUMMY1-sDUMMY2);
Brackets fDUMMY1;
.sort
Keep Brackets;
#Do pow=`MINLaurentT',`MAXLaurentT'
   #If `pow' < 0
      Local nd3M{-`pow'} = nd3[fDUMMY1(`pow')];
   #Else
      Local nd3P`pow' = nd3[fDUMMY1(`pow')];
   #EndIf
#EndDo
.sort
#Create <`OUTFILE'3.txt>
#Do pow=`MAXLaurentT',`MINLaurentT',-1
   #If `pow' < 0
      #$nd3M{-`pow'}terms = termsin_(nd3M{-`pow'});
      #If `$nd3M{-`pow'}terms' > 0
         #Write <`OUTFILE'3.txt> \
              "numerator_{`MAXLaurentT'-`pow'}=%e",nd3M{-`pow'}
      #Else
         #Write <`OUTFILE'3.txt> \
              "numerator_{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
      #EndIf
   #Else
      #$nd3P{`pow'}terms = termsin_(nd3P{`pow'});
      #If `$nd3P`pow'terms' > 0
         #Write <`OUTFILE'3.txt> \
              "numerator_{`MAXLaurentT'-`pow'}=%e",nd3P{`pow'}
      #Else
         #Write <`OUTFILE'3.txt> \
              "numerator_{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
      #EndIf
   #EndIf
#EndDo
#Close <`OUTFILE'3.txt>
.store
#EndIf
*---#] GENERATENINJATRIPLE:
*---#[ GENERATENINJADOUBLE:
#IfDef `GENERATENINJADOUBLE'
Vector vecA;
Symbols LaurentT, beta;

#Append <`OUTFILE'.abb>
Global nd2 = diagram`DIAG'x;[%
@if extension qshift %][%
@else %]
Id Q = p1;
#Call shiftmomenta(`DIAG',1)
Id fshift(0) = 0;
Id fshift(?all) = 1;
Id p1 = Q;[%
@end @if %]
Id Q = vecA * LaurentT;[%
@select r2 @case implicit %]
Id Qt2 = beta * LaurentT^2;[%
@end @select %]

#Define MINLaurentT "`LOOPSIZE'"
*#If `RANK' > `LOOPSIZE'
*#Define MAXLaurentT "`RANK'"
*#Else
#Define  MAXLaurentT "`LOOPSIZE'"
*#EndIf
  
#Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
      vecA,beta,LaurentT,qshift[%
  @select r2 @case implicit explicit %],Qt2,eps,epspow[%
     @end @select %])
.sort
Multiply fDUMMY1(0);
Id fDUMMY1(sDUMMY1?) * LaurentT^sDUMMY2? = fDUMMY1(sDUMMY1+sDUMMY2);
Brackets fDUMMY1;
.sort
Keep Brackets;
#Do pow=`MINLaurentT',`MAXLaurentT'
   Local nd2P`pow' = nd2[fDUMMY1(`pow')];
#EndDo
.sort
#Create <`OUTFILE'2.txt>
#Do pow=`MAXLaurentT',`MINLaurentT',-1
   #$nd2P`pow'terms = termsin_(nd2P`pow');
   #If `$nd2P`pow'terms' > 0
      #Write <`OUTFILE'2.txt> "numerator_{`MAXLaurentT'-`pow'}=%e", nd2P`pow'
   #Else
      #Write <`OUTFILE'2.txt> "numerator_{`MAXLaurentT'-`pow'}=NULL*epspow(0);"
   #EndIf
#EndDo
#Close <`OUTFILE'2.txt>
#EndIf
*---#] GENERATENINJADOUBLE:
.end[%
@end @if %]
