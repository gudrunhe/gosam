module     [% process_name asprefix=\_ %]globalsl1
   use [% process_name asprefix=\_ %]config, only: ki
   use [% process_name asprefix=\_ %]color, only: numcs
   implicit none

   private

   [% @if generate_lo_diagrams %]
   ! amp0 is used to store the LO amplitude between the calls
   ! for one kinematics.
   complex(ki), dimension(numcs[%@if helsum%],0:max(0[%@for helicities generated%],&
                                     &[%helicity%][%@end @for%])[%@end @if%]), public :: amp0[%
   @else %]
   ! col0 is the color index to be returned in the virtual diagrams
   integer, public :: col0[%
   @end @if %]
   integer, dimension(numcs), public :: perm
   logical, public :: use_perm

   integer, public :: epspow

   interface ccontract
      module procedure ccontract_cc
      module procedure ccontract_rc
   end interface

   public :: ccontract

contains
   !---#[ function ccontract_cc:
   pure function ccontract_cc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1
      complex(ki), dimension(numcs), intent(in) :: color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      if (use_perm) then
         v1 = matmul(cmat, color_vector1(perm))
      else
         v1 = matmul(cmat, color_vector1)
      end if
      v2 = conjg(color_vector2)
      amp = sum(v1(:) * v2(:))
   end function  ccontract_cc
   !---#] function ccontract_cc:
   !---#[ function ccontract_rc:
   pure function ccontract_rc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
      implicit none
      real(ki), dimension(numcs), intent(in) :: color_vector1
      complex(ki), dimension(numcs), intent(in) :: color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      if (use_perm) then
         v1 = matmul(cmat, color_vector1(perm))
      else
         v1 = matmul(cmat, color_vector1)
      end if
      v2 = conjg(color_vector2)
      amp = sum(v1(:) * v2(:))
   end function  ccontract_rc
   !---#] function ccontract_rc:
end module [% process_name asprefix=\_ %]globalsl1
