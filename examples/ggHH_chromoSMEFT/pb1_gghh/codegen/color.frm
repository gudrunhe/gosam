* vim: ts=3:sw=3
off statistics;
*
* This program calculates the color correlation matrices
* for a given process.
*
#Include- symbols.hh

Indices iDUMMY1, ..., iDUMMY4;
AutoDeclare CFunctions fDUMMY;
CFunctions c;

#Include- color.hh

.global
*InParallel;

* The variable CREATETT defines if the user wants to
* create dipole terms. If this is the case the matrices
* T_i.T_j are needed.

#If `CREATETT'
	#Do I={`COLORED'}
		#If `I'0 != 0
			#Do J={`COLORED'}
					#If `J' >= `I'
					Global T`I'T`J' =
					#Do c1=1,`NUMCS'
						#Do c2=1,`NUMCS'

							+ T(`I',`J')*c(`c1',`c2') * propcolor(`I', `J')

						#EndDo
					#EndDo
					;
				#EndIf
			#EndDo
		#EndIf
	#EndDo
#EndIf

Global CC =
	#Do c1=1,`NUMCS'
	#Do c2=1,`NUMCS'
		+ c(`c1',`c2')
	#EndDo
	#EndDo
;

#Call invcolorbasis(a,1)
#Call invcolorbasis(b,2)
#Call colorinsertion

Id propcolor(?all) = 1;
#Call coloralgebra(0)

Repeat Id delta(iDUMMY1?, iDUMMY2?) * delta(iDUMMY2?, iDUMMY3?) =
	delta(iDUMMY1, iDUMMY3);
Id delta(iDUMMY1?, iDUMMY1?) = NC;



* You are using Form Optimization, this is experimental
* and may crash due to lack of memory
.sort
*
AutoDeclare S TLabel,CLabel;
#Do I={`COLORED'}
	#If `I'0 != 0
		#Do J={`COLORED'}
			#If `J' >= `I'
				#Do c1=1,`NUMCS'
					#Do c2=1,`NUMCS'
						#$T`I'`J'c`c1'c`c2' = TLabel^(`c1' + `c2'*(`NUMCS'+1) + `I'*(`NUMCS'+1)*(`NUMCS'+1) + `J'*(4+1)*(`NUMCS'+1)*(`NUMCS'+1));
						Id T(`I',`J')*c(`c1',`c2') = $T`I'`J'c`c1'c`c2';
					#EndDo
				#EndDo
			#EndIf
		#EndDo
	#EndIf
#EndDo
#Do c1=1,`NUMCS'
	#Do c2=1,`NUMCS'
	#$C`c1'C`c2' = CLabel^(`c1' + `c2'*(`NUMCS'+1));
	Id c(`c1',`c2') = $C`c1'C`c2';
	#EndDo
#EndDo
;
.sort
Local BIG = CC +
#Do I={`COLORED'}
	#If `I'0 != 0
		#Do J={`COLORED'}
			#If `J' >= `I'
				+ T`I'T`J'
			#EndIf
		#EndDo
	#EndIf
#EndDo
;
.sort
Drop CC
#Do I={`COLORED'}
	#If `I'0 != 0
		#Do J={`COLORED'}
			#If `J' >= `I'
				T`I'T`J',
			#EndIf
		#EndDo
	#EndIf
#EndDo
;

.sort
B TLabel,CLabel;
.sort
#Create <`OUTFILE'.txt>
#Create <`OUTFILE'.tmp>
#Write <`OUTFILE'.txt> "#####Color"
#Write <`OUTFILE'.txt> "NA=NC*NC-1;"
#If "`INCOLORS'" != ""
	#Write <`OUTFILE'.txt> "incolors=1%"
	#Do NC={`INCOLORS'}
		#Write <`OUTFILE'.txt> " * `NC'%"
	#EndDo
	#Write <`OUTFILE'.txt> ";"
#Else
	#Write <`OUTFILE'.txt> "incolors=1;"
#EndIf

ExtraSymbols,vector,cabb;
Format O2,stats=off;
#Optimize BIG;
#write <`OUTFILE'.txt> "%O"
#Create <`OUTFILE'.tmp>
#Create <`OUTFILE'.dat>
#write <`OUTFILE'.tmp> "*--#[ BIG:"
#write <`OUTFILE'.tmp> "L BIG=%E;",BIG
#write <`OUTFILE'.tmp> "*--#] BIG:"
#write <`OUTFILE'.tmp> "*--#[ labeltranslation:"
#Do I={`COLORED'}
	#If `I'0 != 0
		#Do J={`COLORED'}
			#If `J' >= `I'
				#Do c1=1,`NUMCS'
					#Do c2=1,`NUMCS'
						#write <`OUTFILE'.tmp> "#Define T`I'`J'c`c1'c`c2' \"`$T`I'`J'c`c1'c`c2''\""
					#EndDo
				#EndDo
			#EndIf
		#EndDo
	#EndIf
#EndDo
#Do c1=1,`NUMCS'
	#Do c2=1,`NUMCS'
	#write <`OUTFILE'.tmp> "#Define C`c1'C`c2' \"`$C`c1'C`c2''\""
	#EndDo
#EndDo
#write <`OUTFILE'.tmp> "*--#] labeltranslation:"
#write <`OUTFILE'.dat> "number_abbs=`optimmaxvar_'";
#Close<`OUTFILE'.dat>

#Close<`OUTFILE'.tmp>
#Close<`OUTFILE'.txt>
.end

