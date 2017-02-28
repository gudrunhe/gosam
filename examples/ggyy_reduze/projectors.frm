#-
Symbols dimS;
Dimension dimS;

Indices mu,nu,rho,sigma;
S k,l,s,u,t,es12,es23,Projlabel1,Projlabel2,Projlabel3;
CF Pmunu,Rmu,H,A1,A2,A3;
CF B1,B2,B3,B4,B5,B6;
CFunctions Projector;
CFunctions inp, inplorentz, inpcolor;
Indices iDUMMY1, ..., iDUMMY5;
Vectors k1, k2, k3, k4;
CFunction DenDim;
Symbols dimD;
CFunction SCREEN;
AutoDeclare Symbols Proj;
Symbols sDUMMY1;
CFunction Den, prf;

.global 

nwrite statistics;

* D dimensional Binoth/Glover/Marquard/Bij projectors
* first projector corresponds to A_1
* second projector corresponds to B^1_11
* third projector corresponds to C_2111

g res= inplorentz(2,iDUMMY1,k1,0)*
  inplorentz(2,iDUMMY2,k2,0)*
  inplorentz(2,iDUMMY3,k3,0)*
  inplorentz(2,iDUMMY4,k4,0);

id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)*
inplorentz(2,iDUMMY3?,k3,0)*
inplorentz(2,iDUMMY4?,k4,0) =
ProjLabel1*
   A1(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4)
+ ProjLabel2*
   B1(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,1,1) 
+ ProjLabel3*
( 
   Rmu(2,iDUMMY1)*Rmu(1,iDUMMY2)*Rmu(1,iDUMMY3)*Rmu(1,iDUMMY4)
   - 2*(
	+ H(2,1)*B1(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,1,1)
	+ H(2,1)*B2(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,1,1) 
	+ H(2,1)*B3(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,1,1) 
	+ H(1,1)*B4(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,2,1) 
	+ H(1,1)*B5(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,2,1) 
	+ H(1,1)*B6(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4,2,1)
	)
   - 4*(
	+ H(2,1)*H(1,1)*A1(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4)
	+ H(2,1)*H(1,1)*A2(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4)
	+ H(2,1)*H(1,1)*A3(iDUMMY1,iDUMMY2,iDUMMY3,iDUMMY4)
	)
 );



*argument Projector;
id B1(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(mu,nu)*Rmu(k,rho)*Rmu(l,sigma)
  - 2*H(k,l)*A1(mu,nu,rho,sigma);

id B2(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(mu,rho)*Rmu(k,nu)*Rmu(l,sigma)
  - 2*H(k,l)*A2(mu,nu,rho,sigma);

id B3(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(mu,sigma)*Rmu(k,nu)*Rmu(l,rho)
  - 2*H(k,l)*A3(mu,nu,rho,sigma);

id B4(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(nu,rho)*Rmu(k,mu)*Rmu(l,sigma)
  - 2*H(k,l)*A3(mu,nu,rho,sigma);

id B5(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(nu,sigma)*Rmu(k,mu)*Rmu(l,rho)
  - 2*H(k,l)*A2(mu,nu,rho,sigma);

id B6(mu?,nu?,rho?,sigma?,k?,l?) = 
  + DenDim(dimS-3)*Pmunu(rho,sigma)*Rmu(k,mu)*Rmu(l,nu)
  - 2*H(k,l)*A1(mu,nu,rho,sigma);
*endargument;
.sort

*argument Projector;
id A1(mu?,nu?,rho?,sigma?) = 
  DenDim(dimS-1)*DenDim(dimS-3)*
  DenDim(dimS-4)*(
		  + (dimS-2)*Pmunu(mu,nu)*Pmunu(rho,sigma)
		  - Pmunu(mu,rho)*Pmunu(nu,sigma) 
		  - Pmunu(mu,sigma)*Pmunu(nu,rho)
		  );

id A2(mu?,nu?,rho?,sigma?) = 
  DenDim(dimS-1)*DenDim(dimS-3)*
  DenDim(dimS-4)*(
		  - Pmunu(mu,nu)*Pmunu(rho,sigma)
		  + (dimS-2)*Pmunu(mu,rho)*Pmunu(nu,sigma) 
		  - Pmunu(mu,sigma)*Pmunu(nu,rho)
		  );

id A3(mu?,nu?,rho?,sigma?) = 
  DenDim(dimS-1)*DenDim(dimS-3)*
  DenDim(dimS-4)*(
		  - Pmunu(mu,nu)*Pmunu(rho,sigma)
		  - Pmunu(mu,rho)*Pmunu(nu,sigma) 
		  + (dimS-2)*Pmunu(mu,sigma)*Pmunu(nu,rho)
		  );
*endargument;
.sort

*argument Projector;
id Pmunu(mu?,nu?) = d_(mu,nu) - (
			     k1(mu)*k1(nu)*2*H(1,1) +
			     k2(mu)*k1(nu)*2*H(2,1) +
			     k3(mu)*k1(nu)*2*H(3,1) +
			     k1(mu)*k2(nu)*2*H(1,2) +
			     k2(mu)*k2(nu)*2*H(2,2) +
			     k3(mu)*k2(nu)*2*H(3,2) +
			     k1(mu)*k3(nu)*2*H(1,3) +
			     k2(mu)*k3(nu)*2*H(2,3) +
			     k3(mu)*k3(nu)*2*H(3,3) 
			     );
*endargument;
.sort

*argument Projector; 
id Rmu(k?,mu?) = 2*(H(k,1)*k1(mu) + H(k,2)*k2(mu) + H(k,3)*k3(mu));
*endargument;
.sort

*argument Projector; 
*id H(1,1) = (1/s+1/u)/2;
*id H(1,2) = 1/s/2;
*id H(1,3) = 1/u/2;
*id H(2,1) = 1/s/2;
*id H(2,2) = (1/s+1/t)/2;
*id H(2,3) = 1/t/2;
*id H(3,1) = 1/u/2;
*id H(3,2) = 1/t/2;
*id H(3,3) = (1/t+1/u)/2;

id H(1,1) = es23/2/es12/(es12 + es23);
id H(1,2) = 1/es12/2;
id H(1,3) = -1/2/(es12 + es23);
id H(2,1) = 1/es12/2;
id H(2,2) = (es12 + es23)/2/es12/es23;
id H(2,3) = 1/es23/2;
id H(3,1) = -1/2/(es12 + es23);
id H(3,2) = 1/es23/2;
id H(3,3) = es12/es23/2/(es12 + es23);
*endargument;
.sort

b DenDim,ProjLabel,H;

print res;
.sort

#write <projectors.hh> "id inplorentz(2,iDUMMY1?,k1,0)*
inplorentz(2,iDUMMY2?,k2,0)* inplorentz(2,iDUMMY3?,k3,0)*
inplorentz(2,iDUMMY4?,k4,0) = %e",res;

.end

*argument Projector; 
id s=es12;
id 1/s=1/es12;
id t=es23;
id 1/t=1/es23;
id u=-es12-es23;
id 1/u=-1/(es12+es23);
*endargument;


.sort

L matrixelementsq = res*res;

id k1.k1=0;
id k1.k2=es12/2;
id k1.k3=-(es12+es23)/2;
id k2.k2=0;
id k2.k3=es23/2;
id k3.k3=0;

.sort

Denominators Den;
.sort
Repeat Id DenDim(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id Den(sDUMMY1?) = prf(1,sDUMMY1);
Repeat Id sDUMMY1?!{ProjLabel1,ProjLabel2,ProjLabel3} = prf(sDUMMY1,1);
Repeat Id  sDUMMY1?^(-1) = prf(1,sDUMMY1);
.sort

PolyRatFun prf;
.sort
PolyRatFun;
.sort

B ProjLabel1, ProjLabel2, ProjLabel3;

print;
.end
