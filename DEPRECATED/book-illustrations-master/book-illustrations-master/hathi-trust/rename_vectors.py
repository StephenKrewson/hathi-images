"""
Author: Stephen Krewson

N.B. run from Anaconda prompt (Windows) in "tensorflow" environment

REVISION: use ImageMagick mogrify to add class labels and (place,date) and
put in a directory structure like that used by tensorflow and PyTorch where the
directory name IS the class label.

htid/extracted/img.jpg --> 

train/htid/htid_page.jpg [file annotated so accesible by Matlab]

USAGE: python3 ht_validate_files.py

MUST be run from the book-illustrations/hathi-trust folder

this gets the extracted images into a better shape; need diagnostics on which
years underrepresented; can then target those!


"""

from collections import defaultdict
import glob
from htrc import metadata as bib
import os
from shutil import copy2
import sys


count = 0
dates = defaultdict(lambda: 0)

# figure out how much we should chop off the front
dirpath = os.getcwd()
targetpath = "D:/stephen-krewson/Documents/vector5/"

# Does shell-style expansion with an iterator
# BAD! too many API calls. do 
# TODO: extraction for all the stuff on desktop
for d in glob.iglob(dirpath + "/*/vectors"):

	# the absolute filepath starting from the HTID, taken apart by slashes
	# WATCH OUT! this will change depending on OS of the shell
	# Right now it's set up for Windows Anaconda
	subpath = d[len(dirpath)+1:].split('\\')

	# from this, extract the HTID itself and lookup the metadata
	htid = subpath[0]
	metadata = bib.get_volume_metadata(htid)


	# we want (1) publish date, (2) publish place, (3) htid as embedded labels
	# in the image itself and also a more sensible data science file structure
	# https://wiki.htrc.illinois.edu/display/COM/HTRC+User+Getting+Started+FAQ
	# Looks like for this round we just have the date...might be OK actually
	pub_date = int(metadata['publishDates'][0])

	pub_date_rounded = pub_date - (pub_date % 5)
	
	#print(pub_date)
	#dates[int(pub_date)] += 1
	#count += 1

	# now loop over the files within d
	for f in os.listdir(d):

		page = f.split('_')[0]
		ext = f.split('.')[-1]

		# new filepath = htid_page.ext within folder named for year
		newpath = targetpath + str(pub_date_rounded) + "/" + htid + "_" + page + "." + ext 

		#print(newpath)

		# now copy this to new folder if it doesn't exist
		# N.B. this DOES overwrite
		copy2(os.path.abspath(os.path.join(d,f)), newpath)