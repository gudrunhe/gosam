program test
use ggHg_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use ggHg_matrix, only: initgolem, exitgolem
use ggHg_kinematics, only: inspect_kinematics, init_event, dotproduct
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
   use ggHg_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(5, 4) :: start_vecs
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   start_vecs(1,:)=(/   298.17848024073913_ki,   0.0000000000000000_ki, &
        &   0.0000000000000000_ki,   298.17848024073913_ki /)
   start_vecs(2,:)=(/   298.17848024073913_ki,   0.0000000000000000_ki, &
        &   0.0000000000000000_ki,  -298.17848024073913_ki /)
   start_vecs(3,:)=(/   166.34601212495804_ki,  -160.07861409570359_ki, &
        &  -6.8750671787421194_ki,  -44.705329775801431_ki /)
   start_vecs(4,:)=(/   144.93284342404036_ki,  -122.48970917623723_ki, &
        &  -13.908717839073878_ki,   76.212517455935341_ki /)
   start_vecs(5,:)=(/   285.07810493247985_ki,   282.56832327194081_ki, &
        &   20.783785017815998_ki,  -31.507187680133825_ki /)

   vecs(1,:) = start_vecs(1,:)
   vecs(2,:) = start_vecs(2,:)
   vecs(3,:) = start_vecs(3,:) + start_vecs(4,:)
   vecs(4,:) = start_vecs(5,:)

   call adjust_kinematics(vecs)

   scale2 = 125_ki**2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ggHg_config, only: renormalisation, convert_to_cdr !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar
   use ggHg_model, only: GF, mH, mW, mZ, alpha, Nf, Nfgen, sqrt2, gH
   implicit none
   real(ki), parameter :: pi = 3.14159265358979323846264&
        &3383279502884197169399375105820974944592307816406286209_ki
   renormalisation = 1

   mH = 125.0_ki
   mW = 80.419_ki
   mZ = 91.1876_ki
   GF = 1.16639E-05_ki

   !alpha = mW**2*(1.0_ki-mW*mW/mZ/mZ)*8.0_ki*GF/sqrt2/4.0_ki/pi

   Nf    = 5
   Nfgen = 1

   convert_to_cdr = .true.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ggHg_matrix, only: samplitude
   use ggHg_model, only: GF, gH, sqrt2
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   double precision, dimension(0:3) :: gauge_amp, diff
   integer :: prec

   logical :: ok, gok

   real(ki), parameter :: pi = 3.14159265358979323846264&
        &3383279502884197169399375105820974944592307816406286209_ki 

   gH = 1.0_ki/(24.0_ki*pi*pi*sqrt(sqrt2/8.0_ki/GF))

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
   use ggHg_kinematics, only: dotproduct
   use ggHg_matrix, only: ir_subtraction
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   real(ki) :: alpha_s
   double precision, dimension(0:3), intent(out) :: amp
   real(ki), parameter :: pi = 3.14159265358979323846264&
        &3383279502884197169399375105820974944592307816406286209_ki

   alpha_s=0.12380606648525325_ki

   amp(0) = 0.00072745638706144032_ki/(4.0_ki*pi*alpha_s)**3

   ! This is the result from MCFM:
   amp(1) =  13.195495732443119_ki*amp(0)
   amp(2) =  12.160134391476900_ki*amp(0)
   amp(3) = -9.0000000000000000_ki*amp(0)

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
