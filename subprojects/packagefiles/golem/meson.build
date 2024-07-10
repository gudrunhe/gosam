project('golem95', 'fortran', version: '1.3.3')

pkg = import('pkgconfig')

add_project_arguments('-w', language: 'fortran')

avh_olo = dependency('avh_olo')

golem95_src = files([])

subdir('src')

golem95 = both_libraries('golem95', golem95_src, dependencies: avh_olo, install: true)

golem95_dep = declare_dependency(link_with: golem95)

meson.add_install_script(
  find_program(files('install_mod_files.py')),
  meson.current_build_dir(),
  get_option('includedir') / 'golem95',
)

meson.override_dependency('golem95', golem95_dep)

pkg.generate(golem95,
    subdirs: 'golem95',
    description: 'A package for the numerical evaluation of integrals and tensor form factors with up to six external legs'
    )