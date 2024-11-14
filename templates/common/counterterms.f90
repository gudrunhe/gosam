[%' vim: sw=3:syntax=golem
'%]module     [% process_name asprefix=\_ %]counterterms
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki, &
    & renormalisation, renorm_logs, renorm_yukawa, renorm_mqse   
   implicit none
   save

   private

public :: yukctOS, yukctMSbar, massctOS

contains

!---#[ function yukctOS:
   function yukctOS(renorm,eps,scale2,m)
      use [% process_name asprefix=\_ %]color, only: CF
      implicit none
      real(ki) :: yukctOS, scale2, m
      integer :: eps
      logical :: renorm

      if (.not.(renorm.and.renorm_yukawa)) then
         yukctOS = 0.0_ki
         return
      end if

      select case (eps)
         case(-1)
            yukctOS = -1.5_ki*CF
         case(0)
            yukctOS = -[% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki*CF
            if (renorm_logs) then
               yukctOS = yukctOS - 1.5_ki*CF*reglog(scale2/m/m)
            end if
         case default
            print *, "ERROR: In function yukctOS: unkown epsilon power."
            stop
      end select

   end function     yukctOS
!---#] function yukctOS:
!---#[ function yukctMSbar:
   function yukctMSbar(renorm,eps)
      use [% process_name asprefix=\_ %]color, only: CF
      implicit none
      real(ki) :: yukctMSbar
      integer :: eps
      logical :: renorm

      if (.not.(renorm.and.renorm_yukawa)) then
         yukctMSbar = 0.0_ki
         return
      end if

      select case (eps)
         case(-1)
            yukctMSbar = -1.5_ki*CF
         case(0)
            yukctMSbar = -[% @if extension dred %]0.5[% @else %]0.0[% @end @if %]_ki*CF
         case default
            print *, "ERROR: In function yukctMSbar: unkown epsilon power."
            stop
      end select

   end function yukctMSbar
!---#] function yukctMSbar:
!---#[ function massctOS:
   function massctOS(renorm,eps,scale2,m)
      use [% process_name asprefix=\_ %]color, only: CF
      implicit none
      real(ki) :: massctOS, scale2, m
      integer :: eps
      logical :: renorm

      if (.not.(renorm.and.renorm_mqse)) then
         massctOS = 0.0_ki
         return
      end if

      select case (eps)
         case(-1)
            massctOS = -1.5_ki*CF
         case(0)
            massctOS = -[% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki*CF
            if (renorm_logs) then
               massctOS = (massctOS - 1.5_ki*CF*reglog(scale2/m/m))
            end if
         case default
            print *, "ERROR: In function massctOS: unkown epsilon power."
            stop
      end select

      massctOS = m*massctOS

   end function massctOS
!---#] function massctOS:
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