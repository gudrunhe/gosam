program test
   use Hbb_4F_config, only: ki, logfile, renormalisation, convert_to_thv
   use Hbb_4F_model
   use Hbb_4F_color, only: CA, CF
   use Hbb_4F_matrix, only: samplitude, initgolem, exitgolem

   implicit none
   integer :: ievt, ierr, prec
   real(ki), dimension(3, 4) :: vecs
   real(ki), dimension(0:3) :: amp, ref_amp, diff
   real(ki) :: scale2, scale
   real(ki), parameter :: eps = 1.0e-10_ki
   real(ki) :: PI = 3.141592653589793_ki

   ! log and output
   integer, parameter :: logf = 27
   logical :: success
   integer, dimension(2) :: channels
   integer :: ic, ch

   channels(1) = logf
   channels(2) = 6

   open(file="test.log", unit=logf)
   success = .true.

   call initgolem()

   scale = mdlMH/2._ki
   scale2 = mdlMH**2/4._ki

   vecs(1,:) = (/mdlMH,0._ki,0._ki,0._ki/)
   vecs(1,:) = (/mdlMH,0._ki,0._ki,0._ki/)
   vecs(2,:) = (/mdlMH/2._ki,0._ki,0._ki,sqrt(mdlMH**2/4._ki-mdlMB**2)/)
   vecs(3,:) = (/mdlMH/2._ki,0._ki,0._ki,-sqrt(mdlMH**2/4._ki-mdlMB**2)/)

   renormalisation = 0

   call set_parameter("mdlWT", 0.0_ki, 0.0_ki, ierr)

   call compute_gosam_result(vecs, scale2, amp)
   call analytic_result(scale, ref_amp)

   diff = abs(rel_diff(amp, ref_amp))

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

   call exitgolem()

contains

    subroutine compute_gosam_result(vecs, scale2, amp)
        implicit none
        real(ki), dimension(3, 4), intent(in) :: vecs
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
    end subroutine

    subroutine analytic_result(scale, amp)
        implicit none
        real(ki), intent(in) :: scale
        real(ki), dimension(0:3), intent(out):: amp
        real(ki) :: C1, C0, ndr_shift
        ! Analytic result in NDR from 1512.02508
        C1 = ( &
            4._ki*mdlMB * (3._ki * mdlMB**2 - mdlMH**2 / 2._ki) * (mdlCqb1 + CF * mdlCqb8) &
            - mdlMT * (3._ki * mdlMT**2 - mdlMH**2 / 2._ki) * ((1._ki + 2._ki * NC) * mdlCqtqb1 + CF * mdlCqtqb8) &
            ) / mdlvev
        C0 = ( &
            mdlMB * (4._ki * I8hat(mdlMB, scale) - 6._ki * mdlMB**2 + mdlMH**2) * (mdlCqb1 + CF * mdlCqb8) &
            - mdlMT * I8hat(mdlMT, scale) * ((1._ki + 2._ki * NC) * mdlCqtqb1 + CF * mdlCqtqb8) &
            ) / mdlvev
        ! From 2310.18221 to convert from NDR to (BM)HV (equivalent to DRED for this process)
        ndr_shift = mdlMB * (mdlCqb1 + CF * mdlCqb8) * (6.0_ki * mdlMB**2 - mdlMH**2) / mdlvev

        amp(0) = 2.0_ki * CA * mdlMB**2 * (mdlMH**2 - 4.0_ki*mdlMB**2) / mdlvev**2
        amp(1) = CA * mdlMB * (mdlMH**2 - 4.0_ki*mdlMB**2) / mdlvev * (C0 + ndr_shift) / 4._ki / PI**2
        amp(2) = CA * mdlMB * (mdlMH**2 - 4.0_ki*mdlMB**2) / mdlvev * C1 / 4._ki / PI**2
        amp(3) = 0.0_ki

        do ic = 1, 2
            ch = channels(ic)
            write(ch,*) "REFERENCE AMP(0):       ", amp(0)
            write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)
            write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)
            write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)
        end do
    end subroutine

    function I8hat(mass, scale) result(res)
        use avh_olo
        implicit none
        real(ki), intent(in) :: mass, scale
        real(ki) :: res
        complex(ki), dimension(0:2) :: a0c, b0c
        call avh_olo_mu_set(scale)
        call avh_olo_a0m(a0c, complex(mass**2, 0.0_ki))
        call avh_olo_b0m(b0c, complex(mdlMH**2, 0.0_ki), complex(mass**2, 0.0_ki), complex(mass**2, 0.0_ki))
        res = a0c(0) - (mdlMH**2 - 4.0_ki*mass**2) * b0c(0) / 2.0_ki
    end function

    pure elemental function rel_diff(a, b)
        implicit none

        real(ki), intent(in) :: a, b
        real(ki) :: rel_diff

        if (a.eq.0.0_ki .and. b.eq.0.0_ki) then
            rel_diff = 0.0_ki
        else
            rel_diff = 2.0_ki * (a-b) / (abs(a)+abs(b))
        end if
    end  function rel_diff

end program
