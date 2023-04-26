module     pb1_gghh_groups
   use pb1_gghh_config, only: ki 
   implicit none
   save

   private
   public :: ninja_exit
contains
!---#[ subroutine ninja_exit:
subroutine ninja_exit()
  use ninjago_module, only: ninja_clear_integral_cache
  implicit none
  !------#[ call ninja_clear_integral_cache():
  call ninja_clear_integral_cache()
  !------#] call ninja_clear_integral_cache():
end subroutine ninja_exit
!---#] subroutine ninja_exit:
end module pb1_gghh_groups
