"""
Use Anaconda environment "tensorflow" (Python 3.5)
Run this from the top-level directory with volume ID subfolders
"""

import os


# Names of subfolders within a volume directory
EXTRACT = "extracted"
VECTORS = "vectors"

# return all directories in cwd; specify mindepth to avoid `.` itself
# specify maxdepth since we don't want to process vectors and extracted
# subfolders
for d in os.listdir():

	# Only consider the folders from the volumes
	if os.path.isdir(d):

		target = os.path.join(d, VECTORS)
		source = os.path.join(d, EXTRACT)

		# Check if the vectors subfolder exists
		if not os.path.exists(target):
			
			print("creating vectors subfolder")
			# create the vectors subfolder
			os.system("mkdir {}".format(target))

			# run the classifier on each image in that folder
			for f in os.listdir(source):

				# full path to the image from CWD
				image = os.path.join(source, f)
				#print(image)

				os.system("python ht_classify_score.py --image_file {}".format(image))
			
		else:
			print("vectors subfolder already exists")

	else:
		print("not a directory")



"""
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
"""
