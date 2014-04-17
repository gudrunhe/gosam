
FC=$(shell sh ../virtual/config.sh -fortcom)
CFLAGS=$(shell sh ../virtual/config.sh -cflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)

OBJECTS=test.o

.PHONY: compile test clean

compile: test_program

$(OBJECTS): %.o: %.f90
	$(FC) $(CFLAGS) -o $@ -c $<

test_program: $(OBJECTS)
	$(FC) -o $@ $+ $(LDFLAGS)

test: test.log

test.log: test_program
	LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):../lib:../lib64 && ./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*

