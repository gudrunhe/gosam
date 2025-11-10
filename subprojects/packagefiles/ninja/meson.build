project('Ninja', 'cpp', 'fortran', version: '1.1.0', meson_version: '>=1.4')

add_project_arguments('-w', language: 'fortran')
add_project_arguments('-w', language: 'cpp')

pkg = import('pkgconfig')
mod_installer = find_program(files('install_mod_files.py'))

avh_olo = dependency('avh_olo')
ninja_dependencies = [avh_olo]

ninja_subdirs = ['ninja']

ninja_src = files(['src/basis.cc', 'src/cuts_utils.cc', 'src/ninja.cc', 'src/Xcuts.cc', 'src/cuts.cc',
    'src/Xninja.cc', 'src/spinors.cc', 'src/tensor_ninja.cc', 'src/coefficient_level_subs.cc',
    'src/integral_library.cc', 'src/avholo_interface.cc', 'src/rambo.cc', 'src/ninja_wraps.cc', 'src/ninjago.F90',
    'src/gosam_interface.cc', 'src/gosam_interface.hh',
    'src/basis.hh', 'src/cuts.hh', 'src/cuts_utils.hh', 'src/Xcuts.hh',
    'src/cuts_utils-inl.hh', 'src/coefficient_level_subs.hh', 'src/integermath.hh', 'src/tmp_utils.hh',
    'src/ninja_scoped_array.hh', 'src/cuts_vector.hh', 'src/integral_library_wrapper.hh', 'src/s_mat_wrapper.hh',
    'src/avholo_decls.hh', 'src/ninja_hash_table.hh', 'src/integral_cache.hh'
    ])
ninja_src += files(['src/avholo_wrapper.F90'])

ninja_args = [
        '-DNINJA_USE_ONELOOP=1',
        '-DVERSION="1.1.0"',
        '-DNINJA_MASSLESS=1',
        '-DNINJA_X1RANK=1',
        '-DNINJA_USE_ONELOOP_WITH_CACHE=1'
        ]

ninja_headers = ['ninja.hh', 'ninja_in.hh', 'tensor_ninja.hh', 'zero_float.hh', 'types.hh', 's_mat.hh',
    'num_defs.hh', 'spinors.hh', 'static_arrays.hh', 'integral_library.hh', 'thread_safe_integral_library.hh',
    'rambo.hh', 'ninjanumgen.hh', 'momentum.hh', 'avholo.hh']

subdir('src/ninja')

ninja_includedirs = [include_directories('src/ninja'), include_directories('src')]

if get_option('quadninja')
    ninja_headers += 'quadruple.hh'
    quadmath = meson.get_compiler('cpp').find_library('quadmath')
    sed = find_program('sed')
    subdir('src/quadninja')
    subdir('src/quadsources')
    ninja_includedirs += include_directories('src/quadninja')
    ninja_src += quadninja_src
    ninja_src += quadninja_headers
    ninja_dependencies += quadmath
    ninja_subdirs += 'quadninja'
endif

ninja_src += files(['src/ninjavholo_wraps.cc', 'src/ninjavholo.F90', 'src/mninja.F90'])

ninja = both_libraries('ninja',
    ninja_src,
    dependencies: ninja_dependencies,
    install: true,
    include_directories: ninja_includedirs,
    cpp_args: ninja_args,
    fortran_args: ninja_args,
    install_rpath:  get_option('prefix') / get_option('libdir')
    )

ninja_dep = declare_dependency(link_with: ninja)
meson.override_dependency('ninja', ninja_dep)


pkg.generate(ninja,
    subdirs: ninja_subdirs,
    description: 'Automated integrand reduction via Laurent series expansion for one-loop amplitudes',
    )