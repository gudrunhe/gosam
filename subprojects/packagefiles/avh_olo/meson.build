project('avh_olo', 'fortran', version: '3.6.1')

pkg = import('pkgconfig')

add_project_arguments('-Wno-unused-variable', language: 'fortran')
add_project_arguments('-Wno-unused-dummy-argument', language: 'fortran')
add_project_arguments('-Wno-conversion', language: 'fortran')
add_project_arguments('-Wno-real-q-constant', language: 'fortran')

avh_olo_gen = custom_target('avh_olo_gen',
    input: files(['create.py']),
    output: 'avh_olp.f90',
    command: [find_program('python3'), '@INPUT@', 'source', '@OUTPUT@']
    )

avh_olo = both_libraries('avh_olo', avh_olo_gen, install: true)

avh_olo_dep = declare_dependency(link_with: avh_olo)

meson.add_install_script(
  find_program(files('install_mod_files.py')),
  meson.current_build_dir(),
  get_option('includedir') / 'avh_olo',
)

meson.override_dependency('avh_olo', avh_olo_dep)

pkg.generate(avh_olo, subdirs: 'avh_olo', description: 'Library for the evaluation of 1-loop scalar 1-, 2-, 3- and 4-point functions')
