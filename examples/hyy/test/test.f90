program test
use hyy_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams, dbl
use hyy_matrix, only: initgolem, exitgolem
use hyy_kinematics, only: inspect_kinematics, init_event
use hyy_groups, only: virt_flags
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

real(ki), parameter :: eps = 1.0E-4_ki

logical :: success

real(ki), dimension(5, 4) :: vecs
real(ki) :: scale2

type(virt_flags) :: flags

double precision, dimension(0:3) :: gosam_amp, ref_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call setup_parameters(flags)
call initgolem()

call load_reference_kinematics(vecs, scale2)

call init_event(vecs)
call inspect_kinematics(logf)
call compute_gosam_result(vecs, scale2, gosam_amp)
call compute_reference_result(flags, vecs, scale2, ref_amp)

diff = abs(rel_diff(gosam_amp, ref_amp))

if (diff(1) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of Amplitude failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
   success = .false.
end if

if (success) then
   write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
else
   write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
end if

close(unit=logf)

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   close(unit=gosamlogf)
end if

call exitgolem()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use hyy_kinematics, only: adjust_kinematics
   use hyy_model, only: mH
   implicit none
   real(ki), dimension(3, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(:,:) = 0.0_ki
   vecs(1,1) = mH
   vecs(2,1) = 0.5_ki * mH
   vecs(2,2) = 0.3_ki * mH
   vecs(2,4) = 0.4_ki * mH
   vecs(3,1)   =   vecs(2,1)
   vecs(3,2:4) = - vecs(2,2:4)

   ! scale is arbitrary in this example
   scale2 = 71.2_ki**2
end  subroutine load_reference_kinematics

subroutine     setup_parameters(flags)
   use hyy_config
   use hyy_model, only: mH, mT, mW, mZ, alpha
   use hyy_groups, only: virt_flags, update_flags
   implicit none
   type(virt_flags), intent(out) :: flags

   mH    = 124.5_ki

   mT    =  172.5_ki
   mW    =  80.398_ki
   mZ    =  91.1876_ki
   alpha =  0.00729735299_ki

   renormalisation = 0

   flags%eval_bosonic   = .false.
   flags%eval_fermionic = .true.

   call update_flags(flags)

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use hyy_matrix, only: samplitude
   use hyy_model, only: alpha, mH, e, sw, mW
   use hyy_config, only: include_symmetry_factor
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   double precision :: pi, prefactor, GF

   pi = 4.0d0 * atan(1.0d0)
   GF =  pi * alpha / sqrt(2.0_ki) / sw**2 / mW**2

   call samplitude(vecs, real(scale2, dbl), amp, prec, ok)
      
   ! factor 1/16/pi/mH for converting to width
   ! factor 2 for summing over helicities
   amp = amp * 2.0_ki / (16.0d0 * pi * mH)
   ! we have set e=1 in the calculation.
   ! furthermore we factored out alpha/2/pi in the amplitude
   amp = amp * alpha ** 3 / pi
   ! we also need to correct for the symmetry factor if it's not done already
   if (.not. include_symmetry_factor) amp = 0.5_ki * amp

   write(logf,*) "GOSAM AMP(1):", amp(1)

   prefactor = mH**3 * GF * alpha**2 / sqrt(2.0d0) / 128.0d0 / pi**3

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "Result includes the prefactor:"
      write(ch,*) "mH^3*GF*alpha^2/sqrt(2)/128/pi^3=", prefactor
      write(ch,*) "GOSAM     AMP(1):", amp(1)
   end do

end subroutine compute_gosam_result

subroutine     compute_reference_result(flags, vecs, scale2, amp)
   use hyy_groups, only: virt_flags
   implicit none

   type(virt_flags), intent(in) :: flags
   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   amp(:) = 0.0d0
   amp(1) = gammaHyy(flags)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(1):", amp(1)
   end do

end subroutine compute_reference_result

pure elemental function rel_diff(a, b)
   implicit none

   double precision, intent(in) :: a, b
   double precision :: rel_diff

   if (a.eq.0.0_ki .and. b.eq.0.0_ki) then
      rel_diff = 0.0_ki
   else
      rel_diff = 2.0_ki * (a-b) / (abs(a)+abs(b))
   end if
end  function rel_diff

!pure function GammaHyy(flags) result(Gamma)
function GammaHyy(flags) result(Gamma)
   use hyy_model, only: mH, mT, mW, alpha, sw, NC
   use hyy_groups, only: virt_flags
   implicit none

   type(virt_flags), intent(in) :: flags

   double precision :: Gamma

   double complex :: amps
   double precision :: tauT, tauW, GF, pi

   pi = 4.0d0 * atan(1.0d0)
   GF =  pi * alpha / sqrt(2.0_ki) / sw**2 / mW**2

   tauT = mH**2/4.0d0/mT**2
   tauW = mH**2/4.0d0/mW**2

   amps = (0.0d0, 0.0d0)

   if (flags%eval_fermionic) &
   & amps = amps + NC * (2.0d0/3.0d0)**2 * AHq(tauT)
   if (flags%eval_bosonic) &
   & amps = amps + AHW(tauW)

   Gamma = mH**3 * real(amps*conjg(amps), kind(1.d0))
   Gamma = Gamma * GF * alpha**2 / sqrt(2.0d0) / 128.0d0 / pi**3
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
