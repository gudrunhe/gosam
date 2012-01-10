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

#Include- `PROCESSPATH'/process.hh

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
							+ c(`c1',`c2') * propcolor(`I', `J')
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

Brackets+ c;
.sort
#Create <`OUTFILE'.txt>

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

#Do c1=1,`NUMCS'
#Do c2=1,`NUMCS'
	#$t=CC[c(`c1',`c2')];
	#Write <`OUTFILE'.txt> "CC_`c1'_`c2' = %$;", $t
#EndDo
#EndDo

#If `CREATETT'
	#Do I={`COLORED'}
		#If `I'0 != 0
			#Do J={`COLORED'}
				#If `J' >= `I'
					#Do c1=1,`NUMCS'
					#Do c2=`c1',`NUMCS'
						#$t=T`I'T`J'[c(`c1',`c2')];
						#Write <`OUTFILE'.txt> "T`I'T`J'_`c1'_`c2' = %$;", $t
					#EndDo
					#EndDo
				#EndIf
			#EndDo
		#EndIf
	#EndDo
#EndIf
#Close <`OUTFILE'.txt>
.end
