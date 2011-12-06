
FC=$(shell sh ../ngolem/config.sh -fortcom)
CFLAGS=$(shell sh ../ngolem/config.sh -cflags)
LDFLAGS=../ngolem/matrix/matrix.a \
	$(shell sh ../ngolem/config.sh -libs)

.PHONY: compile test

compile: test_program

test.o: test.f90
	$(FC) $(CFLAGS) -o $@ -c $<

test_program: test.o
	$(FC) -o $@ $+ $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log bad.points output.dat fort.*
