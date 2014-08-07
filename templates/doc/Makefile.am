
EXTRA_DIST=process.tex gind.ist axodraw.sty redo.log ../diagrams-0.log ../diagrams-1.log

.PHONY: dvi html ps pdf clean-html clean-local

#################### CONFIG_TEX
if CONFIG_TEX

dvi: process.dvi

if CONFIG_MAKEINDEX
process.dvi: process.tex gind.ist axodraw.sty
	@set -e ;\
	${LATEX} process.tex; while grep -q "Rerun to" process.log ; do \
		${LATEX} process.tex; done; \
	${MAKEINDEX} process -s gind.ist; \
	${LATEX} process.tex; while grep -q "Rerun to" process.log ; do \
		${LATEX} process.tex; done
else
process.dvi: process.tex axodraw.sty
	@set -e ;\
	${LATEX} process.tex; while grep -q "Rerun to" process.log ; do \
		${LATEX} process.tex; done
endif

########## CONFIG_PS
if CONFIG_PS
ps: process.ps

process.ps: process.dvi
	${DVIPS} -o process.ps process.dvi

endif
########## CONFIG_PS

########## CONFIG_PDF
if CONFIG_PDF

pdf: process.pdf

process.pdf: process.ps
	${PSTOPDF} $< $@

endif
########## CONFIG_PDF

endif
#################### CONFIG_TEX
