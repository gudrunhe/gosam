program     test
   use gggz_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
   use gggz_matrix, only: initgolem, exitgolem
   use gggz_kinematics, only: inspect_kinematics, init_event
   implicit none

   ! unit of the log file
   integer, parameter :: logf = 27
   integer, parameter :: gosamlogf = 19

   integer, dimension(2) :: channels
   integer :: ic, ch

   double precision, parameter :: eps = 1.0d-4
   double precision, parameter :: abs_eps = 1.0d-10

   logical :: success

   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2

   double precision, dimension(0:3) :: gosam_amp
   double precision :: ref_amp, diff

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

   diff = abs(rel_diff(gosam_amp(1), ref_amp))

   if (gosam_amp(0) .gt. abs_eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Comparison of LO failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "VALUE:", gosam_amp(0)
      success = .false.
   end if

   if (diff .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Comparison of NLO/finite part failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff
      success = .false.
   end if

   if (gosam_amp(2) .gt. abs_eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Comparison of NLO/single pole failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", gosam_amp(2)
      success = .false.
   end if

   if (gosam_amp(3) .gt. abs_eps) then
      write(unit=logf,fmt="(A3,1x,A30)") "==>", &
      & "Comparison of NLO/double pole failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", gosam_amp(3)
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
use gggz_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   vecs(1,1) =  100.0_ki
   vecs(1,2) =    0.0_ki
   vecs(1,3) =    0.0_ki
   vecs(1,4) =  100.0_ki

   vecs(2,1) =  100.0_ki
   vecs(2,2) =    0.0_ki
   vecs(2,3) =    0.0_ki
   vecs(2,4) = -100.0_ki

   vecs(3,1) =   79.21205401560000_ki
   vecs(3,2) =    3.65874234516586_ki
   vecs(3,3) = - 25.12459426066790_ki
   vecs(3,4) =   75.03277863080130_ki

   vecs(4,1) =  120.78794598440000_ki
   vecs(4,2) = -  3.65874234516586_ki
   vecs(4,3) =   25.12459426066790_ki
   vecs(4,4) = - 75.03277863080130_ki

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use gggz_config
   use gggz_model, only: Nf, Nfgen, mZ, mW, mU
   implicit none

   renormalisation = 0
   ! reduction_interoperation = 0

   mZ = 91.1876_ki
   mW = mZ * sqrt(1.0_ki - 0.4808222_ki**2)

   Nf    = 2.0_ki
   Nfgen = 2.0_ki

   mU = 2.0_ki

   convert_to_cdr = .false.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use gggz_matrix, only: samplitude
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   logical :: ok

   call samplitude(vecs, scale2, amp, prec, ok)


   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(1):", amp(1)
      write(ch,*) "GOSAM     AMP(2):", amp(2)
      write(ch,*) "GOSAM     AMP(3):", amp(3)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, intent(out) :: amp

   amp = 0.107574259950483_ki
   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(1):", amp
      write(ch,*) "REFERENCE AMP(2):", 0.0_ki
      write(ch,*) "REFERENCE AMP(3):", 0.0_ki
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
