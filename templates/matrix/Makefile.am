noinst_PROGRAMS=test
noinst_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %]_matrix.la
libgolem_process[% process_name assuffix=\_ %]_matrix_la_SOURCES= matrix.f90[%
@for crossings %] \
	[% $_ asprefix=\_ %]matrix.f90[%
@end @for crossings %]
nodist_pkginclude_HEADERS= [% process_name asprefix=\_ %]matrix.mod[%
@for crossings %] \
	[% $_ asprefix=\_ %]matrix.mod[%
@end @for crossings %]

test_SOURCES=test.f90
test_LDADD=\
   $(builddir)/../matrix/libgolem_process[%
      process_name assuffix=\_ %]_matrix.la[%
@for helicities generated %] \
   $(builddir)/../helicity[% helicity %]/libgolem_process[%
      process_name assuffix=\_ %]_helicity[% helicity %].la[%
@end @for helicities %][%
@if helsum %] \
   $(builddir)/../sum/libgolem_process[%
      process_name assuffix=\_ %]_sum.la[%
@end @if %] \
   $(builddir)/../common/libgolem_process[%
      process_name assuffix=\_ %]_common.la \
   $(GOLEM_CONFIG_LDFLAGS)

CLEANFILES=$(nodist_pkginclude_HEADERS)
ACLOCAL_AMFLAGS=-I m4

AM_FCFLAGS=$(GOLEM_CONFIG_FCFLAGS) -I../common[%
   @for helicities generated %] \
	   -I../helicity[%helicity%][%
   @end @for %][%
   @if helsum %] \
	   -I../sum[%
   @end @if %]

include Makefile.dep
