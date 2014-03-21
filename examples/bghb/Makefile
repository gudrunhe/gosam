
PROCESS=bghb

GOSAM=gosam.py
GOSAM_RC=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS).rc

.PHONY: all golem ntest test clean

all: golem ntest

test: ntest
	@echo Running test programm
	$(MAKE) -C ntest test

ntest: golem
	$(MAKE) -C ntest compile

golem: $(PROCESS).log
	$(MAKE) -C ngolem compile

$(PROCESS).log: $(PROCESS).in
	@echo setting up ngolem ...
	@if [ ! -d ngolem ]; then mkdir ngolem; fi
	$(GOSAM) -z $< -l $@

$(PROCESS).in: $(PROCESS).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC) -t $@

clean:
	rm -f $(PROCESS).in $(PROCESS).log
	$(MAKE) -C ntest clean
	rm -f ngolem/.golem.dir
	$(MAKE) -C ngolem clean
