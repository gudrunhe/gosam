project('ff', 'fortran', version: '2.0', default_options: ['fortran_std=legacy'])

pkg = import('pkgconfig')

add_project_arguments('-w', language: 'fortran')

ff_src = files(['ff/aaxbx.f', 'ff/aaxcx.f', 'ff/aaxdx.f', 'ff/aaxinv.f', 'ff/aacbc.f', 'ff/aaccc.f', 'ff/aacinv.f',
'ff/spence.f', 'ff/npoin.f', 'ff/ff2dl2.f', 'ff/ffabcd.f', 'ff/ffca0.f', 'ff/ffcb0.f', 'ff/ffcb1.f',
'ff/ffcb2p.f', 'ff/ffcdb0.f', 'ff/ffcc0.f', 'ff/ffcc0p.f', 'ff/ffcc1.f', 'ff/ffcel2.f', 'ff/ffcel3.f', 'ff/ffcel4.f',
'ff/ffcel5.f', 'ff/ffceta.f', 'ff/ffcli2.f', 'ff/ffcrr.f', 'ff/ffcxr.f', 'ff/ffcxs3.f', 'ff/ffcxs4.f', 'ff/ffcxyz.f',
'ff/ffdcc0.f', 'ff/ffdcxs.f', 'ff/ffdel2.f', 'ff/ffdel3.f', 'ff/ffdel4.f', 'ff/ffdel5.f', 'ff/ffdel6.f', 'ff/ffdl2i.f',
'ff/ffdl5p.f', 'ff/ffdxc0.f', 'ff/ffinit.f', 'ff/ffrcvr.f', 'ff/fftran.f', 'ff/ffxb0.f', 'ff/ffxb1.f', 'ff/ffxb2p.f',
'ff/ffxc0.f', 'ff/ffxc0i.f', 'ff/ffxc0p.f', 'ff/ffxc1.f', 'ff/ffxd0.f', 'ff/ffxd0h.f', 'ff/ffxd0i.f', 'ff/ffxd0p.f',
'ff/ffxd1.f', 'ff/ffxdb0.f', 'ff/ffxdbd.f', 'ff/ffxdi.f', 'ff/ffxdpv.f', 'ff/ffxe0.f', 'ff/ffxe1.f', 'ff/ffxf0.f',
'ff/ffxf0h.f', 'ff/ffxli2.f', 'ff/ffxxyz.f'])

install_headers('ff/aa.h', 'ff/ff.h', 'ff/ffs.h', subdir: 'ff')

install_data('ff/fferr.dat', 'ff/ffperm5.dat', 'ff/ffwarn.dat', install_dir : get_option('datadir') / 'ff')

ff = both_libraries('ff', ff_src, install: true)

ff_dep = declare_dependency(link_with: ff)

meson.override_dependency('ff', ff_dep)

pkg.generate(ff, subdirs: 'ff', description: 'FF 2.0, a package to evaluate one-loop integrals written by G. J. van Oldenborgh, NIKHEF-H, Amsterdam')