project('Ninja', 'cpp', 'fortran', version: '1.1.0')

pkg = import('pkgconfig')

avh_olo = dependency('avh_olo')

ninja_src = files(['src/basis.cc', 'src/cuts_utils.cc', 'src/ninja.cc', 'src/Xcuts.cc', 'src/cuts.cc',
    'src/Xninja.cc', 'src/spinors.cc', 'src/tensor_ninja.cc', 'src/coefficient_level_subs.cc',
    'src/integral_library.cc', 'src/avholo_interface.cc', 'src/rambo.cc', 'src/ninja_wraps.cc'])

ninja_src += files(['src/avholo_wrapper.F90', 'src/ninjavholo_wraps.cc', 'src/ninjavholo.F90',
    'src/gosam_interface.cc', 'src/ninjago.F90', 'src/mninja.F90'])

ninja = both_libraries('ninja',
    ninja_src,
    dependencies: [avh_olo],
    install: true,
    include_directories: [include_directories('src/ninja'), include_directories('src')],
    cpp_args: [
        '-DNINJA_USE_ONELOOP=1',
        '-DVERSION="1.1.0"',
        '-DNINJA_MASSLESS=1',
        '-DNINJA_X1RANK=1',
        '-DNINJA_USE_ONELOOP_WITH_CACHE=1'
        ]
    )

ninja_dep = declare_dependency(link_with: ninja)

install_headers(files(['src/ninja/ninja.hh', 'src/ninja/ninja_in.hh', 'src/ninja/tensor_ninja.hh',
    'src/ninja/zero_float.hh', 'src/ninja/types.hh', 'src/ninja/s_mat.hh', 'src/ninja/num_defs.hh',
    'src/ninja/spinors.hh', 'src/ninja/static_arrays.hh', 'src/ninja/integral_library.hh',
    'src/ninja/thread_safe_integral_library.hh', 'src/ninja/rambo.hh', 'src/ninja/ninjanumgen.hh']
    ), subdir: 'ninja')

meson.add_install_script(
  find_program(files('install_mod_files.py')),
  meson.current_build_dir(),
  get_option('includedir') / 'ninja',
)

pkg.generate(ninja,
    subdirs: 'ninja',
    description: 'Automated integrand reduction via Laurent series expansion for one-loop amplitudes'
    )