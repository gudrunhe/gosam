[% @if internal OLP_MODE %][% @else %]
project('GoSam_Process_[% process_name %]', 'fortran', version:'1.0', meson_version: '>=0.57.0', default_options: ['buildtype=release'])

add_global_arguments('-w', language: 'fortran')
add_global_arguments('-ffree-line-length-none', language: 'fortran')
add_global_arguments('-march=[% meson.arch %]', language: 'fortran')
add_global_arguments([% @for options %extension%.fcflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %]  language: 'fortran')

add_global_link_arguments('-march=[% meson.arch %]', language: 'fortran')
add_global_link_arguments([% @for options %extension%.ldflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %] language: 'fortran')
[% @end @if %]

[% process_name %]_source = files([])
subdir('common')
subdir('doc')
[%
@for helicities generated %] 
subdir('helicity[% helicity %]')[%
@end @for helicities %][%
@if helsum%] 
subdir('sum')[%
@end @if %]
subdir('matrix')
[% @if internal OLP_MODE %]
OLP_source += [% process_name %]_source
[% @else %]
lib = both_libraries('golem_process_[% process_name %]', [% process_name %]_source, install: true)
meson.add_install_script(
  find_program(files('install_mod_files.py')),
  get_option('includedir') / meson.project_name(),
)
configure_file(input: 'config.sh.in', 
  output: 'config.sh', 
  configuration: {
    'prefix': get_option('prefix'),
    'libdir': get_option('libdir'),
    'includedir': get_option('includedir') / meson.project_name(),
    'static_lib': 'libgolem_olp.a'
  },
  install: true,
  install_dir: meson.current_source_dir()
  )
[% @end @if %]