vim: ts=3:sw=3

include ../../../../Makefile.conf

# @date: [% time_stamp format=%x~%X %]

FORM_OPT= \
	-D PROCESSPATH=../../../../ \
	-D PWD=. \
	-p ../../..:../../../..:../../../../codegen \
	-M -q

INSERTEDINTS=$(wildcard INT*.in)
BACKSUBINTS=$(INSERTEDINTS:.in=.backsub)
COEFFS=$(INSERTEDINTS:%.in=../../../coefficients/[%loop%]loop/codegen/%.coeff)

.PHONY: backsub coeff

backsub: $(BACKSUBINTS)

%.backsub : %.in
	@echo Form is back substituting in integral $(basename $<) @ [%loop%] loop
	@$(FORM) $(FORM_OPT) \
		-w$(FORM_THREADS) \
		-D LOOPS=[%loop%] \
		-D ORD=2 \
		-D INTEGRAL=$(basename $<) \
		../../../../codegen/golemreduzebacksub.frm


coeff: $(COEFFS)

../../../coefficients/[%loop%]loop/codegen/%.coeff : %.backsub
	@echo Form is preparing coefficients for integral $(basename $<) @ [%loop%] loop
	@$(FORM) $(FORM_OPT) \
		-w$(FORM_THREADS) \
		-D LOOPS=[%loop%] \
		-D ORD=2 \
		-D INTEGRAL=$(basename $<) \
		../../../../codegen/golemreduzecoeff.frm
