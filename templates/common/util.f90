[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]util
   use [% process_name asprefix=\_ %]color, only: numcs
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none
   private

   interface     square
      module procedure square_0l_0l
      module procedure square_0l_1l
      module procedure square_0l_0l_mat
   end interface square

   public :: square
   public :: inspect_lo_diagram
   public :: cond[%
@if extension samurai %]
   public :: cmplx_sam, cmplx_ki[%
@end @if %]
contains
   pure function cond(cnd, brack, Q, mu2)
      implicit none
      logical, intent(in) :: cnd
      complex(ki), dimension(4), intent(in) :: Q
      complex(ki), intent(in) :: mu2

      complex(ki) :: cond

      interface
         pure function brack(inner_Q, inner_mu2)
            use [% process_name asprefix=\_ %]config, only: ki
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
   end  function cond

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
      @if generate_lo_diagrams %][% @else %]c, [% @end @if %]unit)
!      implicit none
!
!      complex(ki), dimension(0:2), intent(in) :: values
!      integer, intent(in) :: d, h[%
      @if generate_lo_diagrams %][% @else %], c[% @end @if %]
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
      @if generate_lo_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_lo_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",2,complex(", real(values(2)), ",", aimag(values(2)), "))"
!      write(ch,'(A12,I6,A1,I3,[%
      @if generate_lo_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_lo_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",1,complex(", real(values(1)), ",", aimag(values(1)), "))"
!      write(ch,'(A12,I6,A1,I3,[%
      @if generate_lo_diagrams %][% @else %]A1,I3,[% @end @if
      %]A11,G23.16,A1,G23.16,A2)') &
!         & "evt.set_nlo(", d, ",", h, [%
      @if generate_lo_diagrams %][% @else %]",", c, [% @end @if
      %]&
!         & ",0,complex(", real(values(0)), ",", aimag(values(0)), "))"
!   end subroutine inspect_nlo_diagram
[%
@if extension samurai %]
   !---#[ function cmplx_sam:
   pure elemental function cmplx_sam(z) result(res)
      use precision, only: ki_sam => ki
      implicit none
      complex(ki), intent(in) :: z
      complex(ki_sam) :: res

      res = cmplx(real(z, ki_sam), aimag(z), ki_sam)
   end function cmplx_sam
   !---#] function cmplx_sam:
   !---#[ function cmplx_ki:
   pure elemental function cmplx_ki(z) result(res)
      use precision, only: ki_sam => ki
      implicit none
      complex(ki_sam), intent(in) :: z
      complex(ki) :: res

      res = cmplx(real(z, ki), aimag(z), ki)
   end function cmplx_ki
   !---#] function cmplx_ki:[%
@end @if %]
   !---#[ function square :
   pure function square_0l_0l(color_vector) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      real(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector)
      v2 = conjg(color_vector)
      amp = real(sum(v1(:) * v2(:)), ki)
   end function  square_0l_0l
   pure function square_0l_1l(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
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
end module [% process_name asprefix=\_ %]util
