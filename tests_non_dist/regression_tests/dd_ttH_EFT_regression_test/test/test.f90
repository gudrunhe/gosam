program test
   use dd_ttH_config, only: ki, nlo_prefactors, EFTcount
   use dd_ttH_kinematics, only: boost_to_cms
   use dd_ttH_matrix, only: samplitude, &
        & initgolem, exitgolem, ir_subtraction
   use dd_ttH_model, only: parse
   use dd_ttH_rambo, only: ramb

   implicit none
   integer, parameter :: NEVT = 1
   integer :: ievt, ierr, prec
   integer :: ii, jj, kk, ee
   real(ki), parameter :: pi = 3.141592653589793_ki
   real(ki) :: scale2, factor, nlo_cpl, rat, factor2, eftfac, vev
   real(ki), dimension(5,4) :: vecs
   real(ki), dimension(0:7,0:3) :: amp, ref_amp
   real(ki), dimension(0:3) :: tmp_amp
   real(ki), dimension(0:7,2:3) :: irp, ref_irp
   real(ki), dimension(2:3) :: tmp_irp
   integer, dimension(0:7) :: eftc

   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   
   call initgolem()

   ! call random_seed

   nlo_prefactors=0  ! Do not include any NLO prefactors in order to recognize
                     ! rational numbers for the pole coefficients

   do ievt = 1, NEVT
      ! call ramb(5.0E+02_ki**2, vecs)
      ! call boost_to_cms(vecs)
      ! call generate_reference_vecs(ievt, vecs)
      ! cycle

      call get_reference(ievt,vecs,ref_amp,ref_irp)

      scale2 = (100._ki)**2

      eftc = (/1,2,11,12,3,4,13,14/)

      do ee = 0, 7 
         EFTcount = eftc(ee)
         call samplitude(vecs, scale2, tmp_amp, prec)
         amp(ee,:) = tmp_amp(:)
         call ir_subtraction(vecs, scale2, tmp_irp(:))
         irp(ee,:) = tmp_irp(:)
         !print *, amp(ee,:)
         !print *, ref_amp(ee,:)
         !print *, irp(ee,:)
         !print *, ref_irp(ee,:)
      end do
      
      call check_reference(amp, irp, ref_amp, ref_irp)
      
      ! call generate_reference_output(ievt, amp, irp)
      
   end do

   call exitgolem()

 contains


   INCLUDE 'reference_psp.f90'
   INCLUDE 'reference_vals.f90' 


   subroutine get_reference(ievt,vecs,ref_amp,ref_irp)
     implicit none
     integer, intent(in) :: ievt
     real(ki), dimension(5,4), intent(out) :: vecs
     real(ki), dimension(0:7,0:3), intent(out) :: ref_amp
     real(ki), dimension(0:7,2:3), intent(out) :: ref_irp
     
     call get_reference_psp(ievt,vecs)
     call get_referenve_value(ievt,ref_amp,ref_irp)
    
   end subroutine get_reference


   subroutine check_reference(amp, irp, ref_amp, ref_irp)
     implicit none
     integer, parameter :: logf = 27
     integer, dimension(2,4) ::eftc, eftc2
     integer :: ee, ee2, ii, jj, kk
     real(ki), dimension(0:7,0:3), intent(in) :: amp, ref_amp
     real(ki), dimension(0:7,2:3), intent(in) :: irp, ref_irp
     real(ki), parameter :: eps = 1e-7_ki
     real(ki) :: diff
     logical :: success, isuccess
     character(33), dimension(0:7) :: truncations
     
     ! NOTE: numbering of EFTcount options has changed since rev 3518ed0! 
     eftc(1,:) = (/0,1,4,5/)
     eftc(2,:) = (/2,3,6,7/)
     eftc2(1,:) = (/1,2,3,4/)
     eftc2(2,:) = (/11,12,13,14/)

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

      if (any(isnan(amp))) then
         write(logf,*) "NaN error!"
         success = .false.
      end if
     
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
           ee2 = eftc2(ii,jj)
           write(6,'(A18,I2,A2,A33,A1)') "Truncation option ", ee2, " (", truncations(ee), ")"
           write(logf,'(A18,I2,A2,A33,A1)') "Truncation option ", ee2, " (", truncations(ee), ")"
           do kk = 0, 3
             diff = 0._ki
             diff = abs(rel_diff(amp(ee,kk),ref_amp(ee,kk)))
             if(diff.gt.eps) then
                write(6,'(A57,I2,A8,I2,A13,E13.7)') &
                     & "Result 'amp' differs from reference for truncation option", &
                     & ee2, ", entry ", kk, ". rel_diff = ", diff
                write(logf,'(A57,I2,A8,I2,A13,E13.7)') &
                     & "Result 'amp' differs from reference for truncation option", &
                     & ee2, ", entry ", kk, ". rel_diff = ", diff
                success = .false.
                isuccess = .false.
             end if
          end do
          do kk = 2, 3
             diff = 0._ki
             diff = abs(rel_diff(irp(ee,kk),ref_irp(ee,kk)))
             if(diff.gt.eps) then
                write(6,'(A57,I2,A8,I2,A13,E13.7)') &
                     & "Result 'irp' differs from reference for truncation option", &
                     & ee2, ", entry ", kk, ". rel_diff = ", diff
                write(logf,'(A57,I2,A8,I2,A13,E13.7)') &
                     & "Result 'irp' differs from reference for truncation option", &
                     & ee2, ", entry ", kk, ". rel_diff = ", diff
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
   

   subroutine generate_reference_vecs(ievt, vecs)
     implicit none
     real(ki), dimension(:,:), intent(in) :: vecs
     integer, intent(in) :: ievt
     integer :: i
     
     print '(A9,I3,A1)', "    case(", ievt,")"
     do i = 1, size(vecs,dim=1)
        print '(A12,I1,A9,F0.8,A5,F0.8,A5,F0.8,A,F0.8,A6)', &
             & "       vecs(", i, ",:) = (/ ", vecs(i,1), "_ki, ",vecs(i,2), "_ki, ",vecs(i,3), "_ki, ",vecs(i,4), "_ki /)" 
     end do
     
   end subroutine generate_reference_vecs


   subroutine generate_reference_output(ievt, amp, irp)
     implicit none
     integer, intent(in) :: ievt
     real(ki), dimension(0:7,0:3), intent(in) :: amp
     real(ki), dimension(0:7,2:3), intent(in) :: irp
     integer :: ee
     
     print '(A9,I3,A1)', "    case(", ievt,")"
     do ee = 0, 7
        ! NOTE: E0.d specifier requires gfortran version >= 10
        print '(A15,I1,A9,E19.13,A5,E19.13,A5,E19.13,A,E19.13,A6)', &
             & "       ref_amp(", ee, ",:) = (/ ", &
             & amp(ee,0), "_ki, ",amp(ee,1), "_ki, ",amp(ee,2), "_ki, ",amp(ee,3), "_ki /)"
        ! NOTE: E0.d specifier requires gfortran version >= 10
        print '(A15,I1,A9,E19.13,A,E19.13,A6)', &
             & "       ref_irp(", ee, ",:) = (/ ", &
             & amp(ee,2), "_ki, ",amp(ee,3), "_ki /)" 
     end do
    
   end subroutine generate_reference_output

  
end program test
