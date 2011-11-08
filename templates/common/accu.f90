module     [% process_name asprefix=\_ %]accu
   !
   ! Synopsis:    routines for floating-point accumulation
   !              of sums with small relative error
   ! Author:      Thomas Reiter <thomasr@nikhef.nl>
   ! Date:        28 Jul. 2010
   ! Language:    Fortran 95
   ! Description: Implementation of the algorithm presented in
   !              ``AN ALGORITHM FOR FLOATING-POINT ACCUMULATION OF SUMS
   !                WITH SMALL RELATIVE ERROR''
   !              Michael Malcolm, STAN-CS-70-163, June 1970
   !
   ! Example:
   !              arr = (/ 1.2345E+20_ki, 1.0_ki, -1.2345E+20_ki/)
   !              print*, sum(arr), sorted_sum(arr)
   !              ! output:
   !              !   0.0      1.0
   !
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none

   integer, parameter, private :: min_ex_ki = minexponent(1.0_ki)
   integer, parameter, private :: max_ex_ki = maxexponent(1.0_ki)

   type     accumulator_type
     real(ki), dimension(min_ex_ki:max_ex_ki) :: a = 0.0_ki
   end type accumulator_type

   interface sorted_sum
      module procedure sorted_sum_r
      module procedure sorted_sum_c
   end interface

contains
   pure subroutine add_accu(acc, t)
      implicit none
      type(accumulator_type), intent(inout) :: acc
      real(ki), intent(in) :: t

      real(ki) :: r, d
      integer :: e, i
      real(ki) :: radix_ki
      
      radix_ki = scale(1.0_ki, 1)

      r = fraction(t)
      e = exponent(t)
      i = e

      do while (r .ne. 0.0_ki .and. i .gt. min_ex_ki)
         r = scale(r, 1)
         i = i - 1
         ! The following two lines extract the first
         ! digit from the number. Hence, d plays the
         ! role of a_{ij} in the original publication.
         d = aint(r)
         r = r - d

         ! This is step 3 of the original algorithm:
         ! Add the digit to the according accummulator.
         acc%a(i) = acc%a(i) + d
      end do
   end  subroutine add_accu

   pure function reduce_accu(acc) result(f)
      ! This routine is step 4 of the original algorithm:
      ! Sum in decreasing order.
      implicit none
      type(accumulator_type), intent(in) :: acc
      real(ki) :: f

      integer :: e

      f = 0.0_ki

      do e = max_ex_ki, min_ex_ki, -1
         if (acc%a(e) .ne. 0.0_ki) f = f + scale(acc%a(e), e)
      end do
   end  function reduce_accu

   pure function sorted_sum_r(arr) result(f)
      implicit none
      real(ki), dimension(:), intent(in) :: arr
      real(ki) :: f
      
      type(accumulator_type) :: acc
      integer :: i

      acc%a(:) = 0.0_ki
      do i = lbound(arr,1), ubound(arr,1)
         call add_accu(acc, arr(i))
      end do

      f = reduce_accu(acc)
   end  function sorted_sum_r

   pure function sorted_sum_c(arr) result(f)
      implicit none
      complex(ki), dimension(:), intent(in) :: arr
      complex(ki) :: f
      
      type(accumulator_type) :: acc_r, acc_i
      integer :: i

      acc_r%a(:) = 0.0_ki
      acc_i%a(:) = 0.0_ki

      do i = lbound(arr,1), ubound(arr,1)
         call add_accu(acc_r, real(arr(i), ki))
         call add_accu(acc_i, aimag(arr(i)))
      end do

      f = cmplx(reduce_accu(acc_r), reduce_accu(acc_i), ki)
   end  function sorted_sum_c

   pure function sorted_dotproduct(a1, a2) result(f)
      implicit none
      real(ki), dimension(:), intent(in) :: a1, a2
      real(ki) :: f
      
      type(accumulator_type) :: acc
      integer :: i

      acc%a(:) = 0.0_ki

      do i = lbound(a1,1), ubound(a1,1)
         call add_accu(acc, a1(i)*a2(i))
      end do

      f = reduce_accu(acc)
   end  function sorted_dotproduct

   pure function sorted_matmul(a1, a2) result(f)
      implicit none
      real(ki), dimension(:,:), intent(in) :: a1
      real(ki), dimension(:,:), intent(in) :: a2
      real(ki), dimension(size(a1,1),size(a2,2)) :: f
      
      type(accumulator_type) :: acc
      integer :: i, j

      acc%a(:) = 0.0_ki

      do i = lbound(a1,1), ubound(a1,1)
         do j = lbound(a2,2), ubound(a2,2)
            f(i,j) = sorted_dotproduct(a1(i,:), a2(:,j))
         end do
      end do
   end  function sorted_matmul
end module [% process_name asprefix=\_ %]accu
