C [% ' vim: syntax=golem
   %]
      program ph_test
      use [% process_name asprefix=\_ %]powheg, only: init_event
      use [% process_name asprefix=\_ %]rambo, only: ramb
      implicit none

C - born : double precision
C     | the Born level matrix element squared
      double precision [% process_name asprefix=\_ %]born
C - virt_finite, virt_single, virt_double : double precision
C     | the coefficients of the virtual part of the matrix element.
      double precision [% process_name asprefix=\_ %]virt_finite
      double precision [% process_name asprefix=\_ %]virt_single
      double precision [% process_name asprefix=\_ %]virt_double
      
C - borncc : double precision, dimension(<number of legs>,<number of legs>)
C     | the color correlated Born level matrix element squared
      double precision [% process_name asprefix=\_ 
         %]borncc([%num_legs%],[%num_legs%])
C - bornsc : double precision, dimension(<number of legs>,4,4)
C     | the spin correlated Born level matrix element
      double precision [% process_name asprefix=\_
         %]bornsc([%num_legs%],4,4)

C - momenta : double precision, dimension(<number of legs>, 4)
C     | list of physical momenta, energy components are
C     | in momenta(:,1).
      double precision momenta([%num_legs%],4)
C - scale2 : double precision
C     | the square of the renormalisation scale.
      double precision scale2

      double precision acc
      integer I,J

      call random_seed
      call ramb(1.0d0, momenta)

      scale2 = 1.0d0

      call init_event(scale2,momenta,
     &[% process_name asprefix=\_ %]born,
     &[% process_name asprefix=\_ %]virt_finite,
     &[% process_name asprefix=\_ %]virt_single,
     &[% process_name asprefix=\_ %]virt_double,
     &[% process_name asprefix=\_ 
         %]borncc,
     &[% process_name asprefix=\_
         %]bornsc)

      if ([% process_name asprefix=\_ %]born < 0.0d0) then
         print*, "This event has been marked as BAD POINT"
         stop
      end if
      print*, [% process_name asprefix=\_ %]born
      print*, [% process_name asprefix=\_ %]virt_finite
      print*, [% process_name asprefix=\_ %]virt_single / [%
         process_name asprefix=\_ %]born
      print*, [% process_name asprefix=\_ %]virt_double / [%
         process_name asprefix=\_ %]born

C check the relations for the color correlated born
      do I=1,[%num_legs%]
         acc = 0.0d0
         do J=1,[%num_legs%]
            if (I.ne.J) acc = acc + [%
   process_name asprefix=\_ %]borncc(I,J)/[% process_name asprefix=\_ %]born
         end do
         write (*,'(A17,1x,I1,A1,1x,F23.15,A1,F23.15)') 
     &          "CC-BORN, PARTICLE", I, ":",
     &          acc, "=", -[%
   process_name asprefix=\_ %]borncc(I,I)/[% process_name asprefix=\_ %]born
      end do

[% @for particles lightlike vector %][%
      @if is_first%]
C check the relations for the spin correlated born[%
      @end @if%]
C particle [% index %]
      acc = [% process_name asprefix=\_ %]bornsc([%index%],1,1) - [%
        process_name asprefix=\_ %]bornsc([%index%],2,2)
     &    - [% process_name asprefix=\_ %]bornsc([%index%],3,3) - [%
        process_name asprefix=\_ %]bornsc([%index%],4,4)
      write (*,'(A17,1x,I1,A1,1x,F23.15,A1,F23.15)') 
     &          "SC-BORN, PARTICLE", [%index%], ":",
     &          acc, "=", -[% process_name asprefix=\_ %]born[%
   @end @for %]
      end program ph_test
