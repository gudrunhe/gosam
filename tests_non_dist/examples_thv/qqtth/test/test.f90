program test
use qqtth_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use qqtth_matrix, only: initgolem, exitgolem
use qqtth_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(5, 4) :: vecs
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

pure subroutine load_reference_kinematics(vecs, scale2)
   use qqtth_kinematics, only: dotproduct, adjust_kinematics
   implicit none
   real(ki), dimension(5, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2


   vecs(1,:) = (/ 7000.0_ki, 0.0_ki, 0.0_ki, 7000.0_ki/)
   vecs(2,:) = (/ 7000.0_ki, 0.0_ki, 0.0_ki, -7000.0_ki/)
   vecs(3,:) = (/ 1510.822629385984_ki, -818.6820459804896_ki, &
               &  162.3544247395991_ki,  1253.140361580239_ki /)
   vecs(4,:) = (/ 6315.019901181462_ki, 130.7143483231204_ki, &
               &  5883.824316614950_ki,-2283.351064263005_ki /)
   vecs(5,:) = (/ 6174.157469432554_ki, 687.9676976573693_ki, &
               & -6046.178741354550_ki, 1030.210702682766_ki /)  
   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use qqtth_model, only: set_parameter
   implicit none
   integer :: ierr = 0

   call set_parameter("mH", 125.0_ki, 0.0_ki, ierr)
   call set_parameter("mT", 171.2_ki, 0.0_ki, ierr)
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use qqtth_matrix, only: samplitude
   use qqtth_model, only: mT
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   amp(0)   = 3.7372932537435852D-009
   amp(1)   = 1.2331945765090018D0*amp(0)     
   amp(2)   = 0.16106642465025001D0*amp(0)     
   amp(3)   = -3.3773727880779265D-002*amp(0)

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
