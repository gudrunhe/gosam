[% process_name assuffix=\_ %]_common_gen = \
      custom_target('[% process_name assuffix=\_ %]_common_gen',
              output : ['model.f90', 'color.f90', 'version.f90'],
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

[% process_name %]_source += files(['config.f90', 'accu.f90', 'rambo.f90', 'globalsl1.f90',
                     'util.f90', 'scalar_cache.f90', 'kinematics.f90',
                     'dipoles.f90', 'groups.f90'])
[% process_name %]_source += [% process_name assuffix=\_ %]_common_gen
