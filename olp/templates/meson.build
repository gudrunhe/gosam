project('GoSam_Process', 'fortran', version:'1.0', meson_version: '>=0.57.0')

add_global_arguments('-w', language: 'fortran')
add_global_arguments([% @for options %extension%.fcflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %]  language: 'fortran')

add_global_link_arguments([% @for options %extension%.ldflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %] language: 'fortran')

OLP_source = files('olp_module.f90')

[%
@for subprocesses %]
subdir('[% $_ %]')[%
@end @for subprocesses %]

lib = both_libraries('golem_olp', OLP_source, install: true, install_dir: meson.current_source_dir() / '.libs')

install_headers('olp.h', subdir: 'gosam_process')