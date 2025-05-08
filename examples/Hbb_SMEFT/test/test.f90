program test
   use Hbb_SMEFT_config, only: ki, logfile, EFTcount, renormalisation, nlo_prefactors
   use Hbb_SMEFT_model
   use Hbb_SMEFT_matrix, only: samplitude, initgolem, exitgolem

   implicit none
   integer :: ievt, ierr, prec, ieft
   integer, parameter, dimension(0:3) :: eftc = (/0,1,4,5/)
   real(ki), dimension(3, 4) :: vecs
   real(ki), dimension(0:3,0:3) :: gsres, refres, diff
   real(ki) :: scale2, sqrts
   real(ki), parameter :: eps = 1.0e-10_ki
   character(len=45), dimension(0:3) :: truncation_order
   
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

   renormalisation=1
   nlo_prefactors=0
   
   scale2 = mdlMH/2._ki

   vecs(1,:) = (/mdlMH,0._ki,0._ki,0._ki/)
   vecs(2,:) = (/mdlMH/2._ki,0._ki,0._ki,sqrt(mdlMH**2/4._ki-mdlMQB**2)/)
   vecs(3,:) = (/mdlMH/2._ki,0._ki,0._ki,-sqrt(mdlMH**2/4._ki-mdlMQB**2)/)

   truncation_order = [character(len=45) :: &
        & "Truncation order (SM x SM) + (SM x dim-6):", &
        & "Truncation order (SM + dim-6) x (SM + dim-6):", &
        & "Truncation order (SM x dim-6):", &
        & "Truncation order (dim-6 x dim-6):" ]
   
   do ieft = 0, 3
      EFTcount = eftc(ieft)
      call samplitude(vecs, scale2, gsres(ieft,:), prec)
      call analytic_amp(refres(ieft,:))
      write(unit=6,fmt="(A45)") NEW_LINE('a'), truncation_order(ieft)
      write(unit=6,fmt="((14x,A11,3(15x,A11)))") &
           & "Born       ", "finite part", "single pole", "double pole"
      write(unit=6,fmt="((A11,4(3x,E23.16E3)))") &
           & "GoSam:     ", gsres(ieft,0), gsres(ieft,1), gsres(ieft,2), gsres(ieft,3)
      write(unit=6,fmt="((A11,4(3x,E23.16E3)))") &
           & "Analytical:", refres(ieft,0), refres(ieft,1), refres(ieft,2), refres(ieft,3)
      write(unit=6,fmt="((A11,4(3x,E23.16E3)))") &
           & "Ratio:     ", gsres(ieft,0)/refres(ieft,0), gsres(ieft,1)/refres(ieft,1), &
           & gsres(ieft,2)/refres(ieft,2), gsres(ieft,3)/refres(ieft,3), NEW_LINE('a')
   end do
   
   diff = abs(rel_diff(gsres, refres))
   
   if (diff(0,0) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A59)") "==>", &
           & "Comparison of (SM x SM) + (SM x dim-6) (EFTcount=0) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0,0)
      success = .false.
   end if

   if (diff(0,1) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A62)") "==>", &
           & "Comparison of (SM + dim-6) x (SM + dim-6) (EFTcount=1) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0,1)
      success = .false.
   end if

   if (diff(0,2) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A47)") "==>", &
           & "Comparison of (SM x dim-6) (EFTcount=4) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0,2)
      success = .false.
   end if

   if (diff(0,3) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A50)") "==>", &
           & "Comparison of (dim-6) x (dim-6) (EFTcount) failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0,3)
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
   

subroutine analytic_amp(amp)
  use Hbb_SMEFT_model
  use Hbb_SMEFT_config, only: EFTcount
  implicit none
  real(ki), dimension(0:3), intent(out) :: amp
  real(ki), dimension(0:3) :: coeffSM
  real(ki), dimension(0:3) :: coeffbphi, coeffphiG
  real(ki), dimension(0:3) :: coeffbphibphi, coeffbphiphiG, coeffphiGphiG
  
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
  
end subroutine analytic_amp


function analytic_coeff_SM() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  xb = x()

  amp = 0._ki
  
  amp(0) = sqrt(8._ki)*mdlGf*CA*mdlymb**2*mdlMH**2*(xb+1._ki)**2/(xb-1._ki)**2
  
  amp(1) = 0._ki
  
  amp(2) = 2._ki*real(sqrt(8._ki)*mdlGf*CA*CF*mdlymb**2*mdlMH**2 &
       & *(xb+1._ki)/(xb-1._ki)**3*(1._ki - xb**2 + (xb**2 + 1._ki) * zlog(xb)))
  
  amp(3) = 0._ki
  
end function analytic_coeff_SM


function analytic_coeff_cbphi() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  xb = x()

  amp = 0._ki
  
  amp(0) = -2._ki*2._ki**0.25_ki/sqrt(mdlGf)*CA*mdlymb*mdlMH**2*(xb+1._ki)**2/(xb-1._ki)**2

  amp(1) = 0._ki
  
  amp(2) = 2._ki*real(-2._ki*2._ki**0.25_ki/sqrt(mdlGf)*CA*CF*mdlymb*mdlMH**2 &
       & *(xb+1._ki)/(xb-1._ki)**3*(1._ki - xb**2 + (xb**2 + 1._ki) * zlog(xb)))
  
  amp(3) = 0._ki
  
end function analytic_coeff_cbphi


function analytic_coeff_cphiG() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlMQB
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  xb = x()

  amp = 0._ki

  amp(0) = 0._ki

  amp(1) = 0._ki
  
  ! amp(2) = 2._ki*real(-12._ki*mdlMH**2*mdlymb*CA*CF &
  !      & *( mdlMH*sqrt(-xb) + (xb-1._ki)*mdlymb )) &
  !      & *(xb+1._ki)**2/(xb-1._ki)**3

  amp(2) = 2._ki*real(-12._ki*mdlymb*CA*CF &
       & *(4._ki*mdlMQB**2-mdlMH**2)) &
       & *(mdlMQB - mdlymb)
  ! NOTE that this is EXACTLY zero when the particle mass equals the Yukawa mass!

  amp(3) = 0._ki
  
end function analytic_coeff_cphiG


function analytic_coeff_cbphicbphi() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  xb = x()

  amp = 0._ki

  amp(0) = CA*mdlMH**2/(2._ki*mdlGf**2)*(xb+1._ki)**2/(xb-1._ki)**2

  amp(1) = 0._ki

  amp(2) = 2._ki*real(CA*CF*mdlMH**2/(2._ki*mdlGf**2) &
       & *(xb+1._ki)/(xb-1._ki)**3*(1._ki - xb**2 + (xb**2 + 1._ki) * zlog(xb)))

  amp(3) = 0._ki
  
end function analytic_coeff_cbphicbphi


function analytic_coeff_cbphicphiG() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  xb = x()  

  amp = 0._ki

  amp(0) = 0._ki

  amp(1) = 0._ki

  ! amp(2) = 2._ki*real(3._ki*2._ki**0.75_ki*mdlMH**2*CA*CF/mdlGf**0.75_ki &
  !      & *( mdlMH*sqrt(-xb) + (xb-1._ki)*mdlymb )) &
  !      & *(xb+1._ki)**2/(xb-1._ki)**3

  amp(2) = 2._ki*real(3._ki*2._ki**0.75_ki*CA*CF/mdlGf**0.75_ki &
       & *(4._ki*mdlMQB**2-mdlMH**2)) &
       & *(mdlMQB - mdlymb)
  ! NOTE that this is EXACTLY zero when the particle mass equals the Yukawa mass!
  
  amp(3) = 0._ki

  
end function analytic_coeff_cbphicphiG


function analytic_coeff_cphiGcphiG() result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki), dimension(0:3) :: amp
  real(ki) :: xb

  !xb = x()

  amp = 0._ki
  
end function analytic_coeff_cphiGcphiG


function x()
  use Hbb_SMEFT_model
  implicit none
  real(ki) :: x, tau

  tau = 4._ki*mdlMQB**2/mdlMH**2
  x = (sqrt(1._ki-tau)-1._ki)/(sqrt(1._ki-tau)+1._ki)
  
end function x


function zlog(a) result(l)
  implicit none
  real(ki) :: a
  complex(ki) :: l

  if (a.gt.0) then
     l = COMPLEX(log(a),0)
  else if (a.lt.0) then
     l = COMPLEX(log(abs(a)),1)
  end if
  
end function zlog

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
