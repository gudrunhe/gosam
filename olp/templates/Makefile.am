[% ' vim: syntax=golem:ts=3:sw=3
 %]# vim: ts=3:sw=3
SUBDIRS=[%
@for subprocesses %] \
	[% path %][%
@end @for subprocesses %]

bin_PROGRAMS=olp_daemon
lib_LTLIBRARIES=lib@GENERIC_LIBRARY_NAME@.la

olp_daemon_SOURCES=olp_daemon.c olp_lexer.l olp_parser.y
lib@GENERIC_LIBRARY_NAME@_la_SOURCES=olp_module.f90

nodist_pkginclude_HEADERS=olp_module.mod
pkginclude_HEADERS=olp.h
noinst_HEADERS=olp_daemon.h olp_parser.h

olp_daemon_LDADD=lib@GENERIC_LIBRARY_NAME@.la
lib@GENERIC_LIBRARY_NAME@_la_LIBADD=[%
@for subprocesses %] \
		$(builddir)/[% path %]/libgolem_process_[% $_ %].la[%
@end @for subprocesses %]

lib@GENERIC_LIBRARY_NAME@_la_LDFLAGS=-avoid-version -export-dynamic


AM_FCFLAGS=[%
@for subprocesses %] \
		-I$(builddir)/[% path %]/common/ \
		-I$(builddir)/[% path %]/matrix/[%
@end @for subprocesses %]

[% @for options %extension%.ldflags ignorecase=true %][%
      @if is_first %]AM_LDFLAGS=[%
      @end @if %] \
	[% $_ %][%
   @end @for %]

AM_YFLAGS= -d

EXTRA_DIST=m4 \
			  autogen.sh
ACLOCAL_AMFLAGS=-I m4

olp_lexer.c: olp_parser.h
