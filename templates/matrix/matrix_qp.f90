[% ' vim: syntax=golem '
%]module     [% process_name asprefix=\_ %]matrix_qp   
   use [% process_name asprefix=\_ %]util_qp, only: square_qp => square
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki_qp, &
     & include_helicity_avg_factor, include_color_avg_factor, &
     & debug_lo_diagrams, debug_nlo_diagrams, &
     & include_symmetry_factor, &
     & convert_to_thv, &
     & EFTcount
   use [% process_name asprefix=\_ %]kinematics, only: &
       in_helicities, symmetry_factor, num_legs, &
       corrections_are_qcd, num_light_quarks, num_gluons
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp, only: Nf_qp => Nf, NC_qp => NC, sqrt2_qp => sqrt2, &
     & init_functions_qp => init_functions
   use [% process_name asprefix=\_ %]color_qp, only: CA_qp => CA, CF_qp => CF, &
     & numcs, incolors[%
   @if enable_truncation_orders %][%
   @for helicities generated %][%
      @if generate_tree_diagrams %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_0_qp, only: amplitude[%helicity%]l0_0_qp => amplitude
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_1_qp, only: amplitude[%helicity%]l0_1_qp => amplitude
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_2_qp, only: amplitude[%helicity%]l0_2_qp => amplitude[%
      @end @if generate_tree_diagrams %][%
      @if generate_eft_loopind %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_2_qp, only: amplitude[%helicity%]l0_2_qp => amplitude[%
      @end @if generate_eft_loopind %][%
      @if generate_counterterms %]
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_0_qp, only: ct_amplitude[%helicity%]_0_qp => amplitude
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_1_qp, only: ct_amplitude[%helicity%]_1_qp => amplitude
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_2_qp, only: ct_amplitude[%helicity%]_2_qp => amplitude[% 
      @end @if generate_counterterms %][%
   @if helsum %][% @else %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_0_qp, [% ' '
        %]only: samplitudeh[%helicity%]l1_0_qp => samplitude
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_1_qp, [% ' '
        %]only: samplitudeh[%helicity%]l1_1_qp => samplitude
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_2_qp, [% ' '
        %]only: samplitudeh[%helicity%]l1_2_qp => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @for helicities generated %][%
   @if helsum %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
      %]amplitude_0_qp, only: samplitudel1_0summed_qp => samplitude
   use [% process_name asprefix=\_
      %]amplitude_1_qp, only: samplitudel1_1summed_qp => samplitude
   use [% process_name asprefix=\_
      %]amplitude_2_qp, only: samplitudel1_2summed_qp => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @else %][% ' not enable_truncation_orders ' %][%
   @for helicities generated %][%
      @if generate_tree_diagrams %]  
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_qp, only: amplitude[%helicity%]l0_qp => amplitude[%
      @end @if generate_tree_diagrams %][%
      @if generate_counterterms %]
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_qp, only: ct_amplitude[%helicity%]_qp => amplitude[% 
      @end @if generate_counterterms %][%
   @if helsum %][% @else %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_qp, [% ' '
        %]only: samplitudeh[%helicity%]l1_qp => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @for helicities generated %][%
   @if helsum %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
      %]amplitude_qp, only: samplitudel1summed_qp => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @if enable_truncation_orders %]
   use [% process_name asprefix=\_
      %]dipoles_qp, only: insertion_operator_qp => insertion_operator, &
     & insertion_operator_qed_qp => insertion_operator_qed

   implicit none
   save

   private

   public :: samplitudel01_qp 
   public :: samplitudel0_qp, samplitudel0_h_qp 
   public :: samplitudel1_qp, samplitudel1_h_qp[%
@if generate_counterterms %]
   public :: samplitudect_qp, samplitudect_h_qp[%
@end @if %]
   public :: ir_subtraction_qp, ir_subtraction_h_qp


[% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0  %]   private:: get_formfactor_lo [% @end @if %]
[% @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]   private:: get_formfactor_nlo [% @end @if %]

contains

   !---#[ subroutine samplitudel01_qp :
   subroutine samplitudel01_qp(vecs, scale2, amp, rat2, ok, h)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & debug_lo_diagrams, debug_nlo_diagrams, logfile, deltaOS, &
         & renormalisation, renorm_logs, renorm_mqse, nlo_prefactors
      use [% process_name asprefix=\_ %]kinematics_qp, only: &
         & inspect_kinematics, init_event
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp
      use [% process_name asprefix=\_ %]dipoles_qp, only: pi
      implicit none
      real(ki_qp), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki_qp), intent(in) :: scale2
      real(ki_qp), dimension(4), intent(out) :: amp
      real(ki_qp), intent(out) :: rat2
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h
      real(ki_qp) :: nlo_coupling
      logical :: my_ok

      if(corrections_are_qcd) then[%
      @select QCD_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki_qp[%
      @else %]
         nlo_coupling = [% QCD_COUPLING_NAME %]*[% QCD_COUPLING_NAME %][%
      @end @select %]
      else[%
      @select QED_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki_qp[%
      @else %]
         nlo_coupling = [% QED_COUPLING_NAME %]*[% QED_COUPLING_NAME %][%
      @end @select %]
      end if

      if(debug_lo_diagrams .or. debug_nlo_diagrams) then
         call init_event(vecs)
         write(logfile,'(A7)') "<event>"
         call inspect_kinematics(logfile)
      end if

[% @if generate_tree_diagrams %]
      if (present(h)) then
         amp(1) = samplitudel0_h_qp(vecs, h)
      else
         amp(1)   = samplitudel0_qp(vecs)
      end if[%
      @else %]
      amp(1)   = 0.0_ki_qp[%
@end @if generate_tree_diagrams%][%
@if generate_loop_diagrams %][%
@if generate_counterterms %]
      if (renormalisation.eq.4) then
         ! massive quark counterterms only, OLD IMPLEMENTATION
         deltaOS = 1.0_ki_qp[%
@if use_MQSE %][% @else %]
         print *, "ERROR: Code generated with use_MQSE=false."
         print *, "Mass counterterms based on massive quark" 
         print *, "self-energies not available. Please choose"
         print *, "renormalisation != 3 or regenerate code with"
         print *, "use_MQSE=true. Execution terminates now."
         stop[% 
@end @if %]
      else 
         deltaOS = 0.0_ki_qp
      end if[%
@end @if generate_counterterms %]

      if (present(h)) then[%
         @if helsum %]
         print *, 'ERROR: Cannot select helicity when code was generated'
         print *, 'with "helsum=1".'[%
         @else %][%
         @if is_loopinduced %]
         amp((/4,3,2/)) = samplitudel1_h_qp(vecs, scale2, my_ok, rat2, h)/nlo_coupling/nlo_coupling[%
         @else %]
         amp((/4,3,2/)) = samplitudel1_h_qp(vecs, scale2, my_ok, rat2, h)/nlo_coupling[%
         @end @if %][%
         @end @if %]
      else[%
         @if is_loopinduced %]
         amp((/4,3,2/)) = samplitudel1_qp(vecs, scale2, my_ok, rat2)/nlo_coupling/nlo_coupling[%
         @else %]
         amp((/4,3,2/)) = samplitudel1_qp(vecs, scale2, my_ok, rat2)/nlo_coupling[%
         @end @if %]
      end if[%
@if generate_counterterms %]
      select case (renormalisation)
      case (0)
         ! no renormalisation
      case (1,2,3)
         ! fully renormalised (1), finite gamma5 renormalisation only (2) or massive quark counterterms only (2): 
         ! separation handled in ct_amplitude.f90 and function amplitude_Dym
         if (present(h)) then
            amp((/3,2/)) = amp((/3,2/)) + samplitudect_h_qp(vecs, renorm_logs, scale2, h)
         else
            amp((/3,2/)) = amp((/3,2/)) + samplitudect_qp(vecs, renorm_logs, scale2)
         end if
      case (4)
         ! massive quark counterterms only, OLD IMPLEMENTATION
      case default
         ! not implemented
         print*, "In [% process_name asprefix=\_ %]matrix:"
         print*, "  invalid value for renormalisation=", renormalisation
         stop
      end select[% 
@end @if generate_counterterms %][%
@if extension dred %]
      if (convert_to_thv) then
         ! Scheme conversion for infrared structure
         ! Reference:
         ! S. Catani, M. H. Seymour, Z. Trocsanyi,
         ! ``Regularisation scheme independence and unitarity
         !   in QCD cross-sections,''
         ! Phys.Rev. D 55 (1997) 6819
         ! arXiv:hep-ph/9610553
         amp(2) = amp(2) - amp(1) * (&
           &          num_light_quarks * 0.5_ki_qp * CF_qp &
           &        + num_gluons * 1.0_ki_qp/6.0_ki_qp * CA_qp)
      end if[%
@end @if extension dred %][%
@else %]
      amp(2:4) = 0.0_ki[%
@end @if generate_loop_diagrams%]

      if (present(ok)) ok = my_ok

      if(debug_lo_diagrams .or. debug_nlo_diagrams) then
         write(logfile,'(A25,E24.16,A3)') &
            & "<result kind='lo' value='", amp(1), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-finite' value='", amp(2), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-single' value='", amp(3), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-double' value='", amp(4), "'/>"
         if(my_ok) then
            write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
         else
            write(logfile,'(A29)') "<flag name='ok' status='no'/>"
         end if
         write(logfile,'(A8)') "</event>"
      end if[%
      @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]
      amp(1) = amp(1) * get_formfactor_lo(vecs)[%@end @if %][%
      @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
      amp(2:4) = amp(2:4) * get_formfactor_nlo(vecs)[%@end @if %][%
      @if generate_loop_diagrams %]
      select case(nlo_prefactors)
      case(0)
         ! The result is already in its desired form[%
      @if is_loopinduced %]
      case(1)
         ! loop-induced
         amp(2:4) = amp(2:4) * nlo_coupling * nlo_coupling
      case(2)
         ! loop-induced
         amp(2:4) = amp(2:4) * (nlo_coupling / 8.0_ki_qp / pi / pi)**2[%
      @else %]
      case(1)
         amp(2:4) = amp(2:4) * nlo_coupling
      case(2)
         amp(2:4) = amp(2:4) * nlo_coupling / 8.0_ki_qp / pi / pi[%
      @end @if %]
      end select[%@end @if %]
   end subroutine samplitudel01_qp
   !---#] subroutine samplitudel01_qp :

[% @for each 0 1 var=fh %]
   !---#[ function samplitudel0[% @select fh @case 1 %]_h[% @end @select %]_qp :
   function     samplitudel0[% @select fh @case 1 %]_h[% @end @select %]_qp(vecs[% @select fh @case 1 %], h[% @end @select %]) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: logfile
      use [% process_name asprefix=\_ %]kinematics_qp, only: init_event
      implicit none
      real(ki_qp), dimension([%num_legs%], 4), intent(in) :: vecs
      [% @select fh @case 1 %]integer, optional, intent(in) :: h
      [% @end @select 
      %]real(ki_qp) :: amp, heli_amp
      complex(ki_qp), dimension(numcs) :: color_vector[% @if enable_truncation_orders %]_0, color_vector_1, color_vector_2[% @end @if %]
      real(ki_qp), dimension([%num_legs%], 4) :: pvecs

      amp = 0.0_ki_qp[%
  @if generate_tree_diagrams %][%
  @select fh @case 1 %]
      select case (h)[% 
  @end @select %][%
  @for unique_helicity_mappings %][% 
  @select fh @case 0 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[%
  @end @select %][%
     @for current_helicities %][% 
  @select fh @case 1 %]
      case ([%helicity%])[% 
  @end @select %]
         if (debug_lo_diagrams) then
            write(logfile,*) "<helicity index='[% helicity %]' >"
         end if[% 
  @select fh @case 1 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[% 
  @end @select %][%
     @if enable_truncation_orders %]
         select case (EFTcount)
         ! amplitude*_0 -> SM
         ! amplitude*_1 -> dim-6 coefficient (NP=1) 
         ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)
         ! => "without loopcounting" means that the loop-supressed vertices
         !    are included despite their suppression!   
         case (0)
            ! sigma(SM X SM)
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            heli_amp = square_qp(color_vector_0)
         case (1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            color_vector_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = square_qp(color_vector_0) &
            & + square_qp(color_vector_0, color_vector_1 + color_vector_2)
         case (2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            color_vector_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = square_qp(color_vector_0 + color_vector_1 + color_vector_2)
         case (11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            heli_amp = square_qp(color_vector_0) &
            & + square_qp(color_vector_0, color_vector_1)
         case (12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            heli_amp = square_qp(color_vector_0 + color_vector_1)
         case (3)
            ! sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            color_vector_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = square_qp(color_vector_0, color_vector_1 + color_vector_2)
         case (4)
            ! sigma(dim6 X dim6)  without loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            color_vector_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = square_qp(color_vector_1 + color_vector_2)
         case (13)
            ! sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0_qp()
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            heli_amp = square_qp(color_vector_0, color_vector_1)
         case (14)
            ! sigma(dim6 X dim6)  with loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1_qp()
            heli_amp = square_qp(color_vector_1)
         end select[%
     @else %]
         color_vector = amplitude[% map.index %]l0_qp()
         heli_amp = square_qp(color_vector)[%
     @end @if %]
         if (debug_lo_diagrams) then
            write(logfile,'(A25,E24.16,A3)') &
                & "<result kind='lo' value='", heli_amp, "'/>"
            write(logfile,*) "</helicity>"
         end if
         amp = amp + heli_amp[%
  @end @for current_helicities %][%
  @end @for unique_helicity_mappings %][%
  @select fh @case 1 %]
      end select[% 
  @end @select %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki_qp)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki_qp)
      end if[%
   @end @if generate_tree_diagrams %]
   end function samplitudel0[% @select fh @case 1 %]_h[% @end @select %]_qp
   !---#] function samplitudel0[% @select fh @case 1 %]_h[% @end @select %]_qp :
   [% @end @for %][% 'fh = 0, 1 loop' %]

   [% @if generate_counterterms %][% 
@for each 0 1 var=fh %]
      !---#[ function samplitudect[% @select fh @case 1 %]_h[% @end @select %]_qp :
      function     samplitudect[% @select fh @case 1 %]_h[% @end @select %]_qp(vecs, logs, scale2[% @select fh @case 1 %], h[% @end @select %]) result(amp)
         use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: logfile
         use [% process_name asprefix=\_ %]kinematics_qp, only: init_event
         implicit none
         real(ki_qp), dimension([%num_legs%], 4), intent(in) :: vecs
         [% @select fh @case 1 %]integer, optional, intent(in) :: h
         [% @end @select 
         %]real(ki_qp), dimension(-1:0) :: amp, heli_amp
         complex(ki_qp), dimension(numcs) :: amp0[% @if enable_truncation_orders %]_0, amp0_1, amp0_2[% @end @if %]
         complex(ki_qp), dimension(-1:0,numcs) :: ampct[% @if enable_truncation_orders %]_0, ampct_1, ampct_2[% @end @if %]
         real(ki_qp), dimension([%num_legs%], 4) :: pvecs
         integer :: ieps
         real(ki_qp), intent(in) :: scale2
         logical, intent(in) :: logs
   
         amp = 0.0_ki_qp[%
   @if generate_tree_diagrams %][%
   @select fh @case 1 %]
         select case (h)[% 
   @end @select %][%
   @for unique_helicity_mappings %][% 
   @select fh @case 0 %]
          !---#[ reinitialize kinematics:[%
      @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
            pvecs([%index%],1) = vecs([%$_%],1)
            pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
            pvecs([%index%],1) = -vecs([%$_%],1)
            pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
            pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
            pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
      @end @for %]
            call init_event(pvecs[%
      @for particles lightlike vector %], [%hel%]1[%
      @end @for %])
            !---#] reinitialize kinematics:[%
  @end @select %][%
     @for current_helicities %][% 
  @select fh @case 1 %]
         case ([%helicity%])[% 
  @end @select %]        
            if (debug_lo_diagrams) then
               write(logfile,*) "<helicity index='[% helicity %]' >"
            end if[% 
  @select fh @case 1 %]
            !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
            pvecs([%index%],1) = vecs([%$_%],1)
            pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
            pvecs([%index%],1) = -vecs([%$_%],1)
            pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
            pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
            pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
            call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
            !---#] reinitialize kinematics:[%
  @end @select %][%
        @if enable_truncation_orders %]
            select case (EFTcount)
            ! amplitude*_0 -> SM
            ! amplitude*_1 -> dim-6 coefficient (NP=1) 
            ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)            
            ! => "without loopcounting" means that the loop-supressed vertices
            !    are included despite their suppression!
            case (0)
               ! sigma(SM X SM)
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0, ampct_0(ieps,:))
               end do
            case (1)
               ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               amp0_2 = amplitude[% map.index %]l0_2_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0, ampct_0(ieps,:) + ampct_1(ieps,:) + ampct_2(ieps,:)) &
                  & + square_qp(amp0_1 + amp0_2, ampct_0(ieps,:))
               end do
            case (2)
               ! sigma(SM + dim6 X SM + dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               amp0_2 = amplitude[% map.index %]l0_2_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0 + amp0_1 + amp0_2, ampct_0(ieps,:) + ampct_1(ieps,:) + ampct_2(ieps,:))
               end do
            case (11)
               ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0, ampct_0(ieps,:) + ampct_1(ieps,:)) &
                  & + square_qp(amp0_1, ampct_0(ieps,:))
               end do
            case (12)
               ! sigma(SM + dim6 X SM + dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0 + amp0_1, ampct_0(ieps,:) + ampct_1(ieps,:))
               end do
            case (3)
               ! sigma(SM X dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               amp0_2 = amplitude[% map.index %]l0_2_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0, ampct_1(ieps,:) + ampct_2(ieps,:)) &
                  & + square_qp(amp0_1 + amp0_2, ampct_0(ieps,:))
               end do
            case (4)
               ! sigma(dim6 X dim6)  without loopcounting
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               amp0_2 = amplitude[% map.index %]l0_2_qp()
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_1 + amp0_2, ampct_1(ieps,:) + ampct_2(ieps,:))
               end do
            case (13)
               ! sigma(SM X dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0_qp()
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               ampct_0 = ct_amplitude[% map.index %]_0_qp(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_0, ampct_1(ieps,:)) &
                  & + square_qp(amp0_1, ampct_0(ieps,:))
               end do
            case (14)
               ! sigma(dim6 X dim6)  with loopcounting
               amp0_1 = amplitude[% map.index %]l0_1_qp()
               ampct_1 = ct_amplitude[% map.index %]_1_qp(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square_qp(amp0_1, ampct_1(ieps,:))
               end do
            end select[%
        @else %]
            amp0 = amplitude[% map.index %]l0_qp()
            ampct = ct_amplitude[% map.index %]_qp(scale2)
            do ieps=-1,0
               heli_amp(ieps) = square_qp(amp0, ampct(ieps,:))
            end do[%
        @end @if %]
            if (debug_lo_diagrams) then
               write(logfile,'(A25,E24.16,A3)') &
                   & "<result kind='lo' value='", heli_amp, "'/>"
               write(logfile,*) "</helicity>"
            end if
            amp = amp + heli_amp[%
  @end @for current_helicities %][%
  @end @for unique_helicity_mappings %][%
  @select fh @case 1 %]
         end select[% 
  @end @select %]
         if (include_helicity_avg_factor) then
            amp = amp / real(in_helicities, ki_qp)
         end if
         if (include_color_avg_factor) then
            amp = amp / incolors
         end if
         if (include_symmetry_factor) then
            amp = amp / real(symmetry_factor, ki_qp)
         end if[%
      @end @if generate_tree_diagrams %]
      end function samplitudect[% @select fh @case 1 %]_h[% @end @select %]_qp
      !---#] function samplitudect[% @select fh @case 1 %]_h[% @end @select %]_qp :
   [% @end @for %][% 'fh = 0, 1 loop' 
   %][% @end @if generate_counterterms %]

   [% @for each 0 1 var=fh %]
   !---#[ function samplitudel1[% @select fh @case 1 %]_h[% @end @select %]_qp :
   function     samplitudel1[% @select fh @case 1 %]_h[% @end @select %]_qp(vecs,scale2,ok,rat2[% 
      @select fh @case 1 %][% @if helsum %][% @else %],h[% @end @if %][% @end @select %]) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & debug_nlo_diagrams, logfile, renorm_gamma5
      use [% process_name asprefix=\_ %]kinematics_qp, only: init_event
      implicit none
      real(ki_qp), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki_qp), intent(in) :: scale2
      real(ki_qp), intent(out) :: rat2[%
      @if helsum %][%
      @else %][% @select fh @case 1 %]
      integer, optional, intent(in) :: h[% 
      @end @select %]
      real(ki_qp), dimension([%num_legs%], 4) :: pvecs[%
      @end @if %]
      real(ki_qp), dimension(-2:0) :: amp, heli_amp[%
      @if generate_tree_diagrams %][%
      @if enable_truncation_orders %]
      complex(ki_qp), dimension(numcs) :: amp0_0, amp0_1, amp0_2[%
      @end @if %][%
      @else %][%
      @if enable_truncation_orders %]
      complex(ki_qp), dimension(numcs) :: amp0_2[%
      @end @if %]
      complex(ki_qp), dimension(numcs,-2:0) :: colorvec[% @if enable_truncation_orders %]_0, colorvec_1, colorvec_2[% @end @if %]
      integer :: c[%
      @end @if %]
      logical :: my_ok
      real(ki_qp) :: rational2

      amp(:) = 0.0_ki_qp
      rat2 = 0.0_ki_qp
      ok = .true.[%
   @if generate_loop_diagrams%][%
   @if helsum %]
      if(debug_nlo_diagrams) then
         write(logfile,*) "<helicity index='sum'>"
      end if
      call init_event(vecs)[%
      @if generate_tree_diagrams %][% '=> not loop-induced' %]
      heli_amp = samplitudel1summed_qp(real(scale2,ki_qp),my_ok,rational2)[%
      @else %][% '=> loop-induced' %]
      do c=1,numcs
         colorvec(c,:) = samplitudel1summed_qp(real(scale2,ki_qp),my_ok,rational2,c)
      end do
      heli_amp( 0) = square_qp(colorvec(:, 0))
      heli_amp(-1) = square_qp(colorvec(:,-1), colorvec(:, 0))
      heli_amp(-2) = square_qp(colorvec(:,-2), colorvec(:, 0)) + square_qp(colorvec(:, -1))[%
      @end @if %]
      ok = ok .and. my_ok
      amp = amp + heli_amp
      rat2 = rat2 + rational2

      if(debug_nlo_diagrams) then
         write(logfile,'(A33,E24.16,A3)') &
              & "<result kind='nlo-finite' value='", heli_amp(0), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
              & "<result kind='nlo-single' value='", heli_amp(-1), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
              & "<result kind='nlo-double' value='", heli_amp(-2), "'/>"
         if(my_ok) then
            write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
            else
               write(logfile,'(A29)') "<flag name='ok' status='no'/>"
            end if
            write(logfile,*) "</helicity>"
         end if[%
   @else %][% 'if not helsum' %][%
  @select fh @case 1 %]
      select case (h)[% 
  @end @select %][%
  @for unique_helicity_mappings %][% 
  @select fh @case 0 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[% 
   @end @select %][%
     @if generate_tree_diagrams %][% '=> not loop-induced' %][%
     @for current_helicities %][% 
  @select fh @case 1 %]
      case ([%helicity%])[% 
  @end @select %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<helicity index='[% helicity %]'>"
         end if[% 
  @select fh @case 1 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[% 
  @end @select %][%
     @if enable_truncation_orders %]
         select case (EFTcount)
         ! amplitude*_0 -> SM
         ! amplitude*_1 -> dim-6 coefficient (NP=1) 
         ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)            
         ! => "without loopcounting" means that the loop-supressed vertices
         !    are included despite their suppression!   
         case(0)
            ! sigma(SM X SM)
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0)
         case(1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0) &
            &        + samplitudeh[% map.index %]l1_2_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0)
         case(2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_2_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1 + amp0_2)
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            ! ToDo: Normalisation factor of tree-diagram contribution
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0)
            heli_amp(0) = heli_amp(0) + square_qp(amp0_0, amp0_2) ! this is the contribution of tree diagrams with loop-order vertex
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            ! ToDo: Normalisation factor of tree-diagram contribution
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0 + amp0_1)
            heli_amp(0) = heli_amp(0) + square_qp(amp0_0 + amp0_1, amp0_2) ! this is the contribution of tree diagrams with loop-order vertex
         case(3)
            ! sigma(SM X dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0) &
            &        + samplitudeh[% map.index %]l1_2_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0)
         case(4)
            ! sigma(dim6 X dim6) without loopcounting
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_2_qp(real(scale2,ki_qp),my_ok,rational2,amp0_1 + amp0_2)
         case(13)
            ! sigma(SM X dim6) with loopcounting
            ! ToDo: Normalisation factor of tree-diagram contribution
            amp0_0 = amplitude[% map.index %]l0_0_qp()
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,amp0_1) &
            &        + samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_0)
            heli_amp(0) = heli_amp(0) + square_qp(amp0_0, amp0_2) ! this is the contribution of tree diagrams with loop-order vertex
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            ! ToDo: Normalisation factor of tree-diagram contribution
            amp0_1 = amplitude[% map.index %]l0_1_qp()
            amp0_2 = amplitude[% map.index %]l0_2_qp()
            heli_amp = samplitudeh[% map.index %]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,amp0_1)
            heli_amp(0) = heli_amp(0) + square_qp(amp0_1, amp0_2) ! this is the contribution of tree diagrams with loop-order vertex
         end select[%
     @else %][% 'if not enable_truncation_orders' %]
         heli_amp = samplitudeh[% map.index %]l1_qp(real(scale2,ki_qp),my_ok,rational2)[%
     @end @if enable_truncation_orders %]
     ok = ok .and. my_ok
     amp = amp + heli_amp
     rat2 = rat2 + rational2
     if(debug_nlo_diagrams) then
        write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-finite' value='", heli_amp(0), "'/>"
        write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-single' value='", heli_amp(-1), "'/>"
        write(logfile,'(A33,E24.16,A3)') &
            & "<result kind='nlo-double' value='", heli_amp(-2), "'/>"
        if(my_ok) then
           write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
        else
           write(logfile,'(A29)') "<flag name='ok' status='no'/>"
        end if
        write(logfile,*) "</helicity>"
     end if[%
     @end @for current_helicities %][%
      @else %][% 'if not generate_tree_diagrams' %][% '=> loop-induced' %][%
     @for current_helicities %][% 
  @select fh @case 1 %]
      case ([%helicity%])[% 
  @end @select %]
         if(debug_nlo_diagrams) then
            write(logfile,*) "<helicity index='[% helicity %]'>"
         end if[% 
  @select fh @case 1 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[% 
  @end @select %][%
      @if enable_truncation_orders %]
         select case (EFTcount)
         case(0)
            ! sigma(SM X SM)
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,c)
            end do
            heli_amp( 0) = square_qp(colorvec_0(:, 0))
            heli_amp(-1) = square_qp(colorvec_0(:,-1), colorvec_0(:, 0))
            heli_amp(-2) = square_qp(colorvec_0(:,-2), colorvec_0(:, 0)) + square_qp(colorvec_0(:, -1))
         case(1,2,3,4)
            ! Truncation options without loop-counting => cannot be defined unambiguously for loop-induced processes
            write(unit=*,fmt="(A56)") "EFTcount options 1, 2, 3 and 4 are not defined."
            write(unit=*,fmt="(A10,1x,I1,A44)") "You picked", EFTcount, ". Please choose 0, 11, 12, 13 or 14 instead."
            stop
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,c)
            end do
            heli_amp( 0) = square_qp(colorvec_0(:, 0)) + square_qp(colorvec_0(:, 0), colorvec_1(:, 0))
            heli_amp(-1) = square_qp(colorvec_0(:,-1), colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square_qp(colorvec_0(:, 0), colorvec_1(:,-1))
            heli_amp(-2) = square_qp(colorvec_0(:,-2), colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square_qp(colorvec_0(:, 0), colorvec_1(:,-2)) &
            &            + square_qp(colorvec_0(:, -1)) + square_qp(colorvec_0(:, -1), colorvec_1(:, -1))
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp( 0) = heli_amp( 0) + square_qp(colorvec_0(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square_qp(colorvec_0(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square_qp(colorvec_0(:,-2),amp0_2)
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,c)
            end do
            heli_amp( 0) = square_qp(colorvec_0(:, 0) + colorvec_1(:, 0))
            heli_amp(-1) = square_qp(colorvec_0(:,-1) + colorvec_1(:,-1), & 
            &                     colorvec_0(:, 0) + colorvec_1(:, 0))
            heli_amp(-2) = square_qp(colorvec_0(:,-2) + colorvec_1(:,-2), & 
            &                     colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square_qp(colorvec_0(:,-1) + colorvec_1(:,-1))
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()  
            heli_amp( 0) = heli_amp( 0) + square_qp(colorvec_0(:, 0),amp0_2) + square_qp(colorvec_1(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square_qp(colorvec_0(:,-1),amp0_2) + square_qp(colorvec_1(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square_qp(colorvec_0(:,-2),amp0_2) + square_qp(colorvec_1(:,-2),amp0_2)  
            heli_amp( 0) = heli_amp( 0) + square_qp(amp0_2)          
         case(13)
            ! sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0_qp(real(scale2,ki_qp),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,c)
            end do
            heli_amp( 0) = square_qp(colorvec_0(:, 0), colorvec_1(:, 0)) & 
            heli_amp(-1) = square_qp(colorvec_0(:,-1), colorvec_1(:, 0)) &
            &            + square_qp(colorvec_0(:, 0), colorvec_1(:,-1))
            heli_amp(-2) = square_qp(colorvec_0(:,-2), colorvec_1(:, 0)) &
            &            + square_qp(colorvec_0(:, 0), colorvec_1(:,-2)) &
            &            + square_qp(colorvec_0(:,-1), colorvec_1(:,-1))
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp( 0) = heli_amp( 0) + square_qp(colorvec_0(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square_qp(colorvec_0(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square_qp(colorvec_0(:,-2),amp0_2)
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            do c=1,numcs
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1_qp(real(scale2,ki_qp),my_ok,rational2,c)
            end do
           
            heli_amp( 0) = square_qp(colorvec_1(:, 0))
            heli_amp(-1) = square_qp(colorvec_1(:,-1), & 
            &                     colorvec_1(:, 0))
            heli_amp(-2) = square_qp(colorvec_1(:,-2), & 
            &                     colorvec_1(:, 0)) &
            &            + square_qp(colorvec_1(:,-1))
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp( 0) = heli_amp( 0) + square_qp(colorvec_1(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square_qp(colorvec_1(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square_qp(colorvec_1(:,-2),amp0_2)    
            heli_amp( 0) = heli_amp( 0) + square_qp(amp0_2)
         end select[%
      @else %][% 'if not enable_truncation_orders' %]
        do c=1,numcs
           colorvec(c,:) = samplitudeh[%map.index%]l1_qp(real(scale2,ki_qp),my_ok,rational2,c)
        end do
        heli_amp( 0) = square_qp(colorvec(:, 0))
        heli_amp(-1) = square_qp(colorvec(:,-1), colorvec(:, 0))
        heli_amp(-2) = square_qp(colorvec(:,-2), colorvec(:, 0)) + square_qp(colorvec(:, -1))[%
      @end @if enable_truncation_orders %]
      ok = ok .and. my_ok
      amp = amp + heli_amp
      rat2 = rat2 + rational2
      if(debug_nlo_diagrams) then
         write(logfile,'(A33,E24.16,A3)') &
             & "<result kind='nlo-finite' value='", heli_amp(0), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
             & "<result kind='nlo-single' value='", heli_amp(-1), "'/>"
         write(logfile,'(A33,E24.16,A3)') &
             & "<result kind='nlo-double' value='", heli_amp(-2), "'/>"
         if(my_ok) then
            write(logfile,'(A30)') "<flag name='ok' status='yes'/>"
         else
            write(logfile,'(A29)') "<flag name='ok' status='no'/>"
         end if
         write(logfile,*) "</helicity>"
      end if[%
      @end @for current_helicities %][%
      @end @if generate_tree_diagrams %][%
   @end @for unique_helicity_mappings %][%
  @select fh @case 1 %]
   end select[% 
  @end @select %][%
   @end @if helsum %][%
   @end @if generate_loop_diagrams %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki_qp)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki_qp)
      end if
   end function samplitudel1[% @select fh @case 1 %]_h[% @end @select %]_qp
   !---#] function samplitudel1[% @select fh @case 1 %]_h[% @end @select %]_qp :
[% @end @for %][% 'fh = 0, 1 loop' %]

[% @for each 0 1 var=fh %]
   !---#[ subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %]_qp :
   subroutine     ir_subtraction[% @select fh @case 1 %]_h[% @end @select %]_qp(vecs,scale2,amp,h)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & nlo_prefactors
      use [% process_name asprefix=\_ %]dipoles_qp, only: pi
      use [% process_name asprefix=\_ %]kinematics_qp, only: &
         & init_event, corrections_are_qcd
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model_qp
      implicit none
      real(ki_qp), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki_qp), intent(in) :: scale2
      integer, optional, intent(in) :: h
      real(ki_qp), dimension(2), intent(out) :: amp
      real(ki_qp), dimension(2) :: heli_amp
      real(ki_qp), dimension([%num_legs%], 4) :: pvecs
      complex(ki_qp), dimension(numcs,numcs,2) :: oper[%
@if enable_truncation_orders %]
      complex(ki_qp), dimension(numcs) :: color_vectorl0_0, color_vectorl0_1, color_vectorl0_2
      complex(ki_qp), dimension(numcs) :: pcolor_0, pcolor_1, pcolor_2[%
@else %]
      complex(ki_qp), dimension(numcs) :: color_vectorl0, pcolor[%
@end @if enable_truncation_orders %]
      real(ki_qp) :: nlo_coupling

      [% @select fh @case 0 %]
      if (present(h)) then
         call ir_subtraction_h_qp(vecs, scale2, amp, h)
         return 
      end if
      [% @end @select %]
      if(corrections_are_qcd) then[%
      @select QCD_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki_qp[%
      @else %]
         nlo_coupling = [% QCD_COUPLING_NAME %]*[% QCD_COUPLING_NAME %][%
      @end @select %]
      else[%
      @select QED_COUPLING_NAME
      @case 0 1 %]
         nlo_coupling = 1.0_ki_qp[%
      @else %]
         nlo_coupling = [% QED_COUPLING_NAME %]*[% QED_COUPLING_NAME %][%
      @end @select %]
      end if

      if (corrections_are_qcd) then
        oper = insertion_operator_qp(real(scale2,ki_qp), vecs)
      else
        oper = insertion_operator_qed_qp(real(scale2,ki_qp), vecs)
      endif
      amp(:) = 0.0_ki_qp[%
  @if generate_tree_diagrams %][%
  @select fh @case 1 %]
      select case (h)[% 
  @end @select %][%
  @for unique_helicity_mappings %][% 
  @select fh @case 0 %]
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[%
  @end @select %][%
     @for current_helicities %][% 
  @select fh @case 1 %]
      case ([%helicity%])
         !---#[ reinitialize kinematics:[%
     @for helicity_mapping shift=1 %][%
        @if parity %][%
           @select sign @case 1 %]
         pvecs([%index%],1) = vecs([%$_%],1)
         pvecs([%index%],2:4) = -vecs([%$_%],2:4)[%
           @else %]
         pvecs([%index%],1) = -vecs([%$_%],1)
         pvecs([%index%],2:4) = vecs([%$_%],2:4)[%
           @end @select %][%
        @else %][%
           @select sign @case 1 %]
         pvecs([%index%],:) = vecs([%$_%],:)[%
           @else %]
         pvecs([%index%],:) = -vecs([%$_%],:)[%
           @end @select %][%
        @end @if %][%
     @end @for %]
         call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
         !---#] reinitialize kinematics:[% 
  @end @select %][%
@if enable_truncation_orders %]
         select case (EFTcount)
         ! amplitude*_0 -> SM
         ! amplitude*_1 -> dim-6 coefficient (NP=1) 
         ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)
         ! => "without loopcounting" means that the loop-supressed vertices
         !    are included despite their suppression!
         case(0)
            ! sigma(SM X SM)
            pcolor_0 = amplitude[%map.index%]l0_0_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0, oper(:,:,1))
               heli_amp(2) = square_qp(color_vectorl0_0, oper(:,:,2))
            else
               heli_amp(1) = square_qp(color_vectorl0_0)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0)*oper(1,1,2)
            endif
         case(1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()
            pcolor_2 = amplitude[%map.index%]l0_2_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0, oper(:,:,1)) &
               & + square_qp(color_vectorl0_0, oper(:,:,1), color_vectorl0_1 + color_vectorl0_2)
               heli_amp(2) = square_qp(color_vectorl0_0, oper(:,:,2)) &
               & + square_qp(color_vectorl0_0, oper(:,:,2), color_vectorl0_1 + color_vectorl0_2)
            else
               heli_amp(1) = square_qp(color_vectorl0_0)*oper(1,1,1) &
               & + square_qp(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0)*oper(1,1,2) &
               & + square_qp(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()
            pcolor_2 = amplitude[%map.index%]l0_2_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2, oper(:,:,1))
               heli_amp(2) = square_qp(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2, oper(:,:,2))
            else
               heli_amp(1) = square_qp(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0, oper(:,:,1)) &
               & + square_qp(color_vectorl0_0, oper(:,:,1), color_vectorl0_1)
               heli_amp(2) = square_qp(color_vectorl0_0, oper(:,:,2)) &
               & + square_qp(color_vectorl0_0, oper(:,:,2), color_vectorl0_1)
            else
               heli_amp(1) = square_qp(color_vectorl0_0)*oper(1,1,1) &
               & + square_qp(color_vectorl0_0, color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0)*oper(1,1,2) &
               & + square_qp(color_vectorl0_0, color_vectorl0_1)*oper(1,1,2)
            endif
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0 + color_vectorl0_1, oper(:,:,1))
               heli_amp(2) = square_qp(color_vectorl0_0 + color_vectorl0_1, oper(:,:,2))
            else
               heli_amp(1) = square_qp(color_vectorl0_0 + color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0 + color_vectorl0_1)*oper(1,1,2)
            endif
         case(3)
            ! sigma(SM X dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()
            pcolor_2 = amplitude[%map.index%]l0_2_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0, oper(:,:,1), color_vectorl0_1 + color_vectorl0_2)
               heli_amp(2) = square_qp(color_vectorl0_0, oper(:,:,2), color_vectorl0_1 + color_vectorl0_2)
            else
               heli_amp(1) = square_qp(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(4)
            ! sigma(dim6 X dim6) without loopcounting
            pcolor_1 = amplitude[%map.index%]l0_1_qp()
            pcolor_2 = amplitude[%map.index%]l0_2_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_1 + color_vectorl0_2, oper(:,:,1))
               heli_amp(2) = square_qp(color_vectorl0_1 + color_vectorl0_2, oper(:,:,2))
            else
               heli_amp(1) = square_qp(color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(13)
            ! sigma(SM X dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0_qp()
            pcolor_1 = amplitude[%map.index%]l0_1_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_0, oper(:,:,1), color_vectorl0_1)
               heli_amp(2) = square_qp(color_vectorl0_0, oper(:,:,2), color_vectorl0_1)
            else
               heli_amp(1) = square_qp(color_vectorl0_0, color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_0, color_vectorl0_1)*oper(1,1,2)
            endif
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            pcolor_1 = amplitude[%map.index%]l0_1_qp()[%
     @for color_mapping shift=1%]
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square_qp(color_vectorl0_1, oper(:,:,1))
               heli_amp(2) = square_qp(color_vectorl0_1, oper(:,:,2))
            else
               heli_amp(1) = square_qp(color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square_qp(color_vectorl0_1)*oper(1,1,2)
            endif
         end select[%
@else %][% 'if not enable_truncation_orders' %]
         pcolor = amplitude[%map.index%]l0_qp()[%
     @for color_mapping shift=1%]
         color_vectorl0([% $_ %]) = pcolor([% index %])[%
     @end @for %]
         if (corrections_are_qcd) then
           heli_amp(1) = square_qp(color_vectorl0, oper(:,:,1))
           heli_amp(2) = square_qp(color_vectorl0, oper(:,:,2))
         else
           heli_amp(1) = square_qp(color_vectorl0)*oper(1,1,1)
           heli_amp(2) = square_qp(color_vectorl0)*oper(1,1,2)
         endif[%
@end @if enable_truncation_orders %]
         amp = amp + heli_amp[%
  @end @for current_helicities %][%
  @end @for unique_helicity_mappings %][%
  @select fh @case 1 %]
      end select[% 
  @end @select %][%
      @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
      amp = amp * get_formfactor_nlo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         amp = amp / real(in_helicities, ki_qp)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki_qp)
      end if[%
   @end @if %]
      select case(nlo_prefactors)
      case(0)
         ! The result is already in its desired form
      case(1)
         amp(:) = amp(:) * nlo_coupling
      case(2)
         amp(:) = amp(:) * nlo_coupling / 8.0_ki_qp / pi / pi
      end select
      
   end subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %]_qp
   !---#] subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %]_qp :
[% @end @for %][% 'fh = 0, 1 loop' %]

   [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]
   function get_formfactor_lo(vecs) result(factor)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model
      use [% process_name asprefix=\_ %]kinematics
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki) :: factor

      factor = [% form_factor_lo %]
   end function
   [% @end @if %]

   [% @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]
   function get_formfactor_nlo(vecs) result(factor)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model
      use [% process_name asprefix=\_ %]kinematics
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki) :: factor

      factor = [% form_factor_nlo %]
   end function
   [% @end @if %] 


   end module [% process_name asprefix=\_ %]matrix_qp
