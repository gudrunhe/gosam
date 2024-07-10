project('qcdloop', 'fortran', version: '1.98', default_options: ['fortran_std=legacy'])

pkg = import('pkgconfig')

ff = dependency('ff')

add_project_arguments('-Wno-maybe-uninitialized', language: 'fortran')

qcdloop_src = files(['ql/qlsolvequadratic.f', 'ql/qlB1.f', 'ql/qlinit.f', 'ql/qldiffI2.f',
 'ql/qlI4.f', 'ql/qlI3.f', 'ql/qlI2.f', 'ql/qlI1.f', 'ql/qlI4array.f', 'ql/qlzero.f',
 'ql/qlI4fin.f', 'ql/qlI4DNS41.f', 'ql/qlI4sub0m.f', 'ql/qlI4sub1m.f', 'ql/qlI4sub2m.f',
 'ql/qlI4sub2ma.f', 'ql/qlI4sub2mo.f', 'ql/qlI4sub3m.f', 'ql/qlI3fin.f', 'ql/qlI3sub.f',
 'ql/qlI2fin.f', 'ql/qlfndd.f', 'ql/qlLi2omprod.f', 'ql/qlLi2omrat.f', 'ql/qllnomrat4.f',
 'ql/qlLi2omx.f', 'ql/qlLi2omx2.f', 'ql/qltrisort.f', 'ql/qlsnglsort.f', 'ql/qltri1.f',
 'ql/qltri2.f', 'ql/qltri3.f', 'ql/qltri4.f', 'ql/qltri5.f', 'ql/qltri6.f', 'ql/qlbox1.f',
 'ql/qlbox2.f', 'ql/qlbox3.f', 'ql/qlbox4.f', 'ql/qlbox5.f', 'ql/qlbox6.f', 'ql/qlbox7.f',
 'ql/qlbox8.f', 'ql/qlbox9.f', 'ql/qlbox10.f', 'ql/qlbox11.f', 'ql/qlbox12.f', 'ql/qlbox13.f',
 'ql/qlbox14.f', 'ql/qlbox15.f', 'ql/qlbox16.f', 'ql/qlcLi2omx2.f', 'ql/qlcLi2omx3.f', 'ql/auxCD.f',
 'ql/qlspencer.f', 'ql/qlratreal.f', 'ql/qlratgam.f', 'ql/ddilog.f', 'ql/qllnrat.f',
 'ql/qlfunctions.f', 'ql/qlYcalc.f', 'ql/qlkfn.f', 'ql/qlxpicheck.f'])

qcdloop = both_libraries('qcdloop', qcdloop_src, install: true, dependencies: ff)

qcdloop_dep = declare_dependency(link_with: [qcdloop])

meson.add_install_script(
  find_program(files('install_mod_files.py')),
  meson.current_build_dir(),
  get_option('includedir') / 'qcdloop',
)

meson.override_dependency('qcdloop', qcdloop_dep)

pkg.generate(qcdloop, subdirs: 'qcdloop', description: 'Library for the evaluation of one-loop scalar Feynman integrals')