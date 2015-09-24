* vim: ts=3:sw=3
off statistics;
#include- symbols.hh
CF cabb;
AutoDeclare S T,C;

#include- color.tmp

.sort
B CLabel, TLabel;
.sort
#Append <`OUTFILE'.txt>
#Do I={`COLORED'}
	#If `I'0 != 0
		#Do J={`COLORED'}
			#If `J' >= `I'
				#Do c1=1,`NUMCS'
					#Do c2=1,`NUMCS'
						#$t=BIG[`T`I'`J'c`c1'`c2''];
						#Write <`OUTFILE'.txt> "T`I'T`J'(`c1',`c2') = %$;", $t
						#If `c1' != `c2'
						#Write <`OUTFILE'.txt> "T`I'T`J'(`c2',`c1') = %$;", $t
						#EndIf
					#EndDo
				#EndDo
			#EndIf
		#EndDo
	#EndIf
#EndDo
#Do c1=1,`NUMCS'
	#Do c2=1,`NUMCS'
		#$t=BIG[`C`c1'`c2''];
		#Write <`OUTFILE'.txt> "CC(`c1',`c2') = %$;", $t
	#EndDo
#EndDo
;
#Close<`OUTFILE'.txt>

.end

