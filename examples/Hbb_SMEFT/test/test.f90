program test
   use Hbb_SMEFT_config, only: ki, logfile, EFTcount
   use Hbb_SMEFT_model
   use Hbb_SMEFT_matrix, only: samplitude, initgolem, exitgolem

   implicit none
   integer :: ievt, ierr, prec
   real(ki), dimension(3, 4) :: vecs
   real(ki), dimension(0:3) :: amp, gsres, refres, diff
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

   call initgolem()

   scale2 = mdlMH/2._ki

   vecs(1,:) = (/mdlMH,0._ki,0._ki,0._ki/)
   vecs(2,:) = (/mdlMH/2._ki,0._ki,0._ki,sqrt(mdlMH**2/4._ki-mdlMQB**2)/)
   vecs(3,:) = (/mdlMH/2._ki,0._ki,0._ki,-sqrt(mdlMH**2/4._ki-mdlMQB**2)/)

   ! (SM x SM) + (SM x dim-6)
   EFTcount = 0
   call samplitude(vecs, scale2, amp, prec)
   gsres(0) = amp(0)
   refres(0) = analytic_amp()
   write(unit=6,fmt="(A42)") "Truncation order (SM x SM) + (SM x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(0), &
        & "Analytical:", refres(0), &
        & "Ratio:", gsres(0)/refres(0)

   ! (SM + dim-6) x (SM + dim-6)
   EFTcount = 1
   call samplitude(vecs, scale2, amp, prec)
   gsres(1) = amp(0)
   refres(1) = analytic_amp()
   write(unit=6,fmt="(A45)") "Truncation order (SM + dim-6) x (SM + dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(1), &
        & "Analytical:", refres(1), &
        & "Ratio:", gsres(1)/refres(1)

   ! (SM x dim-6)
   EFTcount = 4
   call samplitude(vecs, scale2, amp, prec)
   gsres(2) = amp(0)
   refres(2) = analytic_amp()
   write(unit=6,fmt="(A30)") "Truncation order (SM x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(2), &
        & "Analytical:", refres(2), &
        & "Ratio:", gsres(2)/refres(2)   
   
   ! (dim-6) x (dim-6)
   EFTcount = 5
   call samplitude(vecs, scale2, amp, prec)
   gsres(3) = amp(0)
   refres(3) = analytic_amp()
   write(unit=6,fmt="(A33)") "Truncation order (dim-6 x dim-6):"
   write(unit=6,fmt="(A6,1x,E23.16E3,3x,A11,1x,E23.16E3,3x,A6,1x,F18.16,/)") &
        & "GoSam:", gsres(3), &
        & "Analytical:", refres(3), &
        & "Ratio:", gsres(3)/refres(3)

   
   diff = abs(rel_diff(gsres, refres))
   
   if (diff(0) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A59)") "==>", &
           & "Comparison of (SM x SM) + (SM x dim-6) (EFTcount=0) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
      success = .false.
   end if

   if (diff(1) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A62)") "==>", &
           & "Comparison of (SM + dim-6) x (SM + dim-6) (EFTcount=1) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(1)
      success = .false.
   end if

   if (diff(2) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A47)") "==>", &
           & "Comparison of (SM x dim-6) (EFTcount=4) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
      success = .false.
   end if

   if (diff(3) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A50)") "==>", &
           & "Comparison of (dim-6) x (dim-6) (EFTcount) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(3)
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
   

function analytic_amp() result(amp)
  use Hbb_SMEFT_model
  use Hbb_SMEFT_config, only: EFTcount
  implicit none
  real(ki) :: amp
  real(ki) :: coeffSM
  real(ki) :: coeffbphi, coeffphiG
  real(ki) :: coeffbphibphi, coeffbphiphiG, coeffphiGphiG
  
  coeffSM = analytic_coeff_SM()
  coeffbphi = analytic_coeff_cbphi()
  coeffphiG = analytic_coeff_cphiG()
  coeffbphibphi= analytic_coeff_cbphicbphi()
  coeffbphiphiG = analytic_coeff_cbphicphiG()
  coeffphiGphiG = analytic_coeff_cphiGcphiG()
  
  select case(EFTcount)
  case(0)
     amp = coeffSM + (mdlcbphi*coeffbphi + mdlcphiG*coeffphiG)*mdlLam
  case(1)
     amp = coeffSM + (mdlcbphi*coeffbphi + mdlcphiG*coeffphiG)*mdlLam &
          & + (mdlcbphi*mdlcbphi*coeffbphibphi &
          & + mdlcbphi*mdlcphiG*coeffbphiphiG &
          & + mdlcphiG*mdlcphiG*coeffphiGphiG)*mdlLam**2
  case(4)
     amp = (mdlcbphi*coeffbphi + mdlcphiG*coeffphiG)*mdlLam
  case(5)
     amp = (mdlcbphi*mdlcbphi*coeffbphibphi &
          & + mdlcbphi*mdlcphiG*coeffbphiphiG &
          & + mdlcphiG*mdlcphiG*coeffphiGphiG)*mdlLam**2    
  case default
     print *, "Unknown value for EFTcount: ", EFTcount
     stop
  end select
  
end function analytic_amp


function analytic_coeff_SM() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: tau, amp

  tau = 4._ki*mdlMQB**2/mdlMH**2
  
  amp = sqrt(8._ki)*mdlGf*NC*mdlymb**2*mdlMH**2*(1._ki-tau)
  
end function analytic_coeff_SM


function analytic_coeff_cbphi() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: tau, amp

  tau = 4._ki*mdlMQB**2/mdlMH**2
  
  amp = -2._ki*sqrt(sqrt(2._ki))*NC*mdlymb*mdlMH**2*(1._ki-tau)/sqrt(mdlGf)
  
end function analytic_coeff_cbphi


function analytic_coeff_cphiG() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: amp

  amp = 0._ki
  
end function analytic_coeff_cphiG


function analytic_coeff_cbphicbphi() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: tau, amp

  tau = 4._ki*mdlMQB**2/mdlMH**2
  
  amp = NC*mdlMH**2*(1._ki-tau)/(2._ki*mdlGf**2)
  
end function analytic_coeff_cbphicbphi


function analytic_coeff_cbphicphiG() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: amp

  amp = 0._ki
  
end function analytic_coeff_cbphicphiG


function analytic_coeff_cphiGcphiG() result(amp)
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: amp

  amp = 0._ki
  
end function analytic_coeff_cphiGcphiG


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
