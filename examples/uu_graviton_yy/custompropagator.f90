module     graviton_custompropagator
   use graviton_config, only: ki
   use graviton_model
   implicit none
   save

   private

   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   real(ki), parameter :: sqrthalf = &
   & 0.7071067811865475244008443621048490392848359376884740365883398689_ki
   real(ki), parameter, private :: pi = &
   & 3.1415926535897932384626433832795028841971693993751058209749445920_ki


public :: customSpin2Prop

contains
  !---#[ function customSpin2Prop :
   function customSpin2Prop(s, m) result(ret)
      implicit none
      real(ki), intent(in) :: s ! four-momentum squared
      real(ki), intent(in) :: m ! mass
      complex(ki) :: ret

      complex(ki) :: tmp, sqrts, sqrtt

      integer :: k, mdlextraD
      real(ki) :: mdlMSScale , t

      mdlextraD = 4

      mdlMSScale = 4E3_ki

      ! hep-ph/9811350 B.8

      ! mdlextraD even

      sqrts = sqrt(s)

      tmp=0
      if (s>0) then
             !  time-like

             ! hep-9811350 B.8
             if (MOD(mdlextraD,2)==0) then ! even dimension
                     do k = 1, mdlextraD/2 -1
                             tmp = tmp - 0.5_ki/k * (mdlMSScale / sqrts)**(2*k)
                     end do
                     tmp = tmp - 0.5_ki * log(mdlMSScale**2/(s) - 1._ki)
             else
                     do k = 1, (mdlextraD-1)/2
                             tmp = tmp -  (mdlMSScale / sqrts)**(2*k-1) /  (2*k-1)
                     end do
                     tmp = tmp + 0.5_ki * log((mdlMSScale+sqrts)/(mdlMSScale-sqrts))
             end if

             ! hep-ph/0306182 eq. 3.5
             ret = s**(mdlextraD/2-1) / (2._ki*mdlMSScale**(mdlextraD+2) * mdlGN ) * &
                     (pi + 2* cmplx(0,1._ki)*tmp)

      else ! space-like
              t=abs(s) ! s now for t
              sqrtt= sqrt(t)

             ! hep-9811350 B.11
              if (MOD(mdlextraD,2)==0) then ! even dimension
                      do k = 1, mdlextraD/2 -1
                              tmp = tmp + (-1._ki)**k / 2._ki / k * (mdlMSScale / sqrtt)**(2*k)
                      end do
                      tmp = tmp + 0.5_ki * log(mdlMSScale**2/t + 1._ki)
                      tmp = tmp * (-1._ki)**(mdlextraD/2+1)
              else ! odd dimensions
                      do k = 1, (mdlextraD - 1)/2
                              tmp = tmp + (-1._ki)**k / (2._ki*k-1._ki) * (mdlMSScale / sqrtt)**(2*k-1)
                      end do
                      tmp = tmp + atan(mdlMSScale/sqrtt)
                      tmp = tmp * (-1._ki)**((mdlextraD-1)/2)
             end if
             ! hep-ph/0306182 eq. 3.4
             ret = t**(mdlextraD/2-1) / (2._ki*mdlMSScale**(mdlextraD+2) * mdlGN ) * &
                     cmplx(0,-2._ki)*tmp
     end if

   end function customSpin2Prop
   !---#] function customSpin2Prop
end module graviton_custompropagator
