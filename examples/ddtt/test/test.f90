program test
use ddtt_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use ddtt_matrix, only: initgolem, exitgolem
use ddtt_kinematics, only: inspect_kinematics, init_event
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
   use ddtt_kinematics, only: adjust_kinematics
   use ddtt_model, only: mT
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2
 
   vecs(1,:) = (/ 74.7646520969852_ki, 0.0_ki, 0.0_ki, 74.7646520969852_ki /)
   vecs(2,:) = (/ 6067.88254935176_ki, 0.0_ki, 0.0_ki, -6067.88254935176_ki /)
   vecs(3,:) = (/ 5867.13826404309_ki,  16.7946967430656_ki, &
               &  169.437140279981_ki, -5862.12966020487_ki /)
   vecs(4,:) = (/ 275.508937405653_ki, -16.7946967430656_ki, &
               & -169.437140279981_ki, -130.988237049907_ki /)
   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2 = mT*mT

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ddtt_config, only: renormalisation, convert_to_cdr !, &
        !     & samurai_test, samurai_verbosity, samurai_scalar
   use ddtt_model, only: Nf, Nfgen, mT
   implicit none

   renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   mT = 172.5_ki

   Nf    = 5.0_ki
   Nfgen = 1.0_ki

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ddtt_matrix, only: samplitude
   use ddtt_model, only: mT
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
   xvecs = vecs / Q
   xscale2 = scale2 / Q ** 2
   mT = mT / Q

   call samplitude(xvecs, xscale2, amp, prec)

   mT = mT * Q

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use ddtt_kinematics, only: dotproduct, lo_qcd_couplings
   use ddtt_matrix, only: ir_subtraction
   use ddtt_model, only: mT
   use ddtt_color, only: CA, TR
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   double precision, dimension(2:3) :: irp

   double precision, parameter :: alphas = 0.13d0
   double precision :: s, tau1, tau2, rho

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   tau1 = 2.0d0 * dotproduct(vecs(1,:), vecs(3,:)) / s
   tau2 = 2.0d0 * dotproduct(vecs(2,:), vecs(3,:)) / s
   rho = 4.0d0 * mT**2 / s

   call ir_subtraction(vecs, scale2, irp)

   ! Formula from Table 10.2 in Ellis, Stirling, Webber: ``QCD and Collider Physics''
   amp(0) = 4.0d0/9.0d0 * (tau1**2 + tau2**2 + rho/2.0d0)
   
   ! MCFM
   amp(1) = -21.193567709324736D0 * amp(0)
   amp(2:3) = irp(2:3)

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
