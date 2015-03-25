* vim: syntax=form:ts=3:sw=3:expandtab
*
* This version of golem.frm generates expressions for the numerator
* only.
*
#-
*on shortstatistics;
*off statistics;
*on statistics;
Format 255; * Number of characters per line

* sj - special header for using reduze
#include- reduze.hh

#If `LOOPS' >= 1
   #Define abb`DIAG' "0"
   #Include- abbreviate.hh
#Else
   #Include- optimizeborn.hh
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

#include- color.hh
.global

#include- diagrams-`LOOPS'.hh #global
#include- model.hh
#If `LOOPS' == 0
#include- diagrams-`LOOPS'.hh #diagram`DIAG'
#Else
F diag1,...,diag`DIAGRAMCOUNT';
#include- diagrams-`LOOPS'.hh #diagram`DIAG'
#EndIf

#ifdef `ISDUMMY'
   Multiply 0;
#endif

Id QGRAFSIGN(sDUMMY1?) = sDUMMY1;

#call zeroes

* sj - screen all external spinors/vectors(polarisations)/tensors
#call ScreenExternalReduze

* sj - include projectors
* note that the way we handle projectors is not ideal
* firstly, the momentum constraint may break this is one of the momenta are eliminated
* secondly, crossing may break this
#include- reduzeprojectors.hh

Id SCREEN(sDUMMY1?) = 1;

* sj - eliminate an external momentum
#Call enforceconservation

* sj - tag diagrams with DiaMatch
#Call DiaMatchTagReduze

* sj - shift momenta onto reduze topologies
#Call ShiftReduze

*sj - apply crossing symmetries
#Call CrossReduze
#Call CrossMomentaReduze

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

*---#[ Process Propagators:
* If the mass is zero the width becomes irrelevant:
Id proplorentz(sDUMMY1?, vDUMMY1?, 0, sDUMMY3?, ?tail) =
   proplorentz(sDUMMY1, vDUMMY1, 0, 0, ?tail);

#include- propagators.hh

.sort:part 0.9.0;
*---#] Process Propagators:

* sj - IS THIS ALL THAT CAN APPEAR HERE? CAN PROPCOLOR APPEAR?
*B inpcolor, outcolor, T, f, delta, dcolor, dcolor8, propcolor;
*.sort
*Collect SCREEN;
*.sort

#call coloralgebra(0)

* sj - collect colour structures, can anything else appear? HOW TO GET ALL COLOUR STRUCTURES HERE
AB TR,NC,NA,c1;
.sort:abcolor1;

Collect COLORFACTOR;
Normalize COLORFACTOR;
.sort:abcolor2;

* sj - unscreen non-colour objects
*Id SCREEN(sDUMMY1?) = sDUMMY1;

*---#[ Process Legs:

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

*repeat id d(iv1L?, iv2L?) * d(iv2L?, iv3L?) = d(iv1L, iv3L);
Repeat Id d(iv1L?, iv2L?) = d_(iv1L, iv2L);

* sj - use ProjMinus + ProjPlus = 1
* useful for double Higgs (eliminates explicit Gamma5)
Id NCContainer(ProjMinus,?tail) = NCContainer(1,?tail) - NCContainer(ProjPlus,?tail);
.sort

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

* sj - compute trace
#Call TraceReduze

* sj - insert kinematics
#Call kinematics

*B inp,SCREEN,c1,PREFACTOR,Sector,inv,Tag,gHHH,gHT,e,i_;
*print+s;
*.end

* sj - map scalar products to propagators
#Call SPToPropReduze

* sj - map propagators onto reduze ordered propagators
#Call MapReduze

* sj - BOF copied from above, process 1PR propagators
Id inv(k1?, m?, sDUMMY1?) = inv(k1.k1 - m^2 + i_ * m * sDUMMY1);
Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id inv(0, m?) = - inv(m^2);
Id inv(0, m?, sDUMMY1?) = + inv(-m^2 + i_ * m * sDUMMY1);

* sj - added - MAY WANT TO CALL THIS FUNCTION DEN!
Denominators inv;
Id ProjDen(?tail) = inv(?tail);
Argument inv;
   Id ZERO = 0;
   #call kinematics
EndArgument;
.sort
* sj - added end

#Call ToIntReduze

#Call CrossInvariantsReduze

Id inp(?all) = 1;
Id out(?all) = 1;

Id ZERO = 0;

#call zeroes
Id csqrt(0) = 0;
*---#] Process Legs:

Multiply replace_(Sqrt2, sqrt2);
Id sqrt2^2  = 2;
Id sqrt2^-2 = 1/2;

Multiply replace_(Sqrt3, sqrt3);
Id sqrt3^2  = 3;
Id sqrt3^-2 = 1/3;

Id csqrt(sDUMMY1?^2) = sDUMMY1;

* sj - to prevent entering prf
Id i_ = PREFACTOR(i_);
Id dimS = PREFACTOR(dimS);

* Post Processing
Id sDUMMY1?^(-1) = inv(sDUMMY1);
Denominators inv;
FactArg inv;
ChainOut inv;
.sort
Id inv(sDUMMY1?number_) = 1/sDUMMY1;
Id sDUMMY1?*inv(sDUMMY1?) = 1;
.sort:post;

Multiply prf(1,1);
Repeat Id inv(sDUMMY1?)*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY2,sDUMMY1*sDUMMY3);
Repeat Id sDUMMY1?*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY1*sDUMMY2,sDUMMY3);
.sort:feed prf;
PolyRatFun prf;
.sort:prf;

* sj - WARNING, WE MUST BE CAREFUL WHAT WE MEAN WITH THIS
*#if `LOOPS' == 1
* Discrepancy between loop-integral libraries' convention 1/(i\pi^(n/2))
* and 1/(2\pi)^n leaving out the pre-factors as described
* in the manual.
*   Multiply PREFACTOR(i_/2);
*#endif

*Repeat Id PREFACTOR(sDUMMY1?) * PREFACTOR(sDUMMY2?) = 
*           PREFACTOR(sDUMMY1 * sDUMMY2);

Id PREFACTOR(sDUMMY1?) = sDUMMY1;

*
* Write amplitude
*

#Create <`OUTFILE'.txt>
.sort

* sj - useful for double Higgs (pulls out overall factors)
Bracket inp,SCREEN,c1,PREFACTOR,Sector,inv,Tag,gHHH,gHT,e,i_,CrossingInvariants,Crossing,COLORFACTOR;
print+s;
.sort

Keep Brackets;
#write <`OUTFILE'.txt> "L d`DIAG'h0l`LOOPS' = %e", diagram`DIAG'
.sort

*
* Write list of integrals
*

*#Create <`OUTFILE'Ints.txt>
*.sort

*B ReduzeInt;
*.sort

*Collect fDUMMY1;
*Id fDUMMY1(?head)=1;
*DropCoefficient;
*.sort

*#write <`OUTFILE'Ints.txt> "%e", diagram`DIAG'
*print+s;
.end
