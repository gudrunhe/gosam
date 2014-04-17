

FORM=form
FORM_OPT=

JAVA=java
HAGGIES_PATH=${HOME}/local/share/golem/haggies
HAGGIES_OPT=-V3

.PHONY: all

all: analytic.f90

analytic.txt: square.frm
	$(FORM) $(FORM_OPT) $<

analytic.f90: analytic.txt analytic.in analytic.out
	$(JAVA) -jar $(HAGGIES_PATH)/haggies.jar \
		$(HAGGIES_OPT) \
		-c analytic.in -t analytic.out -o $@ $<

clean:
	rm -f analytic.txt
