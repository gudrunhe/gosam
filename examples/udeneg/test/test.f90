program test
use udeneg_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use udeneg_matrix, only: initgolem, exitgolem
use udeneg_kinematics, only: inspect_kinematics, init_event, dotproduct
implicit none
!
! Comparison with MCFM for a single phase space point.
!

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

call exitgolem()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use udeneg_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(5, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(1,:)=(/ 500.000000000000_ki,    0.00000000000000_ki, &
            &   0.00000000000000_ki,    500.000000000000_ki/)
   vecs(2,:)=(/ 500.000000000000_ki,    0.00000000000000_ki, &
            &   0.00000000000000_ki,   -500.000000000000_ki/)
   vecs(3,:)=(/ 483.244841094218_ki,   -86.3112218694181_ki, &
            &   147.629518147233_ki,   -451.975082051212_ki/)
   vecs(4,:)=(/ 279.253370247231_ki,    6.62401666401929_ki, &
            &  -5.58083951102529_ki,    279.119009435087_ki/)
   vecs(5,:)=(/ 237.501788658551_ki,    79.6872052053988_ki, &
            &  -142.048678636208_ki,    172.856072616124_ki/)

   call adjust_kinematics(vecs)

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use udeneg_config, only: renormalisation, convert_to_cdr !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar
   use udeneg_model, only: mW, wW, mZ, Nf, Nfgen, VUD, CVDU
   implicit none

   renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 1
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   mW = 80.398_ki
   wW = 2.1054_ki
   mZ = mW / sqrt(1.0_ki - 0.4808222_ki**2)

   VUD  = (0.97419_ki, 0.0_ki)
   CVDU = (0.97419_ki, 0.0_ki)

   Nf = 5
   Nfgen = 5

   convert_to_cdr = .true.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use udeneg_matrix, only: samplitude
   use udeneg_model, only: mW, wW, mZ, wZ
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   double precision, dimension(0:3) :: gauge_amp, diff
   integer :: prec

   logical :: ok, gok

   ! rescaling of all dimensionful quantities that enter the calculation

   call shake_gauge_parameters(0.0_ki)
   call samplitude(vecs, scale2, amp, prec, ok)

   call shake_gauge_parameters(5.0_ki)
   call samplitude(vecs, scale2, gauge_amp, prec, gok)

   diff = abs(rel_diff(amp, gauge_amp))

   if (maxval(diff) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Gauge check failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", maxval(diff)
      success = .false.
   end if

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use udeneg_kinematics, only: dotproduct
   use udeneg_matrix, only: ir_subtraction
   use udeneg_model, only: mW, wW, sw, vud, NC
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   !double precision, dimension(2:3) :: irp

   !call ir_subtraction(vecs, scale2, irp)

   amp(0) =  0.2839850962543592E-06_ki
   ! This is the result from MCFM:
   amp(1) = -6.7719586035440908_ki * amp(0)
   amp(2) = -18.72201065555712_ki * amp(0)
   amp(3) = -17.0_ki / 3.0_ki * amp(0)

   ! In order to convert to CDR we need to subtract
   ! n_q * C_F/2 + n_g * C_A/6 = 2 C_F/2 + 1 C_A/6 = 11/6
   ! see arXiv:hep-ph/9610553
   amp(1) = amp(1) - 11.0_ki/6.0_ki * amp(0)

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

subroutine     shake_gauge_parameters(delta)
   use udeneg_model, only: gauge5z
   implicit none
   real(ki), intent(in) :: delta
   real(ki), dimension(4) :: harvest
   call random_number(harvest)

   gauge5z = delta * (harvest(1) - 0.5_ki)
end subroutine shake_gauge_parameters
end program test
