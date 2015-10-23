If ( Match(Sector( ReduzeT1L2,?tail)) );
id p1.k1 = ( 1/2*num(p1,mT)-1/2*num(p1-k1,mT) );
id p2.k2 = ( 1/2*num(k1-p2,mT)+1/2*es12-1/2*num(k1-p2+k2,mT) );
id p1.p1 = ( num(p1,mT)+mT^2 );
id p2.p2 = ( mT^2+num(p2,mT) );
id k3.p2 = ( 1/2*mH^2-1/2*es12-1/2*num(k3+k1-p2+k2,mT)+1/2*num(k1-p2+k2,mT) );
id k1.p2 = ( -1/2*num(k1-p2,mT)+1/2*num(p2,mT) );
id k3.p1 = ( 1/2*mH^2-1/2*es12-1/2*num(k3-p1+k1+k2,mT)+1/2*num(-p1+k1+k2,mT) );
id p1.k2 = ( 1/2*es12+1/2*num(p1-k1,mT)-1/2*num(-p1+k1+k2,mT) );
id p1.p2 = ( 1/2*num(p1,mT)+mT^2-1/2*num(p1-p2,0)+1/2*num(p2,mT) );
EndIf;
If ( Match(Sector( ReduzeT2L2,?tail)) );
id p1.k2 = ( -1/2*mH^2-1/2*num(p1-p2,0)+1/2*num(k3-p2+k1,mT)+1/2*es12+1/2*num(p1-p2+k2,0)+1/2*es23-1/2*num(k3-p2+k1+k2,mT) );
id p2.p2 = ( mT^2+num(p2,mT) );
id p2.k1 = ( -1/2*num(p2-k1,mT)+1/2*num(p2,mT) );
id p1.p2 = ( -1/2*num(p1-p2,0)+1/2*num(p1,mT)+mT^2+1/2*num(p2,mT) );
id k3.p2 = ( mH^2-1/2*num(k3-p2+k1,mT)-1/2*es12+1/2*num(p2-k1,mT)-1/2*es23 );
id p1.k1 = ( -1/2*num(p1-k1,mT)+1/2*num(p1,mT) );
id k3.p1 = ( -1/2*num(k3-p1+k1,mT)+mH^2-1/2*es12+1/2*num(p1-k1,mT)-1/2*es23 );
id p1.p1 = ( num(p1,mT)+mT^2 );
id p2.k2 = ( -1/2*mH^2+1/2*num(k3-p2+k1,mT)+1/2*es12+1/2*es23-1/2*num(k3-p2+k1+k2,mT) );
EndIf;
If ( Match(Sector( ReduzeT3L2,?tail)) );
id p2.p1 = ( 1/2*num(p1,0)+1/2*num(p2,mT)-1/2*num(p2-p1,mT) );
id p2.k2 = ( 1/2*es12+1/2*num(p2-k1,mT)-1/2*num(-p2+k1+k2,mT) );
id k3.p1 = ( -1/2*num(k3-p2+k1+k2,mT)-1/2*es12+1/2*num(k3-p2+p1,mT)-1/2*num(p2-p1,mT)+1/2*num(-p2+k1+k2,mT) );
id p1.p1 = ( num(p1,0) );
id k2.p1 = ( 1/2*es12+1/2*num(k1-p1,0)-1/2*num(k1+k2-p1,0) );
id p2.k1 = ( 1/2*num(p2,mT)-1/2*num(p2-k1,mT) );
id k3.p2 = ( 1/2*mH^2-1/2*num(k3-p2+k1+k2,mT)-1/2*es12+1/2*num(-p2+k1+k2,mT) );
id k1.p1 = ( 1/2*num(p1,0)-1/2*num(k1-p1,0) );
id p2.p2 = ( num(p2,mT)+mT^2 );
EndIf;
If ( Match(Sector( ReduzeT4L2,?tail)) );
id k3.p2 = ( 1/2*mH^2+1/2*num(k1-p1+k2,mT)-1/2*num(p1,0)-1/2*num(k1-p1+k2+p2,mT)-1/2*num(k3+k1+k2-p2,0)+1/2*num(p1-p2,mT)+1/2*num(p2,0)+1/2*mT^2 );
id p1.p2 = ( 1/2*num(p1,0)-1/2*num(p1-p2,mT)+1/2*num(p2,0)-1/2*mT^2 );
id p1.k2 = ( -1/2*num(k1-p1+k2,mT)+1/2*es12+1/2*num(k1-p1,mT) );
id k3.p1 = ( 1/2*num(k3+p1-p2,mT)+1/2*num(k1-p1+k2,mT)-1/2*num(p1,0)-1/2*num(k1-p1+k2+p2,mT)-1/2*num(k3+k1+k2-p2,0)+1/2*num(p2,0)+1/2*mT^2 );
id p1.p1 = ( num(p1,0) );
id p2.p2 = ( num(p2,0) );
id k1.p1 = ( 1/2*num(p1,0)-1/2*mT^2-1/2*num(k1-p1,mT) );
id k2.p2 = ( -1/2*num(k1-p1+k2,mT)+1/2*num(k1-p2,0)+1/2*num(p1,0)+1/2*num(k1-p1+k2+p2,mT)-1/2*num(p1-p2,mT)-1/2*num(p2,0)-1/2*mT^2 );
id k1.p2 = ( -1/2*num(k1-p2,0)+1/2*num(p2,0) );
EndIf;