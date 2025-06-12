program test
    use uu_uu_config, only: ki
    use uu_uu_kinematics, only: boost_to_cms
    use uu_uu_matrix, only: initgolem, exitgolem

    implicit none
    integer, parameter :: logf = 27

    integer, dimension(2) :: channels
    integer :: ic, ch

    integer :: ievt, ierr, prec
    integer :: ii, jj, kk, ee
    real(ki), parameter :: pi = 3.141592653589793_ki
    real(ki) :: scale2, factor, nlo_cpl, rat, factor2, eftfac, vev
    real(ki), dimension(4,4) :: vecs
    double precision :: amp, ref_amp, diff
    logical :: success
    double precision, parameter :: eps = 1.0d-4

    channels(1) = logf
    channels(2) = 6

    open(file="test.log", unit=logf)

    success = .true.

    call load_reference_kinematics2(vecs, scale2)

    call initgolem()

    call compute_gosam_result(vecs, scale2, amp)

    call get_reference(ref_amp)

    diff = abs(rel_diff(amp, ref_amp))

    do ic = 1, 2
    ch = channels(ic)
    if (diff .gt. eps) then
       write(unit=ch,fmt="(A3,1x,A40)") "==>", &
       & "Comparison of LO failed!"
       write(unit=ch,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff
       success = .false.
    end if

    if (success) then
       write(unit=ch,fmt="(A15)") "@@@ SUCCESS @@@"
    else
       write(unit=ch,fmt="(A15)") "@@@ FAILURE @@@"
    end if
    end do
    close(unit=logf)

    call exitgolem()

 contains

    subroutine load_reference_kinematics2(vecs, scale2)
        use uu_uu_kinematics, only: adjust_kinematics, dotproduct
        implicit none
        real(ki), dimension(4, 4), intent(out) :: vecs
        real(ki), intent(out) :: scale2

        vecs(1,:) =  (/ 1.0_ki, 0.0_ki, 0.0_ki, 1.0_ki /)
        vecs(2,:) =  (/ 1.0_ki, 0.0_ki, 0.0_ki, -1.0_ki /)
        vecs(3,:) = (/ 1.0_ki, -0.76594518737961759_ki, 0.55704927586770248_ki, -0.32097363471984863_ki /)
        vecs(4,:) = (/ 1.0_ki, 0.76594518737961759_ki, -0.55704927586770248_ki, 0.32097363471984863_ki /)

        call adjust_kinematics(vecs)

        scale2 = 0.2_ki ** 2
    end  subroutine load_reference_kinematics2

    subroutine get_reference(ref_amp)
        implicit none
        real(ki), intent(out) :: ref_amp

        ! Computed with MadGraph5_aMC@NLO 3.6.2
        ref_amp = 224.94241535685737_ki

        do ic = 1, 2
        ch = channels(ic)
        write(ch,*) "MG5       AMP:       ", ref_amp
        end do
    end subroutine get_reference

    subroutine     compute_gosam_result(vecs, scale2, gosam_amp)
        use uu_uu_matrix, only: samplitude
        implicit none

        real(ki), dimension(4, 4), intent(in) :: vecs
        real(ki), intent(in) :: scale2
        real(ki), dimension(0:3) :: amp
        real(ki), intent(out) :: gosam_amp
        integer :: prec

        call samplitude(vecs, scale2, amp, prec)
        gosam_amp = amp(0)

        do ic = 1, 2
        ch = channels(ic)
        write(ch,*) "GOSAM     AMP:       ", gosam_amp
        end do
    end subroutine compute_gosam_result

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
