[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]golem95h[% helicity %]
   use precision_golem, only: ki_gol => ki
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none
   private[%

@for groups var=grp %][%
   @if is_first %]
   interface reconstruct_group[%
   @end @if %]
      module procedure reconstruct_group[% grp %][%
   @if is_last %]
   end interface
   
   public :: reconstruct_group[%
   @end @if %][%
@end @for %]
contains[%

@for groups var=grp %]
!---#[ subroutine reconstruct_group[% grp %]:
subroutine     reconstruct_group[% grp %](coeffs)
   use tens_rec
   use [% process_name asprefix=\_ %]config
   use [% process_name asprefix=\_
       %]groups, only:[%
         @if use_flags_1 %] evaluate_virt_diagram,[%
         @end @if %] tensrec_info_group[% grp %][%
         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1, only: numerator_d[% DIAG %] => numerator_golem95[%
            @if internal GENERATE_DERIVATIVES %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1d, only: reconstruct_d[% DIAG %][%
            @end @if %][%
         @end @for %]
   implicit none
   type(tensrec_info_group[% grp %]), intent(out) :: coeffs[%
   @for diagrams group=grp var=DIAG %]
   !------#[ Diagram [% DIAG %]:[%
      @if use_flags_1 %]
   if(evaluate_virt_diagram([% DIAG %])) then[%
      @end @if %][%
      @if internal GENERATE_DERIVATIVES %]
      if (tens_rec_by_derivatives) then
         call reconstruct_d[% DIAG %](coeffs)
      else[%
      @end @if %][%
      @if eval rank .eq. 0 %]
         coeffs%coeffs_[% DIAG %] = &
            & numerator_d[% DIAG %]((/0.0_ki_gol, 0.0_ki_gol, 0.0_ki_gol, &
            & 0.0_ki_gol/), 0.0_ki_gol)[%
      @else %]
         call reconstruct[% 
         rank %](numerator_d[% DIAG %], coeffs%coeffs_[% DIAG %][%
         @select r2 @case implicit %][%
            @with eval loopsize diagram=DIAG result=DIAGLS %][%
               @if eval DIAGLS .lt. 5 %][%
                  @if eval rank .gt. 1 %], &
            & coeffs%coeffs_[% DIAG %]s1[%
                  @end @if %][%
                  @if eval rank .gt. 3 %], coeffs%coeffs_[% DIAG %]s2[%
                  @end @if %][%
               @end @if %][%
               @if eval DIAGLS .eq. 5 %][%
                  @if eval rank .gt. 5 %], &
            & coeffs%coeffs_[% DIAG %]s1, coeffs%coeffs_[% DIAG %]s2, coeffs%coeffs_[% DIAG %]s3[%
                  @end @if %][%
               @end @if %][%
            @end @with %][%
         @end @select %])[%
      @end @if %][%
      @if internal GENERATE_DERIVATIVES %]
      end if[%
      @end @if %][%
      @if use_flags_1 %]
   end if[%
      @end @if %]
   !------#] Diagram [% DIAG %]:[%
   @end @for diagrams %]
end subroutine reconstruct_group[% grp %]
!---#] subroutine reconstruct_group[% grp %]:[%
@end @for groups %]
end module [% process_name asprefix=\_ %]golem95h[% helicity %]
