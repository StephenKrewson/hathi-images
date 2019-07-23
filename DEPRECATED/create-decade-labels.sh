#!/bin/bash

# only creates a new year "bin" if it doesn't exist
# the classification code itself needs to decide whether
# to round to 5 year or decade bins

# location of images organized by year
IMG_DIR=/mnt/c/Users/stephen-krewson/Dropbox/parley-train/*

OUT_DIR=/mnt/d/stephen-krewson/Documents/

# number of years to bin with (e.g. 10 for decade)

# loop and reassign
for dir in $IMG_DIR; do

	date = $(basename $dir)
	date = $(python -c "$date - 0")

	echo $date

	#echo $((date % 5)) 

	#cp -R "$dir/." $OUT_DIR/$(dir )

	#if [ ! -d $i ]; then
	#	mkdir $i
	#fi
done
