#!/bin/bash
#
# Author: Stephen Krewson
#
# Usage: from within directory where only subfolders are HT IDs (with full page
# images inside), run script to create "extracted" sub-subfolder containing
# detail of engraving(s) for each page in the volume subfolder
#
# ./ht_run_extraction.sh
#


# convention for output destination for the image details
EXTRACT=extracted

# return all directories in cwd; specify mindepth to avoid `.` itself
# specify maxdepth since we don't want to process vectors and extracted
# subfolders
for dir in $(find -mindepth 1 -maxdepth 1 -type d); do

	echo Attempting image extraction in $dir

	# the only *files* in this directory should be image files: so no mapping
	# text files, etc. put output of tree on a model dir in the README
	# N.B. it will eventually have "extracted" and "vectors" subfolders
	
	# if HT ID directory already has ./extracted subfolder, no need to process
	if [ ! -d "$dir/$EXTRACT" ]; then
		
		mkdir "$dir/$EXTRACT"
		python ht_extract_images.py --image_dir $dir --output_dir "$dir/$EXTRACT"

	else
		echo "$dir/$EXTRACT" subfolder exists: volume already processed!
	fi

	# just test with one dir
	#exit

done
