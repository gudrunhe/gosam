program test
use stop_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use stop_matrix, only: initgolem, exitgolem
use stop_kinematics, only: inspect_kinematics, init_event
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

write(*,*) "gosam_amp=", gosam_amp
write(*,*) "ref_amp  =", ref_amp

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
   use stop_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(6, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was chosen randomly
 vecs(1,:)=(/  250.00000000000000_ki,  0.0000000000000000_ki, &
          &    0.0000000000000000_ki,  250.00000000000000_ki /)
 vecs(2,:)=(/  250.00000000000000_ki,  0.0000000000000000_ki, &
          &    0.0000000000000000_ki, -250.00000000000000_ki /)
 vecs(3,:)=(/  147.53211468467353_ki,  24.970405230567895_ki, &
          &   -18.431576028372117_ki,  144.23065114968881_ki /)
 vecs(4,:)=(/  108.70359662136400_ki,  103.25573902554709_ki, &
          &  -0.54846846595840537_ki,  33.976807664202191_ki /)
 vecs(5,:)=(/  194.06307653413651_ki, -79.895963003674623_ki, &
          &    7.4858666717648710_ki, -176.69486288452802_ki /)
 vecs(6,:)=(/  49.701212159825850_ki, -48.330181252440347_ki, &
          &    11.494177822565669_ki, -1.5125959293629665_ki /)

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   ! The given reference renormalisation scale is 170.9 GeV
   scale2 = 170.9_ki ** 2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use stop_config, only: renormalisation, convert_to_cdr , &
             & nlo_prefactors !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar, &
       !      & samurai_group_numerators
   implicit none

   renormalisation = 1

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 3
   ! samurai_group_numerators = .true.

   convert_to_cdr = .true.
   nlo_prefactors = 2

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use stop_matrix, only: samplitude, ir_subtraction
   implicit none

   real(ki), dimension(6, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   double precision, dimension(2:3) :: irp
   integer :: prec
   real(ki), parameter :: pi = 3.14159265358979323846264&
     &3383279502884197169399375105820974944592307816406286209_ki

   call samplitude(vecs, scale2, amp, prec)
   call ir_subtraction(vecs, scale2, irp)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)*8.0_ki*pi*pi
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)*8.0_ki*pi*pi
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)*8.0_ki*pi*pi
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use stop_kinematics, only: dotproduct
   implicit none

   real(ki), dimension(6, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   real(ki), parameter :: pi = 3.14159265358979323846264&
     &3383279502884197169399375105820974944592307816406286209_ki

   amp(0) =   6.77798888087183290E-013_ki
   amp(1) =   7.63811712242806362E-014_ki 
   amp(2) =  -4.21705705448444705E-014_ki 
   amp(3) =  -4.57835904083023497E-014_ki

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
      write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)*8.0_ki*pi*pi
      write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)*8.0_ki*pi*pi
      write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)*8.0_ki*pi*pi
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
