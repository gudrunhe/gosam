PROCESS1=udhud_feynman
PROCESS2=udhud_unitary

ifndef GOSAM
GOSAM=gosam.py
endif
GOSAM_RC1=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS1).rc
GOSAM_RC2=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS2).rc

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif


.PHONY: all gosam test comptest clean very-clean

all: gosam test comptest

test: comptest
	@echo Running test program
	$(MAKE) ENABLE_CODE_CHECK=$(ENABLE_CODE_CHECK) -C test test

comptest: gosam
	$(MAKE) -C test compile

gosam: $(PROCESS1).log $(PROCESS2).log
ifeq ($(ENABLE_CODE_CHECK),true)
	cd $(PROCESS1); meson setup build --prefix ${CURDIR}/$(PROCESS1) --warnlevel 3 -Dcode_check=True; cd build; meson compile; meson install
	cd $(PROCESS2); meson setup build --prefix ${CURDIR}/$(PROCESS2) --warnlevel 3 -Dcode_check=True; cd build; meson compile; meson install
else
	cd $(PROCESS1); meson setup build --prefix ${CURDIR}/$(PROCESS1); cd build; meson compile; meson install
	cd $(PROCESS2); meson setup build --prefix ${CURDIR}/$(PROCESS2); cd build; meson compile; meson install
endif

$(PROCESS1).log: $(PROCESS1).in
	@echo setting up $(PROCESS1)...
	@if [ ! -d $(PROCESS1) ]; then mkdir $(PROCESS1); fi
	$(GOSAM) -z $< -l $@

$(PROCESS2).log: $(PROCESS2).in
	@echo setting up $(PROCESS2)...
	@if [ ! -d $(PROCESS2) ]; then mkdir $(PROCESS2); fi
	$(GOSAM) -z $< -l $@

$(PROCESS1).in: $(PROCESS1).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC1) -t $@

$(PROCESS2).in: $(PROCESS2).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC2) -t $@

very-clean:
	rm -f $(PROCESS1).in $(PROCESS1).log
	rm -f $(PROCESS2).in $(PROCESS2).log
	$(MAKE) -C test clean
	rm -f $(PROCESS1)/.golem.dir
	rm -f $(PROCESS2)/.golem.dir
	rm -fr $(PROCESS1)
	rm -fr $(PROCESS2)
