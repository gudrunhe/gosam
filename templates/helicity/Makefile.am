noinst_LTLIBRARIES=libgolem_process[% process_name assuffix=\_ %]_helicity[%helicity%].la
libgolem_process[% process_name assuffix=\_ %]_helicity[%helicity%]_la_SOURCES= \
	globals.f90 amplitudeh[%helicity%].f90[%
@if helsum%][%
@else%][%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95h[%helicity%].f90[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].f90[%
   @end @if %][%
   @if extension ninja %] ninjah[%helicity%].f90[%
   @end @if %][%
@end @select %][%
@end @if helsum %][%
@if generate_lo_diagrams %] \
	diagramsl0.f90[%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	diagramsl0fr5.f90[%
      @if group %][%
      @else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0fr5.f90[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]h[%helicity%].f90[%
      @end @for %][%
   @end @select %][%
   @select r2
   @case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]h[%helicity%]l1.f90[%
         @if internal GENERATE_DERIVATIVES %] d[%$_%]h[%helicity%]l1d.f90[%
         @end @if %][%
         @if extension ninja %] d[%$_%]h[%helicity%]l131.f90  d[%$_%]h[%helicity%]l132.f90  d[%$_%]h[%helicity%]l121.f90[%
         @end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %]

nodist_pkginclude_HEADERS=[%
	process_name asprefix=\_ %]globalsh[% helicity %].mod [%
	process_name asprefix=\_ %]amplitudeh[%helicity%].mod[%
@if helsum %][%
@else %][%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] \
        [% process_name asprefix=\_ %]golem95h[%helicity%].mod[%
   @end @if %][%
   @if extension samurai %] \
	[% process_name asprefix=\_ %]samuraih[%helicity%].mod[%
   @end @if %][%
   @if extension ninja %] \
	[% process_name asprefix=\_ %]ninjah[%helicity%].mod[%
   @end @if %][%
@end @select %][%
@end @if %][%
@if generate_lo_diagrams %] \
	[% process_name asprefix=\_ %]diagramsh[% helicity %]l0.mod[%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	[% process_name asprefix=\_ %]d[%$_%]h[%helicity%]l0.mod[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	[% process_name asprefix=\_ %]diagramsh[%helicity%]l0fr5.mod[%
      @if group %][%
      @else %][%
         @for elements topolopy.keep.tree %] \
	[% process_name asprefix=\_ %]d[%$_%]h[%helicity%]l0fr5.mod[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	[% process_name asprefix=\_ %]abbrevh[%helicity%].mod[%
   @case group %][%
      @for groups var=grp %] \
	[% process_name asprefix=\_ %]abbrevg[%grp%]h[%helicity%].mod[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	[% process_name asprefix=\_ %]abbrevd[%$_%]h[%helicity%].mod[%
      @end @for %][%
   @end @select %][%
   @select r2
   @case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	[% process_name asprefix=\_ %]d[%$_%]h[%helicity%]l1.mod[%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@end @if helsum %]

CLEANFILES=$(nodist_pkginclude_HEADERS)
ACLOCAL_AMFLAGS=-I m4

AM_FCFLAGS=$(GOLEM_CONFIG_FCFLAGS) -I../common
AM_LDFLAGS=$(GOLEM_CONFIG_LDFLAGS)

GENERATED_SRC=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0.f90[%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %][%
      @if group %] \
	diagramsl0fr5.f90[%
      @else %][% 
         @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0fr5.f90[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if helsum %][%
@else %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].f90[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].f90[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]h[%helicity%].f90[%
      @end @for %][%
   @end @select %][%
   @for elements topolopy.keep.virt %] \
	d[%$_%]h[%helicity%]l1.f90[%
      @if internal GENERATE_DERIVATIVES %] d[%$_%]h[%helicity%]l1d.f90[%
      @end @if %][%
      @if extension ninja %] d[%$_%]h[%helicity%]l131.f90  d[%$_%]h[%helicity%]l132.f90  d[%$_%]h[%helicity%]l121.f90[%
      @end @if %][%
   @end @for %][%
@end @if generate_nlo_virt %][%
@end @if helsum %]

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
