#!/usr/bin/python

from __future__ import print_function
from config import ht_keys as ht
from hathidata.api import HathiDataClient
import json
import os
import sys


# establish a connection to the APIs
access_key = ht['access_key']
secret_key = ht['secret_key']
data_api = HathiDataClient(access_key, secret_key)

# prefer non-compressed images
IMG_FORMAT = "png"
IMG_RES = 0

# workflow: books.txt has unique HathiTrust ids, one per line
# if no top-level folder exists with that name (the id), then the images have
# not been downloaded; the advantage of this method is not needing to use PDFs
# Using: https://github.com/iainwatts/hathidata/blob/master/hathidata/api.py
with open('books.txt', 'r') as fp:
	books = fp.readlines()
	
	for doc_id in books:
	
		# remove trailing newline and split at the tab character
		doc_id = doc_id.strip()
		
		# ignore books that have already been processed
		# ignore hathi IDs that have problematic forward slashes
		if os.path.isdir(doc_id) or '/' in doc_id:
			print("skipping", doc_id)
			continue
		
		print("attempting to download illustrations for", doc_id)
		
		# otherwise, get the pages with images using the Data API
		#volume_metadata = json.loads(data_api.getmeta(doc_id, json=True))
		vol_meta = json.loads(data_api.request_vol_meta(doc_id, "json"))
		sequence = vol_meta['htd:seqmap'][0]['htd:seq']
	
		image_pages = []
		
		# there will be at least one feature; often 2 or 3 (convert to set)
		for page in sequence:
		
			# sometimes the feature list contains blank dictionaries, which
			# makes it unhashable (so skip making it a set)
			features = page['htd:pfeat']
			if 'IMAGE_ON_PAGE' in features:
				image_pages.append(page['pseq'])
				
		print(image_pages)
		
		# now need to create folder and then put images in it
		print("Making directory for,", doc_id)
		os.makedirs(doc_id)
		
		# download that page
		for seq in image_pages:
		
			img = data_api.request_page_image(
				doc_id,
				seq,
				IMG_FORMAT,
				IMG_RES
			)
		
			# destination for image is within subfolder ID; name is just seq
			dest = os.path.join(doc_id, seq + "." + IMG_FORMAT)
			
			# LOOK UP: speculative near eastern architecture
			# joseph-francois lafitau
			# johann fischer von erlach
			# connecting skyscraper with tower of babel
			# "skyward trend of thought" leeuwen
			
			# maybe use image library to see the type?
			with open(dest, 'wb') as img_fp:
				img_fp.write(img)
