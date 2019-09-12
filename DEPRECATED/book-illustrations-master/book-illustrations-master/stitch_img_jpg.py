# This code takes a directory of images, turns them into rows of thumbnails
# and inserts blank image spacers in order to "align" the rows.

import numpy as np
import os
import re
import sys

from collections import defaultdict, OrderedDict
from PIL import Image, ImageDraw, ImageFont

from config import blanks_map

# Based on my workflow, just get info from filenames
location = sys.argv[1] #"img_universal"

# Adapted from this thread: http://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
imgs_dict = defaultdict(lambda: {})

# Get some info img.size() gives width, height tuple
imgs_width = []
imgs_height = []

# Loop over all the files and store them
# needs to be done at level of filename
for f in os.listdir(location):
	
	# Get unique ID (for now, just pub. year) and page #
	pub_id = f[:4]
	pub_order = re.findall(r"(?P<position>\d*).jpg", f)
	pub_order = int(pub_order[0])

	# Path to the image; open it as grayscale
	fp = os.path.join(location, f)
	temp_img = Image.open(fp).convert('L')
	
	# Rotate if landscape
	if temp_img.size[0] > temp_img.size[1]:
		temp_img = temp_img.rotate(90)

	# Store the sizes
	imgs_width.append(temp_img.size[0])
	imgs_height.append(temp_img.size[1])
	
	# Add the image to the data structure
	imgs_dict[pub_id][pub_order] = temp_img

# Take average
img_width = int(np.average(imgs_width))
img_height = int(np.average(imgs_height)) 
avg_size = (img_width/8, img_height/8)

print "Each image has dimensions (in pixels):", avg_size

# Just keep it black (color default)
blank_img = Image.new('1', avg_size)

# Store unprocessed rows
rows_unproc = []
row_titles = []
max_imgs = 0

for key, values in sorted(imgs_dict.iteritems()):
	
	row_titles.append(key)
	row_temp = []
	# Go through sorted pages
	for pg in sorted(values):
		if pg in blanks_map[key]:
			for i in range(blanks_map[key][pg]):
				row_temp.append(blank_img)
		
		# Resize the image
		imgs_dict[key][pg] = imgs_dict[key][pg].resize(avg_size)
		
		# Add num for page sorting
		font = ImageFont.truetype("fonts/arial.ttf", 48)
		draw = ImageDraw.Draw(imgs_dict[key][pg])
		draw.text((0, 0), str(pg), 50, font=font)
		
		# Always append the image
		row_temp.append(imgs_dict[key][pg])
	
	# If we add blanks, update the max length accordingly
	if len(row_temp) > max_imgs:
		max_imgs = len(row_temp)
		
	# Add it (unprocessed) to the master list
	rows_unproc.append(row_temp)
	
	
# Master list for processed rows
rows_comb = []

# Now go back through once we know maximum
title = 0
for r in rows_unproc:

	# Add padding
	for i in range(len(r), max_imgs):
		r.append(blank_img)
	
	# Process the row
	row_proc = np.hstack(np.asarray(i) for i in r)
	row_proc = Image.fromarray(row_proc)
	
	# Draw in key label
	font = ImageFont.truetype("fonts/arial.ttf", 72)
	draw = ImageDraw.Draw(row_proc)
	draw.text((0, 0), row_titles[title], 255, font=font)
	title += 1
	
	# Now add it to the list of rows
	# Need to do this OUTSIDE
	rows_comb.append(row_proc)

# FINALLY, outside all the loops...
# Combine all the rows
cols_comb = np.vstack((np.asarray(i) for i in rows_comb))
cols_comb = Image.fromarray(cols_comb)
cols_comb.save('wondergrid.jpg')
