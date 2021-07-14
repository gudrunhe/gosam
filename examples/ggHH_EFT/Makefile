# Born files generation
PROCESS0=pb0_gghh
PROCESS1=pb1_gghh


# files to be modified for correct normalization
fCONFIG=pb0_gghh/common/config.f90
fKINEMATICS=pb1_gghh/common/kinematics.f90


# GOSAM=gosam.py
GOSAM=/home/jankins/PhD/GoSam/1loop/local2/bin/gosam.py

GOSAM_RC0=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS0).rc
GOSAM_RC1=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS1).rc

.PHONY: all gosam test comptest clean very-clean

OLP:
	$(GOSAM) --olp --mc=powhegbox --config=OLP_files/gosam.rc --ignore-unknown --force --destination=OLPVIRT/ OLP_files/orderfile.lh

all: gosam

# test: comptest
# 	@echo Running test programm
# 	$(MAKE) -C test test
#
# comptest: gosam
# 	$(MAKE) -C test compile

gosam: $(PROCESS0).log $(PROCESS1).log
	$(MAKE) -C $(PROCESS0) compile
	$(MAKE) -C $(PROCESS1) compile

$(PROCESS0).log: $(PROCESS0).in
	@echo setting up virtual ...
#	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@
	@sed -i 's/renorm_beta =.*/renorm_beta = .false./' $(fCONFIG)

$(PROCESS0).in: $(PROCESS0).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC0) -t $@

$(PROCESS1).log: $(PROCESS1).in
	@echo setting up virtual ...
#	@if [ ! -d virtual ]; then mkdir virtual; fi
	$(GOSAM) -z $< -l $@
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(fKINEMATICS)

$(PROCESS1).in: $(PROCESS1).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC1) -t $@

clean:
	rm -f $(PROCESS0).in $(PROCESS0).log
	rm -f $(PROCESS1).in $(PROCESS1).log
	$(MAKE) -C test clean
	rm -f virtual/.gosam.dir
	$(MAKE) -C virtual clean

very-clean:
	rm -f $(PROCESS0).in $(PROCESS0).log
	rm -f $(PROCESS1).in $(PROCESS1).log
	rm -f gosam.crashed
	rm -f virtual/.gosam.dir
	rm -fr virtual
	rm -f $(PROCESS0)/.gosam.dir
	rm -fr $(PROCESS0)
	rm -f $(PROCESS1)/.gosam.dir
	rm -fr $(PROCESS1)
	# $(MAKE) -C test clean
