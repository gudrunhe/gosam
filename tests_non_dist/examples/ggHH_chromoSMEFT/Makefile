# reals files generation
PROCESS16=pc16_gghh
PROCESS17=pc17_gghh

PROCESS18=pt18_gghh
PROCESS19=pt19_gghh

PROCESS0=pb0_gghh
PROCESS1=pb1_gghh


# files to be modified for correct normalization
PROC16_KINEMATICS=$(PROCESS16)/common/kinematics.f90
PROC17_CONFIG=$(PROCESS17)/common/config.f90

PROC0_CONFIG=pb0_gghh/common/config.f90
PROC1_KINEMATICS=pb1_gghh/common/kinematics.f90

PROC18_CONFIG=pt18_gghh/common/config.f90
PROC18_KINEMATICS=pt18_gghh/common/kinematics.f90
PROC18_KINEMATICS_qp=pt18_gghh/common/kinematics_qp.f90
PROC19_KINEMATICS=pt19_gghh/common/kinematics.f90
PROC19_KINEMATICS_qp=pt19_gghh/common/kinematics_qp.f90

# GOSAM=gosam.py
GOSAM=../../python3/bin/gosam.py
GOSAM-CHROMO=../../python3-chromo/bin/gosam.py
GOSAM-SMEFT=../../SMEFT/bin/gosam.py

GOSAM_RC16=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS16).rc
GOSAM_RC17=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS17).rc

GOSAM_RC18=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS18).rc
GOSAM_RC19=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS19).rc

GOSAM_RC0=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS0).rc
GOSAM_RC1=$(addprefix -m ,$(wildcard ../setup.in)) \
	 -m $(PROCESS1).rc



include ./Makefile.conf


.PHONY: all gosam test comptest clean very-clean

OLP:
	$(GOSAM) --olp --mc=powhegbox --config=OLP_files/gosam.rc --ignore-unknown --force --destination=OLPVIRT/ OLP_files/orderfile.lh

all: gosam

gosam: $(PROCESS16).log $(PROCESS17).log 
	$(MAKE) -C $(PROCESS16) compile
	$(MAKE) -C $(PROCESS17) compile

$(PROCESS17).log: $(PROCESS17).in
	@echo setting up $(PROCESS17) virtual ...
	@if [ ! -d $(PROCESS17) ]; then mkdir $(PROCESS17); fi
	$(GOSAM-CHROMO) -z $< -l $@
	@sed -i 's/renorm_beta =.*/renorm_beta = .false./' $(PROC17_CONFIG)
	@sed -i 's/renorm_decoupling =.*/renorm_decoupling = .false./' $(PROC17_CONFIG)
	@sed -i 's/renormalisation =.*/renormalisation = 0/' $(PROC17_CONFIG)

$(PROCESS17).in: $(PROCESS17).rc $(wildcard ../setup.in)
	$(GOSAM-CHROMO) $(GOSAM_RC17) -t $@

$(PROCESS16).log: $(PROCESS16).in
	@echo setting up $(PROCESS16) virtual ...
	@if [ ! -d $(PROCESS16) ]; then mkdir $(PROCESS16); fi
	$(GOSAM-CHROMO) -z $< -l $@
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC16_KINEMATICS)

$(PROCESS16).in: $(PROCESS16).rc $(wildcard ../setup.in)
	$(GOSAM-CHROMO) $(GOSAM_RC16) -t $@



$(PROCESS0).log: $(PROCESS0).in
	@echo setting up virtual ...
	@if [ ! -d $(PROCESS0) ]; then mkdir $(PROCESS0); fi
	$(GOSAM) -z $< -l $@
	@sed -i 's/renorm_beta =.*/renorm_beta = .false./' $(PROC0_CONFIG)
	@sed -i 's/renorm_decoupling =.*/renorm_decoupling = .false./' $(PROC0_CONFIG)
	@sed -i 's/renormalisation =.*/renormalisation = 0/' $(PROC0_CONFIG)

$(PROCESS0).in: $(PROCESS0).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC0) -t $@

$(PROCESS1).log: $(PROCESS1).in
	@echo setting up virtual ...
	@if [ ! -d $(PROCESS1) ]; then mkdir $(PROCESS1); fi
	$(GOSAM) -z $< -l $@
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC1_KINEMATICS)

$(PROCESS1).in: $(PROCESS1).rc $(wildcard ../setup.in)
	$(GOSAM) $(GOSAM_RC1) -t $@



$(PROCESS18).log: $(PROCESS18).in
	@echo setting up virtual ...
	@if [ ! -d $(PROCESS18) ]; then mkdir $(PROCESS18); fi
	$(GOSAM-SMEFT) -z $< -l $@
	@sed -i 's/renorm_beta =.*/renorm_beta = .false./' $(PROC18_CONFIG)
	@sed -i 's/renorm_decoupling =.*/renorm_decoupling = .false./' $(PROC18_CONFIG)
	@sed -i 's/renormalisation =.*/renormalisation = 0/' $(PROC18_CONFIG)
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC18_KINEMATICS)
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC18_KINEMATICS_qp)

$(PROCESS18).in: $(PROCESS18).rc $(wildcard ../setup.in)
	$(GOSAM-SMEFT) $(GOSAM_RC18) -t $@

$(PROCESS19).log: $(PROCESS19).in
	@echo setting up virtual ...
	@if [ ! -d $(PROCESS19) ]; then mkdir $(PROCESS19); fi
	$(GOSAM-SMEFT) -z $< -l $@
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC19_KINEMATICS)
	@sed -i 's/corrections_are_qcd =.*/corrections_are_qcd = .true./' $(PROC19_KINEMATICS_qp)

$(PROCESS19).in: $(PROCESS19).rc $(wildcard ../setup.in)
	$(GOSAM-SMEFT) $(GOSAM_RC19) -t $@




clean:
	rm -f $(PROCESS16).in $(PROCESS16).log
	rm -f $(PROCESS17).in $(PROCESS17).log
	rm -f $(PROCESS16)/.gosam.dir
	$(MAKE) -C $(PROCESS16) very-clean
	rm -f $(PROCESS17)/.gosam.dir
	$(MAKE) -C $(PROCESS17) very-clean
	rm -f $(PROCESS0).in $(PROCESS0).log
	rm -f $(PROCESS1).in $(PROCESS1).log
	rm -f $(PROCESS0)/.gosam.dir
	$(MAKE) -C $(PROCESS0) very-clean
	rm -f $(PROCESS1)/.gosam.dir
	$(MAKE) -C $(PROCESS1) very-clean
	rm -f $(PROCESS18).in $(PROCESS18).log
	rm -f $(PROCESS19).in $(PROCESS19).log
	rm -f $(PROCESS18)/.gosam.dir
	$(MAKE) -C $(PROCESS18) very-clean
	rm -f $(PROCESS19)/.gosam.dir
	$(MAKE) -C $(PROCESS19) very-clean

very-clean:
	rm -f gosam.crashed
	rm -f $(PROCESS16).in $(PROCESS16).log
	rm -f $(PROCESS17).in $(PROCESS17).log
	rm -f $(PROCESS16)/.gosam.dir
	rm -fr $(PROCESS16)
	rm -f $(PROCESS17)/.gosam.dir
	rm -fr $(PROCESS17)
	rm -f $(PROCESS0).in $(PROCESS0).log
	rm -f $(PROCESS1).in $(PROCESS1).log
	rm -f $(PROCESS0)/.gosam.dir
	rm -fr $(PROCESS0)
	rm -f $(PROCESS1)/.gosam.dir
	rm -fr $(PROCESS1)
	rm -f $(PROCESS18).in $(PROCESS18).log
	rm -f $(PROCESS19).in $(PROCESS19).log
	rm -f $(PROCESS18)/.gosam.dir
	rm -fr $(PROCESS18)
	rm -f $(PROCESS19)/.gosam.dir
	rm -fr $(PROCESS19)
