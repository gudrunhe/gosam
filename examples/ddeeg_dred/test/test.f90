program test
use ddeeg_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use ddeeg_matrix, only: initgolem, exitgolem
use ddeeg_kinematics, only: inspect_kinematics, init_event, dotproduct
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

call compute_crossed_gosam_result(vecs, scale2, gosam_amp)
call compute_crossed_reference_result(vecs, scale2, ref_amp)

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
   use ddeeg_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(5, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2


   vecs(1,:) = (/219.81636757818666_ki,    0.00000000000000_ki, &
             &     0.00000000000000_ki,  219.81636757818666_ki/)
   vecs(2,:) = (/78.514049708950481_ki,    0.00000000000000_ki, &
             &     0.00000000000000_ki, -78.514049708950481_ki/)
   vecs(3,:) = (/190.91987238779512_ki, -28.468337054964493_ki, &
             &   10.154026810698143_ki,  188.51219376322723_ki/)
   vecs(4,:) = (/36.663063494801236_ki,  27.114750988401063_ki, &
             &   16.579327972459467_ki,  18.278303740841352_ki/)
   vecs(5,:) = (/70.747481404540792_ki,  1.3535860665634296_ki, &
             &  -26.733354783157612_ki, -65.488179634832392_ki/)

   call adjust_kinematics(vecs)

   scale2 = 91.1876_ki**2
   scale2 = 91.188_ki**2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ddeeg_config
   use ddeeg_model, only: mW, mZ, wZ, Nf, Nfgen, alpha
   implicit none

   renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2 
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   mW = 80.44_ki
   mZ = 91.1876_ki
   wZ = 2.4952_ki
   alpha = 1.0_ki/132.6844139_ki

   Nf = 5.0_ki
   Nfgen = 5.0_ki

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ddeeg_matrix, only: samplitude, ir_subtraction
   use ddeeg_model, only: alpha
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   double precision, dimension(0:3) :: gauge_amp, diff
   real(ki), dimension(2:3) :: irp
   integer :: prec

   logical :: ok, gok

   double precision :: pi, gs, e

   pi = 4.0d0 * atan(1.0d0)
   gs = sqrt(4.0d0 * pi * 0.118d0)
   e = sqrt(4.0d0 * pi * alpha)

   call shake_gauge_parameters(0.0_ki)
   call samplitude(vecs, scale2, amp, prec, ok)

   call shake_gauge_parameters(5.0_ki)
   call samplitude(vecs, scale2, gauge_amp, prec, gok)
   call ir_subtraction(vecs, scale2, irp)

   diff = abs(rel_diff(amp, gauge_amp))

   if (maxval(diff) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Gauge check failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", maxval(diff)
      success = .false.
   end if

   amp = (e**2 * gs)**2 * amp
   irp = (e**2 * gs)**2 * irp

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
      write(ch,*) "GOSAM      IR(2)/AMP(0):", irp(2)/amp(0)
      write(ch,*) "GOSAM      IR(3)/AMP(0):", irp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_crossed_gosam_result(vecs, scale2, amp)
   use dgeed_matrix, only: samplitude, ir_subtraction
   use ddeeg_model, only: alpha
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   real(ki), dimension(2:3) :: irp
   integer :: prec

   logical :: ok, gok

   double precision :: pi, gs, e
  
   pi = 4.0d0 * atan(1.0d0)
   gs = sqrt(4.0d0 * pi * 0.118d0)
   e = sqrt(4.0d0 * pi * alpha)

   call shake_gauge_parameters(0.0_ki)
   call samplitude(vecs, scale2, amp, prec, ok)
   call ir_subtraction(vecs, scale2, irp)

   amp = (e**2 * gs)**2 * amp
   irp = (e**2 * gs)**2 * irp

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
      write(ch,*) "GOSAM      IR(2)/AMP(0):", irp(2)/amp(0)
      write(ch,*) "GOSAM      IR(3)/AMP(0):", irp(3)/amp(0)
   end do
end subroutine compute_crossed_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use ddeeg_kinematics, only: dotproduct
   use ddeeg_model, only: mW, sw, NC
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision :: pi
  
   pi = 4.0d0 * atan(1.0d0)

   amp(0) =  6.76069763764682863E-002_ki
   amp(1) =  1.40892172309674130E-002_ki
   amp(2) = -1.21173922992901528E-002_ki
   amp(3) = -7.19484295416346949E-003_ki

   amp(1:3) = amp(1:3) / (0.118_ki/2.0_ki/pi)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
      write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_reference_result

subroutine     compute_crossed_reference_result(vecs, scale2, amp)
   use ddeeg_kinematics, only: dotproduct
   use ddeeg_model, only: mW, sw, NC
   implicit none

   real(ki), dimension(5, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp


   double precision :: pi
  
   pi = 4.0d0 * atan(1.0d0)


   amp(0) =  1.71059868986021858E-002_ki 
   amp(1) =  3.17029216184223396E-003_ki
   amp(2) = -2.91385295414951957E-003_ki
   amp(3) = -1.82044658566124528E-003_ki

   amp(1:3) = amp(1:3) / (0.118_ki/2.0_ki/pi)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
      write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_crossed_reference_result

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
   use ddeeg_model, only: gauge5z
   implicit none
   real(ki), intent(in) :: delta
   real(ki), dimension(4) :: harvest
   call random_number(harvest)

   gauge5z = delta * (harvest(1) - 0.5_ki)
end subroutine shake_gauge_parameters
end program test
