[% ' vim: syntax=golem
%]

include ../Makefile.conf

PROCESS_CFLAGS=[%
	@for helicities %] \
		-I../helicity[%helicity%][%
	@end @for helicities %] \
		-I../common

PROCESS_LDFLAGS=$(shell ${SHELL} ../config.sh -plibs)

OBJECTS=matrix.o[%
   @for crossings %] \
	[% $_ asprefix=\_ %]matrix.o[%
   @end @for %][%
   @if extension powhegbox %] \
	powhegbox.o[%
   @end @if %]

.PHONY: source compile clean very-clean doc
.SUFFIXES:

compile: matrix.a

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) -f Makefile.source source
endif

matrix.a: $(OBJECTS)
	ar rs $@ $+

$(OBJECTS) test.o:%.o:%.f90
	$(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

ph_test.o:%.o:%.f
	$(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

%.exe: %.o $(OBJECTS)
	$(FC) -o $@ $+ $(PROCESS_LDFLAGS) $(LDFLAGS)

clean:
	rm -f *.o *.mod

very-clean: clean
	rm -f filelist-source

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
