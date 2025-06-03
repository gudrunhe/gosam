program test

   use ddzg_config, only: ki, logfile, nlo_prefactors
   use ddzg_kinematics, only: dotproduct !, boost_to_cms
   use ddzg_color, only: numcs, CA
   !use ddzg_kinematics, only: boost_to_cms
   !use ddzg_rambo, only: ramb

   use ddzg_matrix, only: &
   & ddzg_samplitude => samplitude, &
   & ddzg_initgolem => initgolem, &
   & ddzg_exitgolem => exitgolem, &
   & ddzg_ir_subtraction => ir_subtraction

   use ddzg_model, only: &
   & ddzg_gauge4z => gauge4z, &
   & ddzg_gTr => gTr, &
   & ddzg_gTl => gTl

   use dgzd_matrix, only: &
   & dgzd_samplitude => samplitude, &
   & dgzd_initgolem => initgolem, &
   & dgzd_exitgolem => exitgolem, &
   & dgzd_ir_subtraction => ir_subtraction

   use dgzd_model, only: &
   & dgzd_gauge2z => gauge2z, &
   & dgzd_gTr => gTr, &
   & dgzd_gTl => gTl

   implicit none

   ! unit of the log file
   integer, parameter :: logf = 27
   integer, parameter :: gosamlogf = 19
   integer, dimension(2) :: channels
   integer :: ic, ch
   integer :: ievt, ierr, prec
   real(ki), dimension(4, 4) :: vecs, vecs_crossed
   real(ki) :: scale2
   real(ki) :: fac
   real(ki), dimension(0:3) :: ref_amp
   real(ki), dimension(0:3) :: ddzg_amp0, ddzg_amp1
   real(ki), dimension(0:3) :: dgzd_amp0, dgzd_amp1
   real(ki), dimension(2:3) :: ddzg_irp0, ddzg_irp1
   real(ki), dimension(2:3) :: dgzd_irp0, dgzd_irp1
   complex(ki) :: gauge0 = ( 0.0_ki, 0.0_ki )
   complex(ki) :: gauge1 = ( 1.0_ki, 0.0_ki )
   logical :: exclude_top
   double precision, parameter :: eps = 1.0d-4
   logical :: amplitudes_equal, success

   channels(1) = logf
   channels(2) = 6

   open(file="test.log", unit=logf)

   scale2 = 500.00000000000000_ki * 500.00000000000000_ki

   ! Point 1
   vecs(1,:) = (/ 250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,        250.00000000000000_ki /)
   vecs(2,:) = (/ 250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,       -250.00000000000000_ki /)
   vecs(3,:) = (/ 258.31525134399999_ki,       -117.14896464211708_ki,        163.81951079222944_ki,       -133.60690738127471_ki /)
   vecs(4,:) = (/ 241.68474865600007_ki,        117.14896464211711_ki,       -163.81951079222944_ki,        133.60690738127468_ki /)
   ! 2 <-> -4
   vecs_crossed(1,:) = (/ 250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,        250.00000000000000_ki /)
   vecs_crossed(2,:) = (/ -241.68474865600007_ki,       -117.14896464211711_ki,       163.81951079222944_ki,        -133.60690738127468_ki /)
   vecs_crossed(3,:) = (/ 258.31525134399999_ki,        -117.14896464211708_ki,       163.81951079222944_ki,        -133.60690738127471_ki /)
   vecs_crossed(4,:) = (/ -250.00000000000000_ki,       -0.0000000000000000_ki,       -0.0000000000000000_ki,       250.00000000000000_ki /)

   ! Point 1 hardcoded result (computed with Gosam, cross-checked with OpenLoops)
   ref_amp = (/ 2.004083979006331_ki, -7.123099740488900_ki, -26.63290597771187_ki, -11.35647588103587_ki /)

!   ! Point 2
!   vecs(1,:) = (/     250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,        250.00000000000000_ki /)
!   vecs(2,:) = (/     250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,       -250.00000000000000_ki /)
!   vecs(3,:) = (/     258.31525134399993_ki,       -151.29364531250172_ki,        43.250692646028334_ki,        183.44243840128047_ki /)
!   vecs(4,:) = (/     241.68474865600007_ki,        151.29364531250170_ki,       -43.250692646028291_ki,       -183.44243840128044_ki /)
!   ! 2 <-> -4
!   vecs_crossed(1,:) = (/     250.00000000000000_ki,        0.0000000000000000_ki,        0.0000000000000000_ki,        250.00000000000000_ki /)
!   vecs_crossed(2,:) = (/     -241.68474865600007_ki,        -151.29364531250170_ki,       43.250692646028291_ki,       183.44243840128044_ki /)
!   vecs_crossed(3,:) = (/     258.31525134399993_ki,       -151.29364531250172_ki,        43.250692646028334_ki,        183.44243840128047_ki /)
!   vecs_crossed(4,:) = (/     -250.00000000000000_ki,        -0.0000000000000000_ki,        -0.0000000000000000_ki,       250.00000000000000_ki /)
!
!   ! Point 2 hardcoded result (computed with Gosam, cross-checked with OpenLoops)
!   ref_amp = (/ 3.896250580049525_ki, -23.27254421060536_ki, -57.54754527591247_ki, -22.07875328694725_ki /)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "# vecs(1,:)", vecs(1,:)
      write(ch,*) "# vecs(2,:)", vecs(2,:)
      write(ch,*) "# vecs(3,:)", vecs(3,:)
      write(ch,*) "# vecs(4,:)", vecs(4,:)
      write(ch,*) ""
   end do

   fac = 8.0_ki/3.0_ki ! correct color averaging factor g->q

   exclude_top = .true.

   ! Compute ddzg with gauge4z = 0 excluding top contribution
   call ddzg_amplitude(vecs,scale2,gauge0,exclude_top,ddzg_amp0,ddzg_irp0)

   ! Compute ddzg with gauge4z = 1 excluding top contribution
   call ddzg_amplitude(vecs,scale2,gauge1,exclude_top,ddzg_amp1,ddzg_irp1)

   ! Compute dgzd with gauge2z = 0 excluding top contribution
   call dgzd_amplitude(vecs_crossed,scale2,gauge0,exclude_top,dgzd_amp0,dgzd_irp0)

   ! Compute dgzd with gauge2z = 1 excluding top contribution
   call dgzd_amplitude(vecs_crossed,scale2,gauge1,exclude_top,dgzd_amp1,dgzd_irp1)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "# == Excluding top quark contribution == "
      write(ch,*) "# NOTE: Appearance of axial anomaly when excluding the top quark contribution makes this process gauge and crossing dependent"
      write(ch,'(A1,20x,A12,11x,A12,11x,A12,11x,A12)') "#", "ddzg gauge=0", "ddzg gauge=1", "dgzg gauge=0", "dgzg gauge=1"
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "LO:", ddzg_amp0(0), ddzg_amp1(0), dgzd_amp0(0)*fac, dgzd_amp1(0)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, finite part:", ddzg_amp0(1), ddzg_amp1(1), dgzd_amp0(1)*fac, dgzd_amp1(1)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, single pole:", ddzg_amp0(2), ddzg_amp1(2), dgzd_amp0(2)*fac, dgzd_amp1(2)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, double pole:", ddzg_amp0(3), ddzg_amp1(3), dgzd_amp0(3)*fac, dgzd_amp1(3)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "IR,  single pole:", ddzg_irp0(2)/ddzg_amp0(0), ddzg_irp1(2)/ddzg_amp1(0), dgzd_irp0(2)/dgzd_amp0(0), dgzd_irp1(2)/dgzd_amp1(0)
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "IR,  double pole:", ddzg_irp0(3)/ddzg_amp0(0), ddzg_irp1(3)/ddzg_amp1(0), dgzd_irp0(3)/dgzd_amp0(0), dgzd_irp1(3)/dgzd_amp1(0)
      write(ch,*) ""
   end do

   exclude_top = .false.

   ! Compute ddzg with gauge4z = 0 including top contribution
   call ddzg_amplitude(vecs,scale2,gauge0,exclude_top,ddzg_amp0,ddzg_irp0)

   ! Compute ddzg with gauge4z = 1 including top contribution
   call ddzg_amplitude(vecs,scale2,gauge1,exclude_top,ddzg_amp1,ddzg_irp1)

   ! Compute dgzd with gauge2z = 0 including top contribution
   call dgzd_amplitude(vecs_crossed,scale2,gauge0,exclude_top,dgzd_amp0,dgzd_irp0)

   ! Compute dgzd with gauge2z = 1 including top contribution
   call dgzd_amplitude(vecs_crossed,scale2,gauge1,exclude_top,dgzd_amp1,dgzd_irp1)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "# == Including top quark contribution == "
      write(ch,'(A1,20x,A12,11x,A12,11x,A12,11x,A12)') "#", "ddzg gauge=0", "ddzg gauge=1", "dgzg gauge=0", "dgzg gauge=1"
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "LO:", ddzg_amp0(0), ddzg_amp1(0), dgzd_amp0(0)*fac, dgzd_amp1(0)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, finite part:", ddzg_amp0(1), ddzg_amp1(1), dgzd_amp0(1)*fac, dgzd_amp1(1)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, single pole:", ddzg_amp0(2), ddzg_amp1(2), dgzd_amp0(2)*fac, dgzd_amp1(2)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "NLO, double pole:", ddzg_amp0(3), ddzg_amp1(3), dgzd_amp0(3)*fac, dgzd_amp1(3)*fac
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "IR,  single pole:", ddzg_irp0(2)/ddzg_amp0(0), ddzg_irp1(2)/ddzg_amp1(0), dgzd_irp0(2)/dgzd_amp0(0), dgzd_irp1(2)/dgzd_amp1(0)
      write(ch,'(A1,1x,A17,1x,G23.16,G23.16,G23.16,G23.16)') "#", "IR,  double pole:", ddzg_irp0(3)/ddzg_amp0(0), ddzg_irp1(3)/ddzg_amp1(0), dgzd_irp0(3)/dgzd_amp0(0), dgzd_irp1(3)/dgzd_amp1(0)
   end do

   ! Check equality of ref_amp with all 4 amplitudes
   success = .true.

   call check_equality(ddzg_amp0,ref_amp,eps,1.0_ki,amplitudes_equal)
   if(.not.amplitudes_equal) then
      success = .false.
   end if

   call check_equality(ddzg_amp1,ref_amp,eps,1.0_ki,amplitudes_equal)
   if(.not.amplitudes_equal) then
      success = .false.
   end if

   call check_equality(dgzd_amp0,ref_amp,eps,fac,amplitudes_equal)
   if(.not.amplitudes_equal) then
      success = .false.
   end if

   call check_equality(dgzd_amp1,ref_amp,eps,fac,amplitudes_equal)
   if(.not.amplitudes_equal) then
      success = .false.
   end if

   if (success) then
      write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
   else
      write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
   end if

   close(unit=logf)

contains

subroutine check_equality(a,b,eps,fac,amplitudes_equal)
   implicit none

   real(ki), dimension(0:3) :: a, b, diff
   double precision :: eps
   real(ki) :: fac
   logical :: amplitudes_equal

   amplitudes_equal = .true.

   diff = abs(rel_diff(a*fac, b))

   if (diff(0) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", "Comparison of LO failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
      amplitudes_equal = .false.
   end if

   if (diff(1) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Comparison of NLO/finite part failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(1)
      amplitudes_equal = .false.
   end if

   if (diff(2) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A40)") "==>", &
      & "Comparison of NLO/single pole failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
      amplitudes_equal = .false.
   end if

   if (diff(3) .gt. eps) then
      write(unit=logf,fmt="(A3,1x,A30)") "==>", &
      & "Comparison of NLO/double pole failed!"
      write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(3)
      amplitudes_equal = .false.
   end if

end subroutine check_equality

subroutine ddzg_amplitude(vecs,scale2,gauge,exclude_top,amp,irp)

   implicit none

   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2
   complex(ki) :: gauge
   real(ki), dimension(0:3) :: amp
   real(ki), dimension(2:3) :: irp
   logical :: exclude_top
   real(ki) :: t1, t2
   real(ki) :: orig_ddzg_gTr, orig_ddzg_gTl

   call ddzg_initgolem()

   ddzg_gauge4z = gauge

   nlo_prefactors=0

   if(exclude_top) then
      orig_ddzg_gTr = ddzg_gTr
      orig_ddzg_gTl = ddzg_gTl
      ddzg_gTr = 0.0_ki
      ddzg_gTl = 0.0_ki
   end if

   call ddzg_samplitude(vecs, scale2, amp, prec)
   call ddzg_ir_subtraction(vecs, scale2, irp)

   if(exclude_top) then
      ddzg_gTr = orig_ddzg_gTr
      ddzg_gTl = orig_ddzg_gTl
   end if

   call ddzg_exitgolem()

end subroutine ddzg_amplitude

subroutine dgzd_amplitude(vecs,scale2,gauge,exclude_top,amp,irp)

   implicit none

   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2
   complex(ki) :: gauge
   real(ki), dimension(0:3) :: amp
   real(ki), dimension(2:3) :: irp
   logical :: exclude_top
   real(ki) :: t1, t2
   real(ki) :: orig_dgzd_gTr, orig_dgzd_gTl

   call dgzd_initgolem()

   dgzd_gauge2z = gauge

   nlo_prefactors=0

   if(exclude_top) then
      orig_dgzd_gTr = dgzd_gTr
      orig_dgzd_gTl = dgzd_gTl
      dgzd_gTr = 0.0_ki
      dgzd_gTl = 0.0_ki
   end if

   call dgzd_samplitude(vecs, scale2, amp, prec)
   call dgzd_ir_subtraction(vecs, scale2, irp)

   if(exclude_top) then
      dgzd_gTr = orig_dgzd_gTr
      dgzd_gTl = orig_dgzd_gTl
   end if

   call dgzd_exitgolem()

end subroutine dgzd_amplitude

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
