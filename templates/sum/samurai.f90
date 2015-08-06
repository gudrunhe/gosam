[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module     [% process_name asprefix=\_ %]samurai
   ! This file has been generated for samurai version [% samurai.version %]
   ! Please, not the interface changes:
   ! 2.0 -> 2.1   : mu2 has changed from real to complex.
   ! 2.1 -> 2.1.1 : samurai_cm and samurai_rm have been made public
   !                we call them directly instead of the generic routine
   !                in order to avoid problems with some older versions of
   !                gfortran.
   !              + passing of invariants has been added.
   ! 2.1.1 -> 2.9.0: the generic samurai function is now used again.
   use precision, only: ki_sam => ki
   use [% process_name asprefix=\_ %]config, only: ki
   use [% process_name asprefix=\_ %]scalar_cache
   implicit none
   private[%

   @for groups var=grp %]
   public :: reduce_group[% grp %][%
   @end @for %]
contains
!---#[ grouped numerators for samurai:[%
   @for groups var=grp %][%
      @with eval loopsize group=grp result=ls %]
!-----#[ function numeval_group[% grp %]:
function     numeval_group[% grp %](icut, Q, mu2) result(num)[%
         @for repeat num_legs shift=1 %][%
            @if is_first %]
   use [% process_name asprefix=\_ %]kinematics, only:[%
            @else %],[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]l1, only: numerator_d[% DIAG %] => numerator_samurai[%
         @end @for %][%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]
   implicit none
   integer, intent(in) :: icut
   complex(ki_sam), dimension(4), intent(in) :: Q[%
   @if version_newer samurai.version 2.0 %]
   complex(ki_sam), intent(in) :: mu2[%
   @else %]
   real(ki_sam), intent(in) :: mu2[%
   @end @if %]
   complex(ki_sam) :: num

   logical, dimension(0:[% count diagrams group=grp %]-1) :: nonzero
   real(ki_sam), dimension(0:3) :: R
   complex(ki_sam) :: Q2[%
         @for propagators group=grp %][%
            @if is_first %]
   complex(ki_sam) ::[%
            @else %],[%
            @end @if %]denom[% $_ %][%
         @end @for %]

   nonzero(:) = .true.
   Q2 = Q(4)*Q(4) - Q(1)*Q(1) - Q(2)*Q(2) - Q(3)*Q(3) - mu2

   select case(icut)[%
         @for cuts ls %][%
            @for diagrams group=grp global_index=DIAGIDX var=DIAG
                 unpinched=$_ invert=true %][%
               @if is_first %]
   case([% $_ %])[%
               @end @if %]
      nonzero([% DIAGIDX %]) = .false.[%
               @if is_last %][%
                  @for propagators group=grp prefix=k index=propidx %][%
                     @if eval $_ ~ ( propidx - 1 ) %]
      denom[% propidx %] = 0.0_ki[%
                     @else %][%
                        @if eval momentum .eq. 0 %]
      denom[% propidx %] = Q2[%
                           @if eval mass .eq. 0 %][%
                           @else %] - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_sam, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %][%
                        @else %]
      R = real([% momentum %], ki_sam)
      denom[% propidx %] = Q2 + (Q(4) + Q(4) + R(0))*R(0) &
                 &    - (Q(1) + Q(1) + R(1))*R(1) &
                 &    - (Q(2) + Q(2) + R(2))*R(2) &
                 &    - (Q(3) + Q(3) + R(3))*R(3)[%
                           @if eval mass .eq. 0 %][%
                           @else %]&
                 &    - [%mass%]*[%mass%][%
                              @if eval width .eq. 0 %][%
                              @else %] + cmplx(0.0_ki_sam, [%mass%]*[%width%])[%
                              @end @if %][%
                           @end @if %][%
                        @end @if %][%
                     @end @if %][%
                  @end @for propagators %][%
               @end @if %][%
            @end @for diagrams %][%
         @end @for cuts %]
   case default[%
         @for propagators group=grp prefix=k %][%
            @if eval momentum .eq. 0 %]
      denom[% $_ %] = Q2[%
               @if eval mass .eq. 0 %][%
               @else %] - [%mass%]*[%mass%][%
                  @if eval width .eq. 0 %][%
                  @else %] + cmplx(0.0_ki_sam, [%mass%]*[%width%])[%
                  @end @if %][%
               @end @if %][%
            @else %]
      R = real([% momentum %], ki_sam)
      denom[% $_ %] = Q2 + (Q(4) + Q(4) + R(0))*R(0) &
                 &    - (Q(1) + Q(1) + R(1))*R(1) &
                 &    - (Q(2) + Q(2) + R(2))*R(2) &
                 &    - (Q(3) + Q(3) + R(3))*R(3)[%
               @if eval mass .eq. 0 %][%
               @else %]&
                 &    - [%mass%]*[%mass%][%
                  @if eval width .eq. 0 %][%
                  @else %] + cmplx(0.0_ki_sam, [%mass%]*[%width%])[%
                  @end @if width .eq. 0 %][%
               @end @if mass .eq. 0 %][%
            @end @if momentum .eq. 0 %][%
         @end @for propagators %]
   end select
   
   num = (0.0_ki_sam, 0.0_ki_sam)[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:
   if(nonzero([% index %])[%
            @if use_flags_1 %].and.evaluate_virt_diagram([% DIAG %])[%
            @end @if %]) then
      num = num [%
      @if diagsum %]+ numerator_d[% DIAG %](icut, Q, mu2)[%
            @for elements pinches %] * denom[% $_ %][%
            @end @for %][%
            @else %][% diagram_sign %] [%
            @if is_nf %]Nfrat * [%
            @end @if %]numerator_d[% DIAG %](icut, Q, mu2)[%
            @for elements pinches %] * denom[% $_ %][%
            @end @for %][% @end @if %]
   end if
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]
end function numeval_group[% grp %]
!-----#] function numeval_group[% grp %]:[%
      @end @with %][%
   @end @for groups %]
!---#] grouped numerators for samurai:
!---#[ reduce groups with samurai:[%
   @for groups var=grp %]
!-----#[ subroutine reduce_group[% grp %]:
subroutine     reduce_group[% grp %](scale2,tot,totr,ok)
   use msamurai, only: samurai[% @if version_newer samurai.version 2.8 %][%
   @else %][% @if version_newer samurai.version 2.1 %], samurai_rm, samurai_cm[%
   @end @if %][% @end @if %]
   use options, only: samurai_out => iout[%
   @if version_newer samurai.version 2.8 %]
   use mgetkin, only: s_mat[% @else %][%
   @if version_newer samurai.version 2.1 %]
   use madds, only: s_mat[%
   @end @if %][% @end @if %]
   use [% process_name asprefix=\_ %]config, only: samurai_group_numerators, &
      & samurai_verbosity, samurai_istop, samurai_test, &
      & debug_nlo_diagrams, logfile
   use [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_ %]model[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   use [% process_name asprefix=\_ %]d[% DIAG %]l1, only: numerator_diagram[% DIAG %] => numerator_samurai[%
         @end @for %]
   use [% process_name asprefix=\_ %]globalsl1, only: epspow[%
         @if use_flags_1 %]
   use [% process_name asprefix=\_ %]groups, only: evaluate_virt_diagram[%
         @end @if %]

   implicit none
   real(ki_sam), intent(in) :: scale2
   complex(ki_sam), dimension(-2:0), intent(out) :: tot
   complex(ki_sam), intent(out) :: totr
   logical, intent(out) :: ok

   complex(ki_sam), dimension(-2:0) :: acc
   complex(ki_sam) :: accr
   logical :: acc_ok

   integer :: istopm, istop0

   integer, parameter :: effective_group_rank = [% rank %][%
   @if version_newer samurai.version 2.1 %]
   !-----------#[ invariants for samurai:
   complex(ki_sam), dimension([% 
        loopsize group=grp %], [% loopsize group=grp %]) :: g_mat
   !-----------#] initialize invariants:[%
   @end @if %]
   [%
   @if complex_mass_needed group=grp %]complex(ki_sam)[%
   @else %]real(ki_sam)[%
   @end @if %], dimension([% loopsize group=grp %]) :: msq
   real(ki_sam), dimension([% loopsize group=grp %],4) :: Vi
   
   if(samurai_test.eq.1 .or. samurai_test.eq.3) then
      istopm = 1
      istop0 = 1
   else
      istopm = samurai_istop
      istop0 = max(2,samurai_istop)
   end if[%

   @for propagators group=grp suffix=((/2,3,4,1/))%]
   msq([% $_ %]) = [% 
      @if eval mass .eq. 0 %]0.0_ki_sam[%
      @else %][%
         @if eval width .eq. 0 %]real([% mass %]*[% mass %], ki_sam)[%
         @else %]real([%mass%],ki_sam)*cmplx([%mass%],-[%width%],ki_sam)[%
         @end @if %][%
      @end @if %]
   Vi([% $_ %],:) = real([% momentum %], ki_sam)[%
   @end @for %][%
   @if version_newer samurai.version 2.1 %]
   !-----------#[ initialize invariants:[%
      @for smat upper diagonal
           group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es %]
   g_mat([%rowindex%], [%colindex%]) = [%
            @if im.is_zero %]real([% @else %]cmplx([% @end @if %][%
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
            @end @if %][%
      
            @if im.is_zero %][% @else %],[% @end @if %][%
      
            @for elements im delimiter=; var=term first=first_term %][%
               @for elements term delimiter=: %][%
                  @if is_first %][%
                     @if eval $_ .ge. 0 %]+[%
                     @else %]-[%
                     @end @if %][%
      
                     @select $_
                     @case 2 -2 %][%
                     @case 4 -4%]2.0_ki*[%
                     @else %][%
                        @with eval .abs. $_ / 2 result=num %][%
                           num convert=float format=%0.1f_ki %][%
                        @end @with %]*[%
                     @end @select %][%
                  @else %][% $_ %][%
                  @end @if %][%
               @end @for %][%
            @end @for %], ki_sam)[%
      
            @if eval rowindex .ne. colindex %]
   g_mat([% colindex %], [% rowindex %]) = g_mat([% 
                                        rowindex %], [% colindex %])[%
            @end @if %][%
         @end @for %]
   !-----------#] initialize invariants:[%
   @end @if %]

   if(samurai_group_numerators) then
      !------#[ reduce numerator numeval_group[% grp %]:
      if(samurai_verbosity > 0) then
         write(samurai_out,*) "[GoSam] numeval_group[% grp %]"
         write(samurai_out,*) "[GoSam] epspow=", epspow
      end if[%
   @if version_newer samurai.version 2.1 %]
      !-----------#[ initialize invariants:
      allocate(s_mat([% loopsize group=grp %], [% loopsize group=grp %]))
      s_mat(:,:) = g_mat(:,:)
      !-----------#] initialize invariants:[%
   @end @if %]
      call samurai[% @if version_newer samurai.version 2.8 %][% @else %][%
   @if version_newer samurai.version 2.1 %][%
      @if complex_mass_needed group=grp %]_cm[% @else %]_rm[%
      @end @if %][% @end @if%][%
   @end @if %](numeval_group[% grp %], tot, totr, Vi, [%
   @if version_newer samurai.version 2.8 %][% @if complex_mass_needed group=grp %]msq, [% @else
   %]cmplx(msq,0._ki_sam,ki_sam), [% @end @if %][% @else
   %]msq, [% @end @if %][%
         loopsize group=grp %], &
         & effective_group_rank, [%
   @if iterator_empty propagators group=grp massive %]istop0[%
   @else %]istopm[%
   @end @if %], scale2, ok[%
   @if version_newer samurai.version 2.0 %], &
         & samurai_cache_flag_g[%grp%], samurai_cache_g[%grp%][%
   @end @if %])[%
   @if version_newer samurai.version 2.1 %]
      !-----------#[ deallocate invariants:
      deallocate(s_mat)
      !-----------#] deallocate invariants:[%
   @end @if %]

      !------#] reduce numerator numeval_group[% grp %]:
   else
      !------#[ sum over reduction of single diagrams:[%
   @for diagrams group=grp var=DIAG index=DIAGIDX idxshift=1 %][%
      @if use_flags_1 %]
      if(evaluate_virt_diagram([% DIAG %])) then[%
      @end @if %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<diagram index='[% DIAG %]'>"
         end if
         if(samurai_verbosity > 0) then
            write(samurai_out,*) "[GoSam] numerator_diagram[% DIAG %]"
            write(samurai_out,*) "[GoSam] epspow=", epspow
         end if[%
   @if version_newer samurai.version 2.1 %]
         !-----------#[ initialize invariants:
         allocate(s_mat([% loopsize diagram=DIAG %], [%
                           loopsize diagram=DIAG %]))
         s_mat(:,:) = g_mat( (/[%indices%]/), (/[%indices%]/) )
         !-----------#] initialize invariants:[%
   @end @if %]
         call samurai[% @if version_newer samurai.version 2.8 %][% @else %][%
   @if version_newer samurai.version 2.1 %][%
      @if complex_mass_needed group=grp %]_cm[% @else %]_rm[%
      @end @if %][% @end @if%][%
   @end @if %](numerator_diagram[% DIAG %], acc, accr, &
            & Vi((/[% indices %]/),:), [%
   @if version_newer samurai.version 2.8 %][% @if complex_mass_needed group=grp %]msq((/[% indices %]/)), [% @else
   %]cmplx(real(msq((/[% indices %]/)),ki_sam),0._ki_sam,ki_sam), [% @end @if %][% @else
   %]msq((/[% indices %]/)), [% @end @if %][%
         loopsize diagram=DIAG %], &
            & [% rank %], [%
   @if iterator_empty propagators group=grp
          select=indices massive %]istop0[%
   @else %]istopm[%
   @end @if %], scale2, [%
      @if is_first %]ok[%
      @else %]acc_ok[%
      @end @if %][%
   @if version_newer samurai.version 2.0 %], &
            & samurai_cache_flag_d[%DIAG%], samurai_cache_d[%DIAG%][%
   @end @if %])[%
   @if version_newer samurai.version 2.1 %]
         !-----------#[ deallocate invariants:
         deallocate(s_mat)
         !-----------#] deallocate invariants:[%
   @end @if %]
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
   end if
end subroutine reduce_group[% grp %]
!-----#] subroutine reduce_group[% grp %]:[%
   @end @for %]
!---#] reduce groups with samurai:
end module [% process_name asprefix=\_ %]samurai
