
PROCESS=hyy

ifndef GOSAM
GOSAM=gosam.py
endif



.PHONY: all golem test comptest clean very-clean

all: golem test

test: comptest
	@echo Running test programm
	$(MAKE) -C test test

comptest: golem
	$(MAKE) -C test compile

golem: $(PROCESS).log
	cd virtual; meson setup build --prefix ${CURDIR}/virtual; cd build; meson compile; meson install

$(PROCESS).log:
	@echo setting up virtual ...
	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) --olp --config=setup.in --destination=virtual --ignore-unknown $(PROCESS).olp -l $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	cd virtual; meson clean
	rm -f virtual/.golem.dir
	cd virtual; meson clean

very-clean:
	rm -f $(PROCESS).in $(PROCESS).log $(PROCESS).olc
	$(MAKE) -C test clean
	rm -f virtual/.golem.dir
	rm -fr virtual
