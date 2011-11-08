[%' vim: syntax=golem
	 This template defines the Makefiles that go under
    <process_dir>/helicity*/
'%]# vim: ts=3:sw=3

include ../Makefile.conf

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

OBJECTS= \
	globals.o amplitudeh[%helicity%].o[%
@select r2 default=implicit
@case implicit explicit off %][%
   @if extension golem95 %] golem95h[%helicity%].o[%
   @end @if %][%
   @if extension samurai %] samuraih[%helicity%].o[%
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
   @if extension fr5 %] \
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
	@select r2 default=implicit
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]h[%helicity%]l1.o[%
      @end @for %][%
   @end @select %][%
@end @if generate_nlo_virt %]

GENERATED_SRC=[%
@if generate_lo_diagrams %][%
   @if group %] \
	diagramsl0.f90[%
   @else %][% 
      @for elements topolopy.keep.tree %] \
	d[%$_%]h[%helicity%]l0.f90[%
      @end @for %][%
   @end @if %][%
   @if extension fr5 %][%
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
	@select r2 default=implicit
	@case implicit explicit off %][%
      @for elements topolopy.keep.virt %] \
	d[%$_%]h[%helicity%]l1.f90[%
   	@end @for %][%
	@end @select %][%
@end @if generate_nlo_virt %]

.PHONY: compile source clean very-clean doc
.SUFFIXES:

compile: source amplitude[%helicity%].a

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) -f Makefile.source source
endif

$(GENERATED_SRC): %:
	@if [ -f Makefile.source ]; \
	then \
		$(MAKE) -f Makefile.source "$@"; \
	fi

$(OBJECTS): %.o: %.f90
	$(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ -I../common $<

amplitude[%helicity%].a: $(OBJECTS)
	ar rs $@ $+

doc:

clean:
	$(FIND) $(FIND_OPT) . \( -name '*.o' \
		-or -name '*.mod' \) \
		-exec rm \{} \;

very-clean: clean
	rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(FIND) $(FIND_OPT) . \( \
		-name 'd*l[01].f90' \
		-or -name 'd*l[01]fr5.f90' \
		-or -name 'd*l[01].txt' \
		-or -name 'd*l[01]-fr.txt' \
		-or -name 'd*l[01].dat' \
		-or -name 'd*l[01].abb' \
		-or -name 'lightconedecomp.prc' \
		\) -exec rm \{} \;
endif

filelist-source: source
	$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name 'Makefile' \
		-or -name 'Makefile.dep' \
		\) -fprint $@

include Makefile.dep
