If ( Match(Sector( ReduzeT1L2,?tail)) );
Multiply Tag(ReduzeN0,p1, mT);
Multiply Tag(ReduzeN1,p2, mT);
Multiply Tag(ReduzeN2,p1-p2, 0);
Multiply Tag(ReduzeN3,p1-k1, mT);
Multiply Tag(ReduzeN4,-k1+p2, mT);
Multiply Tag(ReduzeN5,p1-k1-k2, mT);
Multiply Tag(ReduzeN6,-k1+p2-k2, mT);
Multiply Tag(ReduzeN7,-k3+p1-k1-k2, mT);
Multiply Tag(ReduzeN8,-k3-k1+p2-k2, mT);
EndIf;

If ( Match(Sector( ReduzeT2L2,?tail)) );
Multiply Tag(ReduzeN0,p1, mT);
Multiply Tag(ReduzeN1,p2, mT);
Multiply Tag(ReduzeN2,p1-p2, 0);
Multiply Tag(ReduzeN3,p1-k1, mT);
Multiply Tag(ReduzeN4,p2-k1, mT);
Multiply Tag(ReduzeN5,p1-p2+k2, 0);
Multiply Tag(ReduzeN6,-k3+p1-k1, mT);
Multiply Tag(ReduzeN7,-k3+p2-k1, mT);
Multiply Tag(ReduzeN8,-k3+p2-k1-k2, mT);
EndIf;

If ( Match(Sector( ReduzeT3L2,?tail)) );
Multiply Tag(ReduzeN0,p1, 0);
Multiply Tag(ReduzeN1,p2, mT);
Multiply Tag(ReduzeN2,-p2+p1, mT);
Multiply Tag(ReduzeN3,-k1+p1, 0);
Multiply Tag(ReduzeN4,p2-k1, mT);
Multiply Tag(ReduzeN5,-k1-k2+p1, 0);
Multiply Tag(ReduzeN6,p2-k1-k2, mT);
Multiply Tag(ReduzeN7,k3-p2+p1, mT);
Multiply Tag(ReduzeN8,-k3+p2-k1-k2, mT);
EndIf;

If ( Match(Sector( ReduzeT4L2,?tail)) );
Multiply Tag(ReduzeN0,p1, 0);
Multiply Tag(ReduzeN1,p2, 0);
Multiply Tag(ReduzeN2,p1-p2, mT);
Multiply Tag(ReduzeN3,-k1+p1, mT);
Multiply Tag(ReduzeN4,-k1+p2, 0);
Multiply Tag(ReduzeN5,-k1+p1-k2, mT);
Multiply Tag(ReduzeN6,k3+p1-p2, mT);
Multiply Tag(ReduzeN7,-k3-k1-k2+p2, 0);
Multiply Tag(ReduzeN8,-k1+p1-k2-p2, mT);
EndIf;

