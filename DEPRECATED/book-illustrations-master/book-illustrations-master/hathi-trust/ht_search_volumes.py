#!/usr/bin/python

from __future__ import print_function
import htrc
from hathitrust_api import BibAPI, SolrAPI
import json
import os
import sys

# workflow: run from the CL to concatenate IDs onto books.txt
# ./ht_search_volumes.py "title : 'Parley' AND publishDate : [1825 TO 1860]" >> books.txt

if len(sys.argv) < 2:
	print("USAGE: ./ht_search_volumes 'title : 'Peter Parley' AND publishDate : [1827 TO 1860]")
	exit("See: https://wiki.htrc.illinois.edu/display/COM/Solr+Proxy+API+User+Guide#SolrProxyAPIUserGuide-BasicQueries")

# NOTE: move as much as possible to htrc SDK, so perhaps the metadata calls
# establish a connection to the API (these are both public)
solr_api = SolrAPI()
bib_api = BibAPI()

# try the query
try:
	iterator = solr_api.getallids(sys.argv[1])
except:
	print("Something went wrong.")

# We don't want to repeat any of the IDs in books.txt
new_ids = set()
for new_id in iterator:
	new_ids.add(new_id)
	
# ensure no duplicates: https://docs.python.org/2/library/sets.html
# open in read and append mode, so we can write out new_ids
with open('books.txt', 'a+') as fp:
	old_ids = set(map(str.strip, fp))
		
	# update new_ids by removing all ids found in old_ids
	new_ids.difference_update(old_ids)	
	
	# concatenate new_ids onto the end of books.txt
	fp.write("\n".join(list(new_ids)))
	fp.write("\n")
	
# for sanity, we need to see the titles of these books
# so we need to sync the csv of mappings between ID and title
with open('mapping.txt', 'a') as fp:
	
	# write out the id, look up title of the volume
	# https://www.hathitrust.org/bib_api
	for id in list(new_ids):
	
		# do lookup based on Hathi ID
		records = bib_api.get_single_record_json('htid', id)['records']
		
		# potentially multiple records per ID and multiple titles per
		# record (but we don't really care, just agglomerate the last one)
		for key in records:
			title = ','.join(records[key]['titles'])
		
		# was breaking on diacriticals; just show first 80 chars in case title
		# is super massive (we can always look up online using htid)
		title = id.strip() + "\t" + title[:80] + "\n"
		print(title)
		
		# ugh whatever, the API is not letting me through, try again in the
		# morning
		fp.write(title.encode("UTF-8"))
		
	# add closing newline
	fp.write("\n")

