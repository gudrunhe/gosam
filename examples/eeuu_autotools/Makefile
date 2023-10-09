
PROCESS=eeuu

GOSAM=gosam.py
GOSAM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

.PHONY: all gosam test comptest clean gosam_install

all: gosam test

test: comptest
	@echo Running test programm
	$(MAKE) -C test test

comptest: gosam_install
	$(MAKE) -C test compile

gosam: $(PROCESS).log virtual/Makefile
	$(MAKE) -C virtual

gosam_install: gosam
	$(MAKE) -C virtual install

virtual/Makefile: $(PROCESS).log
	(cd virtual && sh ./autogen.sh --prefix="$(shell pwd)" --libdir="$(shell pwd)/lib")

$(PROCESS).log: $(PROCESS).in
	@echo setting up virtual ...
	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	-$(MAKE) -C virtual uninstall
	-$(MAKE) -C virtual clean
	rm -f virtual/.golem.dir
	rm -f virtual/Makefile
	rm -fr include
	rm -fr lib lib64

very-clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	-$(MAKE) -C virtual uninstall
	-$(MAKE) -C virtual clean
	rm -fr virtual
	rm -fr include
	rm -fr lib lib64

