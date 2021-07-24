thesis.pdf: slides.tex bibliography.bib
	pdflatex slides
	bibtex slides
	pdflatex slides
	pdflatex slides

clean:
	rm -f *.log *.dvi *.aux *.toc *.lof *.lot *.out *.bbl *.blg *.xmpi *.snm *.nav *.bcf
	rm -f slides.pdf
