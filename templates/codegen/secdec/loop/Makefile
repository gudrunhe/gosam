include ../../../Makefile.conf

SRCS=$(wildcard *.py)
FORMHEADERS=$(SRCS:.py=.hh)

%.hh: %.py
	@echo Secdec is decomposing integral $(subst .py,,$<)
	@$(PYTHON) $<

decompose: $(FORMHEADERS)
	cat ReduzeF*.hh > secdecordersl1.hh
	cp secdecordersl1.hh ../../../amplitude/secdecordersl1.hh
	cp secdec_replace_integrals.hh ../../../amplitude/secdecnamesl1.hh
