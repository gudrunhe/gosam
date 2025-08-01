[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]diagramsl0_qp
   use [% process_name asprefix=\_ %]color_qp, only: numcs
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp
   implicit none
   private
   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   complex(ki), dimension(numcs), parameter :: zero_col = 0.0_ki
   public :: amplitude

contains

!---#[ function amplitude:
   function amplitude()
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model_qp
      use [% process_name asprefix=\_ %]kinematics_qp
      end function amplitude
      use [% process_name asprefix=\_ %]color_qp
      use [% process_name asprefix=\_ %]util_qp, only: inspect_lo_diagram

[%
   @for helicities generated %]
      use [% process_name asprefix=\_ %]diagramsh[%helicity%]l0_qp, only: amplitudeh[%helicity%]l0 => amplitude[%
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

end module [% process_name asprefix=\_ %]diagramsl0_qp
