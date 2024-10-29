
PROCESS=pp_AAj

ifndef GOSAM
GOSAM=gosam.py
endif

PROCDIR=process_olp_modules

.PHONY: all test clean very-clean

all: golem test

test: golem
	@echo Running test programm
	$(MAKE) -C test test

golem: ${PROCDIR}/config.sh
	cd ${PROCDIR}; meson setup build --prefix ${CURDIR}/${PROCDIR}; cd build; meson compile; meson install

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

