CFunction ExternalMomenta,MomList,PropList;
CFunction PropVec;
CFunction DenStore;

* dimS = 4 - 2* epsS
* lower limit from IR divergence of loop integral (true for linear propagators?)
* upper limit from needing O(epS^2) terms for IR terms at 2-loop, WARNING - THIS MUST BE MADE MORE GENERAL
Symbols epsS(:{2*`LOOPS'});
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
             = INT(sDUMMY1,[],?tail,[],sDUMMY6,[],PropList(?head));
#EndProcedure
             
#Procedure FactorDimSecDec()
   FactArg Den;
   ChainOut Den;
   SplitArg Den;
   Id Den(sDUMMY1?number_,dimS) = DenDim(dimS+sDUMMY1);
   Id Den(dimS,sDUMMY1?number_) = DenDim(dimS+sDUMMY1);
   Id dimS = Dim(dimS);
   .sort
   Repeat Id Den(sDUMMY1?,sDUMMY2,?tail) = Den(sDUMMY1+sDUMMY2,?tail); ** THIS LINE SEEMS NOT TO BE WORKING CORRECTLY!
   .sort
* Restore Den(a,b,...) to Den(a+b+...)
   Id Den(?a)=Den(?a,DenStore(0));
   Repeat;
      Id Den(?head,sDUMMY1?,DenStore(sDUMMY2?)) = Den(?head,DenStore(sDUMMY1+sDUMMY2));
   EndRepeat;
   Id Den(DenStore(sDUMMY1?)) = Den(sDUMMY1);
#EndProcedure

* Series expand
* dimS = 4 - 2 * epsS
****
* WARNING: This procedure drops terms of O(epsS^{`TRUNCORD'+1})
*          This is only valid if the full expansion of the MIs
*          has already been inserted
****
#Procedure ExpandDimSecDec(TRUNCORD)
   Multiply replace_(dimS,4-2*epsS);
   .sort:dimS->epsS;
   SplitArg DenDim;
   Id Dim(sDUMMY1?) = sDUMMY1;
   Id DenDim(-2*epsS) = 1/(-2*epsS); * Extract poles
   Id DenDim(sDUMMY1?,-2*epsS) = DenDim(-2*epsS,sDUMMY1); * Bring denominator into correct order
* Taylor expand each factor of Den(d+a) about epsS = 0
* 1/(-2*x+n) = \sum_a=0^\infty ( x^a 2^a n^(-1-a) )
   Repeat Id Once DenDim(-2*epsS,sDUMMY1?)*epsS^sDUMMY2? =
   epsS^sDUMMY2*sum_(sDUMMY3,0,{2*`LOOPS'}-sDUMMY2,epsS^sDUMMY3*2^sDUMMY3*sDUMMY1^(-1-sDUMMY3));
   .sort:expand;
   Id epsS^(`TRUNCORD') = 0;
   .sort:truncate;
#EndProcedure
