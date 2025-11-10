program main
  use olp_module
  use :: iso_c_binding
  
  implicit none
  integer, parameter :: ki = kind(1.0d0)
  integer, parameter :: NEVT = 1
  integer, parameter :: NCHAN = 8
  integer :: ievt, ierr, ipass, ichan
  integer, dimension(0:NCHAN-1) :: eval_chans
  real(ki), dimension(5,4) :: vecs
  real(ki), dimension(50) :: momenta
  real(ki) :: amp, acc, mu
  real(ki), dimension(0:NCHAN-1,60) :: blha_res, ref_res
  real(ki), dimension(60) :: tmp_blha_res

  eval_chans = (/0,6,1,2,3,7,4,5/)
  
  call OLP_Start(c_char_"../pp_AAj.olc"//c_null_char,ipass)
  if(ipass.ne.1) call OLP_error("OLP_Start failed!")
  
  call OLP_SetParameter(c_char_"alpha"//c_null_char, 1._ki/132._ki, 0._ki, ierr)
  if(ierr.eq.0) call OLP_error("Setting of OLP parameter(s) failed!")

  mu = 100._ki
  
  do ievt = 1, NEVT
     !call rambo(500._ki**2,vecs)
     call get_reference(ievt,vecs,ref_res)
     call vecs_to_blha(vecs,momenta)
     do ichan = 0, NCHAN-1
        call OLP_EvalSubProcess2(eval_chans(ichan), momenta, mu, tmp_blha_res, acc)
        blha_res(ichan,:) = tmp_blha_res(:)
        !call print_blha_result(ichan,blha_res(ichan,:))
     end do
     call check_reference(blha_res,ref_res)
     ! call generate_reference_vecs(ievt, vecs)
     ! call generate_reference_output(ievt,blha_res)
  end do

contains 


  subroutine rambo(s,vecs)
    use p0_ddbar_aag_rambo, only: ramb

    implicit none
    real(ki), intent(in) :: s
    real(ki), intent(inout), dimension(:,:) :: vecs 
 
    call ramb(s,vecs)
    
  end subroutine rambo

  
  subroutine vecs_to_blha(vecs,momenta)
    implicit none
    real(ki), dimension(:,:), intent(in) :: vecs
    real(ki), dimension(50), intent(out) :: momenta
    integer :: i, k
    
    momenta = 0._ki

    do i = 1, size(vecs,dim=1)
       k = 5*i-4
       momenta(k:k+3) = vecs(i,:)
       momenta(k+4) = get_mass(vecs(i,:))
    end do
    
  end subroutine vecs_to_blha


  function get_mass(p4) result(m)
    implicit none
    real(ki), dimension(:) :: p4
    real(ki) :: m

    if( size(p4).ne.4 ) then
       print *, "get_mass: four momentum is not four dimensional! ", size(p4)
       stop
    endif
    
    m = sqrt(abs(p4(1)**2-p4(2)**2-p4(3)**2-p4(4)**2))
    
  end function get_mass


  subroutine OLP_error(msg)
    implicit none
    character (*) , intent(in) :: msg
    print *, "OLP Error :", msg
    stop    
  end subroutine OLP_error


  INCLUDE 'reference_psp.f90'
  INCLUDE 'reference_vals.f90' 


  subroutine get_reference(ievt,vecs,ref_res)
    implicit none
    integer, intent(in) :: ievt
    real(ki), dimension(5,4), intent(out) :: vecs
    real(ki), dimension(0:NCHAN-1,60), intent(out) :: ref_res

    call get_reference_psp(ievt,vecs)
    call get_referenve_value(ievt,ref_res)
    
  end subroutine get_reference


  subroutine check_reference(blha_res, ref_res)
    implicit none
    integer, parameter :: logf = 27
    integer ::  ichan, iem, ii, jj, kk
    real(ki), dimension(0:NCHAN-1,60), intent(in) :: blha_res, ref_res
    real(ki), parameter :: eps = 1e-7_ki
    real(ki) :: diff
    logical :: success, isuccess
    character(19), dimension(0:NCHAN-1) :: blha_amptype
  
    blha_amptype = (/ &
         & "dd~ -> AAg: Tree   ", &
         & "dd~ -> AAg: Loop   ", &
         & "dd~ -> AAg: ccTree ", &
         & "dd~ -> AAg: scTree2", &
         & "dg -> AAd: Tree    ", &
         & "dg -> AAd: Loop    ", &
         & "dg -> AAd: ccTree  ", &
         & "dg -> AAd: scTree2 " &
         & /)
    
    open(file="test.log", unit=logf)

    success = .true.

    if (any(isnan(blha_res))) then
       write(logf,*) "NaN error!"
       success = .false.
    end if
    
    write(6,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev 3518ed0)."
    write(logf,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev 3518ed0)."
    
    do ichan = 0, 7

       isuccess = .true.
       
       write(6,'(A21,I1,A2,A19,A1)') "Checking OLP channel ", ichan, " (", blha_amptype(ichan), ")"
       write(logf,'(A21,I1,A2,A19,A1)') "Checking OLP channel ", ichan, " (", blha_amptype(ichan), ")"
       
       select case(ichan)
       case(0,4) ! amptype tree
          diff = 0._ki
          diff = abs(rel_diff(blha_res(ichan,4),ref_res(ichan,4)))
          if(diff.gt.eps) then
             call print_deviation(6,ichan, 4, diff)
             call print_deviation(logf,ichan, 4, diff)
             success = .false.
             isuccess = .false.
          end if
          if(isuccess) then
             write(6,*) "OK"
             write(logf,*) "OK"
          else
             write(6,*) "--"
             write(logf,*) "--"
          end if
       case(1,5) ! amptype loop
          do ii = 1, 4
             diff = 0._ki
             diff = abs(rel_diff(blha_res(ichan,ii),ref_res(ichan,ii)))
             if(diff.gt.eps) then
                call print_deviation(6,ichan, ii, diff)
                call print_deviation(logf,ichan, 4, diff)
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
       case(2,6) ! amptype cctree
          do ii = 1, 5
             do jj = ii+1, 5
                diff = 0._ki
                kk = ii-1+(jj-1)*(jj-2)/2+1
                diff = abs(rel_diff(blha_res(ichan,kk),ref_res(ichan,kk)))
                if(diff.gt.eps) then
                   call print_deviation(6,ichan, kk, diff)
                   call print_deviation(logf,ichan, 4, diff)
                   success = .false.
                   isuccess = .false.
                end if
             end do
          end do
          if(isuccess) then
             write(6,*) "OK"
             write(logf,*) "OK"
          else
             write(6,*) "--"
             write(logf,*) "--"
          end if
       case(3,7) ! amptype sctree2
          do iem = 1, 5
             do ii=1,6
                diff = 0._ki
                kk = 6*(iem-1)+ii
                diff = abs(rel_diff(blha_res(ichan,kk),ref_res(ichan,kk)))
                if(diff.gt.eps) then
                   call print_deviation(6,ichan, kk, diff)
                   call print_deviation(logf,ichan, 4, diff)
                   success = .false.
                   isuccess = .false.
                end if
             end do
          end do
          if(isuccess) then
             write(6,*) "OK"
             write(logf,*) "OK"
          else
             write(6,*) "--"
             write(logf,*) "--"
          end if
       case default
          print *, "Unknown channel number: ", ichan
          stop
       end select
       
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
 

  subroutine print_deviation(outc,ichan, kk, diff)
    implicit none
    integer, intent(in) :: outc,ichan, kk
    real(ki), intent(in) :: diff
    
    write(outc,'(A33,I1,A8,I2,A13,E13.7)') &
         & "BLHA out put differs for channel ", &
         & ichan, ", entry ", kk, ". rel_diff = ", diff
    
  end subroutine print_deviation

  
  subroutine print_blha_result(ichan, res)
    implicit none
    integer, intent(in) :: ichan
    integer :: iem, ii, jj
    real(ki), dimension(60) :: res
    real(ki), dimension(5,4,4) :: bmunu
    real(ki), dimension(5,5) :: cij
    character(19), dimension(0:NCHAN-1) :: blha_amptype
  
    blha_amptype = (/ &
         & "dd~ -> AAg: Tree   ", &
         & "dd~ -> AAg: Loop   ", &
         & "dd~ -> AAg: ccTree ", &
         & "dd~ -> AAg: scTree2", &
         & "dg -> AAd: Tree    ", &
         & "dg -> AAd: Loop    ", &
         & "dg -> AAd: ccTree  ", &
         & "dg -> AAd: scTree2 " &
         & /)

    print *, "-------------------------------"
    print *, blha_amptype(ichan)
    print *, "-------------------------------"
    
    select case(ichan)
    case(0,4) ! amptype tree
       print *, res(4)
    case(1,5) ! amptype loop
       print *, res(1:4)
    case(2,6) ! amptype cctree
       cij = 0._ki
       do ii = 1, 5
          do jj = ii+1, 5
             cij(ii,jj) = res(ii-1+(jj-1)*(jj-2)/2+1)
             cij(jj,ii) = cij(ii,jj)
          end do
          print *, cij(ii,:)
       end do
    case(3,7) ! amptype sctree2
       bmunu = 0._ki
       do iem = 1, 5
          ! Whizard convention
          bmunu(iem,2,2) = res(6*(iem-1)+1)
          bmunu(iem,3,3) = res(6*(iem-1)+3)
          bmunu(iem,4,4) = res(6*(iem-1)+6)
          if (iem.le.2) then
             bmunu(iem,2,3) = -res(6*(iem-1)+2)
             bmunu(iem,2,4) = -res(6*(iem-1)+4)
             bmunu(iem,3,4) = -res(6*(iem-1)+5)
          else
             bmunu(iem,2,3) = res(6*(iem-1)+2)
             bmunu(iem,2,4) = res(6*(iem-1)+4)
             bmunu(iem,3,4) = res(6*(iem-1)+5)
          end if
          bmunu(iem,3,2) = bmunu(iem,2,3)
          bmunu(iem,4,2) = bmunu(iem,2,4)
          bmunu(iem,4,3) = bmunu(iem,3,4)
          print *, "emitter ", iem
          do ii = 1, 4
             print *, bmunu(iem,ii,:)
          end do
       end do
    case default
       print *, "Unknown channel number: ", ichan
       stop
    end select

    print *, ""
    
  end subroutine print_blha_result


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

  

  subroutine generate_reference_output(ievt, res)
    implicit none
    integer, intent(in) :: ievt
    integer ::  ichan, iem, ii, jj, kk
    real(ki), dimension(0:NCHAN-1,60), intent(in) :: res
    real(ki), dimension(60) :: tmpres

    print '(A9,I3,A1)', "    case(", ievt,")"
    
    do ichan = 0, 7
    
       tmpres = 0._ki

       select case(ichan)
       case(0,4) ! amptype tree
          tmpres(4) = res(ichan,4)
       case(1,5) ! amptype loop
          tmpres(1:4) = res(ichan,1:4)
       case(2,6) ! amptype cctree
          do ii = 1, 5
             do jj = ii+1, 5
                tmpres(ii-1+(jj-1)*(jj-2)/2+1) = res(ichan,ii-1+(jj-1)*(jj-2)/2+1)
             end do
          end do
       case(3,7) ! amptype sctree2
          tmpres = 0._ki
          do iem = 1, 5
             do ii=1,6
                tmpres(6*(iem-1)+ii) = res(ichan,6*(iem-1)+ii)
             end do
          end do
       case default
          print *, "Unknown channel number: ", ichan
          stop
       end select

       do kk = 1, 60
          ! NOTE: E0.d specifier requires gfortran version >= 10
          print '(A15,I1,A2,I2,A4,E19.13,A3)', "       ref_res(", ichan, ", ", kk, ") = ", tmpres(kk), "_ki"
       end do
       
    end do
    
  end subroutine generate_reference_output  

  
end program main
