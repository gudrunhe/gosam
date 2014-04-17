* This file computes the square of the amplitude
* We use the symbols
*    CCO: off diagonal entries in the color correlation matrix
*    CDD: (CCO+CDD) is the diagonal entry in the color correlation matrix

Symbols CCO, CDD, T1234, T1324, T1243;
Symbols pi, alphas, NC;
CFunctions sI46, sI34, I24, R;
Symbols s,t,u, LO, NLO;
Symbols SP, DP, FI;
Symbols gs;
Symbols delta;
CFunction log, zlog, scale2;

.global

Global LO2 = LO * LO;
Global NLO2 = (2*pi/alphas) * 2 * LO * NLO;

Id LO = - 16 * pi * alphas / NC * (T1234*s/t+T1243*s/u+T1324*s^2/t/u);

Id NLO =  - 4 * alphas^2 * (
   + (s^2+t^2+u^2)^2/s/t/u/2 * T1324 * sI46(u,t)/s
   + 2 * s*u/t *               T1234 * sI46(s,t)/u
   + 2 * s*t/u *               T1243 * sI46(s,u)/t

   - 2 * (s^2/t * T1234 + s^2/u * T1243) * sI34(s)/s
   - 2 * (s * T1234 + s^2/u * T1324) * sI34(t)/t
   - 2 * (s * T1243 + s^2/t * T1324) * sI34(u)/u

   + ( - 11/3 * s/t * T1234 + (11/3 * s/t + (t-u)/s) * T1324) * I24(t)
   + ( - 11/3 * s/u * T1243 + (11/3 * s/u + (u-t)/s) * T1324) * I24(u)

   - ( s/t/9 * T1234 + s/u/9 * T1243 + (s^2/t/u/9 + 1) * T1324) * R()
);

Id T1234*T1234 = CCO + CDD;
Id T1243*T1243 = CCO + CDD;
Id T1324*T1324 = CCO + CDD;
Id T1234*T1324 = CCO;
Id T1234*T1243 = CCO;
Id T1324*T1243 = CCO;

.store

Local LOFI = LO2;
Local NLOFI = FI * NLO2;
Local NLOSP = SP * NLO2;
Local NLODP = DP * NLO2;

Id R * DP = 0;
Id R * SP = 0;
Id R * FI = 1;

Id I24(s?) * DP = 0;
Id I24(s?) * SP = 1;
Id I24(s?) * FI = 2 - zlog(-s, -1, scale2, 0);

Id sI34(s?) * DP = 1;
Id sI34(s?) * SP = - zlog(-s, -1, scale2, 0);
Id sI34(s?) * FI = 1/2 * zlog(-s, -1, scale2, 0)^2;

Id sI46(s?,t?) * DP = 0;
Id sI46(s?,t?) * SP = 0;
Id sI46(s?,t?) * FI = 1/2 * (zlog(s, 1, t, 1)^2 + pi^2);

If(count(CCO,1)) Id s = -u-t;

Id alphas = gs^2/4/pi;

Multiply dum_(s^2/t^2/u^2) * u^2 * t^2 / s^2;


Brackets CCO, CDD, dum_, gs, NC;
Print +s;

.sort

Id gs = 1;

ToPolynomial;
.sort

#do i=1,`EXTRASYMBOLS_'
   #write<square.txt>  "Z`i'_ = %`i'x;"
#enddo

#write<square.txt> "res0 = %e", LOFI
#write<square.txt> "res1_0 = %e", NLOFI
#write<square.txt> "res1_1 = %e", NLOSP
#write<square.txt> "res1_2 = %e", NLODP

#write<square.in> "@language form -> fortran90;"
#write<square.in> "@type C = \"double complex\";"
#write<square.in> "@type R = \"double precision\";"
#write<square.in> "@operator R * R -> R;"
#write<square.in> "@operator C * C -> C;"
#write<square.in> "@coerce R -> C;"
#write<square.in> "@coerce @int -> R = \"%%s.0d0\";"
#write<square.in> "@coerce @int -> C = \"%%s.0d0\";"
#write<square.in> "@coerce @int/@int -> R = \"%%s.0d0/%%s.0d0\";"
#write<square.in> "@coerce @int/@int -> C = \"%%s.0d0/%%s.0d0\";"

#write<square.in> "@define zlog : R, R, R, R -> C;"
#write<square.in> "@define Z... : C;"
#write<square.in> "s,t,u,pi,CCO,CDD,NC,scale2 : R;"

#write<square.in> "@polynomial CCO, CDD, pi, s, t, u, NC;"
#do i=1,`EXTRASYMBOLS_'
   #write<square.in>  "@polynomial Z`i'_;"
#enddo
.end
