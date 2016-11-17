[% ' vim: syntax=golem
%]

[% @if internal OLP_MODE %]
include ../../Makefile.conf[%
@else %]
include ../Makefile.conf[%
@end @if %]


PROCESS_CFLAGS=[% @if extension reduze %][% @else %][%
    @if helsum %] \
		-I../sum[%
    @end @if %][%
    @for helicities generated %] \
		-I../helicity[%helicity%][%
    @end @for helicities %][% @end @if %] \
		-I../common

PROCESS_LDFLAGS=$(shell ${SHELL} ../config.sh -plibs)

PROCESS_DEPS=$(shell ${SHELL} ../config.sh -deps)

OBJECTS=matrix.o[%
   @for crossings %] \
	[% $_ asprefix=\_ %]matrix.o[%
   @end @for %]

.PHONY: source compile clean very-clean doc
.SUFFIXES:

[% @if extension shared %]
compile: libgosam_process[% process_name assuffix=\_ %]_matrix.so
[% @else %]
compile: matrix.a
[% @end @if %]

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif

[% @if extension shared %]
libgosam_process[% process_name assuffix=\_ %]_matrix.so: $(OBJECTS)
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -Wl,-rpath="\$ORIGIN/../common" [%
	@for helicities generated %]-Wl,-rpath="\$ORIGIN/../helicity[%helicity%]" [%@end @for
        %] -shared -o $@ $+
[% @else %]
matrix.a: $(OBJECTS)
	$(Q) ar rs $@ $+
[% @end @if %]

$(OBJECTS) test.o:%.o:%.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

ph_test.o:%.o:%.f
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(PROCESS_CFLAGS) $(FCFLAGS) -c -o $@ $<

%.exe: %.o $(OBJECTS) $(PROCESS_DEPS)
	$(vecho) "-> Creating executable $@ .."
	$(Q) $(FC) -o $@ $+ $(PROCESS_LDFLAGS) $(LDFLAGS)

[% @if extension shared %]
clean:
	$(Q)rm -f *.o *.mod libgosam_process[% process_name assuffix=\_ %]_matrix.so
[% @else %]
clean:
	$(Q)rm -f *.o *.mod matrix.a
[% @end @if %]

very-clean: clean
	$(Q)rm -f filelist-source

filelist-source: source
	@ $(FIND) $(FIND_OPT) . \( \
		-name "Makefile" -or \
		-name "Makefile.dep" -or \
		-name "ph_test.f" -or \
		-name "test.f90" -or \
		-name "ltest.dat" \
	\) -print >> $@
	@for f in $(subst .o,.f90,$(OBJECTS)); \
	do \
		echo $${f} >> $@; \
	done

include Makefile.dep
