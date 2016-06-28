# vim: ts=3:sw=3
HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

[% @if internal OLP_MODE %]
include ../../Makefile.conf[%
@else %]
include ../Makefile.conf[%
@end @if %]



OBJECTS=config.o kinematics.o dipoles.o model.o rambo.o util.o \
		  color.o accu.o version.o[%
@select r2
@case implicit explicit off %] groups.o[%
@end @select %] globalsl1.o scalar_cache.o[%
@if extension pjfry %] \
		  precision_pjfry.o pjfry95pg.o pjfry_comb.o[%
@end @if %][% @if internal CUSTOM_SPIN2_PROP %] custompropagator.o[%
@end @if %][%
@if generate_ct_internal %] ew_ct.o [%
@end @if %]

.PHONY: compile source clean very-clean doc
.SUFFIXES:

[% @if extension shared %]
compile: source libgosam_process[% process_name assuffix=\_ %]_common.so
[% @else %]
compile: source common.a
[% @end @if %]

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif

doc:

[% @if extension shared %]
libgosam_process[% process_name assuffix=\_ %]_common.so: $(OBJECTS)
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -shared -o $@ $+

clean:
	$(Q)rm -f *.o *.mod libgosam_process[% process_name assuffix=\_ %]_common.so
[% @else %]
common.a: $(OBJECTS)
	$(Q) ar rs $@ $+

clean:
	$(Q)rm -f *.o *.mod common.a
[% @end @if %]


very-clean: clean
	$(Q)rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(FIND) $(FIND_OPT) . \( \
		-name 'color.f90' \
		-or -name 'model.f90' \
		-or -name 'version.f90' \
		\) -exec rm \{} \;
endif

$(OBJECTS):%.o:%.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ $<

version.f90 color.f90 model.f90: source

filelist-source: source
	echo Makefile > $@
	echo Makefile.dep >> $@
	@for f in $(subst .o,.f90,$(OBJECTS)); \
	do \
		echo $${f} >> $@; \
	done

include Makefile.dep
