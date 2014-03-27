program test
use gggg_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams, &
         & convert_to_cdr
use gggg_matrix, only: initgolem, exitgolem
use gggg_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: golemlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(4, 4) :: vecs
real(ki) :: scale2

double precision, dimension(0:3) :: golem_amp, ref_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=golemlogf)
end if

call setup_parameters()
call initgolem()

call load_reference_kinematics(vecs, scale2)

call init_event(vecs)
call inspect_kinematics(logf)

call compute_golem_result(vecs, scale2, golem_amp)
call compute_reference_result(vecs, scale2, ref_amp)

diff = abs(rel_diff(golem_amp, ref_amp))

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
   close(unit=golemlogf)
end if

call exitgolem()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use gggg_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was specified in arXiv:1103.0621v1

   vecs(1,:) = (/220.9501779577791_ki, 0.0_ki, 0.0_ki,  220.9501779577791_ki/)
   vecs(2,:) = (/220.9501779577791_ki, 0.0_ki, 0.0_ki, -220.9501779577791_ki/)
   vecs(3,:) = (/220.9501779577791_ki,  119.9098300357375_ki, &
             &   183.0492135511419_ki, -30.55485589367430_ki/)
   vecs(4,:) = (/220.9501779577791_ki, -119.9098300357375_ki, &
             &  -183.0492135511419_ki,  30.55485589367430_ki/)

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2 = 91.188_ki ** 2
   scale2 = 442.0_ki

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use gggg_config, only: renormalisation, use_sorted_sum !, &
        !     & samurai_test, samurai_verbosity, samurai_scalar
   use gggg_model, only: Nf, Nfgen
   implicit none

   renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 2

   ! We generated the process with no fermion loops 
   Nf    = 0.0_ki

   convert_to_cdr = .true.
end subroutine setup_parameters

subroutine     compute_golem_result(vecs, scale2, amp)
   use gggg_matrix, only: samplitude, ir_subtraction
   implicit none
   ! The amplitude should be a homogeneous function
   ! in the energy dimension and scale like
   !     A(Q*E) = A(E)
   ! We use this fact as
   !  - an additional test for the amplitude
   !  - to enhance precision
   real(ki), parameter :: Q = 442.0d0
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

   call samplitude(xvecs, xscale2, amp, prec)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_golem_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use gggg_config, only: include_color_avg_factor, &
               & include_helicity_avg_factor, &
               & include_symmetry_factor
   use gggg_kinematics, only: dotproduct, &
               & symmetry_factor, in_helicities
   use gggg_color, only: incolors
   use gggg_model, only: NC
   use four_gluon, only: amp_ppmm
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision, parameter :: alphas = 0.13d0
   double precision :: s, t, u

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   t = -2.0d0 * dotproduct(vecs(1,:), vecs(3,:))
   u = -2.0d0 * dotproduct(vecs(1,:), vecs(4,:))
  
   call amp_ppmm(s, u, t, scale2, amp(0), amp(1:3))

   if (include_helicity_avg_factor) then
      amp = amp / real(in_helicities, ki)
   end if
   if (include_color_avg_factor) then
      amp = amp / incolors
   end if
   if (include_symmetry_factor) then
      amp = amp / real(symmetry_factor, ki)
   end if

   ! UV counter-term
   ! -2 (11 C_A - 4 T_R N_f)/6 = - 2 (33 - 0)/6 = - 11
   amp(2) = amp(2) - 11.0_ki * amp(0)

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
