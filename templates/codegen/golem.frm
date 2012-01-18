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
@if extension fr5 %]
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

#If `LOOPS' == 1
   #Include- abbreviate.hh
   #Create <`OUTFILE'.abb>
#EndIf

#include- spinney.hh
#redefine SPCANCEL "0"

#include- symbols.hh
* #include- fermion_flow.hh

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

#If `USETOPOLYNOMIAL'
   ExtraSymbols,underscore,`EXTRAPAT';
#EndIf

#include- color.hh
.global

#include- diagrams-`LOOPS'.hh #global
#include- model.hh
#include- process.hh
#include- diagrams-`LOOPS'.hh #diagram`DIAG'[%
@select r2 default=implicit
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
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = + deltaOS * sDUMMY1 / 4 *
       (
      + (6*p1.vDUMMY1 + 3*(vDUMMY1.vDUMMY1-sDUMMY1*(sDUMMY1+i_*sDUMMY2)))*
        inv(sDUMMY1*(sDUMMY1+i_*sDUMMY2))
      + 3*(4-2*deltaHV)*Qt2*inv(vDUMMY1.vDUMMY1-3*sDUMMY1*(sDUMMY1+i_*sDUMMY2))
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);
  Id fDUMMY1(ZERO, p1, vDUMMY2?, p1, sDUMMY1?, sDUMMY2?,
        iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) = - deltaOS * sDUMMY1 / 4 *
       (
      + (6*p1.vDUMMY2 + 3*(vDUMMY2.vDUMMY2+sDUMMY1*(sDUMMY1+i_*sDUMMY2)))*
        inv(sDUMMY1*(sDUMMY1+i_*sDUMMY2))
      - 3*(4-2*deltaHV)*Qt2*inv(vDUMMY2.vDUMMY2-3*sDUMMY1*(sDUMMY1+i_*sDUMMY2))
     ) * NCContainer(1, iDUMMY2, iDUMMY1) * d(iDUMMY3, iDUMMY4);

   #IfDef `DRED'
      Id deltaHV = 0;
   #Else
      Id deltaHV = -1/2;
   #EndIf
   .sort:MQSE 1.1;
#EndIf

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

*Brackets SplitLorentzIndex;
.sort:part 0.9.0;
*Keep Brackets;

Repeat Id SplitLorentzIndex(iDUMMY1?, iDUMMY2?, ?tail1) *
          SplitLorentzIndex(iDUMMY3?, iDUMMY4?, ?tail2) =
   SplitLorentzIndex(iDUMMY1, ?tail1) *
   SplitLorentzIndex(iDUMMY3, ?tail2) * d_(iDUMMY2, iDUMMY4);
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

Id SCREEN(sDUMMY1?) = sDUMMY1;
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
*---#] Process Legs:

.sort:part 1;

Multiply replace_(Sqrt2, sqrt2);
Id sqrt2^2  = 2;
Id sqrt2^-2 = 1/2;

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

   #If `LOOPSIZE' > 4
      Id Qt2 = 0;
   #ElseIf `LOOPSIZE' == 4
      ToTensor, Functions, p1, ptens;
      If(count(ptens,1)==0) Multiply ptens;
* For boxes we need to consider integrals of type mu2*ptens(mu,nu) and
* mu2^2.
      Id Only ptens * Qt2 = 0;
      Id ptens(iDUMMY1?) * Qt2 = 0;

      ToVector, ptens, p1;
   #EndIf
#Else
   Id dEps(iDUMMY1?, iDUMMY1?) = 0;
#EndIf

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
@select r2 default=implicit
@case implicit %]
* Implicit reduction of R2 term:
* All terms in the numerator which come with a \epsilon or \mu^2
* are reduced with the reduction library (Samurai/Golem95/PJFry etc.)
.sort 5.3;[%
@case explicit %]
* Explicit reduction of R2 term:
* All terms in the numerator which come with a \epsilon or \mu^2
* are replaced by explicit expressions.
   Brackets eps, Qt2;
.sort 5.3;
   Local d`DIAG'R2 = 
      + diagram`DIAG'[eps] * fDUMMY1(eps)
      + diagram`DIAG'[Qt2] * fDUMMY1(Qt2)
      + diagram`DIAG'[Qt2^2] * fDUMMY1(Qt2^2);
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
      + diagram`DIAG'[Qt2^2] * fDUMMY1(Qt2^2);
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
@if extension qshift %]
   #Call shiftmomenta(`DIAG')
   Argument Spab, Spaa, Spbb, Spba;
      #Call shiftmomenta(`DIAG')
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

Id Spa2(vDUMMY1?{`EXTERNAL'}, vDUMMY2?{`EXTERNAL'}) *
   Spb2(vDUMMY2?, vDUMMY1?) = 2 * fDUMMY1(vDUMMY1.vDUMMY2);

Id vDUMMY1?{`EXTERNAL'}.vDUMMY2?{`EXTERNAL'} = fDUMMY1(vDUMMY1.vDUMMY2);

Id SpDenominator(Spa2(vDUMMY1?{k1,...,k`LEGS'}, vDUMMY2?{k1,...,k`LEGS'})) *
   SpDenominator(Spb2(vDUMMY1?, vDUMMY2?)) = -1/2 * inv(vDUMMY1.vDUMMY2);

Argument inv, fDUMMY1;
#call kinematics
EndArgument;

Id fDUMMY1(sDUMMY1?) * inv(sDUMMY1?) = 1;
Id fDUMMY1(sDUMMY1?) = sDUMMY1;
Id inv(sDUMMY1?symbol_) = (1/sDUMMY1);

#call kinematics
Id vDUMMY1?{`LIGHTLIKE'}.vDUMMY2?{`LIGHTLIKE'} =
   1/2 * Spa2(vDUMMY1, vDUMMY2) * Spb2(vDUMMY2, vDUMMY1);

#call spsymbols

Id SpDenominator(sDUMMY1?) = (1/sDUMMY1);
Id inv(sDUMMY1?) = (1/sDUMMY1);

.sort:5.2;

#If `LOOPS' == 1
   #Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
         Q[%
@select r2 default=implicit @case implicit %],Qt2,eps[%
@end @select %])
#EndIf

.sort:5.9;

#If `LOOPS' == 1
   #$terms=termsin_(diagram`DIAG')[%
@select r2 default=implicit @case explicit only %]+ termsin_(d`DIAG'R2)[%
@end @select%];
#Else
   #$terms=termsin_(diagram`DIAG');
#EndIf
#Define TERMS "`$terms'"
.sort:part 7;

#If `LOOPS' == 1[%
@select r2 default=implicit @case explicit only %]
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

@select r2 default=implicit @case implicit %]
#If `LOOPS' > 0
   Multiply epspow(0);
   Id epspow(0) * eps^sDUMMY2? = epspow(sDUMMY2);
#EndIf[%
@end @select %]
.sort:part 9.1;[%

@select r2 default=implicit
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
@select r2 default=implicit
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

#IfNDef `GENERATEDERIVATIVES'
.end:output;
#Else
   #If (`GROUP' == 0) && (`USETOPOLYNOMIAL')
      FromPolynomial;
   #EndIf
.sort:output;
#Append <`OUTFILE'.abb>
#EndIf
Global diagram = diagram`DIAG';[%
@if extension qshift %][%
@else %]
   Id Q = p1;
   #Call shiftmomenta(`DIAG')
   Id p1 = Q;
   #Call ExtractAbbreviationsBracket(`OUTFILE'.abb,abb`DIAG'n,\
         Q[%
     @select r2 default=implicit @case implicit %],Qt2,eps,epspow[%
     @end @select %])[%
@end @if %]
.store:start derivatives;

   Local d0diagram = diagram;
#Do p=1,`LOOPSIZE'
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
#Do p=0,`LOOPSIZE'
   #$d`p'terms = termsin_(d`p'diagram);
   #If `$d`p'terms' > 0
      #Write <`OUTFILE'd.txt> "d`p'diagram = %e", d`p'diagram
   #Else
      #Write <`OUTFILE'd.txt> "d`p'diagram = NULL*epspow(0);"
   #EndIf
#EndDo
#Close <`OUTFILE'.abb>
.end:output derivatives;
