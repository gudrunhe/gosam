[%' vim: sw=3:syntax=golem
   Template file for <process_dir>/groups.f90

   This template should be processed by
   golem.templates.Kinematics.KinematicsTemplate
'%]module     [% process_name asprefix=\_ %]groups[%
@if extension samurai %]
   use precision, only: ki_sam => ki
   use madds[%
@end @if %][%
@if extension golem95 %]
   use precision_golem, only: ki_gol => ki
   use tens_rec[%
@end @if golem95 %]
   use [% process_name asprefix=\_%]config, only: ki [% @if extension golem95
   %][% @if extension samurai %], reduction_interoperation, samurai_scalar [% 
   @end @if %][% @end @if %]
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

   public :: tensrec_info_group[% grp %][%
      @if extension samurai %]
   type(tensrec_info_group[% grp %]), pointer, public :: coeffs_group[% grp %]
   public :: reduce_numetens_group[% grp %][%
      @end @if %]
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
   @if extension pjfry %][%
      @for groups var=grp %][%
         @if is_first %]

   interface contract_pjfry[%
         @end @if %]
      module procedure fry_tensor_coefficients_group_[% grp %][%
         @if is_last %]
   end interface
   
   public :: contract_pjfry[%
         @end @if %][%
      @end @for %][%
   @end @if extension pjfry %][%
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
   use [% process_name asprefix=\_ %]config, only: debug_nlo_diagrams, logfile
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
   use [% process_name asprefix=\_ %]model
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
            @if is_first %][%
            @if diagsum %]+ [%
            @else %][% diagram_sign %][%
            @end @if %][%
            @else %]amp [%
            @if diagsum %]+ [%
            @else %][% diagram_sign %] [%
            @end @if %][%
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
         @end @for diagrams %][%
    @if extension samurai %]
   if ((reduction_interoperation /= 1) .and. (samurai_scalar == 3) ) then
        call tear_down_golem95();
   end if[%
    @end @if %]

   100 format (A30,E24.16,A6,E24.16,A3)
end function contract_tensor_coefficients_group_[% grp %]
!-----#] function contract_tensor_coefficients_group_[% grp %]:[%
         @if extension pjfry %]
!-----#[ function fry_tensor_coefficients_group_[% grp %]:
function     fry_tensor_coefficients_group_[% grp %](coeffs, scale2, ep) result(amp)
   use array, only: packb
   use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
   use [% process_name asprefix=\_ %]pjfry_comb
   use [% process_name asprefix=\_ %]pjfry95pg
   use [% process_name asprefix=\_ %]config, only: debug_nlo_diagrams, logfile
   use [% process_name asprefix=\_ %]kinematics, only:&
   & [%
         @for mandelstam non-zero sym_prefix=es %][% 
            @if is_first %][% @else %],[%
              @if eval index % 8 .eq. 7 %]&
   &[%
              @end @if%] [% @end @if %][%symbol%][%
         @end @for mandelstam %][%
         @for repeat num_legs shift=1 %],[%
            @if is_first %]&
   &[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model
   implicit none
   type(tensrec_info_group[% grp %]), intent(in) :: coeffs
   real(ki), intent(in) :: scale2
   integer, intent(in) :: ep
   complex(ki) :: amp, dbg_amp

   integer :: b_set
   real(ki_gol), dimension([% ls %],0:3) :: rmomenta

   call pginitgolem95([% ls %])[%

         @for smat group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es 
              upper diagonal %]
   call pgsetmat([%rowindex%],[%colindex%], [%
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
            @end @for %], ki_pjf))[%
         @end @for %]
   call pgsetmusq(real(scale2, ki_pjf))
   call pgpreparesmatrix()
   b_ref = b_ref[%ls%][%

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
      end if
      b_set = [%
            @if eval ( .len.  ( .str. pinches ) ) .eq. 0 %]0[%
            @else %]packb((/[% pinches %]/))[%
            @end @if %]

      amp = [%
            @if is_first %][%
            @if diagsum %]+ [%
            @else %][% diagram_sign %][%
            @end @if %][%
            @else %]amp [%
            @if diagsum %]+ [%
            @else %][% diagram_sign %] [%
            @end @if %][%
            @end @if %][%
            @if is_nf %] [% 
            @if diagsum %][%
            @else %] real(Nfrat, ki_gol) * [% @end @if %][%
            @end @if %]([%
            @if eval rank .eq. 0 %]coeffs%coeffs_[% DIAG %] * pga[%
                loopsize diagram=DIAG %]0(b_set, ep)[%
            @else %]contract[% loopsize diagram=DIAG %]_[% rank 
      %](coeffs%coeffs_[% DIAG %], rmomenta, b_set, ep)[%
            @end @if %][%
            @select r2 @case implicit %][%
               @select loopsize diagram=DIAG
               @case 2 3 4 %][%
                  @if eval rank .gt. 1 %]&
       &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s1(coeffs%coeffs_[% DIAG %]s1, rmomenta, b_set, ep)[%
               @end @if %][%
                  @if eval rank .gt. 3 %]&
       &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s2(coeffs%coeffs_[% DIAG %]s2, rmomenta, b_set, ep)[%
                  @end @if %][%
               @case 5 %][%
                  @if eval rank .gt. 5 %]&
       &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s1(coeffs%coeffs_[% DIAG %]s1, rmomenta, b_set, ep)
       &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s2(coeffs%coeffs_[% DIAG %]s2, rmomenta, b_set, ep)&
             &     + contract[% loopsize diagram=DIAG %]_[% rank
      %]s1(coeffs%coeffs_[% DIAG %]s3, rmomenta, b_set, ep)[%
                  @end @if %][%
               @end @select %][%
            @end @select %])
      if(debug_nlo_diagrams) then[%
            @if is_first %]
         dbg_amp = amp[%
            @else %]
         dbg_amp = amp - dbg_amp[%
            @end @if %]
         select case(ep)
         case (0)
            write(logfile,100) &
            & "<result kind='nlo-finite' re='", real(dbg_amp, ki), &
            & "' im='", aimag(dbg_amp), "'/>"
         case (1)
            write(logfile,100) &
            & "<result kind='nlo-single' re='", real(dbg_amp, ki), &
            & "' im='", aimag(dbg_amp), "'/>"
         case (2)
            write(logfile,100) &
            & "<result kind='nlo-double' re='", real(dbg_amp, ki), &
            & "' im='", aimag(dbg_amp), "'/>"
         end select
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
end function fry_tensor_coefficients_group_[% grp %]
!-----#] function fry_tensor_coefficients_group_[% grp %]:[%
         @end @if %][%
      @end @with %][%
   @end @for groups %]
!---#] contract tensor coefficients golem95:[%
   @if extension samurai %]
!---#[ numetens golem95:[%
   @for groups var=grp %][%
      @with eval loopsize group=grp result=ls %]
!-----#[ function numetens_group[% grp %]:
function     numetens_group[% grp %](icut, Q, mu2) result(num)
   use tens_rec[%
         @for repeat num_legs shift=1 %][%
            @if is_first %]
   use [% process_name asprefix=\_ %]kinematics, only:[%
            @else %],[%
            @end @if %] k[% $_ %][%
         @end @for %]
   use [% process_name asprefix=\_ %]model
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
   complex(ki_gol), dimension(0:3) :: Qg
   real(ki_gol), dimension(0:3) :: R
   complex(ki_gol) :: Q2
   complex(ki_sam) :: diag[%
         @for propagators group=grp %], denom[% $_ %][%
         @end @for %]

   nonzero(:) = .true.
   Qg(0) = Q(4)
   Qg(1:3) = Q(1:3)
   Q2 = Qg(0)*Qg(0) - Qg(1)*Qg(1) - Qg(2)*Qg(2) - Qg(3)*Qg(3) - mu2

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
                           @else %] - [%mass%]*[%
                              @if eval width .eq. 0 %][%mass%][%
                              @else %]cmplx([%mass%], -[%width%], ki_sam)[%
                              @end @if %][%
                           @end @if %][%
                        @else %]
      R = real([% momentum %], ki_gol)
      denom[% propidx %] = Q2 + (Qg(0) + Qg(0) + R(0))*R(0) &
                 &    - (Qg(1) + Qg(1) + R(1))*R(1) &
                 &    - (Qg(2) + Qg(2) + R(2))*R(2) &
                 &    - (Qg(3) + Qg(3) + R(3))*R(3)[%
                           @if eval mass .eq. 0 %][%
                           @else %]&
                 &    - [%mass%]*[%
                              @if eval width .eq. 0 %][%mass%][%
                              @else %]cmplx([%mass%], -[%width%], ki_sam)[%
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
               @else %] - [%mass%]*[%
                  @if eval width .eq. 0 %][%mass%][%
                  @else %]cmplx([%mass%], -[%width%], ki_sam)[%
                  @end @if %][%
               @end @if %][%
            @else %]
      R = real([% momentum %], ki_gol)
      denom[% $_ %] = Q2 + (Qg(0) + Qg(0) + R(0))*R(0) &
                 &    - (Qg(1) + Qg(1) + R(1))*R(1) &
                 &    - (Qg(2) + Qg(2) + R(2))*R(2) &
                 &    - (Qg(3) + Qg(3) + R(3))*R(3)[%
               @if eval mass .eq. 0 %][%
               @else %]&
                 &    - [%mass%]*[%
                  @if eval width .eq. 0 %][%mass%][%
                  @else %]cmplx([%mass%],[%width%], ki_sam)[%
                  @end @if %][%
               @end @if %][%
            @end @if %][%
         @end @for %]
   end select
   
   num = (0.0_ki_sam, 0.0_ki_sam)[%

         @for diagrams group=grp var=DIAG idxshift=1 %]
   !-------#[ Diagram [% DIAG %]:
   if(nonzero([% index %])[%
            @if use_flags_1 %].and.evaluate_virt_diagram([% DIAG %])[%
            @end @if %]) then
      diag = [%
            @if eval rank .eq. 0 %]coeffs_group[% grp %]%coeffs_[% DIAG %][%
            @else %]ctenseval[% rank 
      %](Qg, coeffs_group[% grp %]%coeffs_[% DIAG %])[%
            @end @if %][%
            @select r2 @case implicit %][%
               @select loopsize diagram=DIAG
               @case 2 3 4 %][%
                  @if eval rank .gt. 1 %][%
                     @if eval rank .eq. 2 %]&
       &     + mu2 * coeffs_group[% grp %]%coeffs_[% DIAG %]s1[%
                     @else %]&
       &     + mu2 * ctenseval[% eval rank - 2 
      %](Qg, coeffs_group[% grp %]%coeffs_[% DIAG %]s1)[%
                     @end @if %][%
                  @end @if %][%
                  @if eval rank .gt. 3 %]&
       &     + mu2 * mu2 * coeffs_group[% grp %]%coeffs_[% DIAG %]s2%c0[%
                  @end @if %][%
               @end @select %][%
            @end @select %][%
            @for elements pinches %][%
               @if is_first %]
      diag = diag[%
               @end @if %] * denom[% $_ %][%
            @end @for %]
      num = num [% @if diagsum %]+ [% @else %] [% diagram_sign %] [% @end @if %][%
            @if is_nf %]real(Nfrat, ki_sam) * [%
            @end @if %]diag
   end if
   !-------#] Diagram [% DIAG %]:[%
         @end @for diagrams %]
end function numetens_group[% grp %]
!-----#] function numetens_group[% grp %]:
!-----#[ subroutine reduce_numetens_group[% grp %]:
subroutine     reduce_numetens_group[% grp %](scale2,tot,totr,ok)
   use msamurai, only: [%
   @if version_newer samurai.version 2.8 %]samurai
   use mgetkin, only: s_mat[%
   @else %][%
    @if version_newer samurai.version 2.0 %]samurai_rm, samurai_cm[%
    @else %]samurai[%
    @end @if %][%
    @if version_newer samurai.version 2.1 %]
   use madds, only: s_mat[%
   @end @if %][% @end @if %]
   use options, only: samurai_out => iout
   use [% process_name asprefix=\_ %]config, only: samurai_group_numerators, &
      samurai_istop, samurai_verbosity
   use [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_ %]model
   use [% process_name asprefix=\_ %]globalsl1, only: epspow
   implicit none
   real(ki_sam), intent(in) :: scale2
   complex(ki_sam), dimension(-2:0), intent(out) :: tot
   complex(ki_sam), intent(out) :: totr
   logical, intent(out) :: ok

   integer, parameter :: effective_group_rank = [% rank %][%
   @if complex_mass_needed group=grp %]
   complex(ki_sam)[%
   @else %]
   real(ki_sam)[%
   @end @if %], dimension([% loopsize group=grp %]) :: msq
   real(ki_sam), dimension([% loopsize group=grp %],4) :: Vi[%

   @for propagators group=grp %]
   msq([% $_ %]) = [% 
      @if eval mass .eq. 0 %]0.0_ki_sam[%
      @else %][%
         @if eval width .eq. 0 %]real([% mass %]*[% mass %], ki)[%
         @else %]real([%mass%], ki_sam)*cmplx([%mass%],-[%width%],ki_sam)[%
         @end @if %][%
      @end @if %]
   Vi([% $_ %],(/4,1,2,3/)) = real([% momentum %], ki_sam)[%
   @end @for %][%
   @if version_newer samurai.version 2.1 %]
   !-----------#[ initialize invariants:
   allocate(s_mat([% loopsize group=grp %], [% loopsize group=grp %]))[%
      @for smat upper diagonal
           group=grp powfmt=%s**%d prodfmt=%s*%s prefix=es %]
   s_mat([%rowindex%], [%colindex%]) = [%
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
   s_mat([% colindex %], [% rowindex %]) = s_mat([% 
                                        rowindex %], [% colindex %])[%
            @end @if %][%
         @end @for %]
   !-----------#] initialize invariants:[%
   @end @if %]

   if(samurai_verbosity > 0) then
      write(samurai_out,*) "[GoSam] numetens_group[% grp %]"
      write(samurai_out,*) "[GoSam] epspow=", epspow
   end if
   call samurai[% @if version_newer samurai.version 2.8 %][% @else %][%
   @if version_newer samurai.version 2.1 %][%
      @if complex_mass_needed group=grp %]_cm[% @else %]_rm[%
      @end @if %][% @end @if%][%
   @end @if %](numetens_group[% grp %], tot, totr, Vi, [%
   @if version_newer samurai.version 2.8 %][% @if complex_mass_needed group=grp %]msq, [% @else
   %]cmplx(msq,0._ki_sam,ki_sam), [% @end @if %][% @else
   %]msq, [% @end @if %][%
      loopsize group=grp %], &
      & effective_group_rank, samurai_istop, scale2, ok)[%
   @if version_newer samurai.version 2.1 %]
   !-----------#[ deallocate invariants:
   deallocate(s_mat)
   !-----------#] deallocate invariants:[%
   @end @if %]
end subroutine reduce_numetens_group[% grp %]
!-----#] subroutine reduce_numetens_group[% grp %]:[%
      @end @with %][%
   @end @for groups %]
!---#] numetens golem95:[%
   @end @if extension samurai %]
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
   @end @if extension ninja %][%
@if extension pjfry %]
function pga10(b_set, ep)
   use [% process_name asprefix=\_ %]precision_pjfry, only: ki_pjf
   use [% process_name asprefix=\_ %]pjfry95pg
   use array, only: pminus, unpackb
   use [% process_name asprefix=\_ %]pjfry_comb, only: b_ref
   implicit none
   
   integer, intent(in) :: b_set, ep
   complex(ki_pjf) :: pga10

   real(ki_pjf) :: musq, msq, lg
   integer :: b_pin
   integer, dimension(1) :: s_pin

   b_pin = pminus(b_ref, b_set)
   s_pin = unpackb(b_pin, 1)
   msq = - 0.5_ki_pjf * pggetmat(s_pin(1), s_pin(1))

   if (msq.eq.0.0_ki_pjf) then
      pga10 = (0.0_ki_pjf, 0.0_ki_pjf)
      return
   end if

   select case(ep)
   case(0)
      musq = pggetmusq()
      lg = log(musq/msq)
      pga10 = msq * (1.0_ki_pjf + lg)
   case(1)
      pga10 = msq
   case default
      pga10 = (0.0_ki_pjf, 0.0_ki_pjf)
   end select
end function pga10[%
@end @if %]
end module [% process_name asprefix=\_ %]groups
