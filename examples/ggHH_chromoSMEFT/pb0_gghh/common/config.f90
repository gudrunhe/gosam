module     pb0_gghh_config
   implicit none

   integer, parameter :: dbl = kind(1.0d0)
   ! QUADRUPLE PRECISION (ki=16):
   ! integer, parameter :: ki = selected_real_kind(33, 4931)
   ! INTERMEDIATE PRECISION (ki=10):
   ! integer, parameter :: ki = selected_real_kind(18, 4931)
   ! DOUBLE PRECISION (ki=8):
   integer, parameter :: ki = kind(1.0d0)

   ! Options to control the interoperation between different
   ! Reduction libraries:
   integer, parameter :: SAMURAI   = 0
   integer, parameter :: GOLEM95   = 1
   integer, parameter :: NINJA     = 2
   integer, parameter :: PJFRY     = 3 ! experimental
   integer, parameter :: QUADNINJA = 4 ! experimental
   ! Reduction methods
   integer :: reduction_interoperation = NINJA
   ! Rescue reduction method. The rescue system is disabled
   ! if it is equal to reduction_interoperation
   integer :: reduction_interoperation_rescue = NINJA

   ! Debugging settings
   logical :: debug_lo_diagrams  = .false.
   logical :: debug_nlo_diagrams = .false.
   logical :: debug_numpolvec    = .false.

   ! If true, the calculation includes terms proportional to eps^2
   ! multiplying double poles.
   ! These terms are supposed to cancel in QCD.
   logical :: include_eps2_terms = .false.

   ! If true, the calculation includes terms proportional to eps
   ! multiplying double and single poles.
   ! These terms are necessary in 't Hooft-Veltman scheme
   logical :: include_eps_terms = .false.

   logical :: include_color_avg_factor = .true.
   logical :: include_helicity_avg_factor = .true.
   logical :: include_symmetry_factor = .true.

   

   
   integer :: ninja_test = 0
   integer :: ninja_istop = 0

   ! Parameter: Use stable accumulation of diagrams or builtin sum
   !            Stable accumulation is implemented in accu.f90
   logical :: use_sorted_sum = .false.

   ! Flag to decide if results should be converted to CDR
   ! if they are not already in that scheme
   logical :: convert_to_cdr = .false.

   integer :: logfile = 19

   ! Parameter determining the SMEFT counting
   integer :: EFTcount = 3

   !---#[ Renormalisation:
   ! Parameter to switch UV-Counterterms on or off
   integer :: renormalisation = 0

   ! if renormalisation.eq.1, include alpha_s renormalisation:
   logical :: renorm_beta = .false.
   ! if renormalisation.eq.1, include massive quark wave function renorm.:
   logical :: renorm_mqwf = .true.
   ! include massive quark contribution for wave function renormalisation
   ! of the gluon
   logical :: renorm_decoupling = .false.

   ! include mass counter terms for internal quark lines
   logical :: renorm_mqse = .true.

   ! include finite terms proportional to logs
   logical :: renorm_logs = .true.

   ! include finite renormalisation of gamma_5
   logical :: renorm_gamma5 = .true.

   ! include renormalization of yukawa couplings
   logical :: renorm_yukawa = .true.

   ! Switch mass counter terms for massive quarks on or off
   ! deltaOS = 1.0_ki --> on
   ! deltaOS = 0.0_ki --> off
   ! Do not modify directly, use renormalisation=0,1,2 instead.
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
   integer :: nlo_prefactors = 0

   ! Determines the maximum allowed difference among the abs of the
   ! single pole evaluations obtained with the amplitude vs the one
   ! obtained through the IR subroutine relative to the leading order.
   ! Alternatively, the rescue system can be modified to compute all
   ! phase space points twice to asses their stability.

   logical :: PSP_check = .true.
   logical :: PSP_verbosity = .false.
   logical :: PSP_rescue = .false.

   ! Number of good digits in virtual amplitude:
   integer :: PSP_chk_th1 = 8
   integer :: PSP_chk_th2 = 3
   integer :: PSP_chk_th3 = 5
   real(ki) :: PSP_chk_kfactor = 1000.0_ki
   
   ! not used in this process (process is not loop-induced):
   integer :: PSP_chk_li1 = 16
   integer :: PSP_chk_li2 = 7
   integer :: PSP_chk_li3 = 6
   integer :: PSP_chk_li4 = 19


end module pb0_gghh_config

