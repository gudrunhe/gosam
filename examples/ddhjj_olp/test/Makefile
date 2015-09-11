
FC=$(shell sh ../virtual/config.sh -fortcom)
FCFLAGS=$(shell sh ../virtual/config.sh -fcflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)
DEPS=$(shell sh ../virtual/p0_gg_hddbar/config.sh -deps) \
     $(shell sh ../virtual/p1_ddbar_huubar/config.sh -deps) \
     ../virtual/olp_module.o

.PHONY: compile test clean

compile: test_program

test.o: test.f90
	$(FC) $(FCFLAGS) -o $@ -c $<

test_program: test.o $(DEPS)
	$(FC) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
	rm -rf BadPoints
