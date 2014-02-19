[%' vim: syntax=golem
	 This template defines the Makefiles that go under
    <process_dir>/helicity*/
'%]# vim: ts=3:sw=3

[% @if internal OLP_MODE %]
include ../../Makefile.conf[%
@else %]
include ../Makefile.conf[%
@end @if %]


HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)[%
@if diagsum %]
HAVE_ORIG_DIAGRAM_FILE=$(if $(shell grep 'Local' ../diagrams-1.hh),1,0)[%
@end @if %]

OBJECTS= \
	globals.o amplitudeh[%helicity%].o[%
@select r2
@case implicit explicit off %][%
   @if extension golem95 %] golem95h[%helicity%].o[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].o[%
   @end @if %][%
   @if extension ninja %] ninjah[%helicity%].o[%
   @end @if %][%
@end @select %][%
@if generate_lo_diagrams %] \
	diagramsl0.o[%
   @if group %][%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0.o[%
      @end @for %][%
   @end @if %][%
   @if internal REQUIRE_FR5 %] \
	   diagramsl0fr5.o[%
      @if group %][%
		@else %][%
         @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0fr5.o[%
         @end @for %][%
      @end @if %][%
   @end @if %][%
@end @if generate_lo_diagrams %][%
@if generate_nlo_virt %][%
   @select abbrev.level
   @case helicity %] \
	abbrevh[%helicity%].o[%
   @case group %][%
      @for groups var=grp %] \
	abbrevg[%grp%]h[%helicity%].o[%
      @end @for %][%
   @case diagram %][%
      @for elements topolopy.keep.virt %] \
	abbrevd[%$_%]h[%helicity%].o[%
      @end @for %][%
   @end @select %][%
	@select r2
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]h[%helicity%]l1.o[%
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]h[%helicity%]l1d.o[%
			@end @if %][%
		   @if extension ninja %] \
	d[%$_%]h[%helicity%]l131.o \
	d[%$_%]h[%helicity%]l132.o \
	d[%$_%]h[%helicity%]l121.o[%
			@end @if %][%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %][%
@if generate_uv_counterterms %] \
	diagramsct.o[%
	@for elements topolopy.keep.ct %] \
	d[%$_%]h[%helicity%]l1c.o[%
	@end @for %][%
@end @if %]
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
		   @if internal GENERATE_DERIVATIVES %] \
	d[%$_%]h[%helicity%]l1d.f90[%
			@end @if %][%
		   @if extension ninja %] \
	d[%$_%]h[%helicity%]l131.f90 \
	d[%$_%]h[%helicity%]l132.f90 \
	d[%$_%]h[%helicity%]l121.f90[%
			@end @if %][%
	@end @for %][%
	@end @select %][%
@end @if generate_nlo_virt %][%
@if generate_uv_counterterms %][%
	@for elements topolopy.keep.ct %] \
	d[%$_%]h[%helicity%]l1c.f90[%
	@end @for %] \
	diagramsct.f90 [%
@end @if %]

.PHONY: compile source clean very-clean doc
.SUFFIXES:

compile: source amplitude[%helicity%].a

source:[%
@if diagsum %]
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell mv ../diagrams-1.hh ../diags-1.hh)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diags-1.hh >> ../diagrams-1.hh)
	$(shell rm ../diags-1.hh)
endif[%
@end @if %]
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif

[% @for elements topolopy.keep.virt %]

d[%$_%]h[%helicity%]l1:[%
@if diagsum %]
ifeq ($(HAVE_ORIG_DIAGRAM_FILE),1)
	$(shell mv ../diagrams-1.hh ../diags-1.hh)
	$(shell sed -e "s/Local diagram/Id diag/g" ../diags-1.hh >> ../diagrams-1.hh)
	$(shell rm ../diags-1.hh)
endif[%
@end @if %]
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source d[%$_%]h[%helicity%]l1.txt
	$(MAKE) $(S) -f Makefile.source d[%$_%]h[%helicity%]l1.f90
	$(MAKE) $(S) -f Makefile.source abbrevd[%$_%]h[%helicity%].f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o abbrevd[%$_%]h[%helicity%].o -I../common abbrevd[%$_%]h[%helicity%].f90
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o d[%$_%]h[%helicity%]l1.o -I../common d[%$_%]h[%helicity%]l1.f90
endif

[% @end @for %]

$(GENERATED_SRC): %:
	@if [ -f Makefile.source ]; \
	then \
		$(MAKE) $(S) -f Makefile.source "$@"; \
	fi

$(OBJECTS): %.o: %.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ -I../common $<

amplitude[%helicity%].a: $(OBJECTS)
	$(Q) ar rs $@ $+

doc:

clean:
	$(Q)$(FIND) $(FIND_OPT) . \( -name '*.o' \
		-or -name '*.mod' \) \
		-exec rm \{} \;

very-clean: clean
	$(Q)rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name 'd*h[%helicity%]l[01].f90' \
		-or -name 'd*h[%helicity%]l[01]fr5.f90' \
		-or -name 'd*h[%helicity%]l[01].txt' \
		-or -name 'd*h[%helicity%]l1[23d].txt' \
		-or -name 'd*h[%helicity%]l1[23d].f90' \
		-or -name 'd*h[%helicity%]l[01]c.txt' \
		-or -name 'd*h[%helicity%]l[01]c.f90' \
		-or -name 'd*h[%helicity%]l[01]d.txt' \
		-or -name 'd*h[%helicity%]l1d.txt' \
		-or -name 'd*h[%helicity%]l1d.f90' \
		-or -name 'd*h[%helicity%]l[01]-fr.txt' \
		-or -name 'd*h[%helicity%]l[01].dat' \
		-or -name 'd*h[%helicity%]l[01].abb'[%
@if group %] \
		-or -name 'diagramsl0.f90'[%
@end @if %][%
@if extension formopt %] \
		-or -name 'abbrevd*h[%helicity%].f90' \
		-or -name 'd*h[%helicity%]l[01].prc' \
		-or -name 'borndiag.prc' \
		-or -name 'born.txt' [%
@end @if %] \
		-or -name 'lightconedecomp.prc' \
		\) -exec rm \{} \;
endif

filelist-source: source
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name 'Makefile' \
		-or -name 'Makefile.dep' \
		\) -fprint $@

include Makefile.dep
