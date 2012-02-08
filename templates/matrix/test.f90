[% ' vim: syntax=golem
 %]program test
   use [% process_name asprefix=\_ %]config, only: ki, logfile
   use [% process_name asprefix=\_ %]kinematics, only: dotproduct
   use [% process_name asprefix=\_ %]model, only: parse
   use [% process_name asprefix=\_ %]matrix, only: samplitude, &
     & initgolem, ir_subtraction
   use [% process_name asprefix=\_ %]color, only: numcs, CA
   use [% process_name asprefix=\_ %]rambo, only: ramb

   implicit none

   integer :: NEVT = 1

   integer :: ievt, ierr
   real(ki), dimension([%num_legs%], 4) :: vecs
   real(ki) :: scale2
   real(ki), dimension(0:3) :: amp
   real(ki), dimension(2:3) :: irp
   real :: t1, t2

   open(unit=logfile,status='unknown',action='write',file='debug.xml')

   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if

   call initgolem()

   call random_seed

   call cpu_time(t1)
   do ievt = 1, NEVT
      call ramb(5.0E+02_ki**2, vecs)

      scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

      call samplitude(vecs, scale2, amp)
      call ir_subtraction(vecs, scale2, irp)
      if(ievt.eq.NEVT) then[%
      @if generate_lo_diagrams %]
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "LO:", amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, finite part:", &
             &    amp(1)/amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, single pole:", &
             &    amp(2)/amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, double pole:", &
             &    amp(3)/amp(0)
      [% @else %]
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, finite part:", amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, single pole:", amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, double pole:", amp(3)
      [% @end @if %]
      [%
      @if generate_lo_diagrams %]
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  single pole:", &
            & irp(2)/amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  double pole:", &
            & irp(3)/amp(0)
      [% @else %]
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  single pole:", irp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  double pole:", irp(3)
      [% @end @if %]
      end if
   end do
   call cpu_time(t2)
   write(*,'(A1,1x,A17,1x,F23.3)') "#", "Time/Event [ms]:", &
      & 1.0E+03 * (t2 - t1) / real(NEVT)

   close(logfile)
end program test
