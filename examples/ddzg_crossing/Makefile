
PROCESS1=ddzg
PROCESS2=dgzd

GOSAM=gosam.py
GOSAM_RC1=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS1).rc
GOSAM_RC2=$(addprefix -m ,$(wildcard ../setup.in)) -m $(PROCESS2).rc

.PHONY: all golem test comptest clean very-clean

all: golem test

test: comptest
	@echo Running test program
	$(MAKE) -C test test

comptest: golem
	$(MAKE) -C test compile

golem: $(PROCESS1).log $(PROCESS2).log
	$(MAKE) -C $(PROCESS1) compile
	$(MAKE) -C $(PROCESS2) compile

$(PROCESS1).log: $(PROCESS1).in
	@echo setting up $(PROCESS1) ...
	@if [ ! -d $(PROCESS1) ]; then mkdir $(PROCESS1); fi
	$(GOSAM) -z $< -l $@

$(PROCESS2).log: $(PROCESS2).in
	@echo setting up $(PROCESS2) ...
	@if [ ! -d $(PROCESS2) ]; then mkdir $(PROCESS2); fi
	$(GOSAM) -z $< -l $@

$(PROCESS1).in: $(PROCESS1).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC1) -t $@

$(PROCESS2).in: $(PROCESS2).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC2) -t $@

clean:
	rm -f $(PROCESS1).in $(PROCESS1).log
	$(MAKE) -C $(PROCESS1) clean
	rm -f $(PROCESS1)/.golem.dir
	$(MAKE) -C test clean

very-clean:
	rm -f $(PROCESS1).in $(PROCESS1).log
	rm -f $(PROCESS2).in $(PROCESS2).log
	$(MAKE) -C test clean
	rm -f $(PROCESS1)/.golem.dir
	rm -f $(PROCESS2)/.golem.dir
	rm -fr $(PROCESS1)
	rm -fr $(PROCESS2)


