noinst_PROGRAMS=test
noinst_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %]_matrix.la
libgolem_process[% process_name assuffix=\_ %]_matrix_la_SOURCES=[%
@if extension powhegbox %] \
	powhegbox.f90[%
@end @if %] matrix.f90[%
@for crossings %] \
	[% $_ asprefix=\_ %]matrix.f90[%
@end @for crossings %]
nodist_pkginclude_HEADERS=[%
@if extension powhegbox %] [% process_name asprefix=\_ %]powheg.mod[%
@end @if %] [% process_name asprefix=\_ %]matrix.mod[%
@for crossings %] \
	[% $_ asprefix=\_ %]matrix.mod[%
@end @for crossings %]

test_SOURCES=test.f90
test_LDADD=\
   $(builddir)/../matrix/libgolem_process[%
      process_name assuffix=\_ %]_matrix.la[%
@for helicities %] \
   $(builddir)/../helicity[% helicity %]/libgolem_process[%
      process_name assuffix=\_ %]_helicity[% helicity %].la[%
@end @for helicities %] \
   $(builddir)/../common/libgolem_process[%
      process_name assuffix=\_ %]_common.la \
   $(GOLEM_CONFIG_LDFLAGS)

CLEANFILES=$(nodist_pkginclude_HEADERS)
ACLOCAL_AMFLAGS=-I m4

AM_FCFLAGS=$(GOLEM_CONFIG_FCFLAGS) -I../common[%
   @for helicities %] \
	   -I../helicity[%helicity%][%
   @end @for %]

include Makefile.dep
