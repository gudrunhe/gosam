program test
use uudd_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use uudd_matrix, only: initgolem, exitgolem
use uudd_kinematics, only: inspect_kinematics, init_event
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

pure subroutine load_reference_kinematics(vecs, scale2)
   use uudd_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was specified in arXiv:1103.0621v1
   vecs(1,:) = (/102.6289752320661_ki, 0.0_ki, 0.0_ki,  102.6289752320661_ki/)
   vecs(2,:) = (/102.6289752320661_ki, 0.0_ki, 0.0_ki, -102.6289752320661_ki/)
   vecs(3,:) = (/102.6289752320661_ki, -85.98802977488269_ki, &
             &  -12.11018104528534_ki,  54.70017191625945_ki/)
   vecs(4,:) = (/102.6289752320661_ki,  85.98802977488269_ki, &
             &   12.11018104528534_ki, -54.70017191625945_ki/)

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   ! The given reference renormalisation scale is 80 GeV
   scale2 = 91.188_ki ** 2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use uudd_config, only: renormalisation
   use uudd_model, only: Nf, Nfgen
   implicit none

   renormalisation = 1

   Nf    = 2.0_ki
   Nfgen = 2.0_ki
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use uudd_matrix, only: samplitude
   implicit none
   ! The amplitude should be a homogeneous function
   ! in the energy dimension and scale like
   !     A(Q*E) = A(E)
   ! We use this fact as
   !  - an additional test for the amplitude
   !  - to enhance precision
   real(ki), parameter :: Q = 205.0_ki

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   real(ki), dimension(4, 4) :: xvecs
   real(ki) :: xscale2
   integer :: prec

   ! rescaling of all dimensionful quantities that enter the calculation
   xvecs = vecs / Q
   xscale2 = scale2 / Q ** 2

   call samplitude(xvecs, xscale2, amp, prec)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use uudd_matrix, only: ir_subtraction
   use uudd_kinematics, only: dotproduct
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision, parameter :: alphas = 0.13d0
   double precision :: s, that, uhat, aa, pi, gs

   pi = 4.0d0 * atan(1.0d0)
   gs = sqrt(4.0d0 * pi * alphas)

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   that = -2.0d0 * dotproduct(vecs(1,:), vecs(3,:))/s
   uhat = -2.0d0 * dotproduct(vecs(1,:), vecs(4,:))/s
   
   amp(0) = 4.0d0/9.0d0 * (that*that+uhat*uhat)
   amp(1) = -0.44023547006851060D-001 / (alphas/2.0d0/pi) / gs**4
   call ir_subtraction(vecs, scale2, amp(2:3))

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
