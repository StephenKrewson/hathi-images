#!/bin/bash
#
# tensorflow file needs to be run from volume ID DIR

#find $1 -name '*.jpg' | while read file; do python classify_image_mk.py --image_file $file; done
#!/bin/bash
#
# Author: Stephen Krewson
#
# Usage: from within directory where only subfolders are HT IDs (with full page
# images inside), run Inception model on "extracted"
#
# ./ht_run_extraction.sh
#


# convention for output destination for the image details
EXTRACT=extracted
VECTORS=vectors

# return all directories in cwd; specify mindepth to avoid `.` itself
# specify maxdepth since we don't want to process vectors and extracted
# subfolders
for dir in $(find -mindepth 1 -maxdepth 1 -type d); do

	echo Attempting classification in $dir

	# the only *files* in this directory should be image files: so no mapping
	# text files, etc. put output of tree on a model dir in the README
	# N.B. it will eventually have "extracted" and "vectors" subfolders

	# ignore folders that already have "vectors"
	if [ ! -d $dir/$VECTORS ]; then
		mkdir $dir/$VECTORS
	fi

	# if HT ID directory already has ./extracted subfolder, no need to process
	for img in $(find $dir/$EXTRACT -type f); do
		echo $img
		python ht_classify_score.py --image_file $img
	done


	#if [ !-d "$dir/$EXTRACT" ]; then
	#	
	#	mkdir "$dir/$EXTRACT"
	#	python ht_extract_images.py --image_dir $dir --output_dir "$dir/$EXTRACT"
	#
	#else
	#	echo "$dir/$EXTRACT" subfolder exists: volume already processed!
	#fi

	# just test with one dir
	#exit

done
