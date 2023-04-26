# vim: ts=3:sw=3


include ../Makefile.conf


# latex and dvips
#
# - Required to create process.ps and process.pdf (make doc)
LATEX=latex
LATEX_OPT=

DVIPS=dvips
DVIPS_OPT=
DVIPS_MINUS_O=-o

MKINDEX=mkindex
MKINDEX_OPT=-s gind.ist

PSTOPDF=ps2pdf

# TARGETS:
.PHONY: compile source clean very-clean doc
.SUFFIXES:

doc: process.dvi process.ps process.pdf

compile:
source:

%.dvi: %.tex
	$(LATEX) $(LATEX_OPT) $<
	@while ($(MKINDEX) $(MKINDEX_OPT) $* ; \
	  	$(LATEX) $(LATEX_OPT) $* ; \
		$(GREP) $(GREP_OPT) -q "Rerun to get cross" $*.log ) do true ; \
	done

process.ps: process.dvi
	$(DVIPS) $(DVIPS_OPT) $< $(DVIPS_MINUS_O) $@

process.pdf: process.ps
	${PSTOPDF} $< $@

clean:
	rm -f process.aux process.log process.toc
	rm -f process.ind process.idx process.ilg

very-clean: clean
	rm -f filelist-source
	rm -f process.dvi process.ps process.pdf

filelist-source:
	echo Makefile > $@
	echo process.tex >> $@
	echo axodraw.sty >> $@
	echo redo.log >> $@
	echo gind.ist >> $@
