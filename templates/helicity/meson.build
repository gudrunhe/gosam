generated_sources = [[%
@if enable_truncation_orders %][%
    @for each 0 1 2 var=efto %][%
        @if generate_lo_diagrams %][%
            @if group %]
	            'diagramsl0_[% efto %].f90',[%
            @else %][%
                @for elements topolopy.keep.tree %]
	                'd[%$_%]_[% efto %]h[%helicity%]l0.f90',[%
                @end @for %][%
            @end @if %][%
            @if internal REQUIRE_FR5 %][%
                @if group %]
	                'diagramsl0_[% efto %]fr5.f90',[%
                @else %][%
                    @for elements topolopy.keep.tree %]
	                    'd[%$_%]_[% efto %]h[%helicity%]l0fr5.f90',[%
                    @end @for %][%
                @end @if %][%
            @end @if %][%
        @end @if generate_lo_diagrams %][%
        @if generate_eft_counterterms %][%
        @if eval topolopy.count.ct .gt. 0 %][%
            @if group %]
	            'diagramsct_[% efto %].f90',[%
            @else %][%
                @for elements topolopy.keep.ct %]
	                'd[%$_%]_[% efto %]h[%helicity%]ct.f90',[%
                @end @for %][%
            @end @if %][%
            @if internal REQUIRE_FR5 %][%
                @if group %]
	                'diagramsct_[% efto %]fr5.f90',[%
                @else %][%
                    @for elements topolopy.keep.ct %]
	                    'd[%$_%]_[% efto %]h[%helicity%]ctfr5.f90',[%
                    @end @for %][%
                @end @if %][%
            @end @if %][% 
        @end @if %][%
        @end @if generate_eft_counterterms %][%
        @if helsum %][% @else %][%
            @if generate_nlo_virt %][%
                @select abbrev.level
                    @case helicity %]
                        'abbrevh[%helicity%].f90',[%
                    @case group %][%
                        @for groups var=grp %]
                            'abbrevg[%grp%]h[%helicity%].f90',[%
                        @end @for %][%
                    @case diagram %][%
                        @for elements topolopy.keep.virt %]
                            'abbrevd[%$_%]_[% efto %]h[%helicity%].f90',[%
                        @end @for %][%
                @end @select %][%
                @for elements topolopy.keep.virt %]
                    'd[%$_%]_[% efto %]h[%helicity%]l1.f90',[%
                    @if internal GENERATE_DERIVATIVES %] 'd[%$_%]_[% efto %]h[%helicity%]l1d.f90',[%
                    @end @if %][%
                    @if extension ninja %] 'd[%$_%]_[% efto %]h[%helicity%]l131.f90', 'd[%$_%]_[% efto %]h[%helicity%]l132.f90', 'd[%$_%]_[% efto %]h[%helicity%]l121.f90',[%
                    @end @if %][%
                @end @for %][%
            @end @if generate_nlo_virt %][%
        @end @if helsum %][%
    @end @for %][%
@else %][%
    @if generate_lo_diagrams %][%
        @if group %]
	        'diagramsl0.f90',[%
        @else %][%
            @for elements topolopy.keep.tree %]
	            'd[%$_%]h[%helicity%]l0.f90',[%
            @end @for %][%
        @end @if %][%
        @if internal REQUIRE_FR5 %][%
            @if group %]
	            'diagramsl0fr5.f90',[%
            @else %][%
                @for elements topolopy.keep.tree %]
                    'd[%$_%]h[%helicity%]l0fr5.f90',[%
                @end @for %][%
            @end @if %][%
        @end @if %][%
    @end @if generate_lo_diagrams %][%
    @if generate_eft_counterterms %][%
    @if eval topolopy.count.ct .gt. 0 %][%
        @if group %]
	        'diagramsct.f90',[%
        @else %][%
            @for elements topolopy.keep.ct %]
	            'd[%$_%]h[%helicity%]ct.f90',[%
            @end @for %][%
        @end @if %][%
        @if internal REQUIRE_FR5 %][%
            @if group %]
	            'diagramsctfr5.f90',[%
            @else %][%
                @for elements topolopy.keep.ct %]
                    'd[%$_%]h[%helicity%]ctfr5.f90',[%
                @end @for %][%
            @end @if %][%
        @end @if %][% 
    @end @if %][%
    @end @if generate_eft_counterterms %][%
    @if helsum %][% @else %][%
        @if generate_nlo_virt %][%
            @select abbrev.level
                @case helicity %]
	                'abbrevh[%helicity%].f90',[%
                @case group %][%
                    @for groups var=grp %]
	                    'abbrevg[%grp%]h[%helicity%].f90',[%
                    @end @for %][%
                @case diagram %][%
                    @for elements topolopy.keep.virt %]
	                    'abbrevd[%$_%]h[%helicity%].f90',[%
                    @end @for %][%
            @end @select %][%
            @for elements topolopy.keep.virt %]
                'd[%$_%]h[%helicity%]l1.f90',[%
                @if internal GENERATE_DERIVATIVES %] 'd[%$_%]h[%helicity%]l1d.f90',[%
                @end @if %][%
                @if extension ninja %] 'd[%$_%]h[%helicity%]l131.f90', 'd[%$_%]h[%helicity%]l132.f90', 'd[%$_%]h[%helicity%]l121.f90',[%
                @end @if %][%
            @end @for %][%
        @end @if generate_nlo_virt %][%
    @end @if helsum %][%
@end @if enable_truncation_orders %]]

[% process_name %]_helicity[%helicity%]_gen = \
      custom_target('[% process_name %]_helicity[%helicity%]_gen',
              output : generated_sources,
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

[% process_name %]_source += files(['globals.f90'])
[% process_name %]_source += files(['amplitudeh[%helicity%][% @if enable_truncation_orders %]_0.f90',
                     'amplitudeh[%helicity%]_1.f90',
                     'amplitudeh[%helicity%]_2[% @end @if %].f90'])
[% process_name %]_source += files([[%
@if enable_truncation_orders %][%
    @for each 0 1 2 var=efto %][%
        @if helsum%][% @else%][%
            @select r2 @case implicit explicit off %][%
                @if extension golem95 %] 'golem95_[% efto %]h[%helicity%].f90',[%
                @end @if %][%
                @if extension samurai %] 'samuraih[%helicity%].f90',[%
                @end @if %][%
                @if extension ninja %] 'ninja_[% efto %]h[%helicity%].f90',[%
                @end @if %][%
            @end @select %][%
        @end @if helsum %][%
    @end @for %][%
@else %][%
    @if helsum%][% @else %][%
        @select r2 @case implicit explicit off %][%
           @if extension golem95 %] 'golem95h[%helicity%].f90',[%
           @end @if %][%
           @if extension samurai %] 'samuraih[%helicity%].f90',[%
           @end @if %][%
           @if extension ninja %] 'ninjah[%helicity%].f90'[%
           @end @if %][%
        @end @select %][%
    @end @if helsum %][%
@end @if enable_truncation_orders %]])
[% process_name %]_source += [% process_name %]_helicity[%helicity%]_gen
