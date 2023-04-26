* vim: ts=3:sw=3:expandtab:syntax=form

#define R2PREFACTOR "1"

#procedure ReduceDiagramR2(DIAG)
   #call shiftmomenta(`DIAG',0)
   Argument Spab, Spaa, Spbb, Spba;
      #Call shiftmomenta(`DIAG',0)
   EndArgument;
   Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, iDUMMY2?, vDUMMY3?) =
      fDUMMY1(vDUMMY1, iDUMMY2, vDUMMY3);
   ToTensor Functions, Q, ptens;
   If(count(ptens,1)==0) Multiply ptens;

   #switch `DIAG'
*---#[ Diagram group 0:
   #case 33
      #define r1 "-k2+k4"
      #define m1sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r2 "-k2"
      #define m2sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r3 "0"
      #define m3sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r4 "-k3"
      #define m4sq "(mdlMT)^2-i_*(0*mdlMT)"
      #break
*---#] Diagram group 0:
*---#[ Diagram group 1:
   #case 5
   #case 12
   #case 14
   #case 31
      #define r1 "-k3-k4"
      #define m1sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r2 "-k3"
      #define m2sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r3 "0"
      #define m3sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r4 "-k2"
      #define m4sq "(mdlMT)^2-i_*(0*mdlMT)"
      #break
*---#] Diagram group 1:
*---#[ Diagram group 2:
   #case 1
   #case 2
   #case 3
   #case 4
   #case 7
   #case 8
   #case 10
   #case 16
   #case 18
   #case 22
   #case 23
   #case 27
   #case 29
      #define r1 "-k3-k4"
      #define m1sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r2 "-k4"
      #define m2sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r3 "0"
      #define m3sq "(mdlMT)^2-i_*(0*mdlMT)"
      #define r4 "-k2"
      #define m4sq "(mdlMT)^2-i_*(0*mdlMT)"
      #break
*---#] Diagram group 2:
   #endswitch
   #switch `DIAG'
*---#[ Diagram group 0:
*------#[ Diagram 33:
   #case 33
      #call ReduceR2N4(`r1',`r2',`r3',`r4')
      #break
*------#] Diagram 33:
*---#] Diagram group 0:
*---#[ Diagram group 1:
*------#[ Diagram 5:
   #case 5
      #call ReduceR2N2(`r2',`m2sq',`r4',`m4sq')
      #break
*------#] Diagram 5:
*------#[ Diagram 12:
   #case 12
      #call ReduceR2N3(`r1',`m1sq',`r2',`m2sq',`r4',`m4sq')
      #break
*------#] Diagram 12:
*------#[ Diagram 14:
   #case 14
      #call ReduceR2N3(`r2',`m2sq',`r3',`m3sq',`r4',`m4sq')
      #break
*------#] Diagram 14:
*------#[ Diagram 31:
   #case 31
      #call ReduceR2N4(`r1',`r2',`r3',`r4')
      #break
*------#] Diagram 31:
*---#] Diagram group 1:
*---#[ Diagram group 2:
*------#[ Diagram 1:
   #case 1
      #call ReduceR2N2(`r1',`m1sq',`r2',`m2sq')
      #break
*------#] Diagram 1:
*------#[ Diagram 2:
   #case 2
      #call ReduceR2N2(`r2',`m2sq',`r3',`m3sq')
      #break
*------#] Diagram 2:
*------#[ Diagram 3:
   #case 3
      #call ReduceR2N2(`r1',`m1sq',`r3',`m3sq')
      #break
*------#] Diagram 3:
*------#[ Diagram 4:
   #case 4
      #call ReduceR2N2(`r2',`m2sq',`r4',`m4sq')
      #break
*------#] Diagram 4:
*------#[ Diagram 7:
   #case 7
      #call ReduceR2N2(`r1',`m1sq',`r3',`m3sq')
      #break
*------#] Diagram 7:
*------#[ Diagram 8:
   #case 8
      #call ReduceR2N3(`r1',`m1sq',`r3',`m3sq',`r4',`m4sq')
      #break
*------#] Diagram 8:
*------#[ Diagram 10:
   #case 10
      #call ReduceR2N3(`r1',`m1sq',`r2',`m2sq',`r4',`m4sq')
      #break
*------#] Diagram 10:
*------#[ Diagram 16:
   #case 16
      #call ReduceR2N3(`r2',`m2sq',`r3',`m3sq',`r4',`m4sq')
      #break
*------#] Diagram 16:
*------#[ Diagram 18:
   #case 18
      #call ReduceR2N3(`r1',`m1sq',`r2',`m2sq',`r3',`m3sq')
      #break
*------#] Diagram 18:
*------#[ Diagram 22:
   #case 22
      #call ReduceR2N2(`r1',`m1sq',`r4',`m4sq')
      #break
*------#] Diagram 22:
*------#[ Diagram 23:
   #case 23
      #call ReduceR2N2(`r3',`m3sq',`r4',`m4sq')
      #break
*------#] Diagram 23:
*------#[ Diagram 27:
   #case 27
      #call ReduceR2N3(`r1',`m1sq',`r3',`m3sq',`r4',`m4sq')
      #break
*------#] Diagram 27:
*------#[ Diagram 29:
   #case 29
      #call ReduceR2N4(`r1',`r2',`r3',`r4')
      #break
*------#] Diagram 29:
*---#] Diagram group 2:
   #endswitch

   Id Qt2 = 0;
   Id eps = 0;

   Id fDUMMY1?{Spaa,Spab,Spbb,Spba}(vDUMMY1?, 0, vDUMMY3?) = 0;
   #call SpContractMetrics
   #call SpContract
   #call SpOpen(`LIGHTLIKE')
#endprocedure
