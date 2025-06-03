program test
use gggg_config, only: ki, debug_lo_diagrams
use gggg_matrix, only: initgolem, exitgolem
use gggg_kinematics, only: inspect_kinematics, init_event
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

double precision, dimension(0:3) :: gosam_amp
double precision, dimension(0:2) :: heli_amps_gosam, heli_amps_ref
double precision :: rdiff
integer :: h

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call setup_parameters()
call initgolem()

call load_reference_kinematics(vecs, scale2)

call init_event(vecs)
call inspect_kinematics(logf)

call compute_gosam_result(vecs, scale2, heli_amps_gosam)
call compute_reference_result(vecs, scale2, heli_amps_ref)

do h = 0, 2
   if(h .eq. 0) then
      rdiff = abs(rel_diff(heli_amps_gosam(h), heli_amps_ref(h)))
   else
      rdiff = abs(heli_amps_gosam(h) - heli_amps_ref(h))
   end if
   if(abs(rdiff) > eps) then
      write(unit=logf,fmt="(A3,1x,A49,I1,A1)") "==>", &
      & "Comparison of LO failed, helicity", h, "!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "gosam:", heli_amps_gosam(h)
      write(unit=logf,fmt="(A10,1x,E10.4)") "ref:", heli_amps_ref(h)
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", rdiff
      success = .false.
   end if
end do


if (success) then
   write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
else
   write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
end if

close(unit=logf)

if (debug_lo_diagrams) then
   close(unit=gosamlogf)
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

   scale2 = 442.0_ki

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   implicit none

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
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
   double precision, dimension(0:2), intent(out) :: amp
   double precision, dimension(0:3) :: res

   real(ki), dimension(4, 4) :: xvecs
   real(ki) :: xscale2
   logical :: ok
   integer :: prec

   integer :: h

   ! rescaling of all dimensionful quantities that enter the calculation
   xvecs = vecs / Q
   xscale2 = scale2 / Q ** 2
   
   call samplitude(xvecs, xscale2, res, prec, ok, 0)
   amp(0) = res(0)
   call samplitude(xvecs, xscale2, res, prec, ok, 1)
   amp(1) = res(0)
   call samplitude(xvecs, xscale2, res, prec, ok, 2)
   amp(2) = res(0)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     ++++:       ", amp(0)
      write(ch,*) "GOSAM     +++-:       ", amp(1)
      write(ch,*) "GOSAM     ++--:       ", amp(2)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use gggg_config, only: include_color_avg_factor, &
               & include_helicity_avg_factor, &
               & include_symmetry_factor
   use gggg_kinematics, only: dotproduct, &
               & symmetry_factor, in_helicities
   use gggg_color, only: incolors
   use gggg_model, only: NC
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:2), intent(out) :: amp

   double precision, parameter :: alphas = 0.13d0
   double precision :: s, t, u, aa, pi, gs

   pi = 4.0d0 * atan(1.0d0)
   gs = sqrt(4.0d0 * pi * alphas)

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   t = -2.0d0 * dotproduct(vecs(1,:), vecs(3,:))
   u = -2.0d0 * dotproduct(vecs(1,:), vecs(4,:))

   amp(0) = 16.0d0*NC*NC*(s*s+t*t+u*u)*(s/t/u)**2
   amp(1:2) = 0.0d0

   if (include_helicity_avg_factor) then
      amp = amp / real(in_helicities, ki)
   end if
   if (include_color_avg_factor) then
      amp = amp / incolors
   end if
   if (include_symmetry_factor) then
      amp = amp / real(symmetry_factor, ki)
   end if

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE ++++:       ", amp(0)
      write(ch,*) "REFERENCE +++-:       ", amp(1)
      write(ch,*) "REFERENCE ++--:       ", amp(2)
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
