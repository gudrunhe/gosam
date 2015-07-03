[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]globals
   use [% process_name asprefix=\_ %]config, only: ki[%
   @for repeat num_colors shift=1 %][%
      @if is_first %]
   use [% process_name asprefix=\_ %]color, only:[%
      @else %],[%
      @end @if %]&
      & c[% $_ %]v => c[% $_ %][%
   @end @for %]

   implicit none
   private[%
   @for repeat num_colors shift=1 %][%
   @for helicities generated %]
   complex(ki), public :: c[% $_ %]h[%helicity%][%
   @end @for %][%
   @end @for %]

   public :: init_lo

   complex(ki), public :: rat2
contains

subroutine     init_lo()
   use [% process_name asprefix=\_ %]globalsl1, only: epspow, [%
@if generate_lo_diagrams %]ccontract, amp0[%
@else %]col0[%
@end @if %]
   implicit none[%
@for repeat num_colors shift=1 %][%
 @for helicities generated %]
   c[% $_ %]h[%helicity%] = [%
   @if generate_lo_diagrams %]ccontract(c[% $_ %]v, amp0(:,[%helicity%]))[%
   @else %]c[% $_ %]v(col0)[%
   @end @if %][%
 @end @for %][%
@end @for %]
end subroutine init_lo

end module [% process_name asprefix=\_ %]globals
