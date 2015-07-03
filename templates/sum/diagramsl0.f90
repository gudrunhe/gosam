[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]diagramsl0
   use [% process_name asprefix=\_ %]color, only: numcs
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none
   private
   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki
   public :: amplitude

contains

!---#[ function amplitude:
   function amplitude()
      use [% process_name asprefix=\_ %]model
      use [% process_name asprefix=\_ %]kinematics
      use [% process_name asprefix=\_ %]color
      use [% process_name asprefix=\_ %]config, only: debug_lo_diagrams, &
        & use_sorted_sum
      use [% process_name asprefix=\_ %]accu, only: sorted_sum
      use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram

[%
   @for helicities generated %]
      use [% process_name asprefix=\_ %]diagramsh[%helicity%]l0, only: amplitudeh[%helicity%]l0 => amplitude[%
   @end @for %]

      implicit none
      complex(ki), dimension(numcs) :: amplitude[%
   @for helicities generated %][%
     @if is_first %]
      amplitude(:) = amplitudeh[%helicity%]l0()[%
     @else%]
      amplitude(:) = amplitude + amplitudeh[%helicity%]l0()[%
     @end @if %][%
   @end @for %]

   end function     amplitude
!---#] function amplitude:

end module [% process_name asprefix=\_ %]diagramsl0
