[%' vim: sw=3:syntax=golem
   Template file for <process_dir>/kinematics.f90

   This template should be processed by
   golem.templates.Kinematics.KinematicsTemplate
'%]module     [% process_name asprefix=\_ %]kinematics
   use [% process_name asprefix=\_%]config, only: ki
   use [% process_name asprefix=\_ %]model
   use [% process_name asprefix=\_ %]scalar_cache
   implicit none
   save

   private

   complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)
   real(ki), parameter :: sqrthalf = &
   & 0.7071067811865475244008443621048490392848359376884740365883398689_ki

   integer, parameter, public :: num_legs = [% num_legs %]
   integer, parameter, public :: num_light_quarks = [%
      count particles fundamental spinor lightlike %]
   integer, parameter, public :: num_heavy_quarks = [%
      count particles fundamental spinor  massive %]
   integer, parameter, public :: num_quarks = [%
      count particles fundamental spinor %]
   integer, parameter, public :: num_gluons = [%
      count particles adjoint vector lightlike %]
   integer, parameter, public :: lo_qcd_couplings = [% loqcd %]
   logical, parameter, public :: corrections_are_qcd = [%
      @if isqcd %].true.[% @else %].false.[% @end @if %]
   integer, parameter, public :: in_helicities = [% in_helicities %]
   integer, parameter, public :: symmetry_factor = [% symmetry_factor %]
   [% @for mandelstam zero sym_prefix=es
   %]real(ki), parameter, public :: [%symbol%] = 0.0_ki
   [% @end @for mandelstam %]
   [% @for mandelstam non-zero sym_prefix=es
   %]real(ki), public :: [%symbol%]
   [% @end @for mandelstam %][%
@for pairs ordered distinct %]
   complex(ki), public :: spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %], spb[% 
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][%
@end @for %][% 
@for pairs distinct %]
   complex(ki), dimension(4), public :: spva[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %][% @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %][% 
@end @for %][%
@for particles %]
   real(ki), dimension(4), public :: k[%index%][%
@end @for particles %][%
@for particles massive %]
   real(ki), dimension(4), public :: l[%index%][%
@end @for particles %][%
@if internal NUMPOLVEC %]

   ! Polarisation vectors and related symbols[%
   @for particles lightlike vector %]
   complex(ki), dimension(4), public :: e[%index%][%
   @end @for %][%
   @for pairs ordered %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   complex(ki), public :: spa[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2
            %], spbe[% index2
            %][% @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%
      @end @if %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %]
   complex(ki), public :: spae[% index1 %][%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2
            %], spb[%
                 @if is_lightlike2 %]k[% @else %]l[% @end @if %][% index2 %]e[%
                    index1 %][%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   complex(ki), public :: spae[% index1
            %]e[% index2 %], spbe[% index2 %]e[% index1 %][%
      @end @if %][%
   @end @for %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   complex(ki), dimension(4), public :: spva[%
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1
            %]e[% index2 %], spvae[% index2 %][% 
                 @if is_lightlike1 %]k[% @else %]l[% @end @if %][% index1 %][%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
   complex(ki), dimension(4), public :: spvae[% index1
            %]e[% index2 %], spvae[% index2 %]e[% index1 %][%
      @end @if %][%
   @end @for %][%
@end @if%]

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

   public :: Spaa, Spbb, Spab3, Spba3, dotproduct
   public :: inspect_kinematics, init_event
   public :: adjust_kinematics
   public :: lambda
   public :: epsi, epso

contains
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
      [% @for particles initial %]
      write(ch,*) "<momentum index='[% index %]' inout='in'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k[% index %](1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k[% index %](2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k[% index %](3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k[% index %](4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real([% mass %], ki), "'/>"
      write(ch,*) "<!-- k[%index%].k[%index%] = ", &
         & dotproduct(k[%index%],k[%index%]), "-->"
      write(ch,*) "</momentum>"[%
      @end @for particles %][%
      @for particles final %]
      write(ch,*) "<momentum index='[% index %]' inout='out'>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='E' value='", k[% index %](1), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='x' value='", k[% index %](2), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='y' value='", k[% index %](3), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='z' value='", k[% index %](4), "'/>"
      write(ch,'(A27,G24.16,A3)') &
         & "<component name='m' value='", real([% mass %], ki), "'/>"
      write(ch,*) "<!-- k[%index%].k[%index%] = ", &
         & dotproduct(k[%index%],k[%index%]), "-->"
      write(ch,*) "</momentum>"[%
      @end @for particles %][%
      @for mandelstam non-zero sym_prefix=es %]
      write(ch,*) "<!-- [%symbol%] = ", [%symbol%], "-->"[%
      @end @for mandelstam %]
   end subroutine inspect_kinematics
!---#] subroutine inspect_kinematics:
!---#[ subroutine init_event:
   subroutine     init_event(vecs[%
@for particles lightlike vector %], hel[%index%][%
@end @for %])[%
@if internal NUMPOLVEC %]
      use [% process_name asprefix=\_ %]config, only: debug_numpolvec, [% '
      %]logfile[%
@end @if %]
      use [% process_name asprefix=\_ %]model
      implicit none
      real(ki), dimension(num_legs,4), intent(in) :: vecs[%
@for particles lightlike vector %]
      integer, intent(in), optional :: hel[%index%][%
@end @for %][%
@for particles lightlike vector %]
      complex(ki) :: N[%index%]
      logical :: flag[%index%][%
@end @for %]
      
      call invalidate_cache()[%
@for particles %]
      k[%index%] = vecs([%index%],:)[%
@end @for particles %][%
@for instructions %][%
   @select opcode
   @case 1 %]
      ! mass1 = '[% mass1 %]', mass2 = '[% mass2 %]'
      call light_cone_decomposition(k[% index1%], l[%index1%], [%
      @select mass2 
      @case 0%]k[%index2%][%
      @else %]l[%index2%][%
      @end @select mass2 %], [%mass1%])[%
   @case 2 %]
      call light_cone_splitting_iter(k[% index1%], k[%index2%], l[%
                index1%], l[%index2%], [%mass1%], [%mass2%])[%
   @end @select opcode %][%
@end @for instructions %][%
@for mandelstam non-zero sym_prefix=es %]
      [%symbol%] = [%
   @for mandelstam_expression %][%
      @if is_first_term %][%
      @else %]&
            & + [%
      @end @if %][% 
      @if term_is_mass %][% term_mass %]**2[%
      @else %][%
         @select term_coeff
         @case 2 %]2.0_ki*[%
         @end @select %]dotproduct([%
         @if is_final1 %]-[% @end @if %]vecs([%index1%],:), [%
         @if is_final2 %]-[% @end @if %]vecs([%index2%],:))[%
      @end @if %][%
   @end @for mandelstam_expression %][%
@end @for mandelstam %][%
@for pairs ordered distinct %]
      spa[%
   @if is_lightlike1 %]k[%
   @else %]l[%
   @end @if %][% index1 %][%
   @if is_lightlike2 %]k[%
   @else %]l[%
   @end @if %][% index2 %] = Spaa([%
   @if is_lightlike1%]k[%index1%][%
   @else %]l[%index1%][%
   @end @if %], [%
   @if is_lightlike2%]k[%index2%][%
   @else %]l[%index2%][%
   @end @if %])
      spb[% 
   @if is_lightlike2 %]k[%
   @else %]l[%
   @end @if %][% index2
         %][%
   @if is_lightlike1 %]k[%
   @else %]l[%
   @end @if %][% index1 %] = Spbb([%
   @if is_lightlike2%]k[%index2%][%
   @else %]l[%index2%][%
   @end @if %], [%
   @if is_lightlike1%]k[%index1%][%
   @else %]l[%index1%][%
   @end @if %])[%
@end @for %][%
@for pairs distinct %]
      spva[%
    @if is_lightlike1 %]k[%
    @else %]l[%
    @end @if %][% index1 %][%
    @if is_lightlike2 %]k[%
    @else %]l[%
    @end @if %][% index2 %] = Spab3_vec([%
    @if is_lightlike1%]k[%index1%][%
    @else %]l[%index1%][%
    @end @if %], [%
    @if is_lightlike2%]k[%index2%][%
    @else %]l[%index2%][%
    @end @if %])[%
@end @for %][%
@if internal NUMPOLVEC %]
      if(.true.[%
   @for particles lightlike vector %] .and. present(hel[%index%])[%
   @end @for %]) then[%   
   @for particles lightlike vector initial %][%
      @with eval 'k .rep. ( reference > 0 ) . 'l .rep. ( reference < 0 )
          . reference result=refvec %]
         select case(hel[%index%])
         case(1)
            flag[%index%] = .false.
            N[%index%] = sqrt2*Spaa([%refvec%],k[%index%])
            e[% index %] = spva[%refvec%]k[%index%]/N[%index%]
         case(-1)
            flag[%index%] = .true.
            N[%index%] = sqrt2*Spbb(k[%index%],[%refvec%])
            e[% index %] = spvak[%index%][%refvec%]/N[%index%]
         case default
            print*, "Illegal helicity for particle [%
               index %]:", hel[% index %]
            stop
         end select
         N[%index%] = sqrt(2.0_ki/N[%index%])[%
      @end @with %][%
   @end @for %][%
   @for particles lightlike vector final %][%
      @with eval 'k .rep. ( reference > 0 ) . 'l .rep. ( reference < 0 )
          . reference result=refvec %]
         select case(hel[%index%])
         case(1)
            flag[%index%] = .true.
            N[%index%] = sqrt2*Spbb(k[%index%],[%refvec%])
            e[% index %] = spvak[%index%][%
               refvec%]/N[%index%]
         case(-1)
            flag[%index%] = .false.
            N[%index%] = sqrt2*Spaa([%refvec%],k[%index%])
            e[% index %] = spva[%refvec%]k[%
               index%]/N[%index%]
         case default
            print*, "Illegal helicity for particle [%
               index %]:", hel[% index %]
            stop
         end select
         N[%index%] = sqrt(2.0_ki/N[%index%])[%
      @end @with %][%
   @end @for %][%
   @for pairs ordered %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %][%
         @with eval 'k .rep. ( reference2 > 0 ) . 'l .rep. ( reference2 < 0 )
          . reference2 result=refvec2 %][%
            @with eval 'k .rep. ( is_lightlike1 ~> 'rue )
             . 'l .rep. ( is_lightlike1 ~> 'lse )
             . index1 result=vec1 %]
         if(flag[%index2%]) then
            spa[% vec1 %]e[%index2%] = [%
                    @if eval ( 'k . index2 ) .eq. vec1 %]0.0_ki[%
                    @else %]N[%index2%] * Spaa([%vec1%], k[%index2%])[%
                    @end @if %]
            spbe[%index2%][%vec1%] = [%
                    @if eval refvec2 .eq. vec1 %]0.0_ki[%
                    @else %]N[%index2%] * Spbb([%refvec2%], [%vec1%])[%
                    @end @if %]
         else
            spa[% vec1 %]e[%index2%] = [%
                    @if eval refvec2 .eq. vec1 %]0.0_ki[%
                    @else %]N[%index2%] * Spaa([%vec1%], [%refvec2%])[%
                    @end @if %]
            spbe[%index2%][%vec1%] = [%
                    @if eval ( 'k . index2 ) .eq. vec1 %]0.0_ki[%
                    @else %]N[%index2%] * Spbb(k[%index2%], [%vec1%])[%
                    @end @if %]
         end if[%
            @end @with %][%
         @end @with %][%
      @end @if %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) %][%
         @with eval 'k .rep. ( reference1 > 0 ) . 'l .rep. ( reference1 < 0 )
          . reference1 result=refvec1 %][%
            @with eval 'k .rep. ( is_lightlike2 ~> 'rue )
             . 'l .rep. ( is_lightlike2 ~> 'lse )
             . index2 result=vec2 %]
         if(flag[%index1%]) then
            spae[%index1%][% vec2 %] = [%
                    @if eval ( 'k . index1 ) .eq. vec2 %]0.0_ki[%
                    @else %]N[%index1%] * Spaa(k[%index1%], [%vec2%])[%
                    @end @if %]
            spb[%vec2%]e[%index1%] = [%
                    @if eval refvec1 .eq. vec2 %]0.0_ki[%
                    @else %]N[%index1%] * Spbb([%vec2%], [%refvec1%])[%
                    @end @if %]
         else
            spae[% index1 %][%vec2%] = [%
                    @if eval refvec1 .eq. vec2 %]0.0_ki[%
                    @else %]N[%index1%] * Spaa([%refvec1%], [%vec2%])[%
                    @end @if %]
            spb[%vec2%]e[%index1%] = [%
                    @if eval ( 'k . index1 ) .eq. vec2 %]0.0_ki[%
                    @else %]N[%index1%] * Spbb([%vec2%], k[%index1%])[%
                    @end @if %]
         end if[%
            @end @with %][%
         @end @with %][%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %][%
         @with eval 'k .rep. ( reference1 > 0 ) . 'l .rep. ( reference1 < 0 )
          . reference1 result=refvec1 %][%
            @with eval 'k .rep. ( reference2 > 0 ) . 'l .rep. ( reference2 < 0 )
          . reference2 result=refvec2 %]
         if (flag[%index1%]) then
            if (flag[%index2%]) then
               spae[% index1 %]e[% index2 %] = N[%index1%] * N[%index2
                  %] * Spaa(k[%index1%], k[%index2%])
               spbe[% index2 %]e[% index1 %] = [%
            @if eval refvec1 .eq. refvec2 %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spbb([%refvec2%], [%refvec1%])[%
            @end @if %]
            else
               spae[% index1 %]e[% index2 %] = [%
            @if eval refvec2 .eq. ( 'k . index1 ) %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spaa(k[%index1%], [%refvec2%])[%
            @end @if %]
               spbe[% index2 %]e[% index1 %] = [%
            @if eval refvec1 .eq. ( 'k . index2 ) %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spbb(k[%index2%], [%refvec1%])[%
            @end @if %]
            endif
         else
            if (flag[%index2%]) then
               spae[% index1 %]e[% index2 %] = [%
            @if eval ( 'k . index2 ) .eq. refvec1 %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spaa([%refvec1%], k[%index2%])[%
            @end @if %]
               spbe[% index2 %]e[% index1 %] = [%
            @if eval refvec2 .eq. ( 'k . index1 ) %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spbb([%refvec2%], k[%index1%])[%
            @end @if %]
            else
               spae[% index1 %]e[% index2 %] = [%
            @if eval refvec2 .eq. refvec1 %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spaa([%refvec1%], [%refvec2%])[%
            @end @if %]
               spbe[% index2 %]e[% index1 %] = [%
            @if eval index1 .eq. index2 %]0.0_ki[%
            @else %]N[%index1%] * N[%index2%] * Spbb(k[%index2%], k[%index1%])[%
            @end @if %]
            endif
         end if[%
            @end @with %][%
         @end @with %][%
      @end @if %][%
   @end @for %][%
   @for pairs %][%
      @if eval is_lightlike2 .and. ( 2spin2 .eq. 2 ) %][%
         @with eval 'k .rep. ( reference2 > 0 ) . 'l .rep. ( reference2 < 0 )
          . reference2 result=refvec2 %][%
            @with eval 'k .rep. ( is_lightlike1 ~> 'rue )
             . 'l .rep. ( is_lightlike1 ~> 'lse )
             . index1 result=vec1 %]
         if (flag[%index2%]) then
            spva[% vec1 %]e[% index2 %] = N[%index2%] * [%
               @if eval vec1 .eq. refvec2 %]2.0_ki * [% vec1 %][%
               @else %]Spab3_vec([%vec1%], [%refvec2%])[%
               @end @if %]
            spvae[% index2 %][% vec1 %] = N[%index2%] * [%
               @if eval vec1 .eq. ( 'k . index2 ) %]2.0_ki * [% vec1 %][%
               @else %]Spab3_vec(k[%index2%], [%vec1%])[%
               @end @if %]
         else
            spva[% vec1 %]e[% index2 %] = N[%index2%] * [%
               @if eval vec1 .eq. ( 'k . index2 ) %]2.0_ki * [% vec1 %][%
               @else %]Spab3_vec([%vec1%], k[%index2%])[%
               @end @if %]
            spvae[% index2 %][% vec1 %] = N[%index2%] * [%
               @if eval vec1 .eq. refvec2 %]2.0_ki * [% vec1 %][%
               @else %]Spab3_vec([%refvec2%], [%vec1%])[%
               @end @if %]
         end if[%
            @end @with %][%
         @end @with %][%
      @end @if %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %][%
         @with eval 'k .rep. ( reference1 > 0 ) . 'l .rep. ( reference1 < 0 )
          . reference1 result=refvec1 %][%
            @with eval 'k .rep. ( reference2 > 0 ) . 'l .rep. ( reference2 < 0 )
          . reference2 result=refvec2 %]
         if (flag[%index1%]) then
            if (flag[%index2%]) then[% '
               ! T T => <k1 r2] %]
               spvae[% index1 %]e[% index2 %] = N[%index1%] * N[%index2%] * [%
               @if eval refvec2 .eq. ( 'k . index1 ) %]2.0_ki * [%refvec2%][%
               @else %]Spab3_vec(k[%index1%], [%refvec1%])[%
               @end @if %][% '
               ! T T => <k2 r1] %]
               spvae[% index2 %]e[% index1 %] = N[%index1%] * N[%index2%] * [%
               @if eval ( 'k . index2 ) .eq. refvec1 %]2.0_ki * [%refvec1%][%
               @else %]Spab3_vec(k[%index2%], [%refvec1%])[%
               @end @if %]
            else[% '
               ! T F => <k1 k2] %]
               spvae[% index1 %]e[% index2 %] = N[%index1%] * N[%index2%] * [% 
               @if eval index1 .eq. index2 %]2.0_ki * k[%index1%][%
               @else %]Spab3_vec(k[%index1%], k[%index2%])[%
               @end @if %][% '
               ! T F => <r2 r1] %]
               spvae[% index2 %]e[% index1 %] = N[%index1%] * N[%index2%] * [%
               @if eval refvec1 .eq. refvec2 %]2.0_ki * [%refvec1%][%
               @else %]Spab3_vec([%refvec2%], [%refvec1%])[%
               @end @if %]
            end if
         else
            if (flag[%index2%]) then[% '
               ! F T => <r1 r2] %]
               spvae[% index1 %]e[% index2 %] = N[%index1%] * N[%index2%] * [%
               @if eval refvec1 .eq. refvec2 %]2.0_ki * [%refvec1%][%
               @else %]Spab3_vec([%refvec1%], [%refvec2%])[%
               @end @if %][% '
               ! F T => <k2 k1] %]
               spvae[% index2 %]e[% index1 %] = N[%index1%] * N[%index2%] * [% '
                %]Spab3_vec(k[%index2%], k[%index1%])
            else[% '
               ! F F => <r1 k2] %]
               spvae[% index1 %]e[% index2 %] = N[%index1%] * N[%index2 %] * [%
               @if eval ( 'k . index2 ) .eq. refvec1 %]2.0_ki * [%refvec1%][%
               @else %]Spab3_vec([%refvec1%], k[%index2%])[%
               @end @if %][% '
               ! F F => <r2 k1] %]
               spvae[% index2 %]e[% index1 %] = N[%index1%] * N[%index2%] * [%
               @if eval ( 'k . index1 ) .eq. refvec2 %]2.0_ki * [%refvec2%][%
               @else %]Spab3_vec([%refvec2%], k[%index1%])[%
               @end @if %]
            end if
         end if[%
            @end @with %][%
         @end @with %][%
      @end @if %][%
   @end @for %]
         if (debug_numpolvec) then
            write(logfile, "(A17)") "<!-- NUMPOLVEC --"[%
   @for particles lightlike vector %]
            write(logfile, "(A9,I2,A4,I2,A9,L1)") &
            & "Helicity(", [%index%], ") = ", hel[%
            index%], "; flag = ", flag[%index%][%
   @end @for %][%
   @for particles lightlike vector %]
            write(logfile, *) "k[%index%].e[%index%]", dotproduct(k[%
              index%], e[%index%])
            write(logfile, *) "r[%index%].e[%index%]", dotproduct([%
      @if eval reference .lt. 0 %]l[%
      @else %]k[%
      @end @if %][% eval .abs. reference %], e[%index%])[%
   @end @for %][%
   @for pairs distinct %][%
      @for particles lightlike vector %]
            write(logfile, *) "<[%index1%]|e[%index%]|[%index2%]]", &
              & dotproduct(spva[%
         @if is_lightlike1 %]k[%
         @else %]l[%
         @end @if %][%index1%][%
         @if is_lightlike2 %]k[%
         @else %]l[%
         @end @if %][%index2%], e[%index%]), spa[%
         @if eval index .gt. index1 %][%
            @if is_lightlike1 %]k[%
            @else %]l[%
            @end @if %][%index1%]e[%index%][%
         @else %]e[%index%][%
            @if is_lightlike1 %]k[%
            @else %]l[%
            @end @if %][%index1%]*(-1.0_ki)[%
         @end @if %]*spb[%
         @if eval index .lt. index2 %][%
            @if is_lightlike2 %]k[%
            @else %]l[%
            @end @if %][%index2%]e[%index%]*(-1.0_ki)[%
         @else %]e[%index%][%
            @if is_lightlike2 %]k[%
            @else %]l[%
            @end @if %][%index2%][%
         @end @if %][%
      @end @for %][%
   @end @for %][%
   @for pairs distinct ordered %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %]
            write(logfile, *) "e[%index1%].e[%index2%]", &
            & dotproduct(e[%index1%], e[%index2%]), &
            & 0.5_ki * spae[%index1%]e[%index2%] * spbe[%index2%]e[%index1%][%
      @end @if %][%
   @end @for %][%
   @for pairs distinct lightlike1 lightlike2 %][%
      @for particles lightlike vector %]
            write(logfile, *) "<k[%index1%]|mu|e[%index%]]<e[%
                 index%]|mu|k[%index2%]]", &
            & dotproduct(spvak[%index1%]e[%index%], spvae[%index
                      %]k[%index2%]), &
            & -2.0_ki * dotproduct(spvak[%index1%]k[%index2%], e[%index%])[%
      @end @for %][%
   @end @for %][%
   @for pairs distinct index1=ie1 index2=ie2 %][%
      @if eval is_lightlike1 .and. ( 2spin1 .eq. 2 ) .and.
               is_lightlike2 .and. ( 2spin2 .eq. 2 ) %][%
         @for pairs index1=ik1 index2=ik2 %][%
            @with eval 'k .rep. ( is_lightlike1 ~> 'rue )
             . 'l .rep. ( is_lightlike1 ~> 'lse )
             . ik1 result=k1 %][%
            @with eval 'k .rep. ( is_lightlike2 ~> 'rue )
             . 'l .rep. ( is_lightlike2 ~> 'lse )
             . ik2 result=k2 %][%
            @for particles lightlike %]
            write(logfile, *) "[[%ik1%]|e[%ie1%]]<e[%ie1%]|[%
                  index%]|e[%ie2%]]<e[%ie2%]|[%ik2%]>", &
            & [%
               @if eval ik1 .gt. ie1 %]spb[%k1%]e[%ie1%][%
               @else               %](-spbe[%ie1%][%k1%])[%
               @end @if %]*dotproduct(spvae[%ie1%]e[%ie2%], k[%index%])*[%
               @if eval ie2 .lt. ik2 %]spae[%ie2%][%k2%][%
               @else               %](-spa[%k2%]e[%ie2%])[%
               @end @if %], [%
               @if eval index .eq. ik1 %]2.0_ki*dotproduct(k[%index%][%
               @else %]dotproduct(spvak[%index%][%k1%][%
               @end @if %], e[%ie1%])*[%
               @if eval index .eq. ik2 %]2.0_ki*dotproduct(k[%index%][%
               @else %]dotproduct(spva[%k2%]k[%index%][%
               @end @if %], e[%ie2%])[%
            @end @for %][%
            @end @with %][%
            @end @with %][%
         @end @for %][%
      @end @if %][%
   @end @for %]
            write(logfile, "(A18)") "  -- NUMPOLVEC -->"
         end if
      end if[%
@end @if%]
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
      real(ki), dimension([%num_legs%],4), intent(inout) :: vecs
   
      real(ki) :: p02, p12, Sz, SE, s0, s1
      real(ki) :: z0, z1, z0a, z0b, E0, E1, E0a, E0b
      real(ki) :: a, b, c, d, x, y
      integer :: i

      ! Put particles onshell.[%
@for particles %][%
   @if eval index .lt. ( num_legs - 1 ) %]
      vecs([%index%],1) = sqrt(vecs([%index%],2)**2 + vecs([%index
        %],3)**2 + vecs([%index%],4)**2[% @if is_massive
        %] + [%mass%]**2[% @end @if %])[%
   @else %][%
      @if eval index .eq. ( num_legs - 1 ) %]
      s0[%
      @else %]
      s1[%
      @end @if%] = [%
      @if is_massive %][%mass%]**2[%
      @else %]0.0_ki[%
      @end @if %][%
   @end @if %][%
@end @for %]
      ! Momentum conservation in x- and y- direction
      vecs([%num_legs%],2) = sum(vecs(1:[%num_in
          %],2)) - sum(vecs([%eval num_in + 1%]:[%eval num_legs - 1%],2))
      vecs([%num_legs%],3) = sum(vecs(1:[%num_in
          %],3)) - sum(vecs([%eval num_in + 1%]:[%eval num_legs - 1%],3))
   
      SE = sum(vecs([%eval num_in + 1%]:[%
         eval num_legs - 2%],1)) - sum(vecs(1:[%num_in%],1))
      Sz = sum(vecs([%eval num_in + 1%]:[%
         eval num_legs - 2%],4)) - sum(vecs(1:[%num_in%],4))
      p02 = vecs([%eval num_legs - 1%],2)**2 + vecs([%
         eval num_legs - 1%],3)**2 + s0
      p12 = vecs([%num_legs %],2)**2 + vecs([%num_legs%],3)**2 + s1

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

            if (abs(E0a - vecs([%eval num_legs - 1
            %],1)) + abs(z0a - vecs([%eval num_legs - 1
            %],4)) .lt. abs(E0b - vecs([%eval num_legs - 1
            %],1)) + abs(z0b - vecs([%eval num_legs - 1
            %],4))) then
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
      vecs([%eval num_legs - 1%],1) = E0
      vecs([%eval num_legs - 1%],4) = z0
      vecs([%num_legs%],1) = E1
      vecs([%num_legs%],4) = z1
   end subroutine adjust_kinematics
   !---#] subroutine adjust_kinematics :   
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
end module [% process_name asprefix=\_ %]kinematics
