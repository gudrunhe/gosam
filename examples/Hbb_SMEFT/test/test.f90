program test
   use Hbb_SMEFT_config, only: ki, logfile, EFTcount, renormalisation, nlo_prefactors
   use Hbb_SMEFT_model
   use Hbb_SMEFT_matrix, only: samplitude, initgolem, exitgolem, ir_subtraction

   implicit none
   integer :: ievt, ierr, prec, ieft
   integer, parameter, dimension(0:3) :: eftc = (/0,1,4,5/)
   real(ki), dimension(3, 4) :: vecs
   real(ki), dimension(0:3,0:3) :: gsres, refres, gsirp, diff
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
   
   scale2 = mdlMH**2/4._ki

   vecs(1,:) = (/mdlMH,0._ki,0._ki,0._ki/)
   vecs(2,:) = (/mdlMH/2._ki,0._ki,0._ki,sqrt(mdlMH**2/4._ki-mdlMQB**2)/)
   vecs(3,:) = (/mdlMH/2._ki,0._ki,0._ki,-sqrt(mdlMH**2/4._ki-mdlMQB**2)/)

   truncation_order = [character(len=45) :: &
        & "Truncation order (SM x SM) + (SM x dim-6):", &
        & "Truncation order (SM + dim-6) x (SM + dim-6):", &
        & "Truncation order (SM x dim-6):", &
        & "Truncation order (dim-6 x dim-6):" ]

   gsres = 0._ki
   gsirp = 0._ki
   refres = 0._ki
   
   do ieft = 0, 3
      EFTcount = eftc(ieft)
      call samplitude(vecs, scale2, gsres(ieft,:), prec)
      call ir_subtraction(vecs,scale2, gsirp(ieft,2:3))
      call analytic_amp(scale2,refres(ieft,:))
      write(unit=6,fmt="(A45)") NEW_LINE('a'), truncation_order(ieft)
      write(unit=6,fmt="((15x,A11,3(15x,A11)))") &
           & "Born       ", "finite part", "single pole", "double pole"
      write(unit=6,fmt="((A12,4(3x,E23.16E3)))") &
           & "GoSam      :", gsres(ieft,0), gsres(ieft,1), gsres(ieft,2), gsres(ieft,3)
      write(unit=6,fmt="((A12,4(3x,E23.16E3)))") &
           & "Analytical :", refres(ieft,0), refres(ieft,1), refres(ieft,2), refres(ieft,3)
      write(unit=6,fmt="((A12,52x,2(3x,E23.16E3)))") &
           & "IR poles   :", gsirp(ieft,2), gsirp(ieft,3)
      write(unit=6,fmt="((A12,4(3x,E23.16E3)))") &
           & "Ratio GS/A :", gsres(ieft,0)/refres(ieft,0), gsres(ieft,1)/refres(ieft,1), &
           & gsres(ieft,2)/refres(ieft,2), gsres(ieft,3)/refres(ieft,3), NEW_LINE('a')

      diff(ieft,:) = abs(rel_diff(gsres(ieft,:), refres(ieft,:)))

      if (any(diff(ieft,:) .gt. eps)) then
         write(unit=logf,fmt="(A3,1x,A59)") "==>", &
              & "Comparison of (SM x SM) + (SM x dim-6) (EFTcount=0) failed!"
         write(unit=logf,fmt="((15x,A11,3(15x,A11)))") &
              & "Born       ", "finite part", "single pole", "double pole"
         write(unit=logf,fmt="((A12,4(3x,E23.16E3)))") &
              & "GoSam      :", gsres(ieft,0), gsres(ieft,1), gsres(ieft,2), gsres(ieft,3)
         write(unit=logf,fmt="((A12,4(3x,E23.16E3)))") &
              & "Analytical :", refres(ieft,0), refres(ieft,1), refres(ieft,2), refres(ieft,3)
         write(unit=logf,fmt="((A12,4(3x,E23.16E3)))") &
              & "DIFFERENCE :", diff(ieft,0), diff(ieft,1), diff(ieft,2), diff(ieft,3)
         success = .false.
      end if

   end do

   if (success) then
      write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
   else
      write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
   end if

   close(unit=logf)
  
   call exitgolem()
   
 contains
   

subroutine analytic_amp(scale2,amp)
  use Hbb_SMEFT_model
  use Hbb_SMEFT_config, only: EFTcount
  implicit none
  real(ki), intent(in) :: scale2
  real(ki), dimension(0:3), intent(out) :: amp
  real(ki), dimension(0:3) :: coeffSM
  real(ki), dimension(0:3) :: coeffbphi, coeffphiG
  real(ki), dimension(0:3) :: coeffbphibphi, coeffbphiphiG, coeffphiGphiG
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  call avh_olo_a0c(a0b, &
       & complex(mdlMQB**2,0._ki))
  a0b(0) = a0b(0) + log(scale2)*a0b(1)
  
  call avh_olo_b0c(b0hbb, &
       & complex(mdlMH**2,0._ki), &
       & complex(mdlMQB**2,0._ki), &
       & complex(mdlMQB**2,0._ki))
  b0hbb(0) = b0hbb(0) + log(scale2)*b0hbb(1)
  
  call avh_olo_b0c(b0b0b, &
       & complex(mdlMQB**2,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(mdlMQB**2,0._ki))
  b0b0b(0) = b0b0b(0)+ log(scale2)*b0b0b(1)

  call avh_olo_b0c(b0h00, &
       & complex(mdlMH**2,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(0._ki,0._ki))
  b0h00(0) = b0h00(0)+ log(scale2)*b0h00(1)
  
  call avh_olo_c0c(c0bbhb0b, &
       & complex(mdlMQB**2,0._ki), &
       & complex(mdlMQB**2,0._ki), &
       & complex(mdlMH**2,0._ki), &
       & complex(mdlMQB**2,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(mdlMQB**2,0._ki))
  c0bbhb0b(0) = c0bbhb0b(0) + log(scale2)*c0bbhb0b(1)

  call avh_olo_c0c(c0bbh0b0, &
       & complex(mdlMQB**2,0._ki), &
       & complex(mdlMQB**2,0._ki), &
       & complex(mdlMH**2,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(mdlMQB**2,0._ki), &
       & complex(0._ki,0._ki))
  c0bbh0b0(0) = c0bbh0b0(0) + log(scale2)*c0bbh0b0(1)
  
  coeffSM = analytic_coeff_SM(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  coeffbphi = analytic_coeff_cbphi(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  coeffphiG = analytic_coeff_cphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  coeffbphibphi= analytic_coeff_cbphicbphi(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  coeffbphiphiG = analytic_coeff_cbphicphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  coeffphiGphiG = analytic_coeff_cphiGcphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0)
  
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


function analytic_coeff_SM(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
  use avh_olo
  use Hbb_SMEFT_config, only: renormalisation
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  prefac = sqrt(8._ki)*mdlGf*CA*mdlymb**2
  
  amp1lbare = 2._ki*real(prefac*CF*( &
       & (-4._ki*mdlMQB**2*b0hbb &
       & + 2._ki*(mdlMH**2-2._ki*mdlMQB**2)*b0b0b &
       & - (8._ki*mdlMQB**4-6._ki*mdlMQB**2*mdlMH**2+mdlMH**4)*c0bbhb0b)))

  if(renormalisation.eq.1)then
     ampct(0) =  2._ki*prefac*CF*( &
          & (4._ki*mdlMQB**2-mdlMH**2)*(3._ki*log(scale2/mdlMQB**2)+5._ki))
     ampct(1) =  2._ki*prefac*CF*( &
          & (4._ki*mdlMQB**2-mdlMH**2)*(3._ki))
     ampct(2) = 0._ki
  else
     ampct = 0._ki
  end if
  
  amp(0) = prefac*(mdlMH**2-4._ki*mdlMQB**2)
  amp(1) = amp1lbare(0) + ampct(0)
  amp(2) = amp1lbare(1) + ampct(1)
  amp(3) = 0._ki
  
end function analytic_coeff_SM


function analytic_coeff_cbphi(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlmueft
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  prefac = sqrt(sqrt(2._ki)/mdlGf)*CA*mdlymb
  
  amp1lbare = 2._ki*real(prefac*CF*2._ki*( &
       & 4._ki*mdlMQB**2*b0hbb &
       & - 2._ki*(mdlMH**2-2._ki*mdlMQB**2)*b0b0b &
       & + (8._ki*mdlMQB**4-6._ki*mdlMQB**2*mdlMH**2+mdlMH**4)*c0bbhb0b))

  if(renormalisation.eq.1)then
     ampct(0) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*( &
          &   9._ki/2._ki*log(scale2/mdlMQB**2) &
          & + 3._ki/2._ki*log(scale2/mdlmueft**2) &
          & + 8._ki))
     ampct(1) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*(6._ki))
     ampct(2) = 0._ki
  else
     ampct = 0._ki
  end if
  
  amp(0) = -prefac*2._ki*(mdlMH**2-4._ki*mdlMQB**2)
  amp(1) = amp1lbare(0) + ampct(0)
  amp(2) = amp1lbare(1) + ampct(1)
  amp(3) = 0._ki
  
end function analytic_coeff_cbphi


function analytic_coeff_cphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlmueft
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  prefac = 4._ki*CA*mdlymb/mdlMQB
  
  amp1lbare = 2._ki*real(prefac*CF*(mdlMH**2-4._ki*mdlMQB**2)*( &
       & -mdlMQB**2*mdlMH**2*c0bbh0b0+2._ki*mdlMQB**2*b0b0b+a0b))

  if(renormalisation.eq.1)then
     ampct(0) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*mdlMQB*mdlymb*( &
          & - 3._ki*log(scale2/mdlmueft**2) - 1._ki))
     ampct(1) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*mdlMQB*mdlymb*(-3._ki))
     ampct(2) = 0._ki
  else
     ampct = 0._ki
  end if

  amp(0) = 0._ki
  amp(1) = amp1lbare(0) + ampct(0)
  amp(2) = amp1lbare(1) + ampct(1)
  amp(3) = 0._ki
  
end function analytic_coeff_cphiG


function analytic_coeff_cbphicbphi(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
 use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlmueft
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  prefac = CA/2._ki/mdlGf**2

  amp1lbare = 2._ki*real(prefac*CF*( &
       & - 4._ki*mdlMQB**2*b0hbb &
       & + 2._ki*(mdlMH**2-2._ki*mdlMQB**2)*b0b0b &
       & - (8._ki*mdlMQB**4-6._ki*mdlMQB**2*mdlMH**2+mdlMH**4)*c0bbhb0b))

  if(renormalisation.eq.1)then
     ampct(0) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*( &
          & - 3._ki/2._ki*log(scale2/mdlMQB**2) &
          & - 3._ki/2._ki*log(scale2/mdlmueft**2) &
          & - 3._ki))
     ampct(1) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*(-3._ki))
     ampct(2) = 0._ki
  else
     ampct = 0._ki
  end if

  amp(0) = prefac*(mdlMH**2-4._ki*mdlMQB**2)
  amp(1) = amp1lbare(0) + ampct(0)
  amp(2) = amp1lbare(1) + ampct(1)
  amp(3) = 0._ki
  
end function analytic_coeff_cbphicbphi


function analytic_coeff_cbphicphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlmueft
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0
  
  prefac = sqrt(sqrt(8._ki)/mdlGf**3)*CA/mdlMQB
  
  amp1lbare = 2._ki*real(prefac*CF*(mdlMH**2-4._ki*mdlMQB**2)*( &
       & mdlMQB**2*mdlMH**2*c0bbh0b0-2._ki*mdlMQB**2*b0b0b-a0b))

  if(renormalisation.eq.1)then
     ampct(0) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*mdlMQB*mdlymb*( &
          & 3._ki*log(scale2/mdlmueft**2) + 1._ki))
     ampct(1) =  2._ki*prefac*CF*( &
          & (mdlMH**2-4._ki*mdlMQB**2)*mdlMQB*mdlymb*(3._ki))
     ampct(2) = 0._ki
  else
     ampct = 0._ki
  end if

  amp(0) = 0._ki
  amp(1) = amp1lbare(0) + ampct(0)
  amp(2) = amp1lbare(1) + ampct(1)
  amp(3) = 0._ki

end function analytic_coeff_cbphicphiG


function analytic_coeff_cphiGcphiG(scale2, a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0) result(amp)
  use Hbb_SMEFT_model, only: mdlMH, mdlGf, mdlymb, mdlmueft
  use Hbb_SMEFT_color, only: CA, CF
  implicit none
  real(ki) :: scale2, prefac
  real(ki), dimension(0:3) :: amp
  real(ki), dimension(0:2):: amp1lbare, ampct
  complex(ki), dimension(0:2) :: a0b, b0hbb, b0b0b, b0h00, c0bbhb0b, c0bbh0b0

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
