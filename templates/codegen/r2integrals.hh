#procedure ReduceR2N1(r1,m1sq)
Id only eps * ptens =
 - 1/2*(fDUMMY1(1,1));

Id only eps * ptens(iDUMMY1?) =
1/2*(vDUMMY1(iDUMMY1))*(fDUMMY1(1,1));

Id fDUMMY1(1, 1) = - 2 * (`m1sq');
Id vDUMMY1 = `r1';
Argument;
   Id vDUMMY1 = `r1';
EndArgument;
Id only Qt2 * ptens =
 'm1sq'^2/2;
#endprocedure


#procedure ReduceR2N2(r1,m1sq,r2,m2sq)
Id only eps * ptens =
1;

Id only eps * ptens(iDUMMY1?) =
 - 1/2*(vDUMMY1(iDUMMY1) + vDUMMY2(iDUMMY1));

Id only eps * ptens(iDUMMY1?, iDUMMY2?) =
1/6*(2*vDUMMY1(iDUMMY1)*vDUMMY1(iDUMMY2) + vDUMMY1(iDUMMY1)*vDUMMY2(iDUMMY2)
       + vDUMMY1(iDUMMY2)*vDUMMY2(iDUMMY1) + 2*vDUMMY2(iDUMMY1)*
      vDUMMY2(iDUMMY2)) - 1/12*(d_(iDUMMY1,iDUMMY2))*(fDUMMY1(1,1) + fDUMMY1(1
      ,2) + fDUMMY1(2,2));

Id only Qt2 * ptens =
 - 1/6*(fDUMMY1(1,1) + fDUMMY1(1,2) + fDUMMY1(2,2));


Id fDUMMY1(1, 1) = - 2 * (`m1sq');
Id fDUMMY1(1, 2) =
 + vDUMMY1.vDUMMY1 + vDUMMY2.vDUMMY2 - 2 * vDUMMY1.vDUMMY2
 - (`m1sq') - (`m2sq');
Id fDUMMY1(2, 2) = - 2 * (`m2sq');


Id only Qt2 * ptens(iDUMMY1?) =
 1/12*(vDUMMY2(iDUMMY1) - vDUMMY1(iDUMMY1))*(fDUMMY1(1,1) + fDUMMY1(1,2));

Id fDUMMY1(1, 1) =
  + vDUMMY1.vDUMMY1 + vDUMMY2.vDUMMY2 - 2 * vDUMMY1.vDUMMY2;
Id fDUMMY1(1, 2) =  - 2*(`m1sq') - 4*(`m2sq');

Id vDUMMY1 = `r1';
Id vDUMMY2 = `r2';

Argument;
   Id vDUMMY1 = `r1';
   Id vDUMMY2 = `r2';
EndArgument;


#endprocedure


#procedure ReduceR2N3(r1,m1sq,r2,m2sq,r3,m3sq)
Id only eps * ptens =
 0;

Id only eps * ptens(iDUMMY1?) =
 0;

Id only eps * ptens(iDUMMY1?, iDUMMY2?) =
1/4*(d_(iDUMMY1,iDUMMY2));

Id only Qt2 * ptens =
1/2;

Id only eps * ptens(iDUMMY1?, iDUMMY2?, iDUMMY3?) =
 - 1/12*(d_(iDUMMY1,iDUMMY2)*vDUMMY1(iDUMMY3) + d_(iDUMMY1,iDUMMY2)*
      vDUMMY2(iDUMMY3) + d_(iDUMMY1,iDUMMY2)*vDUMMY3(iDUMMY3) + 
      d_(iDUMMY1,iDUMMY3)*vDUMMY1(iDUMMY2) + d_(iDUMMY1,iDUMMY3)*
      vDUMMY2(iDUMMY2) + d_(iDUMMY1,iDUMMY3)*vDUMMY3(iDUMMY2) + 
      d_(iDUMMY2,iDUMMY3)*vDUMMY1(iDUMMY1) + d_(iDUMMY2,iDUMMY3)*
      vDUMMY2(iDUMMY1) + d_(iDUMMY2,iDUMMY3)*vDUMMY3(iDUMMY1));

Id only Qt2 * ptens(iDUMMY1?) =
 - 1/6*(vDUMMY1(iDUMMY1) + vDUMMY2(iDUMMY1) + vDUMMY3(iDUMMY1));


Id only Qt2^2 * ptens =
  1/6*fDUMMY1(1,1);


Id only Qt2 * ptens(iDUMMY1?, iDUMMY2?) =
 -1/12*fDUMMY1(1,1) * d_(iDUMMY1,iDUMMY2)
 +1/24*( 2*vDUMMY1(iDUMMY1)*vDUMMY1(iDUMMY2)
       + 2*vDUMMY2(iDUMMY1)*vDUMMY2(iDUMMY2)
       + 2*vDUMMY3(iDUMMY1)*vDUMMY3(iDUMMY2)
       +   vDUMMY1(iDUMMY1)*vDUMMY2(iDUMMY2)
       +   vDUMMY1(iDUMMY2)*vDUMMY2(iDUMMY1)
       +   vDUMMY1(iDUMMY1)*vDUMMY3(iDUMMY2)
       +   vDUMMY1(iDUMMY2)*vDUMMY3(iDUMMY1)
       +   vDUMMY2(iDUMMY1)*vDUMMY3(iDUMMY2)
       +   vDUMMY2(iDUMMY2)*vDUMMY3(iDUMMY1));



Id fDUMMY1(1, 1) =
 + 1/2*(vDUMMY1.vDUMMY1 + vDUMMY2.vDUMMY2 + vDUMMY3.vDUMMY3
      - vDUMMY1.vDUMMY2 - vDUMMY2.vDUMMY3 - vDUMMY1.vDUMMY3)
  - (`m1sq') - (`m2sq') - (`m3sq');




Id vDUMMY1 = `r1';
Id vDUMMY2 = `r2';
Id vDUMMY3 = `r3';
Argument;
   Id vDUMMY1 = `r1';
   Id vDUMMY2 = `r2';
   Id vDUMMY3 = `r3';
EndArgument;
#endprocedure


#procedure ReduceR2N4(r1,r2,r3,r4)
Id only eps * ptens =
 0;

Id only eps * ptens(iDUMMY1?) =
 0;

Id only eps * ptens(iDUMMY1?, iDUMMY2?) =
 0;

Id only Qt2 * ptens =
 0;

Id only eps * ptens(iDUMMY1?, iDUMMY2?, iDUMMY3?) =
 0;

Id only Qt2 * ptens(iDUMMY1?) =
 0;

Id only eps * ptens(iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) =
1/24*(d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4) + d_(iDUMMY1,iDUMMY3)*
      d_(iDUMMY2,iDUMMY4) + d_(iDUMMY1,iDUMMY4)*d_(iDUMMY2,iDUMMY3));

Id only Qt2 * ptens(iDUMMY1?, iDUMMY2?) =
1/12*(d_(iDUMMY1,iDUMMY2));

Id only Qt2^2 * ptens =
 - 1/6;

Id only Qt2^2 * ptens(iDUMMY1?) =
  1/24*(vDUMMY1(iDUMMY1)+vDUMMY2(iDUMMY1)+vDUMMY3(iDUMMY1)+vDUMMY4(iDUMMY1)
);

Id only Qt2 * ptens(iDUMMY1?,iDUMMY2?,iDUMMY3?) =
  -1/48*((vDUMMY1(iDUMMY1)+vDUMMY2(iDUMMY1)+vDUMMY3(iDUMMY1)+vDUMMY4(iDUMMY1))*d_(iDUMMY2,iDUMMY3)
        +(vDUMMY1(iDUMMY2)+vDUMMY2(iDUMMY2)+vDUMMY3(iDUMMY2)+vDUMMY4(iDUMMY2))*d_(iDUMMY1,iDUMMY3)
        +(vDUMMY1(iDUMMY3)+vDUMMY2(iDUMMY3)+vDUMMY3(iDUMMY3)+vDUMMY4(iDUMMY3))*d_(iDUMMY1,iDUMMY2));


Id vDUMMY1 = `r1';
Id vDUMMY2 = `r2';
Id vDUMMY3 = `r3';
Id vDUMMY4 = `r4';
Argument;
   Id vDUMMY1 = `r1';
   Id vDUMMY2 = `r2';
   Id vDUMMY3 = `r3';
   Id vDUMMY4 = `r4';
EndArgument;

#endprocedure

#procedure ReduceR2N5

Id only Qt2 * ptens(iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) =
 1/96*(d_(iDUMMY1,iDUMMY2)*d_(iDUMMY3,iDUMMY4) + d_(iDUMMY1,iDUMMY3)*
       d_(iDUMMY2,iDUMMY4) + d_(iDUMMY1,iDUMMY4)*d_(iDUMMY2,iDUMMY3));

Id only Qt2^2 * ptens(iDUMMY1?, iDUMMY2?) =
 -1/48*(d_(iDUMMY1,iDUMMY2));

Id only Qt2^3 * ptens =
 1/12;

#endprocedure
