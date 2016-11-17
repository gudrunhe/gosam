# vim: syntax=golem
SUBDIRS=[% @for subprocesses %] \
	[% path %][% @end @for %]

include Makefile.conf

FCFLAGS=$(shell sh config.sh -fcflags)
CFLAGS=$(shell sh config.sh -cflags)[%
@if extension shared %]
LDFLAGS=$(shell sh config.sh -intern -libs)[%
@else %]
LDFLAGS=$(shell sh config.sh -libs)[%
@end @if %]

# EXTRA_FCFLAGS=
# EXTRA_CFLAGS=
# EXTRA_LDFLAGS=

TAR=tar
TAR_OPT=

SED=sed
SED_OPT=

CC=gcc
CC_OPTS=-ansi

LEX=flex
LEX_OPTS=

YACC=yacc
YACC_OPTS=

F_MODULES=olp_module.mod
F_OBJECTS=olp_module.o
C_OBJECTS=[%
@if internal OLP_DAEMON %]olp_parser.o olp_lexer.o olp_daemon.o[%
@end @if %]

DISTFILES= \
	Makefile olp.h config.sh olp_module.f90 Makefile.conf[%
@if internal OLP_DAEMON %] \
	olp_daemon.c olp_daemon.h olp_lexer.l olp_parser.y \
	olp_lexer.c olp_parser.c olp_parser.h[%
@end @if %]

.PHONY: compile_subprocesses compile source doc clean very-clean

[% @if extension shared %]
compile: olp_module.o compile_subprocesses libgosam_process.so
[% @else %]
compile: olp_module.o compile_subprocesses
[% @end @if %]

compile_subprocesses:
	for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} compile; \
	done

doc:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
	done

clean:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
	done
	rm -f $(F_MODULES) $(C_OBJECTS) $(F_OBJECTS)

very-clean: clean
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
	done

source:
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
	done

filelist-source: source
	@touch $@
	@for f in $(DISTFILES); \
	do \
		echo $${f} >> $@; \
	done
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
		$(SED) $(SED_OPT) -E -e "s/^(.\/)?/$${dir}\//" $${dir}/$@ >> $@; \
	done

dist: golem_olp.tar.gz

golem_olp.tar.gz: source filelist-source
	$(TAR) $(TAR_OPT) c -z -f $@ -T filelist-source[%

@if internal OLP_DAEMON %]

olp_lexer.c: olp_lexer.l olp_parser.h
	$(LEX) $(LEX_OPTS) -o $@ $<

olp_parser.h: olp_parser.c

olp_parser.c: olp_parser.y
	$(YACC) $(YACC_OPTS) -d -o $@ $<

olp_daemon: $(C_OBJECTS) $(F_OBJECTS)
	$(CC) $(CC_OPT) -o $@ $(C_OBJECTS) $(LDFLAGS) $(EXTRA_LDFLAGS)[%
@end @if %]

$(C_OBJECTS): %.o: %.c
	$(CC) $(CC_OPT) -c $< -o $@

$(F_OBJECTS): %.o: %.f90 compile_subprocesses
	$(FC) $(FCFLAGS) $(EXTRA_FCFLAGS) -o $@ -c $<

[% @if extension shared %]
# olp_module.o is in LDFLAGS
libgosam_process.so: olp_module.o
	$(vecho) "-> Linking $@ .."
	$(Q) $(FC) $(FC_OPTS) $(FCFLAGS) $(LDFLAGS) -Wl,-rpath="$$ORIGIN" -shared -o $@
[%@end @if%]

