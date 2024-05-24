* vim: syntax=form:expandtab:ts=3:sw=3

#Procedure ReplaceYukawas
*---#[ identify Yukawa vertices:
* NOTE: This assumes that the structure of the vertex will always be
* quark-antiquark-Higgs or antiquark-quark-Higgs; i.e. the Higgs is
* always the third particle. It will also register any qqH vertex
* (with massive q) as a Yukawa type vertex. In presence of anomalous
* qqH vertices one has to account for that in the corresponding EFT counterterm.
*
[% @for modelparticles massive quarks %]
id vertex(iv?,[% @if is_ufo %] isCT?, RK?, [% @if use_order_names %][% @for ordernames %][% name %]?, [% @end @for %][% @end @if %][% @end @if %]
	  [field.[% name %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% antiname %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% @if is_ufo %]part25[% @else %]H[% @end @if %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, RK, [% @if use_order_names %][% @for ordernames %][% name %], [% @end @for %][% @end @if %][% @end @if %]
	  [field.[% name %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% antiname %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% @if is_ufo %]part25[% @else %]H[% @end @if %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+CYUKAWA*(1+(LOGYUK[% mass %]-1)*RENLOG));
id vertex(iv?,[% @if is_ufo %] isCT?, RK?, [% @if use_order_names %][% @for ordernames %][% name %]?, [% @end @for %][% @end @if %][% @end @if %]
	  [field.[% antiname %]], idx1?, sDUMMY1?, vDUMMY1?, iv1L?, sign1?, iv1C?,
	  [field.[% name %]], idx2?, sDUMMY2?, vDUMMY2?, iv2L?, sign2?, iv2C?,
  	  [field.[% @if is_ufo %]part25[% @else %]H[% @end @if %]], idx3?, sDUMMY3?, vDUMMY3?, iv3L?, sign3?, iv3C?) =
   vertex(iv,[% @if is_ufo %] isCT, RK, [% @if use_order_names %][% @for ordernames %][% name %], [% @end @for %][% @end @if %][% @end @if %]
	  [field.[% antiname %]], idx1, sDUMMY1, vDUMMY1, iv1L, sign1, iv1C,
	  [field.[% name %]], idx2, sDUMMY2, vDUMMY2, iv2L, sign2, iv2C,
  	  [field.[% @if is_ufo %]part25[% @else %]H[% @end @if %]], idx3, sDUMMY3, vDUMMY3, iv3L, sign3, iv3C) *
   (1+CYUKAWA*(1+(LOGYUK[% mass %]-1)*RENLOG));[%
@end @for %]

*---#] identify Yukawa vertices:
*---#[ truncate at linear order in CT constant:

Multiply (1-CYUKAWA);
id CYUKAWA^2 = CYUKAWA2;
id CYUKAWA2 = 0;

*---#] truncate at linear order in CT constant:
#EndProcedure
