#!/bin/bash

# only creates a new year "bin" if it doesn't exist
# the classification code itself needs to decide whether
# to round to 5 year or decade bins
for i in `seq 1800 1860`; do
	if [ ! -d $i ]; then
		mkdir $i
	fi
done
