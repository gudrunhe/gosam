[% process_name assuffix=\_ %]_helicity[%helicity%]_gen = \
      custom_target('[% process_name assuffix=\_ %]_helicity[%helicity%]_gen',
              output : ['diagramsl0.f90'],
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

OLP_source += files(['globals.f90', 'amplitudeh[%helicity%].f90'])
OLP_source += [% process_name assuffix=\_ %]_helicity[%helicity%]_gen