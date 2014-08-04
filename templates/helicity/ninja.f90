![% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]
module     [% process_name asprefix=\_ %]ninjah[% helicity %]
   ! This file has been generated for ninja 
   use ninjago_module, only: ki_nin
   use [% process_name asprefix=\_ %]config
   implicit none
   private[%

   @for groups var=grp %]
   public :: ninja_reduce_group[% grp %][%
   @end @for %]
contains
!---#[ reduce groups with ninja:[%
   @for groups var=grp %]
!-----#[ subroutine ninja_reduce_group[% grp %]:
subroutine     ninja_reduce_group[% grp %](scale2,tot,totr,ok)
   use iso_c_binding, only: c_ptr, c_loc, c_int
   use ninjago_module
   use [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l1, only: numerator_diagram[% DIAG %] => numerator_ninja
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l121, only: numerator_tmu_diagram[% DIAG %] => numerator_tmu
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l131, only: numerator_t3_diagram[% DIAG %] => numerator_t3
   use [% process_name asprefix=\_ %]d[% DIAG %]h[% helicity 
     %]l132, only: numerator_t2_diagram[% DIAG %] => numerator_t2[%
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
   integer(c_int) :: acc_ok

   integer :: istopm, istop0

   integer, parameter :: effective_group_rank = [% rank %]

   !-----------#[ invariants for ninja:
   real(ki_nin), dimension([% loopsize group=grp %],[% loopsize group=grp %]) :: s_mat
   !-----------#] initialize invariants:
   [%
   @if complex_mass_needed group=grp %]complex(ki_nin)[%
   @else %]real(ki_nin)[%
   @end @if %], dimension([% loopsize group=grp %]) :: msq
   real(ki_nin), dimension(4,[% loopsize group=grp %]) :: Vi

   ok = .true.
   
   if (ninja_test.eq.1) then
      istopm = 1
      istop0 = 1
   else
      istopm = ninja_istop
      istop0 = max(2,ninja_istop)
   end if[%
   @for propagators group=grp %]
   msq([% $_ %]) = [% 
      @if eval mass .eq. 0 %]0.0_ki_nin[%
      @else %][%
         @if eval width .eq. 0 %]real([% mass %]*[% mass %], ki_nin)[%
         @else %]real([%mass%],ki_nin)*cmplx([%mass%],-[%width%],ki_nin)[%
         @end @if %][%
      @end @if %]
   Vi(:,[% $_ %]) = real([% momentum %], ki_nin)[%
   @end @for %]
   !-----------#[ initialize invariants:[%
      @for smat upper diagonal
           group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es %]
   s_mat([%rowindex%],[%colindex%]) = real([%
            @if re.is_zero %]0.0_ki[% 
            @else %][%
               @for elements re delimiter=; var=term first=first_term %][%
                  @for elements term delimiter=: %][%
                     @if is_first %][%
                        @if eval $_ .ge. 0 %][%
                           @if first_term %][%
                           @else %]+[%
                           @end @if %][%
                        @else %]-[%
                        @end @if %][%
   
                        @select $_
                        @case 2 -2 %][%
                        @case 4 -4%]2.0_ki*[%
                        @else %][%
                           @with eval .abs. $_ / 2 result=num %][%
                           num convert=float format=%0.1f_ki%][%
                           @end @with %]*[%
                        @end @select %][%
                     @else %][% $_ %][%
                     @end @if %][%
                  @end @for %][%
               @end @for %][%
            @end @if %], ki_nin)[%
      
            @if eval rowindex .ne. colindex %]
   s_mat([% colindex %],[% rowindex %]) = s_mat([% rowindex %],[% colindex %])[%
            @end @if %][%
         @end @for %]
   !-----------#] initialize invariants

   
      !------#[ sum over reduction of single diagrams:[%
   @for diagrams group=grp var=DIAG index=DIAGIDX idxshift=1 %][%
      @if use_flags_1 %]
      if(evaluate_virt_diagram([% DIAG %])) then[%
      @end @if %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<diagram index='[% DIAG %]'>"
         end if
         call ninja_diagram(numerator_diagram[% DIAG %], numerator_t3_diagram[% DIAG %], numerator_t2_diagram[% DIAG %], &
          &  numerator_tmu_diagram[% DIAG %], &
          & [% loopsize group=grp %], [% loopsize diagram=DIAG %], [% rank %], (/[% indices %]/), &
          & Vi, [%
            @if iterator_empty propagators group=grp
            select=indices massive %][%
            @else %]msq, [%
            @end @if %]s_mat, scale2, [%
            @if iterator_empty propagators group=grp
            select=indices massive %]istop0[%
            @else %]istopm[%
            @end @if %], &
          & acc, accr, acc_ok)
            ok = ok .and. (acc_ok.eq.NINJA_SUCCESS)
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
