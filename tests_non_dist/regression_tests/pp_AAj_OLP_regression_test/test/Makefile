GSBASE=$(CURDIR)/..
FC=$(shell sh $(GSBASE)/process_olp_modules/config.sh -fortcom)
FCLAGS += $(shell $(GSBASE)/process_olp_modules/config.sh -cflags)
LDFLAGS += $(shell $(GSBASE)/process_olp_modules/config.sh -libs)

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif

SRC=test_program.f90
OBJ=${SRC:.f90=.o}

run_test: $(OBJ)
	$(FC) -o $@ $(OBJ) $(LDFLAGS)

%.o: %.f90
ifeq ($(ENABLE_CODE_CHECK),true)
	$(FC) $(FCLAGS) -fcheck=all -o $@ -c $<
else
	$(FC) $(FCLAGS) -o $@ -c $<
endif

test: test.log

test.log: run_test
	./run_test

clean:
	@rm -f *.o *.mod *.log run_test


