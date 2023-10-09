program test
use graviton_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use graviton_matrix, only: initgolem, exitgolem
use graviton_kinematics, only: inspect_kinematics, init_event
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
   use graviton_kinematics, only: adjust_kinematics, dotproduct, boost_to_cms
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was chosen randomly
   vecs(1,:)=(/  250.00000000000000_ki ,  0.0000000000000000_ki, &
            &     0.0000000000000000_ki ,  250.00000000000000_ki /)
   vecs(2,:)=(/  250.00000000000000_ki ,  0.0000000000000000_ki, &
            &     0.0000000000000000_ki , -250.00000000000000_ki /)
   vecs(3,:)=(/  250.00000000000000_ki ,  218.30931500994714_ki, &
            &    -29.589212828575324_ki ,  118.17580743990260_ki /)
   vecs(4,:)=(/  250.00000000000000_ki , -218.30931500994714_ki, &
            &     29.589212828575324_ki , -118.17580743990260_ki /)

   !call boost_to_cms(vecs)

   !call adjust_kinematics(vecs)


   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   !call adjust_kinematics(vecs)

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use graviton_config, only: renormalisation, convert_to_cdr , &
             & nlo_prefactors !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar, &
       !      & samurai_group_numerators
   implicit none

   !renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 3
   ! samurai_group_numerators = .true.

   !convert_to_cdr = .false.
   nlo_prefactors = 0

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use graviton_matrix, only: samplitude, ir_subtraction
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   real(ki), dimension(0:3), intent(out) :: amp
   real(ki), dimension(2:3) :: irp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)
   call ir_subtraction(vecs, scale2, irp)

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

subroutine     compute_reference_result(vecs, scale2, amp)
   use graviton_kinematics, only: dotproduct
   use graviton_model
   use graviton_custompropagator
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   real(ki) :: s,t,u
   double precision, dimension(0:3), intent(out) :: amp
   real(ki), parameter :: pi = &
   & 3.1415926535897932384626433832795028841971693993751058209749445920_ki

   s= dotproduct(vecs(1,:)+vecs(2,:), vecs(1,:)+vecs(2,:))
   t= dotproduct(vecs(1,:)-vecs(3,:), vecs(1,:)-vecs(3,:))
   u= dotproduct(vecs(1,:)-vecs(4,:), vecs(1,:)-vecs(4,:))

   ! The following results are calculated based on the formula (9) and (14)
   ! in arXiv:0902.4894v2. The conversion from CDR to DRED is included.

   amp(0) = abs(customSpin2Prop(s,0._ki))**2._ki * mdlkappa**4._ki / 16._ki / 3._ki &
                  &  * (u*t**3._ki + t*u**3._ki) / 4._ki

   amp(1) = 4._ki/3._ki*(-9._ki + pi*pi) * amp(0)
   amp(2) = -4_ki * amp(0)
   amp(3) = -8._ki/3._ki * amp(0)

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
