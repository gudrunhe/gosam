include ../../../Makefile.conf

SRCS=$(wildcard *.py)
FORMHEADERS=$(SRCS:.py=.hh)

%.hh: %.py
	@echo Secdec is decomposing integral $(subst .py,,$<)
	@$(PYTHON) $< > $<.python.log
	@$(MAKE) dynamic -C $(subst .py,,$<) > $<.make.log

.PHONY: decompose-stamp

# TODO: Rewrite this make command
decompose-stamp: $(FORMHEADERS) secdec_replace_integrals.hh
	cat ReduzeF*.hh > secdecordersl1.hh
	cp secdecordersl1.hh ../../../amplitude/secdecordersl1.hh
	cp secdec_replace_integrals.hh ../../../amplitude/secdecnamesl1.hh
	find . -maxdepth 2 -name "*.hpp" | xargs -n 1 -I f sh -c 'cp f ../../../amplitude/integrals/include/$$(basename f)'
	find . -maxdepth 2 -name "lib*.so" | xargs -n 1 -I f sh -c 'cp f ../../../amplitude/integrals/lib/$$(basename f)'
	touch decompose-stamp
