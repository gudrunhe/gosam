program main
  use openloops
  
  implicit none
  integer, parameter :: ki = kind(1.0d0)
  integer :: NEVT = 10
  integer :: ievt, ichan
  integer, dimension(0:9) :: id
  real(ki) :: acc, test
  real(ki), dimension(0:9,0:3) :: res
  real(ki), dimension(4,4) :: vecs, psp
  real(ki), parameter :: pi = 3.141592653589793_ki

  
  call set_parameter("verbose", 0)
  
  call set_parameter("order_ew", 1)
  call set_parameter("alpha_s", 1d0/4d0/pi)
  id(0) = register_process("  1 -1  ->  22  21", 11)
  id(1) = register_process("  1  21 ->  22   1", 11)
  id(2) = register_process("  2  -2 ->  22  21", 11)
  id(3) = register_process("  2  21 ->  22   2", 11)
  id(4) = register_process("  3  -3 ->  22  21", 11)
  id(5) = register_process("  3  21 ->  22   3", 11)
  id(6) = register_process("  4  -4 ->  22  21", 11)
  id(7) = register_process("  4  21 ->  22   4", 11)
  id(8) = register_process("  5  -5 ->  22  21", 11)
  id(9) = register_process("  5  21 ->  22   5", 11) 
  call start()

  do ievt = 1, NEVT
     call set_parameter("mu", 100._ki)
     call get_reference_psp(ievt,vecs)
     call vecs_to_psp(vecs,psp)
     do ichan = 0, 9
        ! res(3) -> tree
        ! res(0:2) -> finite, single, double
        call evaluate_loop(id(ichan), psp, res(ichan,3), res(ichan,0:2), acc)
     end do
     call generate_reference_output(ievt, res)
  end do
     
  call finish()
  
contains

  INCLUDE '../reference_psp.f90'
  
  subroutine vecs_to_psp(vecs,psp)
    implicit none
    real(8), dimension(4, 4), intent(in) :: vecs
    real(8), dimension(4, 4), intent(out) :: psp
    integer :: i, j

    do i=1,4
       do j=1,4
          psp(j,i) = vecs(i,j)
       end do
    end do
    
  end subroutine vecs_to_psp

  subroutine generate_reference_output(ievt, res)
    implicit none
    integer, intent(in) :: ievt
    integer ::  ichan
    real(ki), dimension(0:9,0:3), intent(in) :: res

    print '(A9,I3,A1)', "    case(", ievt,")"
    print '(A36,A25,A20,A23)', "! double pole", "single pole", "finite", "tree"
    do ichan = 0, 9
       ! NOTE: E0.d specifier requires gfortran version >= 10
       print '(A15,I1,A9,4(E19.13,A6))', &
            & "       ref_res(", ichan, ",:) = (/ ", &
            & res(ichan,2), "_ki,  ", &
            & res(ichan,1), "_ki,  ", &
            & res(ichan,0), "_ki,  ", &
            & res(ichan,3), "_ki /)"       
    end do
    
  end subroutine generate_reference_output  

  
end program main
