module     pb0_gghh_globalsl1
   use pb0_gghh_config, only: ki
   use pb0_gghh_color, only: numcs
   implicit none

   private

   
   ! amp0 is used to store the LO amplitude between the calls
   ! for one kinematics.
   complex(ki), dimension(numcs), public :: amp0
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
      use pb0_gghh_color, only: cmat => CC
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
      use pb0_gghh_color, only: cmat => CC
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
end module pb0_gghh_globalsl1
