include ../../../Makefile.conf

SRCS=$(wildcard *.py)
FORMHEADERS=$(SRCS:.py=.hh)

%.hh: %.py
	@echo Secdec is decomposing integral $(subst .py,,$<)
	@$(PYTHON) $<
	@$(MAKE) dynamic -C $(subst .py,,$<)

.PHONY: decompose-stamp

# TODO: Rewrite this make command
decompose-stamp: $(FORMHEADERS)
	cat ReduzeF*.hh > secdecordersl1.hh
	cp secdecordersl1.hh ../../../amplitude/secdecordersl1.hh
	cp secdec_replace_integrals.hh ../../../amplitude/secdecnamesl1.hh
	find . -maxdepth 2 -name "*.hpp" | xargs -n 1 -I f sh -c 'mv f ../../../amplitude/integrals/include/$$(basename f)'
	find . -maxdepth 2 -name "lib*.so" | xargs -n 1 -I f sh -c 'mv f ../../../amplitude/integrals/lib/$$(basename f)'
	touch decompose-stamp
