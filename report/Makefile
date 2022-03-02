main:
	pandoc outline.md -o outline.pdf
	#pandoc thesis.md --citeproc --bibliography="/home/daan/.pandoc/default.bib" -o thesis.pdf
	pandoc thesis.md -o thesis.pdf

prop:
	pdflatex proposal.tex
	rm proposal.aux
	rm proposal.log
