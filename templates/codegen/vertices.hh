* vim: ts=3:sw=3
*
* This file implements the vertices from Boehm, Denner, Joos,
* appendix A.2. The definition of the constants C has to be
* implemented in a model specific way elsewhere. The powers of
* the coupling constants e and g_s are left out.
*
* The cases are distinguished by the spin and the color of the
* particles.
*
* Note that the vertex functions with different particles
* assume a certain ordering which has to be obeyed in the
* qgraf model file.
*
* The Lorentz structures use the notation as defined in
* the spinney note:
*   d(mu, nu) = $g^{\mu\nu}$ (n-dimensional)
*
* The symbol f4(a,b,c,d) is used as f(a,b,x)*f(b,c,x) to avoid
* the extra index x at this point.
*
#Procedure ExpandVertices
*---#[ replace zero vectors :
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, 0, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?,
		field4?, idx4?, sDUMMY4?, vDUMMY4?, iv4L?, sign4?, iv4C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, ZERO, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C,
		field4, idx4, sDUMMY4, vDUMMY4, iv4L, sign4, iv4C);
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, 0, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?,
		field4?, idx4?, sDUMMY4?, vDUMMY4?, iv4L?, sign4?, iv4C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, ZERO, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C,
		field4, idx4, sDUMMY4, vDUMMY4, iv4L, sign4, iv4C);
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, 0, iv3L?, sign3?, iv3C?,
		field4?, idx4?, sDUMMY4?, vDUMMY4?, iv4L?, sign4?, iv4C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, ZERO, iv3L, sign3, iv3C,
		field4, idx4, sDUMMY4, vDUMMY4, iv4L, sign4, iv4C);
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?,
		field4?, idx4?, sDUMMY4?, 0, iv4L?, sign4?, iv4C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C,
		field4, idx4, sDUMMY4, ZERO, iv4L, sign4, iv4C);

id vertex(iv?,
		field1?, idx1?, sDUMMY1?, 0, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, ZERO, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C);
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, 0, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, ZERO, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C);
id vertex(iv?,
		field1?, idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
		field2?, idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
		field3?, idx3?, sDUMMY3?, 0, iv3L?, sign3?, iv3C?) =
	vertex(iv,
		field1, idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
		field2, idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
		field3, idx3, sDUMMY3, ZERO, iv3L, sign3, iv3C);
*---#] replace zero vectors :
*---#[ VVVV vertex (A.2.6) :
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?,
	field4?, idx4?, 2, vDUMMY4?, iv4L?, sign4?{-1,1}, iv4C?) =
		PREFACTOR(i_) * C(field1, field2, field3, field4) * 
			LorVVVV(iv1L, iv2L, iv3L, iv4L);
*---#] VVVV vertex (A.2.6) :
*---#[ VVVV vertex (QCD) (2.4.32) :
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, 8, iv3C?,
	field4?, idx4?, 2, vDUMMY4?, iv4L?, 8, iv4C?) =
		PREFACTOR(-i_) * C(field1, field2, field3, field4) * (
			+ LorVVVV2(iv1L,iv2L,iv3L,iv4L) * f4(iv1C, iv2C, iv3C, iv4C)
			+ LorVVVV2(iv1L,iv3L,iv4L,iv2L) * f4(iv1C, iv3C, iv4C, iv2C)
			+ LorVVVV2(iv1L,iv4L,iv2L,iv3L) * f4(iv1C, iv4C, iv2C, iv3C)
		);
*---#] VVVV vertex (QCD) (2.4.32) :
*---#[ VVV vertex (A.2.8) :
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) *
      LorVVV(vDUMMY1,vDUMMY2,vDUMMY3,iv1L,iv2L,iv3L);
*---#] VVV vertex (A.2.8) :
*---#[ VVV vertex (QCD) (2.4.32) :
* NOTE: Intentionally no i_
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, 8, iv3C?) =
		C(field1, field2, field3) *
      LorVVV(vDUMMY1,vDUMMY2,vDUMMY3,iv1L,iv2L,iv3L) *
		f(iv1C, iv2C, iv3C);
*---#] VVV vertex (QCD) (2.4.32) :
*---#[ SSSS vertex (A.2.10) :
id vertex(iv?,
	field1?, idx1?, 0, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 0, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?,
	field4?, idx4?, 0, vDUMMY4?, iv4L?, sign4?{-1,1}, iv4C?) =
		i_ * C(field1, field2, field3, field4);
*---#] SSSS vertex (A.2.10) :
*---#[ SSS vertex (A.2.12) :
id vertex(iv?,
	field1?, idx1?, 0, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 0, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3);
*---#] SSS vertex (A.2.12) :
*---#[ VVSS vertex (A.2.14) :
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?,
	field4?, idx4?, 0, vDUMMY4?, iv4L?, sign4?{-1,1}, iv4C?) =
		i_ * C(field1, field2, field3, field4) * d(iv1L, iv2L);
*---#] VVSS vertex (A.2.14) :
*---#[ VSS vertex (A.2.16) :
* Note: The momenta of (S1,S2) in the book correspond to (vDUMMY2,vDUMMY3) here.
* This determins the sign of C.
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 0, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) * (vDUMMY2(iv1L) - vDUMMY3(iv1L));
*---#] VSS vertex (A.2.16) :
*---#[ SVV vertex (A.2.18) :
id vertex(iv?,
	field1?, idx1?, 0, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) * d(iv2L, iv3L);
*---#] SVV vertex (A.2.18) :
*---#[ VFF vertex (A.2.20) :
id vertex(iv?,
	field1?, idx1?, -1, vDUMMY1?, iv1L?, -1, iv1C?,
	field2?, idx2?,  1, vDUMMY2?, iv2L?,  1, iv2C?,
	field3?, idx3?,  2, vDUMMY3?, iv3L?,  sign3?{-1,1}, iv3C?) = i_ * (
		+ 1/2 * (CR(field1, field2, field3) + CL(field1, field2, field3)) *
		  NCContainer(Sm(iv3L), iv1L, iv2L)
		+ (CR(field1, field2, field3) - CL(field1, field2, field3)) *
		  1/4 * (1 + 0*deltaaxial) * (
		  + NCContainer(Sm(iv3L) * Gamma5, iv1L, iv2L)
		  - NCContainer(Gamma5 * Sm(iv3L), iv1L, iv2L)
		  )
		);
id vertex(iv?,
	field1?, idx1?, -1, vDUMMY1?, iv1L?, -3, iv1C3?,
	field2?, idx2?,  1, vDUMMY2?, iv2L?,  3, iv2C3?,
	field3?, idx3?,  2, vDUMMY3?, iv3L?,  sign3?{-1,1}, iv3C1?) = i_ * (
		+ 1/2 * (CR(field1, field2, field3) + CL(field1, field2, field3)) *
		  NCContainer(Sm(iv3L), iv1L, iv2L)
		+ (CR(field1, field2, field3) - CL(field1, field2, field3)) *
		  1/4 * (1 + 2*deltaaxial) * (
		  + NCContainer(Sm(iv3L) * Gamma5, iv1L, iv2L)
		  - NCContainer(Gamma5 * Sm(iv3L), iv1L, iv2L)
		  )
		) * dcolor(iv1C3, iv2C3);
*---#] VFF vertex (A.2.20) :
*---#[ VFF vertex (QCD) (2.4.32) :
id vertex(iv?,
	field1?, idx1?, -1, vDUMMY1?, iv1L?, -3, iv1C3?,
	field2?, idx2?,  1, vDUMMY2?, iv2L?,  3, iv2C3?,
	field3?, idx3?,  2, vDUMMY3?, iv3L?,  8, iv3C8?) =
		PREFACTOR(i_) * C(field1, field2, field3) *
		NCContainer(Sm(iv3L), iv1L, iv2L) *
		T(iv3C8, iv1C3, iv2C3);
*---#] VFF vertex (QCD) (2.4.32) :
*---#[ SFF vertex (A.2.24) :
* TODO: Have a look at hep-ph/9302240 --> peudoscalar coupling might not be correct yet.
id vertex(iv?,
	field1?, idx1?, -1, vDUMMY1?, iv1L?, -1, iv1C1?,
	field2?, idx2?,  1, vDUMMY2?, iv2L?,  1, iv2C1?,
	field3?, idx3?,  0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C1?) = i_ * (
		+ CL(field1, field2, field3) *
		  NCContainer(ProjMinus, iv1L, iv2L)
		+ CR(field1, field2, field3) *
		  NCContainer(ProjPlus, iv1L, iv2L)
		+ (CR(field1, field2, field3) - CL(field1, field2, field3)) *
		  1/2 * 0*deltaaxial * NCContainer(Gamma5, iv1L, iv2L)
		);
id vertex(iv?,
	field1?, idx1?, -1, vDUMMY1?, iv1L?, -3, iv1C3?,
	field2?, idx2?,  1, vDUMMY2?, iv2L?,  3, iv2C3?,
	field3?, idx3?,  0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C1?) = i_ * (
		+ CL(field1, field2, field3) *
		  NCContainer(ProjMinus, iv1L, iv2L)
		+ CR(field1, field2, field3) *
		  NCContainer(ProjPlus, iv1L, iv2L)
		+ (CR(field1, field2, field3) - CL(field1, field2, field3)) *
		  1/2 * deltaaxial * NCContainer(Gamma5, iv1L, iv2L)
		) * dcolor(iv1C3, iv2C3);
*---#] SFF vertex (A.2.24) :
*---#[ VGG vertex (A.2.26) :
id vertex(iv?,
	field1?, idx1?,  0, vDUMMY1?, iv1L?, -1, iv1C?,
	field2?, idx2?,  0, vDUMMY2?, iv2L?,  1, iv2C?,
	field3?, idx3?,  2, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) * vDUMMY1(iv3L);
*---#] VGG vertex (A.2.26) :
*---#[ VGG vertex (QCD) (2.4.32) :
id vertex(iv?,
	field1?, idx1?,  0, vDUMMY1?, iv1L?, -8, iv1C?,
	field2?, idx2?,  0, vDUMMY2?, iv2L?,  8, iv2C?,
	field3?, idx3?,  2, vDUMMY3?, iv3L?,  8, iv3C?) =
		- C(field1, field2, field3) * f(iv3C, iv1C, iv2C) *
		  vDUMMY1(iv3L);
*---#] VGG vertex (QCD) (2.4.32) :
*---#[ SGG vertex (A.2.28) :
id vertex(iv?,
	field1?, idx1?,  0, vDUMMY1?, iv1L?, -1, iv1C?,
	field2?, idx2?,  0, vDUMMY2?, iv2L?,  1, iv2C?,
	field3?, idx3?,  0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3);
*---#] SGG vertex (A.2.28) :
*---#[ effective gg(g)(g)H(H):
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign1?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) * dcolor8(iv1C, iv2C) *
      ( d(iv1L, iv2L) * d(vDUMMY1, vDUMMY2)
		- d(vDUMMY2, iv1L) * d(vDUMMY1, iv2L));
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign1?{-1,1}, iv3C?
        field4?, idx4?, 0, vDUMMY4?, iv4L?, sign2?{-1,1}, iv4C?) =
		i_ * C(field1, field2, field3, field4) * dcolor8(iv1C, iv2C) *
      ( d(iv1L, iv2L) * d(vDUMMY1, vDUMMY2)
		- d(vDUMMY2, iv1L) * d(vDUMMY1, iv2L));      
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, 8, iv3C?,
   field4?, idx4?, 0, vDUMMY4?, iv4L?, sign1?{-1,1}, iv4C?) =
	  C(field1, field2, field3, field4) *
      LorVVV(vDUMMY1,vDUMMY2,vDUMMY3,iv1L,iv2L,iv3L) *
		f(iv1C, iv2C, iv3C);
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, 8, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, 8, iv2C?,
	field3?, idx3?, 2, vDUMMY3?, iv3L?, 8, iv3C?,
	field4?, idx4?, 2, vDUMMY4?, iv4L?, 8, iv4C?,
	field5?, idx5?, 0, vDUMMYA?, iv5L?, sign1?{-1,1}, iv5C?) =
		PREFACTOR(-i_) * C(field1, field2, field3, field4, field5) * (
			+ LorVVVV2(iv1L,iv2L,iv3L,iv4L) * f4(iv1C, iv2C, iv3C, iv4C)
			+ LorVVVV2(iv1L,iv3L,iv4L,iv2L) * f4(iv1C, iv3C, iv4C, iv2C)
			+ LorVVVV2(iv1L,iv4L,iv2L,iv3L) * f4(iv1C, iv4C, iv2C, iv3C)
		);
*---#] effective gg(g)(g)H(H):
*---#[ effective AAH:
id vertex(iv?,
	field1?, idx1?, 2, vDUMMY1?, iv1L?, sign1?{-1,1}, iv1C?,
	field2?, idx2?, 2, vDUMMY2?, iv2L?, sign2?{-1,1}, iv2C?,
	field3?, idx3?, 0, vDUMMY3?, iv3L?, sign3?{-1,1}, iv3C?) =
		i_ * C(field1, field2, field3) *
      ( d(iv1L, iv2L) * d(vDUMMY1, vDUMMY2)
		- d(vDUMMY2, iv1L) * d(vDUMMY1, iv2L));
*---#] effective AAH:      
#EndProcedure

#Procedure ExpandLorentzStructures
Id Once LorVVVV(iv1L?, iv2L?, iv3L?, iv4L?) =
			2 * d(iv1L, iv2L) * d(iv3L, iv4L)
			- d(iv2L, iv3L) * d(iv1L, iv4L)
			- d(iv1L, iv3L) * d(iv2L, iv4L)
;
Id once LorVVVV2(iv1L?, iv2L?, iv3L?, iv4L?) =
	d(iv1L, iv3L) * d(iv2L, iv4L) - d(iv1L, iv4L) * d(iv2L, iv3L);
Id once LorVVV(vDUMMY1?,vDUMMY2?,vDUMMY3?,iv1L?,iv2L?,iv3L?) =
			+ d(iv1L, iv2L) * (vDUMMY1(iv3L) - vDUMMY2(iv3L))
			+ d(iv2L, iv3L) * (vDUMMY2(iv1L) - vDUMMY3(iv1L))
			+ d(iv3L, iv1L) * (vDUMMY3(iv2L) - vDUMMY1(iv2L))
;
#EndProcedure
