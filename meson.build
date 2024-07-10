project('GoSam',
    'fortran',
    'cpp',
    version: '3.0.0',
    default_options: [
        'buildtype=release',
        'bindir=' + get_option('bindir') + '/GoSam',
        'includedir=' + get_option('includedir') + '/GoSam',
        'libdir=' + get_option('libdir') + '/GoSam',
        'datadir=' + get_option('datadir') + '/GoSam',
        'b_ndebug=false'
    ]
)

python = import('python').find_installation()

if not python.language_version().version_compare('>=3.6')
    error('Found Python version ' + python.language_version() + ', but the minimum required version is 3.6')
endif

git_rev = run_command(find_program('git'), 'rev-parse', '--short=7', 'HEAD', capture: true, check: true).stdout().strip()

subproject('avh_olo')
subproject('ff')
subproject('qcdloop')
subproject('golem95')
subproject('samurai')
subproject('ninja')
subproject('qgraf')
subproject('form')

subdir('src/python/golem')

install_subdir('models', install_dir: get_option('prefix') / get_option('datadir'))
install_subdir('src/form', install_dir: get_option('prefix') / get_option('datadir') / 'src')
install_subdir('olp', install_dir: get_option('prefix') / get_option('datadir'))
install_subdir('templates', install_dir: get_option('prefix') / get_option('datadir'))

configure_file(
    input: 'gosam_setup_env.sh.in',
    output: 'gosam_setup_env.sh',
    configuration: {
        'prefix': get_option('prefix'),
        'bindir': get_option('bindir'),
        'py_install_dir': python.get_install_dir(),
        'libdir': get_option('libdir')
    },
    install: true,
    install_dir: get_option('prefix') / get_option('bindir')
)