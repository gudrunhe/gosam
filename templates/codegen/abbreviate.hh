
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
