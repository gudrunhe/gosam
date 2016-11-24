* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;

#Include- symbols.hh
#Include- reduze.hh
#Include- secdec.hh
#Include- projectors.hh
#Include- spinney.hh

* Create list of ProjLabel1,...,ProjLabel`NUMPROJ'
#Define ProjectorLabels ""
#Do label = 1, `NUMPROJ'
#Redefine ProjectorLabels "`ProjectorLabels',ProjLabel`label'"
#EndDo
.sort

* disable spinor flipping rules in spinney.hh (RemoveNCContainer)
* does not implement arXiv:1008.0803v1 Eq(21), discussion at the end of section 3.5.2
#Define NOSPFLIP
#Redefine SPCANCEL "0"

#ifndef `USEVERTEXPROC'
   #Include- vertices.hh
#endif

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

#Call ApplyProjectors
#Call enforceconservation
#Call DiaMatchTagReduze
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

#If `MASSCT' == 1


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


#ElseIf `MASSCT' == 2

** Mass renormalization
* First, two insertions on the same fermion line, a two-loop insertion 
* plus two one-loop insertions

Repeat;
Id Once proplorentz(1,k1?,m?,sDUMMY1?,sDUMMY2?,iv1?,iv2?) =
proplorentzct1(1,k1,m,sDUMMY1,sDUMMY2,iv1,iv2)
- i_*dZmp2*deltaZm(2,m)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iDUMMY1)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iDUMMY1,iv2)
-dZmp2*deltaZm(1,m)^2*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iDUMMY1)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iDUMMY1,iDUMMY2)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iDUMMY2,iv2)
;
sum iDUMMY1, iDUMMY2;
EndRepeat;
.sort

* Second , two insertion on different lines
Repeat;
Id proplorentzct1(1,k1?,m?,sDUMMY1?,sDUMMY2?,iv1?,iv2?) =
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iv2)
- i_*dZmp*deltaZm(1,m)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iv1,iDUMMY1)*
proplorentzct(1,k1,m,sDUMMY1,sDUMMY2,iDUMMY1,iv2);
EndRepeat;
.sort


Id proplorentzct(?tail) = proplorentz(?tail);
.sort



* Yukawa Coupling
FactArg PREFACTOR;
ChainOut PREFACTOR;
Id PREFACTOR(gHT) = gHT;
Id gHT = (1+dZmp*deltaZm(1,mT)*Den(mT)+dZmp2*deltaZm(2,mT)*Den(mT))*gHT;
Id gHT = PREFACTOR(gHT);
.sort




* Same as above, throw away non-mct terms
if (count(dZmp,1) != 2 || count(dZmp2,1) == 0) Discard;
.sort
Id dZmp2 =1;
Id dZmp =1;
.sort



#EndIf



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

Id inp(?all) = 1;
Id out(?all) = 1;
Id ZERO = 0;
Id PREFACTOR(sDUMMY1?)^sDUMMY2 = PREFACTOR(sDUMMY1^sDUMMY2);
Repeat Id PREFACTOR(sDUMMY1?)*PREFACTOR(sDUMMY2?) = PREFACTOR(sDUMMY1*sDUMMY2);
Normalize PREFACTOR;
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

* compute traces, match to integral families
#Call TraceReduze
#Call kinematics
#Call SPToPropReduze
*#Call enforceconservation
#Call kinematics
#Call MapReduze

* process 1PR propagators
Id inv(k1?, m?, sDUMMY1?) = inv(k1.k1 - m^2 + i_ * m * sDUMMY1);
Id inv(k1?, m?) = inv(k1.k1 - m^2);
Id inv(0, m?) = - inv(m^2);
Id inv(0, m?, sDUMMY1?) = + inv(-m^2 + i_ * m * sDUMMY1);
Id inv(?tail) = Den(?tail);
.sort

#Call ToIntReduze

#call zeroes
Id csqrt(0) = 0;
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
Normalize Dim, DenDim;
.sort

#Call ExpandProjectors
#Call kinematics
Argument ProjNum,ProjDen,Den;
  Id ZERO = 0;
  #Call kinematics;
EndArgument;
.sort

* Simplify coefficients
#Call FeedPolyRatFun(`ProjectorLabels')
PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:prf;

*
* Write amplitude
*
Bracket `ProjectorLabels',PREFACTOR,COLORFACTOR;
*print+s;
.sort
#Write <`OUTFILE'.txt> "L d`DIAG'l`LOOPS' = %e", diagram`DIAG'
.end

