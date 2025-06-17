program test
   use ggHg_SMEFT_config, only: ki, logfile, EFTcount, nlo_prefactors
   use ggHg_SMEFT_kinematics, only: dotproduct, boost_to_cms
   use ggHg_SMEFT_model
   use ggHg_SMEFT_matrix, only: samplitude, initgolem, exitgolem
   use ggHg_SMEFT_rambo, only: ramb
   
   implicit none
   integer :: ievt, ierr, prec, ieft
   integer, parameter, dimension(0:4) :: eftc = (/0,11,12,13,14/)
   real(ki), dimension(4,4) :: vecs
   real(ki), dimension(0:4,0:3) :: gsres, refres, diff
   real(ki) :: scale2, sqrts
   real(ki), parameter :: eps = 1.0e-10_ki
   character(len=45), dimension(0:4) :: truncation_order, truncation_order2 
   
   ! log and output
   integer, parameter :: logf = 27
   logical :: success

   open(file="test.log", unit=logf)
   success = .true.
   
   ! parameters
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   
   nlo_prefactors = 2
   
   sqrts = 500._ki
   
   call initgolem()

   call random_seed
   call ramb(sqrts**2, vecs)
   call boost_to_cms(vecs)

   scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))
   
   truncation_order = [character(len=45) :: &
        & "Truncation order (SM x SM):", &
        & "Truncation order (SM x SM) + (SM x dim-6):", &
        & "Truncation order (SM + dim-6) x (SM + dim-6):", &
        & "Truncation order (SM x dim-6):", &
        & "Truncation order (dim-6 x dim-6):" ]
   truncation_order2 = [character(len=45) :: &
        & "truncation order (SM x SM):", &
        & "truncation order (SM x SM) + (SM x dim-6):", &
        & "truncation order (SM + dim-6) x (SM + dim-6):", &
        & "truncation order (SM x dim-6):", &
        & "truncation order (dim-6 x dim-6):" ]   

   gsres = 0._ki
   refres = 0._ki
   diff = 999._ki
   
   do ieft = 0, 4
      EFTcount = eftc(ieft)
      call samplitude(vecs, scale2, gsres(ieft,:), prec)
      call analytic_amp(vecs,refres(ieft,:))
      write(unit=6,fmt="(A45)") NEW_LINE('a'), truncation_order(ieft)
      write(unit=6,fmt="((3(15x,A11)))") &
           & "finite part", "single pole", "double pole"
      write(unit=6,fmt="((A12,3(3x,E23.16E3)))") &
           & "GoSam      :", gsres(ieft,1), gsres(ieft,2), gsres(ieft,3)
      write(unit=6,fmt="((A12,3(3x,E23.16E3)))") &
           & "Analytical :", refres(ieft,1), refres(ieft,2), refres(ieft,3)
      write(unit=6,fmt="((A12,3(3x,E23.16E3)))") &
           & "Ratio GS/A :", gsres(ieft,1)/refres(ieft,1), &
           & gsres(ieft,2)/refres(ieft,2), gsres(ieft,3)/refres(ieft,3), NEW_LINE('a')

      diff(ieft,1) = abs(rel_diff(gsres(ieft,1), refres(ieft,1)))

      if (diff(ieft,1) .gt. eps) then
         write(unit=logf,fmt="(A3,1x,A13,1x,A45,1x,A7)") "==>", &
              & "Comparison of", truncation_order(ieft), "failed!"
         write(unit=logf,fmt="((3(15x,A11)))") &
              & "finite part", "single pole", "double pole"
         write(unit=logf,fmt="((A12,3(3x,E23.16E3)))") &
              & "GoSam      :", gsres(ieft,1), gsres(ieft,2), gsres(ieft,3)
         write(unit=logf,fmt="((A12,3(3x,E23.16E3)))") &
              & "Analytical :", refres(ieft,1), refres(ieft,2), refres(ieft,3)
         write(unit=logf,fmt="((A12,3x,E23.16E3))") &
              & "DIFFERENCE :", diff(ieft,1)
         success = .false.
      end if

   end do

   if (success) then
      write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
   else
      write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
   end if
   
   close(unit=logf)
  
   call exitgolem()
   
 contains
 
   
subroutine analytic_amp(vecs,amp)
  use ggHg_SMEFT_model
  use ggHg_SMEFT_config, only: EFTcount
  implicit none
  real(ki), intent(in), dimension(4,4) :: vecs
  real(ki), dimension(0:3), intent(out) :: amp
  real(ki), dimension(0:3) :: coeffSM, coeffggh, coeffggh2
  real(ki), parameter :: pi = 3.141592653589793_ki
  real(ki) :: delta_ct, cggh, s, t, u

  delta_ct = -mdlctphi*mdlLam/2._ki**(5._ki/4._ki)/mdlGf**(3._ki/2._ki)/mdlymt
  cggh = mdlcphiG*mdlLam*8._ki*pi/mdlaS/sqrt(2._ki)/mdlGf

  call Mandelstam(vecs,s,t,u)

  coeffSM = analytic_coeff_SM(s,t,u)
  coeffggh = analytic_coeff_cggh(s,t,u)
  coeffggh2 = analytic_coeff_cggh2(s,t,u)
  
  select case(EFTcount)
  case(0)
     amp = coeffSM
  case(11)
     amp = (1._ki + 2._ki*delta_ct)*coeffSM + cggh*coeffggh
  case(12)
     amp = (1._ki + delta_ct)**2*coeffSM + (1._ki + delta_ct)*cggh*coeffggh + cggh**2*coeffggh2
  case(13)
     amp = 2._ki*delta_ct*coeffSM + cggh*coeffggh
  case(14)
     amp = delta_ct**2*coeffSM + delta_ct*cggh*coeffggh + cggh**2*coeffggh2
  case default
     print *, "Unknown value for EFTcount: ", EFTcount
     stop
  end select
  
end subroutine analytic_amp
 

subroutine Mandelstam(vecs,s,t,u)
  use ggHg_SMEFT_kinematics, only: dotproduct
  implicit none
  real(ki), intent(in), dimension(4,4) :: vecs
  real(ki), intent(out) :: s, t, u

  s = dotproduct(vecs(1,:)+vecs(2,:),vecs(1,:)+vecs(2,:))
  t = dotproduct(vecs(2,:)-vecs(4,:),vecs(2,:)-vecs(4,:))
  u = dotproduct(vecs(1,:)-vecs(4,:),vecs(1,:)-vecs(4,:))
  
end subroutine Mandelstam


function analytic_coeff_SM(s, t, u, ih) result(amp)
  use ggHg_SMEFT_model, only: mdlGf, NC, mdlaS
  use ggHg_SMEFT_color, only: incolors
  use ggHg_SMEFT_kinematics, only: in_helicities, symmetry_factor
  implicit none
  real(ki) :: s, t, u
  real(ki) :: prefac
  integer, optional :: ih
  real(ki), dimension(0:3) :: amp
  integer :: hel
  real(ki), parameter :: pi = 3.141592653589793_ki
  complex(ki), dimension(1:3) :: dummy
  
  amp = 0._ki
  
  prefac = NC*(NC**2-1._ki)*mdlGf*sqrt(2._ki)*mdlaS**3/2._ki/pi
  prefac = prefac/incolors/in_helicities/symmetry_factor
  
  if (present(ih)) then
     select case(ih)
     case(3,4) ! ++-/--+ (gosam convention)
        amp(1:3) = real(b(s,t,u,1)*conjg(b(s,t,u,1)))*H(s,t,u,1)
     case(2,5) ! +-+/+-+ (gosam convention)
        amp(1:3) = real(b(s,t,u,4)*conjg(b(s,t,u,4)))*H(s,t,u,4)
     case(1,6) ! +--/-++ (gosam convention)
        amp(1:3) = real(b(s,t,u,3)*conjg(b(s,t,u,3)))*H(s,t,u,3)
     case(0,7) ! ---/+++ (gosam convention)
        amp(1:3) = real(b(s,t,u,2)*conjg(b(s,t,u,2)))*H(s,t,u,2)
     end select
  else
     do hel = 1, 4
        ! factor 2 because of parity (+++ = --- etc.)
        amp(1:3) = amp(1:3) + 2._ki*real(b(s,t,u,hel)*conjg(b(s,t,u,hel)))*H(s,t,u,hel)
     end do
  end if

  amp = prefac*amp
  
end function analytic_coeff_SM


function analytic_coeff_cggh(s, t, u, ih) result(amp)
  use ggHg_SMEFT_model, only: mdlGf, NC, mdlaS
  use ggHg_SMEFT_color, only: incolors
  use ggHg_SMEFT_kinematics, only: in_helicities, symmetry_factor
  implicit none
  real(ki) :: s, t, u
  real(ki) :: prefac
  integer, optional :: ih
  real(ki), dimension(0:3) :: amp
  integer :: hel
  real(ki), parameter :: pi = 3.141592653589793_ki
  
  amp = 0._ki

  prefac = NC*(NC**2-1._ki)*mdlGf*sqrt(2._ki)*mdlaS**3/2._ki/pi
  prefac = prefac/incolors/in_helicities/symmetry_factor
  
  if (present(ih)) then
     select case(ih)
     case(3,4) ! ++-/--+ (gosam convention)
        amp(1:3) = 2._ki*real(b(s,t,u,1))*a()*H(s,t,u,1)
     case(2,5) ! +-+/+-+ (gosam convention)
        amp(1:3) = 2._ki*real(b(s,t,u,4))*a()*H(s,t,u,4)
     case(1,6) ! +--/-++ (gosam convention)
        amp(1:3) = 2._ki*real(b(s,t,u,3))*a()*H(s,t,u,3)
     case(0,7) ! ---/+++ (gosam convention)
        amp(1:3) = 2._ki*real(b(s,t,u,2))*a()*H(s,t,u,2)
     end select
  else
     do hel = 1, 4
        ! factor 2 because of parity (+++ = --- etc.)
        amp(1:3) = amp(1:3) + 2._ki*2._ki*real(b(s,t,u,hel))*a()*H(s,t,u,hel)
     end do
  end if
     
  amp = prefac*amp
  
end function analytic_coeff_cggh


function analytic_coeff_cggh2(s, t, u, ih) result(amp)
  use ggHg_SMEFT_model, only: mdlGf, NC, mdlaS
  use ggHg_SMEFT_color, only: incolors
  use ggHg_SMEFT_kinematics, only: in_helicities, symmetry_factor
  implicit none
  real(ki) :: s, t, u
  real(ki) :: prefac
  integer, optional :: ih
  real(ki), dimension(0:3) :: amp
  integer :: hel
  real(ki), parameter :: pi = 3.141592653589793_ki
  
  amp = 0._ki

  prefac = NC*(NC**2-1._ki)*mdlGf*sqrt(2._ki)*mdlaS**3/2._ki/pi
  prefac = prefac/incolors/in_helicities/symmetry_factor
  
  if (present(ih)) then
     select case(ih)
     case(3,4) ! ++-/--+ (gosam convention)
        amp(1:3) = a()**2*H(s,t,u,1)
     case(2,5) ! +-+/+-+ (gosam convention)
        amp(1:3) = a()**2*H(s,t,u,4)
     case(1,6) ! +--/-++ (gosam convention)
        amp(1:3) = a()**2*H(s,t,u,3)
     case(0,7) ! ---/+++ (gosam convention)
        amp(1:3) = a()**2*H(s,t,u,2)
     end select
  else
     do hel = 1, 4
        ! factor 2 because of parity (+++ = --- etc.)
        amp(1:3) = amp(1:3) + 2._ki*a()**2*H(s,t,u,hel)
     end do
  end if
  
  amp = prefac*amp
  
end function analytic_coeff_cggh2


function H(s, t, u, hel)
  implicit none
  real(ki) :: H, s, t, u
  integer :: hel

  H = 0._ki

  ! Note: helicities for all outgoing
  select case(hel)
  case(1) ! ++0+ / --0-
     H = (s+t+u)**4
  case(2) ! ++0- / --0+
     H = s**4
  case(3) ! +-0+ / -+0-
     H = u**4
  case(4) ! -+0+ / +-0-
     H = t**4
  end select

  H = H/(s*t*u)
  
end function H


function a()
  use ggHg_SMEFT_model, only: mdlGf, mdlaS
  implicit none
  real(ki), dimension(0:2) :: a

  a(0) = 1._ki
  a(1) = 0._ki
  a(2) = 0._ki
  
end function a


function b(s, t, u, hel)
  implicit none
  complex(ki), dimension(0:2) :: b
  real(ki) :: s, t, u
  integer :: hel

  b = (0._ki, 0._ki)

  ! Note: helicities for all outgoing
  select case(hel)
  case(1) ! ++0+ / --0-
     b = bppp(s, t, u)
  case(2) ! ++0- / --0+
     b = bppm(s, t, u)
  case(3) ! +-0+ / -+0-
     b = bppm(u, s, t)
  case(4) ! -+0+ / +-0-
     b = bppm(t, u, s)
  end select
  
end function b


! h->ggg: auxiliary function, summing up the different cyclic permutations
! of (4.24) according to (2.5) from hep-ph/9709423 (only curly brackets),
function bppp(s, t, u)
  use ggHg_SMEFT_model, only: mdlMH, mdlMQT
  implicit none
  complex(ki), dimension(0:2) :: bppp
  real(ki) :: s, t, u, m2, mh2

  m2 = mdlMQT**2
  mh2 = mdlMH**2

  bppp = -m2/mh2/mh2*0.5_ki*(4._ki*m2-mh2)*(W2(s,m2) + W2(t,m2) + W2(u,m2) - 3._ki*W2(mh2,m2) &
       &                      + W3(t,u,s,m2) + W3(s,t,u,m2) + W3(u,s,t,m2))  
  
  bppp(0) = bppp(0) - complex(m2/mh2/mh2*(-4._ki*mh2),0._ki)
  
end function bppp
       
! h->ggg: auxiliary function, summing up the different cyclic permutations
! of (4.25),(4.26) according to (2.5) from hep-ph/9709423 (only curly brackets),
function bppm(s, t, u)
  use ggHg_SMEFT_model, only: mdlMH, mdlMQT
  implicit none
  complex(ki), dimension(0:2) :: bppm
  real(ki) :: s, t, u, m2, mh2, s1, t1, u1

  m2 = mdlMQT**2
  mh2 = mdlMH**2

  s1 = s-mh2
  t1 = t-mh2
  u1 = u-mh2

  bppm = -m2/s/s*( &
       &          4._ki*t*u*(s-t1)/t1/t1*(W1(t,m2)-W1(mh2,m2)) &
       &	 +4._ki*t*u*(s-u1)/u1/u1*(W1(u,m2)-W1(mh2,m2)) &
       &	 +(4._ki*m2-s)/2._ki*W2(s,m2) &
       &	 +(-(4._ki*m2-s)/2._ki-2._ki*t*u/s+4._ki*m2*s*s/t1/t1+s*s/t1)*W2(t,m2) &
       &	 +(-(4._ki*m2-s)/2._ki-2._ki*u*t/s+4._ki*m2*s*s/u1/u1+s*s/u1)*W2(u,m2) &
       &	 +((4._ki*m2-s)/2._ki-4._ki*m2*(s*s/t1/t1+s*s/u1/u1) &
       &	   -s*s*(1._ki/t1+1._ki/u1)+2._ki*t*u/s)*W2(mh2,m2) &
       &	 +(4._ki*m2-s)/2._ki*W3(s,t,u,m2) &
       &	 +(4._ki*m2-s)/2._ki*W3(s,u,t,m2) &
       &	 +(-6._ki*m2+s/2._ki-2._ki*t*u/s)*W3(t,s,u,m2))

  bppm(0) = bppm(0) - complex(m2/s/s*(-4._ki*s*(s*s-t*u)/t1/u1),0._ki)
  
end function bppm


function W1(s, msq)
  use avh_olo
  implicit none
  complex(ki), dimension(0:2) :: W1
  real(ki) :: s, msq

  call avh_olo_b0c(W1, &
       & complex(s,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki))

  W1 = -W1
  
end function W1


! function W1check(s, msq)
!   implicit none
!   real(ki) :: s, msq
!   complex(ki) :: x, one, W1check

!   one = complex(1._ki,0._ki)
  
!   x = (sqrt(one*(1._ki-4._ki*msq/s))-one)/(sqrt(one*(1._ki-4._ki*msq/s))+one)

!   W1check = (x+one)/(x-one)*log(x)

! end function W1check


function W2(s, msq)
  use avh_olo
  implicit none
  complex(ki), dimension(0:2) :: W2
  real(ki) :: s, msq

  call avh_olo_c0c(W2, &
       & complex(0._ki,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(s,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki))

  W2 = 2._ki*s*W2
  
end function W2


! function W2check(s, msq)
!   implicit none
!   real(ki) :: s, msq
!   complex(ki) :: x, one, W2check

!   one = complex(1._ki,0._ki)
  
!   x = (sqrt(one*(1._ki-4._ki*msq/s))-one)/(sqrt(one*(1._ki-4._ki*msq/s))+one)

!   W2check = log(x)**2

! end function W2check


function W3(s, t, u, msq)
  use avh_olo
  implicit none
  complex(ki), dimension(0:2) :: W3
  real(ki) :: s, t, u, msq

  call avh_olo_d0c(W3, &
       & complex(0._ki,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(0._ki,0._ki), &
       & complex(s+t+u,0._ki), &
       & complex(s,0._ki), &
       & complex(u,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki), &
       & complex(msq,0._ki))

  W3 = -s*u*W3
  
end function W3


pure elemental function rel_diff(a, b)
   implicit none

   double precision, intent(in) :: a, b
   double precision :: rel_diff

   if (a.eq.0.0d0 .and. b.eq.0.0d0) then
      rel_diff = 0.0d0
   else
      rel_diff = 2.0d0 * (a-b) / (abs(a)+abs(b))
   end if
 end  function rel_diff

 
end program test
