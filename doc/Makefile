
PDFLATEX=pdflatex
PDFLATEX_OPT=

BIBTEX=bibtex
BIBTEX_OPT=

GOLEM=gosam.py

.PHONY: all clean

all: refman.pdf devel.pdf

devel.pdf: devel.tex
	$(PDFLATEX) $(PDFLATEX_OPT) devel.tex
	-$(BIBTEX) $(BIBTEX_OPT) devel
	@while ( grep "Rerun to get cross-references" \
		devel.log > /dev/null ); do	\
		echo '** Re-running LaTeX **'; \
		$(PDFLATEX) $(PDFLATEX_OPT) devel.tex; \
	done

refman_sections/template.tex:
	${GOLEM} --format=LaTeX --template $@

refman.pdf: refman_sections/template.tex refman.bib refman.tex
ifneq (, $(shell which ${GOLEM})) # Always regenerate 'template.tex' if GoSam is installed
	${GOLEM} --format=LaTeX --template refman_sections/template.tex
endif
	$(PDFLATEX) $(PDFLATEX_OPT) refman.tex
	-$(BIBTEX) $(BIBTEX_OPT) refman
	@while ( grep "Rerun to get cross-references" \
		refman.log > /dev/null ); do	\
		echo '** Re-running LaTeX **'; \
		$(PDFLATEX) $(PDFLATEX_OPT) refman.tex; \
	done

clean:
	rm -f devel.aux devel.bbl devel.blg devel.do devel.log devel.out \
	  devel.pdf devel.toc refman.aux refman.bbl refman.blg refman.do \
	  refman.log refman.out refman.toc refman.pdf \
	  refman_sections/template.tex
