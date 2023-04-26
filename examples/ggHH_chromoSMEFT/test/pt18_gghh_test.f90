program pt18_gghh_test
   use pt18_gghh_config, only: ki, pt18_logfile => logfile, pt18_nlo_prefactors =>nlo_prefactors,reduction_interoperation, &
     & pt18_EFTcount => EFTcount
   use pt18_gghh_kinematics, only: dotproduct, boost_to_cms
   use pt18_gghh_model, only: pt18_parse => parse
   ! use pt18_gghh_model_qp, only: pt18_parse_qp => parse
   use pt18_gghh_matrix, only: pt18_samplitude => samplitude, &
     & pt18_initgolem=>initgolem, pt18_exitgolem=>exitgolem, pt18_ir_subtraction=>ir_subtraction
   use pt18_gghh_color, only: numcs, CA
   use pt18_gghh_rambo, only: ramb

   use pb0_gghh_config, only: pb0_logfile => logfile, pb0_nlo_prefactors =>nlo_prefactors, &
     & pb0_EFTcount => EFTcount
   use pb0_gghh_model, only: pb0_parse => parse
   use pb0_gghh_matrix, only: pb0_samplitude => samplitude, &
     & pb0_initgolem=>initgolem, pb0_exitgolem=>exitgolem, pb0_ir_subtraction=>ir_subtraction

   use pc17_gghh_config, only: pc17_logfile => logfile, pc17_nlo_prefactors =>nlo_prefactors, &
     & pc17_EFTcount => EFTcount
   use pc17_gghh_model, only: pc17_parse => parse
   use pc17_gghh_matrix, only: pc17_samplitude => samplitude, &
     & pc17_initgolem=>initgolem, pc17_exitgolem=>exitgolem, pc17_ir_subtraction=>ir_subtraction

   implicit none

   integer :: NEVT = 1

   integer :: ievt, ierr, prec, pt18_prec, pb0_prec, pc17_prec
   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2
   real(ki), dimension(0:3) :: amp,pt18_amp,pb0_amp,pc17_amp
   real(ki), dimension(2:3) :: irp
   real(ki) :: t1, t2

   open(unit=pt18_logfile,status='unknown',action='write',file='debug.xml')

   ! reduction_interoperation=4
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pt18_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   ! open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   ! if(ierr .eq. 0) then
   !    call pt18_parse_qp(10)
   !    close(unit=10)
   ! else
   !    print*, "No file 'param.dat' found. Using defaults"
   ! end if
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pb0_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pc17_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if

   call pt18_initgolem()
   call pb0_initgolem()
   call pc17_initgolem()

   call random_seed

   pt18_nlo_prefactors=0  ! Do not include any NLO prefactors in order to recognize
                     ! rational numbers for the pole coefficients
   pb0_nlo_prefactors=0
   pc17_nlo_prefactors=0

   call cpu_time(t1)
   do ievt = 1, NEVT
      call ramb(5.0E+02_ki**2, vecs)

      call boost_to_cms(vecs)

      scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))


      call pb0_samplitude(vecs, scale2, pb0_amp, pb0_prec)
      call pc17_samplitude(vecs, scale2, pc17_amp, pc17_prec)
      call pc17_exitgolem()

      ! amp=pt18_amp
      ! if (pt18_EFTcount.ne.1) then
      ! endif
      ! write(*,*) vecs
      write(*,*) "p12", dotproduct(vecs(1,:), vecs(2,:))
      write(*,*) "p13", dotproduct(vecs(1,:), vecs(3,:))
      call pt18_samplitude(vecs, scale2, pt18_amp, pt18_prec)
      amp=pt18_amp-pb0_amp

      write(*,*) "pt18",pt18_amp
      write(*,*) "pb0",pb0_amp
      write(*,*) "pt18-pb0",amp
      ! call ir_subtraction(vecs, scale2, irp)
      if(ievt.eq.NEVT) then
         ! call print_parameters(scale2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW LO:", amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD LO:", pc17_amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Ratio OLD/NEW:", pc17_amp(0)/amp(0)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, finite part:", &
             &    amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, finite part:", &
             &    pc17_amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Ratio OLD/NEW:", pc17_amp(1)/amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, single pole:", &
             &    amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, single pole:", &
             &    pc17_amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Ratio OLD/NEW:", pc17_amp(2)/amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, double pole:", &
             &    amp(3)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, double pole:", &
             &    pc17_amp(3)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Ratio OLD/NEW:", pc17_amp(3)/amp(3)


         ! write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  single pole:", &
         !    & irp(2)/amp(0)
         ! write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  double pole:", &
         !    & irp(3)/amp(0)

      end if
   end do
   call cpu_time(t2)
   write(*,'(A1,1x,A17,1x,F23.3)') "#", "Time/Event [ms]:", &
      & 1.0E+03 * (t2 - t1) / real(NEVT)

   close(pt18_logfile)
   call pt18_exitgolem()
   call pb0_exitgolem()

 contains

subroutine  print_parameters(scale2)
   use pt18_gghh_config, only: renormalisation, &
        convert_to_cdr, reduction_interoperation, &
        reduction_interoperation_rescue, PSP_check, PSP_rescue
   use pt18_gghh_model
   implicit none
   real(ki) :: scale2
   call print_parameter()


end subroutine print_parameters

end program pt18_gghh_test
