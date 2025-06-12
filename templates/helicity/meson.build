generated_sources = [[%
@if enable_truncation_orders %][%
    @for each 0 1 2 var=efto %][%
        @if generate_tree_diagrams %]
	            'diagramsl0_[% efto %].f90'[% @if extension quadruple%], 'diagramsl0_[% efto %]_qp.f90' [% @end @if %],[% 
        @end @if generate_tree_diagrams %][%
        @if generate_eft_counterterms %][%
        @if eval topolopy.count.ct .gt. 0 %]
	            'diagramsct_[% efto %].f90'[% @if extension quadruple%], 'diagramsct_[% efto %]_qp.f90' [% @end @if %],[% 
        @end @if %][%
        @end @if generate_eft_counterterms %][%
        @if helsum %][% @else %][%
            @if generate_loop_diagrams %][%
                        @for elements topolopy.keep.virt %]
                            'abbrevd[%$_%]_[% efto %]h[%helicity%].f90'[% @if extension quadruple%], 'abbrevd[%$_%]_[% efto %]h[%helicity%].f90' [% @end @if %],[%
                        @end @for %][%
                @for elements topolopy.keep.virt %]
                    'd[%$_%]_[% efto %]h[%helicity%]l1.f90'[% @if extension quadruple%], 'd[%$_%]_[% efto %]h[%helicity%]l1_qp.f90' [% @end @if %], 'd[%$_%]_[% efto %]h[%helicity%]l1d.f90'[% @if extension quadruple%], 'd[%$_%]_[% efto %]h[%helicity%]l1d_qp.f90' [% @end @if %],[%
                    @if extension ninja %] 'd[%$_%]_[% efto %]h[%helicity%]l131.f90', 'd[%$_%]_[% efto %]h[%helicity%]l132.f90', 'd[%$_%]_[% efto %]h[%helicity%]l121.f90'[%
                     @if extension quadruple%], 'd[%$_%]_[% efto %]h[%helicity%]l131_qp.f90', 'd[%$_%]_[% efto %]h[%helicity%]l132_qp.f90', 'd[%$_%]_[% efto %]h[%helicity%]l121_qp.f90' [% @end @if %],[%
                    @end @if %][%
                @end @for %][%
            @end @if generate_loop_diagrams %][%
        @end @if helsum %][%
    @end @for %][%
@else %][%
    @if generate_tree_diagrams %]
	        'diagramsl0.f90'[% @if extension quadruple%], 'diagramsl0_qp.f90' [% @end @if %],[% 
    @end @if generate_tree_diagrams %][%
    @if generate_eft_counterterms %][%
    @if eval topolopy.count.ct .gt. 0 %]
	        'diagramsct.f90'[% @if extension quadruple%], 'diagramsct_qp.f90' [% @end @if %],[% 
    @end @if %][%
    @end @if generate_eft_counterterms %][%
    @if helsum %][% @else %][%
        @if generate_loop_diagrams %][%
                    @for elements topolopy.keep.virt %]
	                    'abbrevd[%$_%]h[%helicity%].f90'[% @if extension quadruple%], 'abbrevd[%$_%]h[%helicity%]_qp.f90' [% @end @if %],[%
                    @end @for %][%
            @for elements topolopy.keep.virt %]
                'd[%$_%]h[%helicity%]l1.f90'[% @if extension quadruple%], 'd[%$_%]h[%helicity%]l1_qp.f90' [% @end @if %], 'd[%$_%]h[%helicity%]l1d.f90'[% @if extension quadruple%], 'd[%$_%]h[%helicity%]l1d_qp.f90' [% @end @if %],[%
                @if extension ninja %] 'd[%$_%]h[%helicity%]l131.f90', 'd[%$_%]h[%helicity%]l132.f90', 'd[%$_%]h[%helicity%]l121.f90'[%
                @if extension quadruple%], 'd[%$_%]h[%helicity%]l131_qp.f90', 'd[%$_%]h[%helicity%]l132_qp.f90', 'd[%$_%]h[%helicity%]l121_qp.f90' [% @end @if %],[%
                @end @if %][%
            @end @for %][%
        @end @if generate_loop_diagrams %][%
    @end @if helsum %][%
@end @if enable_truncation_orders %]]

[% process_name %]_helicity[%helicity%]_gen = \
      custom_target('[% process_name %]_helicity[%helicity%]_gen',
              output : generated_sources,
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

hel_gen_targets += [% process_name %]_helicity[%helicity%]_gen

[% process_name %]_source += files(['globals.f90'[% @if extension quadruple%], 'globals_qp.f90' [% @end @if %]])
[% process_name %]_source += files(['amplitudeh[%helicity%][% @if enable_truncation_orders %]_0.f90',
                     'amplitudeh[%helicity%]_1.f90',
                     'amplitudeh[%helicity%]_2[% @end @if %].f90', [% @if extension quadruple %]
                     'amplitudeh[%helicity%][% @if enable_truncation_orders %]_0_qp.f90',
                     'amplitudeh[%helicity%]_1_qp.f90',
                     'amplitudeh[%helicity%]_2[% @end @if %]_qp.f90', [% @end @if %][%
                     @if generate_counterterms %]
                     'ct_amplitudeh[%helicity%][% @if enable_truncation_orders %]_0.f90',
                     'ct_amplitudeh[%helicity%]_1.f90',
                     'ct_amplitudeh[%helicity%]_2[% @end @if %].f90'[% @if extension quadruple %],
                     'ct_amplitudeh[%helicity%][% @if enable_truncation_orders %]_0_qp.f90',
                     'ct_amplitudeh[%helicity%]_1_qp.f90',
                     'ct_amplitudeh[%helicity%]_2[% @end @if %]_qp.f90' [% @end @if %][% @end @if %]])
[% process_name %]_source += files([[%
@if enable_truncation_orders %][%
    @for each 0 1 2 var=efto %][%
        @if helsum%][% @else%][%
                @if extension golem95 %] 'golem95_[% efto %]h[%helicity%].f90',[%
                @end @if %][%
                @if extension ninja %] 'ninja_[% efto %]h[%helicity%].f90'[% @if extension quadruple%], 'ninja_[% efto %]h[%helicity%]_qp.f90' [% @end @if %],[%
                @end @if %][%
        @end @if helsum %][%
    @end @for %][%
@else %][%
    @if helsum%][% @else %][%
           @if extension golem95 %] 'golem95h[%helicity%].f90',[%
           @end @if %][%
           @if extension ninja %] 'ninjah[%helicity%].f90'[% @if extension quadruple%], 'ninjah[%helicity%]_qp.f90' [% @end @if %][%
           @end @if %][%
    @end @if helsum %][%
@end @if enable_truncation_orders %]])
[% process_name %]_source += [% process_name %]_helicity[%helicity%]_gen
