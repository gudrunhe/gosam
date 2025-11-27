program main
  use olp_module
  use :: iso_c_binding
  
  implicit none
  integer, parameter :: ki = kind(1.0d0)
  integer, parameter :: NEVT = 10
  integer, parameter :: NCHAN = 10
  integer :: ievt, ierr, ipass, ichan
  integer, dimension(0:NCHAN-1) :: eval_chans
  real(ki), dimension(4,4) :: vecs
  real(ki), dimension(50) :: momenta
  real(ki) :: amp, acc, mu
  real(ki), dimension(0:NCHAN-1,4) :: blha_res, ref_res
  real(ki), dimension(60) :: tmp_blha_res
  logical :: failed, success
  integer, parameter :: logf = 27
    
  success = .true.

  open(file="test.log", unit=logf)
  write(logf,*) "pp_aj test program"
  close(unit=logf)
  
  ! channel arrangement in olp_module.f90, see also olc file
  eval_chans = (/0,1,6,7,2,3,8,9,4,5/)
  
  call OLP_Start(c_char_"../pp_aj.olc"//c_null_char,ipass)
  if(ipass.ne.1) call OLP_error("OLP_Start failed!")
  
  call OLP_SetParameter(c_char_"alpha"//c_null_char, 1._ki/132.34890452162441_ki, 0._ki, ierr)
  if(ierr.eq.0) call OLP_error("Setting of OLP parameter(s) failed!")
 
  mu = 100._ki
  
  do ievt = 1, 1!NEVT
     !call rambo(500._ki**2,vecs)
     call get_reference(ievt,vecs,ref_res)
     call vecs_to_blha(vecs,momenta)
     do ichan = 0, NCHAN-1
        call OLP_EvalSubProcess2(eval_chans(ichan), momenta, mu, tmp_blha_res, acc)
        blha_res(ichan,:) = tmp_blha_res(1:4)
        if (any(isnan(blha_res))) then
           open(file="test.log", unit=logf, status="old", position="append", action="write")
           write(logf,*) "NaN error!"
           write(6,*) "NaN error!"
           close(unit=logf)
           success = .false.
        end if
        call check_results(ichan,blha_res(ichan,:),ref_res(ichan,:),failed,.false.,logf)
        if (failed) then
           success = .false.
        end if
     end do
     ! call generate_reference_vecs(ievt, vecs)
  end do

  open(file="test.log", unit=logf, status="old", position="append", action="write")
  if (success) then
     write(logf,'(A15)') "@@@ SUCCESS @@@"
  else
     write(logf,'(A15)') "@@@ FAILURE @@@"
  end if
  close(unit=logf)
  
contains 


  subroutine rambo(s,vecs)
    use p0_ddbar_ag_rambo, only: ramb

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
    real(ki), dimension(4,4), intent(out) :: vecs
    real(ki), dimension(0:NCHAN-1,4), intent(out) :: ref_res

    call get_reference_psp(ievt,vecs)
    call get_referenve_value(ievt,ref_res)
    
  end subroutine get_reference


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

  
  subroutine check_results(ichan, res, ref, failed, output, logf)
    implicit none
    integer, intent(in) :: ichan, logf
    integer :: i, iout
    integer, dimension(2) :: out
    real(ki) :: diff
    real(ki), dimension(0:3) :: res, ref
    real(ki), parameter :: eps = 1e-7_ki
    character(19), dimension(0:NCHAN-1) :: blha_amptype
    logical, intent(out) :: failed
    logical, intent(in) :: output

    blha_amptype = (/ &
         & "dd~ -> Ag: Loop   ", &
         & "dg  -> Ad: Loop   ", &
         & "uu~ -> Ag: Loop   ", &
         & "ug  -> Au: Loop   ", &
         & "ss~ -> Ag: Loop   ", &
         & "sg  -> As: Loop   ", &
         & "cc~ -> Ag: Loop   ", &
         & "cg  -> Ac: Loop   ", &
         & "bb~ -> Ag: Loop   ", &
         & "bg  -> Ab: Loop   " &         
         & /)

    failed = .false.
    
    do i = 0, 3
       diff = 0._ki
       diff = rel_diff(res(i),ref(i))
       if (abs(diff).gt.eps) then
          failed = .true.
       end if
    end do

    out = (/6, logf/)
    
    if (failed.or.output) then
       open(file="test.log", unit=logf, status="old", position="append", action="write")
       do iout = 1, 2
          write(out(iout),*) "-------------------------------"
          if (failed) then
             write(out(iout),*) "FAILED: ", blha_amptype(ichan)
          else
             write(out(iout),*) blha_amptype(ichan)
          end if
          write(out(iout),*) "              tree                     ", &
               &   " double pole              ", &
               &   " single pole              ", &
               &   " finite"
          write(out(iout),*) "GoSam:     ", res(0:3)
          write(out(iout),*) "OpenLoops: ", ref(0:3)
          write(out(iout),*) "Ratio:     ", res(0:3)/ref(0:3)
       end do
       close(unit=logf)           
    end if
    
  end subroutine check_results


  subroutine generate_reference_vecs(ievt, vecs)
    implicit none
    real(ki), dimension(:,:), intent(in) :: vecs
    integer, intent(in) :: ievt
    integer :: i

    print '(A9,I3,A1)', "    case(", ievt,")"
    do i = 1, size(vecs,dim=1)
       print '(A12,I1,A9,F0.16,A5,F0.16,A5,F0.16,A,F0.16,A6)', &
            & "       vecs(", i, ",:) = (/ ", vecs(i,1), "_ki, ",vecs(i,2), "_ki, ",vecs(i,3), "_ki, ",vecs(i,4), "_ki /)" 
    end do
  end subroutine generate_reference_vecs
  
end program main
