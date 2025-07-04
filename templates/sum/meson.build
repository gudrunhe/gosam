generated_sources += [[%
@if generate_tree_diagrams %][%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %]
	'd[%$_%]l0.f90',[%
      @end @for %][%
   @end @if %][%
@end @if generate_tree_diagrams %][%
@if generate_loop_diagrams %][%
      @for elements topolopy.keep.virt %]
	'abbrevd[%$_%].f90',[%
      @end @for %][%
   @for elements topolopy.keep.virt %]
	'd[%$_%]l1.f90', 'd[%$_%]l1d.f90',%
      @if extension ninja %] 'd[%$_%]l131.f90', 'd[%$_%]l132.f90', 'd[%$_%]l121.f90',[%
      @end @if %][%
   @end @for %][%
@end @if generate_loop_diagrams %]]

[% process_name asprefix=\_ %]sum_gen = \
      custom_target('[% process_name asprefix=\_ %]sum_gen',
              output : generated_sources,
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()},
              depends: [[% @for helicities generated %] [% process_name asprefix=\_ %]helicity[% helicity %]_gen, [% @end @for helicities %]]
                )

[% process_name asprefix=\_ %]source += files(['globals.f90', 'amplitude.f90',[%
   @if extension golem95 %] 'golem95.f90',[%
   @end @if %][%
   @if extension ninja %] 'ninja.f90',[%
   @end @if %]])

[% process_name asprefix=\_ %]source += [% process_name asprefix=\_ %]sum_gen