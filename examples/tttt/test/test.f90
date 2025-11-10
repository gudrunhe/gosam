program test
use tttt_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use tttt_matrix, only: initgolem, exitgolem
use tttt_kinematics, only: inspect_kinematics, init_event
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

if (any(isnan(gosam_amp))) then
	write(unit=logf,fmt="(A10)") "NaN error!"
	success = .false.
end if

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
   use tttt_kinematics, only: adjust_kinematics
   use tttt_model, only: mT
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2
 
   vecs(1,:) = (/ 250.0_ki, 0.0_ki, 0.0_ki, 182.1827653758720_ki /)
   vecs(2,:) = (/ 250.0_ki, 0.0_ki, 0.0_ki, -182.1827653758720_ki /)
   vecs(3,:) = (/ 250.0_ki,  159.0887788632981_ki, &
               &  -21.56257847362032_ki, 86.11838159971188_ki /)
   vecs(4,:) = (/ 250.0_ki, -159.0887788632983_ki, &
               & 21.56257847362032_ki, -86.11838159971194_ki /)
   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2 = mT*mT

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use tttt_config, only: renormalisation, convert_to_thv
   use tttt_model, only: set_parameter
   implicit none
   integer :: ierr = 0
   
   renormalisation = 1


   call set_parameter("mT", 171.2_ki, 0.0_ki, ierr)

   call set_parameter("Nf", 5.0_ki, 0.0_ki, ierr)
   call set_parameter("Nfgen", 1.0_ki, 0.0_ki, ierr)

   convert_to_thv = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use tttt_matrix, only: samplitude
   use tttt_model, only: mT
   implicit none
   ! The amplitude should be a homogeneous function
   ! in the energy dimension and scale like
   !     A(Q*E) = A(E)
   ! We use this fact as
   !  - an additional test for the amplitude
   !  - to enhance precision
   real(ki), parameter :: Q = 172.0_ki
   !real(ki), parameter :: Q = 1.0E+00

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   real(ki), dimension(4, 4) :: xvecs
   real(ki) :: xscale2
   integer :: prec

   ! rescaling of all dimensionful quantities that enter the calculation
   ! Note: it's not safe to use 'set_parameter' for this, because then
   !       also all dependent parameters are recalculated
   xvecs = vecs / Q
   xscale2 = scale2 / Q ** 2
   mT = mT / Q

   call samplitude(xvecs, xscale2, amp, prec)

   mT = mT * Q

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use tttt_kinematics, only: dotproduct, lo_qcd_couplings
   use tttt_matrix, only: ir_subtraction
   use tttt_model, only: mT
   use tttt_color, only: CA, TR
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   ! Computed with Madgraph5 (version 2.3.3)
   amp(0) = 22.56248

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
