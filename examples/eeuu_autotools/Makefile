
PROCESS=eeuu

GOLEM=gosam.py
GOLEM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

.PHONY: all golem ntest test clean golem_install

all: golem ntest

test: ntest
	@echo Running test programm
	$(MAKE) -C ntest test

ntest: golem_install
	$(MAKE) -C ntest compile

golem: $(PROCESS).log ngolem/Makefile
	$(MAKE) -C ngolem

golem_install: golem
	$(MAKE) -C ngolem install

ngolem/Makefile:
	(cd ngolem && sh ./autogen.sh --prefix="$(shell pwd)")

$(PROCESS).log: $(PROCESS).in
	@echo setting up ngolem ...
	@if [ ! -d ngolem ]; then mkdir ngolem; fi
	$(GOLEM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOLEM) $(GOLEM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C ntest clean
	rm -f ngolem/.golem.dir
	rm -f ngolem/Makefile
	$(MAKE) -C ngolem clean
