* vim: ts=3:sw=3

Id propcolor( 3, iv1?, iv2?) = d_(iv1, iv2);
Id propcolor(-3, iv1?, iv2?) = d_(iv1, iv2);
Id propcolor( 8, iv1?, iv2?) = d_(iv1, iv2);
Id propcolor( 1, iv1?, iv2?) = 1;
*---#[ Scalar Bosons :
Id proplorentz(0, k1?, m?, sDUMMY1?, 0, iv1?, iv2?) =
   PREFACTOR(i_) * inv(k1, m, sDUMMY1);
Id proplorentz(0, 0, m?, sDUMMY1?, 0,iv1?, iv2?) =
   PREFACTOR(i_) * inv(ZERO, m, sDUMMY1);
*---#] Scalar Bosons :
*---#[ Fermions :
Id proplorentz(1, k1?, m?, sDUMMY1?, 0, iv1?, iv2?) =
  PREFACTOR(i_) * (NCContainer(Sm(k1), iv2, iv1)
   + m * NCContainer(1, iv2, iv1)
  ) * inv(k1, m, sDUMMY1);
Id proplorentz(1, 0, m?, sDUMMY1?, 0, iv1?, iv2?) =
   + PREFACTOR(i_ * m) * NCContainer(1, iv2, iv1) * inv(ZERO, m, sDUMMY1);
Id proplorentz(1, k1?, 0, 0, 1, iv1?, iv2?) =
  PREFACTOR(i_) * NCContainer(Sm(k1)*ProjPlus, iv2, iv1) * inv(k1, 0);
Id proplorentz(1, k1?, 0, 0, -1, iv1?, iv2?) =
  PREFACTOR(i_) * NCContainer(Sm(k1)*ProjMinus, iv2, iv1) * inv(k1, 0);
*---#] Fermions :
*---#[ Gauge Bosons :
Id proplorentz(2, k1?, m?, sDUMMY1?, 0, iv1?, iv2?) =
   - PREFACTOR(i_) * d(iv1, iv2) * inv(k1, m, sDUMMY1);
Id proplorentz(2, 0, m?, sDUMMY1?, 0, iv1?, iv2?) =
   - PREFACTOR(i_) * d(iv1, iv2) * inv(ZERO, m, sDUMMY1);
*---#] Gauge Bosons :
*---#[ Vector-Spinor propagator :
Repeat;
   Id once proplorentz(3, k1?, m?, sDUMMY1?, 0, iv1?, iv2?) =
      PREFACTOR(i_) *
      SplitLorentzIndex(iv1, iv1L2, iv1L1) *
      SplitLorentzIndex(iv2, iv2L2, iv2L1) * 1/3 * (
         + 4*k1(iv1L2)*k1(iv2L2)/m
         - 3*d(iv1L2,iv2L2)*m
         + 2*NCContainer(Sm(k1),iv1L1,iv2L1)*k1(iv1L2)*k1(iv2L2)/m^2
         - 3*NCContainer(Sm(k1),iv1L1,iv2L1)*d(iv1L2,iv2L2)
         - NCContainer(Sm(k1)*Sm(iv2L2),iv1L1,iv2L1)*k1(iv1L2)/m
         + NCContainer(Sm(iv1L2),iv1L1,iv2L1)*k1(iv2L2)
         - NCContainer(Sm(iv1L2)*Sm(k1),iv1L1,iv2L1)*k1(iv2L2)/m
         - NCContainer(Sm(iv1L2)*Sm(k1)*Sm(iv2L2),iv1L1,iv2L1)
         + NCContainer(Sm(iv1L2)*Sm(iv2L2),iv1L1,iv2L1)*m
         + NCContainer(Sm(iv2L2),iv1L1,iv2L1)*k1(iv1L2)
      ) * inv(k1, m, sDUMMY1);
   Sum iv1L2, iv1L1, iv2L2, iv2L1;
EndRepeat;
*---#] Vector-Spinor propagator :
*---#[ Tensor Bosons :
Repeat;
   Id once proplorentz(4, k1?, m?, sDUMMY1?, 1, iv1?, iv2?) =
      - PREFACTOR(i_) *
        SplitLorentzIndex(iv1, iv1a, iv1b) *
        SplitLorentzIndex(iv2, iv2a, iv2b) *
        d(iv1a, iv2a) * d(iv1b, iv2b);
   Sum iv1a, iv1b, iv2a, iv2b;
   Id once proplorentz(4, k1?, m?, sDUMMY1?, 0, iv1?, iv2?) =
      SplitLorentzIndex(iv1, iv1a, iv1b) *
      SplitLorentzIndex(iv2, iv2a, iv2b) *
      (
         + 1/2 * (
            + d(iv1a, iv2a) * d(iv1b, iv2b)
            + d(iv1b, iv2a) * d(iv1a, iv2b)
            - d(iv1a, iv1b) * d(iv2a, iv2b)
         )
         - 1/2/m^2 * (
            + d(iv1a, iv2a) * k1(iv1b) * k1(iv2b)
            + d(iv1b, iv2a) * k1(iv1a) * k1(iv2b)
            + d(iv1a, iv2b) * k1(iv1b) * k1(iv2a)
            + d(iv1b, iv2b) * k1(iv1a) * k1(iv2a)
         )
         + 1/6 * (d(iv1a, iv1b) + 2*k1(iv1a)*k1(iv1b)/m^2) *
                 (d(iv2a, iv2b) + 2*k1(iv2a)*k1(iv2b)/m^2)
      ) * inv(k1, m, sDUMMY1);
   
EndRepeat;
*---#] Tensor Bosons :
