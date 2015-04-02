*on shortstatistics;
*off statistics;

Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Process integralfamilies;
G integralfamilies =
#Do i = `FIRST', `LAST'
   + DiaMatch(`i')
#EndDo
;

#Call ShiftReduze
#Call CrossReduze
#Call MapReduze
#Call CrossMomentaReduze
#Call CrossInvariantsReduze

#Call ToPropListSecDec
#Call MomListSecDec
#Call ExternalMomentaSecDec

DropCoefficient;
.sort

DropCoefficient;
print+s;
.sort:integralfamilies;
.end

Drop integralfamilies;

* Process sum
* Load GoSam result
#Do i = `FIRST', `LAST'
#include- d`i'h0l`LOOPS'.txt;
#EndDo

Id Sector(?tail) = 1;
Id Tag(?tail) = 1;
.sort:drop;

G sum =
#Do i = `FIRST', `LAST'
   + d`i'h0l`LOOPS'
#EndDo
;
.sort:sum;

Drop;
NDrop sum;
.sort

B INT;
.sort:bracket;

Collect SCREEN;
.sort:collect;

#include- reduzereduction-`LOOPS'.hh
.sort:reduce;

*#define LISTINTEGRALS "1"
*
* Write list of integrals
*
#ifdef `LISTINTEGRALS'
   Id SCREEN(?head)=1;
   .sort:drop screen;
   B INT;
   .sort:bracket2;
   Collect SCREEN;
   .sort:collect2;
   Id SCREEN(?head)=1;
   .sort:drop screen2;
   DropCoefficient;
   #Create <`OUTFILE'integrals.txt>
   #Write <`OUTFILE'integrals.txt> "%e", sum
   print+s;
   .end
#endif

Id SCREEN(sDUMMY1?) = sDUMMY1;

#call ExpandDim()
Repeat Id Den(sDUMMY1?)*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY2,sDUMMY1*sDUMMY3);
Repeat Id sDUMMY1?!{epsS,}*prf(sDUMMY2?,sDUMMY3?) = prf(sDUMMY1*sDUMMY2,sDUMMY3);
.sort:feed prf;
PolyRatFun prf;
.sort:prf;

Id INT(?tail)*epsS^sDUMMY1? = INT(?tail,[],sDUMMY1);
Repeat Id PREFACTOR(sDUMMY1?)*PREFACTOR(sDUMMY2?) = PREFACTOR(sDUMMY1*sDUMMY2);
.sort

** Prepare for SecDec **
PolyRatFun;
.sort
Id prf(sDUMMY1?,sDUMMY2?) = prf(sDUMMY1)/sDUMMY2;


#OpenDictionary SecDec
#Add prf: ""
#CloseDictionary

#UseDictionary SecDec

Bracket PREFACTOR,COLORFACTOR;
print+s;
.end

Format C;
#Create <`OUTFILE'.cc>
#Write <`OUTFILE'.cc>, "l1 = %e", sum(l1)

.end

** OLD CODE **
Format O3;
.sort
ExtraSymbols,array,w;
Format Fortran;
#Optimize sum
#Create <`OUTFILE'.cc>
#Write <`OUTFILE'.cc>, "w_(`optimmaxvar_')"
#Write <`OUTFILE'.cc>, "%O"
#Write <`OUTFILE'.cc>, "l1 = %e", sum(l1)
#ClearOptimize
.end
