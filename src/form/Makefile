MAINSTUB=lorentz

.PHONY: all dvi pdf formfiles test
all: $(MAINSTUB).pdf formfiles

pdf: $(MAINSTUB).pdf

$(MAINSTUB).tex: $(MAINSTUB).nw
	nuweb -o $<

formfiles: $(MAINSTUB).nw
	nuweb -t $<

%.aux: %.tex
	pdflatex $<

%.pdf: %.tex
	pdflatex $<
