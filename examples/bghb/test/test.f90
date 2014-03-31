program test
use bghb_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use bghb_matrix, only: initgolem, exitgolem
use bghb_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(4, 4) :: vecs
real(ki) :: scale2

double precision, dimension(0:3) :: gosam_amp, ref_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call setup_parameters()
call initgolem()

call load_reference_kinematics(vecs, scale2)

call init_event(vecs)
call inspect_kinematics(logf)

call compute_gosam_result(vecs, scale2, gosam_amp)
call compute_reference_result(vecs, scale2, ref_amp)

diff = abs(rel_diff(gosam_amp, ref_amp))

if (diff(0) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of LO failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
   success = .false.
end if

if (diff(1) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/finite part failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(1)
   success = .false.
end if

if (diff(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/single pole failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
   success = .false.
end if

if (diff(3) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A30)") "==>", &
   & "Comparison of NLO/double pole failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(3)
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

!pure 
subroutine load_reference_kinematics(vecs, scale2)
   use bghb_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was specified in 1103.0621v1 [hep-ph]
   vecs(1,:) = (/250.0_ki,  0.0_ki, 0.0_ki,  250.0_ki/)
   vecs(2,:) = (/250.0_ki,  0.0_ki, 0.0_ki, -250.0_ki/)
   vecs(3,:) = (/264.4_ki, -83.84841332241601_ki, -86.85350630148753_ki, &
             &  -202.3197272300720_ki/)
   vecs(4,:) = (/235.6_ki,  83.84841332241601_ki,  86.85350630148753_ki, &
             &   202.3197272300720_ki/)

   call adjust_kinematics(vecs)

   scale2 = 91.188_ki ** 2
end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use bghb_config, only: renormalisation !, &
     !        & samurai_test, samurai_verbosity, samurai_scalar, &
     !        & samurai_group_numerators, &
     !        & reduction_interoperation
   use bghb_model, only: mBMS, mH, sw, cw, alpha, mW, mZ
   implicit none

   real(ki), parameter :: vev = 246.2185_ki
   real(ki), parameter :: my_sw = 0.47229_ki
   real(ki), parameter :: pi =  3.14159265358979323846264338327948_ki

   renormalisation = 1

   !reduction_interoperation = 0
   !samurai_group_numerators = .true.

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   alpha = 1.0_ki/(4.0_ki*pi)
   mBMS = 2.937956_ki
   mH = 120.0_ki
   mW = vev / my_sw * 0.5_ki
   mZ = mW / sqrt(1.0_ki - my_sw*my_sw)

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use bghb_matrix, only: samplitude
   use bghb_model, only: mW, wW, mH, mBMS
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)

   ! Renormalization of the Yukawa Coupling
   ! See Appendix D of:
   ! Campbell, Ellis, Maltoni, Willenbrock; hep-ph/0204093
   amp(2) = amp(2) - 4.0_ki * amp(0)
   amp(1) = amp(1) - 4.0_ki/3.0_ki * amp(0)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use bghb_kinematics, only: dotproduct
   use bghb_matrix, only: ir_subtraction
   use bghb_model, only: mW, wW, sw, NC, mH, mBMS, alpha
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision :: s, t, u, l, yB, vev
   double precision, dimension(2:3) :: irp

   ! MCFM/MadLoop results
   double precision, parameter :: pi = &
   & 3.14159265358979323846264338327948_ki
   double precision, parameter :: alpha_s = 0.118d0
   double precision, parameter :: a0 =  3.11285493372811162D-007
   double precision, parameter :: c0 = -1.4107608671538634D-007
   double precision, parameter :: c1 =  6.99063829676930686D-008
   double precision, parameter :: c2 = -3.31275018959846227E-008

   call ir_subtraction(vecs, scale2, irp)

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   t = -2.0d0 * dotproduct(vecs(1,:), vecs(3,:)) + mH**2
   u = mH**2 - s - t

   vev = 0.5d0 * sw * mW
   yB = mBMS / vev

   amp(0) = - 0.25_ki * yB**2 * (mH**4 + u**2) / s / t / 24.0d0

   amp(1) = c0/a0 * amp(0)/(alpha_s/2/pi)
   amp(2) = c1/a0 * amp(0)/(alpha_s/2/pi)
   amp(3) = -17.0d0/3.0d0 * amp(0)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
      write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)
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

end program test
