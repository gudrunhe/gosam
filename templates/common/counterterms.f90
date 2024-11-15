[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]counterterms
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki
   implicit none
   save

   private

public :: counterterm_yukawa_OS, counterterm_yukawa_MSbar, counterterm_mass_OS 

contains
 
!---#[ function counterterm_yukawa_OS:
   function counterterm_yukawa_OS(renorm,eps,scale2,m) result(ct)
      use [% process_name asprefix=\_ %]color, only: CF
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & renormalisation, renorm_logs, renorm_yukawa
      implicit none
      real(ki) :: ct, scale2, m
      integer :: eps
      logical :: renorm

      ct = 0.0_ki   

      if (.not.(renorm.and.renorm_yukawa)) then
         return
      end if

      select case (eps)
         case(-2)
            ct = 0.0_ki
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
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & renormalisation, renorm_logs, renorm_yukawa
      implicit none
      real(ki) :: ct
      integer :: eps
      logical :: renorm

      ct = 0.0_ki

      if (.not.(renorm.and.renorm_yukawa)) then
         return
      end if

      select case (eps)
         case(-2)
            ct = 0.0_ki
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
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & renormalisation, renorm_logs, renorm_mqse
      implicit none
      real(ki) :: ct, scale2, m
      integer :: eps
      logical :: renorm

      ct = 0.0_ki

      if (.not.(renorm.and.renorm_mqse)) then
         return
      end if

      select case (eps)  
         case(-2)
            ct = 0.0_ki 
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