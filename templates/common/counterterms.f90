[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]counterterms
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki
   implicit none
   save

   private

public :: counterterm_alphas, counterterm_gluonwf, counterterm_mqwf, & 
   & counterterm_yukawa_OS, counterterm_yukawa_MSbar, counterterm_mass_OS,& 
   & counterterm_fr5

contains
 
!---#[ function counterterm_alphas:
   function counterterm_alphas(scale2) result(ct)
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model
      use [% process_name asprefix=\_ %]kinematics, only: lo_qcd_couplings
      use [% process_name asprefix=\_ %]color, only: TR, CA
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: renorm_logs
      implicit none
      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
      real(ki), dimension(-1:0) :: ct
      real(ki) :: scale2

      ! Number of heavy quark flavours in loops.
      real(ki), parameter :: NFh = [% count quark_loop_masses %].0_ki

      ct = 0.0_ki

      ct(-1) = - lo_qcd_couplings * (11.0_ki * CA - 4.0_ki * TR * (NF + NFh)) / 6.0_ki[%    
@for quark_loop_masses %][%
@if is_first %]
      if (renorm_logs) then[%
@end @if %][%
@if is_real %]
         ct(0) = ct(0) + lo_qcd_couplings * (4.0_ki * TR / 6.0_ki * log(scale2/[% $_ %]**2))[%
@end @if %][%
@if is_complex %]
         ct(0) = ct(0) + lo_qcd_couplings * (4.0_ki * TR / 6.0_ki * log(scale2/[% $_ %]/conjg([% $_ %])))[%
@end @if %][%
@if is_last %]
      end if[%
@end @if %][%
@end @for %][%
@if extension dred %]
      ct(0) = ct(0) + lo_qcd_couplings * (CA / 6.0_ki)[%
@end @if %]

   end function counterterm_alphas
!---#] function counterterm_alphas:
!---#[ function counterterm_gluonwf:
   function counterterm_gluonwf(scale2) result(ct)
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model
      use [% process_name asprefix=\_ %]kinematics, only: num_gluons
      use [% process_name asprefix=\_ %]color, only: TR
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: renorm_logs
      implicit none
      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
      real(ki), dimension(-1:0) :: ct
      real(ki) :: scale2

      ! Number of heavy quark flavours in loops.
      real(ki), parameter :: NFh = [% count quark_loop_masses %].0_ki

      ct = 0.0_ki

      ct(-1) = - num_gluons * 2.0_ki * TR / 3.0_ki * NFh[%
@for quark_loop_masses %][%
@if is_first %]
      if (renorm_logs) then[%
@end @if %][%
@if is_real %]
         ct(0) = ct(0) - num_gluons * 2.0_ki * TR / 3.0_ki * log(scale2/[% $_ %]**2)[%
@end @if %][%
@if is_complex %]
         ct(0) = ct(0) - num_gluons * 2.0_ki * TR / 3.0_ki * log(scale2/[% $_ %]/conjg([% $_ %]))[%
@end @if %][%
@if is_last %]
      end if[%
@end @if %][%
@end @for %]   

   end function counterterm_gluonwf
!---#] function counterterm_gluonwf:
!---#[ function counterterm_mqwf:
   function counterterm_mqwf(scale2) result(ct)
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: renorm_logs
      implicit none
      real(ki), dimension(-1:0) :: ct
      real(ki) :: scale2
      
      ct = 0.0_ki
[% @for particles massive quarks anti-quarks %]
      ! wf-counterterm for [% name %]
      ct(-1) = ct(-1) - 1.5_ki * CF
      ct(0) = ct(0) - [% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki * CF
      if (renorm_logs) then
         ct(0) = ct(0) - (1.5_ki*log(scale2/[%mass%]/[%mass%])) * CF
      end if
[% @end @for %]
      
   end function counterterm_mqwf
!---#] function counterterm_mqwf:
!---#[ function counterterm_yukawa_OS:
   function counterterm_yukawa_OS(renorm,eps,scale2,m) result(ct)
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: &
         & renorm_logs, renorm_yukawa
      implicit none
      real(ki) :: ct, scale2, m
      integer :: eps
      logical :: renorm

      ct = 0.0_ki   

      if (.not.(renorm.and.renorm_yukawa)) then
         return
      end if

      select case (eps)
         case(-1)
            ct = -1.5_ki*CF
         case(0)
            ct = -[% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki*CF
            if (renorm_logs) then
               ct = ct - 1.5_ki*CF*reglog(scale2/m/m)
            end if
         case default
            print *, "ERROR: In function counterterm_yukawa_OS: unkown epsilon power."
            stop
      end select

   end function counterterm_yukawa_OS
!---#] function counterterm_yukawa_OS:
!---#[ function counterterm_yukawa_MSbar:
   function counterterm_yukawa_MSbar(renorm,eps) result(ct)
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: &
         & renorm_logs, renorm_yukawa
      implicit none
      real(ki) :: ct
      integer :: eps
      logical :: renorm

      ct = 0.0_ki

      if (.not.(renorm.and.renorm_yukawa)) then
         return
      end if

      select case (eps)
         case(-1)
            ct = -1.5_ki*CF
         case(0)
            ct = -[% @if extension dred %]0.5[% @else %]0.0[% @end @if %]_ki*CF
         case default
            print *, "ERROR: In function counterterm_yukawa_MSbar: unkown epsilon power."
            stop
      end select

   end function counterterm_yukawa_MSbar
!---#] function counterterm_yukawa_MSbar:
!---#[ function counterterm_mass_OS:
   function counterterm_mass_OS(renorm,eps,scale2,m) result(ct)
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: &
         & renorm_logs, renorm_mqse
      implicit none
      real(ki) :: ct, scale2, m
      integer :: eps
      logical :: renorm

      ct = 0.0_ki

      if (.not.(renorm.and.renorm_mqse)) then
         return
      end if

      select case (eps)  
         case(-1)
            ct = -1.5_ki*CF
         case(0)
            ct = -[% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki*CF
            if (renorm_logs) then
               ct = ct - 1.5_ki*CF*reglog(scale2/m/m)
            end if
         case default
            print *, "ERROR: In function counterterm_mass_OS: unkown epsilon power."
            stop
      end select

      ct = m*ct

   end function counterterm_mass_OS
!---#] function counterterm_mass_OS:
!---#[ function counterterm_fr5:
   function counterterm_fr5(renorm,eps) result(ct)
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: &
         & renorm_gamma5
      implicit none
      real(ki) :: ct
      integer :: eps      
      logical :: renorm

      ct = 0.0_ki

      if (.not.(renorm.and.renorm_gamma5)) then
         return
      end if

      select case (eps)  
      case(-1)
         ct = 0.0_ki
      case(0)
         ct = [% @if extension dred %]0.0[% @else %]-1.0[% @end @if %]_ki*CF
      case default
         print *, "ERROR: In function counterterm_fr5: unkown epsilon power."
         stop
   end select

   end function counterterm_fr5
!---#] function counterterm_fr5:
!---#[ function reglog:
   function reglog(r)
      implicit none
      real(ki) :: reglog, r

      if (r.le.0.0_ki) then
         reglog = 0.0_ki
      else
         reglog = log(r)
      end if

   end function reglog
!---#] function reglog:

end module [% process_name asprefix=\_ %]counterterms
