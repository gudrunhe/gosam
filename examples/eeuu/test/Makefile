
FC=$(shell sh ../virtual/config.sh -fortcom)
CFLAGS=$(shell sh ../virtual/config.sh -cflags)
LDFLAGS=$(shell sh ../virtual/config.sh -libs)
DEPS=$(shell sh ../virtual/config.sh -deps)

OBJECTS=test.o

.PHONY: compile test clean

compile: test_program

$(OBJECTS): %.o: %.f90
	$(FC) $(CFLAGS) -o $@ -c $<

test_program: $(OBJECTS) $(DEPS)
	$(FC) -o $@ $(OBJECTS) $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*

