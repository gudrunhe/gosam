generated_source = ['color.f90' [% @if internal OLP_MODE %][% @else %], 'version.f90', 'model.f90'[% @end @if %]]
[% @if extension quadruple %] generated_source += ['color_qp.f90' [% @if internal OLP_MODE %][% @else %], 'model_qp.f90'[% @end @if %]][% @end @if %]

[% process_name %]_common_gen = \
      custom_target('[% process_name %]_common_gen',
              output : generated_source,
              command : ['generate_source.sh'],
              build_by_default: true,
              env: {'OUTDIR': meson.current_build_dir(), 'CURRENT_SOURCE_DIR': meson.current_source_dir()}
                )

[% process_name %]_source += files(['rambo.f90', 'globalsl1.f90',
                     'util.f90', 'scalar_cache.f90', 'kinematics.f90',
                     'dipoles.f90', 'groups.f90'])

[% @if extension quadruple %]
[% process_name %]_source += files(['rambo_qp.f90', 'globalsl1_qp.f90',
                     'util_qp.f90', 'kinematics_qp.f90', 'dipoles_qp.f90'])[%
@end @if %]

[% @if internal OLP_MODE %][% @else %]
[% process_name %]_source += files(['config.f90', 'accu.f90', 'SpinorBrackets.f90' [% @if internal CUSTOM_SPIN2_PROP %], 'custompropagator.f90'[%
@end @if %]])
[% @if extension quadruple %] [% process_name %]_source += files(['accu_qp.f90', 'SpinorBrackets_qp.f90'[% @end @if %]])
[% @end @if %]
[% process_name %]_source += [% process_name %]_common_gen
