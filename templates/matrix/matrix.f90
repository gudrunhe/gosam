[% ' vim: syntax=golem '
%]module     [% process_name asprefix=\_ %]matrix
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki, &
     & PSP_check, PSP_verbosity, PSP_rescue, PSP_chk_th1, &
     & PSP_chk_th2, PSP_chk_th3, PSP_chk_th4, PSP_chk_th5, &
     & PSP_chk_kfactor, PSP_chk_rotdiff, reduction_interoperation, &
     & PSP_chk_li1, PSP_chk_li2, PSP_chk_li3, PSP_chk_li4, &
     & PSP_chk_li5, PSP_chk_kfactor_li, PSP_chk_rotdiff_li, &
     & reduction_interoperation_rescue
   use [% process_name asprefix=\_ %]kinematics, only: &
       num_legs, corrections_are_qcd
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model, only: init_functions[%
@if extension quadruple %]
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model_qp, only: init_functions_qp => init_functions[%
@end @if extension quadruple %]
   use [% process_name asprefix=\_ %]color, only: init_color[%
@if extension quadruple %]
   use [% process_name asprefix=\_ %]color_qp, only: init_color_qp => init_color[%
@end @if extension quadruple %]
   use [% process_name asprefix=\_ %]matrix_dp, only: &
      & samplitudel01_dp => samplitudel01, &
      & samplitudel0_dp => samplitudel0, samplitudel0_h_dp => samplitudel0_h, &
      & samplitudel1_dp => samplitudel1, samplitudel1_h_dp => samplitudel1_h, &
      & ir_subtraction_dp => ir_subtraction, ir_subtraction_h_dp => ir_subtraction_h, &
      & color_correlated_lo2_dp => color_correlated_lo2, &
      & OLP_color_correlated_dp => OLP_color_correlated, &
      & spin_correlated_lo2_dp => spin_correlated_lo2, &
      & spin_correlated_lo2_whizard_dp => spin_correlated_lo2_whizard, &
      & OLP_spin_correlated_lo2_dp => OLP_spin_correlated_lo2[%
@if extension quadruple %]
   ! use [% process_name asprefix=\_ %]matrix_qp[%
@end @if extension quadruple %]
   use [% process_name asprefix=\_ %]rescue_system
   implicit none
   save

   private

   integer :: banner_ch = 6

   public :: initgolem, exitgolem, samplitude
   public :: samplitudel0, samplitudel0_h, samplitudel1, samplitudel1_h
   public :: ir_subtraction, color_correlated_lo2, spin_correlated_lo2
   public :: spin_correlated_lo2_whizard
   public :: OLP_color_correlated, OLP_spin_correlated_lo2

contains

   !---#[ C bindings:
   subroutine intigolem_ffi() bind(C, name="[% process_name asprefix=\_ %]initgolem")
      call initgolem()
   end subroutine

   subroutine exitgolem_ffi() bind(C, name="[% process_name asprefix=\_ %]exitgolem")
      call exitgolem()
   end subroutine

   subroutine samplitude_ffi(vecs, scale2, amp, prec) bind(C, name="[% process_name asprefix=\_ %]samplitude")
      use, intrinsic :: iso_c_binding
      implicit none
      real(kind=c_double), dimension([%num_legs%]*4), intent(in) :: vecs
      real(kind=c_double), intent(in) :: scale2
      real(kind=c_double), dimension(1:4), intent(out) :: amp
      real(ki), dimension([%num_legs%], 4) :: f_vecs
      integer(kind=c_int), intent(out) :: prec
      f_vecs(:,1) = real(vecs(1::4),ki)
      f_vecs(:,2) = real(vecs(2::4),ki)
      f_vecs(:,3) = real(vecs(3::4),ki)
      f_vecs(:,4) = real(vecs(4::4),ki)
      call samplitude(f_vecs, scale2, amp, prec)
   end subroutine
   !---#] C bindings:

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
      end if
      if (init_third_party) then
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
      end if

      call init_functions()
      call init_color()
[% @if extension quadruple %]
      call init_functions_qp()
      call init_color_qp()
[% @end @if extension quadruple %]
   end subroutine initgolem
   !---#] subroutine initgolem :

   !---#[ subroutine exitgolem :
   subroutine     exitgolem(is_last)[%
   @if extension golem95 %]
      use [% process_name asprefix=\_ %]groups, only: tear_down_golem95[%
   @end @if %]
      implicit none
      logical, optional, intent(in) :: is_last

      logical :: exit_third_party

      if(present(is_last)) then
         exit_third_party = is_last
      else
         exit_third_party = .true.
      end if
      if (exit_third_party) then[%
   @if extension golem95 %]
         call tear_down_golem95()[%
   @end @if %]
         if(PSP_check.and.PSP_rescue.and.PSP_verbosity) then
            write(42,'(A6)')  "</run>"
            close(unit=42)
         endif
      end if
   end subroutine exitgolem
   !---#] subroutine exitgolem

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
      integer icheck, i, irot
      ampdef=0.0_ki
      amprot=0.0_ki
      ampres=0.0_ki
      ampresrot=0.0_ki
      icheck=1[%
      @if anymember PoleRotation PSP_chk_method ignore_case=true %]
      icheck=1 ! do pole followed by rotation (PSP_chk_method=PoleRotation)[%
      @end @if %][%
      @if anymember LoopInduced PSP_chk_method ignore_case=true %]
      icheck=1 ! do pole followed by rotation (PSP_chk_method=LoopInduced)[%
      @end @if %][%
      @if anymember Rotation PSP_chk_method ignore_case=true %]
      icheck=2 ! do rotation in all cases (PSP_chk_method=Rotation)[%
      @end @if %]
      angle = 1.234_ki
      prec = 18
      if(reduction_interoperation.eq.reduction_interoperation_rescue) then
         ! write(*,*) '--reduction_interoperation is reduction_interoperation_rescue, disabling rescue--'
         PSP_rescue=.false.
      endif
      call samplitudel01(vecs, scale2, ampdef, rat2, ok, h)
      amp = ampdef
      ! RESCUE SYSTEM
      if(PSP_check) then
         if(icheck.eq.1) then
            ! sets prec, icheck
            call pole_check(vecs, scale2, amp, irp, prec, icheck, ok, h)
         endif
         if(icheck.eq.2) then
            ! sets amprot, prec, icheck
            call rotation_check(vecs, scale2, amp, amprot, prec, icheck, ok, h)
         endif
         if(icheck.ne.1.and.PSP_rescue) then[%
         @if extension quadruple %]
            ! sets amp, prec, icheck
            call rescue_qp(vecs, scale2, amp, ampdef, amprot, ampres, ampresrot, prec, icheck, ok, h)[%
         @else %]
            ! sets amp, ampres, ampresrot, prec, icheck
            call rescue(vecs, scale2, amp, ampdef, amprot, ampres, ampresrot, prec, icheck, ok, h)[%
         @end @if extension quadruple %]
         endif

         if(icheck.ne.1) then
            ! RESCUE SYSTEM HAS FAILED
            icheck=3                                                    ! FAIL
            fpprec2=-10        ! Set -10 as finite part precision       ! DISCARD
            prec=min(prec,fpprec2)
         endif

         ! if(icheck.eq.1) write(*,*) '--point passed--', amp(2), prec
         ! if(icheck.eq.3) write(*,*) '--point failed--', amp(2), prec

         if(icheck.eq.3.and.PSP_verbosity) then
            write(42,'(2x,A7)')"<event>"
            write(42,'(4x,A15,A[% process_name asstringlength=\ %],A3)') &
                 &  "<process name='","[% process_name %]","'/>"[%
           @if anymember PoleRotation Rotation PSP_chk_method ignore_case=true %]
            write(42,'(4x,A21,I2.1,A7,I2.1,A7,I2.1,A7,I2.1,A7,I2.1,A3)') &
                 &  "<PSP_thresholds th1='", PSP_chk_th1, &
                 &                "' th2='", PSP_chk_th2, &
                 &                "' th3='", PSP_chk_th3, &
                 &                "' th4='", PSP_chk_th4, &
                 &                "' th5='", PSP_chk_th5,"'/>"
            write(42,'(4x,A16,D23.16,A3)') &
                 &  "<PSP_kfaktor k='", PSP_chk_kfactor,"'/>"
            write(42,'(4x,A16,D23.16,A3)') &
                 &  "<PSP_rotdiff d='", PSP_chk_rotdiff,"'/>"[%
            @else %]
            write(42,'(4x,A21,I2.1,A7,I2.1,A7,I2.1,A7,I2.1,A7,I2.1,A3)') &
                 &  "<PSP_thresholds li1='", PSP_chk_li1, &
                 &                "' li2='", PSP_chk_li2, &
                 &                "' li3='", PSP_chk_li3, &
                 &                "' li4='", PSP_chk_li4, &
                 &                "' li5='", PSP_chk_li5,"'/>"
            write(42,'(4x,A19,D23.16,A3)') &
                 &  "<PSP_kfaktor_li k='", PSP_chk_kfactor_li,"'/>"
            write(42,'(4x,A19,D23.16,A3)') &
                 &  "<PSP_rotdiff_li d='", PSP_chk_rotdiff_li,"'/>"[%
            @end @if %]
            write(42,'(4x,A15,I3.1,A6,I3.1,A3)') &
                 &  "<PSP_prec1 sp='", spprec1, "' fp='", fpprec1, "'/>"
            write(42,'(4x,A15,I3.1,A6,I3.1,A3)') &
                 &  "<PSP_prec2 sp='", spprec2, "' fp='", fpprec2, "'/>"
            write(42,'(4x,A10,D23.16,A3)') &
                 &  "<born LO='", ampdef(1), "'/>"
            write(42,'(4x,A10,D23.16,A3)') &
                 &  "<rat2 r2='", rat2, "'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<amp       sp='", amp(3)   ,"' ir='", irp(2),"' fp='", amp(2)   ,"'/>"
            write(42,'(4x,A15,D23.16,A6,D23.16,A6,D23.16,A3)') &
                 &  "<ampdef    sp='", ampdef(3)   ,"' ir='", irp(2),"' fp='", ampdef(2)   ,"'/>"
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
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(4), intent(out) :: amp
      real(ki), intent(out) :: rat2
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h

      call samplitudel01_dp(vecs, scale2, amp, rat2, ok, h)

   end subroutine samplitudel01
   !---#] subroutine samplitudel01 :

   !---#[ function samplitudel0 :
   function     samplitudel0(vecs) result(amp)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki) :: amp

      amp = samplitudel0_dp(vecs)

   end function samplitudel0
   !---#] function samplitudel0 :

   !---#[ function samplitudel0_h :
   function     samplitudel0_h(vecs, h) result(amp)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      integer, optional, intent(in) :: h
      real(ki) :: amp

      amp = samplitudel0_h_dp(vecs, h)

   end function samplitudel0_h
   !---#] function samplitudel0_h :

   !---#[ function samplitudel1 :
   function     samplitudel1(vecs,scale2,ok,rat2) result(amp)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki), intent(in) :: scale2
      real(ki), intent(out) :: rat2
      real(ki), dimension(-2:0) :: amp

      amp = samplitudel1_dp(vecs,scale2,ok,rat2)

   end function samplitudel1
   !---#] function samplitudel1 :

   !---#[ function samplitudel1_h :
   function     samplitudel1_h(vecs,scale2,ok,rat2[% @if helsum %][% @else %],h[% @end @if %]) result(amp)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki), intent(in) :: scale2
      real(ki), intent(out) :: rat2[%
      @if helsum %][%
      @else %]
      integer, optional, intent(in) :: h[%
      @end @if %]
      real(ki), dimension(-2:0) :: amp

      amp = samplitudel1_h_dp(vecs,scale2,ok,rat2[% @if helsum %][% @else %],h[% @end @if %])

   end function samplitudel1_h
   !---#] function samplitudel1_h :

   !---#[ subroutine ir_subtraction :
   subroutine     ir_subtraction(vecs,scale2,amp,h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      integer, optional, intent(in) :: h
      real(ki), dimension(2), intent(out) :: amp

      call ir_subtraction_dp(vecs,scale2,amp,h)

   end subroutine ir_subtraction
   !---#] subroutine ir_subtraction :

   !---#[ subroutine ir_subtraction_h :
   subroutine     ir_subtraction_h(vecs,scale2,amp,h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      integer, optional, intent(in) :: h
      real(ki), dimension(2), intent(out) :: amp

     call ir_subtraction_h_dp(vecs,scale2,amp,h)

   end subroutine ir_subtraction_h
   !---#] subroutine ir_subtraction_h :

   !---#[ color correlated ME :
   subroutine color_correlated_lo2(vecs,borncc)
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,num_legs), intent(out) :: borncc

[% @if enable_truncation_orders %][% @if generate_tree_diagrams %][% @else %][% @if helsum%]
      write(*,*) "################################################################################"
      write(*,*) "Warning: The subroutine color_correlated_lo2 is not available for loop-induced"
      write(*,*) "processes generated with both 'enable_truncation_orders=true' and 'helsum=true'." 
      write(*,*) "################################################################################"
      stop
[% @end @if helsum%][% @end @if generate_tree_diagrams %][% @end @if enable_truncation_orders%]

      call color_correlated_lo2_dp(vecs,borncc)

   end subroutine color_correlated_lo2

   subroutine OLP_color_correlated(vecs,ampcc)
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs*(num_legs-1)/2), intent(out) :: ampcc

[% @if enable_truncation_orders %][% @if generate_tree_diagrams %][% @else %][% @if helsum%]
      write(*,*) "################################################################################"
      write(*,*) "Warning: The subroutine OLP_color_correlated is not available for loop-induced"
      write(*,*) "processes generated with both 'enable_truncation_orders=true' and 'helsum=true'." 
      write(*,*) "################################################################################"
      stop
[% @end @if helsum%][% @end @if generate_tree_diagrams %][% @end @if enable_truncation_orders%]

      call OLP_color_correlated_dp(vecs,ampcc)

   end subroutine OLP_color_correlated
   !---#] color correlated ME :

   !---#[ spin correlated ME :
   subroutine spin_correlated_lo2(vecs, bornsc)
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,4,4) :: bornsc

[% @if generate_tree_diagrams %][% @else %][% @if helsum%]
      write(*,*) "############################################################"
      write(*,*) "Warning: The subroutine spin_correlated_lo2 is not available"
      write(*,*) "for loop-induced processes generated with 'helsum=true'."
      write(*,*) "############################################################"
      stop
[% @end @if helsum%][% @end @if generate_tree_diagrams %]

      call spin_correlated_lo2_dp(vecs, bornsc)

   end subroutine spin_correlated_lo2

   subroutine spin_correlated_lo2_whizard(vecs, bornsc)
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,4,4) :: bornsc

[% @if generate_tree_diagrams %][% @else %][% @if helsum%]
      write(*,*) "####################################################################"
      write(*,*) "Warning: The subroutine spin_correlated_lo2_whizard is not available"
      write(*,*) "for loop-induced processes generated with 'helsum=true'."
      write(*,*) "####################################################################"
      stop
[% @end @if helsum%][% @end @if generate_tree_diagrams %]

      call spin_correlated_lo2_whizard_dp(vecs, bornsc)

   end subroutine spin_correlated_lo2_whizard

   subroutine OLP_spin_correlated_lo2(vecs, ampsc)
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(2*num_legs*num_legs) :: ampsc

[% @if generate_tree_diagrams %][% @else %][% @if helsum%]
      write(*,*) "################################################################"
      write(*,*) "Warning: The subroutine OLP_spin_correlated_lo2 is not available"
      write(*,*) "for loop-induced processes generated with 'helsum=true'."
      write(*,*) "################################################################"
      stop
[% @end @if helsum%][% @end @if generate_tree_diagrams %]

      call OLP_spin_correlated_lo2_dp(vecs, ampsc)

   end subroutine OLP_spin_correlated_lo2
   !---#] spin correlated ME :

end module [% process_name asprefix=\_ %]matrix
