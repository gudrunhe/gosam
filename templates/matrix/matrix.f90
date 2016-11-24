[% ' vim: syntax=golem
%]module     [% process_name asprefix=\_ %]matrix[%
@if extension samurai %]
   use msamurai, only: initsamurai, exitsamurai[%
@end @if %]
   use [% process_name asprefix=\_ %]util, only: square
   use [% process_name asprefix=\_ %]config, only: ki, &
     & include_helicity_avg_factor, include_color_avg_factor, &
     & debug_lo_diagrams, debug_nlo_diagrams, &
     & include_symmetry_factor, &
     & PSP_check, PSP_verbosity, PSP_rescue, PSP_chk_th1, &
     & PSP_chk_th2, PSP_chk_th3, PSP_chk_kfactor, reduction_interoperation, &
     & PSP_chk_li1, PSP_chk_li2, PSP_chk_li3, PSP_chk_li4, &
     & reduction_interoperation_rescue, convert_to_cdr[%
@if extension samurai %], &
     & samurai_verbosity, samurai_test, samurai_scalar[%
@end @if %]
   use [% process_name asprefix=\_ %]kinematics, only: &
       in_helicities, symmetry_factor, num_legs, &
       lo_qcd_couplings, corrections_are_qcd, num_light_quarks, num_gluons
   use [% process_name asprefix=\_ %]model, only: Nf, NC, sqrt2, init_functions
   use [% process_name asprefix=\_ %]color, only: TR, CA, CF, numcs, &
     & incolors, init_color[%
@if helsum %][%
   @for helicities generated %][%
      @if generate_lo_diagrams %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0, only: amplitude[%helicity%]l0 => amplitude[%
      @end @if %][%
   @end @for %]
   use [% process_name asprefix=\_ 
      %]amplitude, only: samplitudel1summed => samplitude[%
@else %][%
   @for helicities generated %][%
      @if generate_lo_diagrams %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0, only: amplitude[%helicity%]l0 => amplitude[%
      @end @if %][%
      @if generate_nlo_virt %]
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%], [% ' '
        %]only: samplitudeh[%helicity%]l1 => samplitude, &
        &   finite_renormalisation[%helicity%] => finite_renormalisation[%
      @end @if %][%
   @end @for %][%
@end @if %]
   use [% process_name asprefix=\_
      %]dipoles, only: insertion_operator, insertion_operator_qed

   implicit none
   save

   private

   integer :: banner_ch = 6

   public :: initgolem, exitgolem, samplitude
   public :: samplitudel0, samplitudel1
   public :: ir_subtraction, color_correlated_lo2, spin_correlated_lo2
   public :: OLP_color_correlated, OLP_spin_correlated_lo2

   [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]private:: get_formfactor_lo [% @end @if %]
   [% @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]private:: get_formfactor_nlo [% @end @if %]

contains
   !---#[ subroutine banner:
   subroutine     banner()
      implicit none

      character(len=74) :: frame = "+" // repeat("-", 72) // "+"

      if (banner_ch .le. 0) return

      write(banner_ch,'(A74)') frame[%
   @for banner prefix=| suffix=| width=74 %]
      write(banner_ch,'(A74)') "[% $_ %]"[%
   @end @for %]
      write(banner_ch,'(A74)') frame

      banner_ch = 0
   end subroutine banner
   !---#] subroutine banner:

   !---#[ subroutine initgolem :
   subroutine     initgolem(is_first,stage,rndseed)
      implicit none
      logical, optional, intent(in) :: is_first
      integer, optional, intent(in) :: stage
      integer, optional, intent(in) :: rndseed
      logical :: init_third_party
      logical :: file_exists, dir_exists
      integer i, j
      character(len=50) :: file_name
      character(len=9)  :: dir_name = "BadPoints"
      character(len=6)  :: file_numb
      character(len=9)  :: file_pre = "gs_badpts"
      character(len=3)  :: file_ext = "log"
      character(len=1)  :: cstage
      character(len=4)  :: crndseed
      i = 1
      file_exists =.true.

      if(present(is_first)) then
         init_third_party = is_first
      else
         init_third_party = .true.
      end if

      if(.not. corrections_are_qcd) then
         PSP_check = .false.
      end if[%

@select r2
@case implicit explicit off %]
      if (init_third_party) then[%
   @if extension samurai %]
         call initsamurai('diag',samurai_scalar,&
         &                samurai_verbosity,samurai_test)[%
   @end @if %]
      ! call our banner
      call banner()
      if(PSP_check.and.PSP_rescue.and.PSP_verbosity) then
         inquire(file=dir_name, exist=dir_exists)
         if(.not. dir_exists) then
            call system('mkdir BadPoints')
         end if
         if(present(stage)) then
            write(cstage,'(i1)') stage
            write(crndseed,'(i4)') rndseed
            do j=1,4
               if(crndseed(j:j).eq.' ') crndseed(j:j)='0'
            enddo
            file_name = dir_name//"/"//file_pre//"-"//cstage//"-"//crndseed//"."//file_ext
            open(unit=42, file=file_name, status='replace', action='write')
            write(42,'(A22)') "<?xml version='1.0' ?>"
            write(42,'(A5)')  "<run>"
         else
            do while(file_exists)
               write(file_numb, '(I6.1)') i
               file_name = dir_name//"/"//file_pre//trim(adjustl(file_numb))//"."//file_ext
               inquire(file=file_name, exist=file_exists)
               if(file_exists) then
                  write(*,*) "File ", file_name, " already exists!"
                  i = i+1
               else
                  write(*,*) "Bad points stored in file: ", file_name
                  open(unit=42, file=file_name, status='unknown', action='write')
                  write(42,'(A22)') "<?xml version='1.0' ?>"
                  write(42,'(A5)')  "<run>"
               end if
            enddo
         end if
      end if
      end if[%
@end @select %]

      call init_functions()
      call init_color()

   end subroutine initgolem
   !---#] subroutine initgolem :
   !---#[ subroutine exitgolem :
   subroutine     exitgolem(is_last)[%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %]
      use [% process_name asprefix=\_ %]groups, only: tear_down_golem95[%
   @end @if %][%
@end @select %]
      implicit none
      logical, optional, intent(in) :: is_last
      
      logical :: exit_third_party

      if(present(is_last)) then
         exit_third_party = is_last
      else
         exit_third_party = .true.
      end if[%

@select r2
@case implicit explicit off %]
      if (exit_third_party) then[%
   @if extension samurai %]
         call exitsamurai()[%
   @end @if %][%
   @if extension golem95 %]
         call tear_down_golem95()[%
   @end @if %]
         if(PSP_check.and.PSP_rescue.and.PSP_verbosity) then
            write(42,'(A6)')  "</run>"
            close(unit=42)
         endif
      end if[%
@end @select %]
   end subroutine exitgolem
   !---#] subroutine exitgolem :

   !---#[ subroutine samplitude :
   subroutine     samplitude(vecs, scale2, amp, prec, ok, h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), dimension([%num_legs%], 4) :: vecsrot
      real(ki), intent(in) :: scale2
      real(ki), dimension(1:4), intent(out) :: amp
      real(ki), dimension(1:4) :: ampdef, amprot, ampres, ampresrot
      real(ki) :: rat2, kfac, zero, angle
      real(ki), dimension(2:3) :: irp
      integer, intent(out) :: prec
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h
      integer spprec1, fpprec1, spprec2, fpprec2
      integer tmp_red_int, icheck, i, irot
      ampdef=0.0_ki
      amprot=0.0_ki
      ampres=0.0_ki
      ampresrot=0.0_ki
      icheck = 1
      angle = 1.234_ki
      fpprec1 = 18
      fpprec2 = 18
      if(reduction_interoperation.eq.reduction_interoperation_rescue) &
           & PSP_rescue=.false.
      tmp_red_int = reduction_interoperation
      call samplitudel01(vecs, scale2, ampdef, rat2, ok, h)
      amp = ampdef
      ! RESCUE SYSTEM
      if(PSP_check) then[%
              @if anymember PoleRotation PSP_chk_method ignore_case=true %]
         call ir_subtraction(vecs, scale2, irp, h)
         if((ampdef(3)-irp(2)) .ne. 0.0_ki) then
            spprec1 = -int(log10(abs((ampdef(3)-irp(2))/irp(2))))
         else
            spprec1 = 16
         endif
         if(ampdef(1) .ne. 0.0_ki) then
            kfac = abs(ampdef(2)/ampdef(1))
         else
            kfac = 0.0_ki
         endif
         if(spprec1.lt.PSP_chk_th1.and.spprec1.ge.PSP_chk_th2 &
              .or.(kfac.gt.PSP_chk_kfactor.and.PSP_chk_kfactor.gt.0)) icheck=2 ! ROTATION
         if(spprec1.lt.PSP_chk_th2) then                                       ! RESCUE
            icheck=3
            fpprec1=-10        ! Set -10 as finite part precision
         endif[%
         @elif anymember Rotation PSP_chk_method ignore_case=true %]
         icheck=2 ! do rotation in all cases (PSP_chk_method=Rotation)
         [%
         @else %]
         ! poles should be zero for loop-induced processes
         if(ampdef(2) .ne. 0.0_ki .and. ampdef(3) .ne. 0.0_ki) then
            spprec1 = -int(log10(abs((ampdef(3)/ampdef(2)))))
         else
            spprec1 = 18
         endif
         kfac = 0.0_ki
         if(spprec1.lt.PSP_chk_li1.and.spprec1.ge.PSP_chk_li2) then
            icheck=2 ! ROTATION
         end if
         if(spprec1.lt.PSP_chk_li2) then                                       ! RESCUE
            icheck=3
            fpprec1=-10        ! Set -10 as finite part precision
         end if[%
         @end @if %]
         if(icheck.eq.2) then
            do irot = 1,[%num_legs%]
               vecsrot(irot,1) = vecs(irot,1)
               vecsrot(irot,2) = vecs(irot,2)*Cos(angle)-vecs(irot,3)*Sin(angle)
               vecsrot(irot,3) = vecs(irot,2)*Sin(angle)+vecs(irot,3)*Cos(angle)
               vecsrot(irot,4) = vecs(irot,4)
            enddo
            call samplitudel01(vecsrot, scale2, amprot, rat2, ok, h)
            if((amprot(2)-amp(2)) .ne. 0.0_ki) then
               fpprec1 = -int(log10(abs((amprot(2)-amp(2))/((amprot(2)+amp(2))/2.0_ki))))
            else
               fpprec1 = 16
            endif[%
            @if anymember PoleRotation PSP_chk_method ignore_case=true %]
            if(fpprec1.ge.PSP_chk_th3) icheck=1                            ! ACCEPTED
            if(fpprec1.lt.PSP_chk_th3) icheck=3                            ! RESCUE[%
            @else %]
            if(fpprec1.ge.PSP_chk_li3) icheck=1                            ! ACCEPTED
            if(fpprec1.lt.PSP_chk_li3) icheck=3                            ! RESCUE[%
            @end @if %]
         endif
         prec = min(spprec1,fpprec1)

         if(icheck.eq.3.and.PSP_rescue) then
            icheck=1
            reduction_interoperation = reduction_interoperation_rescue
            call samplitudel01(vecs, scale2, ampres, rat2, ok, h)
            amp=ampres[%
            @if anymember PoleRotation Rotation PSP_chk_method ignore_case=true %]
            if((ampres(3)-irp(2)) .ne. 0.0_ki) then
               spprec2 = -int(log10(abs((ampres(3)-irp(2))/irp(2))))
            else
               spprec2 = 16
            endif
            if(ampres(1) .ne. 0.0_ki) then
               kfac = abs(ampres(2)/ampres(1))
            else
               kfac = 0.0_ki
            endif
            ! if(spprec2.lt.PSP_chk_th1.and.spprec2.ge.PSP_chk_th2 &
            !      .or.(kfac.gt.PSP_chk_kfactor.and.PSP_chk_kfactor.gt.0)) icheck=2 ! ROTATION
            ! if(spprec2.lt.PSP_chk_th2) then                                       ! DISCARD
            if(spprec2.lt.PSP_chk_th3 &
                 .or.(kfac.gt.PSP_chk_kfactor.and.PSP_chk_kfactor.gt.0)) then ! DISCARD
               icheck=3
               fpprec2=-10        ! Set -10 as finite part precision
            endif[%
            @else %]
            ! poles should be zero for loop-induced processes
            if(ampres(2) .ne. 0.0_ki .and. ampres(3) .ne. 0.0_ki) then
               spprec2 = -int(log10(abs(ampres(3)/ampres(2))))
            else
               spprec2 = 16
            endif
            kfac = 0.0_ki
            if(spprec2.lt.PSP_chk_li4) then ! DISCARD
               icheck=3
               fpprec2=-10        ! Set -10 as finite part precision
            endif[%
            @end @if %]
            if(icheck.eq.2) then
               do irot = 1,[%num_legs%]
                  vecsrot(irot,1) = vecs(irot,1)
                  vecsrot(irot,2) = vecs(irot,2)*Cos(angle)-vecs(irot,3)*Sin(angle)
                  vecsrot(irot,3) = vecs(irot,2)*Sin(angle)+vecs(irot,3)*Cos(angle)
                  vecsrot(irot,4) = vecs(irot,4)
               enddo
               ! call adjust_kinematics(vecsrot)
               call samplitudel01(vecsrot, scale2, ampresrot, rat2, ok, h)
               if((ampresrot(2)-ampres(2)) .ne. 0.0_ki) then
                  fpprec2 = -int(log10(abs((ampresrot(2)-ampres(2))/((ampresrot(2)+ampres(2))/2.0_ki))))
               else
                  fpprec2 = 16
               endif[%
            @if anymember PoleRotation Rotation PSP_chk_method ignore_case=true %]
               if(fpprec2.ge.PSP_chk_th3) icheck=1                         ! ACCEPTED
               if(fpprec2.lt.PSP_chk_th3) icheck=3                         ! DISCARD[%
               @else %]
               if(fpprec2.ge.PSP_chk_li3) icheck=1                         ! ACCEPTED
               if(fpprec2.lt.PSP_chk_li3) icheck=3                         ! DISCARD[%
               @end @if %]
            endif
            reduction_interoperation = tmp_red_int
            prec = min(spprec2,fpprec2)
         endif

         if(icheck.eq.3.and.PSP_verbosity) then
            write(42,'(2x,A7)')"<event>"
            write(42,'(4x,A15,A[% process_name asstringlength=\ %],A3)') & 
                 &  "<process name='","[% process_name %]","'/>"[%
           @if anymember PoleRotation Rotation PSP_chk_method ignore_case=true %]
            write(42,'(4x,A21,I2.1,A7,I2.1,A7,I2.1,A3)') &
                 &  "<PSP_thresholds th1='", PSP_chk_th1, &
                 &                "' th2='", PSP_chk_th2, &
                 &                "' th3='", PSP_chk_th3,"'/>"[%
           @else %]
            write(42,'(4x,A21,I2.1,A7,I2.1,A7,I2.1,A7,I2.1,A3)') &
                 &  "<PSP_thresholds li1='", PSP_chk_li1, &
                 &                "' li2='", PSP_chk_li2, &
                 &                "' li3='", PSP_chk_li3, &
                 &                "' li4='", PSP_chk_li4,"'/>"[% @end @if %]
            write(42,'(4x,A16,D23.16,A3)') &
                 &  "<PSP_kfaktor k='", PSP_chk_kfactor,"'/>"
            write(42,'(4x,A15,I3.1,A6,I3.1,A3)') &
                 &  "<PSP_prec1 sp='", spprec1, "' fp='", fpprec1, "'/>"
            write(42,'(4x,A15,I3.1,A6,I3.1,A3)') &
                 &  "<PSP_prec2 sp='", spprec2, "' fp='", fpprec2, "'/>"
            write(42,'(4x,A10,D23.16,A3)') &
                 &  "<born LO='", ampdef(1), "'/>"
            write(42,'(4x,A10,D23.16,A3)') &
                 &  "<rat2 r2='", rat2, "'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<amp       sp='", ampdef(3)   ,"' ir='", irp(2),"' fp='", ampdef(2)   ,"'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<amprot    sp='", amprot(3)   ,"' ir='", irp(2),"' fp='", amprot(2)   ,"'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<ampres    sp='", ampres(3)   ,"' ir='", irp(2),"' fp='", ampres(2)   ,"'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<ampresrot sp='", ampresrot(3),"' ir='", irp(2),"' fp='", ampresrot(2),"'/>"
            write(42,'(4x,A9)') "<momenta>"
            do i=1,[%num_legs%]
               write(42,'(8x,A8,3(D23.16,A6),D23.16,A3)') "<mom e='", vecs(i,1), &
                    &  "' px='", vecs(i,2), &
                    &  "' py='", vecs(i,3), &
                    &  "' pz='", vecs(i,4), "'/>"
            enddo
            write(42,'(4x,A10)')"</momenta>"
            write(42,'(2x,A8)')"</event>"
         endif
      else
         prec = 20 ! If PSP_check is off, precision is set to unrealistic value = 20.
      end if
 end subroutine samplitude
   !---#] subroutine samplitude :

   !---#[ subroutine samplitudel01 :
   subroutine     samplitudel01(vecs, scale2, amp, rat2, ok, h)
      use [% process_name asprefix=\_ %]config, only: &
         & debug_lo_diagrams, debug_nlo_diagrams, logfile, deltaOS, &
         & renormalisation, renorm_beta, renorm_mqwf, renorm_decoupling, &
         & renorm_logs, renorm_mqse, nlo_prefactors
      use [% process_name asprefix=\_ %]kinematics, only: &
         & inspect_kinematics, init_event
      use [% process_name asprefix=\_ %]model
      use [% process_name asprefix=\_ %]dipoles, only: pi
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(4), intent(out) :: amp
      real(ki), intent(out) :: rat2
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h
      real(ki) :: nlo_coupling

      complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)

      ! Number of heavy quark flavours in loops.
      real(ki), parameter :: NFh = [% count quark_loop_masses %].0_ki

      logical :: my_ok

      ! used for m=0 QCD renormalisation
      real(ki) :: beta0

      if(corrections_are_qcd) then[%
      @select QCD_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki[%
      @else %]
         nlo_coupling = [% QCD_COUPLING_NAME %]*[% QCD_COUPLING_NAME %][%
      @end @select %]
      else[%
      @select QED_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki[%
      @else %]
         nlo_coupling = [% QED_COUPLING_NAME %]*[% QED_COUPLING_NAME %][%
      @end @select %]
      end if

      if(debug_lo_diagrams .or. debug_nlo_diagrams) then
         call init_event(vecs)
         write(logfile,'(A7)') "<event>"
         call inspect_kinematics(logfile)
      end if

      [% @if generate_lo_diagrams %]
      if (present(h)) then
         amp(1) = samplitudel0(vecs, h)
      else
         amp(1)   = samplitudel0(vecs)
      end if[%
      @else %]
      amp(1)   = 0.0_ki[%
      @end @if%][%
      @if generate_nlo_virt %]
      select case (renormalisation)
      case (0)
         ! no renormalisation
         deltaOS = 0.0_ki
      case (1)
         ! fully renormalized 
         if(renorm_mqse) then
            deltaOS = 1.0_ki
         else
            deltaOS = 0.0_ki
         end if
      case (2)
         ! massive quark counterterms only
         deltaOS = 1.0_ki
      case default
         ! not implemented
         print*, "In [% process_name asprefix=\_ %]matrix:"
         print*, "  invalid value for renormalisation=", renormalisation
         stop
      end select

      if (present(h)) then[%
         @if helsum %]
         print *, 'ERROR: Cannot select helicity when code was generated'
         print *, 'with "helsum=1".'[%
         @else %]
         amp((/4,3,2/)) = samplitudel1(vecs, scale2, my_ok, rat2, h)/nlo_coupling[%
         @end @if %]
      else
         amp((/4,3,2/)) = samplitudel1(vecs, scale2, my_ok, rat2)/nlo_coupling
      end if[%

         @select r2
         @case implicit explicit off %]
      select case (renormalisation)
      case (0)
         ! no renormalisation
      case (1)
         ! fully renormalized[%
            @if generate_lo_diagrams %]
         if(corrections_are_qcd) then
            if (renorm_beta) then
               beta0 = (11.0_ki * CA - 4.0_ki * TR * (NF + NFh)) / 6.0_ki
               amp(3) = amp(3) - lo_qcd_couplings * beta0 * amp(1)[%
               @for effective_higgs %][%
               @if is_ehc%]
               ! Adding finite renormalization of Wilson coefficient for effective Higgs coupling
               !amp(2) = amp(2) + (11.0_ki -2.0_ki/3.0_ki*log(scale2/mH**2)) * amp(1)
               amp(2) = amp(2) + (11.0_ki) * amp(1)[%
               @end @if %][%
               @end @for %][%
               @for quark_loop_masses %][%
                  @if is_first %]
               if (renorm_logs) then[%
                  @end @if %][%
                  @if is_real %]
                  amp(2) = amp(2) + lo_qcd_couplings * 4.0_ki * TR / 6.0_ki * &
                      &            log(scale2/[% $_ %]**2) * amp(1)[%
                  @end @if %] [%
                  @if is_complex %]
                  amp(2) = amp(2) + lo_qcd_couplings * 4.0_ki * TR / 6.0_ki * &
                      &            log(scale2/[% $_ %]/conjg([% $_ %])) * amp(1)[%
                  @end @if %] [%
                  @if is_last %]
               end if[%
                  @end @if %][%
               @end @for %][%
               @if extension dred %]
               amp(2) = amp(2) + lo_qcd_couplings * CA / 6.0_ki * amp(1)[%
               @end @if %]
            end if
            if (renorm_mqwf) then[%
            @for particles massive quarks anti-quarks %][%
               @if is_first %]
            ! wave function renormalisation:[%
               @end @if %]
               amp(3) = amp(3) - 1.5_ki * CF * amp(1)
               amp(2) = amp(2) - [%
               @if extension dred %]2.5[% @else %]2.0[%
               @end @if %]_ki * CF * amp(1)
               if (renorm_logs) then
                  amp(2) = amp(2) &
                 &   - (1.5_ki*log(scale2/[%mass%]/[%mass%])) * CF * amp(1)
               end if[%
            @end @for %]
            end if[%
            @for quark_loop_masses %][%
               @if is_first %]
            if (renorm_decoupling) then
               amp(3) = amp(3) - num_gluons * 2.0_ki * TR / 3.0_ki * NFh * &
                                &  amp(1)
                    
               if (renorm_logs) then[%
               @end @if %][%
               @if is_real %]
                  amp(2) = amp(2) - num_gluons * 2.0_ki * TR / 3.0_ki * &
                      &            log(scale2/[% $_ %]**2) * amp(1)[%
                  @end @if %] [%
                  @if is_complex %]
                  amp(2) = amp(2) - num_gluons * 2.0_ki * TR / 3.0_ki * &
                       &            log(scale2/[% $_ %]/conjg([% $_ %])) * amp(1)[%
                  @end @if %] [%
               @if is_last %]
               end if
            end if[%
               @end @if %][%
            @end @for %]
         end if[%
            @else %]
         ! No tree level present[%
            @end @if %]
      case (2)
         ! massive quark counterterms only
      case default
         ! not implemented
         print*, "In [% process_name asprefix=\_ %]matrix:"
         print*, "  invalid value for renormalisation=", renormalisation
         stop
      end select[%
         @end @select r2 %][%
      @else %]
      amp(2:4) = 0.0_ki[%
      @end @if%][%

      @select r2
      @case implicit explicit off %]
      if (convert_to_cdr) then
         ! Scheme conversion for infrared structure
         ! Reference:
         ! S. Catani, M. H. Seymour, Z. Trocsanyi,
         ! ``Regularisation scheme independence and unitarity
         !   in QCD cross-sections,''
         ! Phys.Rev. D 55 (1997) 6819
         ! arXiv:hep-ph/9610553[%
         @if extension dred %]
         amp(2) = amp(2) - amp(1) * (&
           &          num_light_quarks * 0.5_ki * CF &
           &        + num_gluons * 1.0_ki/6.0_ki * CA)[%
         @end @if extension dred %]
      end if[%
      @end @select r2 %]
      if (present(ok)) ok = my_ok

      if(debug_lo_diagrams .or. debug_nlo_diagrams) then
         write(logfile,'(A25,E24.16,A3)') &
            & "<result kind='lo' value='", amp(1), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-finite' value='", amp(2), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-single' value='", amp(3), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-double' value='", amp(4), "'/>"
         if(my_ok) then
            write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
         else
            write(logfile,'(A29)') "<flag name='ok' status='no'/>"
         end if
         write(logfile,'(A8)') "</event>"
      end if[%
      @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]
      amp(1) = amp(1) * get_formfactor_lo(vecs)[%@end @if %][%
      @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
      amp(2:4) = amp(2:4) * get_formfactor_nlo(vecs)[%@end @if %][%
      @if generate_nlo_virt %]
      select case(nlo_prefactors)
      case(0)
         ! The result is already in its desired form[%
      @if generate_lo_diagrams %]
      case(1)
         amp(2:4) = amp(2:4) * nlo_coupling
      case(2)
         amp(2:4) = amp(2:4) * nlo_coupling / 8.0_ki / pi / pi[%
      @else %]
      case(1)
         ! loop-induced
         amp(2:4) = amp(2:4) * nlo_coupling * nlo_coupling
      case(2)
         ! loop-induced
         amp(2:4) = amp(2:4) * (nlo_coupling / 8.0_ki / pi / pi)**2[%
      @end @if %]
      end select[%@end @if %]
   end subroutine samplitudel01
   !---#] subroutine samplitudel01 :
   !---#[ function samplitudel0 :
   function     samplitudel0(vecs, h) result(amp)
      use [% process_name asprefix=\_ %]config, only: logfile
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      integer, optional, intent(in) :: h
      real(ki) :: amp, heli_amp
      complex(ki), dimension(numcs) :: color_vector
      logical, dimension(0:[% eval num_helicities - 1 %]) :: eval_heli
      real(ki), dimension([%num_legs%], 4) :: pvecs

      if (present(h)) then
         eval_heli(:) = .false.
         eval_heli(h) = .true.
      else
         eval_heli(:) = .true.
      end if

      amp = 0.0_ki[%
  @if generate_lo_diagrams %][%
  @for helicities %]
      if (eval_heli([%helicity%])) then
         if (debug_lo_diagrams) then
            write(logfile,*) "<helicity index='[% helicity %]' >"
         end if
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:
         color_vector = amplitude[% map.index %]l0()
         heli_amp = square(color_vector)
         if (debug_lo_diagrams) then
            write(logfile,'(A25,E24.16,A3)') &
                & "<result kind='lo' value='", heli_amp, "'/>"
            write(logfile,*) "</helicity>"
         end if
         amp = amp + heli_amp
      end if[%
  @end @for helicities %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if[%
   @end @if %]
   end function samplitudel0
   !---#] function samplitudel0 :
   !---#[ function samplitudel1 :
   function     samplitudel1(vecs,scale2,ok,rat2[% @if helsum %][% @else %],h[% @end @if %]) result(amp)
      use [% process_name asprefix=\_ %]config, only: &
         & debug_nlo_diagrams, logfile, renorm_gamma5
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki), intent(in) :: scale2
      real(ki), intent(out) :: rat2[%
      @if helsum %][%
      @else %]
      integer, optional, intent(in) :: h
      real(ki), dimension([%num_legs%], 4) :: pvecs[%
      @end @if %]
      real(ki), dimension(-2:0) :: amp, heli_amp[%
      @if generate_lo_diagrams %][%
      @else %]
      complex(ki), dimension(numcs,-2:0) :: colorvec
      integer :: c[%
      @end @if %]
      logical :: my_ok
      logical, dimension(0:[% eval num_helicities - 1 %]) :: eval_heli
      real(ki) :: fr, rational2

      amp(:) = 0.0_ki
      rat2 = 0.0_ki
      ok = .true.[%
   @if generate_nlo_virt%][%
   @if helsum %]
      if(debug_nlo_diagrams) then
         write(logfile,*) "<helicity index='sum'>"
      end if
      call init_event(vecs)[%
      @if generate_lo_diagrams %]
         heli_amp = samplitudel1summed(real(scale2,ki),my_ok,rational2)[%
      @else %]
         do c=1,numcs
            colorvec(c,:) = samplitudel1summed(real(scale2,ki),my_ok,rational2,c)
         end do
         heli_amp( 0) = square(colorvec(:, 0))
         heli_amp(-1) = square(colorvec(:,-1))
         heli_amp(-2) = square(colorvec(:,-2))[%
      @end @if %]
         ok = ok .and. my_ok
         amp = amp + heli_amp
         rat2 = rat2 + rational2

         if(debug_nlo_diagrams) then
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-finite' value='", heli_amp(0), "'/>"
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-single' value='", heli_amp(-1), "'/>"
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-double' value='", heli_amp(-2), "'/>"
            if(my_ok) then
               write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
            else
               write(logfile,'(A29)') "<flag name='ok' status='no'/>"
            end if
            write(logfile,*) "</helicity>"
         end if[%
   @else %][% 'if not helsum' %]

      if (present(h)) then
         eval_heli(:) = .false.
         eval_heli(h) = .true.
      else
         eval_heli(:) = .true.
      end if

[%
   @for helicities%]
      if (eval_heli([%helicity%])) then
         if(debug_nlo_diagrams) then
            write(logfile,*) "<helicity index='[% helicity %]'>"
         end if[%
      @if generate_lo_diagrams %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:
         heli_amp = samplitudeh[% map.index %]l1(real(scale2,ki),my_ok,rational2)[%
      @else %]
         !---#[ reinitialize kinematics:[%
         @for helicity_mapping shift=1 %][%
            @if parity %][%
               @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
               @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
               @end @select %][%
            @else %][%
               @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
               @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
               @end @select %][%
            @end @if %][%
         @end @for %]
         call init_event(pvecs[%
         @for particles lightlike vector %], [%hel%]1[%
         @end @for %])
            !---#] reinitialize kinematics:
         do c=1,numcs
            colorvec(c,:) = samplitudeh[%map.index%]l1(real(scale2,ki),my_ok,rational2,c)
         end do
         heli_amp( 0) = square(colorvec(:, 0))
         heli_amp(-1) = square(colorvec(:,-1))
         heli_amp(-2) = square(colorvec(:,-2))
      [%
      @end @if %]
         if (corrections_are_qcd .and. renorm_gamma5) then
            !---#[ reinitialize kinematics:[%
      @for helicity_mapping shift=1 %][%
         @if parity %][%
            @select sign @case 1 %]
            pvecs([%index%],1) = vecs([%$_%],1)
            pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
            @else %]
            pvecs([%index%],1) = -vecs([%$_%],1)
            pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
            @end @select %][%
         @else %][%
            @select sign @case 1 %]
            pvecs([%index%],:) = vecs([%$_%],:)[%
            @else %]
            pvecs([%index%],:) = -vecs([%$_%],:)[%
            @end @select %][%
         @end @if %][%
      @end @for %]
            call init_event(pvecs[%
         @for particles lightlike vector %], [%hel%]1[%
         @end @for %])
            !---#] reinitialize kinematics:
            fr = finite_renormalisation[%map.index%](real(scale2,ki))
            heli_amp(0) = heli_amp(0) + fr
         end if
         ok = ok .and. my_ok
         amp = amp + heli_amp
         rat2 = rat2 + rational2

         if(debug_nlo_diagrams) then
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-finite' value='", heli_amp(0), "'/>"
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-single' value='", heli_amp(-1), "'/>"
            write(logfile,'(A33,E24.16,A3)') &
                & "<result kind='nlo-double' value='", heli_amp(-2), "'/>"
            if (corrections_are_qcd .and. renorm_gamma5) then
               write(logfile,'(A30,E24.16,A3)') &
                   & "<result kind='fin-ren' value='", fr, "'/>"
            end if
            if(my_ok) then
               write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
            else
               write(logfile,'(A29)') "<flag name='ok' status='no'/>"
            end if
            write(logfile,*) "</helicity>"
         end if
      end if[%
   @end @for helicities%][%
   @end @if %][%
   @end @if helsum %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if
   end function samplitudel1
   !---#] function samplitudel1 :
   !---#[ subroutine ir_subtraction :
   subroutine     ir_subtraction(vecs,scale2,amp,h)
      use [% process_name asprefix=\_ %]config, only: &
         & nlo_prefactors
      use [% process_name asprefix=\_ %]dipoles, only: pi
      use [% process_name asprefix=\_ %]kinematics, only: &
         & init_event, corrections_are_qcd
      use [% process_name asprefix=\_ %]model
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      integer, optional, intent(in) :: h
      real(ki), dimension(2), intent(out) :: amp
      real(ki), dimension(2) :: heli_amp
      real(ki), dimension([%num_legs%], 4) :: pvecs
      complex(ki), dimension(numcs,numcs,2) :: oper
      complex(ki), dimension(numcs) :: color_vectorl0, pcolor
      logical, dimension(0:[% eval num_helicities - 1 %]) :: eval_heli
      real(ki) :: nlo_coupling

      if (present(h)) then
         eval_heli(:) = .false.
         eval_heli(h) = .true.
      else
         eval_heli(:) = .true.
      end if

      if(corrections_are_qcd) then[%
      @select QCD_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki[%
      @else %]
         nlo_coupling = [% QCD_COUPLING_NAME %]*[% QCD_COUPLING_NAME %][%
      @end @select %]
      else[%
      @select QED_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki[%
      @else %]
         nlo_coupling = [% QED_COUPLING_NAME %]*[% QED_COUPLING_NAME %][%
      @end @select %]
      end if
     
      if (corrections_are_qcd) then
        oper = insertion_operator(real(scale2,ki), vecs)
      else
        oper = insertion_operator_qed(real(scale2,ki), vecs)
      endif
      amp(:) = 0.0_ki[%
  @if generate_lo_diagrams %][%
  @for helicities %]
      if (eval_heli([%helicity%])) then
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:
         pcolor = amplitude[%map.index%]l0()[%
     @for color_mapping shift=1%]
         color_vectorl0([% $_ %]) = pcolor([% index %])[%
     @end @for %]
         if (corrections_are_qcd) then
           heli_amp(1) = square(color_vectorl0, oper(:,:,1))
           heli_amp(2) = square(color_vectorl0, oper(:,:,2))
         else
           heli_amp(1) = square(color_vectorl0)*oper(1,1,1)
           heli_amp(2) = square(color_vectorl0)*oper(1,1,2)
         endif
         amp = amp + heli_amp
      endif[%
  @end @for helicities %][%
      @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
      amp = amp * get_formfactor_nlo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if[%
   @end @if %]
      select case(nlo_prefactors)
      case(0)
         ! The result is already in its desired form
      case(1)
         amp(:) = amp(:) * nlo_coupling
      case(2)
         amp(:) = amp(:) * nlo_coupling / 8.0_ki / pi / pi
      end select
   end subroutine ir_subtraction
   !---#] subroutine ir_subtraction :
   !---#[ color correlated ME :
   pure subroutine color_correlated_lo(color_vector,res)
      use [% process_name asprefix=\_ %]color, only: [%
      @for pairs colored1 colored2 ordered %][%
      @if is_first %][% @else %], &
      & [% @end @if %]T[%index1%]T[%index2%][%
      @end @for pairs %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      real(ki), dimension(num_legs,num_legs), intent(out) :: res
      res(:,:)=0.0_ki[%
      @for pairs colored1 colored2 ordered %]
      res([%index1%],[%index2%]) = square(color_vector,T[%
        index1%]T[%index2%])
      res([%index2%],[%index1%]) = res([%index1%],[%index2%])[%
      @end @for pairs %]
   end subroutine color_correlated_lo

   subroutine     color_correlated_lo2(vecs,borncc)
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,num_legs), intent(out) :: borncc
      real(ki), dimension(num_legs,num_legs) :: borncc_heli
      real(ki), dimension(num_legs, 4) :: pvecs
      complex(ki), dimension(numcs) :: color_vector

      borncc(:,:) = 0.0_ki[%
  @if generate_lo_diagrams %][%
  @for helicities %]
      !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
      pvecs([%index%],1) = vecs([%$_%],1)
      pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
      pvecs([%index%],1) = -vecs([%$_%],1)
      pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
      pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
      pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
      call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
      !---#] reinitialize kinematics:
      color_vector = amplitude[%map.index%]l0()
      call color_correlated_lo(color_vector,borncc_heli)[%
      @if is_first %]
      ! The minus is part in the definition according to PowHEG Box.
      ! Since they use it we include it:[%
      @end @if is_first %]
      borncc(:,:) = borncc(:,:) - borncc_heli(:,:)[%
  @end @for helicities %]
      if (include_helicity_avg_factor) then
         borncc = borncc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         borncc = borncc / incolors
      end if
      if (include_symmetry_factor) then
         borncc = borncc / real(symmetry_factor, ki)
      end if[%
   @end @if %]
   end subroutine color_correlated_lo2


   pure subroutine OLP_color_correlated_lo(color_vector,res)
      use [% process_name asprefix=\_ %]color, only: [%
      @for pairs colored1 colored2 ordered %][%
      @if is_first %][% @else %], &
      & [% @end @if %]T[%index1%]T[%index2%][%
      @end @for pairs %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      real(ki), dimension(num_legs*(num_legs-1)/2), intent(out) :: res
      res(:)=0.0_ki[%
      @for pairs colored1 colored2 ordered %] [%
      @if eval index1 .ne. index2 %]
      res([% eval index1 - 1 + ( index2 - 1 ) * ( index2 - 2 ) // 2 + 1 %]) = square(color_vector,T[%
        index1%]T[%index2%])[%
      @end @if %] [%
      @end @for pairs %]
   end subroutine OLP_color_correlated_lo


   subroutine OLP_color_correlated(vecs,ampcc)
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs*(num_legs-1)/2), intent(out) :: ampcc
      real(ki), dimension(num_legs,num_legs) :: borncc
      real(ki), dimension(num_legs*(num_legs-1)/2) :: ampcc_heli
      real(ki), dimension(num_legs, 4) :: pvecs
      complex(ki), dimension(numcs) :: color_vector
      ampcc(:) = 0.0_ki[%
  @if generate_lo_diagrams %][%
  @for helicities %]
      !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
      pvecs([%index%],1) = vecs([%$_%],1)
      pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
      pvecs([%index%],1) = -vecs([%$_%],1)
      pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
      pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
      pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
      call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
      !---#] reinitialize kinematics:
      color_vector = amplitude[%map.index%]l0()
      call OLP_color_correlated_lo(color_vector,ampcc_heli)
      ampcc(:) = ampcc(:) + ampcc_heli(:)[%
  @end @for helicities %]

      [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]ampcc = ampcc*get_formfactor_lo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         ampcc = ampcc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         ampcc = ampcc / incolors
      end if
      if (include_symmetry_factor) then
         ampcc = ampcc / real(symmetry_factor, ki)
      end if[%
   @end @if %]


   end subroutine OLP_color_correlated


   !---#] color correlated ME :
   !---#[ spin correlated ME :
   subroutine spin_correlated_lo2(vecs, bornsc)
      use [% process_name asprefix=\_ %]kinematics
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,4,4) :: bornsc
      real(ki), dimension(num_legs, 4) :: pvecs
      complex(ki), dimension(4,4) :: tens
      complex(ki) :: pp, pm, mp, mm[%
@if generate_lo_diagrams %][%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      complex(ki), dimension(numcs) :: heli_amp[%helicity%][%
         @end @for %][%
      @end @if is_first %]
      complex(ki), dimension(4) :: eps[%index%][%
   @end @for %][%
@end @if generate_lo_diagrams %]

      bornsc(:,:,:) = 0.0_ki
      !---#[ Initialize helicity amplitudes :[%
@if generate_lo_diagrams %][%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      !---#[ reinitialize kinematics:[%
            @for helicity_mapping shift=1 %][%
               @if parity %][%
                  @select sign @case 1 %]
      pvecs([%index%],1) = vecs([%$_%],1)
      pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
                  @else %]
      pvecs([%index%],1) = -vecs([%$_%],1)
      pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
                  @end @select %][%
               @else %][%
                  @select sign @case 1 %]
      pvecs([%index%],:) = vecs([%$_%],:)[%
                  @else %]
      pvecs([%index%],:) = -vecs([%$_%],:)[%
                  @end @select %][%
               @end @if %][%
            @end @for %]
      call init_event(pvecs[%
            @for particles lightlike vector %], [%hel%]1[%
            @end @for %])
      !---#] reinitialize kinematics:
      heli_amp[%helicity%] = amplitude[% map.index %]l0()[%
         @end @for helicities %][%
      @end @if is_first %][%
   @end @for %]
      !---#] Initialize helicity amplitudes :
      !---#[ Initialize polarization vectors :[%
   @for particles lightlike vector initial %]
      eps[%index%] = spva[% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %]k[%index%]/Spaa([% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %],k[%index%])/sqrt2[%
   @end @for %][%
   @for particles lightlike vector final %]
      eps[%index%] = conjg(spva[%
      @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %]k[%index%]/Spaa([% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %],k[%index%])/sqrt2)[%
   @end @for %]
      !---#] Initialize polarization vectors :
      ! Note: By omitting the imaginary parts we lose a term:
      !   Imag(B_j(mu,nu)) = i_ * e_(k_j, mu, q_j, nu) * |Born|^2
      ! where q_j is the reference momentum chosen for the paticle
      ! of momentum k_j. This term should, however not be phenomenologically
      ! relevant.[%
   @for particles lightlike vector %]
      !---#[ particle [%index%] :
      pp  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
      &          + square_0l_0l_sc(heli_amp[%helicity%],heli_amp[%helicity%])[%
      @end @for helicities %]
      pm  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
              symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_0l_0l_sc(heli_amp[%
                         helicity%],heli_amp[%mhelicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]
      mp  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
                symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_0l_0l_sc(heli_amp[%
                          mhelicity%],heli_amp[%helicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]
      mm  = 0.0_ki[%
      @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
      &          + square_0l_0l_sc(heli_amp[%helicity%],heli_amp[%helicity%])[%
      @end @for helicities %]

      call construct_polarization_tensor(conjg(eps[%index%]),eps[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pp, ki)
      call construct_polarization_tensor(conjg(eps[%index%]),conjg(eps[%index%]),tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pm, ki)
      call construct_polarization_tensor(eps[%index%],eps[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mp, ki)
      call construct_polarization_tensor(eps[%index%],conjg(eps[%index%]),tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mm, ki)
      !---#] particle [%index%] :[%
   @end @for %]

      [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]bornsc = bornsc*get_formfactor_lo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         bornsc = bornsc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         bornsc = bornsc / incolors
      end if
      if (include_symmetry_factor) then
         bornsc = bornsc / real(symmetry_factor, ki)
      end if[%
@end @if generate_lo_diagrams %]
   end subroutine spin_correlated_lo2




   subroutine OLP_spin_correlated_lo2(vecs, ampsc)
      use [% process_name asprefix=\_ %]kinematics
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(2*num_legs*num_legs) :: ampsc
      real(ki), dimension(num_legs, 4) :: pvecs
      integer :: i
      complex(ki) :: pm, mp[%
@if generate_lo_diagrams %][%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      complex(ki), dimension(numcs) :: heli_amp[%helicity%][%
         @end @for %][%
      @end @if is_first %]
      complex(ki), dimension(4) :: eps[%index%][%
   @end @for %][%
@end @if generate_lo_diagrams %]

      ampsc(:) = 0.0_ki
      !---#[ Initialize helicity amplitudes :[%
@if generate_lo_diagrams %][%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      !---#[ reinitialize kinematics:[%
            @for helicity_mapping shift=1 %][%
               @if parity %][%
                  @select sign @case 1 %]
      pvecs([%index%],1) = vecs([%$_%],1)
      pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
                  @else %]
      pvecs([%index%],1) = -vecs([%$_%],1)
      pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
                  @end @select %][%
               @else %][%
                  @select sign @case 1 %]
      pvecs([%index%],:) = vecs([%$_%],:)[%
                  @else %]
      pvecs([%index%],:) = -vecs([%$_%],:)[%
                  @end @select %][%
               @end @if %][%
            @end @for %]
      call init_event(pvecs[%
            @for particles lightlike vector %], [%hel%]1[%
            @end @for %])
      !---#] reinitialize kinematics:
      heli_amp[%helicity%] = amplitude[% map.index %]l0()[%
         @end @for helicities %][%
      @end @if is_first %][%
   @end @for %]
      !---#] Initialize helicity amplitudes :

      [%
   @for pairs gluons1 colored2 %][%
     @if eval index1 .ne. index2 %]
      !---#[ pair [%index1%][%index2%] :

      mp  = 0.0_ki[%
      @for helicities where=index1.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index1 to=L
                symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_[%index1%]_[%index2%]_sc(heli_amp[%
                          mhelicity%],heli_amp[%helicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]


      ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs+1)   = ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs +1) + real(mp, ki)
      ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs+2) = ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs + 2)  + real(aimag(mp),ki)

      !---#] pair [%index1%][%index2%] :
     [% @end @if %] [%
   @end @for %]

      [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]ampsc = ampsc * get_formfactor_lo(vecs)[%@end @if %]

      if (include_helicity_avg_factor) then
         ampsc = ampsc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         ampsc = ampsc / incolors
      end if
      if (include_symmetry_factor) then
         ampsc = ampsc / real(symmetry_factor, ki)
      end if[%
@end @if generate_lo_diagrams %]
   end subroutine OLP_spin_correlated_lo2
   !---#] spin correlated ME :


   !---#[ construct polarisation tensor :
   pure subroutine construct_polarization_tensor(eps1, eps2, tens)
      implicit none
      complex(ki), dimension(0:3), intent(in) :: eps1, eps2
      complex(ki), dimension(0:3,0:3), intent(out) :: tens

      integer :: mu, nu

      do mu = 0,3
         do nu = 0, 3
            tens(mu,nu) = eps1(mu) * eps2(nu)
         end do
      end do
   end  subroutine construct_polarization_tensor
   !---#] construct polarisation tensor :

   pure function square_0l_0l_sc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1, color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector2)
      v2 = conjg(color_vector1)
      amp = sum(v1(:) * v2(:))
   end function  square_0l_0l_sc


   [% @for pairs gluons1 colored2 %][%
     @if eval index1 .ne. index2 %]
   pure function square_[%index1%]_[%index2%]_sc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => [%@if eval index1 < index2%]T[%index1%]T[%index2%]
      [% @else %]T[%index2%]T[%index1%]
      [% @end @if %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1, color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector2)
      v2 = conjg(color_vector1)
      amp = sum(v1(:) * v2(:))
   end function  square_[%index1%]_[%index2%]_sc
     [% @end @if %] [%
   @end @for %]

   [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]
   function get_formfactor_lo(vecs) result(factor)
      use [% process_name asprefix=\_ %]model
      use [% process_name asprefix=\_ %]kinematics
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki) :: factor

      factor = [% form_factor_lo %]
   end function
   [% @end @if %]

   [% @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
   function get_formfactor_nlo(vecs) result(factor)
      use [% process_name asprefix=\_ %]model
      use [% process_name asprefix=\_ %]kinematics
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki) :: factor

      factor = [% form_factor_nlo %]
   end function
   [% @end @if %] 

end module [% process_name asprefix=\_ %]matrix
