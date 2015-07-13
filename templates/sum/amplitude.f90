[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module    [% process_name asprefix=\_ %]amplitude
   use [% process_name asprefix=\_ %]config, only: ki, &
       & reduction_interoperation
   use [% process_name asprefix=\_ %]color, only: numcs[%
@if generate_nlo_virt %][%
   @select r2
   @case implicit explicit off %]
   use [% process_name asprefix=\_ %]groups[%
      @if extension samurai %]
   use precision, only: ki_sam => ki
   use [% process_name asprefix=\_ %]samurai[%
      @end @if %][%
      @if extension golem95 %]
   use precision_golem, only: ki_gol => ki
   use [% process_name asprefix=\_ %]golem95[%
      @end @if %][%
      @if extension ninja %]
   use ninjago_module, only: ki_nin
   use [% process_name asprefix=\_ %]ninja[%
      @end @if %][%
   @end @select %][%
@end @if %]
   [% @if internal CUSTOM_SPIN2_PROP
   %]use [% process_name asprefix=\_ %]custompropagator[% @end @if %]
   implicit none
   private

   public :: samplitude
contains
   !---#[ function samplitude:
   function     samplitude(scale2,ok,rational2,[%
@if generate_lo_diagrams %]opt_amp0,[%
@else %]the_col0,[%
@end @if%]opt_perm)
      use [% process_name asprefix=\_
         %]config, only: include_eps_terms, include_eps2_terms, &
      & logfile, debug_nlo_diagrams
      use [% process_name asprefix=\_
         %]globalsl1, only:[%
@if generate_lo_diagrams %] amp0,[%
@else %] col0,[%
@end @if %]perm, use_perm, epspow
      use [% process_name asprefix=\_ %]globals, &
     & only: init_lo, rat2[%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %]
      use [% process_name asprefix=\_
      %]abbrevh[%helicity %], only: init_abbrev[%
   @case diagram %][%
      @for groups var=grp %][%
         @for diagrams group=grp %]
      use [% process_name asprefix=\_
      %]abbrevd[%$_%], only: init_abbrevd[%$_%] => init_abbrev[%
         @end @for %][%
      @end @for %][%
   @case group %][%
      @for groups var=grp %]
      use [% process_name asprefix=\_
      %]abbrevg[%grp%], only: init_abbrevg[%grp%] => init_abbrev[%
      @end @for %][%
   @end @select %][%
@end @if %][%
@if generate_lo_diagrams %][%
   @for helicities generated %]
      use [% process_name asprefix=\_
      %]diagramsh[%helicity%]l0, only: amplitudeh[%helicity%]l0 => amplitude[%
   @end @for %][%
@end @if %][%
@select r2 @case only %][%
@else %]
      use [% process_name asprefix=\_ %]groups[%
@end @select %][%
      @if generate_uv_counterterms %]
      use [% process_name asprefix=\_
      %]diagramsct, only: samplitudect => samplitudect[%
      @end @if %]
      implicit none
      real(ki), intent(in) :: scale2
      logical, intent(out) :: ok
      real(ki), intent(out) :: rational2[%
@if generate_lo_diagrams %]
      complex(ki), dimension(numcs,0:max(0,[%@for helicities generated%][%@if is_first%][%@else%],[%@end @if%][%helicity%][%@end @for%])), intent(in), optional :: opt_amp0[%
@else %]
      integer, intent(in) :: the_col0[%
@end @if %]
      integer, dimension(numcs), intent(in), optional :: opt_perm
      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(-2:0) :: samplitude

      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(-2:0) :: acc
      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(0:2,-2:0) :: samp_part[%
      @if generate_uv_counterterms %]
      real(ki), dimension(3) :: sampct[%
      @end @if %]

      logical :: acc_ok

      ok = .true.
      rational2 = 0.0_ki

      samplitude(:) = 0.0_ki[%
@if generate_lo_diagrams %]
      if (present(opt_amp0)) then
         amp0 = opt_amp0
      else[%
         @for helicities generated %]
         amp0(:,[%helicity%]) = amplitudeh[%helicity%]l0()[%
         @end @for %]
      end if[%
@else %]
      col0 = the_col0[%
@end @if %]
      if (present(opt_perm)) then
         use_perm = .true.
         perm = opt_perm
      else
         use_perm = .false.
      end if

      rat2 = (0.0_ki, 0.0_ki)
      call init_lo()[%
@if generate_nlo_virt %][%

   @select abbrev.level
   @case helicity %]
      call init_abbrev()[%
   @case diagram %][%
      @for groups var=grp %][%
         @for diagrams group=grp %][%
            @if use_flags_1 %]
      if(evaluate_virt_diagram([%$_%])) then[%
            @end @if %]
        call init_abbrevd[%$_%]()[%
            @if use_flags_1 %]
      endif[%
         @end @if %][%
         @end @for %][%
      @end @for %][%
   @case group %][%
      @for groups var=grp %][%
            @if use_flags_1 %]
      if(evaluate_virt_group([%grp%])) then[%
            @end @if %]
        call init_abbrevg[%grp%]()[%
            @if use_flags_1 %]
      endif[%
         @end @if %][%
      @end @for %][%
   @end @select %][%


   @select r2
   @case implicit %]
      samp_part(:,:) = 0.0_ki
      do epspow=0,2
         if((epspow.eq.1) .and. .not. include_eps_terms) cycle
         if((epspow.eq.2) .and. .not. include_eps2_terms) cycle[%
      @for repeat maxloopsize shift=1 var=ls %][%
         @for groups loopsize=ls var=grp %][%
            @if use_flags_1 %]
         if(evaluate_virt_group([% grp %])) then[%
            @end @if %]
            call evaluate_group[% grp %](scale2, acc, acc_ok)
            ok = ok .and. acc_ok
            samp_part(epspow,:) = samp_part(epspow,:) + acc[%
            @if use_flags_1 %]
         end if[%
            @end @if %][%
         @end @for groups %][%
      @end @for %]
      end do
      samplitude( 0) = samp_part(0, 0) + samp_part(1,-1) + samp_part(2,-2)
      samplitude(-1) = samp_part(0,-1) + samp_part(1,-2)
      samplitude(-2) = samp_part(0,-2)[%
   @case off %]
      epspow=0
      samplitude(:) = 0.0_ki[%
      @for repeat maxloopsize shift=1 var=ls %][%
         @for groups loopsize=ls var=grp %][%
            @if use_flags_1 %]
      if(evaluate_virt_group([% grp %])) then[%
            @end @if %]
         call evaluate_group[% grp %](scale2, acc, acc_ok)
         ok = ok .and. acc_ok
         samplitude(:) = samplitude(:) + acc[%
            @if use_flags_1 %]
      end if[%
            @end @if %][%
         @end @for groups %][%
      @end @for %][%
   @case only %]
      samplitude(-2:-1) = 0.0_ki
      if(debug_nlo_diagrams) then
         write(logfile,'(A22,G24.16,A6,G24.16,A4)') &
         & "<result name='r2' re='", real(rat2, ki), &
         &                 "' im='", aimag(rat2), "' />"
      end if
      samplitude(0) = [%
      @if generate_lo_diagrams %]2.0_ki * real(rat2, ki)[%
      @else %]rat2[%
      @end @if %][%
   @case explicit %]
      epspow=0
      samplitude(-2) = 0.0_ki
      samplitude(-1) = 0.0_ki
      if(debug_nlo_diagrams) then
         write(logfile,'(A22,G24.16,A6,G24.16,A4)') &
         & "<result name='r2' re='", real(rat2, ki), &
         &                 "' im='", aimag(rat2), "' />"
      end if[%
      @if generate_lo_diagrams %]
      rational2 = 2.0_ki * real(rat2, ki)[%
      @end @if %]
      samplitude(0) = [%
      @if generate_lo_diagrams %]2.0_ki * real(rat2, ki)[%
      @else %]rat2[%
      @end @if %][%
      @for repeat maxloopsize shift=1 var=ls %][%
         @for groups loopsize=ls var=grp %][%
            @if use_flags_1 %]
      if(evaluate_virt_group([% grp %])) then[%
            @end @if %]
         call evaluate_group[% grp %](scale2, acc, acc_ok)
         ok = ok .and. acc_ok
         samplitude(:) = samplitude(:) + acc[%
            @if use_flags_1 %]
      end if[%
            @end @if %][%
         @end @for groups %][%
      @end @for %][%
   @end @select %][%
   @if generate_uv_counterterms %]
      sampct = samplitudect(scale2)
      samplitude(0) = samplitude(0) + sampct(3)
      samplitude(-1) = samplitude(-1) + sampct(2)
      samplitude(-2) = samplitude(-2) + sampct(1)[%
   @end @if %][%
@else %]
      samplitude(:) = (0.0_ki, 0.0_ki)[%
@end @if generate_nlo_virt %]
   end function samplitude
   !---#] function samplitude:[%
@select r2
@case implicit explicit off %][%
   @for groups var=grp %]
!---#[ subroutine evaluate_group[% grp %]:
subroutine     evaluate_group[% grp %](scale2,samplitude,ok)
   use [% process_name asprefix=\_ %]config, only: &
      & logfile, debug_nlo_diagrams
   use [% process_name asprefix=\_ %]globalsl1, only: epspow[%
      @if extension golem95 %]
   use parametre, only: mu2_scale_par
   use form_factor_type, only: form_factor
   use [% process_name asprefix=\_ %]golem95, only: reconstruct_golem95 => reconstruct_group
   use [% process_name asprefix=\_ %]groups, only: contract_golem95[%
         @if extension pjfry %], contract_pjfry[%
         @end @if %][%
         @if extension samurai %], &
      & global_coeffs => coeffs_group[% grp %], &
      & reduce_numetens => reduce_numetens_group[% grp %][%
         @end @if %][%
         @if extension pjfry %]
   use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf[%
         @end @if %][%
      @end @if %][%
      @if extension samurai %]
   use [% process_name asprefix=\_ %]samurai, only: samurai_reduce => reduce_group[% grp %]
   use options, only: samurai_out => iout[%
      @end @if %][%
      @if extension ninja %]
   use [% process_name asprefix=\_ %]ninja, only: ninja_reduce => ninja_reduce_group[% grp %][%
      @end @if %]
   implicit none
   real(ki), intent(in) :: scale2
   logical, intent(out) :: ok[%
      @if generate_lo_diagrams %]
   real(ki)[%
      @else %]
   complex(ki)[%
      @end @if %], dimension(-2:0), intent(out) :: samplitude[%
      @if extension golem95 %]
   type(tensrec_info_group[% grp %]), target :: coeffs
   type(form_factor) :: gres[%
         @if extension pjfry %]
   integer :: ep
   complex(ki_pjf) :: pjres[%
         @end @if %][%
      @end @if %][%
      @if extension samurai %]
   complex(ki_sam), dimension(-2:0) :: tot
   complex(ki_sam) :: totr
   logical :: samurai_ok[% @else
     %][% @if extension ninja %]
   complex(ki_nin), dimension(-2:0) :: tot
   complex(ki_nin) :: totr[%
      @end @if %][% @end @if %]

   if(debug_nlo_diagrams) then
      write(logfile,*) "<diagram-group index='[% grp %]'>"
      write(logfile,*) "<param name='epspow' value='", epspow, "'/>"
   end if
   select case(reduction_interoperation)[%
      @if extension samurai %]
   case(0) ! use Samurai only
      call samurai_reduce(real(scale2, ki_sam), tot, totr, ok)[%
         @if generate_lo_diagrams %]
      samplitude(:) = 2.0_ki * real(tot(:), ki)[%
         @else %]
      samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
         @end @if %][%
      @end @if %][%
      @if extension golem95 %]
   case(1) ! use Golem95 only
      call reconstruct_golem95(coeffs)
      mu2_scale_par = real(scale2, ki_gol)
      gres = contract_golem95(coeffs)[%
         @if generate_lo_diagrams %]
      samplitude(-2) = 2.0_ki * real(gres%A, ki)
      samplitude(-1) = 2.0_ki * real(gres%B, ki)
      samplitude( 0) = 2.0_ki * real(gres%C, ki)[%
         @else %]
      samplitude(-2) = cmplx(real(gres%A, ki_gol), aimag(gres%A), ki)
      samplitude(-1) = cmplx(real(gres%B, ki_gol), aimag(gres%B), ki)
      samplitude( 0) = cmplx(real(gres%C, ki_gol), aimag(gres%C), ki)[%
         @end @if %]
      ok = .true.[%
      @end @if %][%      
      @if extension ninja %]
   case(2) ! use Ninja only
      call ninja_reduce(real(scale2, ki_nin), tot, totr, ok)[%
         @if generate_lo_diagrams %]
      samplitude(:) = 2.0_ki * real(tot(:), ki)[%
         @else %]
      samplitude(:) = cmplx(real(tot(:), ki_nin), aimag(tot(:)), ki)[%
         @end @if %][%
      @end @if %][%
         @if extension pjfry %]
   case(3) ! use PJFry only
      call reconstruct_golem95(coeffs)[%
            @if generate_lo_diagrams %]
      do ep=0,2
         pjres = contract_pjfry(coeffs, scale2, ep)
         samplitude(-ep) = 2.0_ki * real(pjres, ki)
      end do[%
            @else %]
      do ep=0,2
         pjres = contract_pjfry(coeffs, scale2, ep)
         samplitude(-ep) = cmplx(real(pjres, ki_pjf), aimag(pjres), ki)
      end do[%
            @end @if %]
      ok = .true.[%
      @end @if %][%
      @if extension samurai %][%
         @if extension golem95 %]
   ! Modes which require Golem95 and Samurai
   case(20) ! Try Samurai first, use Golem95 is samurai fails
      call samurai_reduce(real(scale2, ki_sam), tot, totr, samurai_ok)
      if(samurai_ok) then[%
            @if generate_lo_diagrams %]
         samplitude(:) = 2.0_ki * real(tot(:), ki)[%
            @else %]
         samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
            @end @if %]
         ok = .true.
      else
         call reconstruct_golem95(coeffs)
         mu2_scale_par = real(scale2, ki_gol)
         gres = contract_golem95(coeffs)[%
            @if generate_lo_diagrams %]
         samplitude(-2) = 2.0_ki * real(gres%A, ki)
         samplitude(-1) = 2.0_ki * real(gres%B, ki)
         samplitude( 0) = 2.0_ki * real(gres%C, ki)[%
            @else %]
         samplitude(-2) = cmplx(real(gres%A, ki_gol), aimag(gres%A), ki)
         samplitude(-1) = cmplx(real(gres%B, ki_gol), aimag(gres%B), ki)
         samplitude( 0) = cmplx(real(gres%C, ki_gol), aimag(gres%C), ki)[%
            @end @if %]
         ok = .true.
      end if
   case(30) ! Tensorial Reconstruction + Samurai on numetens
      call reconstruct_golem95(coeffs)
      global_coeffs => coeffs
      call reduce_numetens(real(scale2, ki_sam), tot, totr, ok)[%
            @if generate_lo_diagrams %]
      samplitude(:) = 2.0_ki * real(tot(:), ki)[%
            @else %]
      samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
            @end @if %]
      nullify(global_coeffs)
   case(40) ! Tensorial Reconstruction + Samurai on numetens
           ! + Golem95 on failure
      call reconstruct_golem95(coeffs)
      global_coeffs => coeffs
      call reduce_numetens(real(scale2, ki_sam), tot, totr, samurai_ok)
      if(samurai_ok) then[%
            @if generate_lo_diagrams %]
         samplitude(:) = 2.0_ki * real(tot(:), ki)[%
            @else %]
         samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
            @end @if %]
         ok = .true.
      else
         mu2_scale_par = real(scale2, ki_gol)
         gres = contract_golem95(coeffs)[%
            @if generate_lo_diagrams %]
         samplitude(-2) = 2.0_ki * real(gres%A, ki)
         samplitude(-1) = 2.0_ki * real(gres%B, ki)
         samplitude( 0) = 2.0_ki * real(gres%C, ki)[%
            @else %]
         samplitude(-2) = cmplx(real(gres%A, ki_gol), aimag(gres%A), ki)
         samplitude(-1) = cmplx(real(gres%B, ki_gol), aimag(gres%B), ki)
         samplitude( 0) = cmplx(real(gres%C, ki_gol), aimag(gres%C), ki)[%
            @end @if %]
         ok = .true.
      end if[%
            @if extension pjfry %]
   ! Modes which require Golem95, PJFry and Samurai
   case(12) ! Try Samurai first, use PJFry is samurai fails
      call samurai_reduce(real(scale2, ki_sam), tot, totr, samurai_ok)
      if(samurai_ok) then[%
               @if generate_lo_diagrams %]
         samplitude(:) = 2.0_ki * real(tot(:), ki)[%
               @else %]
         samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
               @end @if %]
         ok = .true.
      else
         call reconstruct_golem95(coeffs)[%
               @if generate_lo_diagrams %]
         do ep=0,2
            pjres = contract_pjfry(coeffs, scale2, ep)
            samplitude(-ep) = 2.0_ki * real(pjres, ki)
         end do[%
               @else %]
         do ep=0,2
            pjres = contract_pjfry(coeffs, scale2, ep)
            samplitude(-ep) = cmplx(real(pjres, ki_pjf), aimag(pjres), ki)
         end do[%
               @end @if %]
         ok = .true.
      end if
   case(14) ! Tensorial Reconstruction + Samurai on numetens
           ! + PJFry on failure
      call reconstruct_golem95(coeffs)
      global_coeffs => coeffs
      call reduce_numetens(real(scale2, ki_sam), tot, totr, samurai_ok)
      if(samurai_ok) then[%
               @if generate_lo_diagrams %]
         samplitude(:) = 2.0_ki * real(tot(:), ki)[%
               @else %]
         samplitude(:) = cmplx(real(tot(:), ki_sam), aimag(tot(:)), ki)[%
               @end @if %]
         ok = .true.
      else[%
               @if generate_lo_diagrams %]
         do ep=0,2
            pjres = contract_pjfry(coeffs, scale2, ep)
            samplitude(-ep) = 2.0_ki * real(pjres, ki)
         end do[%
               @else %]
         do ep=0,2
            pjres = contract_pjfry(coeffs, scale2, ep)
            samplitude(-ep) = cmplx(real(pjres, ki_pjf), aimag(pjres), ki)
         end do[%
               @end @if %]
         ok = .true.
      end if[%
            @end @if %][%
         @end @if %][%
      @end @if %]
   case default
      print*, "Your current choice of reduction_interoperation is", &
            & reduction_interoperation
      print*, "This choice is not valid for your current setup."
      print*, "* This code was generated [%
      @if extension samurai %]with[%
      @else %]without[%
      @end @if %] support for Samurai."
      print*, "* This code was generated [%
      @if extension ninja %]with[%
      @else %]without[%
      @end @if %] support for Ninja."
      print*, "* This code was generated [%
      @if extension golem95 %]with[%
      @else %]without[%
      @end @if %] support for Golem95."[%
      @if extension golem95 %]
      print*, "* This code was generated [%
         @if extension pjfry %]with[%
         @else %]without[%
         @end @if %] support for PJFry."[%
      @else %][%
         @if extension pjfry %]
      print*, "* PJFry cannot be used without the extension 'golem95'"[%
         @end @if %][%
      @end @if %]
   end select

   if(debug_nlo_diagrams) then[%
      @if generate_lo_diagrams %]
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-finite' value='", samplitude(0), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-single' value='", samplitude(-1), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-double' value='", samplitude(-2), "'/>"[%
      @else %]
      write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
         & "<result kind='nlo-finite' re='", real(samplitude(0), ki), &
         & "' im='", aimag(samplitude(0)), "'/>"
      write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
         & "<result kind='nlo-single' re='", real(samplitude(-1), ki), &
         & "' im='", aimag(samplitude(-1)), "'/>"
      write(logfile,'(A30,E24.16,A6,E24.16,A3)') &
         & "<result kind='nlo-double' re='", real(samplitude(-2), ki), &
         & "' im='", aimag(samplitude(-2)), "'/>"[%
      @end @if %]
      if(ok) then
         write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
      else
         write(logfile,'(A29)') "<flag name='ok' status='no'/>"
      end if
      write(logfile,*) "</diagram-group>"
   end if
end subroutine evaluate_group[% grp %]
!---#] subroutine evaluate_group[% grp %]:[%
   @end @for groups %][%
@end @select %]
end module [% process_name asprefix=\_ %]amplitude
