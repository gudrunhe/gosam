[% @if internal OLP_MODE %][% @else %]
project('GoSam_Process', 'fortran', version:'1.0', meson_version: '>=0.57.0')

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
lib = both_libraries('golem_process_[% process_name %]', [% process_name %]_source, install: true, install_dir: meson.current_source_dir() / '.libs')
[% @end @if %]