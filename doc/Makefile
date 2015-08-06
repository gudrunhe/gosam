
PDFLATEX=pdflatex
PDFLATEX_OPT=

BIBTEX=bibtex
BIBTEX_OPT=

GOLEM=gosam.py

.PHONY: all clean

all: refman.pdf devel.pdf

%.pdf: %.tex
	$(PDFLATEX) $(PDFLATEX_OPT) $*
	-$(BIBTEX) $(BIBTEX_OPT) $*
	@while ( grep "Rerun to get cross-references" \
		$*.log > /dev/null ); do	\
		echo '** Re-running LaTeX **'; \
		$(PDFLATEX) $(PDFLATEX_OPT) $*; \
	done

template.tex:
	${GOLEM} --format=LaTeX --template $@

refman.pdf: template.tex refman.bib

clean:
	rm -f devel.aux devel.bbl devel.blg devel.do devel.log devel.out \
	  devel.pdf devel.toc refman.aux refman.bbl refman.blg refman.do \
	  refman.log refman.out refman.toc refman.pdf template.tex
