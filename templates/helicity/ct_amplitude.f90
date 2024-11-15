[% ' vim: ts=3:sw=3:expandtab:syntax=golem '
 %]module    [% process_name asprefix=\_ %]ct_amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki[% @if extension quadruple %] => ki_qp[% @end @if %]
   implicit none
   private

   public :: amplitude
contains

   !---#[ function amplitude:
   function     amplitude(logs,scale2) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model[% @if extension quadruple %]_qp[% @end @if %]
      use [% process_name asprefix=\_ %]color[% @if extension quadruple %]_qp[% @end @if %], only: TR, CF, CA, numcs
      use [% process_name asprefix=\_ %]kinematics, only: lo_qcd_couplings, corrections_are_qcd, num_gluons
      use [% @if internal OLP_MODE %][% @else %][% process_name %]_[% @end @if %]config, only: &
         & renormalisation, renorm_beta, renorm_mqwf, renorm_decoupling, &
         & renorm_logs, renorm_mqse, renorm_yukawa, renorm_eftwilson, &
         & renorm_ehc, nlo_prefactors
      use [% process_name asprefix=\_ %]dipoles[% @if extension quadruple %]_qp[% @end @if %], only: pi
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
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0_qp, only: amp0_0_qp => amplitude[% 
@select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1_qp, only: amp0_1_qp => amplitude[% 
@case 2%]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2_qp, only: amp0_2_qp => amplitude[% 
@end @select %][%
@end @if %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0, only: amp0 => amplitude[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_qp, only: amp0_qp => amplitude[%
@end @if %][%
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
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0_qp, only: ampdymct_0_qp => amplitude_Dym[% 
@select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1_qp, only: ampdymct_1_qp => amplitude_Dym[% 
@case 2%]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2_qp, only: ampdymct_2_qp => amplitude_Dym[% 
           @end @select %][%
@end @if %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0, only: ampdymct => amplitude_Dym[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_qp, only: ampdymct_qp => amplitude_Dym[%
@end @if %][%
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
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_0_qp, only: ampeftct_0_qp => amplitude[% 
@select trnco @case 1 %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_1_qp, only: ampeftct_1_qp => amplitude[% 
@case 2%]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_2_qp, only: ampeftct_2_qp => amplitude[% 
@end @select %][%
@end @if %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct, only: ampeftct => amplitude[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_qp, only: ampeftct_qp => amplitude[%
@end @if %][%
@end @if enable_truncation_orders %][%
@end @if %][%
@end @if generate_eft_counterterms %]

      implicit none
      complex(ki), dimension(-2:0,numcs) :: amp
      real(ki), dimension(-2:0) ::  Deltagwf[% @if enable_truncation_orders %]_0, Deltagwf_1, Deltagwf_2[% @end @if %]
      real(ki) :: scale2, nlo_coupling, prefac     
      logical :: logs

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
            if (renorm_yukawa.or.renorm_mqse) then
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
               amp((/-2,-1,0/),:) = amp((/-2,-1,0/),:) + prefac*ampeftct_0(renorm_logs, scale2)
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
            if (renorm_yukawa.or.renorm_mqse) then
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
               amp((/-2,-1,0/),:) = amp((/-2,-1,0/),:) + prefac*ampeftct_1(renorm_logs, scale2)
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
            if (renorm_yukawa.or.renorm_mqse) then
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
               amp((/-2,-1,0/),:) = amp((/-2,-1,0/),:) + prefac*ampeftct_2(renorm_logs, scale2)
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
            if (renorm_yukawa.or.renorm_mqse) then
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
               amp((/-2,-1,0/),:) = amp((/-2,-1,0/),:) + prefac*ampeftct(renorm_logs, scale2)
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
   !---#] function amplitude:

end module [% process_name asprefix=\_ %]ct_amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]