vim: ts=3:sw=3

include ../Makefile.conf

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

.PHONY: source

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif