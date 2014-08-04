[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]custompropagator
   use [% process_name asprefix=\_%]config, only: ki
   use [% process_name asprefix=\_ %]model
   implicit none
   save

   private

   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   real(ki), parameter :: sqrthalf = &
   & 0.7071067811865475244008443621048490392848359376884740365883398689_ki

public :: customSpin2Prop

contains
  !---#[ function customSpin2Prop :
   function customSpin2Prop(s, m) result(ret)
      implicit none
      real(ki), intent(in) :: s ! four-momentum squared
      real(ki), intent(in) :: m ! mass
      complex(ki) :: ret

      ! write here your custom code and delete the next three lines
      ret = 0
      write (*, *) "customSpin2Prop in custompropagator.f90 need to be changed."
      stop

   end function customSpin2Prop
   !---#] function customSpin2Prop 
end module [% process_name asprefix=\_ %]custompropagator
