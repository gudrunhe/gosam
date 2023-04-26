# vim: ts=3:sw=3
HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)


include ../Makefile.conf



OBJECTS=config.o kinematics.o dipoles.o model.o rambo.o util.o \
		  color.o accu.o version.o groups.o globalsl1.o scalar_cache.o

.PHONY: compile source clean very-clean doc
.SUFFIXES:


compile: source common.a


source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif

doc:


common.a: $(OBJECTS)
	$(Q) ar rs $@ $+

clean:
	$(Q)rm -f *.o *.mod common.a



very-clean: clean
	$(Q)rm -f filelist-source
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(FIND) $(FIND_OPT) . \( \
		-name 'color.f90' \
		-or -name 'model.f90' \
		-or -name 'version.f90' \
		\) -exec rm \{} \;
endif

$(OBJECTS):%.o:%.f90
	$(vecho) "-> Compiling $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) -c -o $@ $<

version.f90 color.f90 model.f90 version_qp.f90 color_qp.f90 model_qp.f90: source

filelist-source: source
	echo Makefile > $@
	echo Makefile.dep >> $@
	@for f in $(subst .o,.f90,$(OBJECTS)); \
	do \
		echo $${f} >> $@; \
	done

include Makefile.dep
