generated_sources += [[%
@if generate_lo_diagrams %][%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %]
	'd[%$_%]l0.f90',[%
      @end @for %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if generate_nlo_virt %][%
      @for elements topolopy.keep.virt %]
	'abbrevd[%$_%].f90',[%
      @end @for %][%
   @for elements topolopy.keep.virt %]
	'd[%$_%]l1.f90',[%
      @if internal GENERATE_DERIVATIVES %] 'd[%$_%]l1d.f90',[%
      @end @if %][%
      @if extension ninja %] 'd[%$_%]l131.f90', 'd[%$_%]l132.f90', 'd[%$_%]l121.f90',[%
      @end @if %][%
   @end @for %][%
@end @if generate_nlo_virt %]]

[% process_name %]_sum_gen = \
      custom_target('[% process_name %]_sum_gen',
              output : generated_sources,
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()},
              depends: [[% @for helicities generated %] [% process_name %]_helicity[% helicity %]_gen, [% @end @for helicities %]]
                )

[% process_name %]_source += files(['globals.f90', 'amplitude.f90',[%
   @if extension golem95 %] 'golem95.f90',[%
   @end @if %][%
   @if extension ninja %] 'ninja.f90',[%
   @end @if %]])

[% process_name %]_source += [% process_name %]_sum_gen