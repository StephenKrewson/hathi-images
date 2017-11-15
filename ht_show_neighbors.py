"""
Author: Stephen Krewson

First checks in the given directory for files of the form:

<DATE>_saved_paths.pkl
<DATE>_saved_distances.npy
<DATE>_saved_indices.npy

if these don't exist (with the same date for each), it exits. Normal usage is:

	python ht_show_neighbors.py <PATH_TO_IMAGE>

If no argument is supplied, a random index is chosen.

Uses this package; run from "tensorflow" environment in Windows
https://anaconda.org/htrc/pysolr

"""


import cv2
import glob
from htrc import metadata as bib
from imutils import build_montages
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import os
import pickle
import random
import re
import sys


# Make sure we have three files of format <DATE>_saved_*
saved = glob.glob("*_saved*")
if len(saved) is not 3:
	exit("Saved files for distances, indices, and paths must exist. Run \
		ht_calc_neighbors.py to generate these three files.")

# Make sure the dates are the same for all three
dates = [x.split('_')[0] for x in saved]
if len(set(dates)) is not 1:
	exit("The dates for the saved distance matrix mappings must be identical.")
date = dates[0]

# handles for the three saved mappings (maybe refactor this, but OK for now)
saved_paths = date + "_saved_paths.pkl"
saved_distances = date + "_saved_distances.npy"
saved_indices = date + "_saved_indices.npy"

# Now go ahead and open everything
with open(saved_paths, 'rb') as f:
	paths = pickle.load(f)

	# load the numpy arrays
	distances = np.load(saved_distances)
	indices = np.load(saved_indices)

	# ensure the total number of images is the same (number of rows)
	if not len(paths) == distances.shape[0] == indices.shape[0]:
		exit("Paths, distances, and indices must have same number of rows.")
	num_rows = len(paths)

	# ensure the number of neighbors is the same (the "K" in KNN)
	if not distances.shape == indices.shape:
		exit("Distances and indices must have same shape.")
	num_nbrs = distances.shape[1]

	# pick a random row from the matrix (avoid ) 3721 is great
	# 1509 is cover photo snakes and such
	# 376 Aunt Sue Puzzle Bureau headers
	# 2109 is parley's cabinet: image of children spinning globe by pyramids
	# this also occurs in universal history i think
	# 3231 is pretty great
	# idea: will ML pick up reverse traced images?? test out on UH to see what
	# their vector similarities are
	idx = 1509 #random.randint(0, num_rows)
	print("idx =", idx)

	# loop over the neighbors of this image and open them in OpenCV
	# first image is image itself; we will send array to montage 
	images = []
	images_full_page = []
	nearest_nbrs = [y for (x,y) in sorted(zip(distances[idx],indices[idx]),\
		key=lambda pair: pair[0])]

	# try to see how many of the images are coming from the same volume
	htids = {}
	htidx = 0

	for i, nbr in enumerate(nearest_nbrs):

		# HACK: paths should really have another column with just the HTID
		# this will break if other people not using my exact directory and OS
		# setup try to use it!!
		volume = paths[nbr].split('\\')[5]
		
		# keep track of which volumes we've seen
		if not volume in htids.keys():
			htids[volume] = htidx
			htidx = htidx+1

		# See: https://htrc.github.io/HTRC-WorksetToolkit/sdk.html
		# docs are still being written, so be safe since Solr API might not
		# always work or could require higher credentials
		#metadata = bib.volume_solr_metadata(volume)
		# ok this issue is that this keeps changing: 11/12/2017
		# and they made solr unavailable NOT giving an error just hanging
		metadata = bib.get_volume_metadata(volume)
		safe_metadata = bib.safe_volume_metadata(volume)

		#if not metadata:
		annotation = "{0:2}: {1:25}\t{2})".format(
				htids[volume],
				metadata['titles'][0][:25],
				','.join(metadata['publishDates'])
		)
		tag = "{},{}".format(i,htids[volume])
		#else:
		#	annotation = "{2:25.25}. {3:13.13}: {4:20.20}\t{5}\t{0:2}:{1:2}:{6}".format(
		#			i,
		#		htids[volume],
		#		metadata['title_top'][0],
		#		','.join(metadata['publication_place']),
		#		','.join(metadata['publisher']),
		#		','.join(metadata['publishDate']),
		#		volume
		#	)
		#	tag = "{},{}".format(i,htids[volume])
		
		# can look at this alongside the montage (eventually will be REACT UI)
		print(annotation)
		#exit("ok what are fields")


		img = cv2.imread(paths[nbr])
		if img == None:
			continue
		h,w = img.shape[:2]
		
		# Move away from this approach: not very elegant
		# Write some text on the image before appending it to array
		font = cv2.FONT_HERSHEY_SIMPLEX 
		cv2.putText(
			img,			# target image
			tag,			# text that will be drawn
			(10,h//2),		# pixel coordinates of bottom left corner
			font, 			# typeface
			5,				# scale factor (e.g. 2 would be double base size)
			(0,0,255),		# BGR color (full red)
			4,				# thickness of line
			True			# "bottomLeftOrigin" is (0,0) (otherwise top left)
		)
		
		images.append(img)

		# full page image is a directory up, outside of /extracted subfolder
		# N.B. this slash is different for Windows vs. Unix!
		full_page_path = paths[nbr].replace("\extracted", "")

		# strip out the _ex_[0-9]* tag
		extracted_tag = re.search("(_ex_[0-9]+)", full_page_path)
		if extracted_tag:
			extracted_tag = extracted_tag.group(1)
			full_page_path = full_page_path.replace(extracted_tag, "")

			# TODO: this is a hack, since extractor has jpg hardcoded into it
			# either insist on one format or re-run the extractor
			if not os.path.exists(full_page_path):
				full_page_path = full_page_path.replace("jpg", "png")


			images_full_page.append(cv2.imread(full_page_path))

			# https://github.com/htrc/htrc-feature-reader
			# http://www.porganized.com/
			# https://github.com/htrc/HTRC-WorksetToolkit
			# https://joshpeng.github.io/post/wsl/



	# concat the full pages onto the extracts; montage will page through the
	# extracts first and then the full page images
	images = images + images_full_page

	# construct montage: first tuple (width, height) then (columns, rows)
	# http://www.pyimagesearch.com/2017/05/29/montages-with-opencv/
	montages = build_montages(images, (166, 234), (5, num_nbrs//10))
	for montage in montages:
		cv2.imshow("Montage", montage)
		cv2.waitKey(0)
