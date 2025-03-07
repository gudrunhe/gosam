[% ' vim: ts=3:sw=3:expandtab:syntax=golem '
 %]module    [% process_name asprefix=\_ %]ct_amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki
   implicit none
   private

   public :: amplitude
contains[% 
@if generate_counterterms %]

   !---#[ function amplitude:
   function amplitude(scale2) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model
      use [% process_name asprefix=\_ %]color, only: numcs
      use [% process_name asprefix=\_ %]kinematics, only: corrections_are_qcd
      use [% @if internal OLP_MODE %][% @else %][% process_name %]_[% @end @if %]config, only: &
         & renormalisation, renorm_beta, renorm_mqwf, renorm_decoupling, &
         & renorm_logs, renorm_mqse, renorm_yukawa, renorm_eftwilson, &
         & renorm_ehc, renorm_gamma5, nlo_prefactors
      use [% process_name asprefix=\_ %]dipoles, only: pi
      use [% process_name asprefix=\_ %]counterterms, only: counterterm_alphas, counterterm_gluonwf, counterterm_mqwf[%
@if generate_lo_diagrams %][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0, only: amp0_0 => amplitude[%
@select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1, only: amp0_1 => amplitude[%
@case 2%]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2, only: amp0_2 => amplitude[%
@end @select %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0, only: amp0 => amplitude[%
@end @if enable_truncation_orders %][%
@end @if generate_lo_diagrams %][%
@if generate_ym_counterterms %][%
@if generate_lo_diagrams%][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0, only: ampdymct_0 => amplitude_Dym[%
@select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1, only: ampdymct_1 => amplitude_Dym[%
@case 2 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2, only: ampdymct_2 => amplitude_Dym[%
@end @select %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0, only: ampdymct => amplitude_Dym[%
@end @if enable_truncation_orders %][%
@end @if generate_lo_diagrams%][%
@end @if generate_ym_counterterms %][%
@if generate_eft_counterterms %][%
@if eval topolopy.count.ct .gt. 0 %][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_0, only: ampeftct_0 => amplitude[%
           @select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_1, only: ampeftct_1 => amplitude[%
@case 2%]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_2, only: ampeftct_2 => amplitude[%
@end @select %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct, only: ampeftct => amplitude[%
@end @if enable_truncation_orders %][%
@end @if %][%
@end @if generate_eft_counterterms %]

      implicit none
      complex(ki), dimension(-1:0,numcs) :: amp
      real(ki), dimension(-1:0) ::  Deltagwf[% @if enable_truncation_orders %]_0, Deltagwf_1, Deltagwf_2[% @end @if %]
      real(ki) :: scale2, nlo_coupling, prefac

      ! Number of heavy quark flavours in loops.
      real(ki), parameter :: NFh = [% count quark_loop_masses %].0_ki

      amp(:,:) = 0._ki[% 
@if enable_truncation_orders %]
      Deltagwf_0(:) = 0._ki[% 
@select trnco @case 1 %]
      Deltagwf_1(:) = 0._ki[% 
@case 2%]
      Deltagwf_2(:) = 0._ki[% 
@end @select %][% 
@else %]
      Deltagwf(:) = 0._ki[% 
@end @if %]

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
[% @if generate_lo_diagrams %][%
@if enable_truncation_orders %][%
@select trnco @case 0 %]
      select case (renormalisation)
      case(0)
         ! no renormalisation; should never get here
         return
      case(1)
         ! fully renormalised
         if (corrections_are_qcd) then
      
            ! alpha_s renormalisation:      
            if (renorm_beta) then
               Deltagwf_0 = Deltagwf_0 + counterterm_alphas(scale2)
            end if

            ! gluon wave function renormalisation:
            if (renorm_decoupling) then
               Deltagwf_0 = Deltagwf_0 + counterterm_gluonwf(scale2)
            end if  

            ! quark wave function renormalisation:
            if (renorm_mqwf) then
               Deltagwf_0 = Deltagwf_0 + counterterm_mqwf(scale2)
            end if
                    
            amp(-1,:) = amp(-1,:) + 0.5_ki*Deltagwf_0(-1)*amp0_0()
            amp( 0,:) = amp( 0,:) + 0.5_ki*Deltagwf_0( 0)*amp0_0()[%
     @if generate_ym_counterterms %]
     
            ! Yukawa coupling and quark mass renormalisation
            ! Finite renormalisation for gamma5 in cdr
            if (renorm_yukawa.or.renorm_mqse.or.renorm_gamma5) then
               amp(-1,:) = amp(-1,:) + ampdymct_0(scale2, -1)
               amp( 0,:) = amp( 0,:) + ampdymct_0(scale2,  0)
            end if[% 
     @end @if generate_ym_counterterms %][%
     @if generate_eft_counterterms %][%
     @if eval topolopy.count.ct .gt. 0 %]
     
            ! EFT Wilson coefficient renormalisation
            if (renorm_eftwilson) then
               ! account for nlo_prefactors in EFT counterterms
               prefac = 8.0_ki*pi**2/nlo_coupling
               amp((/-1,0/),:) = amp((/-1,0/),:) + prefac*ampeftct_0(renorm_logs, scale2)
            end if[%
     @end @if %][%
     @end @if generate_eft_counterterms %]
         end if ! corrections_are_qcd
      case(2)[%
     @if generate_ym_counterterms %]
         if (corrections_are_qcd) then
         ! quark mass renormalisation
            amp(-1,:) = amp(-1,:) + ampdymct_0(scale2, -1)
            amp( 0,:) = amp( 0,:) + ampdymct_0(scale2,  0)
         end if[% 
     @end @if generate_ym_counterterms %]
      case(3)
         ! quark mass renormalisation using old implementation; should never get here
         return
      end select ! renormalisation[%
 @case 1 %]
      select case (renormalisation)
      case(0)
         ! no renormalisation; should never get here
         return
      case(1)
         ! fully renormalised
         if (corrections_are_qcd) then
      
            ! alpha_s renormalisation:      
            if (renorm_beta) then
               Deltagwf_0 = Deltagwf_0 + counterterm_alphas(scale2)
               ! SMEFT contribution to QCD beta function (currently placeholder):
               Deltagwf_1 = Deltagwf_1 + 0._ki
            end if

            ! gluon wave function renormalisation:
            if (renorm_decoupling) then
               Deltagwf_0 = Deltagwf_0 + counterterm_gluonwf(scale2)
               ! SMEFT contribution to gluon WF renormalisation (currently placeholder):
               Deltagwf_1 = Deltagwf_1 + 0._ki
            end if  

            ! quark wave function renormalisation:
            if (renorm_mqwf) then
               Deltagwf_0 = Deltagwf_0 + counterterm_mqwf(scale2)
               ! SMEFT contribution to massive quark WF renormalisation (currently placeholder):
               Deltagwf_1 = Deltagwf_1 + 0._ki
            end if
        
            amp(-1,:) = amp(-1,:) + 0.5_ki*Deltagwf_0(-1)*amp0_1() + 0.5_ki*Deltagwf_1(-1)*amp0_0()
            amp( 0,:) = amp( 0,:) + 0.5_ki*Deltagwf_0( 0)*amp0_1() + 0.5_ki*Deltagwf_1( 0)*amp0_0()[%
     @if generate_ym_counterterms %]
     
            ! Yukawa coupling and quark mass renormalisation
            ! Finite renormalisation for gamma5 in cdr
            if (renorm_yukawa.or.renorm_mqse.or.renorm_gamma5) then
               amp(-1,:) = amp(-1,:) + ampdymct_1(scale2, -1)
               amp( 0,:) = amp( 0,:) + ampdymct_1(scale2,  0)
            end if[% 
     @end @if generate_ym_counterterms %][%
     @if generate_eft_counterterms %][%
     @if eval topolopy.count.ct .gt. 0 %]
     
            ! EFT Wilson coefficient renormalisation
            if (renorm_eftwilson) then
               ! account for nlo_prefactors in EFT counterterms
               prefac = 8.0_ki*pi**2/nlo_coupling
               amp((/-1,0/),:) = amp((/-1,0/),:) + prefac*ampeftct_1(renorm_logs, scale2)
            end if[%
     @end @if %][%
     @end @if generate_eft_counterterms %]
         end if ! corrections_are_qcd
      case(2)[%
      @if generate_ym_counterterms %]
         if (corrections_are_qcd) then
            ! quark mass renormalisation
            amp(-1,:) = amp(-1,:) + ampdymct_1(scale2, -1)
            amp( 0,:) = amp( 0,:) + ampdymct_1(scale2,  0)
         end if[% 
      @end @if generate_ym_counterterms %]
      case(3)
         ! quark mass renormalisation using old implementation; should never get here
         return
      end select ! renormalisation[%
@case 2 %]
      select case (renormalisation)
      case(0)
         ! no renormalisation; should never get here
         return
      case(1)
         ! fully renormalised
         if (corrections_are_qcd) then
      
            ! alpha_s renormalisation:      
            if (renorm_beta) then
               Deltagwf_0 = Deltagwf_0 + counterterm_alphas(scale2)
               ! SMEFT contribution to QCD beta function (currently placeholder):
               Deltagwf_2 = Deltagwf_2 + 0._ki
            end if

            ! gluon wave function renormalisation:
            if (renorm_decoupling) then
               Deltagwf_0 = Deltagwf_0 + counterterm_gluonwf(scale2)
               ! SMEFT contribution to gluon WF renormalisation (currently placeholder):
               Deltagwf_2 = Deltagwf_2 + 0._ki
            end if  

            ! quark wave function renormalisation:
            if (renorm_mqwf) then
               Deltagwf_0 = Deltagwf_0 + counterterm_mqwf(scale2)
               ! SMEFT contribution to massive quark WF renormalisation (currently placeholder):
               Deltagwf_2 = Deltagwf_2 + 0._ki
            end if
        
            amp(-1,:) = amp(-1,:) + 0.5_ki*Deltagwf_0(-1)*amp0_2() + 0.5_ki*Deltagwf_2(-1)*amp0_0()
            amp( 0,:) = amp( 0,:) + 0.5_ki*Deltagwf_0( 0)*amp0_2() + 0.5_ki*Deltagwf_2( 0)*amp0_0()[%
     @if generate_ym_counterterms %]
     
            ! Yukawa coupling and quark mass renormalisation
            ! Finite renormalisation for gamma5 in cdr
            if (renorm_yukawa.or.renorm_mqse.or.renorm_gamma5) then
               amp(-1,:) = amp(-1,:) + ampdymct_2(scale2, -1)
               amp( 0,:) = amp( 0,:) + ampdymct_2(scale2,  0)
            end if[% 
     @end @if generate_ym_counterterms %][%
     @if generate_eft_counterterms %][%
     @if eval topolopy.count.ct .gt. 0 %]
     
            ! EFT Wilson coefficient renormalisation
            if (renorm_eftwilson) then
               ! account for nlo_prefactors in EFT counterterms
               prefac = 8.0_ki*pi**2/nlo_coupling
               amp((/-1,0/),:) = amp((/-1,0/),:) + prefac*ampeftct_2(renorm_logs, scale2)
            end if[%
     @end @if %][%
     @end @if generate_eft_counterterms %]
         end if ! corrections_are_qcd
      case(2)[%
      @if generate_ym_counterterms %]
         if (corrections_are_qcd) then
            ! quark mass renormalisation
            amp(-1,:) = amp(-1,:) + ampdymct_2(scale2, -1)
            amp( 0,:) = amp( 0,:) + ampdymct_2(scale2,  0)
         end if[% 
      @end @if generate_ym_counterterms %]
      case(3)
         ! quark mass renormalisation using old implementation; should never get here
         return
      end select ! renormalisation[%
@else %]
      ! ct_amplitude.f90 has been generated with trnco = [% trnco %]. This should dnever happen!
[% @end @select  %]
[% @else %][% ' not enable_truncation_orders '%]
      select case (renormalisation)
      case(0)
         ! no renormalisation; should never get here
         return
      case(1)
         ! fully renormalised
         if (corrections_are_qcd) then
      
            ! alpha_s renormalisation:      
            if (renorm_beta) then
               Deltagwf = Deltagwf + counterterm_alphas(scale2)
            end if

            ! gluon wave function renormalisation:
            if (renorm_decoupling) then
               Deltagwf = Deltagwf + counterterm_gluonwf(scale2)
            end if  

            ! quark wave function renormalisation:
            if (renorm_mqwf) then
               Deltagwf = Deltagwf + counterterm_mqwf(scale2)
            end if

            amp(-1,:) = amp(-1,:) + 0.5_ki*Deltagwf(-1)*amp0()
            amp( 0,:) = amp( 0,:) + 0.5_ki*Deltagwf( 0)*amp0()[% 
      @if finite_renorm_ehc %]
      
            ! Adding finite renormalization of Wilson coefficient for effective Higgs coupling
            ! CAUTION: 
            ! This will only work if the number of Higgs-gluon couplings is the 
            ! same for all Born diagrams!
            if (renorm_ehc) then[%
      @for effective_higgs %][%
      @if is_ehc%]
               !amp(0,:) = amp(0,:) + (11.0_ki/2.0_ki -1.0_ki/3.0_ki*log(scale2/mH**2)) * amp0
               amp(0,:) = amp(0,:) + (11.0_ki/2.0_ki) * amp0()[%
      @end @if %][%
      @end @for %]
            end if[% 
      @end @if %][%
      @if generate_ym_counterterms %]
      
            ! Yukawa coupling and quark mass renormalisation
            ! Finite renormalisation for gamma5 in cdr
            if (renorm_yukawa.or.renorm_mqse.or.renorm_gamma5) then
               amp(-1,:) = amp(-1,:) + ampdymct(scale2, -1)
               amp( 0,:) = amp( 0,:) + ampdymct(scale2,  0)
            end if[% 
      @end @if generate_ym_counterterms %][%
      @if generate_eft_counterterms %][%
      @if eval topolopy.count.ct .gt. 0 %]
      
            ! EFT Wilson coefficient renormalisation
            if (renorm_eftwilson) then
               ! account for nlo_prefactors in EFT counterterms
               prefac = 8.0_ki*pi**2/nlo_coupling
               amp((/-1,0/),:) = amp((/-1,0/),:) + prefac*ampeftct(renorm_logs, scale2)
            end if[%
      @end @if %][%
      @end @if generate_eft_counterterms %]
         end if ! corrections_are_qcd
      case(2)[%
         @if generate_ym_counterterms %]
         if (corrections_are_qcd) then
            ! quark mass renormalisation
            amp(-1,:) = amp(-1,:) + ampdymct(scale2, -1)
            amp( 0,:) = amp( 0,:) + ampdymct(scale2,  0)
         end if[% 
         @end @if generate_ym_counterterms %]
      case(3)
         ! quark mass renormalisation using old implementation; should never get here
         return
      end select ! renormalisation[%
      @end @if enable_truncation_orders %][%
      @else %]
      ! No tree level present[%
      @end @if generate_lo_diagrams %]

   end function amplitude
   !---#] function amplitude:[% 
@end @if generate_counterterms %]

end module [% process_name asprefix=\_ %]ct_amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]