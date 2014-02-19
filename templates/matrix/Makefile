[% ' vim: syntax=golem
%]

[% @if internal OLP_MODE %]
include ../../Makefile.conf[%
@else %]
include ../Makefile.conf[%
@end @if %]


PROCESS_CFLAGS=[%
	@for helicities %] \
		-I../helicity[%helicity%][%
	@end @for helicities %] \
		-I../common

PROCESS_LDFLAGS=$(shell ${SHELL} ../config.sh -plibs)

OBJECTS=matrix.o[%
   @for crossings %] \
	[% $_ asprefix=\_ %]matrix.o[%
   @end @for %]

.PHONY: source compile clean very-clean doc
.SUFFIXES:

compile: matrix.a

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif

matrix.a: $(OBJECTS)
	ar rs $@ $+

$(OBJECTS) test.o:%.o:%.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

ph_test.o:%.o:%.f
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

%.exe: %.o $(OBJECTS)
	$(vecho) "-> Creating executable $@ .."
	$(Q) $(FC) -o $@ $+ $(PROCESS_LDFLAGS) $(LDFLAGS)

clean:
	$(Q)rm -f *.o *.mod

very-clean: clean
	$(Q)rm -f filelist-source

filelist-source: source
	@ $(FIND) $(FIND_OPT) . \( \
		-name "Makefile" -or \
		-name "Makefile.dep" -or \
		-name "ph_test.f" -or \
		-name "test.f90" -or \
		-name "ltest.dat" \
	\) -fprint $@
	@for f in $(subst .o,.f90,$(OBJECTS)); \
	do \
		echo $${f} >> $@; \
	done

include Makefile.dep
