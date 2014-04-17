program test
use eeuu_config, only: ki, debug_lo_diagrams, debug_nlo_diagrams
use eeuu_matrix, only: initgolem, exitgolem
use eeuu_kinematics, only: inspect_kinematics, init_event
implicit none

! unit of the log file
integer, parameter :: logf = 27
integer, parameter :: gosamlogf = 19

integer, dimension(2) :: channels
integer :: ic, ch

double precision, parameter :: eps = 1.0d-4

logical :: success

real(ki), dimension(4, 4) :: vecs
real(ki) :: scale2

double precision, dimension(0:3) :: gosam_amp, ref_amp, diff

channels(1) = logf
channels(2) = 6

open(file="test.log", unit=logf)
success = .true.

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   open(file="gosam.log", unit=gosamlogf)
end if

call setup_parameters()
call initgolem()

call load_reference_kinematics(vecs, scale2)

call init_event(vecs)
call inspect_kinematics(logf)

call compute_gosam_result(vecs, scale2, gosam_amp)

call compute_reference_result(vecs, scale2, ref_amp)

diff = abs(rel_diff(gosam_amp, ref_amp))

if (diff(0) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of LO failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(0)
   success = .false.
end if

if (diff(1) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/finite part failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(1)
   success = .false.
end if

if (diff(2) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A40)") "==>", &
   & "Comparison of NLO/single pole failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(2)
   success = .false.
end if

if (diff(3) .gt. eps) then
   write(unit=logf,fmt="(A3,1x,A30)") "==>", &
   & "Comparison of NLO/double pole failed!"
   write(unit=logf,fmt="(A10,1x,E10.4)") "DIFFERENCE:", diff(3)
   success = .false.
end if

if (success) then
   write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
else
   write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
end if

close(unit=logf)

if (debug_lo_diagrams .or. debug_nlo_diagrams) then
   close(unit=gosamlogf)
end if

call exitgolem()

contains

pure subroutine load_reference_kinematics(vecs, scale2)
   use eeuu_kinematics, only: adjust_kinematics, dotproduct
   implicit none
   real(ki), dimension(4, 4), intent(out) :: vecs
   real(ki), intent(out) :: scale2

   real(ki), parameter :: phi   = 2.46_ki
   real(ki), parameter :: theta = 1.35_ki
   real(ki), parameter :: E = 74.7646520969852_ki

   vecs(1,:) =  (/ E, 0.0_ki, 0.0_ki,  E /)
   vecs(2,:) =  (/ E, 0.0_ki, 0.0_ki, -E /)
   vecs(3,1) =  E
   vecs(3,2) =  E * sin(theta) * sin(phi)
   vecs(3,3) =  E * sin(theta) * cos(phi)
   vecs(3,4) =  E * cos(theta)
   vecs(4,1) =  E
   vecs(4,2) = -E * sin(theta) * sin(phi)
   vecs(4,3) = -E * sin(theta) * cos(phi)
   vecs(4,4) = -E * cos(theta)

   scale2 = (2.0_ki*E)**2

end  subroutine load_reference_kinematics

subroutine     setup_parameters()
   use eeuu_config, only: renormalisation, convert_to_cdr !, &
       !      & samurai_test, samurai_verbosity, samurai_scalar, &
       !      & reduction_interoperation
   use eeuu_model, only: Nf, Nfgen, mZ, wZ, mW
   implicit none

   renormalisation = 0

   ! settings for samurai:
   ! verbosity: we keep it zero here unless you want some extra files.
   ! samurai_verbosity = 0
   ! samurai_scalar: 1=qcdloop, 2=OneLOop
   ! samurai_scalar = 2
   ! samurai_test: 1=(N=N test), 2=(local N=N test), 3=(power test)
   ! samurai_test = 1

   mZ = 91.1876_ki
   wZ = 2.4952_ki
   mW = mZ * sqrt(1.0_ki - 0.47303762_ki**2)

   Nf    = 5.0_ki
   Nfgen = 1.0_ki

   convert_to_cdr = .true.
end subroutine setup_parameters

subroutine     compute_gosam_result(vecs, scale2, amp)
   use eeuu_matrix, only: samplitude
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp
   integer :: prec

   call samplitude(vecs, scale2, amp, prec)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "GOSAM     AMP(0):       ", amp(0)
      write(ch,*) "GOSAM     AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "GOSAM     AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "GOSAM     AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_gosam_result

subroutine     compute_reference_result(vecs, scale2, amp)
   use eeuu_kinematics, only: es12
   use eeuu_model, only: mZ, wZ, e, NC, sw, cw, gev, gea, gUv, gUa, gZ
   implicit none

   real(ki), dimension(4, 4), intent(in) :: vecs
   real(ki), intent(in) :: scale2
   double precision, dimension(0:3), intent(out) :: amp

   double precision, parameter :: Qf  =  2.d0/3.d0
   double precision, parameter :: Qe  = -1.d0
   double precision, parameter :: I3f =  0.5d0
   double precision, parameter :: I3e = -0.5d0

   double precision :: cost, Ve, Vf, Ae, Af, Chi1, Chi2, Chi0
   double precision :: flgAA, flgAZ, flgZZ
   double precision :: CF, l, pi

   flgAA = 1.d0
   flgAZ = 1.d0
   flgZZ = 1.d0

   ! LO results of [1] (see README)

   cost = vecs(3,4) / vecs(3,1)

   if(.false.) then
      Vf =  (I3f - 2.d0 * Qf * sw**2) * 0.5d0 * gZ
      Af =  I3f * 0.5d0 * gZ
      Ve =  (I3e - 2.d0 * Qe * sw**2) * 0.5d0 * gZ
      Ae =  I3e * 0.5d0 * gZ
   else
      Vf = gUv
      Af = gUa
      Ve = gev
      Ae = gea
   end if


   Chi0 = flgAA * 1.d0
   Chi1 = flgAZ * es12 * (es12 - mZ**2) &
        &  / ((es12 - mZ**2)**2 + wZ**2 * mZ**2)
   Chi2 = flgZZ * es12**2 &
        & / ((es12 - mZ**2)**2 + wZ**2 * mZ**2)

   amp(0) = NC * ( &
     & (1.d0 + cost**2) * (Qf**2 * Qe**2 * Chi0 &
     &        + 2.d0 * Qf * Qe * Ve * Vf * Chi1 &
     & + (Ae**2 + Ve**2) * (Af**2 + Vf**2) * Chi2) &
     & + 2.d0 * cost * Ae*Af * (2.d0 * Qf * Qe * Chi1 + 4.d0 * Vf * Ve * Chi2))

   pi = 4.0d0 * atan(1.0d0)
   CF = 0.5d0 * (NC*NC-1.0d0) / NC
   l = log(scale2/es12)

   amp(1) = CF*(-l**2-3.0d0*l+pi**2-8.0d0) * amp(0)
   amp(2) = CF * (-3.0d0 - 2.0d0*l) * amp(0)
   amp(3) = -2.0d0 * CF * amp(0)

   do ic = 1, 2
      ch = channels(ic)
      write(ch,*) "REFERENCE AMP(0):       ", amp(0)
      write(ch,*) "REFERENCE AMP(1)/AMP(0):", amp(1)/amp(0)
      write(ch,*) "REFERENCE AMP(2)/AMP(0):", amp(2)/amp(0)
      write(ch,*) "REFERENCE AMP(3)/AMP(0):", amp(3)/amp(0)
   end do
end subroutine compute_reference_result

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
