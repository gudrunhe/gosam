program test
   use pt19_gghh_config, only: ki, pt19_logfile => logfile, pt19_nlo_prefactors =>nlo_prefactors,reduction_interoperation, &
     & pt19_EFTcount => EFTcount
   use pt19_gghh_kinematics, only: dotproduct, boost_to_cms
   use pt19_gghh_model, only: pt19_parse => parse
   ! use pt19_gghh_model_qp, only: pt19_parse_qp => parse
   use pt19_gghh_matrix, only: pt19_samplitude => samplitude, &
     & pt19_initgolem=>initgolem, pt19_exitgolem=>exitgolem, pt19_ir_subtraction=>ir_subtraction
   use pt19_gghh_color, only: numcs, CA
   use pt19_gghh_rambo, only: ramb

   use pb1_gghh_config, only: pb1_logfile => logfile, pb1_nlo_prefactors =>nlo_prefactors, &
     & pb1_EFTcount => EFTcount
   use pb1_gghh_model, only: pb1_parse => parse
   use pb1_gghh_matrix, only: pb1_samplitude => samplitude, &
     & pb1_initgolem=>initgolem, pb1_exitgolem=>exitgolem, pb1_ir_subtraction=>ir_subtraction

   use pc16_gghh_config, only: pc16_logfile => logfile, pc16_nlo_prefactors =>nlo_prefactors,EFTcount, &
     & pc16_EFTcount => EFTcount
   use pc16_gghh_model, only: pc16_parse => parse
   use pc16_gghh_matrix, only: pc16_samplitude => samplitude, &
     & pc16_initgolem=>initgolem, pc16_exitgolem=>exitgolem, pc16_ir_subtraction=>ir_subtraction

   implicit none

   integer :: NEVT = 1

   integer :: ievt, ierr, prec, pt19_prec, pb1_prec, pc16_prec
   real(ki), dimension(4, 4) :: vecs
   real(ki) :: scale2
   real(ki), dimension(0:3) :: amp,pt19_amp,pb1_amp,pc16_amp,pc16_sub
   real(ki), dimension(2:3) :: irp
   real(ki) :: t1, t2

   ! reduction_interoperation=4

   open(unit=pt19_logfile,status='unknown',action='write',file='debug.xml')

   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pt19_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   ! open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   ! if(ierr .eq. 0) then
   !    call pt19_parse_qp(10)
   !    close(unit=10)
   ! else
   !    print*, "No file 'param.dat' found. Using defaults"
   ! end if
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pb1_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if
   open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
   if(ierr .eq. 0) then
      call pc16_parse(10)
      close(unit=10)
   else
      print*, "No file 'param.dat' found. Using defaults"
   end if

   call pt19_initgolem()
   call pb1_initgolem()
   call pc16_initgolem()

   call random_seed

   pt19_nlo_prefactors=0  ! Do not include any NLO prefactors in order to recognize
                     ! rational numbers for the pole coefficients
   pb1_nlo_prefactors=0
   pc16_nlo_prefactors=0

   if (pt19_EFTcount.eq.3) then
      pb1_EFTcount = 1
   endif

   call cpu_time(t1)
   do ievt = 1, NEVT
      call ramb(5.0E+02_ki**2, vecs)

      call boost_to_cms(vecs)

      scale2 = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))

      call pt19_samplitude(vecs, scale2, pt19_amp, pt19_prec)
      call pt19_exitgolem()
      call pb1_samplitude(vecs, scale2, pb1_amp, pb1_prec)
      call pc16_samplitude(vecs, scale2, pc16_amp, pc16_prec)

      if (pt19_EFTcount.eq.3) then
         pc16_EFTcount=1
         call pc16_samplitude(vecs, scale2, pc16_sub, pc16_prec)
         pc16_EFTcount=pt19_EFTcount
         amp=pt19_amp-pb1_amp-pc16_sub
         write(*,*) "pt19",pt19_amp
         write(*,*) "pb1",pb1_amp
         write(*,*) "pc16_sub",pc16_sub
         write(*,*) "pt19-pb1-pc16_sub",amp
      else
         amp=pt19_amp-pb1_amp
         write(*,*) "pt19",pt19_amp
         write(*,*) "pb1",pb1_amp
         write(*,*) "pt19-pb1",amp
      endif

      if(ievt.eq.NEVT) then
         call print_parameters(scale2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, finite part:", &
             &    amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, finite part:", &
             &    pc16_amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Ratio OLD/NEW:", &
             &    pc16_amp(1)/amp(1)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, single pole:", &
             &    amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, single pole:", &
             &    pc16_amp(2)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Discr OLD/NEW:", &
             &    1d0-abs(pc16_amp(2)-amp(2))/max(abs(pc16_amp(2)),abs(amp(2)))
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "NEW NLO, double pole:", &
             &    amp(3)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "OLD NLO, double pole:", &
             &    pc16_amp(3)
         write(*,'(A1,1x,A17,1x,G23.16)') "#", "--> Discr OLD/NEW:", &
             &    1d0-abs(pc16_amp(3)-amp(3))/max(abs(pc16_amp(3)),abs(amp(3)))


         ! write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  single pole:", &
         !    & irp(2)
         ! write(*,'(A1,1x,A17,1x,G23.16)') "#", "IR,  double pole:", &
         !    & irp(3)

      end if
   end do
   call cpu_time(t2)
   write(*,'(A1,1x,A17,1x,F23.3)') "#", "Time/Event [ms]:", &
      & 1.0E+03 * (t2 - t1) / real(NEVT)

   close(pt19_logfile)
   call pc16_exitgolem()
   call pb1_exitgolem()

 contains

subroutine  print_parameters(scale2)
   use pt19_gghh_config, only: renormalisation, &
        convert_to_cdr, reduction_interoperation, &
        reduction_interoperation_rescue, PSP_check, PSP_rescue
   use pt19_gghh_model
   implicit none
   real(ki) :: scale2
   call print_parameter()


end subroutine print_parameters

end program test
