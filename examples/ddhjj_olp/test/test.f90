program test
use olp_module
use, intrinsic :: iso_c_binding
implicit none

character(kind=c_char,len=13) :: contract_file_name = "../ddhjj.olc"

integer, parameter :: ki = kind(1.0d0)

! unit of the log file
integer, parameter :: logf = 28
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch, ierr, stage = 0, subprocess, rndseed = 1234

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(60) :: blha_kinematics
real(ki) :: renorm_scale

double precision, dimension(0:3) :: gosam_amp, ref_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

call OLP_Start(contract_file_name,ierr,stage,rndseed)

do subprocess = 0, 1
   call load_reference_kinematics(subprocess, blha_kinematics, renorm_scale)
   call compute_gosam_result(subprocess, blha_kinematics, renorm_scale, gosam_amp)
   call compute_reference_result(subprocess, ref_amp)
   if (subprocess .eq. 0) then
      do ic = 1, 2
         ch = channels(ic)
         write(ch,'(A58)') "----------------------------------------------------"
      end do
   end if

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

end do

if (success) then
   write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
else
   write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
end if

call OLP_Finalize()
close(unit=logf)

contains

subroutine load_reference_kinematics(subprocess, blha_kinematics, renorm_scale)
   use p0_gg_hddbar_model, only: p0_mD => mD, p0_mH => mH
   use p1_ddbar_huubar_model, only: p1_mD => mD, p1_mU => mU, p1_mH => mH
   implicit none
   integer, intent(in) :: subprocess
   real(ki), dimension(60), intent(out) :: blha_kinematics
   real(ki), intent(out) :: renorm_scale
   real(ki), dimension(5) :: mass

   if (subprocess .eq. 0) then
      mass(1) = p0_mD
      mass(2) = p0_mD
      mass(3) = p0_mH
      mass(4) = 0 ! gluon
      mass(5) = 0 ! gluon
   else if (subprocess .eq. 1) then
      mass(1) = p1_mD
      mass(2) = p1_mD
      mass(3) = p1_mH
      mass(4) = p1_mU
      mass(5) = p1_mU
   else
      write(logf,*) "ERROR: Invalid subprocess in ""load_reference_kinematics"""
      success = .false.
   end if

   ! syntax is: p0, p1, p2, p3, mass, <next particle>, ...
   blha_kinematics(1:5*5) = (/250.00000000000000_ki, 0.0000000000000000_ki, 0.0000000000000000_ki, 250.00000000000000_ki, mass(1),&
                             &250.00000000000000_ki, 0.0000000000000000_ki, 0.0000000000000000_ki,-250.00000000000000_ki, mass(2),&
                             &143.67785106160801_ki, 51.663364918413812_ki,-22.547134012261804_ki, 42.905108772983255_ki, mass(3),&
                             &190.20318863787611_ki,-153.36110830475005_ki,-108.23578590696623_ki,-30.702411577195452_ki, mass(4),&
                             &166.11896030051594_ki, 101.69774338633616_ki, 130.78291991922802_ki,-12.202697195787838_ki, mass(5)/)

   renorm_scale = 500

end  subroutine load_reference_kinematics

subroutine     compute_gosam_result(subprocess, blha_kinematics, renorm_scale, gosam_amp)
   implicit none
   integer, intent(in) :: subprocess
   real(ki), dimension(60), intent(in) :: blha_kinematics
   real(ki), intent(in) :: renorm_scale
   real(ki), dimension(0:3), intent(out) :: gosam_amp

   real(ki), dimension(60) :: blha_amp

   ! parameters(1) is interpreted as alpha_s
   real(ki), dimension(10) :: parameters = 1.0
   real(ki), parameter :: two_pi = &
            &6.2831853071795864769252867665590057683943387987502116419498891846156328125724179972560696506842341359&
            &64296173026564613294187689219101164463450718816256962234900568205403877042211119289_ki

   call OLP_EvalSubProcess(subprocess, blha_kinematics, renorm_scale,  parameters, blha_amp)

   gosam_amp(0) = blha_amp(4)
   gosam_amp(1) = blha_amp(3)/gosam_amp(0) * two_pi
   gosam_amp(2) = blha_amp(2)/gosam_amp(0) * two_pi
   gosam_amp(3) = blha_amp(1)/gosam_amp(0) * two_pi

   do ic = 1, 2
      ch = channels(ic)
      write(ch,'(A10,1x,A16,1x,G23.16)') "GOSAM,", "LO:", &
         & gosam_amp(0)
      write(ch,'(A10,1x,A16,1x,G23.16)') "GOSAM,", "NLO finite part:", &
         & gosam_amp(1)
      write(ch,'(A10,1x,A16,1x,G23.16)') "GOSAM,", "NLO single pole:", &
         & gosam_amp(2)
      write(ch,'(A10,1x,A16,1x,G23.16)') "GOSAM,", "NLO double pole:", &
         & gosam_amp(3)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(subprocess, amp)
   implicit none
   integer, intent(in) :: subprocess
   real(ki), dimension(0:3), intent(out) :: amp

   if (subprocess .eq. 1) then
      ! process g g -> h d d~
      amp(0) =   0.5677813961826772E-06_ki
      amp(1) =  66.66351423714880_ki
      amp(2) = -16.58166333155296_ki
      amp(3) =  -8.666666666666572_ki
   else if (subprocess .eq. 0) then
      ! process d d~ -> h u u~
      amp(0) =   0.1011096724203530E-06_ki
      amp(1) =  33.95216267342636_ki
      amp(2) = -13.86492928341135_ki
      amp(3) =  -5.333333333333357_ki
   else
      write(logf,*) "ERROR: Invalid subprocess for reference result selected"
      success = .false.
   end if

   do ic = 1, 2
      ch = channels(ic)
      write(ch,'(A10,1x,A16,1x,G23.16)') "REFERENCE,", "LO:", amp(0)
      write(ch,'(A10,1x,A16,1x,G23.16)') "REFERENCE,", "NLO finite part:", amp(1)
      write(ch,'(A10,1x,A16,1x,G23.16)') "REFERENCE,", "NLO single pole:", amp(2)
      write(ch,'(A10,1x,A16,1x,G23.16)') "REFERENCE,", "NLO double pole:", amp(3)
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
