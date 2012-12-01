[% ' vim: syntax=golem
 %]module     [% process_name asprefix=\_ %]diagramsh[%helicity%]l0[%
   @if fr5 %]fr5[%
   @end @if %]
   use [% process_name asprefix=\_ %]accu, only: sorted_sum
   use [% process_name asprefix=\_ %]config, only: ki, use_sorted_sum, &
      & debug_lo_diagrams, logfile
   use [% process_name asprefix=\_ %]util, only: inspect_lo_diagram
   use [% process_name asprefix=\_ %]color, only: numcs
   [% @if internal CUSTOM_SPIN2_PROP
   %]use [% process_name asprefix=\_ %]custompropagator[% @end @if %]
   implicit none

   private

   public :: amplitude

contains
   function     amplitude() result(amp)[%
   @for elements topolopy.keep.tree %]
      use [% process_name asprefix=\_ %]d[%$_%]h[%
                   helicity%]l0[%
            @if fr5 %]fr5[%
	    @end @if %], only: diagram[%$_%][%
   @end @for %][%
   @if use_flags_0 %]
      use [% process_name asprefix=\_ %]groups, only: evaluate_lo_diagram[%
   @end @if %]
      implicit none
      complex(ki), dimension(numcs) :: amp
      complex(ki), dimension([% topolopy.count.tree %],numcs) :: diagrams
      integer :: i[%
      @for elements topolopy.keep.tree %][%
         @with eval index + 1 result=DIAG %][%
	    @if use_flags_0 %]
      if(evaluate_lo_diagram([% DIAG %])) then[%
	    @end @if %]
         diagrams([%DIAG%],:) = [%
	    @select tree_sign DIAG @case -1 - %]-[%
	    @end @select %]diagram[%$_%]()[% 

	    @if use_flags_0 %]
      else
         diagrams([%DIAG%],:) = 0.0_ki
      end if[%
	    @end @if %][%
	 @end @with %][%
      @end @for %]
      if (debug_lo_diagrams) then[%
         @for elements topolopy.keep.tree %]
         [% @if use_flags_0 %]if(evaluate_lo_diagram([% eval index + 1 %])) [%
	    @end @if %]call inspect_lo_diagram(diagrams([%
                eval index + 1 %],:), [%$_%], [%
            helicity%], logfile)[%
         @end @for %]
      end if

      if (use_sorted_sum) then
         do i=1,numcs
            amp(i) = sorted_sum(diagrams(:,i))
         end do
      else
         do i=1,numcs
            amp(i) = sum(diagrams(:,i))
         end do
      end if
   end function amplitude
end module [% process_name asprefix=\_ %]diagramsh[%helicity%]l0[%
   @if fr5 %]fr5[%
   @end @if %]
