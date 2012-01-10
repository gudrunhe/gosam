#-
Off Statistics;

CFunction TI, GammaRat, SI, Prefactor, OtherFactor, P;
Indices iDUMMY1, ..., iDUMMY10;
Vectors vDUMMY1, ..., vDUMMY10;
Symbols N, alpha, beta, eps, j1, ..., j4, d, eta, rk;
CFunction R, Z, zTSz, Temp, fDUMMY1(symmetric);
Symbols z1, ..., z4;

.global

#Define MAXLEGS "4"
#Define FORMFILE "r2integrals.hh"

#Do N=1,`MAXLEGS'
   #Do R=0,`N'
      #Do alpha=0,{`R'/2}
         #If `alpha' == 0
            Local [TI(`N',0,1,`R')] = TI(`N',0,1,`R'
            #Do i=1,`R'
               , iDUMMY`i'
            #EndDo
            );
         #Else
            Local [TI(`N',`alpha',0,{`R'-2*`alpha'})] =
               TI(`N',`alpha',0,{`R'-2*`alpha'}
            #Do i=1,{`R'-2*`alpha'}
               , iDUMMY`i'
            #EndDo
            );
         #EndIf
      #EndDo
   #EndDo
#EndDo

* Prefactor: everything outside the sum over l
* OtherFactor everythin inside the sum over l
Id TI(N?, alpha?, beta?, rk?, ?indices) =
   Prefactor(alpha, beta, rk) * OtherFactor(N, alpha, rk, ?indices);

Id OtherFactor(N?, alpha?, 4, iDUMMY1?, iDUMMY2?, iDUMMY3?, iDUMMY4?) =
    + sum_(j1,1,N, sum_(j2,1,N, sum_(j3,1,N, sum_(j4,1,N,
         R(j1, iDUMMY1) * R(j2, iDUMMY2) * R(j3, iDUMMY3) * R(j4, iDUMMY4) *
         (-1/2)^0 * SI(N, 2*alpha + 2*0, j1, j2, j3, j4)
      ))))
    + sum_(j1,1,N, sum_(j2,1,N,
         (
             + R(j1, iDUMMY1) * R(j2, iDUMMY2) * d_(iDUMMY3, iDUMMY4)
             + R(j1, iDUMMY1) * R(j2, iDUMMY3) * d_(iDUMMY2, iDUMMY4)
             + R(j1, iDUMMY1) * R(j2, iDUMMY4) * d_(iDUMMY2, iDUMMY3)
             + R(j1, iDUMMY2) * R(j2, iDUMMY3) * d_(iDUMMY1, iDUMMY4)
             + R(j1, iDUMMY2) * R(j2, iDUMMY4) * d_(iDUMMY1, iDUMMY3)
             + R(j1, iDUMMY3) * R(j2, iDUMMY4) * d_(iDUMMY1, iDUMMY2)
         ) * 
         (-1/2)^1 * SI(N, 2*alpha + 2*1, j1, j2)
      ))
    +    (
             + d_(iDUMMY1, iDUMMY2) * d_(iDUMMY3, iDUMMY4)
             + d_(iDUMMY1, iDUMMY3) * d_(iDUMMY2, iDUMMY4)
             + d_(iDUMMY1, iDUMMY4) * d_(iDUMMY2, iDUMMY3)
         ) *
         (-1/2)^2 * SI(N, 2*alpha + 2*2)
    ;

Id OtherFactor(N?, alpha?, 3, iDUMMY1?, iDUMMY2?, iDUMMY3?) =
    + sum_(j1,1,N, sum_(j2,1,N, sum_(j3,1,N,
         R(j1, iDUMMY1) * R(j2, iDUMMY2) * R(j3, iDUMMY3) *
         (-1/2)^0 * SI(N, 2*alpha + 2*0, j1, j2, j3)
      )))
    + sum_(j1,1,N,
         (
             + R(j1, iDUMMY1) * d_(iDUMMY2, iDUMMY3)
             + R(j1, iDUMMY2) * d_(iDUMMY1, iDUMMY3)
             + R(j1, iDUMMY3) * d_(iDUMMY1, iDUMMY2)
         ) * 
         (-1/2)^1 * SI(N, 2*alpha + 2*1, j1)
      )
    ;

Id OtherFactor(N?, alpha?, 2, iDUMMY1?, iDUMMY2?) =
    + sum_(j1,1,N, sum_(j2,1,N,
         R(j1, iDUMMY1) * R(j2, iDUMMY2) *
         (-1/2)^0 * SI(N, 2*alpha + 2*0, j1, j2)
      ))
    +    (
             + d_(iDUMMY1, iDUMMY2)
         ) * 
         (-1/2)^1 * SI(N, 2*alpha + 2*1)
    ;

Id OtherFactor(N?, alpha?, 1, iDUMMY1?) =
    + sum_(j1,1,N,
         R(j1, iDUMMY1) *
         (-1/2)^0 * SI(N, 2*alpha + 2*0, j1)
      )
    ;

Id OtherFactor(N?, alpha?, 0) =
         (-1/2)^0 * SI(N, 2*alpha + 2*0)
    ;


Id Prefactor(alpha?, beta?, rk?) =
   sign_(rk) * GammaRat(alpha) * eps^beta;
* GammaRat = Gamma(alpha - eps) / Gamma(-eps)
Id GammaRat(0) = 1;
Id GammaRat(alpha?) = - eps * fac_(alpha-1);

* d = 2*alpha + 2*l => eta = 2 + d/2 - N
Id eps * SI(N?, d?, ?tail) = Temp(N, 2 + d/2 - N, ?tail);

Id Temp(N?, eta?neg_, ?tail) = 0;

Id Temp(N?, eta?) =
   sign_(N) * invfac_(eta)/(2^eta) * zTSz(N)^eta *
   P(N);

Id Temp(N?, eta?, ?tail) =
   sign_(N) * invfac_(eta)/(2^eta) * zTSz(N)^eta *
   P(N) * Z(?tail);

ChainOut Z;
Id zTSz(N?) = sum_(j1,1,N,sum_(j2,1,N, Z(j1) * Z(j2) * fDUMMY1(j1, j2)));

#Do i=1,4
   Id R(`i', iDUMMY1?) = vDUMMY`i'(iDUMMY1);
   Id Z(`i') = z`i';
#EndDo

#Do i=1,4
   Id P(?all) * z`i'^d?pos_ = P(?all, d);
#EndDo

Repeat Id P(N?, j1?, ?tail) = fac_(j1) * P(N + j1, ?tail);
Id P(N?) = invfac_(N-1);

AntiBrackets d_, vDUMMY1, ..., vDUMMY4;
.sort
Collect dum_;
MakeInteger dum_;

AntiBrackets fDUMMY1;
.sort
Collect dum_;
MakeInteger dum_;

Id dum_(1) = 1;

.sort

#Do N=1,`MAXLEGS'
   #Switch `N'
   #Case 1
      #Write <`FORMFILE'> "#procedure ReduceR2N1(r1,m1sq)"
      #Break
   #Case 2
      #Write <`FORMFILE'> "#procedure ReduceR2N2(r1,m1sq,r2,m2sq)"
      #Break
   #Case 3
      #Write <`FORMFILE'> "#procedure ReduceR2N3(r1,r2,r3)"
      #Break
   #Case 4
      #Write <`FORMFILE'> "#procedure ReduceR2N4(r1,r2,r3,r4)"
      #Break
   #EndSwitch
   #Do R=0,`N'
      #Do alpha=0,{`R'/2}
         #If `alpha' == 0
            #Write <`FORMFILE'> "Id only eps * ptens%"
            #If `R' >= 1
               #Write <`FORMFILE'> "(iDUMMY1?%"
               #Do i=2,`R'
                  #Write <`FORMFILE'> ", iDUMMY`i'?%"
               #EndDo
               #Write <`FORMFILE'> ")%"
            #EndIf
            #Write <`FORMFILE'> " ="
            #Write <`FORMFILE'> "%e", [TI(`N',0,1,`R')]
         #Else
            #If `alpha' == 1
                #Write <`FORMFILE'> "Id only Qt2 * ptens%"
            #Else
                #Write <`FORMFILE'> "Id only Qt2^`alpha' * ptens%"
            #EndIf
            #If {`R'-2*`alpha'} >= 1
               #Write <`FORMFILE'> "(iDUMMY1?%"
               #Do i=2,{`R'-2*`alpha'}
                  #Write <`FORMFILE'> ", iDUMMY`i'?%"
               #EndDo
               #Write <`FORMFILE'> ")%"
            #EndIf
            #Write <`FORMFILE'> " ="
            #Write <`FORMFILE'> "%e", [TI(`N',`alpha',0,{`R'-2*`alpha'})]
         #EndIf
      #EndDo
   #EndDo
   #If `N' <= 2
      #Do i=1,`N'
         #Write <`FORMFILE'> "Id fDUMMY1(`i', `i') = - 2 * (\`m`i'sq\');"
         #Do j={`i'+1}, `N'
            #Write <`FORMFILE'> "Id fDUMMY1(`i', `j') ="
            #Write <`FORMFILE'> " + vDUMMY`i'.vDUMMY`i'%"
            #Write <`FORMFILE'> " + vDUMMY`j'.vDUMMY`j'%"
            #Write <`FORMFILE'> " - 2 * vDUMMY`i'.vDUMMY`j'"
            #Write <`FORMFILE'> " - (\`m`i'sq\') - (\`m`j'sq\');"
         #EndDo
      #EndDo
   #EndIf

   #Do i=1,`N'
      #Write <`FORMFILE'> "Id vDUMMY`i' = \`r`i'\';"
   #EndDo
   #Write <`FORMFILE'> "Argument;"
   #Do i=1,`N'
      #Write <`FORMFILE'> "   Id vDUMMY`i' = \`r`i'\';"
   #EndDo
   #Write <`FORMFILE'> "EndArgument;"

   #Write <`FORMFILE'> "#endprocedure"
#EndDo
.end
