[%' vim: sw=3:syntax=golem
   Template file for <process_dir>/groups.f90

   This template should be processed by
   golem.templates.Kinematics.KinematicsTemplate
'%]module     [% process_name asprefix=\_ %]groups[%
@if extension golem95 %]
   use precision_golem, only: ki_gol => ki
   use tens_rec[%
@end @if golem95 %]
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki [% @if extension golem95
   %][% @end @if %]
   implicit none
   save

   private[%

@if extension golem95 %]
!---#[ tensor coefficients for golem95:[%
   @for groups var=grp %]
   !-----#[ tensor coefficients group [% grp %]:
   type tensrec_info_group[% grp %][%
      @for diagrams group=grp var=DIAG rank=diag_rank %][%
         @if eval diag_rank .eq. 0 %]
      complex(ki_gol)[%
         @else %]
      type(coeff_type_[% diag_rank %])[%
         @end @if %] :: coeffs_[% DIAG %][%
         @select r2 @case implicit %][%
            @with eval loopsize diagram=DIAG result=DIAGLS %][%
               @if eval DIAGLS .lt. 5 %][%
                  @if eval diag_rank .gt. 1 %][%
                     @if eval diag_rank .eq. 2 %]
      complex(ki_gol)[%
                     @else %]
      type(coeff_type_[% eval diag_rank - 2 %])[%
                     @end @if %] :: coeffs_[% DIAG %]s1[%
                  @end @if %][%
                  @if eval diag_rank .gt. 3 %]
      type(coeff_type_[% eval diag_rank - 2 %]) :: coeffs_[% DIAG %]s2[%
                  @end @if %][%
               @end @if %][%
               @if eval DIAGLS .eq. 5 %][%
                  @if eval diag_rank .gt. 5 %]
      type(coeff_type_[% eval diag_rank - 2 %]) :: coeffs_[% DIAG %]s1
      type(coeff_type_[% eval diag_rank - 2 %]) :: coeffs_[% DIAG %]s2
      type(coeff_type_[% eval diag_rank - 2 %]) :: coeffs_[% DIAG %]s3[%
                  @end @if %][%
               @end @if %][%
            @end @with %][%
         @end @select %][%
      @end @for diagrams %]
   end type

   public :: tensrec_info_group[% grp %]
   !-----#] tensor coefficients group [% grp %]:[%
   @end @for groups %]
!---#] tensor coefficients for golem95:[%
@end @if %][%

@if extension golem95 %]
   integer :: prev_ls = -1[%
   @for groups var=grp %][%
      @if is_first %]

   interface contract_golem95[%
      @end @if %]
      module procedure contract_tensor_coefficients_group_[% grp %][%
      @if is_last %]
   end interface

   public :: contract_golem95[%
      @end @if %][%
   @end @for %]
   public :: tear_down_golem95[%
@end @if %][%

@if use_flags_0 %]

   ! Flags for selecting diagrams at LO
   type lo_flags[%
   @for elements lo_flags delimiter=\  %]
      logical, public :: eval[% $_ assuffix=\_ %] = .true.[%
   @end @for %]
   end type

   public :: lo_flags

   logical, public, dimension([%
      min_diagram_0 %]:[% max_diagram_0 %]) :: evaluate_lo_diagram = .true.[%
@end @if %][%
@if use_flags_1 %]

   ! Flags for selecting diagrams at NLO
   type virt_flags[%
   @for elements nlo_flags delimiter=\  %]
      logical, public :: eval[% $_ assuffix=\_ %] = .true.[%
   @end @for %]
   end type

   public :: virt_flags

   logical, public, dimension(0:[%
         count groups %]-1) :: evaluate_virt_group = .true.
   logical, public, dimension([%
      min_diagram_1%]:[% max_diagram_1 %]) :: evaluate_virt_diagram = .true.[%
@end @if %][%

@if use_flags_0 %][%
   @if use_flags_1 %]

   interface update_flags
      module procedure update_lo_flags
      module procedure update_virt_flags
   end interface

   public :: update_flags
   private :: update_lo_flags, update_virt_flags[%
   @else %]

   interface update_flags
      module procedure update_lo_flags
   end interface

   public :: update_flags
   private :: update_lo_flags[%
   @end @if %][%
@else %][%
   @if use_flags_1 %]

   interface update_flags
      module procedure update_virt_flags
   end interface

   public :: update_flags
   private :: update_virt_flags[%
   @end @if %][%
@end @if %][%
@if extension ninja %]
   public :: ninja_exit[%
@if extension quadruple %]
   public :: quadninja_exit[%
@end @if %][%
@end @if %]
contains[%

@if use_flags_0 %]
!---#[ subroutine update_lo_flags:
subroutine     update_lo_flags(flags)
   implicit none
   type(lo_flags), intent(in) :: flags[%
   @for repeat min_diagram_0 max_diagram_0 inclusive=.true. var=DIAG%][%
      @for elements lo_flags diagram=DIAG delimiter=\ %][%
         @if is_first %]
   evaluate_lo_diagram([%DIAG%]) = [%
         @else %].or.[%
         @end @if %]flags%eval[% $_ assuffix=\_ %][%
      @end @for %][%
   @end @for range %]
end subroutine update_lo_flags
!---#] subroutine update_lo_flags:[%
@end @if use_flags_0 %][%

@if use_flags_1 %]
!---#[ subroutine update_virt_flags:
subroutine     update_virt_flags(flags)
   implicit none
   type(virt_flags), intent(in) :: flags[%
   @for groups var=grp %]
   !---#[ group [%grp%]:[%

      @for elements nlo_flags group=grp delimiter=\  %][%
         @if is_first %]
   evaluate_virt_group([%grp%]) = [%
         @else %].or.[%
         @end @if %]flags%eval[% $_ assuffix=\_%][%
      @end @for %][%


      @for diagrams group=grp var=DIAG idxshift=1 %][%
         @for elements flags delimiter=\  %][%
            @if is_first %]
   evaluate_virt_diagram([%DIAG%]) = [%
            @else %].or.[%
            @end @if %]flags%eval[% $_ assuffix=\_%][%
         @end @for %][%
      @end @for diagrams %]
   !---#] group [%grp%]:[%
   @end @for groups%]
end subroutine update_virt_flags
!---#] subroutine update_lo_flags:[%
@end @if use_flags_1 %][%

@if extension golem95 %]
!---#[ contract tensor coefficients golem95:[%
   @for groups var=grp %][%
      @with eval loopsize group=grp result=ls %]
!-----#[ function contract_tensor_coefficients_group_[% grp %]:
function     contract_tensor_coefficients_group_[% grp %](coeffs) result(amp)
   use matrice_s, only: allocation_s, deallocation_s, s_mat, set_ref, &
                      & s_mat_c, b_ref, preparesmatrix
   use parametre, only: rmass_or_cmass_par, cmass
   use cache, only: allocate_cache, clear_cache, reset_cache
   use array, only: packb
   use tens_comb[%
      @for repeat ls shift=1 %]
   use form_factor_[% $_ %]p, only: a[% $_ %]0[%
      @end @for %]
   use form_factor_type, only: form_factor, operator(+), operator(-)
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: debug_nlo_diagrams, logfile
   use [% process_name asprefix=\_ %]kinematics, only:[%
      @for repeat num_legs shift=1 %][%
         @if is_first %] [% @else %], [%
         @end @if %]k[% $_ %][%
      @end @for %][%
      @for mandelstam non-zero sym_prefix=es %], [%
         @if eval index % 8 .eq. 0 %]&
   & [%
         @end @if%][%symbol%][%
      @end @for mandelstam %]
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model
   implicit none
   type(tensrec_info_group[% grp %]), intent(in) :: coeffs
   type(form_factor) :: amp, dbg_amp

   integer :: b_set
   real(ki_gol), dimension([% ls %],0:3) :: rmomenta
   logical :: ev_diagram

   if(prev_ls.ne.[% ls %]) then
      if(prev_ls > 0) then
         !------#[ call sequence of exitgolem95():
         rmass_or_cmass_par = cmass
         nullify(s_mat)
         call deallocation_s()
         call clear_cache()
         !------#] call sequence of exitgolem95():
      end if

      !------#[ call sequence of initgolem95():
      rmass_or_cmass_par = cmass
      call allocation_s([% ls %])
      set_ref = (/[%
         @for repeat ls shift=1 %][%
            @if is_first %][% @else %], [% @end @if %][% $_ %][%
         @end @for %]/)
      b_ref = packb(set_ref)
      call allocate_cache([% ls %])
      s_mat => s_mat_c
      !------#] call sequence of initgolem95():
      prev_ls = [% ls %]
   !else
   !   reset_cache() is called by preparesmatrix()
   !   call reset_cache()
   end if[%

         @for smat upper diagonal
              group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es %]
   s_mat([%rowindex%],[%colindex%])=[%
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
            @end @for %], ki_gol)[%

            @if eval rowindex .ne. colindex %]
   s_mat([% colindex %],[% rowindex %])=s_mat([%
                                        rowindex %],[% colindex %])[%
            @end @if %][%

         @end @for %]
   call preparesmatrix()[%

         @for propagators group=grp prefix=k %]
   rmomenta([% $_ %],:) = [%
            @if eval momentum .eq. 0 %]0.0_ki_gol[%
            @else %]real([% momentum %], ki_gol)[%
            @end @if %][%
         @end @for %][%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:[%
            @if use_flags_1 %]
   if(evaluate_virt_diagram([% DIAG %])) then[%
            @end @if %]
      if(debug_nlo_diagrams) then
         write(logfile,*) "<diagram index='[% DIAG %]'>"
         dbg_amp = [%
         @if is_first %]0.0_ki_gol[%
         @else %]amp[%
         @end @if %]
      end if
      b_set = [%
            @if eval ( .len.  ( .str. pinches ) ) .eq. 0 %]0[%
            @else %]packb((/[% pinches %]/))[%
            @end @if %]

      amp = [%
            @if is_first %] + [%
            @else %]amp + [%
            @end @if %][%
            @if is_nf %] [%
            @if diagsum %][%
            @else %] real(Nfrat, ki_gol) * [% @end @if %][%
            @end @if %]([%
            @if eval rank .eq. 0 %]coeffs%coeffs_[% DIAG %] * a[%
                loopsize diagram=DIAG %]0(b_set)[%
            @else %]contract[% loopsize diagram=DIAG %]_[% rank
      %](coeffs%coeffs_[% DIAG %], rmomenta, b_set)[%
            @end @if %][%
            @select r2 @case implicit %][%
               @select loopsize diagram=DIAG
               @case 2 3 4 %][%
                  @if eval rank .gt. 1 %]&
          &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s1(coeffs%coeffs_[% DIAG %]s1, rmomenta, b_set)[%
                  @end @if %][%
                  @if eval rank .gt. 3 %]&
          &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s2(coeffs%coeffs_[% DIAG %]s2, rmomenta, b_set)[%
                  @end @if %][%
               @case 5 %][%
                  @if eval rank .gt. 5 %]&
          &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s1(coeffs%coeffs_[% DIAG %]s1, rmomenta, b_set)&
          &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s2(coeffs%coeffs_[% DIAG %]s2, rmomenta, b_set)&
          &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s3(coeffs%coeffs_[% DIAG %]s3, rmomenta, b_set)[%
                  @end @if %][%
               @end @select %][%
            @end @select %])
      if(debug_nlo_diagrams) then
         dbg_amp = amp - dbg_amp
         write(logfile,100) &
            & "<result kind='nlo-finite' re='", real(dbg_amp%C, ki), &
            & "' im='", aimag(dbg_amp%C), "'/>"
         write(logfile,100) &
            & "<result kind='nlo-single' re='", real(dbg_amp%B, ki), &
            & "' im='", aimag(dbg_amp%B), "'/>"
         write(logfile,100) &
            & "<result kind='nlo-double' re='", real(dbg_amp%A, ki), &
            & "' im='", aimag(dbg_amp%A), "'/>"
         write(logfile,*) "</diagram>"
      end if[%
           @if use_flags_1 %][%
              @if is_first %]
   else
      amp = 0.0_ki[%
              @end @if %]
   end if[%
           @end @if %]
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]

   100 format (A30,E24.16,A6,E24.16,A3)
end function contract_tensor_coefficients_group_[% grp %]
!-----#] function contract_tensor_coefficients_group_[% grp %]:[%
      @end @with %][%
   @end @for groups %]
!---#] contract tensor coefficients golem95:
!---#[ subroutine tear_down_golem95:
subroutine     tear_down_golem95()
   use matrice_s, only: deallocation_s, s_mat
   use parametre, only: rmass_or_cmass_par, cmass
   use cache, only: clear_cache
   implicit none
   if(prev_ls.gt.0) then
      !------#[ call sequence of exitgolem95():
      rmass_or_cmass_par = cmass
      nullify(s_mat)
      call deallocation_s()
      call clear_cache()
      !------#] call sequence of exitgolem95():
      prev_ls = -1
   end if
end subroutine tear_down_golem95
!---#] subroutine tear_down_golem95:[%
@end @if extension golem95 %][%
   @if extension ninja %]
!---#[ subroutine ninja_exit:
subroutine ninja_exit()
  use ninjago_module, only: ninja_clear_integral_cache
  implicit none
  !------#[ call ninja_clear_integral_cache():
  call ninja_clear_integral_cache()
  !------#] call ninja_clear_integral_cache():
end subroutine ninja_exit
!---#] subroutine ninja_exit:[%
   @if extension quadruple %]
!---#[ subroutine quadninja_exit:
subroutine quadninja_exit()
  use quadninjago_module, only: quadninja_clear_integral_cache
  implicit none
  !------#[ call quadninja_clear_integral_cache():
  call quadninja_clear_integral_cache()
  !------#] call quadninja_clear_integral_cache():
end subroutine quadninja_exit
!---#] subroutine quadninja_exit:[%
   @end @if extension quadruple %][%
   @end @if extension ninja %]
end module [% process_name asprefix=\_ %]groups
