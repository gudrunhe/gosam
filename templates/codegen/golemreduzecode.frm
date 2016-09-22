#-
off statistics;
*Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh
#include- seriesprocedures.hh

* Load GoSam result
#include- `COFILE'
.sort

Id INT(ReduzeF?$IntegralName,sDUMMY1?$LowestPrefactorOrder,sDUMMY2?$LowestOrder) = 1; * Get integral name, lowest_prefactor_order, lowest_order
.sort

Id SCREEN(sDUMMY1?) = sDUMMY1;

#write "IntegralName = `$IntegralName'"
#write "LowestPrefactorOrder = `$LowestPrefactorOrder'"
#write "LowestOrder = `$LowestOrder'"
.sort

Multiply replace_(dimS,4-2*epsS);
.sort

#call seriesExpand(coeff, epsS, {`ORD'-`$LowestPrefactorOrder'-`$LowestOrder'})

B epsS,ProjLabel,COLORFACTOR,PREFACTOR;
print+s;

.end