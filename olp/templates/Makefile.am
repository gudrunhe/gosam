[% ' vim: syntax=golem:ts=3:sw=3
 %]# vim: ts=3:sw=3
SUBDIRS=[%
@for subprocesses %] \
	[% path %][%
@end @for subprocesses %][%
@if internal OLP_DAEMON %]
bin_PROGRAMS=olp_daemon[%
@end @if %]
lib_LTLIBRARIES=lib@GENERIC_LIBRARY_NAME@.la[%
@if internal OLP_DAEMON %]
olp_daemon_SOURCES=olp_daemon.c olp_lexer.l olp_parser.y
olp_daemon_LDADD=lib@GENERIC_LIBRARY_NAME@.la
noinst_HEADERS=olp_daemon.h olp_parser.h[%
@end @if %]
lib@GENERIC_LIBRARY_NAME@_la_SOURCES=olp_module.f90

nodist_pkginclude_HEADERS=olp_module.mod
pkginclude_HEADERS=olp.h

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
ACLOCAL_AMFLAGS=-I m4[%
@if internal OLP_DAEMON %]

olp_lexer.c: olp_parser.h[%
@end @if %]

OBJEXT ?=o
OBJEXTG=[%@if extension autotools %]lo[% @else %]$(OBJEXT)[%@end @if%]

olp_module.mod: olp_module.$(OBJEXTG)
