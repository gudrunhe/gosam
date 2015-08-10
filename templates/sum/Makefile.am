noinst_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %]_sum.la
libgolem_process[% process_name assuffix=\_ %]_sum_la_SOURCES= \
	globals.f90 amplitude.f90[%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95.f90[%
   @end @if %][%
   @if extension samurai %] samurai.f90[%
   @end @if %][%
   @if extension ninja %] ninja.f90[%
   @end @if %][%
@end @select %][%
@if generate_lo_diagrams %] \
	diagramsl0.f90[%
@end @if generate_lo_diagrams %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrev.f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%].f90[%
      @end @for %][%
   @end @select %][%
   @select r2
   @case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]l1.f90[%
         @if internal GENERATE_DERIVATIVES %] d[%$_%]l1d.f90[%
         @end @if %][%
         @if extension ninja %] d[%$_%]l131.f90  d[%$_%]l132.f90  d[%$_%]l121.f90[%
         @end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %]

nodist_pkginclude_HEADERS=[%
	process_name asprefix=\_ %]globals.mod [%
	process_name asprefix=\_ %]amplitude.mod[%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] \
        [% process_name asprefix=\_ %]golem95.mod[%
   @end @if %][%
   @if extension samurai %] \
	[% process_name asprefix=\_ %]samurai.mod[%
   @end @if %][%
   @if extension ninja %] \
	[% process_name asprefix=\_ %]ninja.mod[%
   @end @if %][%
@end @select %][%
@if generate_lo_diagrams %] \
	[% process_name asprefix=\_ %]diagramsl0.mod[%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	[% process_name asprefix=\_ %]d[%$_%]l0.mod[%
      @end @for %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	[% process_name asprefix=\_ %]abbrev.mod[%
   @case group %][%
      @for groups var=grp %] \
	[% process_name asprefix=\_ %]abbrevg[%grp%].mod[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	[% process_name asprefix=\_ %]abbrevd[%$_%].mod[%
      @end @for %][%
   @end @select %][%
   @select r2
   @case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	[% process_name asprefix=\_ %]d[%$_%]l1.mod[%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %]

CLEANFILES=$(nodist_pkginclude_HEADERS)
ACLOCAL_AMFLAGS=-I m4

AM_FCFLAGS=$(GOLEM_CONFIG_FCFLAGS) -I../common[%
   @for helicities generated %] \
	   -I../helicity[%helicity%][%
   @end @for %]
AM_LDFLAGS=$(GOLEM_CONFIG_LDFLAGS)

GENERATED_SRC=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0.f90[%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	d[%$_%]l0.f90[%
      @end @for %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrev.f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%].f90[%
      @end @for %][%
   @end @select %][%
   @for elements topolopy.keep.virt %] \
	d[%$_%]l1.f90[%
      @if internal GENERATE_DERIVATIVES %] d[%$_%]l1d.f90[%
      @end @if %][%
      @if extension ninja %] d[%$_%]l131.f90  d[%$_%]l132.f90  d[%$_%]l121.f90[%
      @end @if %][%
   @end @for %][%
@end @if generate_nlo_virt %]

$(GENERATED_SRC): %: source

TEMPFILE:=$(shell mktemp -u -t gosam.tempfile.XXXXXX || echo gosam.tempfile.tmp)

source:
[% @if diagsum %]
	@if [ -e ../diagrams-1.hh ] && head -n 100 ../diagrams-1.hh | grep -q 'Local' ; \
	then \
		sed -e "s/Local diagram/Id diag/g" ../diagrams-1.hh > $(TEMPFILE); \
		mv $(TEMPFILE) ../diagrams-1.hh ; \
	fi[%
@end @if %]
	@if [ -f Makefile.source ]; \
	then \
		$(MAKE) -f Makefile.source ; \
	fi

include Makefile.dep
