.DEFAULT_GOAL=runtests

GOSAM_BIN=gosam.py

ENABLE_CODE_CHECK=false

.PHONY : clean
clean :
	for f in * ; \
	do \
	if test -d "$$f" -a -f "$$f/Makefile" ; \
	then \
		$(MAKE) -C $$f very-clean ; \
	fi \
	done

.SILENT .PHONY : summarize
summarize :
	printf "\n"
	printf "\033[0;32m"
	find . -type d -name 'test' -exec grep -Hl "@@@ SUCCESS @@@" \{}/test.log \
		   2>/dev/null \; | \
		sed 's/\.\/\([A-Za-z0-9_-]*\)\/test\/test.log/+ \1 (succeeded)/' | \
		sort
	printf "\033[0m"
	printf "\033[1;31m"
	find . -type d -name 'test' -exec grep -HL "@@@ SUCCESS @@@" \{}/test.log \; | \
		sed 's/\.\/\([A-Za-z0-9_-]*\)\/test\/test.log/+ \1 (FAILED)/' | \
		sort
	printf "\033[0m"
	printf "\n"

ALL_TESTS = $(shell ls -d */ | grep -v "model" | sed s\#/\#\#)
.PHONY .SILENT : $(ALL_TESTS)
$(ALL_TESTS) :
	echo ------------------------------------------------------------
	echo "START `date +'%s'`"
	echo ------------------------------------------------------------
	echo "TEST $@"
	echo ------------------------------------------------------------
	printf "Running 'make very-clean' in $@ ...\n"
	$(MAKE) -C "$@" very-clean \
	|| printf "make very-clean failed\n@@@ FAILURE @@@\n" \
		> "$@/test/test.log" \
	printf "Running 'make test' in $@...\n"
	$(MAKE) GOSAM=$(GOSAM_BIN) ENABLE_CODE_CHECK=$(ENABLE_CODE_CHECK) -C "$@" test \
	|| printf "make test failed\n@@@ FAILURE @@@\n" \
		> "$@/test/test.log"
	echo ------------------------------------------------------------
	echo "DONE `date +'%s'`"
	echo ------------------------------------------------------------

.PHONY : runtests
runtests : $(ALL_TESTS)

# SELECTED_TESTS = gH_tt_OLP_regression_test gH_ttg_EFT_regression_test pp_AAj_OLP_regression_test

SKIP_TESTS = dd_ttH_EFT_regression_test
SELECTED_TESTS = $(filter-out $(SKIP_TESTS),$(ALL_TESTS))

.SILENT .PHONY : check_selection
check_selection :
	for f in $(SELECTED_TESTS) ; do \
		if grep -q "@@@ SUCCESS @@@" $$f/test/test.log 2>/dev/null; then \
			printf "\033[0;32m" ; \
			printf "$$f/test/test.log: success" ; \
			printf "\033[0m\n" ; \
		else \
			err="$(grep -q "@@@ SUCCESS @@@" $$f/test/test.log 2>&1)" ; \
			printf "$$err"; \
			printf "\033[1;31m" ; \
			if [ -z "$${err}" ]; then \
				printf "$$f/test/test.log: failed " ; \
			else \
				printf "$$f/test/test.log: failed: $$err" ; \
			fi ; \
			printf "\033[0m\n" ; \
		fi \
	done ; \
	printf "\033[0m" ;
	printf "\n"

.SILENT .PHONY : run_failed
run_failed :
	for f in $(SELECTED_TESTS) ; do \
		if grep -q "@@@ SUCCESS @@@" $$f/test/test.log 2>/dev/null; then \
			printf "\033[0;32mExample $$f previously succeeded, skipping.\033[0m\n" ; \
		else \
			printf "\033[1;31mExample $$f previously failed, rerunning...\033[0m\n" ; \
			echo ------------------------------------------------------------ ; \
			echo "START `date +'%s'`" ; \
			echo ------------------------------------------------------------ ; \
			echo "TEST $$f" ; \
			echo ------------------------------------------------------------ ; \
			printf "Running 'make very-clean' in $$f ...\n" ; \
			$(MAKE) -C "$$f" very-clean \
			|| printf "make very-clean failed\n@@@ FAILURE @@@\n" \
				> "$@/test/test.log" ; \
			printf "Running 'make test' in $$f...\n" ; \
			$(MAKE) GOSAM=$(GOSAM_BIN) ENABLE_CODE_CHECK=$(ENABLE_CODE_CHECK) -C "$$f" test \
			|| printf "make test failed\n@@@ FAILURE @@@\n" \
				> "$@/test/test.log" ; \
			echo ------------------------------------------------------------ ; \
			echo "DONE `date +'%s'`" ; \
			echo ------------------------------------------------------------ ; \
		fi \
	done ; \
	printf "\033[0m" ;
	printf "\n"


.PHONY : runselected
runselected : printselected $(SELECTED_TESTS)

.PHONY : printselected
printselected :
	@echo "SELECTED TESTS: " $(SELECTED_TESTS)
