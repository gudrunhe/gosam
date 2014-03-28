program test
use tne_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams, dbl
use tne_matrix, only: initgolem, exitgolem
use tne_kinematics, only: inspect_kinematics, init_event
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
   use tne_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(5, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(1,:)= (/  1187.7086110647201_ki,   0.0000000000000000_ki, &
   &    0.0000000000000000_ki,  1187.7086110647201_ki/)
   vecs(2,:)= (/  2897.1481362602890_ki,   0.0000000000000000_ki, &
   &    0.0000000000000000_ki,  -2897.1481362602890_ki/)
   vecs(3,:)= (/   2293.0435558834492_ki,   629.81047833131981_ki, &
   &    258.58120146220904_ki,  -2189.6399870328105_ki/)
   vecs(4,:)= (/   509.48956356743611_ki,   144.72113807954338_ki, &
   &    19.883362437475000_ki,  -488.09841167051400_ki/)
   vecs(5,:)= (/   1282.3236278741238_ki,  -774.53161641086319_ki, &
   &   -278.46456389968404_ki,   968.29887350775562_ki/)

   !call adjust_kinematics(vecs)

   scale2 = 71.2_ki**2
end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use tne_config
   use tne_model
   implicit none

   wW = 2.0476_ki
   mT = 171.2_ki

   renormalisation = 1
   renorm_beta = .true.
   renorm_mqse = .true.
   renorm_logs = .true.

   ! reduction_interoperation=0

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use tne_matrix, only: samplitude
   use tne_model
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   print*, "g_s = ", gs
   print*, "e = ", e
   print*, "cos(theta_w) = ", cw
   print*, "sin(theta_w) = ", sw
   print*, "M_W = ", mW
   print*, "M_Z = ", mZ
   print*, "m_t = ", mT
   print*, "G_F = ", GF
   print*, "Gamma_W = ", wW
   print*, "Gamma_Z = ", wZ
   print*, "Gamma_t = ", wT

   call samplitude(vecs, real(scale2, dbl), amp, prec, ok)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use tne_kinematics, only: dotproduct
   use tne_matrix, only: ir_subtraction
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   real(ki), dimension(2:3) :: irp

   call ir_subtraction(vecs, real(scale2, dbl), irp(2:3))

   ! MCFM
   amp(0) = 8.52301540708130106E-002_ki
   amp(1) = -78.713051902606352_ki * amp(0)
   amp(2:3) = real(irp(2:3), dbl)

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

   if (a.eq.0.0_ki .and. b.eq.0.0_ki) then
      rel_diff = 0.0_ki
   else
      rel_diff = 2.0_ki * (a-b) / (abs(a)+abs(b))
   end if
end  function rel_diff

end program test
