* vim: syntax=form:ts=3:sw=3:expandtab
*
* This version of golem.frm generates expressions for the numerator
* only.
*
#-
*on shortstatistics;
off statistics;
*on statistics;

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

Id QGRAFSIGN(sDUMMY1?) = 1;

#call zeroes

* sj - tag diagrams with DiaMatch
#Call DiaMatchTagReduze
* sj - shift momenta onto reduze topologies
#Call ShiftReduze

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

#call coloralgebra(0)

*---#[ Process Legs:

* sj - screen all external spinors/vectors(polarisations)/tensors
#call ScreenExternalReduze

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

* sj - use ProjMinus + ProjPlus = 1
* useful for double Higgs (eliminates explicit Gamma5)
id NCContainer(ProjMinus,?tail) = NCContainer(1,?tail) - NCContainer(ProjPlus,?tail); 
*.sort

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

* sj - include projectors
*#include- reduzeprojectors.hh
*Multiply d_(iv2r3L2,iv3r3L2);
id SCREEN(inplorentz(2,iDUMMY1?,k1,0))*
   SCREEN(inplorentz(2,iDUMMY2?,k2,0))=
   SCREEN(inplorentz(2,iDUMMY1,k1,0))*
   SCREEN(inplorentz(2,iDUMMY2,k2,0))*
   d_(iDUMMY1,iDUMMY2);

id d(iv1L?, iv2L?) = d_(iv1L, iv2L);

* sj - insert kinematics
#Call kinematics

*B inp,SCREEN,c1,PREFACTOR,Sector,inv,Tag,gHHH,gHT,e,i_;
*print+s;
*.end

*sj - eliminate k4
Argument inv;
   #Call conservation()
EndArgument;
   #Call conservation()

*sj - apply crossing symmetries
#Call CrossingReduze

* sj - map scalar products to propagators
#Call SPToPropReduze

* sj - map propagators onto reduze ordered propagators
#Call MapReduze

* sj - BOF copied from above, process 1PR propagators
Id inv(k1?, m?, sDUMMY1?) = inv(k1.k1 - m^2 + i_ * m * sDUMMY1);
Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id inv(0, m?) = - inv(m^2);
Id inv(0, m?, sDUMMY1?) = + inv(-m^2 + i_ * m * sDUMMY1);

Argument inv;
   Id ZERO = 0;
   #call kinematics
EndArgument;
Id inv(sDUMMY1?symbol_) = 1/sDUMMY1;
* sj - EOF copied from above

#Call ToIntReduze

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

* sj - WARNING, WE MUST BE CAREFUL WHAT WE MEAN WITH THIS
#if `LOOPS' == 1
* Discrepancy between loop-integral libraries' convention 1/(i\pi^(n/2))
* and 1/(2\pi)^n leaving out the pre-factors as described
* in the manual.
   Multiply PREFACTOR(i_/2);
#endif

Repeat Id PREFACTOR(sDUMMY1?) * PREFACTOR(sDUMMY2?) =
   PREFACTOR(sDUMMY1 * sDUMMY2);

Id PREFACTOR(sDUMMY1?) = sDUMMY1;

Id Sector(?head)*ReduzeInt(?tail)=ReduzeInt(?head,?tail);

#Create <`OUTFILE'.txt>
#Create <`OUTFILE'Ints.txt>
.sort

* sj - useful for double Higgs (pulls out overall factors)
Bracket inp,SCREEN,c1,PREFACTOR,Sector,inv,Tag,gHHH,gHT,e,i_,CrossingInvariants,Crossing;
print+s;
.sort

Keep Brackets;
#write <`OUTFILE'.txt> "%e", diagram`DIAG'
.sort

B ReduzeInt;
.sort

Collect fDUMMY1;
Id fDUMMY1(?head)=1;
DropCoefficient;
.sort

#write <`OUTFILE'Ints.txt> "%e", diagram`DIAG'
print+s;
.end
