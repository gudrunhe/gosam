[% ' vim: syntax=golem '
%]module     [% process_name asprefix=\_ %]matrix_dp
   use [% process_name asprefix=\_ %]util, only: square
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: ki, &
     & include_helicity_avg_factor, include_color_avg_factor, &
     & debug_lo_diagrams, debug_nlo_diagrams, &
     & include_symmetry_factor, &
     & convert_to_thv, &
     & EFTcount
   use [% process_name asprefix=\_ %]kinematics, only: &
       in_helicities, symmetry_factor, num_legs, &
       corrections_are_qcd, num_light_quarks, num_gluons
   use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model, only: sqrt2
   use [% process_name asprefix=\_ %]color, only: CA, CF, numcs, incolors[%
   @if enable_truncation_orders %][%
   @for helicities generated %][%
      @if generate_tree_diagrams %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_0, only: amplitude[%helicity%]l0_0 => amplitude
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_1, only: amplitude[%helicity%]l0_1 => amplitude
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_2, only: amplitude[%helicity%]l0_2 => amplitude[%
      @end @if generate_tree_diagrams %][%
      @if generate_eft_loopind %]
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0_2, only: amplitude[%helicity%]l0_2 => amplitude[%
      @end @if generate_eft_loopind %][%
      @if generate_counterterms %]
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_0, only: ct_amplitude[%helicity%]_0 => amplitude
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_1, only: ct_amplitude[%helicity%]_1 => amplitude
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%]_2, only: ct_amplitude[%helicity%]_2 => amplitude[% 
      @end @if generate_counterterms %][%
   @if helsum %][% @else %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_0, [% ' '
        %]only: samplitudeh[%helicity%]l1_0 => samplitude
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_1, [% ' '
        %]only: samplitudeh[%helicity%]l1_1 => samplitude
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%]_2, [% ' '
        %]only: samplitudeh[%helicity%]l1_2 => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @for helicities generated %][%
   @if helsum %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
      %]amplitude_0, only: samplitudel1_0summed => samplitude
   use [% process_name asprefix=\_
      %]amplitude_1, only: samplitudel1_1summed => samplitude
   use [% process_name asprefix=\_
      %]amplitude_2, only: samplitudel1_2summed => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @else %][% ' not enable_truncation_orders ' %][%
   @for helicities generated %][%
      @if generate_tree_diagrams %]  
   use [% process_name asprefix=\_
        %]diagramsh[%helicity%]l0, only: amplitude[%helicity%]l0 => amplitude[%
      @end @if generate_tree_diagrams %][%
      @if generate_counterterms %]
   use [% process_name asprefix=\_
        %]ct_amplitudeh[%helicity%], only: ct_amplitude[%helicity%] => amplitude[% 
      @end @if generate_counterterms %][%
   @if helsum %][% @else %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
        %]amplitudeh[%helicity%], [% ' '
        %]only: samplitudeh[%helicity%]l1 => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @for helicities generated %][%
   @if helsum %][%
   @if generate_loop_diagrams %]
   use [% process_name asprefix=\_
      %]amplitude, only: samplitudel1summed => samplitude[%
   @end @if generate_loop_diagrams %][% 
   @end @if helsum%][%
   @end @if enable_truncation_orders %]
   use [% process_name asprefix=\_
      %]dipoles, only: insertion_operator, insertion_operator_qed

   implicit none
   save

   private

   public :: samplitudel01 
   public :: samplitudel0, samplitudel0_h 
   public :: samplitudel1, samplitudel1_h[%
@if generate_counterterms %]
   public :: samplitudect, samplitudect_h[%
@end @if %]
   public :: ir_subtraction, ir_subtraction_h
   public :: color_correlated_lo2, OLP_color_correlated
   public :: spin_correlated_lo2, spin_correlated_lo2_whizard, OLP_spin_correlated_lo2

[% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0  %]   private:: get_formfactor_lo [% @end @if %]
[% @if eval ( .len. ( .str. form_factor_nlo ) ) .gt. 0 %]   private:: get_formfactor_nlo [% @end @if %]

contains

   !---#[ subroutine samplitudel01 :
   subroutine samplitudel01(vecs, scale2, amp, rat2, ok, h)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & debug_lo_diagrams, debug_nlo_diagrams, logfile, deltaOS, &
         & renormalisation, renorm_logs, renorm_mqse, nlo_prefactors
      use [% process_name asprefix=\_ %]kinematics, only: &
         & inspect_kinematics, init_event
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model
      use [% process_name asprefix=\_ %]dipoles, only: pi
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      real(ki), dimension(4), intent(out) :: amp
      real(ki), intent(out) :: rat2
      logical, intent(out), optional :: ok
      integer, intent(in), optional :: h
      real(ki) :: nlo_coupling
      logical :: my_ok

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

      if(debug_lo_diagrams .or. debug_nlo_diagrams) then
         call init_event(vecs)
         write(logfile,'(A7)') "<event>"
         call inspect_kinematics(logfile)
      end if

[% @if generate_tree_diagrams %]
      if (present(h)) then
         amp(1) = samplitudel0_h(vecs, h)
      else
         amp(1)   = samplitudel0(vecs)
      end if[%
      @else %]
      amp(1)   = 0.0_ki[%
@end @if generate_tree_diagrams%][%
@if generate_loop_diagrams %][%
@if generate_counterterms %]
      if (renormalisation.eq.4) then
         ! massive quark counterterms only, OLD IMPLEMENTATION
         deltaOS = 1.0_ki[%
@if use_MQSE %][% @else %]
         print *, "ERROR: Code generated with use_MQSE=false."
         print *, "Mass counterterms based on massive quark" 
         print *, "self-energies not available. Please choose"
         print *, "renormalisation != 3 or regenerate code with"
         print *, "use_MQSE=true. Execution terminates now."
         stop[% 
@end @if %]
      else 
         deltaOS = 0.0_ki
      end if[%
@end @if generate_counterterms %]

      if (present(h)) then[%
         @if helsum %]
         print *, 'ERROR: Cannot select helicity when code was generated'
         print *, 'with "helsum=1".'[%
         @else %][%
         @if is_loopinduced %]
         amp((/4,3,2/)) = samplitudel1_h(vecs, scale2, my_ok, rat2, h)/nlo_coupling/nlo_coupling[%
         @else %]
         amp((/4,3,2/)) = samplitudel1_h(vecs, scale2, my_ok, rat2, h)/nlo_coupling[%
         @end @if %][%
         @end @if %]
      else[%
         @if is_loopinduced %]
         amp((/4,3,2/)) = samplitudel1(vecs, scale2, my_ok, rat2)/nlo_coupling/nlo_coupling[%
         @else %]
         amp((/4,3,2/)) = samplitudel1(vecs, scale2, my_ok, rat2)/nlo_coupling[%
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
            amp((/3,2/)) = amp((/3,2/)) + samplitudect_h(vecs, renorm_logs, scale2, h)
         else
            amp((/3,2/)) = amp((/3,2/)) + samplitudect(vecs, renorm_logs, scale2)
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
           &          num_light_quarks * 0.5_ki * CF &
           &        + num_gluons * 1.0_ki/6.0_ki * CA)
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
         amp(2:4) = amp(2:4) * (nlo_coupling / 8.0_ki / pi / pi)**2[%
      @else %]
      case(1)
         amp(2:4) = amp(2:4) * nlo_coupling
      case(2)
         amp(2:4) = amp(2:4) * nlo_coupling / 8.0_ki / pi / pi[%
      @end @if %]
      end select[% @end @if %]
   end subroutine samplitudel01
   !---#] subroutine samplitudel01 :

   [% @for each 0 1 var=fh %]
   !---#[ function samplitudel0[% @select fh @case 1 %]_h[% @end @select %] :
   function     samplitudel0[% @select fh @case 1 %]_h[% @end @select %](vecs[% @select fh @case 1 %], h[% @end @select %]) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: logfile
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      [% @select fh @case 1 %]integer, optional, intent(in) :: h
      [% @end @select 
      %]real(ki) :: amp, heli_amp
      complex(ki), dimension(numcs) :: color_vector[% @if enable_truncation_orders %]_0, color_vector_1, color_vector_2[% @end @if %]
      real(ki), dimension([%num_legs%], 4) :: pvecs

      amp = 0.0_ki[%
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
            color_vector_0 = amplitude[% map.index %]l0_0()
            heli_amp = square(color_vector_0)
         case (1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            heli_amp = square(color_vector_0) &
            & + square(color_vector_0, color_vector_1 + color_vector_2)
         case (2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            heli_amp = square(color_vector_0 + color_vector_1 + color_vector_2)
         case (11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            heli_amp = square(color_vector_0) &
            & + square(color_vector_0, color_vector_1)
         case (12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            heli_amp = square(color_vector_0 + color_vector_1)
         case (3)
            ! sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            heli_amp = square(color_vector_0, color_vector_1 + color_vector_2)
         case (4)
            ! sigma(dim6 X dim6)  without loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            heli_amp = square(color_vector_1 + color_vector_2)
         case (13)
            ! sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            heli_amp = square(color_vector_0, color_vector_1)
         case (14)
            ! sigma(dim6 X dim6)  with loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1()
            heli_amp = square(color_vector_1)
         end select[%
     @else %]
         color_vector = amplitude[% map.index %]l0()
         heli_amp = square(color_vector)[%
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
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if[%
   @end @if generate_tree_diagrams %]
   end function samplitudel0[% @select fh @case 1 %]_h[% @end @select %]
   !---#] function samplitudel0[% @select fh @case 1 %]_h[% @end @select %] :
   [% @end @for %][% 'fh = 0, 1 loop' %]

   [% @if generate_counterterms %][% 
@for each 0 1 var=fh %]
      !---#[ function samplitudect[% @select fh @case 1 %]_h[% @end @select %] :
      function     samplitudect[% @select fh @case 1 %]_h[% @end @select %](vecs, logs, scale2[% @select fh @case 1 %], h[% @end @select %]) result(amp)
         use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: logfile
         use [% process_name asprefix=\_ %]kinematics, only: init_event
         implicit none
         real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
         [% @select fh @case 1 %]integer, optional, intent(in) :: h
         [% @end @select 
         %]real(ki), dimension(-1:0) :: amp, heli_amp
         complex(ki), dimension(numcs) :: amp0[% @if enable_truncation_orders %]_0, amp0_1, amp0_2[% @end @if %]
         complex(ki), dimension(-1:0,numcs) :: ampct[% @if enable_truncation_orders %]_0, ampct_1, ampct_2[% @end @if %]
         real(ki), dimension([%num_legs%], 4) :: pvecs
         integer :: ieps
         real(ki), intent(in) :: scale2
         logical, intent(in) :: logs
   
         amp = 0.0_ki[%
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
               amp0_0 = amplitude[% map.index %]l0_0()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0, ampct_0(ieps,:))
               end do
            case (1)
               ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               amp0_2 = amplitude[% map.index %]l0_2()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0, ampct_0(ieps,:) + ampct_1(ieps,:) + ampct_2(ieps,:)) &
                  & + square(amp0_1 + amp0_2, ampct_0(ieps,:))
               end do
            case (2)
               ! sigma(SM + dim6 X SM + dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               amp0_2 = amplitude[% map.index %]l0_2()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0 + amp0_1 + amp0_2, ampct_0(ieps,:) + ampct_1(ieps,:) + ampct_2(ieps,:))
               end do
            case (11)
               ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0, ampct_0(ieps,:) + ampct_1(ieps,:)) &
                  & + square(amp0_1, ampct_0(ieps,:))
               end do
            case (12)
               ! sigma(SM + dim6 X SM + dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0 + amp0_1, ampct_0(ieps,:) + ampct_1(ieps,:))
               end do
            case (3)
               ! sigma(SM X dim6) without loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               amp0_2 = amplitude[% map.index %]l0_2()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0, ampct_1(ieps,:) + ampct_2(ieps,:)) &
                  & + square(amp0_1 + amp0_2, ampct_0(ieps,:))
               end do
            case (4)
               ! sigma(dim6 X dim6)  without loopcounting
               amp0_1 = amplitude[% map.index %]l0_1()
               amp0_2 = amplitude[% map.index %]l0_2()
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               ampct_2 = ct_amplitude[% map.index %]_2(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_1 + amp0_2, ampct_1(ieps,:) + ampct_2(ieps,:))
               end do
            case (13)
               ! sigma(SM X dim6) with loopcounting
               amp0_0 = amplitude[% map.index %]l0_0()
               amp0_1 = amplitude[% map.index %]l0_1()
               ampct_0 = ct_amplitude[% map.index %]_0(scale2)
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_0, ampct_1(ieps,:)) &
                  & + square(amp0_1, ampct_0(ieps,:))
               end do
            case (14)
               ! sigma(dim6 X dim6)  with loopcounting
               amp0_1 = amplitude[% map.index %]l0_1()
               ampct_1 = ct_amplitude[% map.index %]_1(scale2)
               do ieps=-1,0
                  heli_amp(ieps) = square(amp0_1, ampct_1(ieps,:))
               end do
            end select[%
        @else %]
            amp0 = amplitude[% map.index %]l0()
            ampct = ct_amplitude[% map.index %](scale2)
            do ieps=-1,0
               heli_amp(ieps) = square(amp0, ampct(ieps,:))
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
            amp = amp / real(in_helicities, ki)
         end if
         if (include_color_avg_factor) then
            amp = amp / incolors
         end if
         if (include_symmetry_factor) then
            amp = amp / real(symmetry_factor, ki)
         end if[%
      @end @if generate_tree_diagrams %]
      end function samplitudect[% @select fh @case 1 %]_h[% @end @select %]
      !---#] function samplitudect[% @select fh @case 1 %]_h[% @end @select %] :
   [% @end @for %][% 'fh = 0, 1 loop' 
   %][% @end @if generate_counterterms %]

   [% @for each 0 1 var=fh %]
   !---#[ function samplitudel1[% @select fh @case 1 %]_h[% @end @select %] :
   function     samplitudel1[% @select fh @case 1 %]_h[% @end @select %](vecs,scale2,ok,rat2[% 
      @select fh @case 1 %][% @if helsum %][% @else %],h[% @end @if %][% @end @select %]) result(amp)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & debug_nlo_diagrams, logfile, renorm_gamma5
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      use [% process_name asprefix=\_ %]dipoles, only: pi
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      logical, intent(out) :: ok
      real(ki), intent(in) :: scale2
      real(ki), intent(out) :: rat2[%
      @if helsum %][%
      @else %][% @select fh @case 1 %]
      integer, optional, intent(in) :: h[% 
      @end @select %]
      real(ki), dimension([%num_legs%], 4) :: pvecs[%
      @end @if %]
      real(ki), dimension(-2:0) :: amp, heli_amp[%
      @if generate_tree_diagrams %][%
      @if enable_truncation_orders %]
      complex(ki), dimension(numcs) :: amp0_0, amp0_1, amp0_2[%
      @end @if %][%
      @else %][%
      @if enable_truncation_orders %]
      complex(ki), dimension(numcs) :: amp0_2[%
      @end @if %]
      complex(ki), dimension(numcs,-2:0) :: colorvec[% @if enable_truncation_orders %]_0, colorvec_1, colorvec_2[% @end @if %]
      integer :: c[%
      @end @if %]
      logical :: my_ok
      real(ki) :: rational2

      amp(:) = 0.0_ki
      rat2 = 0.0_ki
      ok = .true.[%
   @if generate_loop_diagrams%][%
   @if helsum %]
      if(debug_nlo_diagrams) then
         write(logfile,*) "<helicity index='sum'>"
      end if
      call init_event(vecs)[%
      @if generate_tree_diagrams %][% '=> not loop-induced' %]
      heli_amp = samplitudel1summed(real(scale2,ki),my_ok,rational2)[%
      @else %][% '=> loop-induced' %]
      do c=1,numcs
         colorvec(c,:) = samplitudel1summed(real(scale2,ki),my_ok,rational2,c)
      end do
      heli_amp( 0) = square(colorvec(:, 0))
      heli_amp(-1) = square(colorvec(:,-1), colorvec(:, 0))
      heli_amp(-2) = square(colorvec(:,-2), colorvec(:, 0)) + square(colorvec(:, -1))[%
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
            amp0_0 = amplitude[% map.index %]l0_0()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_0)
         case(1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0) &
            &        + samplitudeh[% map.index %]l1_2(real(scale2,ki),my_ok,rational2,amp0_0)
         case(2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_2(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1 + amp0_2)
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0)
            ! this is the contribution of tree diagrams with loop-order vertex, compensate for LO vs NLO prefactor
            heli_amp(0) = heli_amp(0) + square(amp0_0, amp0_2)*8._ki*pi*pi
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0 + amp0_1)
            ! this is the contribution of tree diagrams with loop-order vertex, compensate for LO vs NLO prefactor
            heli_amp(0) = heli_amp(0) + square(amp0_0 + amp0_1, amp0_2)*8._ki*pi*pi
         case(3)
            ! sigma(SM X dim6) without loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0) &
            &        + samplitudeh[% map.index %]l1_2(real(scale2,ki),my_ok,rational2,amp0_0)
         case(4)
            ! sigma(dim6 X dim6) without loopcounting
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_1 + amp0_2) &
            &        + samplitudeh[% map.index %]l1_2(real(scale2,ki),my_ok,rational2,amp0_1 + amp0_2)
         case(13)
            ! sigma(SM X dim6) with loopcounting
            amp0_0 = amplitude[% map.index %]l0_0()
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_0(real(scale2,ki),my_ok,rational2,amp0_1) &
            &        + samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_0)
            ! this is the contribution of tree diagrams with loop-order vertex, compensate for LO vs NLO prefactor
            heli_amp(0) = heli_amp(0) + square(amp0_0, amp0_2)*8._ki*pi*pi 
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            amp0_1 = amplitude[% map.index %]l0_1()
            amp0_2 = amplitude[% map.index %]l0_2()
            heli_amp = samplitudeh[% map.index %]l1_1(real(scale2,ki),my_ok,rational2,amp0_1)
            ! this is the contribution of tree diagrams with loop-order vertex, compensate for LO vs NLO prefactor
            heli_amp(0) = heli_amp(0) + square(amp0_1, amp0_2)*8._ki*pi*pi
         end select[%
     @else %][% 'if not enable_truncation_orders' %]
         heli_amp = samplitudeh[% map.index %]l1(real(scale2,ki),my_ok,rational2)[%
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
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
            end do
            heli_amp( 0) = square(colorvec_0(:, 0))
            heli_amp(-1) = square(colorvec_0(:,-1), colorvec_0(:, 0))
            heli_amp(-2) = square(colorvec_0(:,-2), colorvec_0(:, 0)) + square(colorvec_0(:, -1))
         case(1,2,3,4)
            ! Truncation options without loop-counting => cannot be defined unambiguously for loop-induced processes
            write(unit=*,fmt="(A74)") "EFTcount options 1, 2, 3 and 4 are not defined for loop-induced processes."
            write(unit=*,fmt="(A10,1x,I1,A44)") "You picked", EFTcount, ". Please choose 0, 11, 12, 13 or 14 instead."
            stop
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            heli_amp( 0) = square(colorvec_0(:, 0)) + square(colorvec_0(:, 0), colorvec_1(:, 0))
            heli_amp(-1) = square(colorvec_0(:,-1), colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square(colorvec_0(:, 0), colorvec_1(:,-1))
            heli_amp(-2) = square(colorvec_0(:,-2), colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square(colorvec_0(:, 0), colorvec_1(:,-2)) &
            &            + square(colorvec_0(:, -1)) + square(colorvec_0(:, -1), colorvec_1(:, -1))[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi
            heli_amp( 0) = heli_amp( 0) + square(colorvec_0(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square(colorvec_0(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square(colorvec_0(:,-2),amp0_2)[% 
@end @if %]
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            heli_amp( 0) = square(colorvec_0(:, 0) + colorvec_1(:, 0))
            heli_amp(-1) = square(colorvec_0(:,-1) + colorvec_1(:,-1), & 
            &                     colorvec_0(:, 0) + colorvec_1(:, 0))
            heli_amp(-2) = square(colorvec_0(:,-2) + colorvec_1(:,-2), & 
            &                     colorvec_0(:, 0) + colorvec_1(:, 0)) &
            &            + square(colorvec_0(:,-1) + colorvec_1(:,-1))[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi
            heli_amp( 0) = heli_amp( 0) + square(colorvec_0(:, 0),amp0_2) + square(colorvec_1(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square(colorvec_0(:,-1),amp0_2) + square(colorvec_1(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square(colorvec_0(:,-2),amp0_2) + square(colorvec_1(:,-2),amp0_2)  
            heli_amp( 0) = heli_amp( 0) + square(amp0_2)[% 
@end @if %]
         case(13)
            ! sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            heli_amp( 0) = square(colorvec_0(:, 0), colorvec_1(:, 0))
            heli_amp(-1) = square(colorvec_0(:,-1), colorvec_1(:, 0)) &
            &            + square(colorvec_0(:, 0), colorvec_1(:,-1))
            heli_amp(-2) = square(colorvec_0(:,-2), colorvec_1(:, 0)) &
            &            + square(colorvec_0(:, 0), colorvec_1(:,-2)) &
            &            + square(colorvec_0(:,-1), colorvec_1(:,-1))[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi
            heli_amp( 0) = heli_amp( 0) + square(colorvec_0(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square(colorvec_0(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square(colorvec_0(:,-2),amp0_2)[% 
@end @if %]
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            do c=1,numcs
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do           
            heli_amp( 0) = square(colorvec_1(:, 0))
            heli_amp(-1) = square(colorvec_1(:,-1), & 
            &                     colorvec_1(:, 0))
            heli_amp(-2) = square(colorvec_1(:,-2), & 
            &                     colorvec_1(:, 0)) &
            &            + square(colorvec_1(:,-1))[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            amp0_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi
            heli_amp( 0) = heli_amp( 0) + square(colorvec_1(:, 0),amp0_2)
            heli_amp(-1) = heli_amp(-1) + square(colorvec_1(:,-1),amp0_2)
            heli_amp(-2) = heli_amp(-2) + square(colorvec_1(:,-2),amp0_2)    
            heli_amp( 0) = heli_amp( 0) + square(amp0_2)[% 
@end @if %]
         end select[%
      @else %][% 'if not enable_truncation_orders' %]
        do c=1,numcs
           colorvec(c,:) = samplitudeh[%map.index%]l1(real(scale2,ki),my_ok,rational2,c)
        end do
        heli_amp( 0) = square(colorvec(:, 0))
        heli_amp(-1) = square(colorvec(:,-1), colorvec(:, 0))
        heli_amp(-2) = square(colorvec(:,-2), colorvec(:, 0)) + square(colorvec(:, -1))[%
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
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if
   end function samplitudel1[% @select fh @case 1 %]_h[% @end @select %]
   !---#] function samplitudel1[% @select fh @case 1 %]_h[% @end @select %] :
[% @end @for %][% 'fh = 0, 1 loop' %]

[% @for each 0 1 var=fh %]
   !---#[ subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %] :
   subroutine     ir_subtraction[% @select fh @case 1 %]_h[% @end @select %](vecs,scale2,amp,h)
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]config, only: &
         & nlo_prefactors
      use [% process_name asprefix=\_ %]dipoles, only: pi
      use [% process_name asprefix=\_ %]kinematics, only: &
         & init_event, corrections_are_qcd
      use [% @if internal OLP_MODE %][% @else %][% process_name%]_[% @end @if %]model
      implicit none
      real(ki), dimension([%num_legs%], 4), intent(in) :: vecs
      real(ki), intent(in) :: scale2
      integer, optional, intent(in) :: h
      real(ki), dimension(2), intent(out) :: amp
      real(ki), dimension(2) :: heli_amp
      real(ki), dimension([%num_legs%], 4) :: pvecs
      complex(ki), dimension(numcs,numcs,2) :: oper[%
@if enable_truncation_orders %]
      complex(ki), dimension(numcs) :: color_vectorl0_0, color_vectorl0_1, color_vectorl0_2
      complex(ki), dimension(numcs) :: pcolor_0, pcolor_1, pcolor_2[%
@else %]
      complex(ki), dimension(numcs) :: color_vectorl0, pcolor[%
@end @if enable_truncation_orders %]
      real(ki) :: nlo_coupling

      [% @select fh @case 0 %]
      if (present(h)) then
         call ir_subtraction_h(vecs, scale2, amp, h)
         return 
      end if
      [% @end @select %]
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

      if (corrections_are_qcd) then
        oper = insertion_operator(real(scale2,ki), vecs)
      else
        oper = insertion_operator_qed(real(scale2,ki), vecs)
      endif
      amp(:) = 0.0_ki[%
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
            pcolor_0 = amplitude[%map.index%]l0_0()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0, oper(:,:,1))
               heli_amp(2) = square(color_vectorl0_0, oper(:,:,2))
            else
               heli_amp(1) = square(color_vectorl0_0)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0)*oper(1,1,2)
            endif
         case(1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()
            pcolor_2 = amplitude[%map.index%]l0_2()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0, oper(:,:,1)) &
               & + square(color_vectorl0_0, oper(:,:,1), color_vectorl0_1 + color_vectorl0_2)
               heli_amp(2) = square(color_vectorl0_0, oper(:,:,2)) &
               & + square(color_vectorl0_0, oper(:,:,2), color_vectorl0_1 + color_vectorl0_2)
            else
               heli_amp(1) = square(color_vectorl0_0)*oper(1,1,1) &
               & + square(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0)*oper(1,1,2) &
               & + square(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()
            pcolor_2 = amplitude[%map.index%]l0_2()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2, oper(:,:,1))
               heli_amp(2) = square(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2, oper(:,:,2))
            else
               heli_amp(1) = square(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0 + color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0, oper(:,:,1)) &
               & + square(color_vectorl0_0, oper(:,:,1), color_vectorl0_1)
               heli_amp(2) = square(color_vectorl0_0, oper(:,:,2)) &
               & + square(color_vectorl0_0, oper(:,:,2), color_vectorl0_1)
            else
               heli_amp(1) = square(color_vectorl0_0)*oper(1,1,1) &
               & + square(color_vectorl0_0, color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0)*oper(1,1,2) &
               & + square(color_vectorl0_0, color_vectorl0_1)*oper(1,1,2)
            endif
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0 + color_vectorl0_1, oper(:,:,1))
               heli_amp(2) = square(color_vectorl0_0 + color_vectorl0_1, oper(:,:,2))
            else
               heli_amp(1) = square(color_vectorl0_0 + color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0 + color_vectorl0_1)*oper(1,1,2)
            endif
         case(3)
            ! sigma(SM X dim6) without loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()
            pcolor_2 = amplitude[%map.index%]l0_2()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0, oper(:,:,1), color_vectorl0_1 + color_vectorl0_2)
               heli_amp(2) = square(color_vectorl0_0, oper(:,:,2), color_vectorl0_1 + color_vectorl0_2)
            else
               heli_amp(1) = square(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0, color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(4)
            ! sigma(dim6 X dim6) without loopcounting
            pcolor_1 = amplitude[%map.index%]l0_1()
            pcolor_2 = amplitude[%map.index%]l0_2()[%
     @for color_mapping shift=1%]
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])
            color_vectorl0_2([% $_ %]) = pcolor_2([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_1 + color_vectorl0_2, oper(:,:,1))
               heli_amp(2) = square(color_vectorl0_1 + color_vectorl0_2, oper(:,:,2))
            else
               heli_amp(1) = square(color_vectorl0_1 + color_vectorl0_2)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_1 + color_vectorl0_2)*oper(1,1,2)
            endif
         case(13)
            ! sigma(SM X dim6) with loopcounting
            pcolor_0 = amplitude[%map.index%]l0_0()
            pcolor_1 = amplitude[%map.index%]l0_1()[%
     @for color_mapping shift=1%]
            color_vectorl0_0([% $_ %]) = pcolor_0([% index %])
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_0, oper(:,:,1), color_vectorl0_1)
               heli_amp(2) = square(color_vectorl0_0, oper(:,:,2), color_vectorl0_1)
            else
               heli_amp(1) = square(color_vectorl0_0, color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_0, color_vectorl0_1)*oper(1,1,2)
            endif
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            pcolor_1 = amplitude[%map.index%]l0_1()[%
     @for color_mapping shift=1%]
            color_vectorl0_1([% $_ %]) = pcolor_1([% index %])[%
     @end @for %]
            if (corrections_are_qcd) then
               heli_amp(1) = square(color_vectorl0_1, oper(:,:,1))
               heli_amp(2) = square(color_vectorl0_1, oper(:,:,2))
            else
               heli_amp(1) = square(color_vectorl0_1)*oper(1,1,1)
               heli_amp(2) = square(color_vectorl0_1)*oper(1,1,2)
            endif
         end select[%
@else %][% 'if not enable_truncation_orders' %]
         pcolor = amplitude[%map.index%]l0()[%
     @for color_mapping shift=1%]
         color_vectorl0([% $_ %]) = pcolor([% index %])[%
     @end @for %]
         if (corrections_are_qcd) then
           heli_amp(1) = square(color_vectorl0, oper(:,:,1))
           heli_amp(2) = square(color_vectorl0, oper(:,:,2))
         else
           heli_amp(1) = square(color_vectorl0)*oper(1,1,1)
           heli_amp(2) = square(color_vectorl0)*oper(1,1,2)
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
         amp = amp / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         amp = amp / incolors
      end if
      if (include_symmetry_factor) then
         amp = amp / real(symmetry_factor, ki)
      end if[%
   @end @if %]
      select case(nlo_prefactors)
      case(0)
         ! The result is already in its desired form
      case(1)
         amp(:) = amp(:) * nlo_coupling
      case(2)
         amp(:) = amp(:) * nlo_coupling / 8.0_ki / pi / pi
      end select

   end subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %]
   !---#] subroutine ir_subtraction[% @select fh @case 1 %]_h[% @end @select %] :
[% @end @for %][% 'fh = 0, 1 loop' %]
   
   !---#[ color correlated ME :
   pure subroutine color_correlated_lo(color_vector,perm,res)
      use [% process_name asprefix=\_ %]color, only: [%
      @for pairs colored1 colored2 ordered %][%
      @if is_first %][% @else %], &
      & [% @end @if %]T[%index1%]T[%index2%][%
      @end @for pairs %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector
      integer, dimension(num_legs), intent(in) :: perm
      real(ki), dimension(num_legs,num_legs), intent(out) :: res
      res(:,:)=0.0_ki[%
      @for pairs colored1 colored2 ordered %]
      res(perm([%index1%]),perm([%index2%])) = square(color_vector,T[%
        index1%]T[%index2%])[%
      @if eval index1 .ne. index2 %]
      res(perm([%index2%]),perm([%index1%])) = res(perm([%index1%]),perm([%index2%]))[%
      @end @if %][%
      @end @for pairs %]
   end subroutine color_correlated_lo


   subroutine     color_correlated_lo2(vecs,borncc)
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,num_legs), intent(out) :: borncc
      real(ki), dimension(num_legs,num_legs) :: borncc_heli
      real(ki), dimension(num_legs, 4) :: pvecs
      integer, dimension(num_legs) :: perm
      complex(ki), dimension(numcs) :: color_vector
     
      borncc(:,:) = 0.0_ki
      
      [% @if enable_truncation_orders %]
      write(*,*) "color_correlated_lo2 not implemented yet for use with truncation options."
      stop[% 
      @else %][%
  @for repeat 1 num_legs inclusive=true %][%
     @if is_first %]
      perm = (/[%
     @else %],[%
     @end @if %][%$_%][%
     @if is_last %]/)[%
     @end @if %][%
  @end @for %][%
  @if generate_tree_diagrams %][% ' => not loop induced ' %][%
  @for helicities %]
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
     @end @for %][%
     @for helicity_mapping shift=1 %][%
        @if is_first %]
      perm = (/[%
        @else %],[%
        @end @if %][%$_%][%
        @if is_last %]/)[%
        @end @if %][%
     @end @for %]
      call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
      !---#] reinitialize kinematics:
      color_vector = amplitude[%map.index%]l0[% @if enable_truncation_orders %]_0[% @end @if %]()
      call color_correlated_lo(color_vector,perm,borncc_heli)[%
      @if is_first %]
      ! The minus is part in the definition according to PowHEG Box.
      ! Since they use it we include it:[%
      @end @if is_first %]
      borncc(:,:) = borncc(:,:) - borncc_heli(:,:)[%
  @end @for helicities %]
      if (include_helicity_avg_factor) then
         borncc = borncc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         borncc = borncc / incolors
      end if
      if (include_symmetry_factor) then
         borncc = borncc / real(symmetry_factor, ki)
      end if[% 
   @else %][% ' => loop induced ' %]
      write(*,*) "color_correlated_lo2 not implemented yet for loop-induced processes."
      stop[%
   @end @if generate_tree_diagrams %][% 
   @end @if enable_truncation_orders %]
   end subroutine color_correlated_lo2


   pure subroutine OLP_color_correlated_lo(color_vector1,perm,res,color_vector2)
      use [% process_name asprefix=\_ %]color, only: [%
      @for pairs colored1 colored2 ordered %][%
      @if is_first %][% @else %], &
      & [% @end @if %]T[%index1%]T[%index2%][%
      @end @for pairs %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1
      complex(ki), dimension(numcs), optional, intent(in) :: color_vector2
      integer, dimension(num_legs), intent(in) :: perm
      real(ki), dimension(num_legs*(num_legs-1)/2), intent(out) :: res
      real(ki), dimension(num_legs, num_legs) :: cij
      cij(:,:) = 0.0_ki
      if(present(color_vector2)) then[%
      @for pairs colored1 colored2 ordered %] [%
      @if eval index1 .ne. index2 %]
      cij(perm([%index1%]),perm([%index2%])) = square(color_vector1,T[%index1%]T[%index2%],color_vector2)
      cij(perm([%index2%]),perm([%index1%])) = cij(perm([%index1%]),perm([%index2%]))[%
      @end @if %] [%
      @end @for pairs %]      
      else[%
      @for pairs colored1 colored2 ordered %] [%
      @if eval index1 .ne. index2 %]
      cij(perm([%index1%]),perm([%index2%])) = square(color_vector1,T[%index1%]T[%index2%])
      cij(perm([%index2%]),perm([%index1%])) = cij(perm([%index1%]),perm([%index2%]))[%
      @end @if %] [%
      @end @for pairs %]
      end if
      res(:)=0.0_ki[%
      @for pairs colored1 colored2 ordered %] [%
      @if eval index1 .ne. index2 %]
      res([% eval index1 - 1 + ( index2 - 1 ) * ( index2 - 2 ) // 2 + 1 %]) = cij([%
        index1%],[%index2%])[%
      @end @if %] [%
      @end @for pairs %]
   end subroutine OLP_color_correlated_lo


   subroutine OLP_color_correlated(vecs,ampcc)
      use [% process_name asprefix=\_ %]kinematics, only: init_event
      use [% process_name asprefix=\_ %]dipoles, only: pi
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs*(num_legs-1)/2), intent(out) :: ampcc
      real(ki), dimension(num_legs,num_legs) :: borncc
      real(ki), dimension(num_legs*(num_legs-1)/2) :: ampcc_heli[%
      @if enable_truncation_orders %]
      real(ki), dimension(num_legs*(num_legs-1)/2) :: ampcc_heli_tmp1, ampcc_heli_tmp2[%
      @end @if %]
      real(ki), dimension(num_legs, 4) :: pvecs
      integer, dimension(num_legs) :: perm
      complex(ki), dimension(numcs) :: color_vector[% @if enable_truncation_orders %]_0, color_vector_1, color_vector_2[% @end @if %][%
      @if generate_tree_diagrams %][%
      @else %]
      complex(ki), dimension(numcs,-2:0) :: colorvec[% @if enable_truncation_orders %]_0, colorvec_1, colorvec_2[% @end @if %]
      integer :: c
      logical :: my_ok
      real(ki) :: rational2, scale2[%
      @end @if generate_tree_diagrams %]
      ampcc(:) = 0.0_ki[%
     @for repeat 1 num_legs inclusive=true %][%
        @if is_first %]
      perm = (/[%
        @else %],[%
        @end @if %][%$_%][%
        @if is_last %]/)[%
        @end @if %][%
     @end @for %][%
@if generate_tree_diagrams %][% ' => not loop-induced ' %][%
@for helicities %]
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
     @end @for %][%
     @for helicity_mapping shift=1 %][%
        @if is_first %]
      perm = (/[%
        @else %],[%
        @end @if %][%$_%][%
        @if is_last %]/)[%
        @end @if %][%
     @end @for %]
      call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
      !---#] reinitialize kinematics:[%
     @if enable_truncation_orders %]
         select case (EFTcount)
         ! amplitude*_0 -> SM
         ! amplitude*_1 -> dim-6 coefficient (NP=1) 
         ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)
         ! => "without loopcounting" means that the loop-supressed vertices
         !    are included despite their suppression!   
         case (0)
            ! sigma(SM X SM)
            color_vector_0 = amplitude[% map.index %]l0_0()
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case (1)
            ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1)
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp2,color_vector_1+color_vector_2)
            ampcc_heli = ampcc_heli_tmp1 + ampcc_heli_tmp2
         case(2)
            ! sigma(SM + dim6 X SM + dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            call OLP_color_correlated_lo(color_vector_0+color_vector_1+color_vector_2,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1)
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp2,color_vector_1)
            ampcc_heli = ampcc_heli_tmp1 + ampcc_heli_tmp2
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            call OLP_color_correlated_lo(color_vector_0+color_vector_1,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case (3)
            ! sigma(SM X dim6) without loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1,color_vector_1+color_vector_2)
            ampcc_heli = ampcc_heli_tmp1
         case(4)
            ! sigma(dim6 X dim6) without loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1()
            color_vector_2 = amplitude[% map.index %]l0_2()
            call OLP_color_correlated_lo(color_vector_1+color_vector_2,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case (13)
            ! sigma(SM X dim6) with loopcounting
            color_vector_0 = amplitude[% map.index %]l0_0()
            color_vector_1 = amplitude[% map.index %]l0_1()
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1,color_vector_1)
            ampcc_heli = ampcc_heli_tmp1
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            color_vector_1 = amplitude[% map.index %]l0_1()
            call OLP_color_correlated_lo(color_vector_1,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         end select[%
     @else %][% 'if not enable_truncation_orders' %]
         color_vector = amplitude[%map.index%]l0()
         call OLP_color_correlated_lo(color_vector,perm,ampcc_heli)[%
     @end @if enable_truncation_orders %]
         ampcc(:) = ampcc(:) + ampcc_heli(:)[%
@end @for helicities %][%
@else %][% ' not generate_tree_diagrams ' %][% ' => loop-induced ' %]
   ! For loop induced diagrams the scale should not matter
      scale2 = 100.0_ki[% 
@if helsum %][%
@if enable_truncation_orders %]
      write(*,*) "Subroutine 'OLP_color_correlated' including truncation options not available for processes generated with helsum=true."
      stop
[% @else %][% 'if not enable_truncation_orders' %]
      do c=1,numcs
         colorvec(c,:) = samplitudel1summed(real(scale2,ki),my_ok,rational2,c)
      end do
      color_vector = colorvec(:,0)
      call OLP_color_correlated_lo(color_vector,perm,ampcc)[%
@end @if enable_truncation_orders %][%
@else %][% ' not helsum ' %][%
@for helicities %]
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
     @end @for %][%
     @for helicity_mapping shift=1 %][%
        @if is_first %]
      perm = (/[%
        @else %],[%
        @end @if %][%$_%][%
        @if is_last %]/)[%
        @end @if %][%
     @end @for %]
      call init_event(pvecs[%
     @for particles lightlike vector %], [%hel%]1[%
     @end @for %])
      !---#] reinitialize kinematics:[%
     @if enable_truncation_orders %]
         select case (EFTcount)
         ! amplitude*_0 -> SM
         ! amplitude*_1 -> dim-6 coefficient (NP=1) 
         ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)
         ! => "without loopcounting" means that the loop-supressed vertices
         !    are included despite their suppression!   
         case (0)
            ! sigma(SM X SM)
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
            end do
            color_vector_0 = colorvec_0(:,0)
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case(1,2,3,4)
            ! Truncation options without loop-counting => cannot be defined unambiguously for loop-induced processes
            write(unit=*,fmt="(A74)") "EFTcount options 1, 2, 3 and 4 are not defined for loop-induced processes."
            write(unit=*,fmt="(A10,1x,I1,A44)") "You picked", EFTcount, ". Please choose 0, 11, 12, 13 or 14 instead."
            stop
         case(11)
            ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            color_vector_0 = colorvec_0(:,0)
            color_vector_1 = colorvec_1(:,0)[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            color_vector_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi[% 
@end @if %]
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1)
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp2,color_vector_1[% @if generate_eft_loopind %]+color_vector_2[% @end @if %])
            ampcc_heli = ampcc_heli_tmp1 + ampcc_heli_tmp2
         case(12)
            ! sigma(SM + dim6 X SM + dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            color_vector_0 = colorvec_0(:,0)
            color_vector_1 = colorvec_1(:,0)[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            color_vector_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi[% 
@end @if %]
            call OLP_color_correlated_lo(color_vector_0+color_vector_1[% @if generate_eft_loopind %]+color_vector_2[% @end @if %],perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         case (13)
            ! sigma(SM X dim6) with loopcounting
            do c=1,numcs
               colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            color_vector_0 = colorvec_0(:,0)
            color_vector_1 = colorvec_1(:,0)[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            color_vector_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi[% 
@end @if %]
            call OLP_color_correlated_lo(color_vector_0,perm,ampcc_heli_tmp1,color_vector_1[% @if generate_eft_loopind %]+color_vector_2[% @end @if %])
            ampcc_heli = ampcc_heli_tmp1
         case(14)
            ! sigma(dim6 X dim6) with loopcounting
            do c=1,numcs
               colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
            end do
            color_vector_1 = colorvec_1(:,0)[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            color_vector_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi[% 
@end @if %]
            call OLP_color_correlated_lo(color_vector_1[% @if generate_eft_loopind %]+color_vector_2[% @end @if %],perm,ampcc_heli_tmp1)
            ampcc_heli = ampcc_heli_tmp1
         end select[%
     @else %][% 'if not enable_truncation_orders' %]
      do c=1,numcs
         colorvec(c,:) = samplitudeh[%map.index%]l1(real(scale2,ki),my_ok,rational2,c)
      end do
      color_vector = colorvec(:,0)
      call OLP_color_correlated_lo(color_vector,perm,ampcc_heli)[%
     @end @if enable_truncation_orders %]
      ampcc(:) = ampcc(:) + ampcc_heli(:)[%
@end @for helicities %][% 
@end @if helsum%][%
@end @if generate_tree_diagrams %]
  [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]ampcc = ampcc*get_formfactor_lo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         ampcc = ampcc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         ampcc = ampcc / incolors
      end if
      if (include_symmetry_factor) then
         ampcc = ampcc / real(symmetry_factor, ki)
      end if

   end subroutine OLP_color_correlated
   !---#] color correlated ME :


   !---#[ spin correlated ME :
[% @for each 0 1 var=sct %]
   subroutine spin_correlated_lo2[% @select sct @case 1 %]_whizard[% @end @select %](vecs, bornsc)[% 
      @select sct @case 1 %]
     ! This is a version of the original spin_correlated_lo2, but using
     ! the OpenLoops (HELAS) convention for the polarization vectors.
     ! This is required by Whizard.[% 
      @end @select %]
      use [% process_name asprefix=\_ %]kinematics
      use [% process_name asprefix=\_ %]dipoles, only: pi
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(num_legs,4,4) :: bornsc
      real(ki), dimension(num_legs, 4) :: pvecs
      complex(ki), dimension(4,4) :: tens
      complex(ki) :: pp, pm, mp, mm[%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      complex(ki), dimension(numcs) :: heli_amp[%helicity%][% @if enable_truncation_orders %]_0, heli_amp[%helicity%]_1, heli_amp[%helicity%]_2[% @end @if %][%
         @end @for %][%
      @end @if is_first %]
      complex(ki), dimension(4) :: eps[%index%][% @select sct @case 1 %], epsp[%index%], epsm[%index%]
      complex(ki) :: phasefac[%index%][% @end @select %][%
   @end @for %][%
      @if generate_tree_diagrams %][%
      @else %]
      complex(ki), dimension(numcs,-2:0) :: colorvec[% @if enable_truncation_orders %]_0, colorvec_1, colorvec_2[% @end @if %]
      integer :: c
      logical :: my_ok
      real(ki) :: rational2, scale2[%
      @end @if generate_tree_diagrams %]

      bornsc(:,:,:) = 0.0_ki[% 
      @if generate_tree_diagrams %][% @else %][% @if helsum %]
         write(*,*) "spin_correlated_lo2[% @select sct @case 1 %]_whizard[% @end @select %] not implemented for loop-induced processes when helsum=true."
      stop[% 
      @end @if %][% @end @if %]

      !---#[ Initialize helicity amplitudes :[%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
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
@if generate_tree_diagrams %][% ' => not loop-induced ' %][%
      @if enable_truncation_orders %]
         heli_amp[%helicity%]_0 = amplitude[% map.index %]l0_0()
         heli_amp[%helicity%]_1 = amplitude[% map.index %]l0_1()
         heli_amp[%helicity%]_2 = amplitude[% map.index %]l0_2()[%
      @else %]
         heli_amp[%helicity%] = amplitude[% map.index %]l0()[%
      @end @if %][% 
@else %][% ' not generate_tree_diagrams => loop-induced' %]
         ! For loop induced diagrams the scale should not matter
         scale2 = 100.0_ki[%
      @if enable_truncation_orders %]
         do c=1,numcs
            colorvec_0(c,:) = samplitudeh[%map.index%]l1_0(real(scale2,ki),my_ok,rational2,c)
            colorvec_1(c,:) = samplitudeh[%map.index%]l1_1(real(scale2,ki),my_ok,rational2,c)
         end do
         heli_amp[%helicity%]_0 = colorvec_0(:,0)
         heli_amp[%helicity%]_1 = colorvec_1(:,0)[% 
@if generate_eft_loopind %]
            ! contributions of tree diagrams with loop-order vertex
            heli_amp[%helicity%]_2 = amplitude[% map.index %]l0_2()*8._ki*pi*pi[% 
@else %]
            heli_amp[%helicity%]_2 = 0._ki[% 
@end @if %][%
      @else %]
         do c=1,numcs
            colorvec(c,:) = samplitudeh[%map.index%]l1(real(scale2,ki),my_ok,rational2,c)
         end do
         heli_amp[%helicity%] = colorvec(:,0)[%
      @end @if enable_truncation_orders %][% 
@end @if generate_tree_diagrams %][%
         @end @for helicities %][%
      @end @if is_first %][%
   @end @for %]
      !---#] Initialize helicity amplitudes :
      !---#[ Initialize polarization vectors :[% 
   @select sct @case 1 %]
      ! Initializing the polarization vectors according to the OpenLoops
      ! convention as used by Whizard. Calculating the relative phasefactor
      ! accounting for the different conventions used for the helicity amplitudes.[% 
   @end @select %][%
   @for particles lightlike vector initial %]
      eps[%index%] = spva[% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %]k[%index%]/Spaa([% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %],k[%index%])/sqrt2[% 
   @select sct @case 1 %]
      call eps_MG(k[%index%], 0.0_ki, -1, epsm[%index%])
      call eps_MG(k[%index%], 0.0_ki, 1, epsp[%index%])
      phasefac[%index%] = (eps[%index%](2)-vecs([%index%],2)/vecs([%index%],1)*eps[%index%](1))/epsm[%index%](2)
      phasefac[%index%] = -phasefac[%index%]**2[% 
   @end @select %][%
   @end @for %][%
   @for particles lightlike vector final %]
      eps[%index%] = conjg(spva[%
      @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %]k[%index%]/Spaa([% @if eval reference > 0 %]k[%reference
		%][% @else %]l[% eval - reference %][% @end @if
                %],k[%index%])/sqrt2)[% 
   @select sct @case 1 %]
      call eps_MG(k[%index%], 0.0_ki, -1, epsm[%index%])
      call eps_MG(k[%index%], 0.0_ki, 1, epsp[%index%])
      phasefac[%index%] = (eps[%index%](2)-vecs([%index%],2)/vecs([%index%],1)*eps[%index%](1))/epsm[%index%](2)
      phasefac[%index%] = -phasefac[%index%]**2[% 
   @end @select %][%
   @end @for %]
      !---#] Initialize polarization vectors :
      ! Note: By omitting the imaginary parts we lose a term:
      !   Imag(B_j(mu,nu)) = i_ * e_(k_j, mu, q_j, nu) * |Born|^2
      ! where q_j is the reference momentum chosen for the paticle
      ! of momentum k_j. This term should, however not be phenomenologically
      ! relevant.[%
   @for particles lightlike vector %]
      !---#[ particle [%index%] :[%
   @if enable_truncation_orders %][%
@if generate_tree_diagrams %][% ' => not loop-induced ' %]
      select case (EFTcount)
      ! amplitude*_0 -> SM
      ! amplitude*_1 -> dim-6 coefficient (NP=1) 
      ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)   
      ! => "without loopcounting" means that the loop-supressed vertices
      !    are included despite their suppression! 
      case (0)
         ! sigma(SM X SM)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for helicities %]           
      case (1)
         ! sigma(SM X SM) + sigma(SM X dim6) without loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (2)
         ! sigma(SM + dim6 X SM + dim6) without loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
              &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
      case (11)
         ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (12)
         ! sigma(SM + dim6 X SM + dim6) with loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1,&
              &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1,&
         &                            heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1)[%
         @end @for helicities %]
      case (3)
         ! sigma(SM X dim6) without loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (4)
         ! sigma(dim6 X dim6) without loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
              &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,&
         &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
      case (13)
         ! sigma(SM X dim6) with loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (14)
         ! sigma(dim6 X dim6) with loopcounting
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_1)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%mhelicity%]_1)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1,heli_amp[%helicity%]_1)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1,heli_amp[%helicity%]_1)[%
         @end @for helicities %]
      end select[% 
@else %][% ' not generate_tree_diagrams => loop-induced' %]
      select case (EFTcount)
      ! amplitude*_0 -> SM
      ! amplitude*_1 -> dim-6 coefficient (NP=1) 
      ! amplitude*_2 -> dim-6 loop-suppressed coefficient (QL=1)   
      ! => "without loopcounting" means that the loop-supressed vertices
      !    are included despite their suppression! 
      case (0)
         ! sigma(SM X SM)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case(1,2,3,4)
            ! Truncation options without loop-counting => cannot be defined unambiguously for loop-induced processes
            write(unit=*,fmt="(A74)") "EFTcount options 1, 2, 3 and 4 are not defined for loop-induced processes."
            write(unit=*,fmt="(A10,1x,I1,A44)") "You picked", EFTcount, ". Please choose 0, 11, 12, 13 or 14 instead."
            stop
      case (11)
         ! sigma(SM X SM) + sigma(SM X dim6) with loopcounting
         ! Note: for loop-induced heli_amp_0 & heli_amp_1 = 1-loop amps, heli_amp_2 = tree (see above)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_0)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_0)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (12)
         ! sigma(SM + dim6 X SM + dim6) with loopcounting
         ! Note: for loop-induced heli_amp_0 & heli_amp_1 = 1-loop amps, heli_amp_2 = tree (see above)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
              &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0+heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%helicity%]_0+heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
      case (13)
         ! sigma(SM X dim6) with loopcounting
         ! Note: for loop-induced heli_amp_0 & heli_amp_1 = 1-loop amps, heli_amp_2 = tree (see above)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)&
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%mhelicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_0,heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)&
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,heli_amp[%helicity%]_0)[%
         @end @for helicities %]
      case (14)
         ! sigma(dim6 X dim6) with loopcounting
         ! Note: for loop-induced heli_amp_0 & heli_amp_1 = 1-loop amps, heli_amp_2 = tree (see above)
         pp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
              &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
              &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
         pm  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mp  = 0.0_ki[%
         @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
         symbol_plus=X symbol_minus=L var=mhelicity%] &
         &          + square_0l_0l_sc(heli_amp[%mhelicity%]_1+heli_amp[%mhelicity%]_2,&
         &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for modified_helicity %][%
         @end @for helicities %]
         mm  = 0.0_ki[%
         @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
         &          + square_0l_0l_sc(heli_amp[%helicity%]_1+heli_amp[%helicity%]_2,&
         &                            heli_amp[%helicity%]_1+heli_amp[%helicity%]_2)[%
         @end @for helicities %]
      end select[% 
@end @if generate_tree_diagrams %][%
   @else %][% 'if not enable_truncation_orders' %]
      pp  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %] &
      &          + square_0l_0l_sc(heli_amp[%helicity%],heli_amp[%helicity%])[%
      @end @for helicities %]
      pm  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
              symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_0l_0l_sc(heli_amp[%
                         helicity%],heli_amp[%mhelicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]
      mp  = 0.0_ki[%
      @for helicities where=index.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index to=L
                symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_0l_0l_sc(heli_amp[%
                          mhelicity%],heli_amp[%helicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]
      mm  = 0.0_ki[%
      @for helicities where=index.eq.L symbol_plus=X symbol_minus=L %] &
      &          + square_0l_0l_sc(heli_amp[%helicity%],heli_amp[%helicity%])[%
      @end @for helicities %][%
      @end @if enable_truncation_orders %]

      [% @select sct @case 0 %]
      call construct_polarization_tensor(conjg(eps[%index%]),eps[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pp, ki)
      call construct_polarization_tensor(conjg(eps[%index%]),conjg(eps[%index%]),tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pm, ki)
      call construct_polarization_tensor(eps[%index%],eps[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mp, ki)
      call construct_polarization_tensor(eps[%index%],conjg(eps[%index%]),tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mm, ki)
      [% @case 1 %]
      pm = phasefac[%index%]*pm
      mp = conjg(phasefac[%index%])*mp
      
      call construct_polarization_tensor(conjg(epsp[%index%]),epsp[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pp, ki)
      call construct_polarization_tensor(conjg(epsp[%index%]),epsm[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * pm, ki)
      call construct_polarization_tensor(conjg(epsm[%index%]),epsp[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mp, ki)
      call construct_polarization_tensor(conjg(epsm[%index%]),epsm[%index%],tens)
      bornsc([%index%],:,:) = bornsc([%index%],:,:) + real(tens(:,:) * mm, ki)[% 
      @end @select %]
      !---#] particle [%index%] :[%
   @end @for particles lightlike vector %]

      [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]bornsc = bornsc*get_formfactor_lo(vecs)[%@end @if %]
      if (include_helicity_avg_factor) then
         bornsc = bornsc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         bornsc = bornsc / incolors
      end if
      if (include_symmetry_factor) then
         bornsc = bornsc / real(symmetry_factor, ki)
      end if

   end subroutine spin_correlated_lo2[% @select sct @case 1 %]_whizard[% @end @select %]
[% @end @for %][% ' sct loop ' %]

   subroutine OLP_spin_correlated_lo2(vecs, ampsc)
      use [% process_name asprefix=\_ %]kinematics
      implicit none
      real(ki), dimension(num_legs, 4), intent(in) :: vecs
      real(ki), dimension(2*num_legs*num_legs) :: ampsc
      real(ki), dimension(num_legs, 4) :: pvecs
      integer :: i
      complex(ki) :: pm, mp[%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
      complex(ki), dimension(numcs) :: heli_amp[%helicity%][%
         @end @for %][%
      @end @if is_first %]
      complex(ki), dimension(4) :: eps[%index%][%
   @end @for %][%
@if generate_tree_diagrams %][%
@else %]
      complex(ki), dimension(numcs,-2:0) :: colorvec
      integer :: c
      logical :: my_ok
      real(ki) :: rational2, scale2[%
@end @if generate_tree_diagrams %]

      ampsc(:) = 0.0_ki

      [% @if enable_truncation_orders %]
      write(*,*) "OLP_spin_correlated_lo2 not implemented yet for use with truncation options."
      stop[% 
      @else %]

      !---#[ Initialize helicity amplitudes :[%
   @for particles lightlike vector %][%
      @if is_first %][%
         @for helicities %]
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
             @if generate_tree_diagrams %]
      heli_amp[%helicity%] = amplitude[% map.index %]l0()[%
             @else %]
      ! For loop induced diagrams the scale should not matter
      scale2 = 100.0_ki
      do c=1,numcs
         colorvec(c,:) = samplitudeh[%map.index%]l1(real(scale2,ki),my_ok,rational2,c)
      end do
      heli_amp[%helicity%] = colorvec(:, 0)[%
             @end @if generate_tree_diagrams %][%
         @end @for helicities %][%
      @end @if is_first %][%
   @end @for %]
      !---#] Initialize helicity amplitudes :

      [%
   @for pairs gluons1 colored2 %][%
     @if eval index1 .ne. index2 %]
      !---#[ pair [%index1%][%index2%] :

      mp  = 0.0_ki[%
      @for helicities where=index1.eq.X symbol_plus=X symbol_minus=L %][%
         @for modified_helicity modify=index1 to=L
                symbol_plus=X symbol_minus=L var=mhelicity%] &
      &          + square_[%index1%]_[%index2%]_sc(heli_amp[%
                          mhelicity%],heli_amp[%helicity%])[%
         @end @for modified_helicity %][%
      @end @for helicities %]

      ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs+1)   = ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs +1) + real(mp, ki)
      ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs+2) = ampsc(2*([%index1%]-1)+2*([%index2%]-1)*num_legs + 2)  + real(aimag(mp),ki)

      !---#] pair [%index1%][%index2%] :
     [% @end @if %] [%
   @end @for %]

      [% @if eval ( .len. ( .str. form_factor_lo ) ) .gt. 0 %]ampsc = ampsc * get_formfactor_lo(vecs)[%@end @if %]

      if (include_helicity_avg_factor) then
         ampsc = ampsc / real(in_helicities, ki)
      end if
      if (include_color_avg_factor) then
         ampsc = ampsc / incolors
      end if
      if (include_symmetry_factor) then
         ampsc = ampsc / real(symmetry_factor, ki)
      end if

      [% @end @if enable_truncation_orders %]

   end subroutine OLP_spin_correlated_lo2
   !---#] spin correlated ME :


   !---#[ construct polarisation tensor :
   pure subroutine construct_polarization_tensor(eps1, eps2, tens)
      implicit none
      complex(ki), dimension(0:3), intent(in) :: eps1, eps2
      complex(ki), dimension(0:3,0:3), intent(out) :: tens

      integer :: mu, nu

      do mu = 0,3
         do nu = 0, 3
            tens(mu,nu) = eps1(mu) * eps2(nu)
         end do
      end do
   end  subroutine construct_polarization_tensor
   !---#] construct polarisation tensor :

   
   !---#[ polarisation vectors in HELAS/MadGraph Konvention :
   ! Note: this subroutine is a (slightly modified) copy of wfIN_V_MG from
   ! OpenLoops2 ([1]: Eur. Phys. J. C 79 (2019) no.10, 866; arXiv:1907.13071 [hep-ph])
   ! See Appendix A.2 of [2]: KEK-91-11 (HELAS)
  pure subroutine eps_MG(P, M, POL, EPS)
     implicit none
     real(ki), intent(in)  :: P(0:3), M
     integer, intent(in)  :: POL
     complex(ki), intent(out) :: EPS(4)
     real(ki) :: P2_T, P_T, P_MOD
     complex(ki) :: ea(4), eb(4), epss(4)
     real(ki) :: small_real
     complex(ki) :: CI
     real(ki) :: sqrt05

     small_real = 1e-44_ki
     CI = (0.0_ki,1.0_ki)
     sqrt05 = 1.0_ki/sqrt(2.0_ki)
     
     P2_T  = P(1)*P(1) + P(2)*P(2)
     P_T   = sqrt(P2_T)
     P_MOD = sqrt(P2_T + P(3)*P(3))
    
     if (POL == -1 .or. POL == 1) then
       
       if (P_MOD == 0) then
          
          ea(1)   = 0
          ea(2)   = 1
          ea(3:4) = 0
          
          eb(1:2) = 0
          eb(3)   = 1
          eb(4)   = 0
          
       else if (P2_T == 0) then
          
          ea(1)   = 0
          ea(2)   = 1
          ea(3:4) = 0
          
          eb(1:2) = 0
          eb(3)   = P(3)/P_MOD
          eb(4)   = 0
          
       else
          
          ea(1)   =   0
          ea(2:3) =   P(1:2)*P(3)/(P_MOD*P_T)
          ea(4)   = - P_T/P_MOD
          
          eb(1) =   0
          eb(2) = - P(2)/P_T
          eb(3) =   P(1)/P_T
          eb(4) =   0
          
       end if

       ! Note: helicities swapped compared to original publication [2]
       if (POL == -1) then
          epss = - (ea + CI * eb) * sqrt05
       else if (POL == 1) then
          epss =   (ea - CI * eb) * sqrt05
       end if
       
     else if (POL == 0) then
       if (P_MOD == 0) then
          epss(1) =     0
          epss(2) =     0
          epss(3) =     0
          epss(4) =     1
       else
          epss(1) =     P_MOD / M
          epss(2) = P(1)*P(0) / (M*P_MOD)
          epss(3) = P(2)*P(0) / (M*P_MOD)
          epss(4) = P(3)*P(0) / (M*P_MOD)
       end if
     end if

     EPS(1) = epss(1)
     EPS(2) = epss(2)
     EPS(3) = epss(3)
     EPS(4) = epss(4)

     ! workaround (copied from OpenLoops. Doesn't hurt to have it here.)
     EPS = EPS + small_real
     
   end subroutine eps_MG
   !---#] polarisation vectors in HELAS/MadGraph Konvention :

   
   pure function square_0l_0l_sc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => CC
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1, color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector2)
      v2 = conjg(color_vector1)
      amp = sum(v1(:) * v2(:))
   end function  square_0l_0l_sc


   [% @for pairs gluons1 colored2 %][%
     @if eval index1 .ne. index2 %]
   pure function square_[%index1%]_[%index2%]_sc(color_vector1, color_vector2) result(amp)
      use [% process_name asprefix=\_ %]color, only: cmat => [%@if eval index1 < index2%]T[%index1%]T[%index2%]
      [% @else %]T[%index2%]T[%index1%]
      [% @end @if %]
      implicit none
      complex(ki), dimension(numcs), intent(in) :: color_vector1, color_vector2
      complex(ki) :: amp
      complex(ki), dimension(numcs) :: v1, v2

      v1 = matmul(cmat, color_vector2)
      v2 = conjg(color_vector1)
      amp = sum(v1(:) * v2(:))
   end function  square_[%index1%]_[%index2%]_sc
     [% @end @if %] [%
   @end @for %]

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

end module [% process_name asprefix=\_ %]matrix_dp
