module    pc17_gghh_amplitudeh0_1
   use pc17_gghh_config, only: ki, &
       & reduction_interoperation
   use pc17_gghh_color, only: numcs
   use pc17_gghh_groups
   use precision_golem, only: ki_gol => ki
   use pc17_gghh_golem95_1h0
   
   implicit none
   private

   public :: finite_renormalisation, samplitude
contains
!---#[ function finite_renormalisation:
   function     finite_renormalisation(scale2) result(amp)
      use pc17_gghh_util, only: square
      use pc17_gghh_color, only: CF, CA
      use pc17_gghh_kinematics, only: &
      & num_light_quarks, num_gluons
      use pc17_gghh_diagramsh0l0_1, only: amplitudel0 => amplitude
      implicit none
      real(ki), intent(in) :: scale2
      real(ki) :: amp
      amp = 0.0_ki
   end function finite_renormalisation
   !---#] function finite_renormalisation:

   !---#[ function samplitude:
   function     samplitude(scale2,ok,rational2,opt_amp0,opt_perm)
      use pc17_gghh_config, only: include_eps_terms, include_eps2_terms, &
      & logfile, debug_nlo_diagrams
      use pc17_gghh_globalsl1, only: amp0,perm, use_perm, epspow
      use pc17_gghh_globalsh0, &
     & only: init_lo, rat2
      use pc17_gghh_abbrevd33_1h0, only: init_abbrevd33 => init_abbrev
      use pc17_gghh_abbrevd5_1h0, only: init_abbrevd5 => init_abbrev
      use pc17_gghh_abbrevd12_1h0, only: init_abbrevd12 => init_abbrev
      use pc17_gghh_abbrevd14_1h0, only: init_abbrevd14 => init_abbrev
      use pc17_gghh_abbrevd31_1h0, only: init_abbrevd31 => init_abbrev
      use pc17_gghh_abbrevd1_1h0, only: init_abbrevd1 => init_abbrev
      use pc17_gghh_abbrevd2_1h0, only: init_abbrevd2 => init_abbrev
      use pc17_gghh_abbrevd3_1h0, only: init_abbrevd3 => init_abbrev
      use pc17_gghh_abbrevd4_1h0, only: init_abbrevd4 => init_abbrev
      use pc17_gghh_abbrevd7_1h0, only: init_abbrevd7 => init_abbrev
      use pc17_gghh_abbrevd8_1h0, only: init_abbrevd8 => init_abbrev
      use pc17_gghh_abbrevd10_1h0, only: init_abbrevd10 => init_abbrev
      use pc17_gghh_abbrevd16_1h0, only: init_abbrevd16 => init_abbrev
      use pc17_gghh_abbrevd18_1h0, only: init_abbrevd18 => init_abbrev
      use pc17_gghh_abbrevd22_1h0, only: init_abbrevd22 => init_abbrev
      use pc17_gghh_abbrevd23_1h0, only: init_abbrevd23 => init_abbrev
      use pc17_gghh_abbrevd27_1h0, only: init_abbrevd27 => init_abbrev
      use pc17_gghh_abbrevd29_1h0, only: init_abbrevd29 => init_abbrev
      use pc17_gghh_diagramsh0l0_1, only: amplitudel0 => amplitude
      use pc17_gghh_groups
      implicit none
      real(ki), intent(in) :: scale2
      logical, intent(out) :: ok
      real(ki), intent(out) :: rational2
      complex(ki), dimension(numcs), intent(in), optional :: opt_amp0
      integer, dimension(numcs), intent(in), optional :: opt_perm
      real(ki), dimension(-2:0) :: samplitude

      real(ki), dimension(-2:0) :: acc
      real(ki), dimension(0:2,-2:0) :: samp_part

      logical :: acc_ok

      ok = .true.
      rational2 = 0.0_ki

      samplitude(:) = 0.0_ki
      if (present(opt_amp0)) then
         amp0 = opt_amp0
      else
         amp0 = amplitudel0()
      end if
      if (present(opt_perm)) then
         use_perm = .true.
         perm = opt_perm
      else
         use_perm = .false.
      end if

      rat2 = (0.0_ki, 0.0_ki)
      call init_lo()
        call init_abbrevd33()
        call init_abbrevd5()
        call init_abbrevd12()
        call init_abbrevd14()
        call init_abbrevd31()
        call init_abbrevd1()
        call init_abbrevd2()
        call init_abbrevd3()
        call init_abbrevd4()
        call init_abbrevd7()
        call init_abbrevd8()
        call init_abbrevd10()
        call init_abbrevd16()
        call init_abbrevd18()
        call init_abbrevd22()
        call init_abbrevd23()
        call init_abbrevd27()
        call init_abbrevd29()
      epspow=0
      samplitude(-2) = 0.0_ki
      samplitude(-1) = 0.0_ki
      if(debug_nlo_diagrams) then
         write(logfile,'(A22,G24.16,A6,G24.16,A4)') &
         & "<result name='r2' re='", real(rat2, ki), &
         &                 "' im='", aimag(rat2), "' />"
      end if
      rational2 = 2.0_ki * real(rat2, ki)
      samplitude(0) = 2.0_ki * real(rat2, ki)
         call evaluate_group0(scale2, acc, acc_ok)
         ok = ok .and. acc_ok
         samplitude(:) = samplitude(:) + acc
         call evaluate_group1(scale2, acc, acc_ok)
         ok = ok .and. acc_ok
         samplitude(:) = samplitude(:) + acc
         call evaluate_group2(scale2, acc, acc_ok)
         ok = ok .and. acc_ok
         samplitude(:) = samplitude(:) + acc
   end function samplitude
   !---#] function samplitude:
!---#[ subroutine evaluate_group0:
subroutine     evaluate_group0(scale2,samplitude,ok)
   use pc17_gghh_config, only: &
      & logfile, debug_nlo_diagrams
   use pc17_gghh_globalsl1, only: epspow
   use parametre, only: mu2_scale_par
   use form_factor_type, only: form_factor
   use pc17_gghh_golem95_1h0, only: reconstruct_golem95 => reconstruct_group
   use pc17_gghh_groups, only: contract_golem95
   implicit none
   real(ki), intent(in) :: scale2
   logical, intent(out) :: ok
   real(ki), dimension(-2:0), intent(out) :: samplitude
   type(tensrec_info_group0), target :: coeffs
   type(form_factor) :: gres

   if(debug_nlo_diagrams) then
      write(logfile,*) "<diagram-group index='0'>"
      write(logfile,*) "<param name='epspow' value='", epspow, "'/>"
   end if
   select case(reduction_interoperation)
   case(1) ! use Golem95 only
      call reconstruct_golem95(coeffs)
      mu2_scale_par = real(scale2, ki_gol)
      gres = contract_golem95(coeffs)
      samplitude(-2) = 2.0_ki * real(gres%A, ki)
      samplitude(-1) = 2.0_ki * real(gres%B, ki)
      samplitude( 0) = 2.0_ki * real(gres%C, ki)
      ok = .true.
   case default
      print*, "Your current choice of reduction_interoperation is", &
            & reduction_interoperation
      print*, "This choice is not valid for your current setup."
      print*, "* This code was generated without support for Samurai."
      print*, "* This code was generated without support for Ninja."
      print*, "* This code was generated with support for Golem95."
      print*, "* This code was generated without support for PJFry."
   end select

   if(debug_nlo_diagrams) then
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-finite' value='", samplitude(0), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-single' value='", samplitude(-1), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-double' value='", samplitude(-2), "'/>"
      if(ok) then
         write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
      else
         write(logfile,'(A29)') "<flag name='ok' status='no'/>"
      end if
      write(logfile,*) "</diagram-group>"
   end if
end subroutine evaluate_group0
!---#] subroutine evaluate_group0:
!---#[ subroutine evaluate_group1:
subroutine     evaluate_group1(scale2,samplitude,ok)
   use pc17_gghh_config, only: &
      & logfile, debug_nlo_diagrams
   use pc17_gghh_globalsl1, only: epspow
   use parametre, only: mu2_scale_par
   use form_factor_type, only: form_factor
   use pc17_gghh_golem95_1h0, only: reconstruct_golem95 => reconstruct_group
   use pc17_gghh_groups, only: contract_golem95
   implicit none
   real(ki), intent(in) :: scale2
   logical, intent(out) :: ok
   real(ki), dimension(-2:0), intent(out) :: samplitude
   type(tensrec_info_group1), target :: coeffs
   type(form_factor) :: gres

   if(debug_nlo_diagrams) then
      write(logfile,*) "<diagram-group index='1'>"
      write(logfile,*) "<param name='epspow' value='", epspow, "'/>"
   end if
   select case(reduction_interoperation)
   case(1) ! use Golem95 only
      call reconstruct_golem95(coeffs)
      mu2_scale_par = real(scale2, ki_gol)
      gres = contract_golem95(coeffs)
      samplitude(-2) = 2.0_ki * real(gres%A, ki)
      samplitude(-1) = 2.0_ki * real(gres%B, ki)
      samplitude( 0) = 2.0_ki * real(gres%C, ki)
      ok = .true.
   case default
      print*, "Your current choice of reduction_interoperation is", &
            & reduction_interoperation
      print*, "This choice is not valid for your current setup."
      print*, "* This code was generated without support for Samurai."
      print*, "* This code was generated without support for Ninja."
      print*, "* This code was generated with support for Golem95."
      print*, "* This code was generated without support for PJFry."
   end select

   if(debug_nlo_diagrams) then
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-finite' value='", samplitude(0), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-single' value='", samplitude(-1), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-double' value='", samplitude(-2), "'/>"
      if(ok) then
         write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
      else
         write(logfile,'(A29)') "<flag name='ok' status='no'/>"
      end if
      write(logfile,*) "</diagram-group>"
   end if
end subroutine evaluate_group1
!---#] subroutine evaluate_group1:
!---#[ subroutine evaluate_group2:
subroutine     evaluate_group2(scale2,samplitude,ok)
   use pc17_gghh_config, only: &
      & logfile, debug_nlo_diagrams
   use pc17_gghh_globalsl1, only: epspow
   use parametre, only: mu2_scale_par
   use form_factor_type, only: form_factor
   use pc17_gghh_golem95_1h0, only: reconstruct_golem95 => reconstruct_group
   use pc17_gghh_groups, only: contract_golem95
   implicit none
   real(ki), intent(in) :: scale2
   logical, intent(out) :: ok
   real(ki), dimension(-2:0), intent(out) :: samplitude
   type(tensrec_info_group2), target :: coeffs
   type(form_factor) :: gres

   if(debug_nlo_diagrams) then
      write(logfile,*) "<diagram-group index='2'>"
      write(logfile,*) "<param name='epspow' value='", epspow, "'/>"
   end if
   select case(reduction_interoperation)
   case(1) ! use Golem95 only
      call reconstruct_golem95(coeffs)
      mu2_scale_par = real(scale2, ki_gol)
      gres = contract_golem95(coeffs)
      samplitude(-2) = 2.0_ki * real(gres%A, ki)
      samplitude(-1) = 2.0_ki * real(gres%B, ki)
      samplitude( 0) = 2.0_ki * real(gres%C, ki)
      ok = .true.
   case default
      print*, "Your current choice of reduction_interoperation is", &
            & reduction_interoperation
      print*, "This choice is not valid for your current setup."
      print*, "* This code was generated without support for Samurai."
      print*, "* This code was generated without support for Ninja."
      print*, "* This code was generated with support for Golem95."
      print*, "* This code was generated without support for PJFry."
   end select

   if(debug_nlo_diagrams) then
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-finite' value='", samplitude(0), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-single' value='", samplitude(-1), "'/>"
      write(logfile,'(A33,E24.16,A3)') &
         & "<result kind='nlo-double' value='", samplitude(-2), "'/>"
      if(ok) then
         write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
      else
         write(logfile,'(A29)') "<flag name='ok' status='no'/>"
      end if
      write(logfile,*) "</diagram-group>"
   end if
end subroutine evaluate_group2
!---#] subroutine evaluate_group2:
end module pc17_gghh_amplitudeh0_1
