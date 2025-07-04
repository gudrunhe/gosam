[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]globalsh[% helicity %]_qp
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki => ki_qp[%
   @for repeat num_colors shift=1 %][%
      @if is_first %]
   use [% process_name asprefix=\_ %]color_qp, only:[%
      @else %],[%
      @end @if %]&
      & c[% $_ %]v => c[% $_ %][%
   @end @for %]

   implicit none
   private[%

   @for repeat num_colors shift=1 %]
   complex(ki), public :: c[% $_ %][%
   @end @for %]

   public :: init_lo

   complex(ki), public :: rat2
contains

subroutine     init_lo()
   use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow, [%
@if generate_tree_diagrams %]ccontract, amp0[%
@else %]col0[%
@end @if %]
   implicit none[%

@for repeat num_colors shift=1 %]
   c[% $_ %] = [%
   @if generate_tree_diagrams %]ccontract(c[% $_ %]v, amp0[% @if helsum %](:,[%helicity%])[%@end @if%])[%
   @else %]c[% $_ %]v(col0)[%
   @end @if %][%
@end @for %]
end subroutine init_lo

end module [% process_name asprefix=\_ %]globalsh[% helicity %]_qp
