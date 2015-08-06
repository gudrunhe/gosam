module [% name asprefix=\_ %]matrix
   use [% process_name asprefix=\_ %]config, only: ki
   implicit none
   private

   public :: initgolem, exitgolem, samplitude
   public :: samplitudel0, samplitudel1, ir_subtraction
   public :: OLP_spin_correlated_lo2, OLP_color_correlated
   ! TODO:
   ! public :: color_correlated_lo2, spin_correlated_lo2


contains

   pure function prefactor()
      use [% process_name asprefix=\_ %]config, only: &
      & include_color_avg_factor, include_helicity_avg_factor, &
      & include_symmetry_factor
      use [% process_name asprefix=\_ %]model, only: NC
      use [% process_name asprefix=\_ %]kinematics, only: &
      & in_helicities, symmetry_factor
      use [% process_name asprefix=\_ %]color, only: incolors
      implicit none
      real(ki) :: prefactor, NA

      prefactor = 1.0_ki
      NA = (NC + 1.0_ki) * (NC - 1.0_ki)

      if (include_color_avg_factor) then
         prefactor = prefactor * real(incolors, ki)[%
   @for crossed_color initial %][%
      @select $_
      @case -1 1 %][%
      @case -3 3 %]/NC[%
      @case -8 8 %]/NA[%
      @else %]/unknown_color_charge([% color %])[%
      @end @select %][%
   @end @for %]
      end if
      if (include_helicity_avg_factor) then
         prefactor = prefactor * real(in_helicities, ki)[%
   @for crossed_helicities initial %]/[% $_ %].0_ki[%
   @end @for %]
      end if
      if (include_symmetry_factor) then
         prefactor = prefactor * real(symmetry_factor, ki)/[%
          crossed_symmetry_factor %].0_ki
      end if
   end function prefactor

   subroutine     initgolem(is_first)
      use [% process_name asprefix=\_ 
        %]matrix, only: orig_initgolem => initgolem
      implicit none
      logical, optional, intent(in) :: is_first

      if (present(is_first)) then
         call orig_initgolem(is_first)
      else
         call orig_initgolem()
      endif
   end subroutine initgolem

   subroutine     exitgolem(is_last)
      use [% process_name asprefix=\_
         %]matrix, only: orig_exitgolem => exitgolem
      implicit none
      logical, optional, intent(in) :: is_last

      if (present(is_last)) then
         call orig_exitgolem(is_last)
      else
         call orig_exitgolem()
      endif
   end subroutine exitgolem

   subroutine     samplitude(vecs, scale2, amp, prec, ok, h)
      use [% process_name asprefix=\_ %]matrix, only: orig_sub => samplitude
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(4), intent(out) :: amp
      integer, intent(out) :: prec
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h

      real(ki), dimension([%num_legs%], 4) :: new_vecs

      call twist_momenta(vecs, new_vecs)

      if (present(ok)) then
         if (present(h)) then
            call orig_sub(new_vecs, scale2, amp, prec, ok, h)
         else
            call orig_sub(new_vecs, scale2, amp, prec, ok)
         end if
      else
         call orig_sub(new_vecs, scale2, amp, prec, ok)
      end if

      amp = amp * prefactor()
   end subroutine samplitude

   function     samplitudel0(vecs, h) result(amp)
      use [% process_name asprefix=\_ %]matrix, only: orig_func => samplitudel0
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      integer, optional, intent(in) :: h
      real(ki) :: amp
      real(ki), dimension([%num_legs%], 4) :: new_vecs
      
      call twist_momenta(vecs, new_vecs)

      if (present(h)) then
         amp = orig_func(new_vecs, h)
      else
         amp = orig_func(new_vecs)
      end if
      amp = amp * prefactor()
   end function samplitudel0

   function     samplitudel1(vecs,scale2,ok,rat2,h) result(amp)
      use [% process_name asprefix=\_ %]matrix, only: orig_func => samplitudel1
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki), intent(in) :: scale2
      real(ki), intent(out) :: rat2
      integer, optional, intent(in) :: h
      real(ki), dimension(-2:0) :: amp
      real(ki), dimension([%num_legs%], 4) :: new_vecs
      
      call twist_momenta(vecs, new_vecs)

      if (present(h)) then[%
         @if helsum %]
         print *, 'ERROR: Cannot select helicity when code was generated'
         print *, 'with "helsum=1".'[%
         @else %]
         amp = orig_func(new_vecs, scale2, ok, rat2, h)[%
         @end @if %]
      else
         amp = orig_func(new_vecs, scale2, ok, rat2)
      end if
      amp = amp * prefactor()
   end function samplitudel1

   subroutine     ir_subtraction(vecs,scale2,amp)
      use [% process_name asprefix=\_ %]matrix, &
      & only: orig_sub => ir_subtraction
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(2), intent(out) :: amp

      real(ki), dimension([%num_legs%], 4) :: new_vecs

      call twist_momenta(vecs, new_vecs)

      call orig_sub(new_vecs, scale2, amp)
      amp = amp * prefactor()
   end subroutine ir_subtraction

   subroutine OLP_color_correlated(vecs,ampcc)
      use [% process_name asprefix=\_ %]matrix, only: orig_func => OLP_color_correlated
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), dimension([%eval ( num_legs * ( num_legs - 1 ) ) // 2 %]), intent(out) :: ampcc

      real(ki), dimension([%num_legs%], 4) :: new_vecs

      call twist_momenta(vecs, new_vecs)

      call orig_func(new_vecs, ampcc)

      call twist_result_OLP_color_correlated(ampcc)
      
      ampcc(:)=ampcc(:)*prefactor()

   end subroutine OLP_color_correlated


   subroutine OLP_spin_correlated_lo2(vecs, ampsc)
      use [% process_name asprefix=\_ %]matrix, only: orig_func => OLP_spin_correlated_lo2
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), dimension([% eval 2 * num_legs * num_legs%]) :: ampsc

      real(ki), dimension([%num_legs%], 4) :: new_vecs

      call twist_momenta(vecs, new_vecs)

      call orig_func(new_vecs, ampsc)

      call twist_result_OLP_spin_correlated(ampsc)
      
      ampsc(:)=ampsc(:)*prefactor()

   end subroutine OLP_spin_correlated_lo2


   pure subroutine twist_momenta(vecs, new_vecs)
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), dimension([%num_legs%], 4), intent(out) :: new_vecs[%
@for crossing %]
      new_vecs([% $_ %],:) = [%sign%] vecs([% index %],:)[%
@end @for %]
   end  subroutine twist_momenta

   pure subroutine twist_result_OLP_spin_correlated(ampsc)
      implicit none
      real(ki), dimension([% eval 2 * num_legs * num_legs %]), intent(inout) :: ampsc
      real(ki), dimension([% eval 2 * num_legs * num_legs %]) :: temp
      temp = ampsc[%
      @for olp_spin_correlated_twist %]
      ampsc([% $_ %]) =  [% sign %] temp([% index %])[%
      @end @for %]
   end subroutine twist_result_OLP_spin_correlated

   pure subroutine twist_result_OLP_color_correlated(ampcc)
      implicit none
      real(ki), dimension([%eval ( num_legs * ( num_legs - 1 ) ) // 2 %]), intent(inout) :: ampcc
      real(ki), dimension([%eval ( num_legs * ( num_legs - 1 ) ) // 2 %]) :: temp
      temp = ampcc[%
      @for olp_color_correlated_twist %]
      ampcc([% $_ %]) = temp([% index %])[%
      @end @for %]
   end subroutine twist_result_OLP_color_correlated


end module [% name asprefix=\_ %]matrix
