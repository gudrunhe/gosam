[%' vim: syntax=golem
'%]module     [% process_name %]_config
   implicit none

   integer, parameter :: dbl = kind(1.0d0)
   ! QUADRUPLE PRECISION (ki=16):[%
   @if extension quadruple %]
   integer, parameter :: ki_qp = selected_real_kind(33, 4931)[%
   @else %]
   ! integer, parameter :: ki = selected_real_kind(33, 4931)[%
   @end @if extension quadruple %]
   ! INTERMEDIATE PRECISION (ki=10):
   ! integer, parameter :: ki = selected_real_kind(18, 4931)
   ! DOUBLE PRECISION (ki=8):
   integer, parameter :: ki = kind(1.0d0)

   ! Options to control the interoperation between different
   ! Reduction libraries:
   integer, parameter :: GOLEM95   = 1
   integer, parameter :: NINJA     = 2
   integer, parameter :: QUADNINJA = 4
   ! Reduction methods
   integer :: reduction_interoperation = [%
   @select reduction_interoperation default="-1"
   @case -1 %][%
      @if extension ninja %]NINJA[%
      @else %][%
            @if extension golem95 %]GOLEM95[%
             @else%]-1[%
            @end @if %][%
      @end @if %][%
   @else %][% reduction_interoperation %][%
   @end @select %]
   ! Rescue reduction method. The rescue system is disabled
   ! if it is equal to reduction_interoperation
   integer :: reduction_interoperation_rescue = [%
   @select reduction_interoperation_rescue default="-1"
   @case -1 %][%
      @if extension golem95 %]GOLEM95[%
      @else %][%
           @if extension quadruple %]QUADNINJA[%
           @else %][%
           @select reduction_interoperation default="-1"
           @case -1 %][%
              @if extension ninja %]NINJA[%
              @else %][%
                    @if extension golem95 %]GOLEM95[%
                     @else%]-1[%
                    @end @if %][%
              @end @if %][%
           @else %]-1[%
           @end @select %][%
           @end @if %][%
      @end @if %][%
   @else %][% reduction_interoperation_rescue %][%
   @end @select %]

   ! Debugging settings
   logical :: debug_lo_diagrams  = [%
      @if anymember lo all debug ignore_case=true %].true.[%
      @else %].false.[%
      @end @if %]
   logical :: debug_nlo_diagrams = [%
      @if anymember nlo all debug ignore_case=true %].true.[%
      @else %].false.[%
      @end @if %][%

      @if internal NUMPOLVEC %]
   logical :: debug_numpolvec    = [%
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

   logical :: include_color_avg_factor = .[%
        olp.include_color_average default=true %].
   logical :: include_helicity_avg_factor = .[%
        olp.include_helicity_average default=true %].
   logical :: include_symmetry_factor = .[%
        olp.include_symmetry_factor default=true %].

   [% @if extension ninja %]
   integer :: ninja_test = 0
   integer :: ninja_istop = 0[%
      @end @if extension ninja %]

   ! Parameter: Use stable accumulation of diagrams or builtin sum
   !            Stable accumulation is implemented in accu.f90
   logical :: use_sorted_sum = .false.

   ! Flag to decide if results should be converted to CDR
   ! if they are not already in that scheme
   logical :: convert_to_cdr = [% convert_to_cdr
             convert=bool
             true=.true.
             false=.false. %]

   integer :: logfile = 19

   ! Parameter determining the SMEFT counting
   integer :: EFTcount = 3

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

   ! include renormalization of yukawa couplings
   logical :: renorm_yukawa = [% renorm_yukawa
              convert=bool
              true=.true.
              false=.false. %]

   ! if renormalisation.eq.1, include renormalisation of EFT Wilson coefficients (only works with special UFO models):
   logical :: renorm_eftwilson = [% renorm_eftwilson
             convert=bool
             true=.true.
             false=.false. %]

   ! if renormalisation.eq.1 and heavy-top limit, include finite Higgs-gluon-vertex renormalisation:
             logical :: renorm_ehc = [% renorm_ehc
             convert=bool
             true=.true.
             false=.false. %]

   ! Switch mass counter terms for massive quarks on or off (old way, only left for debugging)
   ! deltaOS = 1.0_ki --> on
   ! deltaOS = 0.0_ki --> off
   ! Do not modify directly, use renormalisation=0,1,2,3,4 instead.
   real(ki) :: deltaOS = 1.0_ki
   !---#] Renormalisation:

   ! This generated code provides the derivatives of the numerator.
   ! Therefore we have the choice between using Golem95's tens_rec
   ! modules for determining the tensor coefficients from N(q) and
   ! using the derivatives to directly accessing the terms of the
   ! Taylor series.
   !
   ! This option affects the calculation only if reduction_interoperation
   ! is chosen such that the tensorial reconstruction method is used.
   logical :: tens_rec_by_derivatives = .true.

   ! Determines the way GoSam treats the overall factor of alpha_(s)/2/pi
   ! in the result of an NLO amplitude.
   !
   ! 0: A factor of alpha_(s)/2/pi is not included in the NLO result
   ! 1: A factor of 1/8/pi^2 is not included in the NLO result
   ! 2: The NLO includes all prefactors
   !
   ! For loop-induced processes:
   ! 0: A factor of (alpha_(s)/2/pi)**2 is not included in the virtual result
   ! 1: A factor of (1/8/pi^2)**2 is not included in the virtual result
   ! 2: The result includes all prefactors (= (alpha_(s)/2/pi)**2)
   !
   ! Note, however, that the factor of 1/Gamma(1-eps) is not included
   ! in any of the cases.
   integer :: nlo_prefactors = [% nlo_prefactors %]

   ! Determines the maximum allowed difference among the abs of the
   ! single pole evaluations obtained with the amplitude vs the one
   ! obtained through the IR subroutine relative to the leading order.
   ! Alternatively, the rescue system can be modified to compute all
   ! phase space points twice to asses their stability.

   logical :: PSP_check = [% PSP_check
             convert=bool
             true=.true.
             false=.false. %]
   logical :: PSP_verbosity = [% PSP_verbosity
             convert=bool
             true=.true.
             false=.false. %]
   logical :: PSP_rescue = [% PSP_rescue
             convert=bool
             true=.true.
             false=.false. %]

   ! Number of good digits in virtual amplitude:[%
   @if generate_lo_diagrams %][% @else %]
   ! not used (tree-level not available):[% @end @if %]
   integer :: PSP_chk_th1 = [% PSP_chk_th1 %] ! pole-check (th1 < r => accept)
   integer :: PSP_chk_th2 = [% PSP_chk_th2 %] ! pole-check (th2 < r < th1 => rotation, r < th2 => rescue)
   integer :: PSP_chk_th3 = [% PSP_chk_th3 %] ! double/double rotation (th3 < r => accept, r < th3 => rescue)
   integer :: PSP_chk_th4 = [% PSP_chk_th4 %] ! double/quad rotation (th4 < r => accept, r < th4 => discard) 
   integer :: PSP_chk_th5 = [% PSP_chk_th5 %] ! quad/quad_rot rotation (th5 < r => accept, r < th5 => discard)

   real(ki) :: PSP_chk_kfactor = [% PSP_chk_kfactor convert=real %].0_ki
   [% @if generate_lo_diagrams %]
   ! not used in this process (process is not loop-induced):[%
   @else %]
   ! used instead:[%
   @end @if %]
   integer :: PSP_chk_li1 = [% PSP_chk_li1 %] ! pole-check (li1 < r => accept)
   integer :: PSP_chk_li2 = [% PSP_chk_li2 %] ! pole-check (li2 < r < li1 => rotation, r < li2 => rescue)
   integer :: PSP_chk_li3 = [% PSP_chk_li3 %] ! double/double rotation (li3 < r => accept, r < li3 => rescue)
   integer :: PSP_chk_li4 = [% PSP_chk_li4 %] ! double/quad rotation (li4 < r => accept, r < li4 => discard)
   integer :: PSP_chk_li5 = [% PSP_chk_li5 %] ! quad/quad_rot rotation (li5 < r => accept, r < li5 => discard)

[%
@if ewchoose %]
   !
   ! The integer ewchoice allows the user to change the 
   ! ew parameter input scheme at runtime (between 1 and 8)
   ! The choices are as follows:
   !  ewchoice :   Input            :  Output
   !  #---------------------------------------# 
   !  1        :   GF,mW,mZ         : e,sw
   !  2        :   alpha, mW, mZ    : e,sw
   !  3        :   alpha, sw, mZ    : e, mW
   !  4        :   alpha, sw, GF    : e, mW
   !  5        :   alpha, GF, mZ    : e, mW, sw[% 
@if e_not_one %]
   !  6        :   e, mW, mZ        : sw
   !  7        :   e, sw, mZ        : mW
   !  8        :   e, sw, GF        : mW, mZ[%
@else %]
   !
   !  WARNING:
   !  Since 'e' was set to ONE algebraically, it cannot
   !  be used as an input parameter, and will also not
   !  be computed from the other parameters.[%
@end @if %]
   !
   !  If one is using the ewchoice, the user should provide the 
   !  correct input parameters, otherwise default values are used.
   !
   integer :: ewchoice = [% starting_choice %][%
   @end @if %]
end module [% process_name %]_config

