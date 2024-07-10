config_data = configuration_data({
  'case_with_golem': '',
  'case_wout_golem': '!AC!',
  'case_with_avh': '',
  'case_wout_avh': '!AC!',
  'case_with_ql': '',
  'case_wout_ql': '!AC!',
  'case_with_lt': '!AC!',
  'case_wout_lt': '',
  'fortran_real_kind': 'kind(1.0d0)',
  'VERSION': meson.project_version()
})

samurai_src += configure_file(input: 'madds.f90.in', output: 'madds.f90', configuration: config_data)
samurai_src += configure_file(input: 'msamurai.f90.in', output: 'msamurai.f90', configuration: config_data)
samurai_src += configure_file(input: 'precision.f90.in', output: 'precision.f90', configuration: config_data)

samurai_src += files(['constants.f90', 'kinematic.f90', 'ltest.f90', 'mcgs.f90', 'mfunctions.f90',
    'mgetbase.f90', 'mgetc1.f90', 'mgetc2.f90', 'mgetc3.f90', 'mgetc4.f90', 'mgetc5.f90', 'mgetqs.f90',
    'mglobal.f90', 'mrestore.f90', 'mtens.f90', 'mtests.f90', 'ncuts.f90', 'notfirst.f90',
    'options.f90', 'save.f90', 'maccu.f90'])