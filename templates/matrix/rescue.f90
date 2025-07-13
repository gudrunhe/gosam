[% ' vim: syntax=golem '
%]module     [% process_name asprefix=\_ %]rescue_system
   use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]config, only: ki,[% @if extension quadruple %] ki_qp,[% @end @if extension quadruple %] &
     & PSP_chk_th1, &
     & PSP_chk_th2, PSP_chk_th3, PSP_chk_th4, PSP_chk_th5, &
     & PSP_chk_kfactor, reduction_interoperation, &
     & PSP_chk_li1, PSP_chk_li2, PSP_chk_li3, PSP_chk_li4, &
     & PSP_chk_li5, &
     & reduction_interoperation_rescue
   use [% process_name asprefix=\_ %]matrix_dp, only: samplitudel01, ir_subtraction[%
@if extension quadruple %]
   use [% process_name asprefix=\_ %]matrix_qp, only: samplitudel01_qp[%
@end @if extension quadruple %]

   implicit none
   save

   private

   public :: pole_check, rotation_check[% @if extension quadruple %], rescue_qp[% @else %], rescue[% @end @if %]

contains

   !---#[ subroutine pole_check :
   subroutine     pole_check(vecs, scale2, amp, irp, prec, icheck, ok, h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(1:4), intent(in) :: amp
      real(ki) :: kfac
      real(ki), dimension(2:3), intent(out) :: irp
      integer, intent(inout) :: prec
      integer, intent(inout) :: icheck
      logical, intent(inout), optional :: ok
      integer, intent(in), optional :: h
      integer spprec1, fpprec1
      kfac=0.0_ki
      irp=0.0_ki
      spprec1 = 18
      fpprec1 = 18[%
@if anymember LoopInduced PSP_chk_method ignore_case=true %]
      ! poles should be zero for loop-induced processes
      ! write(*,*) '--performing pole_check (loop-induced)--' 
      if(amp(2) .ne. 0.0_ki .and. amp(3) .ne. 0.0_ki) then
        spprec1 = -int(log10(abs((amp(3)/amp(2)))))
      endif
      icheck=1                                                              ! ACCEPT
      if(spprec1.lt.PSP_chk_li1.and.spprec1.ge.PSP_chk_li2) then
         icheck=2                                                           ! ROTATION
      endif
      if(spprec1.lt.PSP_chk_li2) then                                       ! RESCUE
         icheck=3
         fpprec1=-10        ! Set -10 as finite part precision
      endif[%
@else %]
      ! poles should match IR subtraction prediction
      ! write(*,*) '--performing pole_check (ir_subtraction)--' 
      call ir_subtraction(vecs, scale2, irp, h)
      if((amp(3)-irp(2)) .ne. 0.0_ki) then      ! single pole vs IR prediction
         spprec1 = -int(log10(abs((amp(3)-irp(2))/irp(2))))
      endif
      if(amp(1) .ne. 0.0_ki) then                                           ! NLO/LO
         kfac = abs(amp(2)/amp(1))
      else
         kfac = 0.0_ki
      endif
      icheck=1                                                              ! ACCEPT
      if(spprec1.lt.PSP_chk_th1.and.spprec1.ge.PSP_chk_th2 &
           .or.(kfac.gt.PSP_chk_kfactor.and.PSP_chk_kfactor.gt.0)) then
         icheck=2                                                           ! ROTATION
      endif
      if(spprec1.lt.PSP_chk_th2) then                                       ! RESCUE
         icheck=3
         fpprec1=-10        ! Set -10 as finite part precision
      endif[%
@end @if anymember LoopInduced PSP_chk_method ignore_case=true %]
      prec = min(prec,spprec1,fpprec1)
      ! if(icheck.eq.1) write(*,*) 'passed pole_check', amp(2), amp(3), irp(2), kfac, spprec1, fpprec1, prec 
      ! if(icheck.eq.2) write(*,*) 'failed pole_check (=> rotation)', amp(2), amp(3), irp(2), kfac, spprec1, fpprec1, prec 
      ! if(icheck.eq.3) write(*,*) 'failed pole_check (=> rescue)', amp(2), amp(3), irp(2), kfac, spprec1, fpprec1, prec 
   end subroutine pole_check
   !---#] subroutine pole_check

   !---#[ subroutine rotation_check
   subroutine     rotation_check(vecs, scale2, amp, amprot, prec, icheck, ok, h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), dimension([%num_legs%], 4) :: vecsrot
      real(ki), intent(in) :: scale2
      real(ki), dimension(1:4), intent(in) :: amp
      real(ki), dimension(1:4), intent(out) :: amprot
      real(ki) :: rat2, angle
      integer, intent(inout) :: prec
      integer, intent(inout) :: icheck
      logical, intent(inout), optional :: ok
      integer, intent(in), optional :: h
      integer fpprec1
      integer irot
      amprot=0.0_ki
      angle = 1.234_ki
      fpprec1 = 18
      ! write(*,*) '--double/double rot test---' 
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
      icheck=1                                                       ! ACCEPTED
      if(fpprec1.lt.PSP_chk_th3) icheck=2                            ! RESCUE[%
      @else %]
      icheck=1                                                       ! ACCEPTED
      if(fpprec1.lt.PSP_chk_li3) icheck=2                            ! RESCUE[%
      @end @if %]
      prec = fpprec1
      ! if(icheck.eq.1) write(*,*) 'passed double vs double_rot', amp(2), amprot(2), fpprec1, prec 
      ! if(icheck.eq.2) write(*,*) 'failed double vs double_rot', amp(2), amprot(2), fpprec1, prec 
   end subroutine rotation_check
   !---#] subroutine rotation_check[%
   @if extension quadruple %]

   !---#[ subroutine rescue_qp
   subroutine     rescue_qp(vecs, scale2, amp, ampdef, amprot, ampres, ampresrot, prec, icheck, ok, h)
      use [% process_name asprefix=\_ %]kinematics_qp, only: adjust_kinematics_qp => adjust_kinematics
      use [% @if internal OLP_MODE %][% @else %][% process_name asprefix=\_ %][% @end @if %]model
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki_qp), dimension([%num_legs%], 4) :: vecs_qp
      real(ki), dimension([%num_legs%], 4) :: vecsrot
      real(ki), intent(in) :: scale2
      real(ki), dimension(1:4), intent(inout) :: amp
      real(ki), dimension(1:4), intent(out) :: ampdef
      real(ki), dimension(1:4), intent(inout) :: amprot
      real(ki), dimension(1:4), intent(out) :: ampres
      real(ki), dimension(1:4), intent(out) :: ampresrot
      real(ki_qp), dimension(1:4) :: amp_qp, amprot_qp
      real(ki_qp) :: scale2_qp, rat2_qp
      real(ki) :: rat2, angle
      integer, intent(inout) :: prec
      integer, intent(inout) :: icheck
      logical, intent(inout), optional :: ok
      integer, intent(in), optional :: h
      integer spprec1, fpprec1, spprec2, fpprec2
      integer tmp_red_int, irot
      ampdef=amp ! store amp, will be updated by rescue system
      ampres=0.0_ki
      ampresrot=0.0_ki
      angle = 1.234_ki
      fpprec1 = 18
      fpprec2 = 18

      !****************************************
      !   Step 1 - check double vs double_rot
      !****************************************
      if(icheck.eq.3) then
         ! sets amprot, prec, icheck
         call rotation_check(vecs, scale2, amp, amprot, prec, icheck, ok, h)
      endif
      if(icheck.eq.2) icheck=3 ! double/double_rot has failed

      tmp_red_int = reduction_interoperation
      reduction_interoperation = reduction_interoperation_rescue

      !******************************************************************
      !   Step 2 - double/double_rot do not agree to PSP_chk_th/li3 digits
      !            compute quad
      !******************************************************************
      if(icheck.eq.3) then
         ! write(*,*) '--double does not agree with double_rot, computing quad--', amp(2), amprot(2) 
         scale2_qp = real(scale2,ki_qp)
         vecs_qp = vecs
         call adjust_kinematics_qp(vecs_qp)
         call samplitudel01_qp(vecs_qp, scale2_qp, amp_qp, rat2_qp, ok, h)
         ampres = real(amp_qp,ki)
         amp=ampres ! update amplitude

         !******************************************************************
         !   Step 2a - check double vs quad, double_rot vs quad
         !******************************************************************
         if((ampdef(2)-amp(2)) .ne. 0.0_ki) then
            fpprec1 = -int(log10(abs((ampdef(2)-amp(2))/((ampdef(2)+amp(2))/2.0_ki))))
         endif
         if((amprot(2)-amp(2)) .ne. 0.0_ki) then
            fpprec2 = -int(log10(abs((amprot(2)-amp(2))/((amprot(2)+amp(2))/2.0_ki))))
         endif[%
         @if anymember PoleRotation PSP_chk_method ignore_case=true %]
         icheck=1                                                       ! ACCEPTED
         if(fpprec1.lt.PSP_chk_th4) icheck=3                            ! RESCUE
         if(fpprec2.lt.PSP_chk_th4) icheck=3                            ! RESCUE[%
         @else %]
         icheck=1                                                       ! ACCEPTED
         if(fpprec1.lt.PSP_chk_li4) icheck=3                            ! RESCUE
         if(fpprec2.lt.PSP_chk_li4) icheck=3                            ! RESCUE[%
         @end @if %]
         prec = min(fpprec1,fpprec2)
         ! if(icheck.eq.1) write(*,*) 'passed double/double_rot vs quad', amp(2), amprot(2), amp_qp(2), fpprec1, fpprec2, prec 
         ! if(icheck.eq.3) write(*,*) 'failed double/double_rot vs quad', amp(2), amprot(2), amp_qp(2), fpprec1, fpprec2, prec
      endif

      !******************************************************************
      !   Step 3 - double/double_rot do not agree with quad to
      !            PSP_chk_li4 digits compute quad_rot
      !******************************************************************
      if(icheck.eq.3) then
         scale2_qp = real(scale2,ki_qp)
         do irot = 1,[%num_legs%]
            vecsrot(irot,1) = vecs(irot,1)
            vecsrot(irot,2) = vecs(irot,2)*Cos(angle)-vecs(irot,3)*Sin(angle)
            vecsrot(irot,3) = vecs(irot,2)*Sin(angle)+vecs(irot,3)*Cos(angle)
            vecsrot(irot,4) = vecs(irot,4)
         enddo
         vecs_qp = vecsrot
         call adjust_kinematics_qp(vecs_qp)
         call samplitudel01_qp(vecs_qp, scale2_qp, amprot_qp, rat2_qp, ok, h)
         ampresrot = real(amprot_qp,ki)
         if((ampresrot(2)-amp(2)) .ne. 0.0_ki) then
            fpprec1 = -int(log10(abs((ampresrot(2)-amp(2))/((ampresrot(2)+amp(2))/2.0_ki))))
         else
            fpprec1 = 16
         endif[%
         @if anymember PoleRotation PSP_chk_method ignore_case=true %]
         icheck=1                                                       ! ACCEPTED
         if(fpprec1.lt.PSP_chk_th5) icheck=3                            ! RESCUE[%
         @else %]
         icheck=1                                                       ! ACCEPTED
         if(fpprec1.lt.PSP_chk_li5) icheck=3                            ! RESCUE[%
         @end @if %]
         prec = fpprec1
         ! if(icheck.eq.1) write(*,*) 'passed quad vs quad_rot', amp(2), amprot(2), amp_qp(2), amprot_qp(2), prec 
         ! if(icheck.eq.3) write(*,*) 'failed quad vs quad_rot', amp(2), amprot(2), amp_qp(2), amprot_qp(2), prec 
      endif

      reduction_interoperation = tmp_red_int
   end subroutine rescue_qp
   !---#] subroutine rescue_qp[%
   @else %]

   !---#[ subroutine rescue
   subroutine     rescue(vecs, scale2, amp, ampdef, amprot, ampres, ampresrot, prec, icheck, ok, h)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(1:4), intent(inout) :: amp
      real(ki), dimension(1:4), intent(out) :: ampdef
      real(ki), dimension(1:4), intent(in) :: amprot
      real(ki), dimension(1:4), intent(out) :: ampres
      real(ki), dimension(1:4), intent(out) :: ampresrot
      real(ki) :: rat2, kfac, zero, angle
      real(ki), dimension(2:3) :: irp
      integer, intent(inout) :: prec
      integer, intent(inout) :: icheck
      logical, intent(inout), optional :: ok
      integer, intent(in), optional :: h
      integer spprec1, fpprec1, spprec2, fpprec2
      integer tmp_red_int, i, irot
      ! COMPUTE AMPLITUDE WITH reduction_interoperation_rescue
      ! write(*,*) '--double does not agree with double_rot, computing with reduction_interoperation_rescue--', amp(2), amprot(2), reduction_interoperation, reduction_interoperation_rescue 
      tmp_red_int = reduction_interoperation
      reduction_interoperation = reduction_interoperation_rescue
      ampdef=amp ! store amp, will be updated by rescue system
      ampres=0.0_ki
      ampresrot=0.0_ki
      call samplitudel01(vecs, scale2, ampres, rat2, ok, h)
      amp=ampres
      ! sets prec, icheck
      call pole_check(vecs, scale2, amp, irp, prec, icheck, ok, h)
      if(icheck.eq.2) then
         ! sets ampresrot, prec, icheck
         call rotation_check(vecs, scale2, amp, ampresrot, prec, icheck, ok, h)
      endif
      ! if(icheck.eq.1) write(*,*) 'passed rescue', amp(2), amprot(2), ampres(2), ampresrot(2), prec 
      ! if(icheck.eq.2) write(*,*) 'failed rescue rotation_check', amp(2), amprot(2), ampres(2), ampresrot(2), prec 
      ! if(icheck.eq.3) write(*,*) 'failed rescue pole_check', amp(2), amprot(2), ampres(2), ampresrot(2), prec 
      reduction_interoperation = tmp_red_int
   end subroutine rescue
   !---#] subroutine rescue[%
   @end @if extension quadruple %]

end module [% process_name asprefix=\_ %]rescue_system