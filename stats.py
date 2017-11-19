#!/usr/bin/python3

from collections import defaultdict
import fnmatch
import os
import sys


IMG_DIR = '/mnt/c/Users/stephen-krewson/Dropbox/parley-train'

year_hist = defaultdict(lambda: 0)
total = 0

for d in os.listdir(IMG_DIR):

	#print(d, end=': ')

	year_size = len(os.listdir(os.path.join(IMG_DIR, d)))

	#print(year_size)
	
	# round DOWN to the half-decade
	year_hist[int(d) - int(d) % 5] += year_size
	total += year_size
	
for k,v in sorted(year_hist.items()):
	print(k,'-',k+4,':',v)



print("Total images:", total)
