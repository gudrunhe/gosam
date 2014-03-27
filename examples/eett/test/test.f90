program test
use eett_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use eett_matrix, only: initgolem, exitgolem
use eett_kinematics, only: inspect_kinematics, init_event
use eett_groups, only: tear_down_golem95
implicit none

! Note: I also did a cross-check with CalcHEP for the leading order.
! |ME|^2 = 2.58146098703207 + 2.816625880343903 + 0.963982317687123
!                     (A-A)               (A-Z)               (Z-Z)
!        = 6.362069185063096


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

call exitgolem()

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

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use eett_kinematics, only: adjust_kinematics
   use eett_model, only: mT
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
   !call adjust_kinematics(vecs)
  
   scale2 = 29756.25_ki

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use eett_config, only: renormalisation, convert_to_cdr !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar, &
       !      & reduction_interoperation
   use eett_model, only: Nf, Nfgen, mT, mZ, wZ, mW
   use analytic, only: include_Z
   implicit none

   real(ki) :: my_sw, my_cw

   renormalisation = 0

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 1
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1
   ! reduction_interoperation = 1

   my_sw = 0.47303762_ki
   my_cw = sqrt(1.0_ki - my_sw**2)

   mT = 172.5_ki

   mZ = 91.1876_ki
   wZ = 2.4952_ki

   mW = my_cw * mZ

   Nf    = 5.0_ki
   Nfgen = 1.0_ki

   include_Z = .true.

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use eett_matrix, only: samplitude
   use eett_model, only: mT, sw, cw
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   call samplitude(vecs, scale2, amp, prec, ok)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use analytic
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   amp = reference_amp(vecs, scale2)

   ! beta0 = (11.0d0 * CA - 4.0d0 * (Nf + 1.0d0) * TR) / 6.0d0
   !amp(2) = amp(2) + lo_qcd_couplings * beta0 * amp(0)

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
