if get_option('doc')
    [% process_name %]_doc = custom_target('[% process_name %]_doc',
                                            output : '[% process_name %].pdf',
                                            command : ['generate_doc.sh'],
                                            env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()},
                                            install: true,
                                            install_dir: meson.project_source_root() / 'doc'
                                            )
endif