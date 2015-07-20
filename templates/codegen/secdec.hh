CFunction ExternalMomenta,MomList,PropList;
CFunction PropVec;
CFunction DenStore;

* dimS = 4 - 2* epsS
Symbols epsS;
Symbols sDUMMY6;

#Procedure TagToPropListSecDec()
   Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?) = Tag(sDUMMY1,PropVec(vDUMMY1)^2-sDUMMY2^2);
   Multiply PropList;
* (maximal) number of independent scalar products is LOOPS*(LOOPS+1)/2 + LOOPS*(LEGS-1), provided momentum is conserved and LEGS-1<dimS
   #Do i = 0, {`LOOPS'*(`LOOPS'+1)/2 +`LOOPS'*(`LEGS'-1) - 1}
      Id Tag(ReduzeN`i',?tail)*PropList(?head) = PropList(?head,?tail);
   #EndDo
#EndProcedure

#Procedure IntToSecDec()
   Id INT(sDUMMY1?,sDUMMY2?,sDUMMY3?,sDUMMY4?,sDUMMY5?,[],?tail,[],sDUMMY6?)*PropList(?head)
             = INT(sDUMMY1,[],sDUMMY2,sDUMMY3,sDUMMY4,sDUMMY5,[],?tail,[],sDUMMY6,[],PropList(?head));
#EndProcedure
