"""
USAGE: python3 create_vector_training_set.py

N.B. must be run from top-level directory that contains <ht_id> volume folders.
"""

import os


# Names of subfolders within a volume directory
VECTORS = "vectors"
TARGET = "/mnt/d/stephen-krewson/Documents/vector5"

unique = set()
missing = 0

for d in os.listdir():

	# Only consider the folders from the volumes
	if os.path.isdir(d):

		unique.add(d)

		source = os.path.join(d, VECTORS)

		# Check if the vectors subfolder exists
		if not os.path.exists(source):
			
			print("No vectors folder found.")
			missing += 1
			continue

		# otherwise print them out
		for f in os.listdir(source):
			concatf = d + '_' + f.split('_')[0] + '.npy'
			print(concatf)

			os.system("echo {}".format(concatf))

	else:
		print("not a directory")

print(unique)
print("# books =", len(unique))
print("unrepresented =", missing)

# note: image files have mix of jpg and png types
# they have format: htid_page#
# need to delete all non-vectorized images (or calc for missing ones)