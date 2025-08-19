
PROCESS1=udeneg_dred
PROCESS2=udeneg_thv

FC=$(shell sh ../$(PROCESS1)/config.sh -fortcom)

FCFLAGS=-ffree-line-length-none

CFLAGS=$(shell sh ../$(PROCESS1)/config.sh -cflags)
CFLAGS+=$(shell sh ../$(PROCESS2)/config.sh -cflags)

LDFLAGS=$(shell sh ../$(PROCESS1)/config.sh -libs)
LDFLAGS+=$(shell sh ../$(PROCESS2)/config.sh -libs)

DEPS=$(shell sh ../$(PROCESS1)/config.sh -deps)
DEPS+=$(shell sh ../$(PROCESS2)/config.sh -deps)

ifndef ENABLE_CODE_CHECK
ENABLE_CODE_CHECK=false
endif

.PHONY: compile test clean

compile: test_program

test.o: test.f90
ifeq ($(ENABLE_CODE_CHECK),true)
	$(FC) $(CFLAGS) $(FCFLAGS) -fcheck=all -o $@ -c $<
else
	$(FC) $(CFLAGS) $(FCFLAGS) -o $@ -c $<
endif

test_program: test.o $(DEPS)
	$(FC) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
