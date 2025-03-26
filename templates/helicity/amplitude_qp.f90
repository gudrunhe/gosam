[% ' vim: ts=3:sw=3:expandtab:syntax=golem
 %]module    [% process_name asprefix=\_ %]amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki => ki_qp, &
       & reduction_interoperation
   use [% process_name asprefix=\_ %]color_qp, only: numcs[%
@if generate_nlo_virt %][%
@if helsum %][%
@else %]
   use [% process_name asprefix=\_ %]groups[%
      @if extension golem95 %]
   use precision_golem, only: ki_gol => ki
   use [% process_name asprefix=\_ %]golem95[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h[% helicity %][%
      @end @if %][%
      @if extension ninja %]
   use quadninjago_module, only: ki_nin
   use [% process_name asprefix=\_ %]ninja[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h[% helicity %]_qp[%
      @end @if %][%
@end @if %][%
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
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: include_eps_terms, include_eps2_terms, &
      & logfile, debug_nlo_diagrams
      use [% process_name asprefix=\_
         %]globalsl1_qp, only:[%
@if generate_lo_diagrams %] amp0,[%
@else %] col0,[%
@end @if %]perm, use_perm, epspow
      use [% process_name asprefix=\_ %]globalsh[%helicity%]_qp, &
     & only: init_lo, rat2[%
@if generate_nlo_virt %][%
@if helsum %][%
@else %][%
      @for groups var=grp %][%
         @for diagrams group=grp %]
      use [% process_name asprefix=\_
      %]abbrevd[%$_%][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h[%helicity%]_qp, only: init_abbrevd[%$_%] => init_abbrev[%
         @end @for %][%
      @end @for %][%
@end @if %][%
@end @if %][%
@if generate_lo_diagrams %]
      use [% process_name asprefix=\_
      %]diagramsh[%helicity%]l0[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp, only: amplitudel0 => amplitude[%
@end @if %]
      use [% process_name asprefix=\_ %]groups
      implicit none
      real(ki), intent(in) :: scale2
      logical, intent(out) :: ok
      real(ki), intent(out) :: rational2[%
@if generate_lo_diagrams %]
      complex(ki), dimension(numcs), intent(in), optional :: opt_amp0[%
@else %]
      integer, intent(in) :: the_col0[%
@end @if %]
      integer, dimension(numcs), intent(in), optional :: opt_perm
      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(-2:0) :: samplitude

      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(-2:0) :: acc
      [% @if generate_lo_diagrams %]real(ki)[% @else 
      %]complex(ki)[% @end @if %], dimension(0:2,-2:0) :: samp_part

      logical :: acc_ok

      ok = .true.
      rational2 = 0.0_ki

      samplitude(:) = 0.0_ki[%
@if generate_lo_diagrams %]
      if (present(opt_amp0)) then
         amp0[% @if helsum %](:,[%helicity%])[%@end @if%] = opt_amp0
      else
         amp0[% @if helsum %](:,[%helicity%])[%@end @if%] = amplitudel0()
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
@if helsum %][%
@else %][%
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
@else %]
      samplitude(:) = (0.0_ki, 0.0_ki)[%
@end @if helsum %][%
@end @if generate_nlo_virt %]
   end function samplitude
   !---#] function samplitude:[%
   @for groups var=grp %][%
@if helsum %][%
@else %][% 'evaluate group only for sum' %]
!---#[ subroutine evaluate_group[% grp %]:
subroutine     evaluate_group[% grp %](scale2,samplitude,ok)
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
      & logfile, debug_nlo_diagrams
   use [% process_name asprefix=\_ %]globalsl1_qp, only: epspow[%
      @if extension golem95 %]
   use parametre, only: mu2_scale_par
   use form_factor_type, only: form_factor
   use [% process_name asprefix=\_ %]golem95[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h[% helicity
       %], only: reconstruct_golem95 => reconstruct_group
   use [% process_name asprefix=\_ %]groups, only: contract_golem95[%
      @end @if %][%
      @if extension ninja %]
   use [% process_name asprefix=\_ %]ninja[% @if enable_truncation_orders %]_[% trnco %][% @end @if %]h[% helicity
      %]_qp, only: ninja_reduce => ninja_reduce_group[% grp %][%
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
      @end @if %][% @if extension ninja %]
   complex(ki_nin), dimension(-2:0) :: tot
   complex(ki_nin) :: totr[%
      @end @if %]

   if(debug_nlo_diagrams) then
      write(logfile,*) "<diagram-group index='[% grp %]'>"
      write(logfile,*) "<param name='epspow' value='", epspow, "'/>"
   end if
   select case(reduction_interoperation)[%
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
   case(4) ! use QuadNinja only
      call ninja_reduce(real(scale2, ki_nin), tot, totr, ok)[%
         @if generate_lo_diagrams %]
      samplitude(:) = 2.0_ki * real(tot(:), ki)[%
         @else %]
      samplitude(:) = cmplx(real(tot(:), ki_nin), aimag(tot(:)), ki)[%
         @end @if %][%
      @end @if %]
   case default
      print*, "Your current choice of reduction_interoperation is", &
            & reduction_interoperation
      print*, "This choice is not valid for your current setup."
      print*, "* This code was generated [%
      @if extension ninja %]with[%
      @else %]without[%
      @end @if %] support for Ninja."
      print*, "* This code was generated [%
      @if extension golem95 %]with[%
      @else %]without[%
      @end @if %] support for Golem95."
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
@end @if %][%
   @end @for groups %]
end module [% process_name asprefix=\_ %]amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]_qp
