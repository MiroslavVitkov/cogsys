RMDFILE=hw_ch4

all:
	Rscript -e "require(knitr); require(markdown); knit("$(RMDFILE).rmd", "$(RMDFILE).md"); markdownToHTML("$(RMDFILE).md", "$(RMDFILE).html", options=c('use_xhml'))"
	pandoc -s "$RMDFILE".html -o "$RMDFILE".pdf
	evince "$RMDFILE".pdf
