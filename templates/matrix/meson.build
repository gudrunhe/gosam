[% process_name %]_source += files(['matrix.f90', \
    'matrix_dp.f90', \
    [% @if extension quadruple %]'matrix_qp.f90', \
    [% @end @if%]'rescue.f90', [%
@for crossings %] \
	'[% $_ asprefix=\_ %]matrix.f90',[%
@end @for crossings %]])

if get_option('test_executables')
    [% process_name %]_test_source = [% process_name %]_source + files(['test.f90'])
    [% @if internal OLP_MODE %]
    [% process_name %]_test_source += common_source
    [% @end @if %]
    [% process_name %]_test = executable('[% process_name %]_test',
                                         [% process_name %]_test_source,
                                         dependencies: dependencies,
                                         install_rpath: dependencies[0].get_variable('libdir'),
                                         link_args: '-Wl,--disable-new-dtags',
                                         build_by_default: false,
                                         install: true,
                                         install_dir: meson.project_source_root() / 'test')
endif