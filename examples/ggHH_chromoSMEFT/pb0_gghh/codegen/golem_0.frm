* vim: syntax=form:ts=3:sw=3:expandtab
*
* This version of golem_0.frm generates expressions for the numerator
* only.
*
#-
*on shortstatistics;
off statistics;
*on statistics;

* The reference vectors are determined by the global setting
* 'reference-vectors' in the configuration file.
* Changing them here might lead to inconsistent results.
#define REFk1 "k2"
#define REFk2 "k1"
#define REFk3 "k2"
#define REFk4 "k2"
#Define DRED "defined"

#Define EXTRAPAT "EXSYM"
#Define USETOPOLYNOMIAL "0"




#If `LOOPS' == 1
   #Define abb`DIAG' "0"
   Autodeclare Symbol Qsp;
   #Include- abbreviate.hh
   Symbol CC, R2;
#Else
   #Include- optimizeborn_0.hh
#EndIf

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
Symbol Nfrat;


#If `USETOPOLYNOMIAL'
   ExtraSymbols,underscore,`EXTRAPAT';
#EndIf

#include- color.hh
.global

#include- diagrams-`LOOPS'.hh #global
#include- model.hh
#If `LOOPS' == 0
#include- diagrams-`LOOPS'.hh #diagram`DIAG'
#Else
F diag1,...,diag`DIAGRAMCOUNT';
#include- diagsum.frm #diag`DIAG'
#EndIf
#If `LOOPS' == 1
   #include- r2.hh
   #include- r2integrals.hh
#EndIf

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

.sort

Id mdlGC9 = mdlGC9SM + mdlGC9DIM6*mdlLambdam2;
Id mdlGC31 = mdlGC31DIM6*mdlLambdam2;
Id mdlGC32 = mdlGC32DIM6*mdlLambdam2;
Id mdlGC33 = mdlGC33DIM6*mdlLambdam2;
Id mdlGC34 = mdlGC34DIM6*mdlLambdam2;
Id mdlGC35 = mdlGC35DIM6*mdlLambdam2;
Id mdlGC36 = mdlGC36DIM6*mdlLambdam2;
Id mdlGC39 = mdlGC39SM + mdlGC39DIM6*mdlLambdam2;
Id mdlGC40 = mdlGC40DIM6*mdlLambdam2;
Id mdlGC41 = mdlGC41SM + mdlGC41DIM6*mdlLambdam2;
.sort

Id mdlLambdam2 = 0;



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

Id SCREEN(sDUMMY1?) = sDUMMY1;
Id inplorentz(2, ivL2?, k1, 0) *
   inp(field1?, k1, sDUMMY1?{-1,1}, vDUMMY1?) = e1(ivL2);
Id inplorentz(2, ivL2?, k2, 0) *
   inp(field1?, k2, sDUMMY1?{-1,1}, vDUMMY1?) = e2(ivL2);
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
* We use already d4 and Sm4 although this is an abuse of
* notation here since the dimension splitting happens only
* later, after the call to tHooftAlgebra.
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
    Id d4(p1,p1) = d4(p1,p1) - Qt2;
    Id Sm4(p1) = Sm4(p1) + SmQt;
    Repeat;
        Repeat Id Sm4(p1)*Sm4(p1) = d4(p1,p1);

            Id SmQt * Sm4(iDUMMY1?) = - Sm4(iDUMMY1) * SmQt;
    Endrepeat;
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

#If `LOOPS' == 1
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
   UnHide diagram`DIAG';
#EndIf


#if `LOOPS' == 1
   Id p1 = Q;
   Argument Spab, Spaa, Spbb, Spba;
      Id p1 = Q;
   EndArgument;
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
   #Create <`OUTFILE'.txt>
   #Create <`OUTFILE'.dat>
   #Call  OptimizeCode(`R2PREFACTOR')
   #Close <`OUTFILE'.txt>
   #Close <`OUTFILE'.dat>
#Else
   #If `BORNFLG' == 1
   #Create <`OUTFILE'.txt>
        #write <`OUTFILE'.txt> "#Procedure borndiag0"
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == 0
        #Create <`OUTFILE'.txt>
	#write <`OUTFILE'.txt> "Id diag`DIAG'  = %e",diagram`DIAG'
   #ElseIf `BORNFLG' == -1
        #Append <borndiag0.prc>
	#write <borndiag0.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag0.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #ElseIf `BORNFLG' == 2
	#Create <borndiag0.prc>
        #write <borndiag0.prc> "#Procedure borndiag0"
	#write <borndiag0.prc> "Id diag`DIAG'  = %e",diagram`DIAG'
        #write <borndiag0.prc> "#EndProcedure"
        #Call OptimizeBorn()
   #EndIf
#EndIf
.end
