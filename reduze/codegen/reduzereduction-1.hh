id INT(ReduzeT1L1x12,1,1,1,0,[],1,0,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1x34,1,1,1,0,[],1,0,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1,1,2,1,0,[],0,1,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1x34,1,2,1,0,[],0,1,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1,1,4,1,0,[],0,0,1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1x34,1,4,1,0,[],0,0,1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1,2,3,2,0,[],1,1,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT1L1,2,3,2,1,[],1,1,-1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/4*(4*mT^2+dimS*es12-2*es12)*Den(mT)^2);

id INT(ReduzeT1L1,2,3,2,1,[],1,1,0,-1) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/4*Den(mT)^2*(2*es23-4*mT^2-dimS*(es23+mH^2)+2*mH^2));

id INT(ReduzeT1L1x34,2,3,2,0,[],1,1,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT1L1x34,2,3,2,1,[],1,1,0,-1) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/4*Den(mT)^2*(2*es23+4*mT^2-(es23-3*mH^2+es12)*dimS-6*mH^2+2*es12));

id INT(ReduzeT1L1,2,5,2,1,[],1,-1,1,0) = 
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-1/2*es12)
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1,2,5,2,1,[],1,0,1,-1) = 
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (mH^2-1/2*es12)
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1x34,2,5,2,0,[],1,0,1,0) = 
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (1);

id INT(ReduzeT1L1x34,2,5,2,1,[],1,-1,1,0) = 
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-1/2*es12)
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1x34,2,5,2,1,[],1,0,1,-1) = 
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (mH^2-1/2*es12)
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1);

id INT(ReduzeT1L1,2,6,2,0,[],0,1,1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT1L1,2,6,2,1,[],0,1,1,-1) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/4*Den(mT)^2*(2*es23-4*mT^2-dimS*(es23+mH^2)+2*mH^2));

id INT(ReduzeT1L1x34,2,6,2,0,[],0,1,1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT1L1x34,2,6,2,1,[],-1,1,1,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/4*(4*mT^2+dimS*es12-2*es12)*Den(mT)^2);

id INT(ReduzeT1L1x34,2,6,2,1,[],0,1,1,-1) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/4*Den(mT)^2*(2*es23+4*mT^2-(es23-3*mH^2+es12)*dimS-6*mH^2+2*es12));

id INT(ReduzeT1L1x12,2,9,2,0,[],1,0,0,1) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT1L1x34,2,9,2,0,[],1,0,0,1) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT1L1x34,2,10,2,0,[],0,1,0,1) = 
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * (1);

id INT(ReduzeT1L1,2,12,2,0,[],0,0,1,1) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT1L1x34,2,12,2,0,[],0,0,1,1) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT1L1,3,7,3,1,[],1,1,1,-1) = 
  + INT(ReduzeT1L1,3,7,3,0,[],1,1,1,0)
    * (es23)
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * ((2*es23-2*mH^2+es12)*Den(es12))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * ((2*es23-dimS*(es23-mH^2)-2*mH^2)*Den(mT)^2*Den(es12));

id INT(ReduzeT1L1,3,7,3,2,[],1,1,1,-2) = 
  + INT(ReduzeT1L1,3,7,3,0,[],1,1,1,0)
    * ((4*(mT^2*es12-2*mH^2*mT^2)*es23+4*mH^4*mT^2+es23^2*dimS*es12+2*es23^2*(2*mT^2-es12))*Den(dimS*es12-2*es12))
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-1/2*(8*mH^2*es12-12*mH^4-dimS*(4*mH^2*es12-4*mH^4-es12^2+4*es23^2)-2*es12^2+4*es23*(2*mH^2-es12)+4*es23^2)*Den(dimS*es12-2*es12))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(2*mT^2*es12+dimS*(2*es23*mH^2+mH^4-3*es23^2)-4*es23*mH^2-2*mH^4+6*es23^2)*Den(es12));

id INT(ReduzeT1L1x34,3,7,3,0,[],1,1,1,0) = 
  + INT(ReduzeT1L1,3,7,3,0,[],1,1,1,0)
    * (1);

id INT(ReduzeT1L1x34,3,7,3,1,[],1,1,1,-1) = 
  + INT(ReduzeT1L1,3,7,3,0,[],1,1,1,0)
    * (-es23+2*mH^2-es12)
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-(2*es23-2*mH^2+es12)*Den(es12))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-Den(mT)^2*Den(es12)*(2*es23-dimS*(es23-mH^2+es12)-2*mH^2+2*es12));

id INT(ReduzeT1L1x34,3,7,3,2,[],1,1,1,-2) = 
  + INT(ReduzeT1L1,3,7,3,0,[],1,1,1,0)
    * (-Den(dimS*es12-2*es12)*((4*mH^2*es12^2+2*es23*(2*mH^2*es12-es12^2)-es23^2*es12-4*mH^4*es12-es12^3)*dimS-8*mH^2*es12^2-4*mH^4*mT^2+8*mH^4*es12+2*es12^3-2*es23^2*(2*mT^2-es12)+4*es23*(es12^2-(mT^2+2*mH^2)*es12+2*mH^2*mT^2)))
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-1/2*Den(dimS*es12-2*es12)*(dimS*(12*mH^2*es12-12*mH^4-3*es12^2+8*es23*(2*mH^2-es12)-4*es23^2)-24*mH^2*es12+20*mH^4+6*es12^2-12*es23*(2*mH^2-es12)+4*es23^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*Den(mT)^2*Den(es12)*(4*(5*mH^2-3*es12)*es23-dimS*(2*(5*mH^2-3*es12)*es23+10*mH^2*es12-7*mH^4-3*es12^2-3*es23^2)-14*mH^4-6*es12^2-2*(mT^2-10*mH^2)*es12-6*es23^2));

id INT(ReduzeT1L1,3,11,3,1,[],1,1,-1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (es23*Den(es23-mH^2)*es12)
  + INT(ReduzeT1L1,2,10,2,0,[],0,1,0,1)
    * (-Den(2*es23*mH^2-mH^4-es23^2)*(mH^4-2*es23*(mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (Den(2*es23*mH^2-mH^4-es23^2)*(mH^2*es12+es23*es12))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*Den(es23*mT^2-mH^2*mT^2)*(dimS*es12-2*es12));

id INT(ReduzeT1L1x12,3,11,3,1,[],1,1,-1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (-(2*mH^2*es12-es23*es12-es12^2)*Den(es23-mH^2+es12))
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * ((2*es23*mH^2-2*mH^2*es12-mH^4+es12^2-es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2)*(3*mH^2*es12-es23*es12-es12^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT^2*es12+es23*mT^2-mH^2*mT^2)*(dimS*es12-2*es12));

id INT(ReduzeT1L1x34,3,11,3,0,[],1,1,0,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT1L1x34,3,11,3,1,[],1,1,-1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (-(2*mH^2*es12-es23*es12-es12^2)*Den(es23-mH^2+es12))
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * ((2*es23*mH^2-2*mH^2*es12-mH^4+es12^2-es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2)*(3*mH^2*es12-es23*es12-es12^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT^2*es12+es23*mT^2-mH^2*mT^2)*(dimS*es12-2*es12));

id INT(ReduzeT1L1,3,13,3,1,[],1,-1,1,1) = 
  + INT(ReduzeT1L1,3,13,3,0,[],1,0,1,1)
    * (-(2*mH^4-es23*(2*mH^2-es12))*Den(4*mH^2-es12))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (2*(es23+mH^2)*Den(4*mH^2-es12))
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * (-(2*es23-2*mH^2+es12)*Den(4*mH^2-es12));

id INT(ReduzeT1L1x34,3,13,3,0,[],1,0,1,1) = 
  + INT(ReduzeT1L1,3,13,3,0,[],1,0,1,1)
    * (1);

id INT(ReduzeT1L1x34,3,13,3,1,[],1,-1,1,1) = 
  + INT(ReduzeT1L1,3,13,3,0,[],1,0,1,1)
    * (-(4*mH^2*es12-2*mH^4-es12^2+es23*(2*mH^2-es12))*Den(4*mH^2-es12))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (-2*(es23-3*mH^2+es12)*Den(4*mH^2-es12))
  + INT(ReduzeT1L1,2,5,2,0,[],1,0,1,0)
    * ((2*es23-2*mH^2+es12)*Den(4*mH^2-es12));

id INT(ReduzeT1L1,3,14,3,0,[],0,1,1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT1L1,3,14,3,1,[],-1,1,1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (es23*Den(es23-mH^2)*es12)
  + INT(ReduzeT1L1,2,10,2,0,[],0,1,0,1)
    * (-Den(2*es23*mH^2-mH^4-es23^2)*(mH^4-2*es23*(mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (Den(2*es23*mH^2-mH^4-es23^2)*(mH^2*es12+es23*es12))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*Den(es23*mT^2-mH^2*mT^2)*(dimS*es12-2*es12));

id INT(ReduzeT1L1x34,3,14,3,0,[],0,1,1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT1L1x34,3,14,3,1,[],-1,1,1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (-(2*mH^2*es12-es23*es12-es12^2)*Den(es23-mH^2+es12))
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * ((2*es23*mH^2-2*mH^2*es12-mH^4+es12^2-es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2)*(3*mH^2*es12-es23*es12-es12^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT^2*es12+es23*mT^2-mH^2*mT^2)*(dimS*es12-2*es12));

id INT(ReduzeT1L1x34,4,15,4,0,[],1,1,1,1) = 
  + INT(ReduzeT1L1x12,4,15,4,0,[],1,1,1,1)
    * (1);

id INT(ReduzeT2L1,2,3,2,0,[],1,1,0,0) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT2L1,2,5,2,0,[],1,0,1,0) = 
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * (1);

id INT(ReduzeT2L1,2,6,2,0,[],0,1,1,0) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT2L1,2,9,2,0,[],1,0,0,1) = 
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (1);

id INT(ReduzeT2L1,2,10,2,0,[],0,1,0,1) = 
  + INT(ReduzeT1L1,2,10,2,0,[],0,1,0,1)
    * (1);

id INT(ReduzeT2L1,2,12,2,0,[],0,0,1,1) = 
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (1/2*Den(mT)^2*(-2+dimS));

id INT(ReduzeT2L1,3,7,3,0,[],1,1,1,0) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT2L1,3,7,3,1,[],1,1,1,-1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * ((mH^4-es23*(2*mH^2-es12)+es23^2)*Den(es23-mH^2+es12))
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * (-(2*es23*mH^2-2*mH^2*es12-mH^4+es12^2-es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (-(mH^2*es12+mH^4-es23*(2*mH^2-es12)+es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*(2*es23-dimS*(es23-mH^2)-2*mH^2)*Den(mT^2*es12+es23*mT^2-mH^2*mT^2));

id INT(ReduzeT2L1,3,11,3,0,[],1,1,0,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT2L1,3,11,3,1,[],1,1,-1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (-(mH^4-es23*(2*mH^2-es12)+es23^2)*Den(es23-mH^2))
  + INT(ReduzeT1L1,2,10,2,0,[],0,1,0,1)
    * (Den(2*es23*mH^2-mH^4-es23^2)*(mH^4-2*es23*(mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (-Den(2*es23*mH^2-mH^4-es23^2)*(mH^2*es12+mH^4-es23*(2*mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*Den(es23*mT^2-mH^2*mT^2)*(2*es23-dimS*(es23-mH^2+es12)-2*mH^2+2*es12));

id INT(ReduzeT2L1,3,13,3,0,[],1,0,1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT2L1,3,13,3,1,[],1,-1,1,1) = 
  + INT(ReduzeT1L1x12,3,11,3,0,[],1,1,0,1)
    * ((mH^4-es23*(2*mH^2-es12)+es23^2)*Den(es23-mH^2+es12))
  + INT(ReduzeT1L1x12,2,10,2,0,[],0,1,0,1)
    * (-(2*es23*mH^2-2*mH^2*es12-mH^4+es12^2-es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (-(mH^2*es12+mH^4-es23*(2*mH^2-es12)+es23^2)*Den(2*mH^2*es12-mH^4+2*es23*(mH^2-es12)-es12^2-es23^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*(2*es23-dimS*(es23-mH^2)-2*mH^2)*Den(mT^2*es12+es23*mT^2-mH^2*mT^2));

id INT(ReduzeT2L1,3,14,3,0,[],0,1,1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (1);

id INT(ReduzeT2L1,3,14,3,1,[],-1,1,1,1) = 
  + INT(ReduzeT1L1,3,11,3,0,[],1,1,0,1)
    * (-(mH^4-es23*(2*mH^2-es12)+es23^2)*Den(es23-mH^2))
  + INT(ReduzeT1L1,2,10,2,0,[],0,1,0,1)
    * (Den(2*es23*mH^2-mH^4-es23^2)*(mH^4-2*es23*(mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,2,9,2,0,[],1,0,0,1)
    * (-Den(2*es23*mH^2-mH^4-es23^2)*(mH^2*es12+mH^4-es23*(2*mH^2-es12)+es23^2))
  + INT(ReduzeT1L1,1,1,1,0,[],1,0,0,0)
    * (-1/2*Den(es23*mT^2-mH^2*mT^2)*(2*es23-dimS*(es23-mH^2+es12)-2*mH^2+2*es12));

