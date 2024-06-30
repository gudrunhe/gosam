
FC=$(shell sh ../virtual/config.sh -fortcom)
FCFLAGS=$(shell sh ../virtual/config.sh -cflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)

.PHONY: compile test clean

compile: test_program

test.o: test.f90
	$(FC) $(FCFLAGS) -o $@ -c $<

test_program: test.o
	$(FC) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
	rm -rf BadPoints
