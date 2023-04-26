program test
   use pc16_gghh_config, only: ki, logfile, nlo_prefactors
   use pc16_gghh_kinematics, only: dotproduct, boost_to_cms
   use pc16_gghh_model, only: parse
   use pc16_gghh_matrix, only: samplitude, &
     & initgolem, exitgolem, ir_subtraction
   use pc16_gghh_color, only: numcs, CA
   use pc16_gghh_rambo, only: ramb

   implicit none

   integer :: NEVT = 1

   integer :: ievt, ierr, prec
   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2
   real(ki), dimension(0:3) :: amp
   real(ki), dimension(2:3) :: irp
   real(ki) :: t1, t2

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

   nlo_prefactors=0  ! Do not include any NLO prefactors in order to recognize
                     ! rational numbers for the pole coefficients

   call cpu_time(t1)
   do ievt = 1, NEVT
      call ramb(5.0E+02_ki**2, vecs)

      call boost_to_cms(vecs)

      scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

      call samplitude(vecs, scale2, amp, prec)
      call ir_subtraction(vecs, scale2, irp)
      if(ievt.eq.NEVT) then
         call print_parameters(scale2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, finite part:", amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, single pole:", amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NLO, double pole:", amp(3)


         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  single pole:", irp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  double pole:", irp(3)

      end if
   end do
   call cpu_time(t2)
   write(*,'(A1,1x,A17,1x,F23.3)') "#", "Time/Event [ms]:", &
      & 1.0E+03 * (t2 - t1) / real(NEVT)

   close(logfile)
   call exitgolem()

 contains

subroutine  print_parameters(scale2)
   use pc16_gghh_config, only: renormalisation, &
        convert_to_cdr, reduction_interoperation, &
        reduction_interoperation_rescue, PSP_check, PSP_rescue
   use pc16_gghh_model
   implicit none
   real(ki) :: scale2
   call print_parameter()


end subroutine print_parameters

end program test
