[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]util_qp
   use [% process_name asprefix=\_ %]color_qp, only: numcs
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
   implicit none
   private

   interface     square
      module procedure square_0l_0l
      module procedure square_0l_1l
      module procedure square_0l_0l_mat
   end interface square

   interface     cond
      module procedure cond_q_mu2
      module procedure cond_mu2
   end interface

[% @if extension ninja %]
   interface     cond_t
      module procedure cond_mu_r1
      module procedure cond_mu_r2
      module procedure cond_abc_p2
      module procedure cond_abc_p3
   end interface
[% @end @if %]

   public :: square
   public :: inspect_lo_diagram
   public :: metric_tensor
   public :: cond[%
@if extension ninja %]
   public :: cond_t[%
@end @if %]
contains
   pure function metric_tensor(mu,nu) result(d)
      implicit none
      integer, intent(in) :: mu, nu
      real(ki) :: d
      if (mu.ne.nu) then
         d = 0.0_ki
      elseif (mu.eq.1) then
         d = 1.0_ki
      else
         d = -1.0_ki
      end if
   end  function metric_tensor

   function cond_q_mu2(cnd, brack, Q, mu2) result(cond)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: Q
      complex(ki), intent(in) :: mu2

      complex(ki) :: cond

      interface
         function brack(inner_Q, inner_mu2)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), dimension(4), intent(in) :: inner_Q
            complex(ki), intent(in) :: inner_mu2
            complex(ki) :: brack
         end  function brack
      end interface

      if (cnd) then
         cond = brack(Q, mu2)
      else
         cond = (0.0_ki, 0.0_ki)
      end if
   end  function cond_q_mu2

   function cond_mu2(cnd, brack, mu2) result(cond)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), intent(in) :: mu2

      complex(ki) :: cond

      interface
         function brack(inner_mu2)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), intent(in) :: inner_mu2
            complex(ki) :: brack
         end  function brack
      end interface

      if (cnd) then
         cond = brack(mu2)
      else
         cond = (0.0_ki, 0.0_ki)
      end if
   end  function cond_mu2

[% @if extension ninja %]
   subroutine cond_mu_r1(cnd, brack, a, coeffs)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: a
      complex(ki), dimension(0:*), intent(inout) :: coeffs

      interface
         subroutine brack(inner_a, inner_co)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), dimension(4), intent(in) :: inner_a
            complex(ki), dimension(0:*), intent(inout) :: inner_co
         end  subroutine brack
      end interface

      if (cnd) then
         call brack(a, coeffs)
      end if
   end  subroutine cond_mu_r1

   subroutine cond_mu_r2(cnd, brack, a, b, coeffs)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: a, b
      complex(ki), dimension(0:*), intent(inout) :: coeffs

      interface
         subroutine brack(inner_a, inner_b, inner_co)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), dimension(4), intent(in) :: inner_a
            complex(ki), dimension(4), intent(in) :: inner_b
            complex(ki), dimension(0:*), intent(inout) :: inner_co
         end  subroutine brack
      end interface

      if (cnd) then
         call brack(a, b, coeffs)
      end if
   end  subroutine cond_mu_r2

   subroutine cond_abc_p3(cnd, brack, a, b, c, param, coeffs)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: a, b, c
      complex(ki), intent(in) :: param
      complex(ki), dimension(0:*), intent(inout) :: coeffs

      interface
         subroutine brack(inner_a, inner_b, inner_c, inner_param, inner_co)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), dimension(4), intent(in) :: inner_a
            complex(ki), dimension(4), intent(in) :: inner_b
            complex(ki), dimension(4), intent(in) :: inner_c
            complex(ki), intent(in) :: inner_param
            complex(ki), dimension(0:*), intent(inout) :: inner_co
         end  subroutine brack
      end interface

      if (cnd) then
         call brack(a, b, c, param, coeffs)
      end if
   end  subroutine cond_abc_p3

   subroutine    cond_abc_p2(cnd, brack, a0, a1, b, c, param, coeffs)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: a0, a1, b, c
      complex(ki), dimension(0:2), intent(in) :: param
      complex(ki), dimension(0:*), intent(inout) :: coeffs

      interface
         subroutine brack(inner_a0, inner_a1, inner_b, inner_c, inner_param,&
           & inner_co)
            use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
            implicit none
            complex(ki), dimension(4), intent(in) :: inner_a0
            complex(ki), dimension(4), intent(in) :: inner_a1
            complex(ki), dimension(4), intent(in) :: inner_b
            complex(ki), dimension(4), intent(in) :: inner_c
            complex(ki), dimension(0:2), intent(in) :: inner_param
            complex(ki), dimension(0:*), intent(inout) :: inner_co
         end  subroutine brack
      end interface

      if (cnd) then
         call brack(a0, a1, b, c, param, coeffs)
      end if
   end  subroutine cond_abc_p2
[% @end @if %]

   subroutine     inspect_lo_diagram(values, d, h, unit)
      implicit none

      complex(ki), dimension(numcs), intent(in) :: values
      integer, intent(in) :: d, h
      integer, intent(in), optional :: unit

      integer :: ch, i

      if(present(unit)) then
              ch = unit
      else
              ch = 5
      end if

      write(ch,'(A19,I3,A2)') "<lo-diagram index='", d, "'>"
      do i=1,numcs
         write(ch,'(A21,I3,A6,G23.16,A6,G23.16,A3)') &
            & "<result color-index='", i-1, "' re='", real(values(i)), &
            & "' im='", aimag(values(i)), "'/>"
      end do
      write(ch,'(A13)') "</lo-diagram>"
   end subroutine inspect_lo_diagram

!   subroutine     inspect_nlo_diagram(values, d, h, [%
      @if generate_tree_diagrams %][% @else %]c, [% @end @if %]unit)
!      implicit none
!
!      complex(ki), dimension(0:2), intent(in) :: values
!      integer, intent(in) :: d, h[%
      @if generate_tree_diagrams %][% @else %], c[% @end @if %]
!      integer, intent(in), optional :: unit
!
!      integer :: ch
!
!      if(present(unit)) then
!              ch = unit
!      else
!              ch = 5
!      end if
!
!      write(ch,'(A12,I6,A1,I3,[%
      @if generate_tree_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_tree_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",2,complex(", real(values(2)), ",", aimag(values(2)), "))"
!      write(ch,'(A12,I6,A1,I3,[%
      @if generate_tree_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_tree_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",1,complex(", real(values(1)), ",", aimag(values(1)), "))"
!      write(ch,'(A12,I6,A1,I3,[%
      @if generate_tree_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_tree_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",0,complex(", real(values(0)), ",", aimag(values(0)), "))"
!   end subroutine inspect_nlo_diagram

   !---#[ function square :
   pure function square_0l_0l(color_vector) result(amp)
      use [% process_name asprefix=\_ %]color_qp, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      real(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector)
      v2 = conjg(color_vector)
      amp = real(sum(v1(:) * v2(:)), ki)
   end function  square_0l_0l
   pure function square_0l_1l(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color_qp, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1
      complex(ki), dimension(numcs), intent(in) :: color_vector2
      real(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector1)
      v2 = conjg(color_vector2)
      amp = 2.0_ki * real(sum(v1(:) * v2(:)), ki)
   end function  square_0l_1l

   pure function square_0l_0l_mat(color_vector, cmat) result(amp)
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      complex(ki), dimension(numcs,numcs), intent(in) :: cmat
      real(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector)
      v2 = conjg(color_vector)
      amp = real(sum(v1(:) * v2(:)), ki)
   end function  square_0l_0l_mat
   !---#] function square :
end module [% process_name asprefix=\_ %]util_qp
