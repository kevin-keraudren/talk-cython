#!/bin/bash

set -x
set -e

main_file="presentation"

pdflatex --shell-escape $main_file
bibtex $main_file
pdflatex $main_file
pdflatex $main_file
