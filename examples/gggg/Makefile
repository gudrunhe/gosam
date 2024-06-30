
PROCESS=gggg

GOSAM=gosam.py
GOSAM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

.PHONY: all gosam test comptest clean fort

all: gosam fort test

test: comptest
	@echo Running test programm
	$(MAKE) -C test test

fort: gosam
	$(MAKE) -C fort all

comptest: gosam fort
	$(MAKE) -C test compile

gosam: $(PROCESS).log
	cd virtual; meson setup build --prefix ${CURDIR}/virtual; cd build; meson compile; meson install

$(PROCESS).log: $(PROCESS).in
	@echo setting up virtual ...
	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	cd virtual; meson clean
	$(MAKE) -C fort clean
	rm -f virtual/.golem.dir

very-clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	$(MAKE) -C fort clean
	rm -f virtual/.golem.dir
	rm -fr virtual
