[%' vim: syntax=golem
'%]module     [% process_name asprefix=\_ %]config
   implicit none

   integer, parameter :: dbl = kind(1.0d0)
   ! QUADRUPLE PRECISION (ki=16):
   ! integer, parameter :: ki = selected_real_kind(33, 4931)
   ! INTERMEDIATE PRECISION (ki=10):
   ! integer, parameter :: ki = selected_real_kind(18, 4931)
   ! DOUBLE PRECISION (ki=8):
   integer, parameter :: ki = kind(1.0d0)

   logical, parameter :: debug_lo_diagrams  = [%
      @if anymember lo all debug ignore_case=true %].true.[%
      @else %].false.[%
      @end @if %]
   logical, parameter :: debug_nlo_diagrams = [%
      @if anymember nlo all debug ignore_case=true %].true.[%
      @else %].false.[%
      @end @if %][%

      @if internal NUMPOLVEC %]
   logical, parameter :: debug_numpolvec    = [%
         @if anymember numpolvec all debug ignore_case=true %].true.[%
         @else %].false.[%
         @end @if %][%
      @end @if %]

   ! If true, the calculation includes terms proportional to eps^2
   ! multiplying double poles.
   ! These terms are supposed to cancel in QCD.
   logical :: include_eps2_terms = [%
      @if extension dred %].false.[% @else %].true.[% @end @if %]

   ! If true, the calculation includes terms proportional to eps
   ! multiplying double and single poles.
   ! These terms are necessary in 't Hooft-Veltman scheme
   logical :: include_eps_terms = [%
      @if extension dred %].false.[% @else %].true.[% @end @if %]

   logical, parameter :: include_color_avg_factor = .[%
        olp.include_color_average default=true %].
   logical, parameter :: include_helicity_avg_factor = .[%
        olp.include_helicity_average default=true %].
   logical, parameter :: include_symmetry_factor = .false.

   [% @if extension samurai %]
   ! Parameters for the initialization of samurai
   ! they can also be set using the subroutine parse in model.f90
   integer :: samurai_scalar = [% samurai_scalar %]
   integer :: samurai_verbosity = 0
   integer :: samurai_test = 3
   ! The following parameter sets the 'istop' argument in all samurai
   ! calls. Unless you really know what you do, you should stick to the
   ! default value.
   integer :: samurai_istop = 0
   logical :: samurai_group_numerators = .true.[%
      @end @if extension samurai %]

   ! Options to control the interoperation between different
   ! reduction methods
   integer :: reduction_interoperation = [%
   @select reduction_interoperation default="-1"
   @case -1 %][%
      @if extension samurai %][%
        @if extension golem95 %]2[%
        @else %]0[%
        @end @if %][%
      @else %]1[%
      @end @if %][%
   @else %][% reduction_interoperation %][%
   @end @select %]
   ! 0: use samurai only
   ! 1: golem95 only
   ! 2: try samurai first, use golem95 if samurai fails
   ! 3: tens. reconstruction with golem95, reduction with samurai
   ! 4: tens. reconstruction with golem95, reduction with samurai,
   !    use golem95 if samurai fails

   ! Parameter: Use stable accumulation of diagrams or builtin sum
   !            Stable accumulation is implemented in accu.f90
   logical :: use_sorted_sum = .false.

   ! Flag to decide if results should be converted to CDR
   ! if they are not already in that scheme
   logical :: convert_to_cdr = [%
   @select olp.irregularisation default=DEFAULT
   @case DEFAULT %].false.[%
   @case tHV CDR %].true.[%
   @else %].false.[%
   @end @select %]

   integer :: logfile = 19

   !---#[ Renormalisation:
   ! Parameter to switch UV-Counterterms on or off
   integer :: renormalisation = [%
   @select olp.renormalisation default=yes
   @case no off false %]0[%
   @else %]1[%
   @end @select %]

   ! if renormalisation.eq.1, include alpha_s renormalisation:
   logical :: renorm_beta = [% renorm_beta
             convert=bool
             true=.true.
             false=.false. %]
   ! if renormalisation.eq.1, include massive quark wave function renorm.:
   logical :: renorm_mqwf = [% renorm_mqwf
             convert=bool
             true=.true.
             false=.false. %]
   ! include massive quark contribution for wave function renormalisation
   ! of the gluon
   logical :: renorm_decoupling = [% renorm_decoupling
             convert=bool
             true=.true.
             false=.false. %]

   ! include mass counter terms for internal quark lines
   logical :: renorm_mqse = [% renorm_mqse
             convert=bool
             true=.true.
             false=.false. %]

   ! include finite terms proportional to logs
   logical :: renorm_logs = [% renorm_logs
             convert=bool
             true=.true.
             false=.false. %]

   ! include finite renormalisation of gamma_5
   logical :: renorm_gamma5 = [% renorm_gamma5
             convert=bool
             true=.true.
             false=.false. %]

   ! Switch mass counter terms for massive quarks on or off
   ! deltaOS = 1.0_ki --> on
   ! deltaOS = 0.0_ki --> off
   ! Do not modify directly, use renormalisation=0,1,2 instead.
   real(ki) :: deltaOS = 1.0_ki
   !---#] Renormalisation:[%
@if internal GENERATE_DERIVATIVES %]

   ! This generated code provides the derivatives of the numerator.
   ! Therefore we have the choice between using Golem95's tens_rec
   ! modules for determining the tensor coefficients from N(q) and
   ! using the derivatives to directly accessing the terms of the
   ! Taylor series.
   !
   ! This option affects the calculation only if reduction_interoperation
   ! is chosen such that the tensorial reconstruction method is used.
   logical :: tens_rec_by_derivatives = .true.[%
@end @if %]

   ! Determines the way GoSam treats the overall factor of alpha_(s)/2/pi
   ! in the result of an NLO amplitude.
   !
   ! 0: A factor of alpha_(s)/2/pi is not included in the NLO result
   ! 1: A factor of 1/8/pi^2 is not included in the NLO result
   ! 2: The NLO includes all prefactors
   !
   ! Note, however, that the factor of 1/Gamma(1-eps) is not included
   ! in any of the cases.
   integer :: nlo_prefactors = [% nlo_prefactors %]

   ! Determines the maximum allowed difference among the abs of the
   ! single pole evaluations obtained with the amplitude vs the one
   ! obtained through the IR subroutine relative to the leading order.
   ! 
   ! Note: at the moment it only works for virtual corrections
   ! to Tree level processes.
   logical :: PSP_check = [% PSP_check
             convert=bool
             true=.true.
             false=.false. %]
   integer :: PSP_verbosity = [% PSP_verbosity %]
   integer :: PSP_chk_threshold1 = [% PSP_chk_threshold1 %]
   logical :: PSP_rescue = [% PSP_rescue
             convert=bool
             true=.true.
             false=.false. %]
   integer :: PSP_chk_threshold2 = [% PSP_chk_threshold2 %]
   real(ki) :: PSP_chk_kfactor = [% PSP_chk_kfactor convert=real %].0_ki
end module [% process_name asprefix=\_ %]config

