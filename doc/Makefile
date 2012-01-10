
PDFLATEX=pdflatex
PDFLATEX_OPT=

BIBTEX=bibtex
BIBTEX_OPT=

GOLEM=gosam.py

.PHONY: all

all: refman.pdf

%.pdf: %.tex %.bib template.tex
	$(PDFLATEX) $(PDFLATEX_OPT) $*
	$(BIBTEX) $(BIBTEX_OPT) $*
	@while ( grep "Rerun to get cross-references" \
		$*.log > /dev/null ); do	\
		echo '** Re-running LaTeX **'; \
		$(PDFLATEX) $(PDFLATEX_OPT) $*; \
	done

template.tex:
	${GOLEM} --no-defaults --format=LaTeX --template $@
