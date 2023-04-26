module     pb0_gghh_kinematics
   use pb0_gghh_config, only: ki
   use pb0_gghh_model
   use pb0_gghh_scalar_cache
   implicit none
   save

   private

   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   real(ki), parameter :: sqrthalf = &
   & 0.7071067811865475244008443621048490392848359376884740365883398689_ki

   integer, parameter, public :: num_legs = 4
   integer, parameter, public :: num_light_quarks = 0
   integer, parameter, public :: num_heavy_quarks = 0
   integer, parameter, public :: num_quarks = 0
   integer, parameter, public :: num_gluons = 2
   integer, parameter, public :: lo_qcd_couplings = -2
   logical, parameter, public :: corrections_are_qcd = .true.
   integer, parameter, public :: in_helicities = 4
   integer, parameter, public :: symmetry_factor = 2
   real(ki), parameter, public :: es1 = 0.0_ki
   real(ki), parameter, public :: es2 = 0.0_ki
   
   real(ki), public :: es12
   real(ki), public :: es4
   real(ki), public :: es23
   real(ki), public :: es3
   
   complex(ki), public :: spak1k2, spbk2k1
   complex(ki), public :: spak1l3, spbl3k1
   complex(ki), public :: spak1l4, spbl4k1
   complex(ki), public :: spak2l3, spbl3k2
   complex(ki), public :: spak2l4, spbl4k2
   complex(ki), public :: spal3l4, spbl4l3
   complex(ki), dimension(4), public :: spvak1k2
   complex(ki), dimension(4), public :: spvak1l3
   complex(ki), dimension(4), public :: spvak1l4
   complex(ki), dimension(4), public :: spvak2k1
   complex(ki), dimension(4), public :: spvak2l3
   complex(ki), dimension(4), public :: spvak2l4
   complex(ki), dimension(4), public :: spval3k1
   complex(ki), dimension(4), public :: spval3k2
   complex(ki), dimension(4), public :: spval3l4
   complex(ki), dimension(4), public :: spval4k1
   complex(ki), dimension(4), public :: spval4k2
   complex(ki), dimension(4), public :: spval4l3
   real(ki), dimension(4), public :: k1
   real(ki), dimension(4), public :: k2
   real(ki), dimension(4), public :: k3
   real(ki), dimension(4), public :: k4
   real(ki), dimension(4), public :: l3
   real(ki), dimension(4), public :: l4

   ! Polarisation vectors and related symbols
   complex(ki), dimension(4), public :: e1
   complex(ki), dimension(4), public :: e2
   complex(ki), public :: spak1e1, spbe1k1
   complex(ki), public :: spae1k1, spbk1e1
   complex(ki), public :: spak1e2, spbe2k1
   complex(ki), public :: spae1k2, spbk2e1
   complex(ki), public :: spae1l3, spbl3e1
   complex(ki), public :: spae1l4, spbl4e1
   complex(ki), public :: spak2e2, spbe2k2
   complex(ki), public :: spae2k2, spbk2e2
   complex(ki), public :: spae2l3, spbl3e2
   complex(ki), public :: spae2l4, spbl4e2
   complex(ki), public :: spae1e2, spbe2e1
   complex(ki), dimension(4), public :: spvak1e1, spvae1k1
   complex(ki), dimension(4), public :: spvak1e2, spvae2k1
   complex(ki), dimension(4), public :: spvak2e1, spvae1k2
   complex(ki), dimension(4), public :: spvak2e2, spvae2k2
   complex(ki), dimension(4), public :: spval3e1, spvae1l3
   complex(ki), dimension(4), public :: spval3e2, spvae2l3
   complex(ki), dimension(4), public :: spval4e1, spvae1l4
   complex(ki), dimension(4), public :: spval4e2, spvae2l4
   complex(ki), dimension(4), public :: spvae1e2, spvae2e1

   interface epsi
      module procedure epsi0
      module procedure epsim
   end interface

   interface epso
      module procedure epso0
      module procedure epsom
   end interface

   interface dotproduct
      module procedure dotproduct_rr
      module procedure dotproduct_rc
      module procedure dotproduct_cr
      module procedure dotproduct_cc
   end interface dotproduct

   interface Spab3
      module procedure Spab3_complex
      module procedure Spab3_mcfm
      module procedure Spab3_mcfmc
      module procedure Spab3_vec
   end interface

   interface Spba3
      module procedure Spba3_complex
      module procedure Spba3_real
   end interface

   interface epstensor
      module procedure e_first_cmplx
      module procedure e_real
      module procedure e_real_idx
   end interface

   public :: Spaa, Spbb, Spab3, Spba3, dotproduct, epstensor
   public :: inspect_kinematics, init_event
   public :: adjust_kinematics
   public :: boost_to_cms
   public :: lambda
   public :: epsi, epso

contains
   ! This is the contracted epsilon tensor in Schoonschip notation
   ! adapted from golem95 version 1.3.0
   !
   ! Note: The final multiplication with i_ is due to FORM's metric
   !       independent treatment of the Dirac algebra.
   !       In particular gamma5(FORM) is defined as gamma5(usual)/i.
   pure function e_real(k1,k2,k3,k4) result(res)
      real(ki), intent (in), dimension(4) :: k1, k2, k3, k4
      complex(ki) :: res

      real(ki) :: k12, k23, k34, k13, k14, k24, tmp

      k12 = k3(1)*k4(2)-k3(2)*k4(1)
      k23 = k3(2)*k4(3)-k3(3)*k4(2)
      k34 = k3(3)*k4(4)-k3(4)*k4(3)
      k13 = k3(1)*k4(3)-k3(3)*k4(1)
      k14 = k3(1)*k4(4)-k3(4)*k4(1)
      k24 = k3(2)*k4(4)-k3(4)*k4(2)

      tmp =  k1(1)*(k2(2)*k34 - k2(3)*k24 + k2(4)*k23)&
      &    + k1(2)*(k2(3)*k14 - k2(1)*k34 - k2(4)*k13)&
      &    + k1(3)*(k2(1)*k24 - k2(2)*k14 + k2(4)*k12)&
      &    + k1(4)*(k2(2)*k13 - k2(1)*k23 - k2(3)*k12)

      res =  i_*tmp

   end function e_real

   pure function  e_first_cmplx(k1,k2,k3,k4) result(res)
      complex(ki), intent (in), dimension(4) :: k1
      real(ki), intent (in), dimension(4) :: k2, k3, k4
      complex(ki) :: res

      res = e_real(real(k1),k2,k3,k4) + i_*e_real(aimag(k1),k2,k3,k4)

    end function e_first_cmplx

   pure function e_real_idx(idx,k1,k2,k3) result(res)
      real(ki), intent (in), dimension(4) :: k1, k2, k3
      integer, intent(in) :: idx
      real(ki), dimension(1:4) :: idxvec
      complex(ki) :: res
      idxvec = (/0.0_ki,0.0_ki,0.0_ki,0.0_ki/)
      ! Minkowski metric
      if (idx==1) then
         idxvec(idx) = 1.0_ki
      else
         idxvec(idx) = -1.0_ki
      end if
      res = e_real(idxvec,k1,k2,k3)
   end function e_real_idx

!---#[ subroutine inspect_kinematics:
   subroutine     inspect_kinematics(unit)
      implicit none
      integer, optional, intent(in) :: unit
      real(ki), dimension(4) :: zero
      integer :: ch

      if (present(unit)) then
         ch = unit
      else
         ch = 5
      end if
      zero(:) = 0.0_ki
      
      write(ch,*) "<momentum index='1' inout='in'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k1(1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k1(2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k1(3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k1(4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real(0, ki), "'/>"
      write(ch,*) "<!-- k1.k1 = ", &
         & dotproduct(k1,k1), "-->"
      write(ch,*) "</momentum>"
      write(ch,*) "<momentum index='2' inout='in'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k2(1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k2(2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k2(3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k2(4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real(0, ki), "'/>"
      write(ch,*) "<!-- k2.k2 = ", &
         & dotproduct(k2,k2), "-->"
      write(ch,*) "</momentum>"
      write(ch,*) "<momentum index='3' inout='out'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k3(1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k3(2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k3(3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k3(4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real(mdlMh, ki), "'/>"
      write(ch,*) "<!-- k3.k3 = ", &
         & dotproduct(k3,k3), "-->"
      write(ch,*) "</momentum>"
      write(ch,*) "<momentum index='4' inout='out'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k4(1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k4(2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k4(3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k4(4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real(mdlMh, ki), "'/>"
      write(ch,*) "<!-- k4.k4 = ", &
         & dotproduct(k4,k4), "-->"
      write(ch,*) "</momentum>"
      write(ch,*) "<!-- es12 = ", es12, "-->"
      write(ch,*) "<!-- es4 = ", es4, "-->"
      write(ch,*) "<!-- es23 = ", es23, "-->"
      write(ch,*) "<!-- es3 = ", es3, "-->"
   end subroutine inspect_kinematics
!---#] subroutine inspect_kinematics:
!---#[ subroutine init_event:
   subroutine     init_event(vecs, hel1, hel2)
      use pb0_gghh_config, only: debug_numpolvec, logfile
      use pb0_gghh_model
      implicit none
      real(ki), dimension(num_legs,4), intent(in) :: vecs
      integer, intent(in), optional :: hel1
      integer, intent(in), optional :: hel2
      complex(ki) :: N1
      logical :: flag1
      complex(ki) :: N2
      logical :: flag2

      call invalidate_cache()
      k1 = vecs(1,:)
      k2 = vecs(2,:)
      k3 = vecs(3,:)
      k4 = vecs(4,:)
      ! mass1 = 'mdlMh', mass2 = '0'
      call light_cone_decomposition(k3, l3, k2, mdlMh)
      ! mass1 = 'mdlMh', mass2 = '0'
      call light_cone_decomposition(k4, l4, k2, mdlMh)
      es12 = 2.0_ki*dotproduct(vecs(1,:), vecs(2,:))
      es4 = mdlMh**2
      es23 = 2.0_ki*dotproduct(vecs(2,:), -vecs(3,:))&
            & + mdlMh**2
      es3 = mdlMh**2
      spak1k2 = Spaa(k1, k2)
      spbk2k1 = Spbb(k2, k1)
      spak1l3 = Spaa(k1, l3)
      spbl3k1 = Spbb(l3, k1)
      spak1l4 = Spaa(k1, l4)
      spbl4k1 = Spbb(l4, k1)
      spak2l3 = Spaa(k2, l3)
      spbl3k2 = Spbb(l3, k2)
      spak2l4 = Spaa(k2, l4)
      spbl4k2 = Spbb(l4, k2)
      spal3l4 = Spaa(l3, l4)
      spbl4l3 = Spbb(l4, l3)
      spvak1k2 = Spab3_vec(k1, k2)
      spvak1l3 = Spab3_vec(k1, l3)
      spvak1l4 = Spab3_vec(k1, l4)
      spvak2k1 = Spab3_vec(k2, k1)
      spvak2l3 = Spab3_vec(k2, l3)
      spvak2l4 = Spab3_vec(k2, l4)
      spval3k1 = Spab3_vec(l3, k1)
      spval3k2 = Spab3_vec(l3, k2)
      spval3l4 = Spab3_vec(l3, l4)
      spval4k1 = Spab3_vec(l4, k1)
      spval4k2 = Spab3_vec(l4, k2)
      spval4l3 = Spab3_vec(l4, l3)
      if(.true. .and. present(hel1) .and. present(hel2)) then
         select case(hel1)
         case(1)
            flag1 = .false.
            N1 = sqrt2*Spaa(k2,k1)
            e1 = spvak2k1/N1
         case(-1)
            flag1 = .true.
            N1 = sqrt2*Spbb(k1,k2)
            e1 = spvak1k2/N1
         case default
            print*, "Illegal helicity for particle 1:", hel1
            stop
         end select
         N1 = sqrt(2.0_ki/N1)
         select case(hel2)
         case(1)
            flag2 = .false.
            N2 = sqrt2*Spaa(k1,k2)
            e2 = spvak1k2/N2
         case(-1)
            flag2 = .true.
            N2 = sqrt2*Spbb(k2,k1)
            e2 = spvak2k1/N2
         case default
            print*, "Illegal helicity for particle 2:", hel2
            stop
         end select
         N2 = sqrt(2.0_ki/N2)
         if(flag1) then
            spak1e1 = 0.0_ki
            spbe1k1 = N1 * Spbb(k2, k1)
         else
            spak1e1 = N1 * Spaa(k1, k2)
            spbe1k1 = 0.0_ki
         end if
         if(flag1) then
            spae1k1 = 0.0_ki
            spbk1e1 = N1 * Spbb(k1, k2)
         else
            spae1k1 = N1 * Spaa(k2, k1)
            spbk1e1 = 0.0_ki
         end if
         if(flag2) then
            spak1e2 = N2 * Spaa(k1, k2)
            spbe2k1 = 0.0_ki
         else
            spak1e2 = 0.0_ki
            spbe2k1 = N2 * Spbb(k2, k1)
         end if
         if(flag1) then
            spae1k2 = N1 * Spaa(k1, k2)
            spbk2e1 = 0.0_ki
         else
            spae1k2 = 0.0_ki
            spbk2e1 = N1 * Spbb(k2, k1)
         end if
         if(flag1) then
            spae1l3 = N1 * Spaa(k1, l3)
            spbl3e1 = N1 * Spbb(l3, k2)
         else
            spae1l3 = N1 * Spaa(k2, l3)
            spbl3e1 = N1 * Spbb(l3, k1)
         end if
         if(flag1) then
            spae1l4 = N1 * Spaa(k1, l4)
            spbl4e1 = N1 * Spbb(l4, k2)
         else
            spae1l4 = N1 * Spaa(k2, l4)
            spbl4e1 = N1 * Spbb(l4, k1)
         end if
         if(flag2) then
            spak2e2 = 0.0_ki
            spbe2k2 = N2 * Spbb(k1, k2)
         else
            spak2e2 = N2 * Spaa(k2, k1)
            spbe2k2 = 0.0_ki
         end if
         if(flag2) then
            spae2k2 = 0.0_ki
            spbk2e2 = N2 * Spbb(k2, k1)
         else
            spae2k2 = N2 * Spaa(k1, k2)
            spbk2e2 = 0.0_ki
         end if
         if(flag2) then
            spae2l3 = N2 * Spaa(k2, l3)
            spbl3e2 = N2 * Spbb(l3, k1)
         else
            spae2l3 = N2 * Spaa(k1, l3)
            spbl3e2 = N2 * Spbb(l3, k2)
         end if
         if(flag2) then
            spae2l4 = N2 * Spaa(k2, l4)
            spbl4e2 = N2 * Spbb(l4, k1)
         else
            spae2l4 = N2 * Spaa(k1, l4)
            spbl4e2 = N2 * Spbb(l4, k2)
         end if
         if (flag1) then
            if (flag2) then
               spae1e2 = N1 * N2 * Spaa(k1, k2)
               spbe2e1 = N1 * N2 * Spbb(k1, k2)
            else
               spae1e2 = 0.0_ki
               spbe2e1 = 0.0_ki
            endif
         else
            if (flag2) then
               spae1e2 = 0.0_ki
               spbe2e1 = 0.0_ki
            else
               spae1e2 = N1 * N2 * Spaa(k2, k1)
               spbe2e1 = N1 * N2 * Spbb(k2, k1)
            endif
         end if
         if (flag1) then
            spvak1e1 = N1 * Spab3_vec(k1, k2)
            spvae1k1 = N1 * 2.0_ki * k1
         else
            spvak1e1 = N1 * 2.0_ki * k1
            spvae1k1 = N1 * Spab3_vec(k2, k1)
         end if
         if (flag2) then
            spvak1e2 = N2 * 2.0_ki * k1
            spvae2k1 = N2 * Spab3_vec(k2, k1)
         else
            spvak1e2 = N2 * Spab3_vec(k1, k2)
            spvae2k1 = N2 * 2.0_ki * k1
         end if
         if (flag1) then
            spvak2e1 = N1 * 2.0_ki * k2
            spvae1k2 = N1 * Spab3_vec(k1, k2)
         else
            spvak2e1 = N1 * Spab3_vec(k2, k1)
            spvae1k2 = N1 * 2.0_ki * k2
         end if
         if (flag2) then
            spvak2e2 = N2 * Spab3_vec(k2, k1)
            spvae2k2 = N2 * 2.0_ki * k2
         else
            spvak2e2 = N2 * 2.0_ki * k2
            spvae2k2 = N2 * Spab3_vec(k1, k2)
         end if
         if (flag1) then
            spval3e1 = N1 * Spab3_vec(l3, k2)
            spvae1l3 = N1 * Spab3_vec(k1, l3)
         else
            spval3e1 = N1 * Spab3_vec(l3, k1)
            spvae1l3 = N1 * Spab3_vec(k2, l3)
         end if
         if (flag2) then
            spval3e2 = N2 * Spab3_vec(l3, k1)
            spvae2l3 = N2 * Spab3_vec(k2, l3)
         else
            spval3e2 = N2 * Spab3_vec(l3, k2)
            spvae2l3 = N2 * Spab3_vec(k1, l3)
         end if
         if (flag1) then
            spval4e1 = N1 * Spab3_vec(l4, k2)
            spvae1l4 = N1 * Spab3_vec(k1, l4)
         else
            spval4e1 = N1 * Spab3_vec(l4, k1)
            spvae1l4 = N1 * Spab3_vec(k2, l4)
         end if
         if (flag2) then
            spval4e2 = N2 * Spab3_vec(l4, k1)
            spvae2l4 = N2 * Spab3_vec(k2, l4)
         else
            spval4e2 = N2 * Spab3_vec(l4, k2)
            spvae2l4 = N2 * Spab3_vec(k1, l4)
         end if
         if (flag1) then
            if (flag2) then
               spvae1e2 = N1 * N2 * 2.0_ki * k1
               spvae2e1 = N1 * N2 * 2.0_ki * k2
            else
               spvae1e2 = N1 * N2 * Spab3_vec(k1, k2)
               spvae2e1 = N1 * N2 * Spab3_vec(k1, k2)
            end if
         else
            if (flag2) then
               spvae1e2 = N1 * N2 * Spab3_vec(k2, k1)
               spvae2e1 = N1 * N2 * Spab3_vec(k2, k1)
            else
               spvae1e2 = N1 * N2 * 2.0_ki * k2
               spvae2e1 = N1 * N2 * 2.0_ki * k1
            end if
         end if
         if (debug_numpolvec) then
            write(logfile, "(A17)") "<!-- NUMPOLVEC --"
            write(logfile, "(A9,I2,A4,I2,A9,L1)") &
            & "Helicity(", 1, ") = ", hel1, "; flag = ", flag1
            write(logfile, "(A9,I2,A4,I2,A9,L1)") &
            & "Helicity(", 2, ") = ", hel2, "; flag = ", flag2
            write(logfile, *) "k1.e1", dotproduct(k1, e1)
            write(logfile, *) "r1.e1", dotproduct(k2, e1)
            write(logfile, *) "k2.e2", dotproduct(k2, e2)
            write(logfile, *) "r2.e2", dotproduct(k1, e2)
            write(logfile, *) "<1|e1|2]", &
              & dotproduct(spvak1k2, e1), spae1k1*(-1.0_ki)*spbk2e1*(-1.0_ki)
            write(logfile, *) "<1|e2|2]", &
              & dotproduct(spvak1k2, e2), spak1e2*spbe2k2
            write(logfile, *) "<1|e1|3]", &
              & dotproduct(spvak1l3, e1), spae1k1*(-1.0_ki)*spbl3e1*(-1.0_ki)
            write(logfile, *) "<1|e2|3]", &
              & dotproduct(spvak1l3, e2), spak1e2*spbl3e2*(-1.0_ki)
            write(logfile, *) "<1|e1|4]", &
              & dotproduct(spvak1l4, e1), spae1k1*(-1.0_ki)*spbl4e1*(-1.0_ki)
            write(logfile, *) "<1|e2|4]", &
              & dotproduct(spvak1l4, e2), spak1e2*spbl4e2*(-1.0_ki)
            write(logfile, *) "<2|e1|1]", &
              & dotproduct(spvak2k1, e1), spae1k2*(-1.0_ki)*spbe1k1
            write(logfile, *) "<2|e2|1]", &
              & dotproduct(spvak2k1, e2), spae2k2*(-1.0_ki)*spbe2k1
            write(logfile, *) "<2|e1|3]", &
              & dotproduct(spvak2l3, e1), spae1k2*(-1.0_ki)*spbl3e1*(-1.0_ki)
            write(logfile, *) "<2|e2|3]", &
              & dotproduct(spvak2l3, e2), spae2k2*(-1.0_ki)*spbl3e2*(-1.0_ki)
            write(logfile, *) "<2|e1|4]", &
              & dotproduct(spvak2l4, e1), spae1k2*(-1.0_ki)*spbl4e1*(-1.0_ki)
            write(logfile, *) "<2|e2|4]", &
              & dotproduct(spvak2l4, e2), spae2k2*(-1.0_ki)*spbl4e2*(-1.0_ki)
            write(logfile, *) "<3|e1|1]", &
              & dotproduct(spval3k1, e1), spae1l3*(-1.0_ki)*spbe1k1
            write(logfile, *) "<3|e2|1]", &
              & dotproduct(spval3k1, e2), spae2l3*(-1.0_ki)*spbe2k1
            write(logfile, *) "<3|e1|2]", &
              & dotproduct(spval3k2, e1), spae1l3*(-1.0_ki)*spbk2e1*(-1.0_ki)
            write(logfile, *) "<3|e2|2]", &
              & dotproduct(spval3k2, e2), spae2l3*(-1.0_ki)*spbe2k2
            write(logfile, *) "<3|e1|4]", &
              & dotproduct(spval3l4, e1), spae1l3*(-1.0_ki)*spbl4e1*(-1.0_ki)
            write(logfile, *) "<3|e2|4]", &
              & dotproduct(spval3l4, e2), spae2l3*(-1.0_ki)*spbl4e2*(-1.0_ki)
            write(logfile, *) "<4|e1|1]", &
              & dotproduct(spval4k1, e1), spae1l4*(-1.0_ki)*spbe1k1
            write(logfile, *) "<4|e2|1]", &
              & dotproduct(spval4k1, e2), spae2l4*(-1.0_ki)*spbe2k1
            write(logfile, *) "<4|e1|2]", &
              & dotproduct(spval4k2, e1), spae1l4*(-1.0_ki)*spbk2e1*(-1.0_ki)
            write(logfile, *) "<4|e2|2]", &
              & dotproduct(spval4k2, e2), spae2l4*(-1.0_ki)*spbe2k2
            write(logfile, *) "<4|e1|3]", &
              & dotproduct(spval4l3, e1), spae1l4*(-1.0_ki)*spbl3e1*(-1.0_ki)
            write(logfile, *) "<4|e2|3]", &
              & dotproduct(spval4l3, e2), spae2l4*(-1.0_ki)*spbl3e2*(-1.0_ki)
            write(logfile, *) "e1.e2", &
            & dotproduct(e1, e2), &
            & 0.5_ki * spae1e2 * spbe2e1
            write(logfile, *) "<k1|mu|e1]<e1|mu|k2]", &
            & dotproduct(spvak1e1, spvae1k2), &
            & -2.0_ki * dotproduct(spvak1k2, e1)
            write(logfile, *) "<k1|mu|e2]<e2|mu|k2]", &
            & dotproduct(spvak1e2, spvae2k2), &
            & -2.0_ki * dotproduct(spvak1k2, e2)
            write(logfile, *) "<k2|mu|e1]<e1|mu|k1]", &
            & dotproduct(spvak2e1, spvae1k1), &
            & -2.0_ki * dotproduct(spvak2k1, e1)
            write(logfile, *) "<k2|mu|e2]<e2|mu|k1]", &
            & dotproduct(spvak2e2, spvae2k1), &
            & -2.0_ki * dotproduct(spvak2k1, e2)
            write(logfile, *) "[1|e1]<e1|1|e2]<e2|1>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k1)*(-spak1e2), 2.0_ki*dotproduct(k1, e1)*2.0_ki*dotproduct(k1, e2)
            write(logfile, *) "[1|e1]<e1|2|e2]<e2|1>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k2)*(-spak1e2), dotproduct(spvak2k1, e1)*dotproduct(spvak1k2, e2)
            write(logfile, *) "[1|e1]<e1|1|e2]<e2|2>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k1)*(-spak2e2), 2.0_ki*dotproduct(k1, e1)*dotproduct(spvak2k1, e2)
            write(logfile, *) "[1|e1]<e1|2|e2]<e2|2>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k2)*(-spak2e2), dotproduct(spvak2k1, e1)*2.0_ki*dotproduct(k2, e2)
            write(logfile, *) "[1|e1]<e1|1|e2]<e2|3>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k1)*spae2l3, 2.0_ki*dotproduct(k1, e1)*dotproduct(spval3k1, e2)
            write(logfile, *) "[1|e1]<e1|2|e2]<e2|3>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k2)*spae2l3, dotproduct(spvak2k1, e1)*dotproduct(spval3k2, e2)
            write(logfile, *) "[1|e1]<e1|1|e2]<e2|4>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k1)*spae2l4, 2.0_ki*dotproduct(k1, e1)*dotproduct(spval4k1, e2)
            write(logfile, *) "[1|e1]<e1|2|e2]<e2|4>", &
            & (-spbe1k1)*dotproduct(spvae1e2, k2)*spae2l4, dotproduct(spvak2k1, e1)*dotproduct(spval4k2, e2)
            write(logfile, *) "[2|e1]<e1|1|e2]<e2|1>", &
            & spbk2e1*dotproduct(spvae1e2, k1)*(-spak1e2), dotproduct(spvak1k2, e1)*2.0_ki*dotproduct(k1, e2)
            write(logfile, *) "[2|e1]<e1|2|e2]<e2|1>", &
            & spbk2e1*dotproduct(spvae1e2, k2)*(-spak1e2), 2.0_ki*dotproduct(k2, e1)*dotproduct(spvak1k2, e2)
            write(logfile, *) "[2|e1]<e1|1|e2]<e2|2>", &
            & spbk2e1*dotproduct(spvae1e2, k1)*(-spak2e2), dotproduct(spvak1k2, e1)*dotproduct(spvak2k1, e2)
            write(logfile, *) "[2|e1]<e1|2|e2]<e2|2>", &
            & spbk2e1*dotproduct(spvae1e2, k2)*(-spak2e2), 2.0_ki*dotproduct(k2, e1)*2.0_ki*dotproduct(k2, e2)
            write(logfile, *) "[2|e1]<e1|1|e2]<e2|3>", &
            & spbk2e1*dotproduct(spvae1e2, k1)*spae2l3, dotproduct(spvak1k2, e1)*dotproduct(spval3k1, e2)
            write(logfile, *) "[2|e1]<e1|2|e2]<e2|3>", &
            & spbk2e1*dotproduct(spvae1e2, k2)*spae2l3, 2.0_ki*dotproduct(k2, e1)*dotproduct(spval3k2, e2)
            write(logfile, *) "[2|e1]<e1|1|e2]<e2|4>", &
            & spbk2e1*dotproduct(spvae1e2, k1)*spae2l4, dotproduct(spvak1k2, e1)*dotproduct(spval4k1, e2)
            write(logfile, *) "[2|e1]<e1|2|e2]<e2|4>", &
            & spbk2e1*dotproduct(spvae1e2, k2)*spae2l4, 2.0_ki*dotproduct(k2, e1)*dotproduct(spval4k2, e2)
            write(logfile, *) "[3|e1]<e1|1|e2]<e2|1>", &
            & spbl3e1*dotproduct(spvae1e2, k1)*(-spak1e2), dotproduct(spvak1l3, e1)*2.0_ki*dotproduct(k1, e2)
            write(logfile, *) "[3|e1]<e1|2|e2]<e2|1>", &
            & spbl3e1*dotproduct(spvae1e2, k2)*(-spak1e2), dotproduct(spvak2l3, e1)*dotproduct(spvak1k2, e2)
            write(logfile, *) "[3|e1]<e1|1|e2]<e2|2>", &
            & spbl3e1*dotproduct(spvae1e2, k1)*(-spak2e2), dotproduct(spvak1l3, e1)*dotproduct(spvak2k1, e2)
            write(logfile, *) "[3|e1]<e1|2|e2]<e2|2>", &
            & spbl3e1*dotproduct(spvae1e2, k2)*(-spak2e2), dotproduct(spvak2l3, e1)*2.0_ki*dotproduct(k2, e2)
            write(logfile, *) "[3|e1]<e1|1|e2]<e2|3>", &
            & spbl3e1*dotproduct(spvae1e2, k1)*spae2l3, dotproduct(spvak1l3, e1)*dotproduct(spval3k1, e2)
            write(logfile, *) "[3|e1]<e1|2|e2]<e2|3>", &
            & spbl3e1*dotproduct(spvae1e2, k2)*spae2l3, dotproduct(spvak2l3, e1)*dotproduct(spval3k2, e2)
            write(logfile, *) "[3|e1]<e1|1|e2]<e2|4>", &
            & spbl3e1*dotproduct(spvae1e2, k1)*spae2l4, dotproduct(spvak1l3, e1)*dotproduct(spval4k1, e2)
            write(logfile, *) "[3|e1]<e1|2|e2]<e2|4>", &
            & spbl3e1*dotproduct(spvae1e2, k2)*spae2l4, dotproduct(spvak2l3, e1)*dotproduct(spval4k2, e2)
            write(logfile, *) "[4|e1]<e1|1|e2]<e2|1>", &
            & spbl4e1*dotproduct(spvae1e2, k1)*(-spak1e2), dotproduct(spvak1l4, e1)*2.0_ki*dotproduct(k1, e2)
            write(logfile, *) "[4|e1]<e1|2|e2]<e2|1>", &
            & spbl4e1*dotproduct(spvae1e2, k2)*(-spak1e2), dotproduct(spvak2l4, e1)*dotproduct(spvak1k2, e2)
            write(logfile, *) "[4|e1]<e1|1|e2]<e2|2>", &
            & spbl4e1*dotproduct(spvae1e2, k1)*(-spak2e2), dotproduct(spvak1l4, e1)*dotproduct(spvak2k1, e2)
            write(logfile, *) "[4|e1]<e1|2|e2]<e2|2>", &
            & spbl4e1*dotproduct(spvae1e2, k2)*(-spak2e2), dotproduct(spvak2l4, e1)*2.0_ki*dotproduct(k2, e2)
            write(logfile, *) "[4|e1]<e1|1|e2]<e2|3>", &
            & spbl4e1*dotproduct(spvae1e2, k1)*spae2l3, dotproduct(spvak1l4, e1)*dotproduct(spval3k1, e2)
            write(logfile, *) "[4|e1]<e1|2|e2]<e2|3>", &
            & spbl4e1*dotproduct(spvae1e2, k2)*spae2l3, dotproduct(spvak2l4, e1)*dotproduct(spval3k2, e2)
            write(logfile, *) "[4|e1]<e1|1|e2]<e2|4>", &
            & spbl4e1*dotproduct(spvae1e2, k1)*spae2l4, dotproduct(spvak1l4, e1)*dotproduct(spval4k1, e2)
            write(logfile, *) "[4|e1]<e1|2|e2]<e2|4>", &
            & spbl4e1*dotproduct(spvae1e2, k2)*spae2l4, dotproduct(spvak2l4, e1)*dotproduct(spval4k2, e2)
            write(logfile, *) "[1|e2]<e2|1|e1]<e1|1>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k1)*(-spak1e1), 2.0_ki*dotproduct(k1, e2)*2.0_ki*dotproduct(k1, e1)
            write(logfile, *) "[1|e2]<e2|2|e1]<e1|1>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k2)*(-spak1e1), dotproduct(spvak2k1, e2)*dotproduct(spvak1k2, e1)
            write(logfile, *) "[1|e2]<e2|1|e1]<e1|2>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k1)*spae1k2, 2.0_ki*dotproduct(k1, e2)*dotproduct(spvak2k1, e1)
            write(logfile, *) "[1|e2]<e2|2|e1]<e1|2>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k2)*spae1k2, dotproduct(spvak2k1, e2)*2.0_ki*dotproduct(k2, e1)
            write(logfile, *) "[1|e2]<e2|1|e1]<e1|3>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k1)*spae1l3, 2.0_ki*dotproduct(k1, e2)*dotproduct(spval3k1, e1)
            write(logfile, *) "[1|e2]<e2|2|e1]<e1|3>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k2)*spae1l3, dotproduct(spvak2k1, e2)*dotproduct(spval3k2, e1)
            write(logfile, *) "[1|e2]<e2|1|e1]<e1|4>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k1)*spae1l4, 2.0_ki*dotproduct(k1, e2)*dotproduct(spval4k1, e1)
            write(logfile, *) "[1|e2]<e2|2|e1]<e1|4>", &
            & (-spbe2k1)*dotproduct(spvae2e1, k2)*spae1l4, dotproduct(spvak2k1, e2)*dotproduct(spval4k2, e1)
            write(logfile, *) "[2|e2]<e2|1|e1]<e1|1>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k1)*(-spak1e1), dotproduct(spvak1k2, e2)*2.0_ki*dotproduct(k1, e1)
            write(logfile, *) "[2|e2]<e2|2|e1]<e1|1>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k2)*(-spak1e1), 2.0_ki*dotproduct(k2, e2)*dotproduct(spvak1k2, e1)
            write(logfile, *) "[2|e2]<e2|1|e1]<e1|2>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k1)*spae1k2, dotproduct(spvak1k2, e2)*dotproduct(spvak2k1, e1)
            write(logfile, *) "[2|e2]<e2|2|e1]<e1|2>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k2)*spae1k2, 2.0_ki*dotproduct(k2, e2)*2.0_ki*dotproduct(k2, e1)
            write(logfile, *) "[2|e2]<e2|1|e1]<e1|3>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k1)*spae1l3, dotproduct(spvak1k2, e2)*dotproduct(spval3k1, e1)
            write(logfile, *) "[2|e2]<e2|2|e1]<e1|3>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k2)*spae1l3, 2.0_ki*dotproduct(k2, e2)*dotproduct(spval3k2, e1)
            write(logfile, *) "[2|e2]<e2|1|e1]<e1|4>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k1)*spae1l4, dotproduct(spvak1k2, e2)*dotproduct(spval4k1, e1)
            write(logfile, *) "[2|e2]<e2|2|e1]<e1|4>", &
            & (-spbe2k2)*dotproduct(spvae2e1, k2)*spae1l4, 2.0_ki*dotproduct(k2, e2)*dotproduct(spval4k2, e1)
            write(logfile, *) "[3|e2]<e2|1|e1]<e1|1>", &
            & spbl3e2*dotproduct(spvae2e1, k1)*(-spak1e1), dotproduct(spvak1l3, e2)*2.0_ki*dotproduct(k1, e1)
            write(logfile, *) "[3|e2]<e2|2|e1]<e1|1>", &
            & spbl3e2*dotproduct(spvae2e1, k2)*(-spak1e1), dotproduct(spvak2l3, e2)*dotproduct(spvak1k2, e1)
            write(logfile, *) "[3|e2]<e2|1|e1]<e1|2>", &
            & spbl3e2*dotproduct(spvae2e1, k1)*spae1k2, dotproduct(spvak1l3, e2)*dotproduct(spvak2k1, e1)
            write(logfile, *) "[3|e2]<e2|2|e1]<e1|2>", &
            & spbl3e2*dotproduct(spvae2e1, k2)*spae1k2, dotproduct(spvak2l3, e2)*2.0_ki*dotproduct(k2, e1)
            write(logfile, *) "[3|e2]<e2|1|e1]<e1|3>", &
            & spbl3e2*dotproduct(spvae2e1, k1)*spae1l3, dotproduct(spvak1l3, e2)*dotproduct(spval3k1, e1)
            write(logfile, *) "[3|e2]<e2|2|e1]<e1|3>", &
            & spbl3e2*dotproduct(spvae2e1, k2)*spae1l3, dotproduct(spvak2l3, e2)*dotproduct(spval3k2, e1)
            write(logfile, *) "[3|e2]<e2|1|e1]<e1|4>", &
            & spbl3e2*dotproduct(spvae2e1, k1)*spae1l4, dotproduct(spvak1l3, e2)*dotproduct(spval4k1, e1)
            write(logfile, *) "[3|e2]<e2|2|e1]<e1|4>", &
            & spbl3e2*dotproduct(spvae2e1, k2)*spae1l4, dotproduct(spvak2l3, e2)*dotproduct(spval4k2, e1)
            write(logfile, *) "[4|e2]<e2|1|e1]<e1|1>", &
            & spbl4e2*dotproduct(spvae2e1, k1)*(-spak1e1), dotproduct(spvak1l4, e2)*2.0_ki*dotproduct(k1, e1)
            write(logfile, *) "[4|e2]<e2|2|e1]<e1|1>", &
            & spbl4e2*dotproduct(spvae2e1, k2)*(-spak1e1), dotproduct(spvak2l4, e2)*dotproduct(spvak1k2, e1)
            write(logfile, *) "[4|e2]<e2|1|e1]<e1|2>", &
            & spbl4e2*dotproduct(spvae2e1, k1)*spae1k2, dotproduct(spvak1l4, e2)*dotproduct(spvak2k1, e1)
            write(logfile, *) "[4|e2]<e2|2|e1]<e1|2>", &
            & spbl4e2*dotproduct(spvae2e1, k2)*spae1k2, dotproduct(spvak2l4, e2)*2.0_ki*dotproduct(k2, e1)
            write(logfile, *) "[4|e2]<e2|1|e1]<e1|3>", &
            & spbl4e2*dotproduct(spvae2e1, k1)*spae1l3, dotproduct(spvak1l4, e2)*dotproduct(spval3k1, e1)
            write(logfile, *) "[4|e2]<e2|2|e1]<e1|3>", &
            & spbl4e2*dotproduct(spvae2e1, k2)*spae1l3, dotproduct(spvak2l4, e2)*dotproduct(spval3k2, e1)
            write(logfile, *) "[4|e2]<e2|1|e1]<e1|4>", &
            & spbl4e2*dotproduct(spvae2e1, k1)*spae1l4, dotproduct(spvak1l4, e2)*dotproduct(spval4k1, e1)
            write(logfile, *) "[4|e2]<e2|2|e1]<e1|4>", &
            & spbl4e2*dotproduct(spvae2e1, k2)*spae1l4, dotproduct(spvak2l4, e2)*dotproduct(spval4k2, e1)
            write(logfile, "(A18)") "  -- NUMPOLVEC -->"
         end if
      end if
   end subroutine init_event
!---#] subroutine init_event:
!---#[ subroutine light_cone_decomposition:
   pure subroutine light_cone_decomposition(vec, lvec, vref, mass)
      implicit none
      real(ki), dimension(4), intent(in) :: vec, vref
      real(ki), dimension(4), intent(out) :: lvec
      real(ki), intent(in) :: mass

      real(ki) :: alpha

      alpha = 2.0_ki * dotproduct(vec, vref)

      if (abs(alpha) < 1.0E+3_ki * epsilon(1.0_ki)) then
         lvec = vec
      else
         lvec = vec - mass * mass / alpha * vref
      end if
   end  subroutine light_cone_decomposition
!---#] subroutine light_cone_decomposition:
!---#[ subroutine light_cone_splitting_iter:
   pure subroutine light_cone_splitting_iter(pI, pJ, li, lj, mI, mJ)
      ! Iteratively applies
      !   li = pI - mI^2/(2*pI.lj) * lj
      !   lj = pJ - mJ^2/(2*pJ.li) * li

      implicit none
      real(ki), dimension(4), intent(in) :: pI, pJ
      real(ki), dimension(4), intent(out) :: li, lj
      real(ki), intent(in) :: mI, mJ

      integer :: i
      real(ki) :: mmI, mmJ, lipJ, pIlj

      mmI = mI*mI
      mmJ = mJ*mJ

      lj = pJ
      do i = 1, 10
         pIlj = 2.0_ki * dotproduct(pI, lj)
         li = pI - mmI/pIlj * lj
         lipJ = 2.0_ki * dotproduct(li, pJ)
         lj = pJ - mmJ/lipJ * li
      end do
   end  subroutine light_cone_splitting_iter
!---#] subroutine light_cone_splitting_iter:
!---#[ subroutine light_cone_splitting_alg:
   pure subroutine light_cone_splitting_alg(pI, pJ, li, lj, mI, mJ)
      ! Splits pI (pI.pI=mI*mI) and pJ (pJ.pJ=mJ*mJ)
      ! into a pair li (li.li=0) and lj (lj.lj=0).
      !
      ! To achieve this, the equation (pI+alpha*pJ)**2 == 0 is solved:
      !   alpha**2 * pJ.pJ + 2 * alpha * pI.pJ + pI.pI == 0
      !   mJ**2 * (alpha**2 + 2 * alpha * t + u**2) == 0
      ! with
      !   t = pI.pJ / mJ**2
      !   u**2 = mI**2/mJ**2
      !
      ! ==> alpha = - t +/- sqrt(det)
      !     det   = t**2 - u**2

      implicit none
      real(ki), dimension(4), intent(in) :: pI, pJ
      real(ki), dimension(4), intent(out) :: li, lj
      real(ki), intent(in) :: mI, mJ

      real(ki) :: det, t, u, pq

      pq = dotproduct(pI/mI, pJ/mJ)

      u = mI/mJ
      t = pq * u

      det = (1.0_ki+1.0_ki/pq)*(1.0_ki-1.0_ki/pq)
      if (det > 0.0_ki) then
         det = sqrt(1.0_ki+1.0_ki/pq)*sqrt(1.0_ki-1.0_ki/pq)

         li = pI - t * (1.0_ki + det) * pJ
         lj = pI - t * (1.0_ki - det) * pJ
      else
         li(:) = 0.0_ki
         lj(:) = 0.0_ki
      end if
   end  subroutine light_cone_splitting_alg
!---#] subroutine light_cone_splitting_alg:
!---#[ function Spbb:
   pure function Spbb(p, q)
      implicit none
      real(ki), dimension(4), intent(in) :: p, q
      complex(ki) :: Spbb
      Spbb = sign(1.0_ki, dotproduct(p, q)) * conjg(Spaa(q, p))
   end  function Spbb
!---#] function Spbb:
!---#[ function Spab3_complex:
   pure function Spab3_complex(k1, Q, k2)
      implicit none
      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)

      real(ki), dimension(4), intent(in) :: k1, k2
      complex(ki), dimension(4), intent(in) :: Q
      complex(ki) :: Spab3_complex

      real(ki), dimension(4) :: R, J

      R = real(Q)
      J = aimag(Q)

      Spab3_complex = Spab3_mcfm(k1, R, k2) &
                  & + i_ * Spab3_mcfm(k1, J, k2)
   end  function Spab3_complex
!---#] function Spab3_complex:
!---#[ function Spab3_vec:
   pure function Spab3_vec(k1, k2)
      implicit none
      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)

      real(ki), dimension(4), intent(in) :: k1, k2
      complex(ki), dimension(0:3) :: Spab3_vec

      Spab3_vec(0) =   Spab3_mcfm(k1, &
         & (/1.0_ki, 0.0_ki, 0.0_ki, 0.0_ki/), k2)
      Spab3_vec(1) = - Spab3_mcfm(k1, &
         & (/0.0_ki, 1.0_ki, 0.0_ki, 0.0_ki/), k2)
      Spab3_vec(2) = - Spab3_mcfm(k1, &
         & (/0.0_ki, 0.0_ki, 1.0_ki, 0.0_ki/), k2)
      Spab3_vec(3) = - Spab3_mcfm(k1, &
         & (/0.0_ki, 0.0_ki, 0.0_ki, 1.0_ki/), k2)
   end  function Spab3_vec
!---#] function Spab3_vec:
!---#[ function Spaa:
   pure function Spaa(k1, k2)
      ! This routine has been copied from mcfm and adapted to our setup
      implicit none
      real(ki), dimension(0:3), intent(in) :: k1, k2
      complex(ki) :: Spaa

      real(ki) :: rt1, rt2
      complex(ki) :: c231, c232, f1, f2
!---if one of the vectors happens to be zero this routine fails.
!-----positive energy case
         if (k1(0) .gt. 0.0_ki) then
            rt1=sqrt(k1(0)+k1(1))
            c231=cmplx(k1(3),-k1(2), ki)
            f1=1.0_ki
         else
!-----negative energy case
            rt1=sqrt(-k1(0)-k1(1))
            c231=cmplx(-k1(3),k1(2), ki)
            f1=(0.0_ki, 1.0_ki)
         endif
!-----positive energy case
         if (k2(0) .gt. 0.0_ki) then
            rt2=sqrt(k2(0)+k2(1))
            c232=cmplx(k2(3),-k2(2), ki)
            f2=1.0_ki
         else
!-----negative energy case
            rt2=sqrt(-k2(0)-k2(1))
            c232=cmplx(-k2(3),k2(2), ki)
            f2=(0.0_ki, 1.0_ki)
         endif

         Spaa = -f2*f1*(c232*rt1/rt2-c231*rt2/rt1)
   end  function Spaa
!---#] function Spaa:
!---#[ function Spab3_mcfm:
   pure function Spab3_mcfm(k1, Q, k2)
      ! This routine has been copied from mcfm and adapted to our setup
      implicit none
      real(ki), dimension(0:3), intent(in) :: k1, k2
      real(ki), dimension(0:3), intent(in) :: Q
      complex(ki) :: Spab3_mcfm

      real(ki) :: kp, km
      complex(ki) :: kr, kl
      complex(ki) :: pr1, pr2, pl1, pl2
      complex(ki) :: f1, f2
      real(ki) :: flip1, flip2, rt1, rt2

      !--setup components for vector which is contracted in
      kp=+Q(0)+Q(1)
      km=+Q(0)-Q(1)
      kr=cmplx(+Q(3),-Q(2),ki)
      kl=cmplx(+Q(3),+Q(2),ki)

      !---if one of the vectors happens to be zero this routine fails.
      if(all(abs(Q) < 1.0E+2_ki * epsilon(1.0_ki))) then
         Spab3_mcfm = 0.0_ki
         return
      end if

      !-----positive energy case
      if (k1(0) .gt. 0.0_ki) then
         flip1=1.0_ki
         f1=1.0_ki
      else
         flip1=-1.0_ki
         f1=(0.0_ki, 1.0_ki)
      endif
      rt1=sqrt(flip1*(k1(0)+k1(1)))
      pr1=cmplx(flip1*k1(3),-flip1*k1(2), ki)
      pl1=conjg(pr1)

      if (k2(0) .gt. 0.0_ki) then
         flip2=1.0_ki
         f2=1.0_ki
      else
         flip2=-1.0_ki
         f2=(0.0_ki, 1.0_ki)
      endif
      rt2=sqrt(flip2*(k2(0)+k2(1)))
      pr2=cmplx(flip2*k2(3),-flip2*k2(2), ki)
      pl2=conjg(pr2)

      Spab3_mcfm=f1*f2*(&
     &     pr1/rt1*(pl2*kp/rt2-kl*rt2)&
     &    +rt1*(rt2*km-kr*pl2/rt2))
   end  function Spab3_mcfm
!---#] function Spab3_mcfm:
!---#[ function Spab3_mcfmc:
   pure function Spab3_mcfmc(k1, Q, k2)
      ! This routine has been copied from mcfm and adapted to our setup
      implicit none
      complex(ki), dimension(0:3), intent(in) :: k1, k2
      complex(ki), dimension(0:3), intent(in) :: Q
      complex(ki) :: Spab3_mcfmc

      complex(ki) :: kp, km
      complex(ki) :: kr, kl
      complex(ki) :: pr1, pr2, pl1, pl2
      complex(ki) :: rt1, rt2

      !--setup components for vector which is contracted in
      kp=+Q(0)+Q(1)
      km=+Q(0)-Q(1)
      kr=+Q(3)-Q(2)*(0.0_ki, 1.0_ki)
      kl=+Q(3)+Q(2)*(0.0_ki, 1.0_ki)

      !---if one of the vectors happens to be zero this routine fails.
      if(all(abs(Q) < 1.0E+2_ki * epsilon(1.0_ki))) then
         Spab3_mcfmc = 0.0_ki
         return
      end if

      rt1=sqrt((k1(0)+k1(1)))
      pr1=k1(3)-k1(2) * (0.0_ki, 1.0_ki)
      pl1=conjg(pr1)

      rt2=sqrt((k2(0)+k2(1)))
      pr2=k2(3)-k2(2) * (0.0_ki, 1.0_ki)
      pl2=conjg(pr2)

      Spab3_mcfmc=(&
     &     pr1/rt1*(pl2*kp/rt2-kl*rt2)&
     &    +rt1*(rt2*km-kr*pl2/rt2))
   end  function Spab3_mcfmc
!---#] function Spab3_mcfmc:
!---#[ function Spba3_complex:
   pure function Spba3_complex(k1, Q, k2)
      implicit none
      real(ki), dimension(4), intent(in) :: k1, k2
      complex(ki), dimension(4), intent(in) :: Q
      complex(ki) :: Spba3_complex

      Spba3_complex = Spab3_complex(k2, Q, k1)
   end  function Spba3_complex
!---#] function Spba3_complex:
!---#[ function Spba3_real:
   pure function Spba3_real(k1, Q, k2)
      implicit none
      real(ki), dimension(4), intent(in) :: k1, k2
      real(ki), dimension(4), intent(in) :: Q
      complex(ki) :: Spba3_real

      Spba3_real = Spab3_mcfm(k2, Q, k1)
   end  function Spba3_real
!---#] function Spba3_real:
!---#[ functions dotproduct_XX:
   !----#[ function dotproduct_rr:
   pure function dotproduct_rr(p, q)
      implicit none
      real(ki), dimension(4), intent(in) :: p, q
      real(ki) :: dotproduct_rr
      dotproduct_rr = p(1)*q(1) - p(2)*q(2) - p(3)*q(3) - p(4)*q(4)
   end  function dotproduct_rr
   !----#] function dotproduct_rr:
   !----#[ function dotproduct_cc:
   pure function dotproduct_cc(p, q)
      implicit none
      complex(ki), dimension(4), intent(in) :: p, q
      complex(ki) :: dotproduct_cc
      dotproduct_cc = p(1)*q(1) - p(2)*q(2) - p(3)*q(3) - p(4)*q(4)
   end  function dotproduct_cc
   !----#] function dotproduct_cc:
   !----#[ function dotproduct_rc:
   pure function dotproduct_rc(p, q)
      implicit none
      real(ki), dimension(4), intent(in) :: p
      complex(ki), dimension(4), intent(in) :: q
      complex(ki) :: dotproduct_rc
      dotproduct_rc = p(1)*q(1) - p(2)*q(2) - p(3)*q(3) - p(4)*q(4)
   end  function dotproduct_rc
   !----#] function dotproduct_rc:
   !----#[ function dotproduct_cr:
   pure function dotproduct_cr(p, q)
      implicit none
      complex(ki), dimension(4), intent(in) :: p
      real(ki), dimension(4), intent(in) :: q
      complex(ki) :: dotproduct_cr
      dotproduct_cr = p(1)*q(1) - p(2)*q(2) - p(3)*q(3) - p(4)*q(4)
   end  function dotproduct_cr
   !----#] function dotproduct_cr:
!---#] functions dotproduct_XX:
   !---#[ function lambda :
   pure function lambda(x, y, z)
      implicit none
      real(ki), intent(in) :: x, y, z
      real(ki) :: lambda, tmp

      lambda = x - y
      tmp    = x + y
      lambda = lambda * lambda
      lambda = lambda + z*(z - tmp - tmp)
   end  function lambda
   !---#] function lambda :
   !---#[ subroutine adjust_kinematics :
   ! Moves the given vectors slightly such that the on-shell conditions
   ! and momentum conservation are improved.
   pure subroutine adjust_kinematics(vecs)
      implicit none
      real(ki), dimension(4,4), intent(inout) :: vecs

      real(ki) :: p02, p12, Sz, SE, s0, s1
      real(ki) :: z0, z1, z0a, z0b, E0, E1, E0a, E0b
      real(ki) :: a, b, c, d, x, y
      integer :: i

      ! Put particles onshell.
      vecs(1,1) = sign(sqrt(vecs(1,2)**2 + vecs(1,3)**2 + vecs(1,4)**2),vecs(1,1))
      vecs(2,1) = sign(sqrt(vecs(2,2)**2 + vecs(2,3)**2 + vecs(2,4)**2),vecs(2,1))
      s0 = mdlMh**2
      s1 = mdlMh**2
      ! Momentum conservation in x- and y- direction
      vecs(4,2) = sum(vecs(1:2,2)) - sum(vecs(3:3,2))
      vecs(4,3) = sum(vecs(1:2,3)) - sum(vecs(3:3,3))

      SE = sum(vecs(3:2,1)) - sum(vecs(1:2,1))
      Sz = sum(vecs(3:2,4)) - sum(vecs(1:2,4))
      p02 = vecs(3,2)**2 + vecs(3,3)**2 + s0
      p12 = vecs(4,2)**2 + vecs(4,3)**2 + s1

      x = Sz/SE
      y = (p12 - p02)/(SE*SE)

      ! Solve a*z0^2 + b*z0 + c = 0

      a = (x - 1.0_ki) * (x + 1.0_ki)
      b = Sz*(a + y)
      c = 0.25_ki * SE*SE * (a*(x*x + 2.0_ki*y - 1.0_ki) + y*y) - p02

      if (abs(a) .lt. epsilon(1.0_ki) * 1.0E+02_ki) then
         ! linear equation
         z0 = - c / b
         E0 = 0.5_ki*SE*(a + y) + z0*x
      else
         ! quadratic equation
         d = b*b-4.0_ki*a*c
         c = 0.5_ki*SE*(a+y)

         if (d .lt. 0.0_ki) then
            ! assume d == 0 because d < 0 must be numerical inaccuracy
            z0 = 0.5_ki * (-b)/a
            E0 = c + z0*x
         else
            d = sqrt(d)

            z0a = 0.5_ki*(- b + d)/a
            z0b = 0.5_ki*(- b - d)/a
            E0a = c + z0a*x
            E0b = c + z0b*x

            if (abs(E0a - vecs(3,1)) + abs(z0a - vecs(3,4)) .lt. abs(E0b - vecs(3,1)) + abs(z0b - vecs(3,4))) then
                 E0 = E0a
                 z0 = z0a
            else
                 E0 = E0b
                 z0 = z0b
            end if
         end if
      end if

      z1 = - z0 - Sz
      E1 = - E0 - SE

      ! Adjust the last two vectors:
      vecs(3,1) = E0
      vecs(3,4) = z0
      vecs(4,1) = E1
      vecs(4,4) = z1
   end subroutine adjust_kinematics
   !---#] subroutine adjust_kinematics :
   !---#[ subroutine boost_to_cms :
   subroutine boost_to_cms(vecs)
     implicit none
     real(ki), dimension(4,4), intent(inout) :: vecs
     real(ki), dimension(4) :: p_cms
     real(ki) :: s_cms, sqrt_s
     integer :: i
     ! Incoming vectors should be vecs(1,:) and vecs(2,:)

     p_cms = (vecs(1,:)+vecs(2,:))

     if(p_cms(2).ne.0.0_ki .and. p_cms(3).ne.0.0_ki) then
        write(*,*) "Error in boost to CMS frame: vecs(1,:) and vecs(2,:) ",&
             &"are not incoming momenta."
        return
     else if(abs(p_cms(4)).lt.1.0E-08_ki) then
        return
     else
        s_cms = 2.0_ki * dotproduct(vecs(1,:), vecs(2,:))
        if(s_cms.lt.0.0_ki) then
           write(*,*) "Error: negative centre-of-mass energy."
        else
           sqrt_s = sqrt(s_cms)
        end if
        call lorentz_boost(sqrt_s,p_cms,vecs)
     end if
     return
   end subroutine boost_to_cms
   !---#] subroutine boost_to_cms :
   !---#[ subroutine lorentz_boost :
   subroutine lorentz_boost(mass,p,vecs)
     ! take momenta vecs in frame in which one particle is at rest with mass "mass"
     ! and convert to frame in which the one particle has fourvector p
     implicit none

     real(ki), dimension(4), intent(in) :: p
     real(ki), dimension(2:4) :: beta
     real(ki) :: mass, gamma, bdotp
     real(ki), dimension(4,4), intent(inout) :: vecs
     real(ki), dimension(4,4) :: vecs_in
     real(ki), parameter :: one = 1.0_ki
     integer :: i,j,k

     vecs_in = vecs
     gamma=p(1)/mass

     ! Loop over particles:
     do i=1,4
        bdotp=0.0_ki
        do j=2,4
           beta(j)=p(j)/p(1)
           bdotp=bdotp+vecs_in(i,j)*beta(j)
        enddo
        vecs(i,1)=gamma*(vecs_in(i,1)-bdotp)
        do k=2,4
           vecs(i,k)=vecs_in(i,k)+gamma*beta(k)*(gamma/(gamma+one)*bdotp-vecs_in(i,1))
        enddo
     enddo

     return
   end subroutine lorentz_boost
   !---#] subroutine lorentz_boost :
   !---#[ function epsi0 :
   pure function epsi0(k, q, s) result(eps)
      implicit none

      real(ki), dimension(0:3), intent(in) :: k, q
      integer, intent(in) :: s
      complex(ki), dimension(0:3) :: eps

      select case(s)
      case(1)
         eps = sqrthalf * Spab3(q,k) / Spaa(q,k)
      case(-1)
         eps = sqrthalf * Spab3(k,q) / Spbb(k,q)
      case default
         eps(:) = (0.0_ki,0.0_ki)
      end select
   end  function epsi0
   !---#] function epsi0 :
   !---#[ function epso0 :
   pure function epso0(k, q, s) result(eps)
      implicit none

      real(ki), dimension(0:3), intent(in) :: k, q
      integer, intent(in) :: s
      complex(ki), dimension(0:3) :: eps

      eps = conjg(epsi0(k, q, s))
   end  function epso0
   !---#] function epso0 :
   !---#[ function epsim :
   pure function epsim(k, q, m, s) result(eps)
      implicit none
      real(ki), dimension(0:3), intent(in) :: k, q
      integer, intent(in) :: s
      real(ki), intent(in) :: m
      complex(ki), dimension(0:3) :: eps

      real(ki), dimension(0:3) :: l

      call light_cone_decomposition(k, l, q, m)

      select case(s)
      case(1)
         eps = sqrthalf * Spab3(q,l) / Spaa(q,l)
      case(-1)
         eps = sqrthalf * Spab3(l,q) / Spbb(l,q)
      case(0)
         eps = (l+l-k)/m
      case default
         eps(:) = (0.0_ki,0.0_ki)
      end select
   end  function epsim
   !---#] function epsim :
   !---#[ function epsom :
   pure function epsom(k, q, m, s) result(eps)
      implicit none
      real(ki), dimension(0:3), intent(in) :: k, q
      integer, intent(in) :: s
      real(ki), intent(in) :: m
      complex(ki), dimension(0:3) :: eps

      eps = conjg(epsim(k, q, m, s))
   end  function epsom
   !---#] function epsom :
end module pb0_gghh_kinematics
