install_subdir('algorithms', install_dir: python.get_install_dir() / 'golem')
install_subdir('app', install_dir: python.get_install_dir() / 'golem')
install_subdir('model', install_dir: python.get_install_dir() / 'golem')
install_subdir('pyxo', install_dir: python.get_install_dir() / 'golem')
install_subdir('templates', install_dir: python.get_install_dir() / 'golem')
install_subdir('topolopy', install_dir: python.get_install_dir() / 'golem')
install_subdir('util', install_dir: python.get_install_dir() / 'golem')

installation_py = configure_file(
    input : 'installation.py.in',
    output : 'installation.py',
    configuration : {
        'prefix': get_option('prefix'),
        'datadir': get_option('datadir'),
        'version': meson.project_version().split('-')[0],
        'major_version': meson.project_version().split('-')[0].split('.')[0],
        'minor_version': meson.project_version().split('-')[0].split('.')[1],
        'patch_version': meson.project_version().split('-')[0].split('.')[2],
        'VCS_TAG': meson.project_version().split('-')[1],
        'WITH_GOLEM': get_option('golem95')
    },
    install: true,
    install_dir: python.get_install_dir() / 'golem'
)

gosam_py = configure_file(
    input: 'gosam.py.in',
    output: 'gosam.py',
    configuration: {'py_install_dir' : python.get_install_dir()},
    install: true,
    install_dir: get_option('prefix') / get_option('bindir')
)

gosam_config_py = configure_file(
    input: 'gosam-config.py.in',
    output: 'gosam-config.py',
    configuration: {'py_install_dir' : python.get_install_dir()},
    install: true,
    install_dir: get_option('prefix') / get_option('bindir')
)

python.install_sources('__init__.py', '__main__.py', 'properties.py', 'shell.py', subdir: 'golem')