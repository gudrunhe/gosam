[% @if internal OLP_MODE %][% @else %]
project('GoSam_Process_[% process_name %]',
    'fortran',
    version:'1.0',
    meson_version: '>=1.4',
    default_options: [
        'buildtype=release',
        'b_asneeded=false',
        'pkg_config_path=[% pkg_config_path %]'
        ]
    )

pkg_env = ['PKG_CONFIG_PATH=[% pkg_config_path %]']

dependencies = []
dependencies += dependency('avh_olo', allow_fallback: true)
[% @if extension golem95 %]dependencies += dependency('golem95', allow_fallback: true)[%@end @if %]
[% @if extension ninja %]dependencies += dependency('ninja', allow_fallback: true)[% @end @if %]
dep_ldflags = ''
dep_cflags = ''
pkg_config = find_program('pkg-config')
if not (dependencies[0].type_name() == 'internal') # Only if dependencies are not vendored
  foreach d : dependencies
    dep_ldflags += ' ' + run_command(pkg_config, '--libs', d.name(), capture: true, check: true, env: pkg_env).stdout()
    dep_ldflags += ' ' + '-Wl,-rpath,' + d.get_variable('libdir')
    dep_cflags += ' ' + run_command(pkg_config, '--cflags', d.name(), capture: true, check: true, env: pkg_env).stdout()
  endforeach
else
  libdir = get_option('prefix') / get_option('libdir')
  incdir = get_option('prefix') / get_option('includedir')
  dep_ldflags += '-L' + libdir + ' -lavh_olo'[% @if extension golem95 %] + ' -lgolem95'[%@end @if %][% @if extension ninja %] + ' -lninja'[% @end @if %]
  dep_ldflags += ' -Wl,-rpath,' + libdir
  dep_cflags += '-I' + incdir + '/avh_olo'[% @if extension golem95 %] + ' -I' + incdir + '/golem95'[%@end @if %][% @if extension ninja %] + ' -I' + incdir + '/ninja'[% @end @if %]
endif

add_project_arguments('-w', language: 'fortran')
add_project_arguments('-ffree-line-length-none', language: 'fortran')
add_project_arguments('-march=[% meson.arch %]', language: 'fortran')
if get_option('code_check')
    add_project_arguments('-fcheck=all', language: 'fortran')
    add_project_arguments('-fbacktrace', language: 'fortran')
endif
add_project_arguments([% @for options %extension%.fcflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %]  language: 'fortran')

add_project_link_arguments('-march=[% meson.arch %]', language: 'fortran')
add_project_link_arguments([% @for options %extension%.ldflags ignorecase=true %]'[% $_ %]'.split(' '),
[% @end @for %] language: 'fortran')
codegen_targets = []
[% @end @if %]

[% process_name asprefix=\_ %]source = files([])
hel_gen_targets = []

subdir('doc')
[%
@for helicities generated %]
subdir('helicity[% helicity %]')[%
@end @for helicities %][%
@if helsum%]
subdir('sum')[%
@end @if %]
subdir('common')
subdir('matrix')
codegen_targets += hel_gen_targets
[% @if internal OLP_MODE %]
OLP_source += [% process_name asprefix=\_ %]source
[% @else %]
codegen = alias_target('codegen', codegen_targets)
lib = both_libraries('golem_process_[% process_name %]',
    [% process_name asprefix=\_ %]source,
    install: true,
    dependencies: dependencies
    )
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
    'static_lib': 'libgolem_process_[% process_name %].a',
    'dep_cflags': dep_cflags,
    'dep_ldflags': dep_ldflags
  },
  install: true,
  install_dir: meson.current_source_dir()
  )
gosam_process_[% process_name asprefix=\_ %]dep = declare_dependency(
  link_with: lib
)
meson.override_dependency('gosam_process_[% process_name%]', gosam_process_[% process_name asprefix=\_ %]dep)
[% @end @if %]
