Format 255; * Number of characters per line

#include- reduze.hh
#include- secdec.hh
#include- symbols.hh
#include- spinney.hh
#include- model.hh

* Process sum
* Load GoSam result
#Do i = `FIRST', `LAST'
#include- d`i'h0l`LOOPS'.log;
#EndDo

.sort:prefactors;

G sum =
#Do i = `FIRST', `LAST'
   + d`i'h0l`LOOPS'
#EndDo
;
.sort:sum;

Drop;
NDrop sum;
.sort

PolyRatFun prf;
.sort:prf;

PolyRatFun;
.sort:noprf;

B INT;
.sort:bracket;
Collect SCREEN;
.sort:collect;

#Write <`OUTFILE'.log>, "L l`LOOPS' = %e", sum
.sort:writesum;

*
* Write list of integrals
*
Id SCREEN(?head)=1;
.sort:drop screen;
DropCoefficient;
.sort:drop coeff;
#Write <`OUTFILE'integrals.txt>, "%E", sum
print+s;
.end