noinst_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %]_common.la
libgolem_process[% process_name assuffix=\_ %]_common_la_SOURCES=[%
@if extension pjfry %] \
	precision_pjfry.f90 pjfry95pg.f90 pjfry_comb.f90[%
@end @if %] \
	config.f90 accu.f90 model.f90 color.f90 rambo.f90 globalsl1.f90 \
	util.f90 scalar_cache.f90 kinematics.f90 dipoles.f90 version.f90[%
@select r2
@case implicit explicit off %] groups.f90[%
@end @select %][% @if internal CUSTOM_SPIN2_PROP %] custompropagator.f90[%
@end @if %]
nodist_pkginclude_HEADERS=[%
@if extension pjfry %] \
	[% process_name asprefix=\_ %]precision_pjfry.mod [%
           process_name asprefix=\_ %]pjfry95pg.mod [%
	   process_name asprefix=\_ %]pjfry_comb.mod[%
@end @if %] \
	[% process_name asprefix=\_ %]config.mod [%
           process_name asprefix=\_ %]accu.mod [%
	   process_name asprefix=\_ %]model.mod [%
	   process_name asprefix=\_ %]color.mod [%
	   process_name asprefix=\_ %]rambo.mod [%
	   process_name asprefix=\_ %]globalsl1.mod \
	[% process_name asprefix=\_ %]util.mod [%
	   process_name asprefix=\_ %]scalar_cache.mod [%
	   process_name asprefix=\_ %]kinematics.mod [%
	   process_name asprefix=\_ %]version.mod [%
	   process_name asprefix=\_ %]dipoles.mod[%
@select r2
@case implicit explicit off %] [%
	   process_name asprefix=\_ %]groups.mod[%
@end @select %][% @if internal CUSTOM_SPIN2_PROP %] [% process_name asprefix=\_ %]custompropagator.mod[%
@end @if %]


CLEANFILES=$(nodist_pkginclude_HEADERS)
ACLOCAL_AMFLAGS=-I m4

AM_FCFLAGS=$(GOLEM_CONFIG_FCFLAGS)
AM_LDFLAGS=$(GOLEM_CONFIG_LDFLAGS)

GENERATED_SRC=model.f90 color.f90 version.f90

$(GENERATED_SRC): %:
	@if [ -f Makefile.source ]; \
	then \
		$(MAKE) -f Makefile.source "$@"; \
	fi

include Makefile.dep
