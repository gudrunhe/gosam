off statistics;

* Simultaneous optimization of multiple expression (in our case: diagrams)
* The approach implemented below basically follows arXiv:1310.7007, section 4.2

#Define LOOPS "1"

* include symbols
* #Include- abbreviate.hh
#Include- spinney.hh
#include- symbols.hh
#include- ../model.hh

* extra symbol for R2prefactor
S Nfrat; 

* scalar products with loop momentum Q
Autodeclare Symbol Q;

.sort

*load diagram expressions 
#Include- diagramsl1.hh

.sort

ExtraSymbols,vector,abb;

* Introduce optimizations for expression that are independent
* of the loop momentum Q.

AutoDeclare S label;
Symbol R2SumLabel;

Local diagsum = `diagsum'
.sort


* Introduce abbreviations for the Q independent terms
`BracketLabelsAndQ'
.sort

Format O[%formopt.level%],stats=off;
#optimize diagsum;
`BracketLabelsAndQ'
.sort

#write <abbrevh`helicity'.txt> "*Abbreviations for all diagrams. Generated on `DATE_'"
#write <abbrevh`helicity'.txt> ""
#write <abbrevh`helicity'.txt> "#####Abbreviations"
#write <abbrevh`helicity'.txt> "%O"
#write <abbrevh`helicity'.dat> "abbrev_terms=`optimmaxvar_'"

* Write out the diagrams in terms of common Q independent abbreviations "abb"
`BracketLabelsOnly'
.sort
#call writeDiagrams()
`BracketLabelsOnly'
.sort

* Write sum of R2 terms
L R2Sum = diagsum[R2SumLabel];
`BracketLabelsOnly'
.sort
#write <abbrevh`helicity'.txt> "#####R2"
#write <abbrevh`helicity'.txt> ""
#Write <abbrevh`helicity'.txt> "R2Sum = %e", R2Sum;
#write <abbrevh`helicity'.txt> ""
.end
