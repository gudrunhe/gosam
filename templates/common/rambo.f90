[% ' vim: syntax=golem
 %]module     [% process_name asprefix=\_%]rambo
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none

   private :: ki

   real(ki), parameter, private :: pi = &
      &3.1415926535897932384626433832795028&
      &841971693993751058209749445920_ki

   interface ramb
      module procedure rambo_a
      module procedure rambo_b
      module procedure rambo_process
   end interface

   interface boost
      module procedure boost_a
      module procedure boost_b
   end interface

   private :: rambo_in, rambo_a, rambo_b, newton, rambo0
   private :: boost_a, boost_b, scalar, rambo_process
contains

   pure function scalar(p, q)
      implicit none
      real(ki), dimension(4), intent(in) :: p, q
      real(ki) :: scalar
      scalar = p(1)*q(1) - p(2)*q(2) - p(3)*q(3) - p(4)*q(4)
   end  function scalar

   subroutine     boost_b(vecs)
      implicit none
      real(ki), dimension(:,:), intent(inout) :: vecs
      real(ki), dimension(2) :: x

      call random_number(x)
      call boost_a(x, vecs)
   end subroutine boost_b

   subroutine     boost_a(x, vecs)
      ! Boost code from T. Binoth's routines
      implicit none
      real(ki), dimension(:,:), intent(inout) :: vecs
      real(ki), dimension(2), intent(in) :: x

      real(ki), dimension(4,4) :: boost_matrix
      real(ki) :: x0, sx, dx
      integer i

      x0 = 2.0_ki * sqrt(x(1)*x(2))
      sx = (x(1)+x(2))/x0
      dx = (x(1)-x(2))/x0

      boost_matrix(1,:) = (/    sx, 0.0_ki, 0.0_ki,     dx/)
      boost_matrix(2,:) = (/0.0_ki, 1.0_ki, 0.0_ki, 0.0_ki/)
      boost_matrix(3,:) = (/0.0_ki, 0.0_ki, 1.0_ki, 0.0_ki/)
      boost_matrix(4,:) = (/    dx, 0.0_ki, 0.0_ki,     sx/)

      do i=lbound(vecs,1), ubound(vecs,1)
         vecs(i,1:4) = matmul(boost_matrix, vecs(i,1:4))
      end do
   end subroutine boost_a

   subroutine     rambo_process(s, vecs, weight)
      use [% process_name asprefix=\_ %]model
      implicit none

      real(ki), intent(in) :: s
      real(ki), dimension([%num_legs%],4), intent(out) :: vecs
      real(ki), intent(out), optional :: weight

      real(ki), dimension([%num_legs%]) :: masses

      [% @for particles %]
      masses([%index%]) = [% @if is_massive
        %][%mass%][% @else %]0.0_ki[% @end @if %][%
         @end @for %]


      if (present(weight)) then
         call rambo_b(s, masses, vecs, weight)
      else
         call rambo_b(s, masses, vecs)
      end if
   end subroutine rambo_process

   subroutine     rambo_b(s, masses, vecs, weight)
      implicit none
      real(ki), intent(in) :: s
      real(ki), dimension(:), intent(in) :: masses
      real(ki), dimension(size(masses),4), intent(out) :: vecs
      real(ki), intent(out), optional :: weight

      real(ki), dimension(4*(size(masses)-[%num_in%])) :: u

      call random_number(u)
      if (present(weight)) then
         call rambo_a(u, s, masses, vecs, weight)
      else
         call rambo_a(u, s, masses, vecs)
      end if
   end subroutine rambo_b

   subroutine     rambo_a(u, s, masses, vecs, weight)
      implicit none
      real(ki), dimension(:), intent(in) :: u
      real(ki), intent(in) :: s
      real(ki), dimension(:), intent(in) :: masses
      real(ki), dimension(size(masses),4), intent(out) :: vecs
      real(ki), intent(out), optional :: weight

      integer :: N, N_out, i
      real(ki) :: wgt, x, x2, S1, S2, P1, k0, k3, m

      N = size(masses)
      N_out = N - [%num_in%]
      [% @if eval num_in .eq. 2 %]
      call rambo_in(s, masses(1:2), vecs(1:2,:))[%
         @else %]
      vecs(1,1) = masses(1)
      vecs(1,2:4) = 0.0_ki[%
         @end @if %]
      if (N_out > 1) then
         wgt = rambo0(u, N_out, s, vecs([% eval num_in + 1 %]:N,:))

         x = newton(N_out, s, vecs([% eval num_in + 1 %]:N,:), masses([%
            eval num_in + 1%]:N))
         x2 = x * x

         do i = [% eval num_in + 1%], N
            m = masses(i)
            vecs(i, 1) = sqrt(m*m + x2 * vecs(i, 1) * vecs(i, 1))
            vecs(i, 2:4) = x * vecs(i, 2:4)
         end do

         if (present(weight)) then
            S1 = 0.0_ki
            S2 = 0.0_ki
            P1 = wgt * s ** (2 - N_out)

            do i = [% eval num_in + 1 %], N
               k0 = vecs(i, 1)
               ! k3 = (\vec(k_j))^2
               k3 = vecs(i,2)*vecs(i,2) + vecs(i,3)*vecs(i,3) &
                & + vecs(i,4)*vecs(i,4)

               S1 = S1 + sqrt(k3)
               S2 = S2 + k3 / k0
               P1 = P1 * sqrt(k3) / k0
            end do

            weight = S1 ** (2 * N_out - 3) * P1 / S2
         end if
      else
         do i = 1, 4
            vecs([% eval num_in + 1 %],i) = sum(vecs(1:[%num_in%],i))
         end do
      end if
   end subroutine rambo_a

   pure function newton(N, s, vecs, masses) result(x)
      implicit none
      integer, intent(in) :: N
      real(ki), intent(in) :: s
      real(ki), dimension(N), intent(in) :: masses
      real(ki), dimension(N,4), intent(in) :: vecs

      real(ki), parameter :: eps = epsilon(s) * 1.0E+03_ki

      real(ki) :: x, sqs, fx, fpx, x2, p0, p2, m, tmp
      integer :: i, limit

      x = 0.5_ki
      sqs = sqrt(s)
      fx = - sqs

      limit = 1000
      do while(abs(fx) > eps .and. limit > 0)
         limit = limit - 1
         fx = - sqs
         fpx = 0.0_ki
         x2 = x * x
         do i = 1, N
            p0 = vecs(i, 1)
            p2 = p0 * p0
            m  = masses(i)
            tmp = sqrt(m*m + x2 * p2)
            fx = fx + tmp
            fpx = fpx + p2 / tmp
         end do
         fpx = x * fpx
         x = x - fx / fpx
      end do
   end  function newton

   pure subroutine rambo_in(s, masses, vecs)
      implicit none
      real(ki), intent(in) :: s
      real(ki), dimension(2), intent(in) :: masses
      real(ki), dimension(2,4), intent(out) :: vecs

      real(ki) :: A, B, m12, m22, sqrts

      m12 = masses(1)*masses(1)
      m22 = masses(2)*masses(2)
      sqrts = 2.0_ki * sqrt(s)
      A = (s + m12 - m22) / sqrts
      B = (s + m22 - m12) / sqrts

      vecs(:, 2:3) = 0.0_ki
      vecs(1, 1) = A
      vecs(1, 4) = sqrt(A*A - m12)
      vecs(2, 1) = B
      vecs(2, 4) = -sqrt(B*B - m22)
   end  subroutine rambo_in

   function     rambo0(u, N, s, vecs) result(w0)
      implicit none
      integer, intent(in) :: N
      real(ki), dimension(4*N), intent(in) :: u
      real(ki), intent(in) :: s
      real(ki), dimension(N,4), intent(out) :: vecs

      real(ki) :: w0
      real(ki), dimension(N,4) :: q
      real(ki), dimension(4) :: v
      real(ki), dimension(2:4) :: b

      real(ki) :: u1, u2, u3, u4
      real(ki) :: cos_theta, sin_theta, phi, E
      real(ki) :: v2, gamma, a, x, bq
      integer :: i

      do i = 1, N
         u1 = u(4*(i-1)+1)
         u2 = u(4*(i-1)+2)
         u3 = u(4*(i-1)+3)
         u4 = u(4*(i-1)+4)

         cos_theta = u1 + u1 - 1.0_ki
         sin_theta = 2.0_ki * sqrt(u1 * (1.0_ki - u1))
         phi       = 2.0_ki * pi * u2
         E = -log(u3 * u4)

         q(i,1) = E
         q(i,2) = E * cos(phi) * sin_theta
         q(i,3) = E * sin(phi) * sin_theta
         q(i,4) = E * cos_theta
      end do
      v(:) = sum(q, dim=1)
      v2 = scalar(v, v)
      b(2:4) = - sqrt(1.0_ki/v2) * v(2:4)
      gamma = sqrt(1.0_ki + b(2)*b(2) + b(3)*b(3) + b(4)*b(4))
      a = 1.0_ki / (1.0_ki + gamma)
      x = sqrt(s/v2)

      do i = 1, N
        ! Lorentz transformation
        bq = b(2)*q(i,2) + b(3)*q(i,3) + b(4)*q(i,4)
        vecs(i, 1)   = (gamma*q(i,1) + bq)
        vecs(i, 2:4) = (b(2:4) * (q(i, 1) + a * bq) + q(i,2:4))
      end do

      ! Loss of precision here. Can this be avoided
      vecs(:,:) = x * vecs(:,:)

      w0 = (2.0_ki * pi) ** (4-3*N) * (pi/2.0_ki) ** (N - 1) * &
         & s ** (N - 2)

      do i = 2, N - 2
         w0 = w0 / real(i, ki) / real(i, ki)
      end do
      w0 = w0 / real(N-1, ki)
   end function rambo0
end module [% process_name asprefix=\_ %]rambo
