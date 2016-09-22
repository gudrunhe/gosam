Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Load GoSam result
#include- `OUTFILE'reduced.log;

#include- secdec-`OUTFILE'.hh
.sort:convert to symbols;

#include- analytic-`OUTFILE'.hh
.sort:analytic expressions;

#IfDef `MASSCT'
#include- counterterms-`LOOPS'.hh
#EndIf

B prf,epsS;
.sort
Collect SCREEN;
.sort

Multiply replace_(dimS,4-2*epsS);
.sort
Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1*Den(sDUMMY2);
.sort

CFunction den; * den(x)=1/x, special function for series package
#include- series.hh
* 2*`LOOPS'+`ORD'+1 is max possible # terms in expansion epsS^(-2*`LOOPS') + ... + 1 + ... + epsS^(`ORD')
#call init({2*`LOOPS'+`ORD'+1})
#call series(epsS,`ORD')
Id Den(sDUMMY1?) = den(sDUMMY1);
#call expand(den)
Id den(sDUMMY1?) = Den(sDUMMY1);
.sort

Repeat Id sDUMMY1?!{epsS} = prf(sDUMMY1,1);
Repeat Id sDUMMY1?!{epsS}^(-1) = prf(1,sDUMMY1);
Id Den(sDUMMY1?) = prf(1,sDUMMY1);
.sort

PolyRatFun prf;
.sort:prf;
PolyRatFun;
.sort:no prf;

Id SCREEN(sDUMMY1?) = sDUMMY1;

B epsS;
.sort

* Define expressions for each epsilon order
#Do i= {-2*`LOOPS'},{`ORD'}
   #If ( `i' < 0)
      #Define j "{-`i'}"
      #Define ORDSIGN "m"
   #Else
      #Define j "`i'"
      #Define ORDSIGN ""
   #EndIf
   L l`LOOPS'ord`ORDSIGN'`j' = l`LOOPS'[epsS^(`i')];
#EndDo
.sort:eps expr;

* Drop original expression
Drop l`LOOPS';
.sort

**** SEE THE DO LOOP SECTION OF THE FORM MANUAL FOR A NEAT WAY TO ITERATE OVER BRACKETS

***** WARNING THE FOLLOWING CODE DOES NOT WORK IN GENERAL *****
* Assuming only c1
Id COLORFACTOR(c1) = c1;
B c1;
.sort:bracket c1;
#Do i= {-2*`LOOPS'},{`ORD'}
   #If ( `i' < 0)
      #Define j "{-`i'}"
      #Define ORDSIGN "m"
   #Else
      #Define j "`i'"
      #Define ORDSIGN ""
   #EndIf
   L l`LOOPS'ord`ORDSIGN'`j'c1 = l`LOOPS'ord`ORDSIGN'`j'[c1];
#EndDo
.sort

* Drop original expressions
#Do i= {-2*`LOOPS'},{`ORD'}
#If ( `i' < 0)
#Define j "{-`i'}"
#Define ORDSIGN "m"
#Else
#Define j "`i'"
#Define ORDSIGN ""
#EndIf
Drop l`LOOPS'ord`ORDSIGN'`j';
#EndDo
.sort

* Assuming only Proj1, Proj2
Id ProjLabel(sDUMMY1?) = sDUMMY1;
B Proj1, Proj2;
.sort:bracket proj;
#Do i= {-2*`LOOPS'},{`ORD'}
   #If ( `i' < 0)
      #Define j "{-`i'}"
      #Define ORDSIGN "m"
   #Else
      #Define j "`i'"
      #Define ORDSIGN ""
   #EndIf
   L l`LOOPS'ord`ORDSIGN'`j'c1p1 = l`LOOPS'ord`ORDSIGN'`j'c1[Proj1];
   L l`LOOPS'ord`ORDSIGN'`j'c1p2 = l`LOOPS'ord`ORDSIGN'`j'c1[Proj2];
#EndDo
.sort:proj exprs;

* Drop original expressions
#Do i= {-2*`LOOPS'},{`ORD'}
#If ( `i' < 0)
#Define j "{-`i'}"
#Define ORDSIGN "m"
#Else
#Define j "`i'"
#Define ORDSIGN ""
#EndIf
Drop l`LOOPS'ord`ORDSIGN'`j'c1;
#EndDo
.sort
***** END WARNING *****

Id COLORFACTOR(sDUMMY1?) = dum_(sDUMMY1);
Repeat Id PREFACTOR(sDUMMY1?)*PREFACTOR(sDUMMY1?) = PREFACTOR(sDUMMY1*sDUMMY1);
Id PREFACTOR(sDUMMY1?) = dum_(sDUMMY1);
*Id ProjLabel(sDUMMY1?) = dum_(sDUMMY1);
.sort:hide funcs;

* Remove prf;
Id prf(sDUMMY1?,sDUMMY2?) = sDUMMY1/sDUMMY2;
.sort:drop prf;

ExtraSymbols,array,w;
Format O3;
Format C;
.sort

#Do i= {-2*`LOOPS'},{`ORD'}
#If ( `i' < 0)
#Define j "{-`i'}"
#Define ORDSIGN "m"
#Else
#Define j "`i'"
#Define ORDSIGN ""
#EndIf
#Do c = 1,1
#Do p = 1,2
#Optimize l`LOOPS'ord`ORDSIGN'`j'c`c'p`p'
#Write <`OUTFILE'.cc>, "dcmplx l`LOOPS'ord`ORDSIGN'`j'c`c'p`p'()"
#Write <`OUTFILE'.cc>, "{"
#Write <`OUTFILE'.cc>, "    dcmplx w[{`optimmaxvar_'+1}];"
#Write <`OUTFILE'.cc>, "%4O"
#Write <`OUTFILE'.cc>, "    dcmplx res = %e", l`LOOPS'ord`ORDSIGN'`j'c`c'p`p'(res)
#Write <`OUTFILE'.cc>, "    return res;"
#Write <`OUTFILE'.cc>, "}\n"
#ClearOptimize
.sort:clear;
#EndDo;
#EndDo;
#EndDo;

.end
