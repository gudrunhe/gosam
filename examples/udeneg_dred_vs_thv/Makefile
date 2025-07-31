PROCESS1=udeneg_dred
PROCESS2=udeneg_thv

ifndef GOSAM
GOSAM=gosam.py
endif
GOSAM_RC1=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS1).rc
GOSAM_RC2=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS2).rc

.PHONY: all gosam test comptest clean very-clean

all: gosam test comptest

test: comptest
	@echo Running test programm
	$(MAKE) -C test test

comptest: gosam
	$(MAKE) -C test compile

gosam: $(PROCESS1).log $(PROCESS2).log
	cd $(PROCESS1); meson setup build --prefix ${CURDIR}/$(PROCESS1); cd build; meson compile; meson install
	cd $(PROCESS2); meson setup build --prefix ${CURDIR}/$(PROCESS2); cd build; meson compile; meson install

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
