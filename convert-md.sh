#!/bin/sh

PROJECT="/mnt/c/Users/stephen-krewson/Documents/StephenKrewson.github.io"

# Ensure a file is given as an argument
if [ "$#" -ne 2 ] || ! [ -f "$1" ]; then
  echo "Usage: [bash] $0 MARKDOWN_FILE EXT" >&2
  exit 1
fi

# First substitute out the markdown extension; then canonicalize the name
# we want nothing to break if we call it from the "wrong" subdirectory provided
# that we are at least within the repo
# EXT needs to be one of: [html, pdf, docx]

name=$(readlink -f ${1%.md})
EXT=${2}

echo "Converting $1 to $name.$EXT"

# For extensions, see: http://pandoc.org/MANUAL.html#pandocs-markdown
# NOTE: the CSS file is given as a relative path because it is just a link
# from the perspective of the site resources (no relation to my dev machine)

# TODO: check against config repo since I have added more pandoc options
# 6/12/18 "smart" option for em-dashes does NOT work with target outputs
# figure out best way to insert unicode em-dash in sublime

# https://github.com/jgm/pandoc/issues/2634 (skinny column problem)

# --smart flag helps turn `--` into the em-dash

# TODO: just use it on Windows; --smart is now +smart extension

# Generate the HTML (use full version of flags; put in alphabetical order)
pandoc\
	--bibliography="$PROJECT/assets/bib/references.bib"\
	--column=1000\
	--csl="$PROJECT/assets/bib/chicago-author-date.csl"\
	--css="github.css"\
	--filter pandoc-citeproc\
	--from markdown+citations+implicit_figures+inline_notes+yaml_metadata_block\
	--smart\
	--standalone\
	--toc\
  --section-divs\
	--output "$name.$EXT"\
	$1

# Print status: 0 is success
echo "Status: $?"
