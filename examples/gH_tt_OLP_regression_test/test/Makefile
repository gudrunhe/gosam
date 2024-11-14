FC=gfortran
FFLAGS=

GSBASE=$(CURDIR)/..
FCLAGS += $(shell $(GSBASE)/process_olp_modules/config.sh -cflags)
LDFLAGS += $(shell $(GSBASE)/process_olp_modules/config.sh -libs)

SRC=test_program.f90 iso_varying_string.f90
DEPS=iso_varying_string.mod
OBJ=${SRC:.f90=.o}

run_test: $(OBJ)
	$(FC) -o $@ $(OBJ) $(LDFLAGS)

iso_varying_string.mod: iso_varying_string.f90
	$(FC) -c iso_varying_string.f90

%.o: %.f90 $(DEPS)
	$(FC) $(FCLAGS) -o $@ -c $<

test: test.log

test.log: run_test
	./run_test

clean:
	@rm -f *.o *.mod *.log run_test


