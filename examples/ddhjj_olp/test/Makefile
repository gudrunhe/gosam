
FC=$(shell sh ../virtual/config.sh -fortcom)
FCFLAGS=$(shell sh ../virtual/config.sh -cflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif

.PHONY: compile test clean

compile: test_program

test.o: test.f90
ifeq ($(ENABLE_CODE_CHECK),true)
	$(FC) $(FCFLAGS) -fcheck=all -o $@ -c $<
else
	$(FC) $(FCFLAGS) -o $@ -c $<
endif

test_program: test.o
	$(FC) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
	rm -rf BadPoints
