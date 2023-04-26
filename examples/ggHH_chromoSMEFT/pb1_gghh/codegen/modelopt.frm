* vim: ts=3:sw=3

off statistics;

#include symbols.hh
CF sqrt,sin,if,complexconjugate,cos,tan,pi,atan;

* for the SM...
AutoDeclare S xy;

#include ../codegen/func.hh

#Create <model.txt>
#Create <model.dat>

.sort

* write out model.txt without any optimizations
#Write <model.txt> "#####Functions"
#do i=0,`$num'
#$t=x`i';
#Write <model.txt> "%$=%$;", $name`i',$t
#enddo

.sort

#Write <model.dat> "number_abbs=0"
#Close <model.txt>
#Close <model.dat>

.end
