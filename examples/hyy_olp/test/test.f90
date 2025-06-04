program test
use olp_module
use config, only: debug_lo_diagrams, debug_nlo_diagrams
use, intrinsic :: iso_c_binding
implicit none

character(kind=c_char,len=13) :: contract_file_name = "../hyy.olc"

integer, parameter :: ki = kind(1.0d0)

! unit of the log file
integer, parameter :: logf = 28
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch, ierr

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(60) :: blha_kinematics
real(ki) :: renorm_scale

double precision, dimension(0:59) :: gosam_amp, ref_amp
real(ki) :: diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

! if (debug_lo_diagrams .or. debug_nlo_diagrams) then
!    open(file="gosam.log", unit=gosamlogf)
! end if

call OLP_Start(contract_file_name,ierr)

call OLP_SetParameter(c_char_"mH"//c_null_char, 124.5_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"mT"//c_null_char, 172.5_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"mW"//c_null_char, 80.398_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"mZ"//c_null_char, 91.1876_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"wW"//c_null_char, 0.0_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"wZ"//c_null_char, 0.0_ki, 0.0_ki, ierr)
call OLP_SetParameter(c_char_"alpha"//c_null_char, 0.00729735299_ki, 0.0_ki, ierr)

call load_reference_kinematics(blha_kinematics, renorm_scale)
call compute_gosam_result(blha_kinematics, renorm_scale, gosam_amp)
call compute_reference_result(ref_amp)

do ic = 1, 2
    ch = channels(ic)
    write(ch,'(A58)') "----------------------------------------------------"
end do

diff = 2.0d0 * (ref_amp(1)-gosam_amp(2)) / (abs(ref_amp(1))+abs(gosam_amp(2)))

if (diff .gt. eps) then
    write(unit=logf,fmt="(A3,1x,A40)") "==>", &
    & "Comparison of LO failed!"
    write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff
    success = .false.
end if

if (success) then
   write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
else
   write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
end if

call OLP_Finalize()
close(unit=logf)

contains

pure subroutine load_reference_kinematics(vecs, scale)
   use model, only: mH
   implicit none
   real(ki), dimension(50), intent(out) :: vecs
   real(ki), intent(out) :: scale

   vecs(:) = 0.0_ki
   vecs(1) = mH
   vecs(5) = mH
   vecs(6) = 0.5_ki * mH
   vecs(7) = 0.3_ki * mH
   vecs(9) = 0.4_ki * mH
   vecs(11)   =   vecs(6)
   vecs(12:15) = - vecs(7:10)

   ! scale is arbitrary in this example
   scale = 71.2_ki
end  subroutine load_reference_kinematics

subroutine     compute_gosam_result(vecs, scale, amp)
   use model, only: alpha, mH, e, sw, mW
   implicit none

   real(ki), dimension(50), intent(in) :: vecs
   real(ki), intent(in) :: scale
   double precision, dimension(0:59), intent(out) :: amp
   real(ki) :: prec

   logical :: ok

   double precision :: pi, prefactor, GF

   pi = 4.0d0 * atan(1.0d0)
   GF =  pi * alpha / sqrt(2.0_ki) / sw**2 / mW**2

   call OLP_EvalSubProcess2(0, vecs, scale, amp, prec)

   ! factor 1/16/pi/mH for converting to width
   ! factor 2 for summing over helicities
   amp = amp * 2.0_ki / (16.0d0 * pi * mH)
   ! we have set e=1 in the calculation.
   ! furthermore we factored out alpha/2/pi in the amplitude
   amp = amp * alpha ** 3 / pi

   write(logf,*) "GOSAM AMP(1):", amp(2)

   prefactor = mH**3 * GF * alpha**2 / sqrt(2.0d0) / 128.0d0 / pi**3

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "Result includes the prefactor:"
      write(ch,*) "mH^3*GF*alpha^2/sqrt(2)/128/pi^3=", prefactor
      write(ch,*) "GOSAM     AMP(1):", amp(2)
   end do

end subroutine compute_gosam_result

subroutine     compute_reference_result(amp)
   implicit none
   double precision, dimension(0:59), intent(out) :: amp

   amp(:) = 0.0d0
   amp(1) = gammaHyy()

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(1):", amp(1)
   end do

end subroutine compute_reference_result

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

function GammaHyy() result(Gamma)
   use model, only: mH, mT, mW, alpha, sw, NC
   implicit none

   double precision :: Gamma

   double complex :: amps
   double precision :: tauT, tauW, GF, pi

   pi = 4.0d0 * atan(1.0d0)
   GF =  pi * alpha / sqrt(2.0_ki) / sw**2 / mW**2

   tauT = mH**2/4.0d0/mT**2
   tauW = mH**2/4.0d0/mW**2

   amps = (0.0d0, 0.0d0)

   amps = amps + NC * (2.0d0/3.0d0)**2 * AHq(tauT) + AHW(tauW)

   Gamma = mH**3 * real(amps*conjg(amps), kind(1.d0))
   Gamma = Gamma * GF * alpha**2 / sqrt(2.0d0) / 128.0d0 / pi**3
   Gamma = Gamma * 2.0d0 ! (two non-zero helicities compared to hyy example)
end function GammaHyy

pure function AHq(tau) result(amp)
   implicit none
   double precision, intent(in) :: tau
   double complex :: amp

   amp = 2.0d0/tau**2 * (tau + (tau - 1.0d0) * f(tau))
end function  AHq

pure function AHW(tau) result(amp)
   implicit none
   double precision, intent(in) :: tau
   double complex :: amp

   amp = -1.0d0/tau**2 * (2.0d0 * tau**2 + 3.0d0 * tau &
       & + 3.0d0 * (2.0d0 * tau - 1.0d0) * f(tau))
end function  AHW

pure function f(tau)
   implicit none
   double precision, intent(in) :: tau
   double complex :: f
   double complex :: ctau, ipi
   double precision :: sq

   ctau = cmplx(tau, 0.0d0, kind(1.0d0))

   if (tau .le. 1.0d0) then
        f = (asin(abs(sqrt(ctau))))**2
   else
        ipi = cmplx(0.0d0, 4.0d0 * atan(1.0d0), kind(1.0d0))
        sq = sqrt(1.0d0 - 1.0d0/tau)

        f = -0.25d0 * (log((1.0d0+sq)/(1.0d0-sq)) - ipi)**2
   end if
end function f

end program test
