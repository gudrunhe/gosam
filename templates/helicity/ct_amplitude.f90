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
         & deltaOS, renorm_beta, renorm_mqwf, renorm_decoupling, &
         & renorm_logs, renorm_mqse, renorm_yukawa, renorm_eftwilson, &
         & renorm_ehc, nlo_prefactors[%
@if generate_lo_diagrams %][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0, only: amp0_0 => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1, only: amp0_1 => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2, only: amp0_2 => amplitude[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0_qp, only: amp0_0_qp => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1_qp, only: amp0_1_qp => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2_qp, only: amp0_2_qp => amplitude[%
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
@if generate_yuk_counterterms %][%
@if generate_lo_diagrams%][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0, only: ampyukct_0 => amplitude_yukren
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1, only: ampyukct_1 => amplitude_yukren
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2, only: ampyukct_2 => amplitude_yukren[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_0_qp, only: ampyukct_0_qp => amplitude_yukren
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_1_qp, only: ampyukct_1_qp => amplitude_yukren
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_2_qp, only: ampyukct_2_qp => amplitude_yukren[%
@end @if %][%
@else %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0, only: ampyukct => amplitude_yukren[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]l0_qp, only: ampyukct_qp => amplitude_yukren[%
@end @if %][%
@end @if enable_truncation_orders %][%
@end @if generate_lo_diagrams%][%
@end @if generate_yuk_counterterms %][%
@if generate_eft_counterterms %][%
@if eval topolopy.count.ct .gt. 0 %][%
@if enable_truncation_orders %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_0, only: ampeftct_0 => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_1, only: ampeftct_1 => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_2, only: ampeftct_2 => amplitude[%
@if extension quadruple %]
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_0_qp, only: ampeftct_0_qp => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_1_qp, only: ampeftct_1_qp => amplitude
      use [% process_name asprefix=\_
           %]diagramsh[%helicity%]ct_2_qp, only: ampeftct_2_qp => amplitude[%
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
      real(ki) :: scale2, nlo_coupling      
      logical :: logs

      ! Number of heavy quark flavours in loops.
      real(ki), parameter :: NFh = [% count quark_loop_masses %].0_ki

      amp(:,:) = 0._ki
      Deltagwf[% 
@if enable_truncation_orders %]_0(:) = 0._ki
      Deltagwf_1(:) = 0._ki
      Deltagwf_2(:)[% 
@end @if %] = 0._ki

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
@if enable_truncation_orders %]
      ! truncation orders not implemented yet!
[% @else %][% ' not enable_truncation_orders '%]
      if (corrections_are_qcd) then
      
      ! alpha_s renormalisation:      
         if (renorm_beta) then
               Deltagwf(-1) = Deltagwf(-1) - lo_qcd_couplings * (11.0_ki * CA - 4.0_ki * TR * (NF + NFh)) / 6.0_ki[%    
      @for quark_loop_masses %][%
      @if is_first %]
               if (renorm_logs) then[%
      @end @if %][%
      @if is_real %]
                  Deltagwf(0) = Deltagwf(0) + lo_qcd_couplings * (4.0_ki * TR / 6.0_ki * log(scale2/[% $_ %]**2))[%
      @end @if %][%
      @if is_complex %]
                  Deltagwf(0) = Deltagwf(0) + lo_qcd_couplings * (4.0_ki * TR / 6.0_ki * log(scale2/[% $_ %]/conjg([% $_ %])))[%
      @end @if %][%
      @if is_last %]
               end if[%
      @end @if %][%
      @end @for %][%
      @if extension dred %]
            Deltagwf(0) = Deltagwf(0) + lo_qcd_couplings * (CA / 6.0_ki)[%
      @end @if %]
         end if[%
      @for particles massive quarks anti-quarks %][%
      @if is_first %]
      
      ! quark wave function renormalisation:[% 
      @end @if %]
         if (renorm_mqwf) then
            Deltagwf(-1) = Deltagwf(-1) - 1.5_ki * CF
            Deltagwf(0) = Deltagwf(0) - [% @if extension dred %]2.5[% @else %]2.0[% @end @if %]_ki * CF
            if (renorm_logs) then
               Deltagwf(0) = Deltagwf(0) - (1.5_ki*log(scale2/[%mass%]/[%mass%])) * CF
            end if
         end if[%
      @end @for %][%
      @for quark_loop_masses %][%
      @if is_first %]
      
      ! gluon wave function renormalisation:
         if (renorm_decoupling) then
            Deltagwf(-1) = Deltagwf(-1) - num_gluons * 2.0_ki * TR / 3.0_ki * NFh
            if (renorm_logs) then[%
      @end @if %][%
      @if is_real %]
               Deltagwf(0) = Deltagwf(0) - num_gluons * 2.0_ki * TR / 3.0_ki * log(scale2/[% $_ %]**2)[%
      @end @if %][%
      @if is_complex %]
               Deltagwf(0) = Deltagwf(0) - num_gluons * 2.0_ki * TR / 3.0_ki * log(scale2/[% $_ %]/conjg([% $_ %]))[%
      @end @if %][%
      @if is_last %]
            end if
         end if[%
      @end @if %][%
      @end @for %]      
         
         amp(-1,:) = amp(-1,:) + 0.5_ki*Deltagwf[% @if enable_truncation_orders %]_0[% @end @if %](-1)*amp0()
         amp(0,:) = amp(0,:) + 0.5_ki*Deltagwf[% @if enable_truncation_orders %]_0[% @end @if %](0)*amp0()[% 
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
      @if generate_yuk_counterterms %]
      
      ! Yukawa coupling renormalisation
         if (renorm_yukawa) then
            amp(-1,:) = amp(-1,:) + ampyukct(renorm_logs, scale2, -1)
            amp(0,:) = amp(0,:) + ampyukct(renorm_logs, scale2, 0)
         end if[% 
      @end @if generate_yuk_counterterms %][%
      @if generate_eft_counterterms %][%
      @if eval topolopy.count.ct .gt. 0 %]
      
      ! EFT Wilson coefficient renormalisation
         if (renorm_eftwilson) then
            ! account for nlo_prefactors in EFT counterterms
            prefac = 8.0_ki*pi**2/nlo_coupling
            amp((/-2,0,1/),:) = amp((/-2,0,1/),:) + prefac*ampeftct(renorm_logs, scale2)
         end if[%
      @end @if %][%
      @end @if generate_eft_counterterms %]
      end if ! corrections_are_qcd[%
      @end @if enable_truncation_orders %][%
      @else %]
      ! No tree level present[%
      @end @if generate_lo_diagrams %]

   end function amplitude
   !---#] function amplitude:

end module [% process_name asprefix=\_ %]ct_amplitudeh[% helicity %][% @if enable_truncation_orders %]_[% trnco %][% @end @if %]