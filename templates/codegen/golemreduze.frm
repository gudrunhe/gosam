* vim: syntax=form:ts=3:sw=3:expandtab
#-
Format 255; * Number of characters per line

#If `LOOPS' >= 1
   #Define abb`DIAG' "0"
   #Include- abbreviate.hh
#Else
   #Include- optimizeborn.hh
#EndIf

#Include- reduze.hh
#Include- spinney.hh
#redefine SPCANCEL "0"

#Include- symbols.hh

#ifndef `USEVERTEXPROC'
   #Include- vertices.hh
#endif

CFunctions Spab3, Spba3;
CFunction epspow;
AutoDeclare Vectors spva;

#Include- color.hh
.global

#Include- diagrams-`LOOPS'.hh #global
#Include- model.hh
#If `LOOPS' == 0
   #Include- diagrams-`LOOPS'.hh #diagram`DIAG'
#Else
   F diag1,...,diag`DIAGRAMCOUNT';
   #Include- diagrams-`LOOPS'.hh #diagram`DIAG'
#EndIf

#ifdef `ISDUMMY'
   Multiply 0;
#endif

Id QGRAFSIGN(sDUMMY1?) = sDUMMY1;

#call zeroes
#call ScreenExternalReduze

#Include- reduzeprojectors.hh

#Call enforceconservation
#Call DiaMatchTagReduze
#Call ShiftReduze
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

#Include- propagators.hh

.sort:part 0.9.0;
*---#] Process Propagators:

#call coloralgebra(0)

* sj - collect colour structures, can anything else appear? HOW TO GET ALL COLOUR STRUCTURES HERE
AB TR,NC,NA,c1;
.sort:abcolor1;

Collect COLORFACTOR;
Normalize COLORFACTOR;
.sort:abcolor2;

*---#[ Process Legs:

#Include- legs.hh

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

Id d(iv1L?, iv2L?) = d_(iv1L, iv2L);

* use ProjMinus + ProjPlus = 1
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

Id Projector(sDUMMY1?) = sDUMMY1;

#Call TraceReduze
#Call kinematics
#Call SPToPropReduze
#Call MapReduze

* process 1PR propagators
Id inv(k1?, m?, sDUMMY1?) = inv(k1.k1 - m^2 + i_ * m * sDUMMY1);
Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id inv(0, m?) = - inv(m^2);
Id inv(0, m?, sDUMMY1?) = + inv(-m^2 + i_ * m * sDUMMY1);

* sj - added - MAY WANT TO CALL THIS FUNCTION DEN!
Denominators Den;
Id inv(?tail) = Den(?tail);
Id ProjDen(?tail) = Den(?tail);
Argument Den;
   Id ZERO = 0;
   #call kinematics
EndArgument;
.sort

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

* prevent some prefactors entering prf
Id i_ = PREFACTOR(i_);
Id dimS = PREFACTOR(dimS);
Id dimD = PREFACTOR(dimD);

* post processing
Id sDUMMY1?^(-1) = Den(sDUMMY1);
Denominators Den;
FactArg Den;
ChainOut Den;
.sort
Id Den(sDUMMY1?number_) = 1/sDUMMY1;
Id sDUMMY1?*Den(sDUMMY1?) = 1;
.sort:post;

Multiply prf(1,1);
Repeat Id Den(sDUMMY1?)*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY2,sDUMMY1*sDUMMY3);
Repeat Id sDUMMY1?*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY1*sDUMMY2,sDUMMY3);
.sort:feed prf;
PolyRatFun prf;
.sort:prf;

*
* Write amplitude
*
#Create <`OUTFILE'.log>
.sort

* sj - useful for double Higgs (pulls out overall factors)
Bracket inp,SCREEN,c1,PREFACTOR,Sector,inv,Tag,gHHH,gHT,e,i_,CrossingInvariants,Crossing,COLORFACTOR;
print+s;
.sort

Keep Brackets;
#write <`OUTFILE'.log> "L d`DIAG'h0l`LOOPS' = %e", diagram`DIAG'
.end
