main:
	# pandoc outline.md -o outline.pdf
	# pandoc thesis.md --citeproc --bibliography="/home/daan/.pandoc/default.bib" -o thesis.pdf
	# pandoc thesis.md -o thesis.pdf
	pdflatex thesis.tex
	biber thesis
	pdflatex thesis.tex
	rm *.log *.aux *.bbl *.bcf *.blg *.run.xml *.toc *.tdo

prop:
	pdflatex proposal.tex
	rm proposal.aux
	rm proposal.log


flash:
	pdflatex flash_talk.tex
	rm *.aux *.log *.nav *.out *.snm *.toc
