program test
   use gH_ttg_config, only: ki, nlo_prefactors, EFTcount
   use gH_ttg_kinematics, only: boost_to_cms
   use gH_ttg_matrix, only: samplitudel0, &
        & initgolem, exitgolem, &
        & OLP_color_correlated, spin_correlated_lo2_whizard
   use gH_ttg_model, only: parse
   use gH_ttg_rambo, only: ramb

   implicit none
   integer, parameter :: NEVT = 1
   integer :: ievt, ierr, prec
   integer :: ii, jj, kk, ee
   real(ki), parameter :: pi = 3.141592653589793_ki
   real(ki) :: scale2
   real(ki), dimension(5,4) :: vecs
   real(ki), dimension(0:7) :: amp, ref_amp
   real(ki), dimension(0:7,10) :: ampcc, ref_ampcc
   real(ki), dimension(0:7,5,4,4) :: bmunu, ref_bmunu
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

      call get_reference(ievt,vecs,ref_amp,ref_ampcc,ref_bmunu)

      scale2 = (100._ki)**2

      eftc = (/1,2,11,12,3,4,13,14/)

      do ee = 0, 7 
         EFTcount = eftc(ee)
         amp(ee) = samplitudel0(vecs)
         call OLP_color_correlated(vecs,ampcc(ee,:))
         call spin_correlated_lo2_whizard(vecs,bmunu(ee,:,:,:))
         do ii = 1, 5
            do jj = 1, 4
               do kk = 1, 4
                  call tiny_to_zero(amp(ee),bmunu(ee,ii,jj,kk))
               end do
            end do
         end do
      end do

      call check_reference(amp, ampcc, bmunu, ref_amp, ref_ampcc, ref_bmunu)
      
      ! call generate_reference_output(ievt, amp, ampcc, bmunu)
      
   end do

   call exitgolem()

 contains


   INCLUDE 'reference_psp.f90'
   INCLUDE 'reference_vals.f90' 


   subroutine get_reference(ievt,vecs,ref_amp,ref_ampcc,ref_bmunu)
     implicit none
     integer, intent(in) :: ievt
     real(ki), dimension(5,4), intent(out) :: vecs
     real(ki), dimension(0:7), intent(out) :: ref_amp
     real(ki), dimension(0:7,10), intent(out) :: ref_ampcc
     real(ki), dimension(0:7,5,4,4), intent(out) :: ref_bmunu
     
     call get_reference_psp(ievt,vecs)
     call get_referenve_value(ievt,ref_amp,ref_ampcc,ref_bmunu)
    
   end subroutine get_reference


   subroutine check_reference(amp, ampcc, bmunu, ref_amp, ref_ampcc, ref_bmunu)
     implicit none
     integer, parameter :: logf = 27
     integer, dimension(2,4) ::eftc, eftc2
     integer :: ee, ee2, ii, jj, kk, iem, mu, nu
     real(ki), dimension(0:7), intent(in) :: amp, ref_amp
     real(ki), dimension(0:7,10), intent(in) :: ampcc, ref_ampcc
     real(ki), dimension(0:7,5,4,4), intent(in) :: bmunu, ref_bmunu
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
           diff = 0._ki
           diff = abs(rel_diff(amp(ee),ref_amp(ee)))
           if(diff.gt.eps) then
              write(6,'(A58,I2,A13,E13.7)') &
                   & "Result 'amp' differs from reference for truncation option ", &
                   & ee2, ". rel_diff = ", diff
              write(logf,'(A58,I2,A13,E13.7)') &
                   & "Result 'amp' differs from reference for truncation option ", &
                   & ee2, ". rel_diff = ", diff
              success = .false.
              isuccess = .false.
           end if
           do kk = 1, 10
              diff = 0._ki
              diff = abs(rel_diff(ampcc(ee,kk),ref_ampcc(ee,kk)))
              if(diff.gt.eps) then
                 write(6,'(A60,I2,A8,I2,A13,E13.7)') &
                      & "Result 'ampcc' differs from reference for truncation option ", &
                      & ee2, ", entry ", kk, ". rel_diff = ", diff
                 write(logf,'(A60,I2,A8,I2,A13,E13.7)') &
                      & "Result 'ampcc' differs from reference for truncation option ", &
                      & ee2, ", entry ", kk, ". rel_diff = ", diff
                 success = .false.
                 isuccess = .false.
              end if
           end do
           do iem = 1, 5
              do mu = 1, 4
                 do nu = 1, 4
                    diff = 0._ki
                    diff = abs(rel_diff(bmunu(ee,iem,mu,nu),ref_bmunu(ee,iem,mu,nu)))
                    if(diff.gt.eps) then
                       write(6,'(A60,I2,A10,I1,A9,I1,A1,I1,A14,E13.7)') &
                            & "Result 'bmunu' differs from reference for truncation option ", &
                            & ee2, ", emitter ", iem, ", entry (", mu, ",", nu, "). rel_diff = ", diff
                       write(logf,'(A60,I2,A10,I1,A9,I1,A1,I1,A14,E13.7)') &
                            & "Result 'bmunu' differs from reference for truncation option ", &
                            & ee2, ", emitter ", iem, ", entry (", mu, ",", nu, "). rel_diff = ", diff
                       success = .false.
                       isuccess = .false.
                    end if
                 end do
              end do
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


   subroutine tiny_to_zero(a,b)
     implicit none
     real(ki), intent(in) :: a
     real(ki), intent(inout) :: b
     real(ki), parameter :: tiny = 1.e-10_ki
     
     if (a.ne.0._ki) then
        if (abs(b/a).lt.tiny) then
           b = 0._ki
        end if
     end if
     
   end subroutine tiny_to_zero

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


   subroutine generate_reference_output(ievt, amp, ampcc, bmunu)
     implicit none
     integer, intent(in) :: ievt
     real(ki), dimension(0:7), intent(in) :: amp
     real(ki), dimension(0:7,10), intent(in) :: ampcc
     real(ki), dimension(0:7,5,4,4), intent(in) :: bmunu
     integer :: iem, ee, ii
     
     print '(A9,I3,A1)', "    case(", ievt,")"
     do ee = 0, 7
        ! NOTE: E0.d specifier requires gfortran version >= 10
        print '(A15,I1,A4,E19.13,A3)', &
             & "       ref_amp(", ee, ") =  ", amp(ee), "_ki"
        do ii = 1, 10
           ! NOTE: E0.d specifier requires gfortran version >= 10
           print '(A17,I1,A1,I2,A4,E19.13,A3)', &
                & "       ref_ampcc(", ee, ",", ii, ") =  ", ampcc(ee,ii), "_ki"
        end do
        do iem = 1, 5
           do ii = 1, 4
              ! NOTE: E0.d specifier requires gfortran version >= 10
              print '(A17,I1,A1,I1,A1,I1,A9,E19.13,A5,E19.13,A5,E19.13,A5,E19.13,A6)', &
                   & "       ref_bmunu(", ee, ",", iem, ",", ii, ",:) = (/ ", &
                   & bmunu(ee,iem,ii,1), "_ki, ", &
                   & bmunu(ee,iem,ii,2), "_ki, ", &
                   & bmunu(ee,iem,ii,3), "_ki, ", &
                   & bmunu(ee,iem,ii,4), "_ki /)" 
           end do
        end do
     end do
    
   end subroutine generate_reference_output

  
end program test
