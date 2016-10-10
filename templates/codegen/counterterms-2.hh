
.sort
Symbols deltaZmm2,deltaZmm1,deltaZm0;

Id deltaZm(2,mT?) = prf(mT,1)*(
                               prf(deltaZmm2,1)*epsS^(-2)
                               +prf(deltaZmm1,1)*epsS^(-1)
                               +prf(deltaZm0 ,1)
                              );
