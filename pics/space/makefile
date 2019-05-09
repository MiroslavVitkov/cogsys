all:
	pdflatex --output-directory /tmp space.tex  && \
	cp space.bib /tmp && \
	cd /tmp  && \
	bibtex space  && \
	cd -  && \
	pdflatex --output-directory /tmp space.tex  && \
	pdflatex --output-directory /tmp space.tex  && \
	evince /tmp/space.pdf
