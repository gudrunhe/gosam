* vim: ts=3:sw=3

*---#[ Scalars :
Id inplorentz(0, iv?, k1?, m?) = 1;
Id outlorentz(0, iv?, k1?, m?) = 1;
*---#] Scalars :
*---#[ Spinors :
*---#[   Massless Spinors :
Id inplorentz( 1, iv?, k1?, 0) *
      inp(field1?, k1?,  1) =
   NCContainer(USpa(k1), iv);
Id outlorentz( 1, iv?, k1?, 0) *
      out(field1?, k1?,  1) =
   NCContainer(UbarSpb(k1), iv);
Id inplorentz( 1, iv?, k1?, 0) *
      inp(field1?, k1?, -1) =
   NCContainer(USpb(k1), iv);
Id outlorentz( 1, iv?, k1?, 0) *
      out(field1?, k1?, -1) =
   NCContainer(UbarSpa(k1), iv);
Id outlorentz(-1, iv?, k1?, 0) *
      out(field1?, k1?,  1) =
   NCContainer(USpb(k1), iv);
Id inplorentz(-1, iv?, k1?, 0) *
      inp(field1?, k1?,  1) =
   NCContainer(UbarSpa(k1), iv);
Id outlorentz(-1, iv?, k1?, 0) *
      out(field1?, k1?, -1) =
   NCContainer(USpa(k1), iv);
Id inplorentz(-1, iv?, k1?, 0) *
      inp(field1?, k1?, -1) =
   NCContainer(UbarSpb(k1), iv);
*---#]   Massless Spinors :
*---#[   Massive Spinors :
Id inplorentz( 1, iv?, k1?, m?) *
      inp(field1?, k1?,  1) =
   NCContainer(USpa(k1, +1), iv);
Id outlorentz( 1, iv?, k1?, m?) *
      out(field1?, k1?,  1) =
   NCContainer(UbarSpb(k1, +1), iv);
Id inplorentz( 1, iv?, k1?, m?) *
      inp(field1?, k1?, -1) =
   NCContainer(USpb(k1, +1), iv);
Id outlorentz( 1, iv?, k1?, m?) *
      out(field1?, k1?, -1) =
   NCContainer(UbarSpa(k1, +1), iv);
Id outlorentz(-1, iv?, k1?, m?) *
      out(field1?, k1?,  1) =
   NCContainer(USpb(k1, -1), iv);
Id inplorentz(-1, iv?, k1?, m?) *
      inp(field1?, k1?,  1) =
   NCContainer(UbarSpa(k1, -1), iv);
Id outlorentz(-1, iv?, k1?, m?) *
      out(field1?, k1?, -1) =
   NCContainer(USpa(k1, -1), iv);
Id inplorentz(-1, iv?, k1?, m?) *
      inp(field1?, k1?, -1) =
   NCContainer(UbarSpb(k1, -1), iv);
*---#]   Massive Spinors :
*---#] Spinors :
*---#[ Polarisation Vectors for Gauge Bosons :
*---#[    Massless Gauge Bosons :
Id outlorentz(2, ivL2?, k1?, 0) *
      out(field1?, k1?,  1, vDUMMY1?) =
   1/sqrt2 * SpDenominator(Spb2(k1, vDUMMY1)) *
           UbarSpb(vDUMMY1) * Sm(ivL2) * USpa(k1);
Id outlorentz(2, ivL2?, k1?, 0) *
      out(field1?, k1?, -1, vDUMMY1?) =
   1/sqrt2 * SpDenominator(Spa2(vDUMMY1, k1)) *
           UbarSpa(vDUMMY1) * Sm(ivL2) * USpb(k1);
Id inplorentz(2, ivL2?, k1?, 0) *
      inp(field1?, k1?,  1, vDUMMY1?) =
   1/sqrt2 * SpDenominator(Spa2(vDUMMY1, k1)) *
           UbarSpa(vDUMMY1) * Sm(ivL2) * USpb(k1);
Id inplorentz(2, ivL2?, k1?, 0) *
      inp(field1?, k1?, -1, vDUMMY1?) =
   1/sqrt2 * SpDenominator(Spb2(k1, vDUMMY1)) *
           UbarSpb(vDUMMY1) * Sm(ivL2) * USpa(k1);
*---#]    Massless Gauge Bosons :
*---#[    Massive Gauge Bosons :
Id outlorentz(2, ivL2?, k1?, m?) *
      out(field1?, k1?,  1, k2?, k3?) =
   (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
      UbarSpb(k3) * Sm(ivL2) * USpa(k2);
Id outlorentz(2, ivL2?, k1?, m?) *
      out(field1?, k1?, -1, k2?, k3?) =
   (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
      UbarSpa(k3) * Sm(ivL2) * USpb(k2);
Id outlorentz(2, ivL2?, k1?, m?) *
      out(field1?, k1?,  0, k2?, k3?) =
   (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
      m * SpDenominator(Spb2(k3,k2)) * k3(ivL2));
Id inplorentz(2, ivL2?, k1?, m?) *
      inp(field1?, k1?,  1, k2?, k3?) =
   (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
      UbarSpa(k3) * Sm(ivL2) * USpb(k2);
Id inplorentz(2, ivL2?, k1?, m?) *
      inp(field1?, k1?, -1, k2?, k3?) =
   (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
      UbarSpb(k3) * Sm(ivL2) * USpa(k2);
Id inplorentz(2, ivL2?, k1?, m?) *
      inp(field1?, k1?,  0, k2?, k3?) =
   (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
      m * SpDenominator(Spb2(k3,k2)) * k3(ivL2));
*---#]    Massive Gauge Bosons :
*---#] Polarisation Vectors for Gauge Bosons :
*---#[ wave functions for Vector-Spinors :
Repeat;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
         UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
      NCContainer(USpb(k1,+1), ivL1);
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
           UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
        NCContainer(USpa(k1,+1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(USpb(k1,+1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
           UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
        NCContainer(USpb(k1,+1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(USpa(k1,+1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
         UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
      NCContainer(USpa(k1,+1), ivL1);
      Sum ivL2, ivL1;
   
   Id once inplorentz(-3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
         UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
      NCContainer(UbarSpb(k1,-1), ivL1);
      Sum ivL2, ivL1;
   Id once inplorentz(-3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
           UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
        NCContainer(UbarSpa(k1,-1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(UbarSpb(k1,-1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(-3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
           UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
        NCContainer(UbarSpb(k1,-1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(UbarSpa(k1,-1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(-3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
         UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
      NCContainer(UbarSpa(k1,-1), ivL1);
      Sum ivL2, ivL1;
   
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
         UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
      NCContainer(UbarSpa(k1,+1), ivL1);
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
           UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
        NCContainer(UbarSpb(k1,+1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(UbarSpa(k1,+1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
           UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
        NCContainer(UbarSpa(k1,+1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(UbarSpb(k1,+1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
         UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
      NCContainer(UbarSpb(k1,+1), ivL1);
      Sum ivL2, ivL1;
   
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
         UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
      NCContainer(USpa(k1,-1), ivL1);
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, -1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
           UbarSpa(k3) * Sm(ivL2) * USpb(k2) *
        NCContainer(USpb(k1,-1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(USpa(k1,-1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +1, k2?, k3?) = 1/sqrt3 *
      SplitLorentzIndex(ivL, ivL2, ivL1) * (
      + (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
           UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
        NCContainer(USpa(k1,-1), ivL1)
      + sqrt2 * (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
                   m * SpDenominator(Spb2(k3,k2)) * k3(ivL2)) *
        NCContainer(USpb(k1,-1), ivL1));
      Sum ivL2, ivL1;
   Id once inplorentz(3, ivL?, k1?, m?!{0,}) *
         inp(field1?, k1?, +2, k2?, k3?) =
      SplitLorentzIndex(ivL, ivL2, ivL1) *
      (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
         UbarSpb(k3) * Sm(ivL2) * USpa(k2) *
      NCContainer(USpb(k1,-1), ivL1);
      Sum ivL2, ivL1;
   
EndRepeat;
*---#] wave functions for Vector-Spinors :
*---#[ wave functions for gravitons :
Repeat;
   Id once inplorentz(4, ivL4?, k1?, m?) *
         inp(field1?, k1?, +2, k2?, k3?) =
      SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
      fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1, +1);
      Sum ivL2a, ivL2b;
   Id once inplorentz(4, ivL4?, k1?, m?) *
         inp(field1?, k1?, +1, k2?, k3?) =
      SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
      1/Sqrt2 * (
         + fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1,  0)
         + fDUMMY1(ivL2a, k1,  0) * fDUMMY1(ivL2b, k1, +1)
      );
      Sum ivL2, ivL1;
   Id once inplorentz(4, ivL4?, k1?, m?) *
         inp(field1?, k1?,  0, k2?, k3?) =
      SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
      1/Sqrt2/Sqrt3 * (
         + fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1, -1)
         + fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1, +1)
         + 2 * fDUMMY1(ivL2a, k1, 0) * fDUMMY1(ivL2b, k1, 0)
      );
      Sum ivL2, ivL1;
   Id once inplorentz(4, ivL4?, k1?, m?) *
         inp(field1?, k1?, -1, k2?, k3?) =
      SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
      1/Sqrt2 * (
         + fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1,  0)
         + fDUMMY1(ivL2a, k1,  0) * fDUMMY1(ivL2b, k1, -1)
      );
      Sum ivL2, ivL1;
   Id once inplorentz(4, ivL4?, k1?, m?) *
         inp(field1?, k1?, -2, k2?, k3?) =
      SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
      fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1, -1);
      Sum ivL2a, ivL2b;
   
   Id fDUMMY1(ivL2?, k1?, +1) =
      (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
         UbarSpa(k3) * Sm(ivL2) * USpb(k2);
   Id fDUMMY1(ivL2?, k1?, 0) =
      (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
         m * SpDenominator(Spb2(k3,k2)) * k3(ivL2));
   Id fDUMMY1(ivL2?, k1?, -1) =
      (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
         UbarSpb(k3) * Sm(ivL2) * USpa(k2);
      Id once inplorentz(4, ivL4?, k1?, m?) *
            inp(field1?, k1?, +2, k2?, k3?) =
         SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
         fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1, +1);
         Sum ivL2a, ivL2b;
      Id once inplorentz(4, ivL4?, k1?, m?) *
            inp(field1?, k1?, +1, k2?, k3?) =
         SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
         1/Sqrt2 * (
            + fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1,  0)
            + fDUMMY1(ivL2a, k1,  0) * fDUMMY1(ivL2b, k1, +1)
         );
         Sum ivL2, ivL1;
      Id once inplorentz(4, ivL4?, k1?, m?) *
            inp(field1?, k1?,  0, k2?, k3?) =
         SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
         1/Sqrt2/Sqrt3 * (
            + fDUMMY1(ivL2a, k1, +1) * fDUMMY1(ivL2b, k1, -1)
            + fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1, +1)
            + 2 * fDUMMY1(ivL2a, k1, 0) * fDUMMY1(ivL2b, k1, 0)
         );
         Sum ivL2, ivL1;
      Id once inplorentz(4, ivL4?, k1?, m?) *
            inp(field1?, k1?, -1, k2?, k3?) =
         SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
         1/Sqrt2 * (
            + fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1,  0)
            + fDUMMY1(ivL2a, k1,  0) * fDUMMY1(ivL2b, k1, -1)
         );
         Sum ivL2, ivL1;
      Id once inplorentz(4, ivL4?, k1?, m?) *
            inp(field1?, k1?, -2, k2?, k3?) =
         SplitLorentzIndex(ivL4, ivL2a, ivL2b) *
         fDUMMY1(ivL2a, k1, -1) * fDUMMY1(ivL2b, k1, -1);
         Sum ivL2a, ivL2b;
      
      Id fDUMMY1(ivL2?, k1?, +1) =
         (1/sqrt2 * SpDenominator(Spb2(k2, k3))) *
            UbarSpb(k3) * Sm(ivL2) * USpa(k2);
      Id fDUMMY1(ivL2?, k1?, 0) =
         (1/m) * (k2(ivL2) - m * SpDenominator(Spa2(k2,k3)) *
            m * SpDenominator(Spb2(k3,k2)) * k3(ivL2));
      Id fDUMMY1(ivL2?, k1?, -1) =
         (1/sqrt2 * SpDenominator(Spa2(k3, k2))) *
            UbarSpa(k3) * Sm(ivL2) * USpb(k2);
EndRepeat;
*---#] wave functions for gravitons :
