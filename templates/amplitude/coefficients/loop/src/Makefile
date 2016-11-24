vim: ts=3:sw=3

include ../../../../Makefile.conf

# @date: [% time_stamp format=%x~%X %]

SOURCES=$(patsubst %.cc.tmp, %.cc, $(notdir $(wildcard ../codegen/*.cc.tmp)))
HEADERS=$(patsubst %.hpp.tmp, %.hpp, $(notdir $(wildcard ../codegen/*.hpp.tmp)))

.PHONY: coeff
coeff: $(SOURCES) $(HEADERS)

%.cc : ../codegen/%.cc.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.cc.tmp, %.cc, $(notdir $<))

%.hpp : ../codegen/%.hpp.tmp
	@cd ../codegen; $(PYTHON) mv.py $(notdir $<) ../src;
	@mv $(notdir $<) $(patsubst %.hpp.tmp, %.hpp, $(notdir $<))
