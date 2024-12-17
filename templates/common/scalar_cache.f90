[%' vim: sw=3:syntax=golem

'%]module     [% process_name asprefix=\_ %]scalar_cache
   implicit none
   save

   private

   public :: invalidate_cache
contains
   subroutine invalidate_cache()
      implicit none
   end subroutine invalidate_cache
end module [% process_name asprefix=\_ %]scalar_cache[%
