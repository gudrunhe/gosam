program test
use udeneg_dred_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use udeneg_dred_matrix, only: initgolem_dred => initgolem, &
     & exitgolem_dred => exitgolem
use udeneg_thv_matrix, only: initgolem_thv => initgolem, &
     & exitgolem_thv => exitgolem
use udeneg_dred_kinematics, only: inspect_kinematics_dred => inspect_kinematics, &
     init_event_dred => init_event
use udeneg_thv_kinematics, only: init_event_thv => init_event
implicit none
!
! Comparison with MCFM and between IR regularisation
! schemes for a single phase space point.
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

double precision, dimension(0:3) :: gosam_amp_dred, gosam_amp_thv, &
     ref_amp_dred, ref_amp_thv, diff_dred, diff_thv

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call setup_parameters()
call initgolem_dred()
call initgolem_thv()

call load_reference_kinematics(vecs, scale2)

call init_event_dred(vecs)
call init_event_thv(vecs)
call inspect_kinematics_dred(logf)

call compute_gosam_result(vecs, scale2, gosam_amp_dred, gosam_amp_thv)
call compute_reference_result(vecs, scale2, ref_amp_dred, ref_amp_thv)

if (any(isnan(gosam_amp_dred)).or.any(isnan(gosam_amp_thv))) then
   write(unit=logf,fmt="(A10)") "NaN error!"
   success = .false.
end if

diff_dred = abs(rel_diff(gosam_amp_dred, ref_amp_dred))
diff_thv = abs(rel_diff(gosam_amp_thv, ref_amp_thv))

if (diff_dred(0) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of LO failed (DRED)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_dred(0)
   success = .false.
end if

if (diff_dred(1) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/finite part failed (DRED)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_dred(1)
   success = .false.
end if

if (diff_dred(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/single pole failed (DRED)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_dred(2)
   success = .false.
end if

if (diff_dred(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A30)") "==>", &
   & "Comparison of NLO/double pole failed (DRED)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_dred(2)
   success = .false.
end if

if (diff_thv(0) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of LO failed (tHV)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_thv(0)
   success = .false.
end if

if (diff_thv(1) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/finite part failed (tHV)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_thv(1)
   success = .false.
end if

if (diff_thv(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/single pole failed (tHV)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_thv(2)
   success = .false.
end if

if (diff_thv(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A30)") "==>", &
   & "Comparison of NLO/double pole failed (tHV)!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff_thv(2)
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

call exitgolem_dred()
call exitgolem_thv()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use udeneg_dred_kinematics, only: adjust_kinematics, dotproduct
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
  use udeneg_dred_config, only: renormalisation_dred => renormalisation, &
       & convert_to_thv_dred => convert_to_thv
  use udeneg_thv_config, only: renormalisation_thv => renormalisation, &
       & convert_to_thv_thv => convert_to_thv
  use udeneg_dred_model, only: set_parameter_dred => set_parameter
  use udeneg_thv_model, only: set_parameter_thv => set_parameter
  implicit none
  integer :: ierr = 0
  
  renormalisation_dred = 1
  renormalisation_thv = 1

  call set_parameter_dred("mW", 80.398_ki, 0.0_ki, ierr)
  call set_parameter_dred("wW", 2.1054_ki, 0.0_ki, ierr)
  call set_parameter_dred("mZ", 80.398_ki / sqrt(1.0_ki - 0.4808222_ki**2), 0.0_ki, ierr)

  call set_parameter_dred("VUD", 0.97419_ki, 0.0_ki, ierr)
  call set_parameter_dred("CVDU", 0.97419_ki, 0.0_ki, ierr)

  call set_parameter_dred("Nf", 5.0_ki, 0.0_ki, ierr)
  call set_parameter_dred("Nfgen", 5.0_ki, 0.0_ki, ierr)

  call set_parameter_thv("mW", 80.398_ki, 0.0_ki, ierr)
  call set_parameter_thv("wW", 2.1054_ki, 0.0_ki, ierr)
  call set_parameter_thv("mZ", 80.398_ki / sqrt(1.0_ki - 0.4808222_ki**2), 0.0_ki, ierr)

  call set_parameter_thv("VUD", 0.97419_ki, 0.0_ki, ierr)
  call set_parameter_thv("CVDU", 0.97419_ki, 0.0_ki, ierr)

  call set_parameter_thv("Nf", 5.0_ki, 0.0_ki, ierr)
  call set_parameter_thv("Nfgen", 5.0_ki, 0.0_ki, ierr)

  convert_to_thv_dred = .false.
  convert_to_thv_thv = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp_dred, amp_thv)
  use udeneg_dred_config, only: convert_to_thv_dred => convert_to_thv
  use udeneg_dred_matrix, only: samplitude_dred => samplitude
  use udeneg_thv_matrix, only: samplitude_thv => samplitude
  use udeneg_dred_model, only: mW_dred => mW, wW_dred => wW, mZ_dred => mZ
  use udeneg_thv_model, only: mW_thv => mW, wW_thv => wW, mZ_thv => mZ
  implicit none

  real(ki), dimension(5, 4), intent(in) :: vecs
  real(ki), intent(in) :: scale2
  double precision, dimension(0:3), intent(out) :: amp_dred, amp_thv
  double precision, dimension(0:3) :: gauge_amp_dred, diff_dred, &
       & gauge_amp_thv, diff_thv, amp_conv, diff_conv
  integer :: prec

  logical :: ok, gok

  call shake_gauge_parameters(0.0_ki)
  call samplitude_dred(vecs, scale2, amp_dred, prec, ok)
  call samplitude_thv(vecs, scale2, amp_thv, prec, ok)
  convert_to_thv_dred = .true.
  call samplitude_dred(vecs, scale2, amp_conv, prec, gok)
  convert_to_thv_dred = .false.
  
  call shake_gauge_parameters(5.0_ki)
  call samplitude_dred(vecs, scale2, gauge_amp_dred, prec, gok)
  call samplitude_thv(vecs, scale2, gauge_amp_thv, prec, gok)

  diff_dred = abs(rel_diff(amp_dred, gauge_amp_dred))
  diff_thv = abs(rel_diff(amp_thv, gauge_amp_thv))
  diff_conv = abs(rel_diff(amp_thv, amp_conv))
  
  if (maxval(diff_dred) .gt. eps) then
     do ic = 1, 2
        ch = channels(ic)
        write(unit=ch,fmt="(A3,1x,A40)") "==>", &
             & "Gauge check of DRED result failed!"
        write(unit=ch,fmt="(A10,1x,E10.4)") "DIFFERENCE:", maxval(diff_dred)
     end do
     success = .false.
  end if

  if (maxval(diff_thv) .gt. eps) then
     do ic = 1, 2
        ch = channels(ic)
        write(unit=ch,fmt="(A3,1x,A40)") "==>", &
             & "Gauge check of tHV result failed!"
        write(unit=ch,fmt="(A10,1x,E10.4)") "DIFFERENCE:", maxval(diff_thv)
     end do
     success = .false.
  end if

  if (maxval(diff_conv) .gt. eps) then
     do ic = 1, 2
        ch = channels(ic)
        write(unit=ch,fmt="(A3,1x,A40)") "==>", &
             & "Conversion test from DRED to tHV failed!"
        write(unit=ch,fmt="(A10,1x,E10.4)") "DIFFERENCE:", maxval(diff_conv)
     end do
     success = .false.
  end if
  
  do ic = 1, 2
     ch = channels(ic)
     write(unit=ch,fmt="(A6,11x,A4,22x,A3)") "GOSAM:", "DRED", "tHV"
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(0):       ", &
          & amp_dred(0), amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(1)/AMP(0):", &
          & amp_dred(1)/amp_dred(0), amp_thv(1)/amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(2)/AMP(0):", &
          & amp_dred(2)/amp_dred(0), amp_thv(2)/amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(3)/AMP(0):", &
          & amp_dred(3)/amp_dred(0), amp_thv(3)/amp_thv(0)
  end do
  
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp_dred, amp_thv)
  implicit none
  real(ki), dimension(5, 4), intent(in) :: vecs
  real(ki), intent(in) :: scale2
  double precision, dimension(0:3), intent(out) :: amp_dred, amp_thv

  amp_dred(0) =  0.2839850962543592E-06_ki
  ! This is the result from MCFM:
  amp_dred(1) = -6.7719586035440908_ki * amp_dred(0)
  amp_dred(2) = -18.72201065555712_ki * amp_dred(0)
  amp_dred(3) = -17.0_ki / 3.0_ki * amp_dred(0)

  ! In order to convert to tHV we need to subtract
  ! n_q * C_F/2 + n_g * C_A/6 = 2 C_F/2 + 1 C_A/6 = 11/6
  ! see arXiv:hep-ph/9610553
  amp_thv(0) = amp_dred(0)
  amp_thv(1) = amp_dred(1) - 11.0_ki/6.0_ki * amp_dred(0)
  amp_thv(2:3) = amp_dred(2:3)

  do ic = 1, 2
     ch = channels(ic)
     write(unit=ch,fmt="(A10,7x,A4,22x,A3)") "REFERENCE:", "DRED", "tHV"
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(0):       ", &
          & amp_dred(0), amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(1)/AMP(0):", &
          & amp_dred(1)/amp_dred(0), amp_thv(1)/amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(2)/AMP(0):", &
          & amp_dred(2)/amp_dred(0), amp_thv(2)/amp_thv(0)
     write(unit=ch,fmt="(A14,3x,E23.16E3,3x,E23.16E3)") "AMP(3)/AMP(0):", &
          & amp_dred(3)/amp_dred(0), amp_thv(3)/amp_thv(0)
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
  use udeneg_dred_model, only: set_parameter_dred => set_parameter
  use udeneg_thv_model, only: set_parameter_thv => set_parameter
  implicit none
  integer :: ierr = 0
  real(ki), intent(in) :: delta
  real(ki), dimension(4) :: harvest
  call random_number(harvest)

  call set_parameter_dred("gauge5z", delta * (harvest(1) - 0.5_ki), 0.0_ki, ierr)
  call set_parameter_thv("gauge5z", delta * (harvest(1) - 0.5_ki), 0.0_ki, ierr)
end subroutine shake_gauge_parameters
end program test
