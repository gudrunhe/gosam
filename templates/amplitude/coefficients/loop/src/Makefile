vim: ts=3:sw=3

include ../../../../Makefile.conf

# @date: [% time_stamp format=%x~%X %]

SOURCESTMP=$(wildcard ../codegen/*.cc.tmp)
HEADERSTMP=$(wildcard ../codegen/*.hpp.tmp)
SOURCES=$(patsubst %.cc.tmp, %.cc, $(notdir $(wildcard ../codegen/*.cc.tmp)))
HEADERS=$(patsubst %.hpp.tmp, %.hpp, $(notdir $(wildcard ../codegen/*.hpp.tmp)))

OBJECTS=$(patsubst %.cc, %.o, $(wildcard *.cc))
DYNAMIC_LIBRARIES=$(patsubst %.cc, lib%.so, $(wildcard *.cc))

.PHONY: $(SOURCESTMP) $(HEADERSTMP)

prepare_coeff-stamp: $(SOURCES) $(HEADERS)
	@touch prepare_coeff-stamp

compile_coeff-stamp: $(OBJECTS) $(DYNAMIC_LIBRARIES)
	@touch compile_coeff-stamp

%.cc : ../codegen/%.cc.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.cc.tmp, %.cc, $(notdir $<))

%.hpp : ../codegen/%.hpp.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.hpp.tmp, %.hpp, $(notdir $<))

lib%.so : %.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ -shared $+
