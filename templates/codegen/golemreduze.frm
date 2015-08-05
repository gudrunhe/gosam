* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

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

#Include- projectors.hh

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

***** WARNING THE FOLLOWING CODE DOES NOT WORK IN GENERAL *****
* sj - this will not always eliminate ProjPlus, need to handle this case also
* use ProjMinus + ProjPlus = 1
Id NCContainer(ProjMinus,?tail) = NCContainer(1,?tail) - NCContainer(ProjPlus,?tail);
.sort
***** END WARNING *****

*---#[ Process Propagators:
* If the mass is zero the width becomes irrelevant:
Id proplorentz(sDUMMY1?, vDUMMY1?, 0, sDUMMY3?, ?tail) =
   proplorentz(sDUMMY1, vDUMMY1, 0, 0, ?tail);

***** WARNING THE FOLLOWING CODE DOES NOT WORK IN GENERAL *****
#IfDef `MASSCT'
** Mass renormalization

* Heavy Fermions, See B9 of  1103.0621 <------ ERROR - Assume only 1 CT insertion possible
Repeat;
Id Once proplorentz(1,k1?,m?,sDUMMY1?,sDUMMY2?,iv1?,iv2?) =
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iv2)
- i_*dZmp*deltaZm(1,m)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iDUMMY1)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iDUMMY1,iv2);
sum iDUMMY1;
EndRepeat;
.sort
Id proplorentzct(?tail) = proplorentz(?tail);
.sort

* Yukawa Couplings <------ ERROR - Only gHT, Assume only 1 CT insertion possible
FactArg PREFACTOR;
ChainOut PREFACTOR;
Id PREFACTOR(gHT) = gHT;
Id gHT = (1+dZmp*deltaZm(1,mT)*Den(mT))*gHT;
Id gHT = PREFACTOR(gHT);
.sort

* Throw non-mct terms, drop power counting
if ( count(dZmp,1) == 0 ) Discard;
.sort
Id dZmp =1;
.sort

#EndIf
***** END WARNING *****

#Include- propagators.hh

.sort:part 0.9.0;
*---#] Process Propagators:

#call coloralgebra(0)

AB TR,NC,NA,[%@for repeat num_colors shift=1%]c[% $_ %][%@if is_last%];[%@else%],[%@end @if%][%@end @for%]
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
Id dimS = Dim(dimS);
Id dimD = PREFACTOR(dimD);

* Simplify coefficients
Repeat Id sDUMMY1? = prf(sDUMMY1,1);
Repeat Id sDUMMY1?^(-1) = prf(1,sDUMMY1);
Repeat Id Dim(sDUMMY1?) = prf(sDUMMY1,1);
Repeat Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id Den(sDUMMY1?) = prf(1,sDUMMY1);
.sort:feed prf;
PolyRatFun prf;
.sort:prf;

* post processing
Repeat Id PREFACTOR(sDUMMY1?)*PREFACTOR(sDUMMY2?) = PREFACTOR(sDUMMY1*sDUMMY2);
Normalize COLORFACTOR;
Normalize PREFACTOR;
Normalize Dim;

*
* Write amplitude
*
Bracket ProjLabel,PREFACTOR,COLORFACTOR;
print+s;
.sort
#Write <`OUTFILE'.txt> "L d`DIAG'l`LOOPS' = %e", diagram`DIAG'
.end

