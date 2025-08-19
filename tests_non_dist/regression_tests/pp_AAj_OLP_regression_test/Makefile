
PROCESS=pp_AAj

ifndef GOSAM
GOSAM=gosam.py
endif

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif

PROCDIR=process_olp_modules

.PHONY: all test clean very-clean

all: golem test

test: golem
	@echo Running test program
	$(MAKE) ENABLE_CODE_CHECK=$(ENABLE_CODE_CHECK) -C test test

golem: ${PROCDIR}/config.sh
ifeq ($(ENABLE_CODE_CHECK),true)
	cd ${PROCDIR}; meson setup build --prefix ${CURDIR}/${PROCDIR} --warnlevel 3 -Dcode_check=True; cd build; meson compile; meson install
else
	cd ${PROCDIR}; meson setup build --prefix ${CURDIR}/${PROCDIR}; cd build; meson compile; meson install
endif

${PROCDIR}/config.sh:
	$(GOSAM) --olp ${PROCESS}.olp --config setup.in --destination=./${PROCDIR} -f -z


clean:
	rm -f $(PROCESS).log $(PROCESS).olc
	cd ${PROCDIR}; rm -rf build lib config.sh; cd ..
	$(MAKE) -C test clean

very-clean:
	rm -f $(PROCESS).log $(PROCESS).olc
	$(MAKE) -C test clean
	rm -rf ${PROCDIR}

