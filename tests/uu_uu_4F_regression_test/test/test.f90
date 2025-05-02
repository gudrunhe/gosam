program test
    use uu_uu_config, only: ki, nlo_prefactors
    use uu_uu_kinematics, only: boost_to_cms
    use uu_uu_matrix, only: initgolem, exitgolem
    use uu_uu_rambo, only: ramb

    implicit none
    integer, parameter :: NEVT = 1
    integer :: ievt, ierr, prec
    integer :: ii, jj, kk, ee
    real(ki), parameter :: pi = 3.141592653589793_ki
    real(ki) :: scale2, factor, nlo_cpl, rat, factor2, eftfac, vev
    real(ki), dimension(5,4) :: vecs
    real(ki), dimension(0:7,0:3) :: amp, ref_amp
    real(ki), dimension(0:7,2:3) :: irp, ref_irp

    call initgolem()

    ! call random_seed

    nlo_prefactors=0  ! Do not include any NLO prefactors in order to recognize
                        ! rational numbers for the pole coefficients

    call get_reference(ievt,vecs,ref_amp,ref_irp)

    scale2 = (100._ki)**2

    call compute_gosam_result(vecs, scale2, gosam_amp)

    call check_reference(amp, irp, ref_amp, ref_irp)

    call exitgolem()

 contains

    subroutine load_reference_kinematics(vecs, scale2)
        use uu_uu_kinematics, only: adjust_kinematics, dotproduct
        implicit none
        real(ki), dimension(4, 4), intent(out) :: vecs
        real(ki), intent(out) :: scale2

        ! This kinematics was specified in 1103.0621v1 [hep-ph]
        vecs(1,:) = (/250.0_ki,  0.0_ki, 0.0_ki,  250.0_ki/)
        vecs(2,:) = (/250.0_ki,  0.0_ki, 0.0_ki, -250.0_ki/)
        vecs(3,:) = (/264.4_ki, -83.84841332241601_ki, -86.85350630148753_ki, &
                &  -202.3197272300720_ki/)
        vecs(4,:) = (/235.6_ki,  83.84841332241601_ki,  86.85350630148753_ki, &
                &   202.3197272300720_ki/)

        call adjust_kinematics(vecs)

        scale2 = 91.188_ki ** 2
    end  subroutine load_reference_kinematics

    subroutine     compute_gosam_result(vecs, scale2, amp)
        use uu_uu_matrix, only: samplitude
        implicit none

        real(ki), dimension(4, 4), intent(in) :: vecs
        real(ki), intent(in) :: scale2
        double precision, dimension(0:3), intent(out) :: amp
        integer :: prec

        call samplitude(vecs, scale2, amp, prec)

        do ic = 1, 2
        ch = channels(ic)
        write(ch,*) "GOSAM     AMP(0):       ", amp(0)
        write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
        write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
        write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
        end do
    end subroutine compute_gosam_result


    subroutine check_reference(amp, irp, ref_amp, ref_irp)
        implicit none
        integer, parameter :: logf = 27
        integer, dimension(2,4) ::eftc
        integer :: ee, ii, jj, kk
        real(ki), dimension(0:7,0:3), intent(in) :: amp, ref_amp
        real(ki), dimension(0:7,2:3), intent(in) :: irp, ref_irp
        real(ki), parameter :: eps = 1e-7_ki
        real(ki) :: diff
        logical :: success, isuccess
        character(33), dimension(0:7) :: truncations

        eftc(1,:) = (/0,1,4,5/)
        eftc(2,:) = (/2,3,6,7/)

        truncations = (/ &
            & "sigma(SM X SM) + sigma(SM X dim6)", &
            & "sigma(SM + dim6 X SM + dim6)     ", &
            & "sigma(SM X SM) + sigma(SM X dim6)", &
            & "sigma(SM + dim6 X SM + dim6)     ", &
            & "sigma(SM X dim6)                 ", &
            & "sigma(dim6 X dim6)               ", &
            & "sigma(SM X dim6)                 ", &
            & "sigma(dim6 X dim6)               " &
            & /)

        open(file="test.log", unit=logf)

        success = .true.

        write(6,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev 3518ed0)."
        write(logf,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev 3518ed0)."

        do ii = 1, 2
            select case(ii)
            case(1)
            write(6,*) "Checking truncation orders ignoring loopcounting."
            write(logf,*) "Checking truncation orders ignoring loopcounting."
            case(2)
            write(6,*) "Checking truncation orders respecting loopcounting."
            write(logf,*) "Checking truncation orders respecting loopcounting."
            case default
            print *, "Should not get here. Stop."
            stop
            end select
            do jj = 1, 4
            isuccess = .true.
            ee = eftc(ii,jj)
            write(6,'(A18,I1,A2,A33,A1)') "Truncation option ", ee, " (", truncations(ee), ")"
            write(logf,'(A18,I1,A2,A33,A1)') "Truncation option ", ee, " (", truncations(ee), ")"
            do kk = 0, 3
                diff = 0._ki
                diff = abs(rel_diff(amp(ee,kk),ref_amp(ee,kk)))
                if(diff.gt.eps) then
                    write(6,'(A57,I1,A8,I2,A13,E13.7)') &
                        & "Result 'amp' differs from reference for truncation option", &
                        & ee, ", entry ", kk, ". rel_diff = ", diff
                    write(logf,'(A57,I1,A8,I2,A13,E13.7)') &
                        & "Result 'amp' differs from reference for truncation option", &
                        & ee, ", entry ", kk, ". rel_diff = ", diff
                    success = .false.
                    isuccess = .false.
                end if
            end do
            do kk = 2, 3
                diff = 0._ki
                diff = abs(rel_diff(irp(ee,kk),ref_irp(ee,kk)))
                if(diff.gt.eps) then
                    write(6,'(A57,I1,A8,I2,A13,E13.7)') &
                        & "Result 'irp' differs from reference for truncation option", &
                        & ee, ", entry ", kk, ". rel_diff = ", diff
                    write(logf,'(A57,I1,A8,I2,A13,E13.7)') &
                        & "Result 'irp' differs from reference for truncation option", &
                        & ee, ", entry ", kk, ". rel_diff = ", diff
                    success = .false.
                    isuccess = .false.
                end if
            end do
            if(isuccess) then
                write(6,*) "OK"
                write(logf,*) "OK"
            else
                write(6,*) "--"
                write(logf,*) "--"
            end if
            end do
        end do

            if (success) then
        write(logf,'(A15)') "@@@ SUCCESS @@@"
        else
        write(logf,'(A15)') "@@@ FAILURE @@@"
        end if

        close(unit=logf)

    end subroutine check_reference


    function rel_diff(a, b)
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
