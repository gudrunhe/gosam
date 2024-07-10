project('Form', 'c', 'cpp', version: '4.2.1', default_options: ['buildtype=release', 'b_ndebug=if-release'])

add_project_arguments('-w', language: 'c')
add_project_arguments('-w', language: 'cpp')

threads = dependency('threads')

cc = meson.get_compiler('cpp')
cdata = configuration_data()
check_headers = [
  'fcntl.h',
  'inttypes.h',
  'limits.h',
  'memory.h',
  'stdint.h',
  'stdlib.h',
  'strings.h',
  'string.h',
  'sys/file.h',
  'sys/stat.h',
  'sys/types.h',
  'unistd.h',
  'windows.h',
  'boost/unordered_map.hpp',
  'boost/unordered_set.hpp',
  'tr1/unordered_map',
  'tr1/unordered_set',
  'unordered_map',
  'unordered_set'
]

foreach h : check_headers
  if cc.has_header(h)
    cdata.set('HAVE_' + h.underscorify().to_upper(), 1)
  endif
endforeach

check_functions = [
  ['HAVE_CLOCK_GETTIME', 'clock_gettime', '#include<time.h>'],
  ['HAVE_FTIME', 'ftime', '#include<sys/timeb.h>'],
  ['HAVE_GETTIMEOFDAY', 'gettimeofday', '#include<sys/time.h>'],
  ['HAVE_BUILTIN_POPCOUNT', '__builtin_popcount', ''],
  ['HAVE_POPCNT', '__popcnt', '#include <intrin.h>']
]

foreach f : check_functions
  if cc.has_function(f.get(1), prefix : f.get(2))
    cdata.set(f.get(0), 1)
  endif
endforeach

cdata.set('SIZEOF_CHAR', cc.sizeof('char'))
cdata.set('SIZEOF_INT', cc.sizeof('int'))
cdata.set('SIZEOF_LONG', cc.sizeof('long'))
cdata.set('SIZEOF_LONG_LONG', cc.sizeof('long long'))
cdata.set('SIZEOF_OFF_T', cc.sizeof('off_t'))
cdata.set('SIZEOF_SHORT', cc.sizeof('short'))
cdata.set('SIZEOF_VOID_P', cc.sizeof('void*'))
cdata.set('HAVE_PTHREADS', 1)
cdata.set('UNIX', 1)

if cc.sizeof('void*') == 4
    cdata.set('ILP32', 1)
elif cc.sizeof('long') == 3
    cdata.set('LLP64', 1)
else
    cdata.set('LP64', 1)
endif

configure_file(input : 'config.h.meson',
  output : 'config.h',
  configuration : cdata)

form_src = files([])
tform_src = files([])

subdir('sources')

executable('form',
    form_src,
    install:true,
    include_directories: include_directories('.', 'sources'),
    c_args: ['-DHAVE_CONFIG_H=1'],
    cpp_args: ['-DHAVE_CONFIG_H=1', '-U_GLIBCXX_ASSERTIONS']
    )

executable('tform',
    form_src + tform_src,
    install:true,
    include_directories: include_directories('.', 'sources'),
    c_args: ['-DHAVE_CONFIG_H=1'],
    cpp_args: ['-DHAVE_CONFIG_H=1'],
    dependencies: threads
    )