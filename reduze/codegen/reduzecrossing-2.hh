Id Sector( ReduzeT1L2x12x34,?tail) = Crossing( ReduzeT1L2x12x34)*Sector( ReduzeT1L2,?tail);
If ( Match(Crossing( ReduzeT1L2x12x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[],k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT1L2x12,?tail) = Crossing( ReduzeT1L2x12)*Sector( ReduzeT1L2,?tail);
If ( Match(Crossing( ReduzeT1L2x12)) );
 Multiply CrossingShift(k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT1L2x34,?tail) = Crossing( ReduzeT1L2x34)*Sector( ReduzeT1L2,?tail);
If ( Match(Crossing( ReduzeT1L2x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT2L2x12x34,?tail) = Crossing( ReduzeT2L2x12x34)*Sector( ReduzeT2L2,?tail);
If ( Match(Crossing( ReduzeT2L2x12x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[],k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT2L2x12,?tail) = Crossing( ReduzeT2L2x12)*Sector( ReduzeT2L2,?tail);
If ( Match(Crossing( ReduzeT2L2x12)) );
 Multiply CrossingShift(k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT2L2x34,?tail) = Crossing( ReduzeT2L2x34)*Sector( ReduzeT2L2,?tail);
If ( Match(Crossing( ReduzeT2L2x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT3L2x12x34,?tail) = Crossing( ReduzeT3L2x12x34)*Sector( ReduzeT3L2,?tail);
If ( Match(Crossing( ReduzeT3L2x12x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[],k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT3L2x12,?tail) = Crossing( ReduzeT3L2x12)*Sector( ReduzeT3L2,?tail);
If ( Match(Crossing( ReduzeT3L2x12)) );
 Multiply CrossingShift(k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT3L2x34,?tail) = Crossing( ReduzeT3L2x34)*Sector( ReduzeT3L2,?tail);
If ( Match(Crossing( ReduzeT3L2x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT4L2x12x34,?tail) = Crossing( ReduzeT4L2x12x34)*Sector( ReduzeT4L2,?tail);
If ( Match(Crossing( ReduzeT4L2x12x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[],k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants([]);
EndIf;

Id Sector( ReduzeT4L2x12,?tail) = Crossing( ReduzeT4L2x12)*Sector( ReduzeT4L2,?tail);
If ( Match(Crossing( ReduzeT4L2x12)) );
 Multiply CrossingShift(k1, k2,[],k2, k1,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

Id Sector( ReduzeT4L2x34,?tail) = Crossing( ReduzeT4L2x34)*Sector( ReduzeT4L2,?tail);
If ( Match(Crossing( ReduzeT4L2x34)) );
 Multiply CrossingShift(k3, -k3-k1-k2,[]);
 Multiply CrossingInvariants(es23, 2*mH^2-es12-es23,[]);
EndIf;

