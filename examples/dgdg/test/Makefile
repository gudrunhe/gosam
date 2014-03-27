
FC=$(shell sh ../virtual/config.sh -fortcom)
CFLAGS=$(shell sh ../virtual/config.sh -cflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)
DEPS=$(shell sh ../virtual/config.sh -deps)

.PHONY: compile test clean

compile: test_program

test.o: test.f90
	$(FC) $(CFLAGS) -o $@ -c $<

test_program: test.o $(DEPS)
	$(FC) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
