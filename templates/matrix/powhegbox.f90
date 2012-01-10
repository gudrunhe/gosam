[% ' vim: syntax=golem
%]module [% process_name asprefix=\_ %]powheg
use [% process_name asprefix=\_ %]config, only: ki, dbl
use [% process_name asprefix=\_ %]matrix, only: initgolem, &
    & samplitude, color_correlated_lo2, spin_correlated_lo2
use [% process_name asprefix=\_ %]kinematics, only: num_legs
use [% process_name asprefix=\_ %]model, only: parse
implicit none
save


   logical, private :: golem_initialized = .false.

   private :: num_legs, ki, parse, dbl
   private :: initgolem, samplitude, color_correlated_lo2, &
            & spin_correlated_lo2

contains

subroutine init_event(scale2, momenta, &
   &    born, virt_finite, virt_single, virt_double, borncc, bornsc)
   implicit none
   double precision, dimension(num_legs,0:3), intent(in) :: momenta
   double precision, intent(in) :: scale2

   double precision, intent(out) :: born
   double precision, intent(out) :: virt_finite, virt_single, virt_double
   double precision, dimension(num_legs,num_legs), intent(out) :: borncc
   double precision, dimension(num_legs,4,4), intent(out) :: bornsc

   real(ki), dimension(0:3) :: amp
   real(ki), dimension(num_legs,num_legs) :: bcc_ki
   real(ki), dimension(num_legs,4,4) :: bsc_ki
   integer :: ierr
   logical :: ok

   if (.not. golem_initialized) then
      open(unit=10,status='old',action='read',file='param.dat',iostat=ierr)
      if(ierr .eq. 0) then
         call parse(10)
         close(unit=10)
      else
         print*, "No file 'param.dat' found. Using defaults"
      end if

      call initgolem()
      golem_initialized = .true.
   end if

   call samplitude(real(momenta,ki),real(scale2,ki),amp,ok)

   if (.not.ok) then
      born = -1.0d0
   else
      born        = real(amp(0), dbl)
      virt_finite = real(amp(1), dbl)
      virt_single = real(amp(2), dbl)
      virt_double = real(amp(3), dbl)

      call color_correlated_lo2(real(momenta,ki),bcc_ki)
      call spin_correlated_lo2(real(momenta,ki),bsc_ki)
      borncc(:,:) = real(bcc_ki(:,:), dbl)
      bornsc(:,:,:) = real(bsc_ki(:,:,:), dbl)
   end if
end subroutine init_event

end module [% process_name asprefix=\_ %]powheg
