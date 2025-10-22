program test
use udhud_feynman_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams, dbl
use udhud_feynman_kinematics, only: f_inspect_kinematics => inspect_kinematics, f_init_event => init_event
use udhud_unitary_kinematics, only: u_inspect_kinematics => inspect_kinematics, u_init_event => init_event
use udhud_feynman_matrix, only: f_initgolem => initgolem, f_exitgolem => exitgolem
use udhud_unitary_matrix, only: u_initgolem => initgolem, u_exitgolem => exitgolem
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

double precision, dimension(0:3) :: feynman_amp, unitary_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call f_initgolem()
call u_initgolem()

call load_reference_kinematics(vecs, scale2)

call f_init_event(vecs)
call f_inspect_kinematics(logf)
call u_init_event(vecs)

call compute_feynman_result(vecs, scale2, feynman_amp)
call compute_unitary_result(vecs, scale2, unitary_amp)

if (any(isnan(feynman_amp)).or.any(isnan(unitary_amp))) then
   write(unit=logf,fmt="(A10)") "NaN error!"
   success = .false.
end if

diff = abs(rel_diff(feynman_amp, unitary_amp))

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

if (diff(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A30)") "==>", &
   & "Comparison of NLO/double pole failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
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

call f_exitgolem()
call u_exitgolem()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   implicit none
   real(ki), dimension(5, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(1,:) = (/ 250.00000000000000_ki, 0.0000000000000000_ki, 0.0000000000000000_ki, 250.00000000000000_ki /)
   vecs(2,:) = (/ 250.00000000000000_ki, 0.0000000000000000_ki, 0.0000000000000000_ki, -250.00000000000000_ki /)
   vecs(3,:) = (/ 175.14149003884074_ki, 98.768323895659933_ki, -67.132235585908631_ki, -28.064616033457614_ki /)
   vecs(4,:) = (/ 156.35384591123687_ki, -67.756855590239823_ki, 39.542341419584517_ki ,-135.24768717732368_ki /)
   vecs(5,:) = (/ 168.50466404992241_ki, -31.011468305420120_ki, 27.589894166324104_ki ,163.31230321078129_ki /)

   ! scale is arbitrary in this example
   scale2 = 500.0_ki**2
end  subroutine load_reference_kinematics

subroutine     compute_feynman_result(vecs, scale2, amp)
   use udhud_feynman_matrix, only: samplitude
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   call samplitude(vecs, real(scale2, dbl), amp, prec, ok)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "FEYNMAN     AMP(0):       ", amp(0)
      write(ch,*) "FEYNMAN     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "FEYNMAN     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "FEYNMAN     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do

end subroutine compute_feynman_result

subroutine     compute_unitary_result(vecs, scale2, amp)
   use udhud_unitary_matrix, only: samplitude
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   call samplitude(vecs, real(scale2, dbl), amp, prec, ok)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "UNITARY     AMP(0):       ", amp(0)
      write(ch,*) "UNITARY     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "UNITARY     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "UNITARY     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do

end subroutine compute_unitary_result

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
end program test
