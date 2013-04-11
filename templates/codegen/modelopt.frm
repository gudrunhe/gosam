* vim: ts=3:sw=3
off statistics;

* At the moment 02.04.13 Form abbreviations do not work therefore
* If you want to work on this uncomment this line
*#define `optim' "0"

* Because Form cannot 'clear' optimizations the way 
* we want we have simply call the script twice
* with the preprocessor variable PASS

*#include model.hh
#include symbols.hh

CF sqrt,sin,if,complexconjugate,cos,tan,pi;
* for the SM...
AutoDeclare S xy;
#include ../codegen/func.hh

#IfDef `optim'

* form abbreviation branch

#If `PASS' == 1

#Create<model.txt>
#Create<model.tmp>
#Create<model.dat>


.sort
Local BIG=
#do i=0,`$num'
    + x`i'*xy`i'
#enddo
;
.sort
#do i=0,`$num'
drop x`i';
#enddo
;
.sort
B
#do i=0,`$num'
xy`i',
#enddo
;
.sort
ExtraSymbols, vector, mabb;
Format O[%formopt.level%],stats=off;
#Optimize BIG
#Write <model.txt> "#####Functions"
#Write <model.txt> "%O", BIG
#write <model.tmp> "*--#[ BIG:"
#write <model.tmp> "L BIG=%E;",BIG
#write <model.tmp> "*--#] BIG:"
#write <model.dat> "number_abbs=`optimmaxvar_'";
#Close <model.tmp>
#Close <model.txt>
#Close <model.dat>
.sort
#ElseIf `PASS' == 2
#Append <model.txt>
.sort
CF mabb;
#include- model.tmp #BIG
.sort
B
#do i=0,`$num'
xy`i',
#enddo
;
.sort
#do i=0,`$num'
#$t=BIG[xy`i'];
#$n=x`i'name;
#Write <model.txt> "%$=%$;", $n,$t
#enddo
#Close <model.txt>
#EndIf

#Else

#If `PASS' == 1
* on pass 1, do nothing
#ElseIf `PASS' == 2
#Create <model.txt>
#Create <model.dat>
.sort
* on pass 2, write out model.txt
* without any optimizations
#Write <model.txt> "#####Functions"
#do i=0,`$num'
#$t=x`i';
#Write <model.txt> "%$=%$;", $name`i',$t
#enddo
.sort
#Write <model.dat> "number_abbs=0"
#Close <model.txt>
#Close <model.dat>

#EndIf
#EndIf


.end


