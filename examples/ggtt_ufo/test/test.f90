program test
use ggtt_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use ggtt_matrix, only: initgolem, exitgolem
use ggtt_kinematics, only: inspect_kinematics, init_event
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
   use ggtt_kinematics, only: adjust_kinematics
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2
 
   vecs(1,:)= (/   137.84795086008967_ki,   0.0000000000000000_ki, &
            &      0.0000000000000000_ki,   137.84795086008967_ki/)
   vecs(2,:)= (/   3161.1731634194916_ki,   0.0000000000000000_ki, &
            &      0.0000000000000000_ki,  -3161.1731634194916_ki/)
   vecs(3,:)= (/   3058.6441209877348_ki,   16.445287185144903_ki, &
            &      165.91204201912493_ki,  -3049.2945357402382_ki/)
   vecs(4,:)= (/   240.37699329184659_ki,  -16.445287185144903_ki, &
            &     -165.91204201912493_ki,   25.969323180836145_ki/)

   ! In order to increase the precision of the kinematical
   ! constraints (on-shell conditions and momentum conservation)
   ! we call the following routine.
   call adjust_kinematics(vecs)

   scale2=71.2_ki**2
end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ggtt_config
   use ggtt_model, only: Nf, Nfgen, mT => MT, aS
   implicit none

   renormalisation = 1
   renorm_logs = .true.
   convert_to_cdr = .false.

   ! reduction_interoperation = 0

   mT    = 171.2_ki
   Nf    = 5.0_ki
   Nfgen = 1.0_ki
   ! set g_s to one
   aS = 1.0_ki / (16.0_ki * atan(1.0_ki))
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ggtt_matrix, only: samplitude
   use ggtt_model, only: gs => G
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)

   amp(0) = amp(0)
   amp(1:3) = amp(1:3)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use ggtt_kinematics, only: dotproduct, lo_qcd_couplings
   use ggtt_matrix, only: ir_subtraction
   use ggtt_model, only: mT => MT, Nf, gs => G
   use ggtt_color, only: CA, TR, CF
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision, parameter :: alphas = 0.13d0
   double precision :: s, tau1, tau2, rho

   s =  2.0d0 * dotproduct(vecs(1,:), vecs(2,:))
   tau1 = 2.0d0 * dotproduct(vecs(1,:), vecs(3,:)) / s
   tau2 = 2.0d0 * dotproduct(vecs(2,:), vecs(3,:)) / s
   rho = 4.0d0 * mT**2 / s

   call ir_subtraction(vecs, scale2, amp(2:3))

   ! Formula from Table 10.2 in Ellis, Stirling, Webber: ``QCD and Collider Physics''
   amp(0) = (1.0_ki/(6.0_ki*tau1*tau2)-3.0_ki/8.0_ki)*&
          & (tau1*tau1+tau2*tau2+rho-0.25_ki*(rho/tau1)*(rho/tau2))
   
   ! MCFM
   amp(1) = -26.235240991775640 * amp(0)
   amp(2:3) = amp(2:3)

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
