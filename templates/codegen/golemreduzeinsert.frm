* vim: syntax=form:ts=3:sw=3:expandtab
#-
off statistics;
*Format 255; * Number of characters per line

#Include- reduze.hh
#Include- secdec.hh
#Include- projectors.hh
#Include- symbols.hh
#Include- spinney.hh
#Include- model.hh
#Include- largeprf.hh

* Create list of ProjLabel1,...,ProjLabel`NUMPROJ'
#Define ProjectorLabels ""
#Do label = 1, `NUMPROJ'
#Redefine ProjectorLabels "`ProjectorLabels',ProjLabel`label'"
#EndDo
.sort

* Load GoSam result
#include- l`LOOPS'.txt;

G l`LOOPS' = l`LOOPS';
.sort:sum;

* Pull prefactors out of INT function
Repeat Id INT(sDUMMY1?,?a,[],?b,[],?c) = sDUMMY1*INT(?a,[],?b,[],?c);
Id Once INT([],?a) = INT(?a);
.sort

* Insert reduction
#include- integralsl`LOOPS'.hh
.sort:reduce;

* Push projector labels, prefactor, colorfactor, colorinternal into INT 
* where they will not be touched
Id Once sDUMMY1?{,`ProjectorLabels'}*INT(?b) = INT(sDUMMY1,[],?b);
Repeat Id fDUMMY1?{PREFACTOR,COLORFACTOR,COLORINTERNAL,Dim,DenDim}(?a)*INT(?b) = INT(fDUMMY1(?a),?b);
.sort

* Get list of integrals
#call producelist(l`LOOPS',list,INT)
#$index = 0;
B INT;
.sort

* Put each integral*coefficients into own expression
#Do term = list
  #$index = $index+1;
  L [INT(`$index')] =  `term'*(l`LOOPS'[`term']);
#EndDo
.sort

* Write integral*coefficients
#Do i = 1,`$index'
  #Write <analytic/`LOOPS'loop/integrals/INT`i'.in> "L expr = %e", [INT(`i')]
#EndDo
.sort

* Drop everything except coefficients
Drop l1, list;
#Do i = 1,`$index'
  Drop [INT(`i')];
#EndDo
.sort

* Write coefficients
#Do e = {`activeexprnames_'}
  #IfDef `e' 
    #Write <analytic/`LOOPS'loop/integrals/coefficients.txt> "L `e' = %e" `e'
  #EndIf
#EndDo
.end

