CFunction ExternalMomenta,MomList,PropList;
CFunction PropVec;

#Procedure ToPropListSecDec
   Id Sector(sDUMMY1?,?tail) = Sector(sDUMMY1);
   Id Sector(sDUMMY1?,?tail)*Crossing(sDUMMY2?) = Sector(sDUMMY2);
   Id Tag(sDUMMY1?,vDUMMY1?,sDUMMY2?) = Tag(sDUMMY1,PropVec(vDUMMY1)^2-sDUMMY2^2);
   Multiply PropList;
* (maximal) number of independent scalar products is LOOPS*(LOOPS+1)/2 + LOOPS*(LEGS-1), provided momentum is conserved and LEGS-1<dimS
   #Do i = 0, {`LOOPS'*(`LOOPS'+1)/2 +`LOOPS'*(`LEGS'-1) - 1}
      Id Tag(ReduzeN`i',?tail)*PropList(?head) = PropList(?head,?tail);
   #EndDo
#EndProcedure

#Procedure MomListSecDec
   Multiply MomList(
   #Do i = 1, `LOOPS'
      p`i'
   #EndDo
   );
#EndProcedure

#Procedure ExternalMomentaSecDec
   Multiply ExternalMomenta(
   #Do i = 1, `LEGS'
      k`i'
   #EndDo
   );
#EndProcedure

*TODO
* - Construct KinematicInvariants list
* - Construct Masses list
* - Construct ScalarProductRules list

