
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



#Procedure OptimizeCode(R2PREFACTOR)

Local tot`DIAG'=CC*diagram`DIAG'+R2*d`DIAG'R2;
Id Q.Q = QspQ;
Id Q.k1 = Qspk1;
Id Q.k2 = Qspk2;
Id Q.k3 = Qspk3;
Id Q.l3 = Qspl3;
Id Q.k4 = Qspk4;
Id Q.l4 = Qspl4;
Id Q.e1 = Qspe1;
Id Q.e2 = Qspe2;
.sort
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);
.sort
Hide diagram`DIAG',d`DIAG'R2;
Format O2,stats=off;
Brackets CC,R2,Qt2,QspQ,Qspk1,Qspk2,Qspk3,Qspl3,Qspk4,Qspl4,Qspe1,Qspe2,Qspvak1k2,Qspvak1l3,Qspvak1l4,Qspvak2k1,Qspvak2l3,Qspvak2l4,Qspval3k1,Qspval3k2,Qspval3l4,Qspval4k1,Qspval4k2,Qspval4l3,Qspvak1e1,Qspvae1k1,Qspvak1e2,Qspvae2k1,Qspvak2e1,Qspvae1k2,Qspvak2e2,Qspvae2k2,Qspval3e1,Qspvae1l3,Qspval3e2,Qspvae2l3,Qspval4e1,Qspvae1l4,Qspval4e2,Qspvae2l4,Qspvae1e2,Qspvae2e1;
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
#EndProcedure


#Procedure WriteUnoptimized(R2PREFACTOR)

Local tot`DIAG'=CC*diagram`DIAG'+R2*d`DIAG'R2;
Id Q.Q = QspQ;
Id Q.k1 = Qspk1;
Id Q.k2 = Qspk2;
Id Q.k3 = Qspk3;
Id Q.l3 = Qspl3;
Id Q.k4 = Qspk4;
Id Q.l4 = Qspl4;
Id Q.e1 = Qspe1;
Id Q.e2 = Qspe2;
.sort
Id vDUMMY1?.vDUMMY2? = dotproduct(vDUMMY1,vDUMMY2);
.sort
Hide diagram`DIAG',d`DIAG'R2;

Brackets CC,R2,Qt2,QspQ,Qspk1,Qspk2,Qspk3,Qspl3,Qspk4,Qspl4,Qspe1,Qspe2,Qspvak1k2,Qspvak1l3,Qspvak1l4,Qspvak2k1,Qspvak2l3,Qspvak2l4,Qspval3k1,Qspval3k2,Qspval3l4,Qspval4k1,Qspval4k2,Qspval4l3,Qspvak1e1,Qspvae1k1,Qspvak1e2,Qspvae2k1,Qspvak2e1,Qspvae1k2,Qspvak2e2,Qspvae2k2,Qspval3e1,Qspvae1l3,Qspval3e2,Qspvae2l3,Qspval4e1,Qspvae1l4,Qspval4e2,Qspvae2l4,Qspvae1e2,Qspvae2e1;
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
