program test
use wpwpjj_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use wpwpjj_matrix, only: initgolem, exitgolem
use wpwpjj_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(8, 4) :: vecs
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
   use wpwpjj_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(8, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! This kinematics was specified in JHEP 1012 (2010) 053.
   vecs(1,:) = (/500.0_ki,  500.0_ki, 0.0_ki, 0.0_ki/)
   vecs(2,:) = (/500.0_ki, -500.0_ki, 0.0_ki, 0.0_ki/)

   vecs(3,:) = (/54.2314070117999_ki, -31.1330162081798_ki, &
             &  -7.92796656791140_ki,  43.6912823611163_ki/)
   vecs(4,:) = (/214.488870161418_ki, -27.0607980217775_ki, &
             &  -98.5198083786150_ki,  188.592247959949_ki/)
   vecs(5,:) = (/85.5312248384887_ki, -8.22193223977868_ki, &
             &   36.1637837682033_ki, -77.0725048002414_ki/)
   vecs(6,:) = (/181.428811610043_ki, -57.8599829481937_ki, &
             &  -171.863734086635_ki, -5.61185898481311_ki/)
   vecs(7,:) = (/82.8493010774356_ki, -65.9095476235891_ki, &
             &  -49.8952157196287_ki,  5.51413360058664_ki/)
   vecs(8,:) = (/381.470385300815_ki,  190.185277041519_ki, &
             &   292.042940984587_ki, -155.113300136598_ki/)

   ! The beam axes must not be collinear with the x-directions
   ! because of the implementation of the spinor products.
   ! Be careful to preserve CP:
   vecs(:,(/2,3,4/)) = vecs(:,(/3,4,2/))

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   ! The given reference renormalisation scale is 80 GeV
   scale2 = 80.0_ki ** 2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use wpwpjj_config, only: renormalisation, convert_to_cdr !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar
   use wpwpjj_model, only: Nf, Nfgen, mW, wW
   implicit none

   ! we compare unrenormalized results:
   renormalisation = 0

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   ! make sure the defaults for Nf have not changed
   Nf    = 5.0_ki
   Nfgen = 5.0_ki

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use wpwpjj_model, only: mW, wW
   use wpwpjj_matrix, only: samplitude
   implicit none

   real(ki), dimension(8, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   !double precision, dimension(2:3) :: irp
   integer :: prec

   logical :: ok

   ! rescaling of all dimensionful quantities that enter the calculation

   call samplitude(vecs, scale2, amp, prec, ok)
 
   write(logf,*) "GOSAM AMP(0):       ", amp(0)
   write(logf,*) "GOSAM AMP(1)/AMP(0):", amp(1)/amp(0)
   write(logf,*) "GOSAM AMP(2)/AMP(0):", amp(2)/amp(0)
   write(logf,*) "GOSAM AMP(3)/AMP(0):", amp(3)/amp(0)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

pure function mmrz_lo(s56, s78) result(res)
   use wpwpjj_model, only: NC, sw, NA, gs, e
   implicit none
   real(ki), intent(in) :: s56, s78

   double precision :: res

   complex(ki) :: A0
   real(ki) :: couplings, gw, A02

   A0 = cmplx(-7.488599d-11,-17.47659d-11)
   A02 = abs(A0 * conjg(A0))
   gw = 1.0_ki / sw
   res = 0.0625_ki*PW2(s56)*PW2(s78)*gw**8*A02*NA
end  function mmrz_lo

pure function PW2(s)
   use wpwpjj_model, only: mW, wW
   implicit none
   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)

   real(ki), intent(in) :: s
   real(ki) :: PW2
   complex(ki) :: PW

   PW = s / (s-mW**2 - i_*wW*mW)
   PW2 = abs(PW*conjg(PW))
end  function PW2

subroutine     compute_reference_result(vecs, scale2, amp)
   use wpwpjj_kinematics, only: dotproduct
   implicit none

   real(ki), dimension(8, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   
   real(ki) :: s56, s78

   s56 = 2.0_ki * dotproduct(vecs(5,:), vecs(6,:))
   s78 = 2.0_ki * dotproduct(vecs(7,:), vecs(8,:))

   amp(0) = mmrz_lo(s56, s78)
   amp(1) = 23.35965d0 * amp(0)
   ! old, incorrect number
   ! amp(1) = 27.48580d0 * amp(0)
   amp(2) = 13.62554d0 * amp(0)
   amp(3) = -5.33333d0 * amp(0)

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
