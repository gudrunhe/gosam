
SUBDIRS=[% @for subprocesses %] \
	[% path %][% @end @for %]

FC=$(shell sh config.sh -fortcom)
FCFLAGS=$(shell sh config.sh -fcflags)
CFLAGS=$(shell sh config.sh -cflags)
LDFLAGS=$(shell sh config.sh -libs)

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

F_OBJECTS=olp_module.o
C_OBJECTS=olp_parser.o olp_lexer.o olp_daemon.o

DISTFILES= \
	Makefile olp.h config.sh olp_module.f90 \
	olp_daemon.c olp_daemon.h olp_lexer.l olp_parser.y \
	olp_lexer.c olp_parser.c olp_parser.h

.PHONY: compile_subprocesses compile source doc clean very-clean

compile: olp_module.o compile_subprocesses

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

very-clean:
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
	@echo -n > $@
	@for f in $(DIST_FILES); \
	do \
		echo $${f} >> $@; \
	done
	@for dir in $(SUBDIRS); \
	do \
		$(MAKE) -C $${dir} $@; \
		$(SED) $(SED_OPT) -e "s/^\\(.\\/\\)\\?/$${dir}\\//" $${dir}/$@ >> $@; \
	done

dist: golem_olp.tar.gz

golem_olp.tar.gz: source filelist-source
	$(TAR) $(TAR_OPT) c -z -f $@ -T filelist-source

olp_lexer.c: olp_lexer.l olp_parser.h
	$(LEX) $(LEX_OPTS) -o $@ $<

olp_parser.h: olp_parser.c

olp_parser.c: olp_parser.y
	$(YACC) $(YACC_OPTS) -d -o $@ $<

olp_daemon: $(C_OBJECTS) $(F_OBJECTS)
	$(CC) $(CC_OPT) -o $@ $(C_OBJECTS) $(LDFLAGS) $(EXTRA_LDFLAGS)

$(C_OBJECTS): %.o: %.c
	$(CC) $(CC_OPT) -c $< -o $@

$(F_OBJECTS): %.o: %.f90 compile_subprocesses
	$(FC) $(FCFLAGS) $(EXTRA_FCFLAGS) -o $@ -c $<

