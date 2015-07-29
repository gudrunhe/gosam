vim: ts=3:sw=3

include ../Makefile.conf

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

.PHONY: source compile clean very-clean [% @for loops_generated %] reductionl[%loop%] prepare_reductionl[%loop%][% @end @for %] prepare_reduction reduce

compile : source # TODO: recipe to come

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
		\) -exec rm \{} \;
endif

filelist-source: source # TODO: probably not correct
	$(Q)$(FIND) $(FIND_OPT) . \( \
		-name '*.f90' \
		-or -name 'Makefile' \
		-or -name 'Makefile.dep' \
		\) -fprint $@

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source all_source
endif
