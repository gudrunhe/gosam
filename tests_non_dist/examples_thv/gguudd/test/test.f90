program test
use gguudd_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use gguudd_matrix, only: initgolem, exitgolem
use gguudd_kinematics, only: inspect_kinematics, init_event
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
   use gguudd_kinematics, only: adjust_kinematics
   use gguudd_model, only: mT
   implicit none
   real(ki), dimension(6, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2
 
   vecs(1,:) = (/  250.00000000000000_ki,        0.0000000000000000_ki,&
               &   0.0000000000000000_ki,        250.00000000000000_ki /)
   vecs(2,:) = (/  250.00000000000000_ki,        0.0000000000000000_ki,&
               &   0.0000000000000000_ki,       -250.00000000000000_ki /)
   vecs(3,:) = (/  48.269226098395414_ki,        33.925647459600142_ki,&
               &  -16.205942009755621_ki,        30.271043526138651_ki /)
   vecs(4,:) = (/  201.71798751288574_ki,       -158.41185336971927_ki,&
               &  -96.998556922243523_ki,       -78.658191901553678_ki /)
   vecs(5,:) = (/  143.29464919632304_ki,        66.707659986339593_ki,&
               &   119.98265934419534_ki,       -41.080482520766196_ki /)
   vecs(6,:) = (/  106.71813719239589_ki,        57.778545923779149_ki,&
               &  -6.7781604121960353_ki,        89.467630896181149_ki /)

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2 = mT*mT

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use gguudd_config, only: renormalisation, convert_to_thv !, &
   use gguudd_model, only: Nf, Nfgen, mT
   implicit none

   renormalisation = 1
   convert_to_thv = .false.

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use gguudd_matrix, only: samplitude
   use gguudd_model, only: mT
   implicit none
   ! The amplitude should be a homogeneous function
   ! in the energy dimension and scale like
   !     A(Q*E) = A(E)
   ! We use this fact as
   !  - an additional test for the amplitude
   !  - to enhance precision
   real(ki), parameter :: Q = 172.0_ki
   !real(ki), parameter :: Q = 1.0E+00

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
   use gguudd_kinematics, only: dotproduct, lo_qcd_couplings
   use gguudd_matrix, only: ir_subtraction
   use gguudd_model, only: mT
   use gguudd_color, only: CA, TR
   implicit none

   real(ki), dimension(6, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   ! Computed with GoSam abbrev.color=none
   amp(0) = 1.6526066702415756E-008

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
