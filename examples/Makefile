.DEFAULT_GOAL=runtests

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

ALL_TESTS = $(shell ls -d */ | sed s\#/\#\#)
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
	$(MAKE) -C "$@" test \
	|| printf "make test failed\n@@@ FAILURE @@@\n" \
		> "$@/test/test.log"
	echo ------------------------------------------------------------
	echo "DONE `date +'%s'`"
	echo ------------------------------------------------------------

.PHONY : runtests
runtests : $(ALL_TESTS)

# TODO: merge ddtt+ggtt --> olp
# TODO: write: tttt, tbWp_tree
# TODO: include: eett_NLOCT, gggh_reduze, gggh
SELECTED_TESTS = bghb ggtt ggtt_ufo eeuu_autotools ggHg gggg_tree gggg gggz hyy s-channel_single-top udene

.SILENT .PHONY : check_selection
check_selection :
	for f in $(SELECTED_TESTS) ; do \
		if [ -d "$$f" ] ; then \
			printf "\033[0;32m" ; \
			printf "$$f OK" ; \
		else \
			printf "\033[1;31m" ; \
			printf "$$f does not exist" ; \
		fi ; \
		printf "\n" ; \
	done ; \
	printf "\033[0m" ;
	printf "\n"

.PHONY : runselected
runselected : $(SELECTED_TESTS)
