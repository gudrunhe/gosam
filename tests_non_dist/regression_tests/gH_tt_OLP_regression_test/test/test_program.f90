program main
  use olp_module
  use :: iso_c_binding
  
  implicit none
  integer, parameter :: ki = kind(1.0d0)
  integer, parameter :: NEVT = 1
  integer :: ievt, ierr, ipass
  real(ki), dimension(4,4) :: vecs
  real(ki), dimension(50) :: momenta
  real(ki) :: amp, acc, mu
  real(ki), dimension(60) :: blha_res
  real(ki), dimension(6) :: ref_res
  real(ki), dimension(2):: irp
  
  call OLP_Start(c_char_"../gH_tt.olc"//c_null_char,ipass)
  if(ipass.ne.1) call OLP_error("OLP_Start failed!")
  
  call OLP_SetParameter(c_char_"alpha"//c_null_char, 1._ki/132._ki, 0._ki, ierr)
  if(ierr.eq.0) call OLP_error("Setting of OLP parameter(s) failed!")

  mu = 100._ki
  
  do ievt = 1, NEVT
     ! call rambo(500._ki**2,vecs)
     call get_reference(ievt,vecs,ref_res)
     call vecs_to_blha(vecs,momenta)
     call OLP_EvalSubProcess2(0, momenta, mu, blha_res, acc)
     call ir_poles(vecs, mu*mu, irp)
     call check_reference(ievt,blha_res,irp,ref_res)
     ! call generate_reference_vecs(ievt, vecs)
     ! call generate_reference_output(ievt,blha_res,irp)
  end do

contains 


  subroutine rambo(s,vecs)
    use p0_gh_ttbar_rambo, only: ramb

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
    real(ki), dimension(4) :: p4
    real(ki) :: m
    
    m = sqrt(abs(p4(1)**2-p4(2)**2-p4(3)**2-p4(4)**2))
    
  end function get_mass


  subroutine OLP_error(msg)
    implicit none
    character (*) , intent(in) :: msg
    print *, "OLP Error :", msg
    stop    
  end subroutine OLP_error



  subroutine ir_poles(vecs,scale2,irp)
    use p0_gh_ttbar_matrix, only: ir_subtraction

    implicit none
    real(ki), intent(in), dimension(:,:) :: vecs
    real(ki), intent(in) :: scale2
    real(ki), intent(out), dimension(2) :: irp

    irp = 0._ki
    call ir_subtraction(vecs, scale2, irp)
    
  end subroutine ir_poles
    

  INCLUDE 'reference_psp.f90'
  INCLUDE 'reference_vals.f90' 


  subroutine get_reference(ievt,vecs,ref_res)
    implicit none
    integer, intent(in) :: ievt
    real(ki), dimension(4,4), intent(out) :: vecs
    real(ki), dimension(6), intent(out) :: ref_res

    call get_reference_psp(ievt,vecs)
    call get_referenve_value(ievt,ref_res)
    
  end subroutine get_reference


  subroutine check_reference(ievt,blha_res, irp, ref_res)
    implicit none
    integer, intent(in) :: ievt
    integer, parameter :: logf = 27
    integer ::  iem, ii, jj, kk
    real(ki), dimension(60), intent(in) :: blha_res
    real(ki), dimension(2), intent(in) :: irp
    real(ki), dimension(6), intent(in) :: ref_res
    real(ki), dimension(6) :: tmpres
    real(ki), parameter :: eps = 1e-7_ki
    real(ki) :: diff
    logical :: success, isuccess
    logical, dimension(6) :: mismatch
    character(15) :: blha_amptype
  
    blha_amptype = "gH -> tt~: Loop"
    
    open(file="test.log", unit=logf)

    success = .true.

    write(6,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev b0db9e47)."
    write(logf,*) "Comparing against reference numbers produced with GoSam 3.0.0 (rev b0db9e47)."
    
    isuccess = .true.

    write(6,'(A24,I3,A6)') "##### Phase space point ", ievt, " #####"
    write(logf,'(A24,I3,A6)') "##### Phase space point ", ievt, " #####"
    
    write(6,'(A22,A15,A1)') "Checking OLP channel (", blha_amptype, ")"
    write(logf,'(A22,A15,A1)') "Checking OLP channel (", blha_amptype, ")"

    ! ordering is:
    ! 1: born
    ! 2: V finite
    ! 3: V single pole
    ! 4: ir_sub single pole
    ! 5: V double pole
    ! 6: ir_sub double pole 
    ! unused blha entries (5 to 60) are dropped!

    tmpres(1) = blha_res(4)
    tmpres(2) = blha_res(3)
    tmpres(3) = blha_res(2)
    tmpres(4) = irp(1)
    tmpres(5) = blha_res(1)
    tmpres(6) = irp(2)

    mismatch = .false.
    
    do ii = 1, 6
       diff = 0._ki
       diff = abs(rel_diff(tmpres(ii),ref_res(ii)))
       if(diff.gt.eps) then
          mismatch(ii) = .true.
          call print_deviation(6, ii, diff)
          call print_deviation(logf, ii, diff)
          success = .false.
          isuccess = .false.
       end if
    end do

    if(any(mismatch)) then
       write(6,'(A60)') "                       GoSam                      Reference"
       call print_comparison(6,"Born               :   ", tmpres(1), ref_res(1), mismatch(1))
       call print_comparison(6,"Finite virtual     :   ", tmpres(2), ref_res(2), mismatch(2))
       call print_comparison(6,"Single pole virtual:   ", tmpres(3), ref_res(3), mismatch(3))
       call print_comparison(6,"Single pole IR sub.:   ", tmpres(4), ref_res(4), mismatch(4))
       call print_comparison(6,"Double pole virtual:   ", tmpres(5), ref_res(5), mismatch(5))
       call print_comparison(6,"Double pole IR sub.:   ", tmpres(6), ref_res(6), mismatch(6))
       write(logf,'(A60)') "                       GoSam                      Reference"
       call print_comparison(logf,"Born               :   ", tmpres(1), ref_res(1), mismatch(1))
       call print_comparison(logf,"Finite virtual     :   ", tmpres(2), ref_res(2), mismatch(2))
       call print_comparison(logf,"Single pole virtual:   ", tmpres(3), ref_res(3), mismatch(3))
       call print_comparison(logf,"Single pole IR sub.:   ", tmpres(4), ref_res(4), mismatch(4))
       call print_comparison(logf,"Double pole virtual:   ", tmpres(5), ref_res(5), mismatch(5))
       call print_comparison(logf,"Double pole IR sub.:   ", tmpres(6), ref_res(6), mismatch(6))
    end if
       
    if(isuccess) then
       write(6,*) "OK"
       write(logf,*) "OK"
    else
       write(6,*) "--"
       write(logf,*) "--"
    end if

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
       rel_diff = (a-b) / b
    end if

  end  function rel_diff
 

  subroutine print_deviation(outc, kk, diff)
    implicit none
    integer, intent(in) :: outc, kk
    real(ki), intent(in) :: diff

    write(outc,'(A31,I1,A13,E13.7)') &
         & "BLHA out put differs for entry ", &
         & kk, ". rel_diff = ", diff
    
  end subroutine print_deviation

  subroutine print_comparison(outc, metype, gsres, refres, mismatch)
    implicit none
    integer, intent(in) :: outc
    real(ki), intent(in) :: gsres, refres
    logical, intent(in) :: mismatch
    character(23), intent(in) :: metype

    if(mismatch) then
       write(outc,'(A23,E20.13,A7,E20.13,A3)') metype, gsres, "  vs.  ", refres, "  X"
    else
       write(outc,'(A23,E20.13,A7,E20.13)') metype, gsres, "  vs.  ", refres
    end if
    
  end subroutine print_comparison
    
  
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


  subroutine generate_reference_output(ievt, res, res2)
    implicit none
    integer, intent(in) :: ievt
    integer ::  iem, ii, jj, kk
    real(ki), dimension(60), intent(in) :: res
    real(ki), dimension(2), intent(in) :: res2
    real(ki), dimension(62) :: tmpres
    
    ! ordering is:
    ! 1: born
    ! 2: V finite
    ! 3: V single pole
    ! 4: ir_sub single pole
    ! 5: V double pole
    ! 6: ir_sub double pole 
    ! unused blha entries (5 to 60) are dropped!

    tmpres(1) = res(4)
    tmpres(2) = res(3)
    tmpres(3) = res(2)
    tmpres(4) = res2(1)
    tmpres(5) = res(1)
    tmpres(6) = res2(2)
    
    print '(A9,I3,A1)', "    case(", ievt,")"
    do kk = 1, 6
       ! NOTE: E0.d specifier requires gfortran version >= 10
       print '(A15,I1,A4,E19.13,A3)', "       ref_res(", kk, ") = ", tmpres(kk), "_ki"
    end do
    
  end subroutine generate_reference_output  

  
end program main
