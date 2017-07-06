
INTS=$(patsubst %.so, %, $(patsubst ../virtual/amplitude/integrals/lib/lib%, -l%, $(wildcard ../virtual/amplitude/integrals/lib/*.so)))

COEFFS1=$(patsubst %.so, %, $(patsubst ../virtual/amplitude/coefficients/1loop/src/lib%, -l%, $(wildcard ../virtual/amplitude/coefficients/1loop/src/*.so)))

LDFLAGS=-L../virtual/amplitude/integrals/lib $(INTS) -Wl,-rpath,$(CURDIR)/../virtual/amplitude/integrals/lib  -L../virtual/amplitude/coefficients/1loop/src $(COEFFS1) -Wl,-rpath,$(CURDIR)/../virtual/amplitude/coefficients/1loop/src  -L$(SECDEC_CONTRIB)/lib -lcuba -lm -Wl,-rpath,$(SECDEC_CONTRIB)/lib

# The C++11 compiler
CXX = g++

# The C++11 compiler flags
CXXFLAGS += -fPIC -std=c++11
# include secdec contrib directory if environment variable set
ifneq (x$(SECDEC_CONTRIB), x)
CXXFLAGS += -I$(SECDEC_CONTRIB)/include
endif

.PHONY: compile test clean

compile: test_program

test.o: test.cpp
	$(CXX) $(CXXFLAGS)  -I../virtual/amplitude/coefficients/1loop/src  -I../virtual/amplitude/integrals/include -o $@ -c $<

test_program: test.o $(DEPS)
	$(CXX) -o $@ $< $(LDFLAGS)

test: test.log

test.log: test_program
	./test_program

clean:
	rm -rf test_program test.o
	rm -rf test.log
