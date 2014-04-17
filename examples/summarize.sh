#!/bin/sh

printf "\n"
printf "\033[0;32m"
find -type d -name 'test' -exec grep -Hl "@@@ SUCCESS @@@" \{}/test.log \
	   2>/dev/null \; | \
	sed 's/\.\/\([A-Za-z0-9_-]*\)\/test\/test.log/+ \1 (succeeded)/' | \
	sort
printf "\033[0m"
printf "\033[1;31m"
find -type d -name 'test' -exec grep -HL "@@@ SUCCESS @@@" \{}/test.log \; | \
	sed 's/\.\/\([A-Za-z0-9_-]*\)\/test\/test.log/+ \1 (FAILED)/' | \
	sort
printf "\033[0m"
printf "\n"
