quadninja_src = files([])

ninja_implem_gen = custom_target('ninja_implem_gen',
                                command: [
                                    sed,
                                    '-f',
                                    meson.project_source_root() / 'src/quadsources/genquadsources.sed',
                                    '@INPUT@'
                                    ],
                                input: meson.project_source_root() / 'src/ninja_implem.cxx',
                                output: 'ninja_implem.cxx',
                                capture: true,
                              )

polys_implem_gen = custom_target('polys_implem_gen',
                                command: [
                                    sed,
                                    '-f',
                                    meson.project_source_root() / 'src/quadsources/genquadsources.sed',
                                    '@INPUT@'
                                    ],
                                input: meson.project_source_root() / 'src/polys_implem.cxx',
                                output: 'polys_implem.cxx',
                                capture: true,
                              )

foreach f : ninja_src
    quadninja_src += custom_target(f.full_path().split('/')[-1].underscorify() + '_gen',
                                    command: [
                                        sed,
                                        '-f',
                                        meson.project_source_root() / 'src/quadsources/genquadsources.sed',
                                        '@INPUT@'
                                        ],
                                    input: f,
                                    output: f.full_path().split('/')[-1],
                                    capture: true,
                                    depends: [ninja_implem_gen, polys_implem_gen]
                                  )
endforeach

ninja_args += [
        '-DQUADNINJA_USE_ONELOOP=1',
        '-DQUADNINJA_MASSLESS=1',
        '-DQUADNINJA_X1RANK=1',
        '-DQUADNINJA_USE_ONELOOP_WITH_CACHE=1',
        '-DQUADNINJA_QUADRUPLE=1'
        ]

meson.add_install_script(
  mod_installer,
  meson.project_build_root(),
  get_option('includedir') / 'quadninja',
)