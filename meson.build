project('GoSam',
    'fortran',
    'cpp',
    version: '3.0.2-' + run_command(find_program('git'), 'rev-parse', '--short=7', 'HEAD', capture: true, check: true).stdout().strip(),
    default_options: {
        'buildtype': 'release',
        'bindir': get_option('bindir') + '/GoSam',
        'includedir': get_option('includedir') + '/GoSam',
        'libdir': get_option('libdir') + '/GoSam',
        'datadir': get_option('datadir') + '/GoSam'
    },
    meson_version: '>=1.4',
    license: 'GPL-3.0-or-later'
)

if not (build_machine.system() == 'linux' or build_machine.system() == 'darwin')
    error('Found system ' + build_machine.system() + ', but only Linux and OSX are supported.')
endif

python = import('python').find_installation()

if not python.language_version().version_compare('>=3.9')
    error('Found Python version ' + python.language_version() + ', but the minimum required version is 3.9')
endif

meson.add_dist_script('cement-version.sh', meson.project_version())

if get_option('native')
    add_global_arguments('-march=native', language: ['fortran', 'c', 'cpp'])
    add_global_link_arguments('-march=native', language: ['fortran', 'c', 'cpp'])
endif

add_global_link_arguments('--disable-new-dtags', language: ['fortran', 'c', 'cpp'])

run_command(
    'wget',
    '--user=anonymous',
    '--password=anonymous',
    '-Psubprojects/packagecache',
    'http://qgraf.tecnico.ulisboa.pt/v3.4/qgraf-3.4.2.tgz',
    check: true
    )

subproject('avh_olo')
if get_option('golem95')
    subproject('golem95')
endif
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

run_target(
    'gs-uninstall', 
    command: find_program(files('uninstall.py')), 
    env: {
        'prefix': get_option('prefix'),
        'bindir': get_option('bindir'),
        'includedir': get_option('includedir'),
        'libdir': get_option('libdir'),
        'datadir': get_option('datadir'),
        'py_dir': python.get_install_dir() / 'golem'
    }
)
