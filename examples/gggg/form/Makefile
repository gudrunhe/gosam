
FORM=form
FORM_OPT=

HAGGIES_JAR=${HOME}/projects/haggies/trunk/dist/haggies.jar
HAGGIES=java -jar ${HAGGIES_JAR}
HAGGIES_OPT=

.PHONY: all

all: four_gluon.f90

square.txt square.out: square.frm
	$(FORM) $(FORM_OPT) $<


four_gluon.f90: square.txt square.in square.out
	$(HAGGIES) $(HAGGIES_OPT) -t square.out -c square.in -o $@ $<
