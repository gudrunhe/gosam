quadninja_headers = []

foreach f : ninja_headers
    quadninja_headers += custom_target(f.underscorify() + '_gen',
                                    command: [
                                        sed,
                                        '-f',
                                        meson.project_source_root() / 'src/quadsources/genquadsources.sed',
                                        '@INPUT@'
                                        ],
                                    input: meson.project_source_root() / 'src/ninja' / f,
                                    output: f,
                                    capture: true,
                                    install: true,
                                    install_dir: get_option('includedir') / 'quadninja'
                                  )
endforeach