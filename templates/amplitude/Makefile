vim: ts=3:sw=3

include ../Makefile.conf

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

INTS=$(patsubst %.so, %, $(patsubst integrals/lib/lib%, -l%, $(wildcard integrals/lib/*.so)))
[% @for loops_generated %]
COEFFS[%loop%]=$(patsubst %.so, %, $(patsubst coefficients/[%loop%]loop/src/lib%, -l%, $(wildcard coefficients/[%loop%]loop/src/*.so)))
[% @end @for %]
LDFLAGS=-Lintegrals/lib $(INTS) -Wl,-rpath,$(CURDIR)/integrals/lib [% @for loops_generated %] -Lcoefficients/[%loop%]loop/src $(COEFFS[%loop%]) -Wl,-rpath,$(CURDIR)/coefficients/[%loop%]loop/src [% @end @for %] 

.PHONY: [% @for loops_generated %] setup_reductionl[%loop%] prepare_reductionl[%loop%] reductionl[%loop%] backsubl[%loop%] secdecl[%loop%][% @end @for %]

.PHONY: source compile [% @for loops_generated %] compilel[%loop%][% @end @for %] clean very-clean

compile: [% @for loops_generated %] compilel[%loop%][% @end @for %]

[% @for loops_generated %]
compilel[%loop%] : source
	@$(MAKE) -C coefficients/[%loop%]loop/src compile_coeff-stamp

prepare_reductionl[%loop%]:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source $@
endif
reductionl[%loop%]:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source $@
endif

[% @end @for %]

prepare_reduction : [% @for loops_generated %] prepare_reductionl[%loop%][% @end @for %]
reduction : [% @for loops_generated %] reductionl[%loop%][% @end @for %]

test:
	$(CXX) $(CXXFLAGS) [% @for loops_generated %] -Icoefficients/[%loop%]loop/src [% @end @for %] -Iintegrals/include -o test.exe test.cpp $(LDFLAGS) $(SECDEC_CONTRIB)/lib/libcuba.a

clean:
	$(Q)$(FIND) $(FIND_OPT) . \( -name '*.o' \
		-or -name '*.mod' -or -name '*.a' -or -name '*.so' \) \
		-exec rm \{} \;

very-clean: clean
	$(Q)rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name '*.log' \
		-or -name '*.txt' \
		-or -name '*-stamp' \
		-or -name '*.m' \
		\) -exec rm \{} \;
endif

filelist-source: source # TODO: probably not correct
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name 'Makefile' \
		-or -name 'Makefile.dep' \
		\) -print > $@

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source all_source
endif
