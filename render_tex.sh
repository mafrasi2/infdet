#!/bin/sh
set -e
dot2tex --preproc G.dot | dot2tex | pdflatex && mv texput.pdf $1
