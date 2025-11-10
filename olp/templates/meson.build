project('GoSam_Process[% process_name assuffix=\_%]',
    'fortran',
    version:'1.0',
    meson_version: '>=0.63.0',
    default_options: [
        'buildtype=release',
        'b_asneeded=false',
        'pkg_config_path=[% pkg_config_path %]'
        ]
    )

pkg_env = ['PKG_CONFIG_PATH=[% pkg_config_path %]']

dependencies = []
dependencies += dependency('avh_olo', allow_fallback: true, static: true)
[% @if extension golem95 %]dependencies += dependency('golem95', allow_fallback: true, static: true)[% @end @if %]
[% @if extension ninja %]dependencies += dependency('ninja', allow_fallback: true, static: true)[% @end @if %]

dep_ldflags = ''
dep_cflags = ''
pkg_config = find_program('pkg-config')

if not (dependencies[0].type_name() == 'internal') # Only if dependencies are not vendored
  foreach d: dependencies
      dep_ldflags += ' ' + run_command(pkg_config, '--libs', d.name(), capture: true, check: true, env: pkg_env).stdout()
      dep_ldflags += ' -Wl,-rpath,' + d.get_variable('libdir')
      dep_cflags += ' ' + run_command(pkg_config, '--cflags', d.name(), capture: true, check: true, env: pkg_env).stdout()
  endforeach
else
  dep_ldflags += '-L' + get_option('libdir') + ' -lavh_olo'[% @if extension golem95 %] + ' -lgolem95'[%@end @if %][% @if extension ninja %] + ' -lninja'[% @end @if %]
  dep_ldflags += ' ' + '-Wl,-rpath,' + get_option('libdir')
  dep_cflags += '-I' + get_option('includedir') + '/avh_olo'[% @if extension golem95 %] + ' -I' + get_option('includedir') + '/golem95'[%@end @if %][% @if extension ninja %] + ' -I' + get_option('includedir') + '/ninja'[% @end @if %]
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

OLP_source = files('olp_module.f90')
common_source = []
codegen_targets = []

subdir('common')
[%
@for subprocesses %]
subdir('[% $_ %]')[%
@end @for subprocesses %]

OLP_source += common_source

codegen = alias_target('codegen', codegen_targets)

lib = both_libraries('golem_olp', OLP_source, install: true, dependencies: dependencies)

install_headers('olp.h', subdir: 'GoSam_Process')
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
    'dep_cflags': dep_cflags,
    'dep_ldflags': dep_ldflags
  },
  install: true,
  install_dir: meson.current_source_dir()
  )

gosam_olp_[% process_name asprefix=\_ %]dep = declare_dependency(
  link_with: lib
)
meson.override_dependency('gosam_olp_[% process_name%]', gosam_olp_[% process_name asprefix=\_ %]dep)
