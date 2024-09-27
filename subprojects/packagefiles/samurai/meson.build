project('Samurai', 'fortran', version: '2.1.1')

pkg = import('pkgconfig')

add_project_arguments('-w', language: 'fortran')

avh_olo = dependency('avh_olo')
qcdloop = dependency('qcdloop')
golem95 = dependency('golem95')

samurai_src = files([])

subdir('samurai')

samurai = both_libraries('samurai',
    samurai_src,
    dependencies: [avh_olo, qcdloop, golem95],
    install: true,
    install_rpath:  get_option('prefix') / get_option('libdir')
    )

samurai_dep = declare_dependency(link_with: samurai)

meson.add_install_script(
  find_program(files('install_mod_files.py')),
  meson.current_build_dir(),
  get_option('includedir') / 'samurai',
)

meson.override_dependency('samurai', samurai_dep)

pkg.generate(samurai,
    subdirs: 'samurai',
    description: 'Scattering amplitudes from unitarity-based reduction algorithms at the integrand level'
    )