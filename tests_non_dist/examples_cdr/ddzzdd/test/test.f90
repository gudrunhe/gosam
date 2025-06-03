program test
use ddzzdd_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use ddzzdd_matrix, only: initgolem, exitgolem
use ddzzdd_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(6, 4) :: vecs
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
   use ddzzdd_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(6, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(1,:) = (/500.0_ki,  0.0_ki, 0.0_ki,  500.0_ki/)
   vecs(2,:) = (/500.0_ki,  0.0_ki, 0.0_ki, -500.0_ki/)
   vecs(3,:) = (/123.87709720686949_ki,  -20.926527367427127_ki,  &
                & 37.950968817889148_ki,  -71.778048779025283_ki/)
   vecs(4,:) = (/323.98354709846132_ki,  -98.332301701286937_ki, &
                & -285.89265371627789_ki,  72.430908041335670_ki/)
   vecs(5,:) = (/144.26364542991371_ki,  -100.25572827408648_ki,  &
                & -92.518531950550354_ki,  46.915984340898092_ki/)
   vecs(6,:) = (/407.875710264756_ki,  219.514557342801_ki,  &
                & 340.460216848939_ki,  -47.568843603209_ki/)

   scale2 = 500.0_ki ** 2
end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ddzzdd_config, only: renormalisation
   implicit none

   renormalisation = 0

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ddzzdd_matrix, only: samplitude
   use ddzzdd_model, only: mW, wW, mH, mBMS
   implicit none

   real(ki), dimension(6, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use ddzzdd_kinematics, only: dotproduct
   use ddzzdd_model, only: GF, mW, mZ, wW, wZ
   implicit none

   real(ki), dimension(6, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   ! Computed with Madgraph (cross-checked against GoSam with different reference vectors)
   amp(0) = 4.4159483504686758E-008

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
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
