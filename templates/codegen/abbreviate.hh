
CFunction ExAbGLOB;
AutoDeclare Symbols abb`DIAG'n;

#Define ExAbCount "0"

#Procedure ExtractAbbreviationsAntiBracket(ABBRFILE,PREFIX,?SYMBOLS)
   AntiBrackets `?SYMBOLS';
.sort:ExAbbr.1;
   Collect ExAbGLOB, ExAbGLOB;
   Normalize ExAbGLOB;
	Id ExAbGLOB(sDUMMY1?number_) = sDUMMY1;

   #Do i=1,1
      #ReDefine ExAbCount "{`ExAbCount'+1}" 
      Id once, ifmatch->ExAbSucc`ExAbCount'
			ExAbGLOB(sDUMMY1?$ExAbBrack`ExAbCount') = ExAbGLOB(sDUMMY1);
      Label ExAbFail`ExAbCount';
			Goto ExAbEndIf`ExAbCount';
      Label ExAbSucc`ExAbCount';
			Redefine i,"0";
      Label ExAbEndIf`ExAbCount';
.sort:ExAbbr.Loop`ExAbCount';
      #If `i' == 0
         Id ExAbGLOB($ExAbBrack`ExAbCount') = `PREFIX'`ExAbCount';
			#Write <`ABBRFILE'> "`PREFIX'`ExAbCount'=%$;", \
				$ExAbBrack`ExAbCount'
      #EndIf
   #EndDo
#EndProcedure

#Procedure ExtractAbbreviationsBracket(ABBRFILE,PREFIX,?SYMBOLS)
   Brackets `?SYMBOLS';
.sort:ExAbbr.1;
   Collect ExAbGLOB, ExAbGLOB;
*   Normalize ExAbGLOB;
   Id ExAbGLOB(sDUMMY1?number_) = sDUMMY1;

   #Do i=1,1
      #ReDefine ExAbCount "{`ExAbCount'+1}" 
      Id once, ifmatch->ExAbSucc`ExAbCount'
			ExAbGLOB(sDUMMY1?$ExAbBrack`ExAbCount') = ExAbGLOB(sDUMMY1);
      Label ExAbFail`ExAbCount';
			Goto ExAbEndIf`ExAbCount';
      Label ExAbSucc`ExAbCount';
			Redefine i,"0";
      Label ExAbEndIf`ExAbCount';
.sort:ExAbbr.Loop`ExAbCount';
      #If `i' == 0
         Id ExAbGLOB($ExAbBrack`ExAbCount') = `PREFIX'`ExAbCount';
			#Write <`ABBRFILE'> "`PREFIX'`ExAbCount'=%$;", \
				$ExAbBrack`ExAbCount'
      #EndIf
   #EndDo
#EndProcedure


[% 
@if extension formopt %]
#Procedure OptimizeCode(R2PREFACTOR)

Local tot`DIAG'=CC*diagram`DIAG'+R2*d`DIAG'R2;
Id Q.Q = QspQ;[%
@for particles %]
Id Q.k[%index%] = Qspk[%index%];[%
@if is_massive %]
Id Q.l[%index%] = Qspl[%index%];[%
@end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for particles lightlike vector %]
Id Q.e[%index%] = Qspe[%index%];[%
@end @for %][%
@end @if %]
.sort
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);[%
@if extension tracify%]
#Do vec1={`LIGHTLIKE'}
  #Do vec2={`LIGHTLIKE'}
    #Do vec3={`LIGHTLIKE'}
      Id Qeps(`vec1',`vec2',`vec3') = Qeps`vec1'`vec2'`vec3';
    #EndDo
  #EndDo
#EndDo[%
@end @if%]
.sort
Hide diagram`DIAG',d`DIAG'R2;
Format O[%formopt.level%],stats=off;
Brackets CC,R2,[%
@if extension tracify%]
  #Do vec1={`LIGHTLIKE'}
    #Do vec2={`LIGHTLIKE'}
      #Do vec3={`LIGHTLIKE'}
        Qeps`vec1'`vec2'`vec3',
      #EndDo
    #EndDo
  #EndDo
[%@end @if%]Qt2,QspQ[%
@for particles %],Qspk[%index%][%
   @if is_massive %],Qspl[%index%][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],Qspe[%index%][%
   @end @for %][%
@end @if %][%
@for pairs distinct %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %],Qspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%@end @if %][%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
            is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspvae[%index1%]e[%index2%],Qspvae[%index2%]e[%index1%][%
      @end @if %][%
   @end @for %][%
@end @if %];
.sort

ExtraSymbols,vector,abb`DIAG';
*Format fortran90,.0_ki;
*Format doublefortran;
#append <`OUTFILE'.txt>
#append <`OUTFILE'.dat>
#optimize tot`DIAG';
#write <`OUTFILE'.txt> "*Abbreviations for diagram `OUTFILE'. Generated on `DATE_'"
#write <`OUTFILE'.txt> ""
#write <`OUTFILE'.txt> "#####Abbreviations"
#write <`OUTFILE'.txt> "%O"
#write <`OUTFILE'.txt> "#####R2"
#write <`OUTFILE'.txt> ""
#write <`OUTFILE'.dat> "abbrev_terms=`optimmaxvar_'"
.sort
L redCC`DIAG' = tot`DIAG'*replace_(CC,1,R2,0);
L redR2`DIAG' = tot`DIAG'*replace_(CC,0,R2,1);
.sort
#If "`R2PREFACTOR'" != "1"
#Write <`OUTFILE'.txt> "R2d`DIAG' = `R2PREFACTOR' *(%E);", redR2`DIAG'
#write <`OUTFILE'.txt> ""
#Else
#Write <`OUTFILE'.txt> "R2d`DIAG' = %E;", redR2`DIAG'
#write <`OUTFILE'.txt> ""
#EndIf
.sort
Format Normal;
#write <`OUTFILE'.prc> "L diagram`DIAG'  = %e",redCC`DIAG';
#EndProcedure[%
@end @if %]


#Procedure WriteUnoptimized(R2PREFACTOR)

Local tot`DIAG'=CC*diagram`DIAG'+R2*d`DIAG'R2;
Id Q.Q = QspQ;[%
@for particles %]
Id Q.k[%index%] = Qspk[%index%];[%
@if is_massive %]
Id Q.l[%index%] = Qspl[%index%];[%
@end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for particles lightlike vector %]
Id Q.e[%index%] = Qspe[%index%];[%
@end @for %][%
@end @if %]
.sort
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);
.sort
Hide diagram`DIAG',d`DIAG'R2;

Brackets CC,R2,Qt2,QspQ[%
@for particles %],Qspk[%index%][%
   @if is_massive %],Qspl[%index%][%
   @end @if %][%
@end @for %][%
@if internal NUMPOLVEC %][%
   @for particles lightlike vector %],Qspe[%index%][%
   @end @for %][%
@end @if %][%
@for pairs distinct %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][% 
   @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %][%
@end @for %][%
@if internal NUMPOLVEC %][%
@for pairs %][%
   @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspva[%
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1%]e[% index2 %],Qspvae[% index2 %][% 
   @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%@end @if %][%
   @end @for %][%
@for pairs distinct ordered %][%
   @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
            is_lightlike2 .and. ( 2spin2 .eq. 2 ) %],Qspvae[%index1%]e[%index2%],Qspvae[%index2%]e[%index1%][%
      @end @if %][%
   @end @for %][%
@end @if %];
.sort

#append <`OUTFILE'.txt>
#append <`OUTFILE'.dat>
.sort
L redCC`DIAG' = tot`DIAG'*replace_(CC,1,R2,0);
L redR2`DIAG' = tot`DIAG'*replace_(CC,0,R2,1);
.sort
#If "`R2PREFACTOR'" != "1"
#Write <`OUTFILE'.txt> "R2d`DIAG' = `R2PREFACTOR' *(%E);", redR2`DIAG'
#write <`OUTFILE'.txt> ""
#Else
#Write <`OUTFILE'.txt> "R2d`DIAG' = %E;", redR2`DIAG'
#write <`OUTFILE'.txt> ""
#EndIf
.sort
#write <`OUTFILE'.prc> "L diagram`DIAG'  = %e",redCC`DIAG';
#write <`OUTFILE'.prc> ""
#Write <`OUTFILE'.prc> "L R2d`DIAG' = %E;", redR2`DIAG'
#EndProcedure
