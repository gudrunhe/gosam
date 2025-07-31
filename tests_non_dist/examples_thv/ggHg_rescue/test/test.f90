program     test
   use ggHg_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
   use ggHg_matrix, only: initgolem, exitgolem
   use ggHg_kinematics, only: inspect_kinematics, init_event
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

subroutine load_reference_kinematics(vecs, scale2)
use ggHg_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   ! (* pt1: s12 =250000.00000000000, s13= -92336.157463848474 - stable *)
   !vecs(1,1) =  250.0_ki
   !vecs(1,2) =    0.0_ki
   !vecs(1,3) =    0.0_ki
   !vecs(1,4) =  250.0_ki

   !vecs(2,1) =  250.0_ki
   !vecs(2,2) =    0.0_ki
   !vecs(2,3) =    0.0_ki
   !vecs(2,4) = -250.0_ki

   !vecs(3,1) =  265.625000000000000000000000000_ki
   !vecs(3,2) =  0.0_ki
   !vecs(3,3) =  -229.044283320067743308883061580_ki
   !vecs(3,4) =  -49.7026850723030590511012695207_ki

   !vecs(4,1) =  234.375000000000000000000000000_ki
   !vecs(4,2) =  0.0_ki
   !vecs(4,3) =  229.044283320067743308883061580_ki
   !vecs(4,4) =  49.7026850723030590511012695207_ki


   ! (* pt2: s12 =250000.00000000000, s13= -9952.7515384127764 - stable*)
   !vecs(1,1) =  250.0_ki
   !vecs(1,2) =    0.0_ki
   !vecs(1,3) =    0.0_ki
   !vecs(1,4) =  250.0_ki

   !vecs(2,1) =  250.0_ki
   !vecs(2,2) =    0.0_ki
   !vecs(2,3) =    0.0_ki
   !vecs(2,4) = -250.0_ki

   !vecs(3,1) =  265.625000000000000000000000000_ki
   !vecs(3,2) =  0.0_ki
   !vecs(3,3) =  -94.5223545756265365277289694364_ki
   !vecs(3,4) =  -214.469496923174445986172261516_ki

   !vecs(4,1) =  234.375000000000000000000000000_ki
   !vecs(4,2) =  0.0_ki
   !vecs(4,3) =  94.5223545756265365277289694364_ki
   !vecs(4,4) =  214.469496923174445986172261516_ki


   ! (* pt3: s12 =250000.00000000000, s13= -500 - unstable => quad)
   vecs(1,1) =  250.0_ki
   vecs(1,2) =    0.0_ki
   vecs(1,3) =    0.0_ki
   vecs(1,4) =  250.0_ki

   vecs(2,1) =  250.0_ki
   vecs(2,2) =    0.0_ki
   vecs(2,3) =    0.0_ki
   vecs(2,4) = -250.0_ki

   vecs(3,1) =  265.625000000000000000000000000_ki
   vecs(3,2) =  0.0_ki
   vecs(3,3) =  -2.16504041532715958458907646670_ki
   vecs(3,4) =  -234.365000000000000000702564468_ki

   vecs(4,1) =  234.375000000000000000000000000_ki
   vecs(4,2) =  0.0_ki
   vecs(4,3) =  2.16504041532715958458907646670_ki
   vecs(4,4) =  234.365000000000000000702564468_ki

   ! (* pt4: s12 =250000.00000000000, s13= -0.000000005 - very unstable => fail)
   !vecs(1,1) =  250.0_ki
   !vecs(1,2) =    0.0_ki
   !vecs(1,3) =    0.0_ki
   !vecs(1,4) =  250.0_ki

   !vecs(2,1) =  250.0_ki
   !vecs(2,2) =    0.0_ki
   !vecs(2,3) =    0.0_ki
   !vecs(2,4) = -250.0_ki

   !vecs(3,1) =  265.625000000000000000000000000_ki
   !vecs(3,2) =  0.0_ki
   !vecs(3,3) =  -0.0000684653196881457522818292761907_ki
   !vecs(3,4) =  -234.374999899999999999999977751_ki

   !vecs(4,1) =  234.375000000000000000000000000_ki
   !vecs(4,2) =  0.0_ki
   !vecs(4,3) =  0.0000684653196881457522818292761907_ki
   !vecs(4,4) =  234.374999899999999999999977751_ki


   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use ggHg_config
   use ggHg_model, only:  set_parameter
   implicit none
   integer :: ierr = 0

   ! gf == Pi*alp/(Sqrt[2]*mw^2*(1-mw^2/mz^2)
   ! alp = e^2/(4*Pi)
   ! e = 0.3
   ewchoice = 1

   call set_parameter("GF", 0.000011663700000_ki, 0.0_ki, ierr)
   call set_parameter("mZ", 90.1861_ki, 0.0_ki, ierr)
   call set_parameter("mW", 80.0_ki, 0.0_ki, ierr)
   call set_parameter("e", 0.3_ki, 0.0_ki, ierr)
   call set_parameter("Nf", 1.0_ki, 0.0_ki, ierr)
   call set_parameter("Nfgen", 1.0_ki, 0.0_ki, ierr)
   call set_parameter("mT", 171.2000000000000_ki, 0.0_ki, ierr)
   call set_parameter("mH", 125.0000000000000_ki, 0.0_ki, ierr)

end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use ggHg_matrix, only: samplitude
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

   !amp = 1.0476110124875102_ki ! pt1
   !amp = 8.5181382409728759_ki ! pt2
   amp = 17329.589029632152_ki ! pt3
   !amp = 17329806665462.062_ki ! pt4
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
