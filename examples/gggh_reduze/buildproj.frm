#-
Format 255;

Symbols d;
Dimension d;

AutoDeclare Indices iDUMMY;
AutoDeclare Vectors p;
AutoDeclare Symbols sDUMMY;
AutoDeclare Symbols ProjLabel;

Symbols s,t,u;
AutoDeclare Symbols F;

CFunctions prf, Dim, DenDim, ProjNum, ProjDen;

L amplitude = 
+ F1*d_(iDUMMY1,iDUMMY2)*p2(iDUMMY3) 
+ F2*d_(iDUMMY1,iDUMMY3)*p1(iDUMMY2) 
+ F3*d_(iDUMMY2,iDUMMY3)*p3(iDUMMY1) 
+ F4*p3(iDUMMY1)*p1(iDUMMY2)*p2(iDUMMY3);
.sort

L spinsum =
( -d_(iDUMMYP1,iDUMMY1) + ( p1(iDUMMYP1)*p2(iDUMMY1)+p2(iDUMMYP1)*p1(iDUMMY1) )/p1.p2 ) *
( -d_(iDUMMYP2,iDUMMY2) + ( p2(iDUMMYP2)*p3(iDUMMY2)+p3(iDUMMYP2)*p2(iDUMMY2) )/p2.p3 ) *
( -d_(iDUMMYP3,iDUMMY3) + ( p1(iDUMMYP3)*p3(iDUMMY3)+p3(iDUMMYP3)*p1(iDUMMY3) )/p1.p3 );

L proj1 = 
DenDim(d-3)*( 
2*p1.p3 * 1/2/p1.p2 * 1/2/p2.p3 * d_(iDUMMYP1,iDUMMYP2)*p2(iDUMMYP3) 
- 1/2/p1.p2 * 1/2/p2.p3 * p3(iDUMMYP1)*p1(iDUMMYP2)*p2(iDUMMYP3)  
) * spinsum * ProjLabel1;

L proj2 = 
DenDim(d-3)*( 
2*p2.p3 * 1/2/p1.p2 * 1/2/p1.p3 * d_(iDUMMYP1,iDUMMYP3)*p1(iDUMMYP2) 
- 1/2/p1.p2 * 1/2/p1.p3 * p3(iDUMMYP1)*p1(iDUMMYP2)*p2(iDUMMYP3)  
) * spinsum * ProjLabel2;

L proj3 = 
DenDim(d-3)*( 
2*p1.p2 * 1/2/p1.p3 * 1/2/p2.p3 * d_(iDUMMYP2,iDUMMYP3)*p3(iDUMMYP1) 
- 1/2/p1.p3 * 1/2/p2.p3 * p3(iDUMMYP1)*p1(iDUMMYP2)*p2(iDUMMYP3)  
) * spinsum * ProjLabel3;

L proj4 = 
DenDim(d-3)*(
 - 1/2/p1.p2 * 1/2/p2.p3 * d_(iDUMMYP1,iDUMMYP2)*p2(iDUMMYP3)
 - 1/2/p1.p2 * 1/2/p1.p3 * d_(iDUMMYP1,iDUMMYP3)*p1(iDUMMYP2)
 - 1/2/p1.p3 * 1/2/p2.p3 * d_(iDUMMYP2,iDUMMYP3)*p3(iDUMMYP1)
 + Dim(d) * 1/2/p1.p2 * 1/2/p1.p3 * 1/2/p2.p3 * p3(iDUMMYP1)*p1(iDUMMYP2)*p2(iDUMMYP3)
) * spinsum * ProjLabel4;

L allproj = proj1+proj2+proj3+proj4;
.sort

*L test1 = amplitude*proj1;
*L test2 = amplitude*proj2;
*L test3 = amplitude*proj3;
*L test4 = amplitude*proj4;
*.sort

* Insert kinematics
id p1.p1 = 0;
id p2.p2 = 0;
id p3.p3 = 0;
id p1.p2 = ProjNum(p1.p2);
id p1.p3 = ProjNum(p1.p3);
id p2.p3 = ProjNum(p2.p3);
id p1.p2^-1 = ProjDen(p1.p2);
id p1.p3^-1 = ProjDen(p1.p3);
id p2.p3^-1 = ProjDen(p2.p3);
.sort

Repeat Id ProjDen(sDUMMY1?)*ProjDen(sDUMMY2?) = ProjDen(sDUMMY1*sDUMMY2);

*Repeat id sDUMMY1?!{,ProjLabel1,ProjLabel2,ProjLabel3, ProjLabel4,d} = prf(sDUMMY1,1);
*Repeat id sDUMMY1?!{ProjLabel1,ProjLabel2,ProjLabel3, ProjLabel4,d}^-1 = prf(1,sDUMMY1);
*.sort

*PolyRatFun prf;
*.sort


*B ProjLabel1,ProjLabel2,ProjLabel3, ProjLabel4;

B d_,p1,p2,p3;

print+s allproj;
.end
