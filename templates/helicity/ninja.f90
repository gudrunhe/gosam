[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]ninjah[% helicity %]
   ! This file has been generated for ninja 
   use ninja_module, only: ki_nin
   use [% process_name asprefix=\_ %]config
   implicit none
   private[%

   @for groups var=grp %]
   public :: ninja_reduce_group[% grp %][%
   @end @for %]
contains[%
   @for groups var=grp %]
!-----#[ subroutine ninja_reduce_group[% grp %]:
subroutine     ninja_reduce_group[% grp %](scale2,tot,totr,ok)
   use ninja_module
   use [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1, only: numerator_diagram[% DIAG %] => numerator_ninja
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l12, only: numerator_d_diagram[% DIAG %] => numerator_d
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l13, only: numerator_t_diagram[% DIAG %] => numerator_t[%
         @end @for %]
   use [% process_name asprefix=\_ %]globalsl1, only: epspow[%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]

   implicit none
   real(ki_nin), intent(in) :: scale2
   complex(ki_nin), dimension(-2:0), intent(out) :: tot
   complex(ki_nin), intent(out) :: totr
   logical, intent(out) :: ok

   complex(ki_nin), dimension(-2:0) :: acc
   complex(ki_nin) :: accr
   logical :: acc_ok

   integer :: istopm, istop0

   integer, parameter :: effective_group_rank = [% rank %]

   !-----------#[ invariants for ninja (not used):
   real(ki_nin), dimension([% loopsize group=grp %]**2) :: s_mat
   !-----------#] initialize invariants:
   [%
   @if complex_mass_needed group=grp %]complex(ki_nin)[%
   @else %]real(ki_nin)[%
   @end @if %], dimension([% loopsize group=grp %]) :: msq
   real(ki_nin), dimension([% loopsize group=grp %]*4) :: Vi
   
   if(samurai_test.eq.1 .or. samurai_test.eq.3) then
      istopm = 1
      istop0 = 1
   else
      istopm = samurai_istop
      istop0 = max(2,samurai_istop)
   end if[%
   @for propagators group=grp %]
   msq([% $_ %]) = [% 
      @if eval mass .eq. 0 %]0.0_ki_nin[%
      @else %][%
         @if eval width .eq. 0 %]real([% mass %]*[% mass %], ki_nin)[%
         @else %]real([%mass%],ki_nin)*cmplx([%mass%],-[%width%],ki_nin)[%
         @end @if %][%
      @end @if %]
   !Vi(([% $_ %]-1)*[% loopsize group=grp %]+1:([% $_ %]-1)*[% loopsize group=grp %]+4) = real([% momentum %], ki_nin)
   Vi(([% $_ %]-1)*4+1:([% $_ %]-1)*4+4) = real([% momentum %], ki_nin)[%
   @end @for %]

      !------#[ sum over reduction of single diagrams:[%
   @for diagrams group=grp var=DIAG index=DIAGIDX idxshift=1 %][%
      @if use_flags_1 %]
      if(evaluate_virt_diagram([% DIAG %])) then[%
      @end @if %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<diagram index='[% DIAG %]'>"
         end if
         call ninja_select_rm(numerator_diagram[% DIAG %], numerator_t_diagram[% DIAG %], &
          &  numerator_d_diagram[% DIAG %],  acc, accr, [% loopsize diagram=DIAG %], &
          & Vi, msq, s_mat, [% rank %], istop0, scale2, &
          & (/[% indices %]/))
         !-----------#[ deallocate invariants:
         ! deallocate(s_mat)
         !-----------#] deallocate invariants:
         if(debug_nlo_diagrams) then
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-finite' re='", [%
                  diagram_sign %]real(acc(0), ki), &
               & "' im='", aimag(acc(0)), "'/>"
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-single' re='", [%
                  diagram_sign %]real(acc(-1), ki), &
               & "' im='", aimag(acc(-1)), "'/>"
            write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-double' re='", [%
                  diagram_sign %]real(acc(-2), ki), &
               & "' im='", aimag(acc(-2)), "'/>"
            write(logfile,'(A32,E24.16,A6,E24.16,A3)') &
               & "<result kind='nlo-rational' re='", [%
                  diagram_sign %]real(accr, ki), &
               & "' im='", aimag(accr), "'/>"
            if(ok) then
               write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
            else
               write(logfile,'(A29)') "<flag name='ok' status='no'/>"
            end if
            write(logfile,*) "</diagram>"
         end if

         tot = [%
      @if is_first %][% @if diagsum %] + [%
      @else %][% diagram_sign %][% @end @if %][%
      @else %]tot [% @if diagsum %] + [% @else %] [% diagram_sign %] [%
      @end @if %][%
      @end @if %][%
      @if is_nf %][% @if diagsum %] [% @else %] Nfrat * [%
      @end @if %][%
      @end @if %]acc
         totr = [%
      @if is_first %][% @if diagsum %] + [%
      @else %][% diagram_sign %][% @end @if %][%
      @else %]totr [% @if diagsum %] + [% @else %] [% diagram_sign %] [%
      @end @if %][%
      @end @if %][%
      @if is_nf %][% @if diagsum %] [% @else %] Nfrat * [%
      @end @if %][%
      @end @if %]accr[%
      @if is_first %][%
      @else %]
         ok = ok .and. acc_ok[%
      @end @if %][%
      @if use_flags_1 %]
      end if[%
      @end @if %][%
   @end @for %]
      !------#] sum over reduction of single diagrams:

end subroutine ninja_reduce_group[% grp %]
!-----#] subroutine ninja_reduce_group[% grp %]:[%
   @end @for %]
!---#] reduce groups with ninja:
end module [% process_name asprefix=\_ %]ninjah[% helicity %]
