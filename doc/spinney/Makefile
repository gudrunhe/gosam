LATEX=pdflatex
LATEX_OPT=

GREP=grep
GREP_OPT= -q "Rerun to get cross" $*.log

.DEFAULT_GOAL=spinney-cpc.pdf

.PHONY: clean
.SUFFIXES:

%.pdf: %.tex
	$(LATEX) $(LATEX_OPT) $<
	while ($(GREP) $(GREP_OPT)) ; \
		do $(LATEX) $(LATEX_OPT) $< ; \
	done

clean:
	rm -f spinney-cpc.aux spinney-cpc.log spinney-cpc.toc
	rm -f spinney-cpc.ind spinney-cpc.idx spinney-cpc.ilg
	rm -f spinney-cpc.dvi spinney-cpc.ps spinney-cpc.pdf
	rm -f spinney-cpc.spl

