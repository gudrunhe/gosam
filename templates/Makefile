[% '
	Template file for the Makefile in process_dir
' %]# vim: ts=3:sw=3

HAVE_MAKEFILE_SOURCE=$(if $(wildcard Makefile.source),1,0)

SUBDIRS=doc common[%
@for helicities generated %] helicity[% helicity %][%
@end @for helicities %][%@if helsum%] sum[%@end @if%] matrix

[% @if internal OLP_MODE %]
include ../Makefile.conf[%
@else %]
include Makefile.conf[%
@end @if %]

# Stream editor.
#
# - Only to be changed on non-standard installations
SED=sed
SED_OPT=

# tar utility
#
# - Required to create tarballs
# - tar must support the -T option
TAR=tar
TAR_OPT=

# TARGETS:
.PHONY: dist compile source clean very-clean doc help
.SUFFIXES:

help:
	@echo Please, choose one of the following targets:
	@echo make source      --  generate source files, mainly Fortran90 files
	@echo make compile     --  compile the Fortran90 sources
	@echo make dist        --  create a tar-ball of the source files
	@echo make clean       --  remove object files and intermediate files
	@echo make very-clean  --  remove files including targets of 'make source'
	@echo make doc         --  create various documents related to the process
	@echo make help        --  show this help screen

dist: [% process_name asprefix=\_ %]matrix.tar.gz

compile:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) $(S) -C $${dir} $@; \
	done

doc:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) $(S) -C $${dir} $@; \
	done

clean:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) $(S) -C $${dir} $@; \
	done

very-clean:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) $(S) -C $${dir} $@; \
	done
else
	@echo =====  This would delete most of the Fortran90 sources. =====
	@echo There is no \'Makefile.source\' which probably means that you
	@echo extracted the source files from a tar-ball. Hence, you won\'t
	@echo be able to restore those files. Therefore I refuse to do what
	@echo you asked me for.
endif

source:
ifeq ($(HAVE_MAKEFILE_SOURCE),1)
	$(MAKE) $(S) -f Makefile.source source
endif


filelist-source: source
	@echo Makefile > $@[%
@if internal OLP_MODE %][%
@else %]
	@echo Makefile.conf >> $@[%
@end @if %]
	@echo config.sh >> $@[% 
@if generate_lo_diagrams %]
	@echo diagrams-0.log >> $@
	@echo diagrams-0.hh >> $@[%
@end @if %][% 
@if generate_nlo_virt %]
	@echo diagrams-1.log >> $@
	@echo diagrams-1.hh >> $@[%
@end @if %]
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
		$(SED) $(SED_OPT) -E -e "s/^(.\/)?/$${dir}\//" $${dir}/$@ >> $@; \
	done

[% process_name asprefix=\_ %]matrix.tar.gz: source filelist-source
	$(TAR) $(TAR_OPT) c -z -f $@ -T filelist-source
