Id Sector( ReduzeT1L1x12x34,?tail) = Crossing( ReduzeT1L1x12x34)*Sector( ReduzeT1L1,?tail);
If ( Match(Crossing( ReduzeT1L1x12x34)) );
 Multiply CrossingShift(k2, k1,[],k3, -k2-k3-k1,[],k1, k2,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT1L1x12,?tail) = Crossing( ReduzeT1L1x12)*Sector( ReduzeT1L1,?tail);
If ( Match(Crossing( ReduzeT1L1x12)) );
 Multiply CrossingShift(k2, k1,[],k1, k2,[]);
 Multiply CrossingInvariants(es23, -es23+2*mH^2-es12,[]);
EndIf;

Id Sector( ReduzeT1L1x34,?tail) = Crossing( ReduzeT1L1x34)*Sector( ReduzeT1L1,?tail);
If ( Match(Crossing( ReduzeT1L1x34)) );
 Multiply CrossingShift(k3, -k2-k3-k1,[]);
 Multiply CrossingInvariants(es23, -es23+2*mH^2-es12,[]);
EndIf;

Id Sector( ReduzeT2L1x12x34,?tail) = Crossing( ReduzeT2L1x12x34)*Sector( ReduzeT2L1,?tail);
If ( Match(Crossing( ReduzeT2L1x12x34)) );
 Multiply CrossingShift(k2, k1,[],k3, -k2-k3-k1,[],k1, k2,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT2L1x12,?tail) = Crossing( ReduzeT2L1x12)*Sector( ReduzeT2L1,?tail);
If ( Match(Crossing( ReduzeT2L1x12)) );
 Multiply CrossingShift(k2, k1,[],k1, k2,[]);
 Multiply CrossingInvariants(es23, -es23+2*mH^2-es12,[]);
EndIf;

Id Sector( ReduzeT2L1x34,?tail) = Crossing( ReduzeT2L1x34)*Sector( ReduzeT2L1,?tail);
If ( Match(Crossing( ReduzeT2L1x34)) );
 Multiply CrossingShift(k3, -k2-k3-k1,[]);
 Multiply CrossingInvariants(es23, -es23+2*mH^2-es12,[]);
EndIf;

