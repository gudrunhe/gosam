
PROCESS=Hbb_4F

ifndef GOSAM
GOSAM=gosam.py
endif
GOSAM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif

.PHONY: all gosam test comptest clean very-clean

all: gosam test

test: comptest
	@echo Running test program
	$(MAKE) ENABLE_CODE_CHECK=$(ENABLE_CODE_CHECK) -C test test

comptest: gosam
	$(MAKE) -C test compile

gosam: $(PROCESS).log
ifeq ($(ENABLE_CODE_CHECK),true)
	cd virtual; meson setup build --prefix ${CURDIR}/virtual --warnlevel 3 -Dcode_check=True; cd build; meson compile; meson install
else
	cd virtual; meson setup build --prefix ${CURDIR}/virtual; cd build; meson compile; meson install
endif

$(PROCESS).log: $(PROCESS).in
	@echo setting up virtual ...
	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	rm -f virtual/.golem.dir
	cd virtual; meson clean

very-clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	rm -f virtual/.golem.dir
	rm -fr virtual
