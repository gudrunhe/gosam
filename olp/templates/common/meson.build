common_gen = custom_target('common_gen',
              output : ['model.f90', 'version.f90'[% @if extension quadruple%], 'model.f90'[% @end @if %]],
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

common_source += files(['accu.f90', 'config.f90', 'SpinorBrackets.f90'])

[% @if extension quadruple %]
common_source += files(['accu_qp.f90', 'SpinorBrackets_qp.f90'])[%
@end @if %]

common_source += common_gen