
FC=$(shell sh ../ngosam/config.sh -fortcom)
FCFLAGS=$(shell sh ../ngosam/config.sh -ocflags)

.PHONY: all clean

all: four_gluon.o

%.o: %.f90
	$(FC) $(FCFLAGS) -c -o $@ $<

clean:
	rm -fr *.mod *.o
