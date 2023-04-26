* vim: syntax=form
*-----------------------------------------------------
*
* This file has been generated automatically
* by "qgraf-3.4.2" using the Feynman rules of the
* model "UFO_modHEFT".
* The file results from the following "qgraf.dat":
*
*---------- <qgraf.dat> ------------------------------
* output = 'diagrams-0.hh';
* style = 'form.sty';
* model = 'model';
* in = part21[k1], part21[k2];
* out = part5000000[k3], part5000000[k4];
* loops=0;
* loop_momentum=p;
* options=onshell, notadpole, nosnail;
* true=chord[part22,part23,part24,part5000000,0,0];
* true=vsum[QQ,4,4];
*
*---------- END OF <qgraf.dat> -----------------------
*--#[diagrams:

*--#[ diagram1:
*
Local diagram1 =
  QGRAFSIGN(+1) * PREFACTOR(1) *
   inp([field.part21], k1) *
   inplorentz(+2, iv1r1L2, k1, 0) *
   inpcolor(1, iv1r1C8) *
   inp([field.part21], k2) *
   inplorentz(+2, iv1r2L2, k2, 0) *
   inpcolor(2, iv1r2C8) *
   out([field.part5000000], k3) *
   outlorentz(+0, iv1r3L0, k3, mdlMh) *
   outcolor(1, iv1r3C1) *
   out([field.part5000000], k4) *
   outlorentz(+0, iv1r4L0, k4, mdlMh) *
   outcolor(2, iv1r4C1) *
   vertex(iv1,
      [field.part21], idx1r1, +2, k1+ZERO, iv1r1L2, +8, iv1r1C8,
      [field.part21], idx1r2, +2, k2+ZERO, iv1r2L2, +8, iv1r2C8,
      [field.part5000000], idx1r3, +0, -k3+ZERO, iv1r3L0, +1, iv1r3C1,
      [field.part5000000], idx1r4, +0, -k4+ZERO, iv1r4L0, +1, iv1r4C1)
;
*--#] diagram1:
*--#[ diagram2:
*
Local diagram2 =
  QGRAFSIGN(+1) * PREFACTOR(1) *
   inp([field.part21], k1) *
   inplorentz(+2, iv1r1L2, k1, 0) *
   inpcolor(1, iv1r1C8) *
   inp([field.part21], k2) *
   inplorentz(+2, iv1r2L2, k2, 0) *
   inpcolor(2, iv1r2C8) *
   out([field.part5000000], k3) *
   outlorentz(+0, iv2r1L0, k3, mdlMh) *
   outcolor(1, iv2r1C1) *
   out([field.part5000000], k4) *
   outlorentz(+0, iv2r2L0, k4, mdlMh) *
   outcolor(2, iv2r2C1) *
   vertex(iv1,
      [field.part21], idx1r1, +2, k1+ZERO, iv1r1L2, +8, iv1r1C8,
      [field.part21], idx1r2, +2, k2+ZERO, iv1r2L2, +8, iv1r2C8,
      [field.part5000000], idx1r3, +0, -k1-k2+ZERO, iv1r3L0, +1, iv1r3C1) *
   vertex(iv2,
      [field.part5000000], idx2r1, +0, -k3+ZERO, iv2r1L0, +1, iv2r1C1,
      [field.part5000000], idx2r2, +0, -k4+ZERO, iv2r2L0, +1, iv2r2C1,
      [field.part5000000], idx2r3, +0, k1+k2+ZERO, iv2r3L0, +1, iv2r3C1) *
   propcolor(+1, iv2r3C1, iv1r3C1) *
   proplorentz(+0, -k1-k2+ZERO, mdlMh, mdlWh, +0, iv2r3L0, iv1r3L0)
;
*--#] diagram2:
*
* END OF DIAGRAMS
*
*--#]diagrams:
*--#[global:

#define DIAGRAMCOUNT "2"

*--#]global:


