program test
   use eeZH_SMEFT_config, only: ki, logfile, EFTcount
   use eeZH_SMEFT_kinematics, only: dotproduct, boost_to_cms
   use eeZH_SMEFT_model
   use eeZH_SMEFT_matrix, only: samplitude, initgolem, exitgolem
   use eeZH_SMEFT_rambo, only: ramb

   implicit none
   integer :: ievt, ierr, prec
   real(ki), dimension(4, 4) :: vecs
   real(ki), dimension(0:4) :: amp, gsres, refres, diff
   real(ki) :: scale2, sqrts
   real(ki), parameter :: eps = 1.0e-10_ki
   
   ! log and output
   integer, parameter :: logf = 27
   logical :: success

   open(file="test.log", unit=logf)
   success = .true.

   
   ! parameters
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if

   sqrts = 500._ki
   
   call initgolem()
   
   call random_seed
   call ramb(sqrts**2, vecs)
   call boost_to_cms(vecs)

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

   ! (SM x SM)
   EFTcount = 0
   call samplitude(vecs, scale2, amp, prec)
   gsres(0) = amp(0)
   refres(0) = analytic_amp(vecs)
   write(unit=6,fmt="(A27)") "Truncation order (SM x SM):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(0), &
        & "Analytical:", refres(0), &
        & "Ratio:", gsres(0)/refres(0)

   ! (SM x SM) + (SM x dim-6)
   EFTcount = 1
   call samplitude(vecs, scale2, amp, prec)
   gsres(1) = amp(0)
   refres(1) = analytic_amp(vecs)
   write(unit=6,fmt="(A42)") "Truncation order (SM x SM) + (SM x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(1), &
        & "Analytical:", refres(1), &
        & "Ratio:", gsres(1)/refres(1)

   ! (SM + dim-6) x (SM + dim-6)
   EFTcount = 2
   call samplitude(vecs, scale2, amp, prec)
   gsres(2) = amp(0)
   refres(2) = analytic_amp(vecs)
   write(unit=6,fmt="(A45)") "Truncation order (SM + dim-6) x (SM + dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(2), &
        & "Analytical:", refres(2), &
        & "Ratio:", gsres(2)/refres(2)

   ! (SM x dim-6)
   EFTcount = 3
   call samplitude(vecs, scale2, amp, prec)
   gsres(3) = amp(0)
   refres(3) = analytic_amp(vecs)
   write(unit=6,fmt="(A30)") "Truncation order (SM x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(3), &
        & "Analytical:", refres(3), &
        & "Ratio:", gsres(3)/refres(3)   
   
   ! (dim-6) x (dim-6)
   EFTcount = 4
   call samplitude(vecs, scale2, amp, prec)
   gsres(4) = amp(0)
   refres(4) = analytic_amp(vecs)
   write(unit=6,fmt="(A33)") "Truncation order (dim-6 x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(4), &
        & "Analytical:", refres(4), &
        & "Ratio:", gsres(4)/refres(4)

   if (any(isnan(gsres))) then
      write(unit=logf,fmt="(A10)") "NaN error!"
      success = .false.
   end if
      
   diff = abs(rel_diff(gsres, refres))
   
   if (diff(0) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A59)") "==>", &
           & "Comparison of (SM x SM) (EFTcount=0) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
      success = .false.
   end if

   if (diff(1) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A59)") "==>", &
           & "Comparison of (SM x SM) + (SM x dim-6) (EFTcount=1) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(1)
      success = .false.
   end if

   if (diff(2) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A62)") "==>", &
           & "Comparison of (SM + dim-6) x (SM + dim-6) (EFTcount=2) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
      success = .false.
   end if

   if (diff(3) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A47)") "==>", &
           & "Comparison of (SM x dim-6) (EFTcount=3) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(3)
      success = .false.
   end if

   if (diff(4) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A52)") "==>", &
           & "Comparison of (dim-6) x (dim-6) (EFTcount=4) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(4)
      success = .false.
   end if

   if (success) then
      write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
   else
      write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
   end if

   close(unit=logf)
  
   call exitgolem()
   
 contains
   

!--------------------------------------------------------------------------------
! Analytic result has been obtained using Feyncalc
!
! V. Shtabovenko, R. Mertig and F. Orellana - 2312.14089
! V. Shtabovenko, R. Mertig and F. Orellana - 2001.04407
! V. Shtabovenko, R. Mertig and F. Orellana - 1601.01167
! R. Mertig, M. Böhm, and A. Denner - Comput. Phys. Commun., 64, 345-359, 1991.
!
! with a FeynArts model generated by SmeftFR3.0
!
! A. Dedes, J. Rosiek, M. Ryczkowski, K. Suxho and L. Trifyllis - 2302.01353
! A. Dedes, M. Paraskevas, J. Rosiek, K. Suxho and L. Trifyllis - 1904.03204
! A. Dedes, W. Materkowska, M. Paraskevas, J. Rosiek and K. Suxho - 1704.03888
!--------------------------------------------------------------------------------
function analytic_amp(vecs) result(amp)
  use eeZH_SMEFT_model
  use eeZH_SMEFT_config, only: EFTcount
  implicit none
  real(ki), intent(in), dimension(4,4) :: vecs
  real(ki) :: amp, s, t, u
  real(ki) :: coeffSM
  real(ki) :: coeffHB, coeffHW, coeffHWB
  real(ki) :: coeffHBHB, coeffHBHW, coeffHBHWB, coeffHWHW, coeffHWHWB, coeffHWBHWB

  call Mandelstam(vecs,s,t,u)
  
  coeffSM = analytic_coeff_SM(s,t,u)
  coeffHB = analytic_coeff_cHB(s,t,u)
  coeffHW = analytic_coeff_cHW(s,t,u)
  coeffHWB = analytic_coeff_cHWB(s,t,u)
  coeffHBHB = analytic_coeff_cHBcHB(s,t,u)
  coeffHBHW = analytic_coeff_cHBcHW(s,t,u)
  coeffHBHWB = analytic_coeff_cHBcHWB(s,t,u)
  coeffHWHW = analytic_coeff_cHWcHW(s,t,u)
  coeffHWHWB = analytic_coeff_cHWcHWB(s,t,u)
  coeffHWBHWB = analytic_coeff_cHWBcHWB(s,t,u)
  
  select case(EFTcount)
  case(0)
     amp = coeffSM
  case(1)
     amp = coeffSM + (mdlcHB*coeffHB + mdlcHW*coeffHW + mdlcHWB*coeffHWB)/mdlLambdaSMEFT**2
  case(2)
     amp = coeffSM + (mdlcHB*coeffHB + mdlcHW*coeffHW + mdlcHWB*coeffHWB)/mdlLambdaSMEFT**2 &
          & + (mdlcHB*mdlcHB*coeffHBHB &
          & + mdlcHB*mdlcHW*coeffHBHW &
          & + mdlcHB*mdlcHWB*coeffHBHWB &
          & + mdlcHW*mdlcHW*coeffHWHW &
          & + mdlcHW*mdlcHWB*coeffHWHWB &
          & + mdlcHWB*mdlcHWB*coeffHWBHWB )/mdlLambdaSMEFT**4
  case(3)
     amp = (mdlcHB*coeffHB + mdlcHW*coeffHW + mdlcHWB*coeffHWB)/mdlLambdaSMEFT**2
  case(4)
     amp = (mdlcHB*mdlcHB*coeffHBHB &
          & + mdlcHB*mdlcHW*coeffHBHW &
          & + mdlcHB*mdlcHWB*coeffHBHWB &
          & + mdlcHW*mdlcHW*coeffHWHW &
          & + mdlcHW*mdlcHWB*coeffHWHWB &
          & + mdlcHWB*mdlcHWB*coeffHWBHWB )/mdlLambdaSMEFT**4     
  case default
     print *, "Unknown value for EFTcount: ", EFTcount
     stop
  end select
  
end function analytic_amp


subroutine Mandelstam(vecs,s,t,u)
  use eeZH_SMEFT_kinematics, only: dotproduct
  implicit none
  real(ki), intent(in), dimension(4,4) :: vecs
  real(ki), intent(out) :: s, t, u

  s = dotproduct(vecs(1,:)+vecs(2,:),vecs(1,:)+vecs(2,:))
  t = dotproduct(vecs(1,:)-vecs(3,:),vecs(1,:)-vecs(3,:))
  u = dotproduct(vecs(1,:)-vecs(4,:),vecs(1,:)-vecs(4,:))
  
end subroutine Mandelstam


function analytic_coeff_SM(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = 2._ki*mdlGf**2*(-12._ki*mdlMW**2*mdlMZ**2 + 8._ki*mdlMW**4 + 5._ki*mdlMZ**4) &
       & *(mdlMH**2*mdlMZ**2 - 2._ki*t*mdlMZ**2 - 2._ki*u*mdlMZ**2 + 2._ki*mdlMZ**4 + t*u) &
       & /(s-mdlMZ**2)**2
  
end function analytic_coeff_SM


function analytic_coeff_cHB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = (4._ki*Sqrt(2._ki)*mdlGf*(t + u - 2._ki*mdlMZ**2)*(-mdlMW**2 + mdlMZ**2) &
       & *(-8._ki*mdlMW**4 - 5._ki*s*mdlMZ**2 + 6._ki*mdlMW**2*(s + mdlMZ**2))) &
       &/(s - mdlMZ**2)**2
  
end function analytic_coeff_cHB


function analytic_coeff_cHW(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp =  (-4._ki*Sqrt(2._ki)*mdlGf*mdlMW**2*(t + u - 2._ki*mdlMZ**2) &
       & *(8._ki*mdlMW**4 - s*mdlMZ**2 + 6._ki*mdlMZ**4 &
       & + 2._ki*mdlMW**2*(s - 7._ki*mdlMZ**2)))/(s - mdlMZ**2)**2
  
end function analytic_coeff_cHW


function analytic_coeff_cHWB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = (4._ki*Sqrt(2._ki)*mdlGf*mdlMW*Sqrt(-mdlMW**2 + mdlMZ**2) &
       & *(-8._ki*mdlMW**4*(t + u - 2._ki*mdlMZ**2) + mdlMZ**2 &
       & *(2._ki*s**2 + 3._ki*s*u + 3._ki*u**2 - (2._ki*s + 3._ki*u)*mdlMH**2 &
       & - (s + 3._ki*u)*mdlMZ**2 + 3._ki*mdlMZ**4) &
       & - 2._ki*mdlMW**2*(t**2 + u**2 - (t + u)*mdlMH**2 &
       & - 4._ki*(t + u)*mdlMZ**2 + 8._ki*mdlMZ**4)))/(s - mdlMZ**2)**2
  
end function analytic_coeff_cHWB


function analytic_coeff_cHBcHB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = (2._ki*(5._ki*s**2 - 12._ki*s*mdlMW**2 + 8._ki*mdlMW**4) &
       & *(mdlMW**2 - mdlMZ**2)**2*(t**2 + u**2 &
       & + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 + 4._ki*mdlMZ**4)) &
       & /(s*mdlMZ**2*(s - mdlMZ**2)**2)

end function analytic_coeff_cHBcHB


function analytic_coeff_cHBcHW(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = (4._ki*mdlMW**2*(mdlMW**2 - mdlMZ**2)*(t**2 + u**2 &
     & + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 + 4._ki*mdlMZ**4) &
     & *(-8._ki*mdlMW**4 + s*(s - 6._ki*mdlMZ**2) + 4._ki*mdlMW**2 &
     & *(s + 2._ki*mdlMZ**2)))/(s*mdlMZ**2*(s - mdlMZ**2)**2)
  
end function analytic_coeff_cHBcHW


function analytic_coeff_cHBcHWB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp = (4._ki*mdlMW*Sqrt(-mdlMW**2 + mdlMZ**2)*(-8._ki*mdlMW**6*(t**2 + u**2 &
       & + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 + 4._ki*mdlMZ**4) &
       & + s*mdlMZ**2*(2._ki*s*(s**2 + 2._ki*s*u + 2._ki*u**2) &
       & + (s**2 + 2._ki*s*u + 6._ki*u**2)*mdlMZ**2 + 2._ki*(s - 3._ki*u)*mdlMZ**4 &
       & + 3._ki*mdlMZ**6 + mdlMH**4*(2._ki*s + 3._ki*mdlMZ**2) &
       & - 2._ki*mdlMH**2*(2._ki*s*(s + u) + 3._ki*u*mdlMZ**2)) + 4._ki*mdlMW**4 &
       & *(2._ki*s*(s**2 + 2._ki*s*u + 2._ki*u**2) + (5._ki*s**2 + 2._ki*s*u &
       & + 6._ki*u**2)*mdlMZ**2 + 6._ki*(s - u)*mdlMZ**4 + 3._ki*mdlMZ**6 &
       & + mdlMH**4*(2._ki*s + 3._ki*mdlMZ**2) - 2._ki*mdlMH**2*(2._ki*s*(s + u) &
       & + (2._ki*s + 3._ki*u)*mdlMZ**2)) - mdlMW**2*(2._ki*s**2*(s**2 + 2._ki*s*u &
       & + 2._ki*u**2) + s*(9._ki*s**2 + 18._ki*s*u + 22._ki*u**2)*mdlMZ**2 &
       & + 2._ki*(7._ki*s**2 - 7._ki*s*u + 4._ki*u**2)*mdlMZ**4 + (11._ki*s &
       & - 8._ki*u)*mdlMZ**6 + 4._ki*mdlMZ**8 + mdlMH**4*(2._ki*s**2 &
       & + 11._ki*s*mdlMZ**2 + 4._ki*mdlMZ**4) - 2._ki*mdlMH**2*(2._ki*s**2*(s + u) &
       & + s*(8._ki*s + 11._ki*u)*mdlMZ**2 + 4._ki*u*mdlMZ**4)))) &
       & /(s*mdlMZ**2*(s - mdlMZ**2)**2)
  
end function analytic_coeff_cHBcHWB


function analytic_coeff_cHWcHW(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp =  (2._ki*mdlMW**4*(t**2 + u**2 + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 &
       & + 4._ki*mdlMZ**4)*(s**2 + 8._ki*mdlMW**4 - 4._ki*s*mdlMZ**2 + 8._ki*mdlMZ**4 &
       & + 4._ki*mdlMW**2*(s - 4._ki*mdlMZ**2)))/(s*mdlMZ**2*(s - mdlMZ**2)**2)
  
end function analytic_coeff_cHWcHW


function analytic_coeff_cHWcHWB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp =  (4._ki*mdlMW**3*Sqrt(-mdlMW**2 + mdlMZ**2)*(8._ki*mdlMW**4*(t**2 + u**2 &
       & + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 + 4._ki*mdlMZ**4) &
       & - 4._ki*mdlMW**2*mdlMZ**2*(t**2 - 4._ki*t*u + u**2 - 6._ki*(t + u)*mdlMZ**2 &
       & + 8._ki*mdlMZ**4 + 2._ki*mdlMH**2*(t + u + mdlMZ**2)) &
       & + mdlMZ**2*(s*(3._ki*s**2 + 2._ki*s*u + 2._ki*u**2) &
       & + 2._ki*u*(3._ki*s + 4._ki*u)*mdlMZ**2 + (s - 8._ki*u)*mdlMZ**4 &
       & + 4._ki*mdlMZ**6 + mdlMH**4*(s + 4._ki*mdlMZ**2) - 2._ki*mdlMH**2*(s*(2._ki*s + u) &
       & + 4._ki*u*mdlMZ**2))))/(s*mdlMZ**2*(s - mdlMZ**2)**2)
  
end function analytic_coeff_cHWcHWB


function analytic_coeff_cHWBcHWB(s,t,u) result(amp)
  use eeZH_SMEFT_model
  implicit none
  real(ki), intent(in) :: s, t, u
  real(ki) :: amp

  amp =  (-2._ki*(8._ki*mdlMW**8*(t**2 + u**2 + (-4._ki*(t + u) + 2._ki*mdlMH**2)*mdlMZ**2 &
       & + 4._ki*mdlMZ**4) + 4._ki*mdlMW**6*(t**3 + t**2*u + t*u**2 + u**3 &
       & - 5._ki*(t**2 + u**2)*mdlMZ**2 - 2._ki*mdlMH**4*mdlMZ**2 + 12._ki*(t + u)*mdlMZ**4 &
       & - 12._ki*mdlMZ**6 - mdlMH**2*(t**2 + u**2 - 2._ki*(t + u)*mdlMZ**2 + 6._ki*mdlMZ**4)) &
       & - mdlMW**2*mdlMZ**2*(s**2*(s**2 + 2._ki*s*u + 2._ki*u**2) - 2._ki*s**2*u*mdlMZ**2 &
       & + (3._ki*s**2 + 4._ki*s*u + 4._ki*u**2)*mdlMZ**4 - 2._ki*(s + 2._ki*u)*mdlMZ**6 &
       & + 2._ki*mdlMZ**8 + mdlMH**4*(s**2 + 2._ki*s*mdlMZ**2 + 2._ki*mdlMZ**4) &
       & - 2._ki*mdlMH**2*(s**2*(s + u) + 2._ki*u*mdlMZ**4)) &
       & + mdlMW**4*(s**2*(s**2 + 2._ki*s*u + 2._ki*u**2) &
       & + 2._ki*s*(2._ki*s**2 + 3._ki*s*u + 4._ki*u**2)*mdlMZ**2 &
       & + (3._ki*s**2 + 12._ki*s*u + 20._ki*u**2)*mdlMZ**4 &
       & + 2._ki*(s - 10._ki*u)*mdlMZ**6 + 10._ki*mdlMZ**8 &
       & + mdlMH**4*(s**2 + 6._ki*s*mdlMZ**2 + 10._ki*mdlMZ**4) &
       & - 2._ki*mdlMH**2*(s**2*(s + u) + 4._ki*s*(s + u)*mdlMZ**2 + 10._ki*u*mdlMZ**4)))) &
       & /(s*mdlMZ**2*(s - mdlMZ**2)**2)
  
end function analytic_coeff_cHWBcHWB
  

pure elemental function rel_diff(a, b)
   implicit none

   double precision, intent(in) :: a, b
   double precision :: rel_diff

   if (a.eq.0.0d0 .and. b.eq.0.0d0) then
      rel_diff = 0.0d0
   else
      rel_diff = 2.0d0 * (a-b) / (abs(a)+abs(b))
   end if
 end  function rel_diff
 

end program test
