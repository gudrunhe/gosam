FC=gfortran
FFLAGS=

#OpenLoops
OLEXEC=$(shell which openloops)
OLBASE=$(dir $(OLEXEC))
FFLAGS += -I$(OLBASE)/lib_src/openloops/mod
LDFLAGS += -Wl,-rpath=$(OLBASE)/lib
LDFLAGS += -L$(OLBASE)/lib -lopenloops
SRC=openloops.f90
OBJ=${SRC:.f90=.o}

%.o: %.f90
	$(FC) $(FFLAGS) -o $@ -c $<

run_openloops: $(OBJ)
	$(FC) -o $@ $(OBJ) $(LDFLAGS)

clean:
	@rm -f *.o run_openloops
