vim: ts=3:sw=3

include ../../../../Makefile.conf

# @date: [% time_stamp format=%x~%X %]

FORM_OPT= \
	-D PROCESSPATH=.. \
	-D PWD=. \
	-p ../../../..:../../../../codegen \
	-M -q

COEFFS=$(wildcard *.coeff)
SOURCES=$(COEFFS:.coeff=.cc)

.PHONY: source
source: $(SOURCES)

%.cc : %.coeff
	@echo Form is generating code for $< @ [%loop%] loop
	@$(FORM) $(FORM_OPT) \
		-w$(FORM_THREADS) \
		-D LOOPS=[%loop%] \
		-D ORD=2 \
		-D COFILE=$< \
		../../../../codegen/golemreduzecode.frm
