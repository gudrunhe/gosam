
FC=$(shell sh ../ngolem/config.sh -fortcom)
FCFLAGS=$(shell sh ../ngolem/config.sh -ocflags)

.PHONY: all

all: four_gluon.o

%.o: %.f90
	$(FC) $(FCFLAGS) -c -o $@ $<
