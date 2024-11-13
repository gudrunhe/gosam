* vim: syntax=form:expandtab:ts=3:sw=3

#Procedure ReplaceYukawas
*---#[ identify Yukawa vertices:
* NOTE: This assumes that the structure of the vertex will always be
* quark-antiquark-Higgs or antiquark-quark-Higgs; i.e. the Higgs is
* always the third particle. If the order parameter 'NP' is present
* in an UFO model, qqH vertices with NP!=0 (i.e. new-physics vertices)
* will not be considered as Yukawa vertices. For those the user needs
* to supply the correct counterterms as part of the UFO model.
*
[% @for modelparticles massive quarks OSyukawa %]
id vertex(iv?,[% @if is_ufo %] isCT?, isNP0, RK?, [% @for ordernames %][% name %]?, [% @end @for %][% @end @if %]
	  [field.[% name %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% antiname %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% modelhiggs %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, isNP0, RK, [% @for ordernames %][% name %], [% @end @for %][% @end @if %]
	  [field.[% name %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% antiname %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% modelhiggs %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+XCT*CYUKAWA*DELTAYUKOS[% mass %]);
id vertex(iv?,[% @if is_ufo %] isCT?, isNP0, RK?, [% @for ordernames %][% name %]?, [% @end @for %][% @end @if %]
	  [field.[% antiname %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% name %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% modelhiggs %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, isNP0, RK, [% @for ordernames %][% name %], [% @end @for %][% @end @if %]
	  [field.[% antiname %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% name %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% modelhiggs %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+XCT*CYUKAWA*DELTAYUKOS[% mass %]);[%
@end @for %][% 
@for modelparticles quarks MSbaryukawa %]
id vertex(iv?,[% @if is_ufo %] isCT?, isNP0, RK?, [% @for ordernames %][% name %]?, [% @end @for %][% @end @if %]
	  [field.[% name %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% antiname %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% modelhiggs %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, isNP0, RK, [% @for ordernames %][% name %], [% @end @for %][% @end @if %]
	  [field.[% name %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% antiname %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% modelhiggs %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+XCT*CYUKAWA*DELTAYUKMSbar);
id vertex(iv?,[% @if is_ufo %] isCT?, isNP0, RK?, [% @for ordernames %][% name %]?, [% @end @for %][% @end @if %]
	  [field.[% antiname %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% name %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% modelhiggs %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, isNP0, RK, [% @for ordernames %][% name %], [% @end @for %][% @end @if %]
	  [field.[% antiname %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% name %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% modelhiggs %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+XCT*CYUKAWA*DELTAYUKMSbar);[%
@end @for %]

*---#] identify Yukawa vertices:
*---#[ identify massive quark propagators and take derivative wrt. mass:
[% @for modelparticles massive quarks %][%
@if eval width .eq. 0 %]
id proplorentz(1, vDUMMY1?, [% mass %], 0, 0, iv1L?, iv2L?) =
   proplorentz(1, vDUMMY1, [% mass %], 0, 0, iv1L, iv2L) -
       i_*XCT*CMASS*DELTAMASSOS[% mass %] * 
	      proplorentz(1, vDUMMY1, [% mass %], 0, 0, iv1L, iDUMMY1) *
		  proplorentz(1, vDUMMY1, [% mass %], 0, 0, iDUMMY1, iv2L);
id proplorentz(1, ZERO, [% mass %], 0, 0, iv1L?, iv2L?) =
   proplorentz(1, ZERO, [% mass %], 0, 0, iv1L, iv2L) -
       i_*XCT*CMASS*DELTAMASSOS[% mass %] * 
	      proplorentz(1, ZERO, [% mass %], 0, 0, iv1L, iDUMMY1) *
		  proplorentz(1, ZERO, [% mass %], 0, 0, iDUMMY1, iv2L);[%
@else %]
id proplorentz(1, vDUMMY1?, [% mass %], [% width %], 0, iv1L?, iv2L?) =
   proplorentz(1, vDUMMY1, [% mass %], [% width %], 0, iv1L, iv2L) -
       i_*XCT*CMASS*DELTAMASSOS[% mass %] * 
	      proplorentz(1, vDUMMY1, [% mass %], [% width %], 0, iv1L, iDUMMY1) *
		  proplorentz(1, vDUMMY1, [% mass %], [% width %], 0, iDUMMY1, iv2L);
id proplorentz(1, ZERO, [% mass %], [% width %], 0, iv1L?, iv2L?) =
   proplorentz(1, ZERO, [% mass %], [% width %], 0, iv1L, iv2L) -
       i_*XCT*CMASS*DELTAMASSOS[% mass %] * 
	      proplorentz(1, ZERO, [% mass %], [% width %], 0, iv1L, iDUMMY1) *
		  proplorentz(1, ZERO, [% mass %], [% width %], 0, iDUMMY1, iv2L);[% 
@end @if %]
[% @end @for %]
*---#] identify massive quark propagators and take derivative wrt. mass:
*---#[ truncate at linear order in CT constant:

Multiply (1-XCT);
id XCT^2 = XCT2;
id XCT2 = 0;

*---#] truncate at linear order in CT constant:
#EndProcedure
