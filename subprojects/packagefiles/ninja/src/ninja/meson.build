install_headers(files(ninja_headers), subdir: 'ninja')

meson.add_install_script(
  mod_installer,
  meson.project_build_root(),
  get_option('includedir') / 'ninja',
)