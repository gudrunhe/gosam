
PROCESS=gggh

GOSAM=gosam.py
GOSAM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

.PHONY: all gosam test comptest clean very-clean

all: gosam test

test: comptest
	@echo Running test programm
	$(MAKE) -C test test

comptest: gosam
	$(MAKE) -C test compile

gosam: $(PROCESS).log
	$(MAKE) -C virtual compile

$(PROCESS).log: $(PROCESS).in
	@echo setting up virtual ...
	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C test clean
	rm -f virtual/.gosam.dir
	$(MAKE) -C virtual clean

very-clean:	
	rm -f $(PROCESS).in $(PROCESS).log
	rm -f virtual/.gosam.dir
	rm -fr virtual
	$(MAKE) -C test clean

