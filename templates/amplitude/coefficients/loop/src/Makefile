vim: ts=3:sw=3

include ../../../../Makefile.conf

# @date: [% time_stamp format=%x~%X %]

SOURCES=$(patsubst %.cc.tmp, %.cc, $(notdir $(wildcard ../codegen/*.cc.tmp)))
HEADERS=$(patsubst %.hpp.tmp, %.hpp, $(notdir $(wildcard ../codegen/*.hpp.tmp)))
OBJECTS=$(patsubst %.cc, %.o, $(SOURCES))
DYNAMIC_LIBRARIES=$(patsubst %.cc, lib%.so, $(SOURCES))

.PHONY: coeff
coeff: $(SOURCES) $(HEADERS) $(OBJECTS) $(DYNAMIC_LIBRARIES)

%.cc : ../codegen/%.cc.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.cc.tmp, %.cc, $(notdir $<))

%.hpp : ../codegen/%.hpp.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.hpp.tmp, %.hpp, $(notdir $<))

lib%.so : %.o
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ -shared $+
