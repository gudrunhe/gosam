
FC=$(shell sh ../ngolem/config.sh -fortcom)
CFLAGS=$(shell sh ../ngolem/config.sh -cflags)
LDFLAGS=$(shell sh ../ngolem/config.sh -libs)

OBJECTS=test.o analytic.o

.PHONY: compile test

compile: test_program

$(OBJECTS): %.o: %.f90
	$(FC) $(CFLAGS) -o $@ -c $<

test_program: $(OBJECTS)
	$(FC) -o $@ $+ $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*

test.o: analytic.o
