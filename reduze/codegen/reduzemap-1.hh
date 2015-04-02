If ( Match(Sector( ReduzeT1L1,?tail)) );
Multiply Tag(ReduzeN0,p1, mT);
Multiply Tag(ReduzeN1,p1-k1, mT);
Multiply Tag(ReduzeN2,-k2+p1-k1, mT);
Multiply Tag(ReduzeN3,-k2-k3+p1-k1, mT);
EndIf;

If ( Match(Sector( ReduzeT2L1,?tail)) );
Multiply Tag(ReduzeN0,p1, mT);
Multiply Tag(ReduzeN1,p1-k1, mT);
Multiply Tag(ReduzeN2,p1-k3-k1, mT);
Multiply Tag(ReduzeN3,-k2+p1-k3-k1, mT);
EndIf;

