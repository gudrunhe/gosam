program test
   use yyyy_config, only: ki
   use yyyy_kinematics, only: dotproduct
   use yyyy_matrix, only: samplitude, initgolem, exitgolem
   use yyyy_rambo, only: ramb
   use yyyy_model, only: me

   implicit none

   ! The amplitudes in all-in notation are
   ! (0) ++++
   ! (1) ++-+
   ! (2) ++--
   ! This means, for gosam (in-out notation) we have
   ! (0) ++--
   ! (1) +++-
   ! (2) ++++
   integer, parameter :: num_helis = 3

   integer, parameter :: logf = 27
   integer, parameter :: NEVT = 10
   double precision, parameter :: eps = 1.0d-5

   integer :: ievt, ihel
   real(ki), dimension(4, 4) :: vecs
   double precision :: scale2, diff
   double precision, dimension(0:3) :: amp
   double precision, dimension(0:num_helis-1) :: gosam_amps
   double precision, dimension(0:num_helis-1) :: reference_amps
   double precision, dimension(0:num_helis-1) :: gauge_amps
   logical :: ok, h_ok, success
   integer :: prec

   integer, dimension(2) :: channels
   integer :: ic, ch

   channels(1) = logf
   channels(2) = 6

   !me = 0.0_ki

   call initgolem()

   call random_seed

   open(file="test.log", unit=logf)
   success = .true.

   do ievt = 1, NEVT
      call ramb(7.0E+00_ki**2, vecs)

      scale2 = 1.03421_ki * 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

      ! compute reference result
      call get_reference_amps(vecs, scale2, me, reference_amps)

      ok = .true.

      ! compute gosam result
      call shake_gauge_parameters(0.0_ki)
      do ihel = 0, num_helis - 1
         call samplitude(vecs, scale2, amp, prec, h_ok, ihel)
         gosam_amps(ihel) = amp(1)
         ok = ok .and. h_ok
      end do

      ! recompute gosam result for a different choice of gauge parameters
      call shake_gauge_parameters(10.0_ki)
      do ihel = 0, 2
         call samplitude(vecs, scale2, amp, prec, h_ok, ihel)
         gauge_amps(ihel) = amp(1)
         ok = ok .and. h_ok
      end do

      do ihel = 0, num_helis - 1

         do ic = 1, 2
            ch = channels(ic)
            write(unit=ch,fmt="(A6,1x,I2,1x,A5,1x,I1)") &
               &  "EVENT:", ievt, "HELI:", ihel
            diff = rel_diff(gosam_amps(ihel), reference_amps(ihel)**2)
            if (diff .gt. eps) then
               write(unit=ch,fmt="(A3,1x,A30)") "==>", &
                  & "Comparison failed!"
               success = .false.
            end if
            write(unit=ch,fmt="(A18,1x,E23.15)") "GOSAM:", gosam_amps(ihel)
            write(unit=ch,fmt="(A18,1x,E23.15)") "GAUGE:", gauge_amps(ihel)
            write(unit=ch,fmt="(A18,1x,E23.15)") "REFERENCE:", &
               & reference_amps(ihel)**2

            diff = rel_diff(gosam_amps(ihel), gauge_amps(ihel))
            if (diff .gt. eps) then
               write(unit=ch,fmt="(A3,1x,A20)") "==>", &
                  & "Gauge test failed!"
               success = .false.
            end if
         end do
      end do
   end do

   call exitgolem()


   if (success) then
     write(unit=logf,fmt="(A15)") "@@@ SUCCESS @@@"
   else
     write(unit=logf,fmt="(A15)") "@@@ FAILURE @@@"
   end if
   close(logf)

contains

   pure function rel_diff(a, b)
      implicit none

      double precision, parameter :: tiny_dbl = 1.0d-13
      double precision, intent(in) :: a, b
      double precision :: rel_diff

      if (abs(a) .lt. tiny_dbl .and. abs(b) .lt. tiny_dbl) then
         rel_diff = 0.0d0
      else
         rel_diff = 2.0d0 * abs(a-b) / (abs(a)+abs(b))
      end if
   end  function rel_diff

   subroutine     shake_gauge_parameters(delta)
      use yyyy_model, only: gauge1z, gauge2z, gauge3z, gauge4z
      implicit none
      real(ki), intent(in) :: delta

      real(ki), dimension(4) :: harvest

      call random_number(harvest)

      gauge1z = delta * (harvest(1) - 0.5_ki)
      gauge2z = delta * (harvest(2) - 0.5_ki)
      gauge3z = delta * (harvest(3) - 0.5_ki)
      gauge4z = delta * (harvest(4) - 0.5_ki)
   end subroutine shake_gauge_parameters

   subroutine get_reference_amps(vecs,scale2,mf,amps)
      ! Reference:
      ! [1] G.J. Gounaris, P.I. Porfyriadis, F.M. Renard,
      !     ``The gamma gamma ---> gamma gamma process in the standard and SUSY
      !       models at high-energies,''
      !     Eur.\ Phys.\ J.\  {\bf C9 } (1999)  673-686.
      !     [hep-ph/9902230].
      implicit none
      real(ki), dimension(4,0:3), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), intent(in) :: mf
      double precision, dimension(0:2), intent(out) :: amps
   
   
      double precision :: m2, ss, tt, uu
      double complex, dimension(0:2) :: D0st, D0tu, D0us
      double complex, dimension(0:2) :: c0u, c0s, c0t, b0u, b0s, b0t
   
      m2=mf*mf
      ss=2.0_ki*dotproduct(vecs(1,:),vecs(2,:))
      tt=-2.0_ki*dotproduct(vecs(1,:),vecs(3,:))
      uu=-2.0_ki*dotproduct(vecs(2,:),vecs(3,:))
   
      call avh_olo_onshell(1.d-10)
      call avh_olo_mu_set(sqrt(real(scale2,kind(1.0d0))))
      call avh_olo_d0m(D0st,0.0d0,0.0d0,0.0d0,0.0d0,ss,tt,m2,m2,m2,m2)
      call avh_olo_d0m(D0tu,0.0d0,0.0d0,0.0d0,0.0d0,tt,uu,m2,m2,m2,m2)
      call avh_olo_d0m(D0us,0.0d0,0.0d0,0.0d0,0.0d0,uu,ss,m2,m2,m2,m2)
      call avh_olo_c0m(c0u,0.0d0,0.0d0,uu,m2,m2,m2)
      call avh_olo_c0m(c0s,0.0d0,0.0d0,ss,m2,m2,m2)
      call avh_olo_c0m(c0t,0.0d0,0.0d0,tt,m2,m2,m2)
      call avh_olo_b0m(b0u,uu,m2,m2)
      call avh_olo_b0m(b0s,ss,m2,m2)
      call avh_olo_b0m(b0t,tt,m2,m2)
   
      amps(0) = -4.0d0+8.0d0*m2**2*( D0st(0)+D0tu(0)+D0us(0))
      amps(1) = +4.0d0-8.0d0*m2**2*( D0st(0)+D0tu(0)+D0us(0))&
       &      -4.0d0*m2*ss*tt*uu*( D0st(0)/uu**2+D0tu(0)/ss**2+D0us(0)/tt**2)&
       &      +8.0d0*m2*(1.0d0/ss+1.0d0/tt+1.0d0/uu)&
       &                *(tt*C0t(0)+uu*C0u(0)+ss*C0s(0))
      amps(2) = -4.0d0 +4.0d0*(ss+2.0d0*uu)/ss*b0u(0)&
       &      +4.0d0*(ss+2.0d0*tt)/ss*b0t(0)&
       &      -4.0d0*(tt**2+uu**2-4.0d0*m2*ss)/ss/ss*(tt*c0t(0)+uu*c0u(0))&
       &      +4.0d0*m2*(ss-2.0d0*m2)*(d0st(0)+d0us(0))&
       &      -2.0d0*(4.0d0*m2**2-(2.0d0*ss*m2+tt*uu)*(tt*tt+uu*uu)/ss/ss&
       &               +4.0d0*m2*tt*uu/ss)*d0tu(0)
   end subroutine get_reference_amps
   
end program test
