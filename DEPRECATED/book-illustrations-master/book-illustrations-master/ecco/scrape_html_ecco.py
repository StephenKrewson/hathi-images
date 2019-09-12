# Use to scrape Gale ECCO html files for the "illustrations" list
# Generates a csv file with all the "illustrated" pages listed in
# the TOC file for that particular ECCO record.

import csv
import os
import re

from collections import defaultdict
from itertools import izip_longest

# Data structure for the page numbers
images = defaultdict(lambda: [])

# Where we keep html to be scraped
location = "html"

# Loop over html files
for f in os.listdir(location):
    
    # Grab a file and search it for the pattern
    with open(os.path.join(location, f)) as handle:
        data = handle.read()
        
        # No need for groups, <page_no> is just a placeholder
        # Tested at: https://regex101.com/#python
        matches = re.findall(r"\|(?P<page_no>\d*)\|Illustration", data)
        
        # Convert to integers
        matches = [int(m) for m in matches]
        
        # remove duplicates
        pages = set(matches)
        pages = list(sorted(pages))
        
        # Put the file # in the list because dict is unsorted
        images[f] = pages
        images[f].insert(0, f)
        

# Now write it out to csv
with open('output/ecco.csv', 'wb') as f:
    writer = csv.writer(f)
    
    # Zip list columns into rows
    rows = images.values()
    
    # For quick-n-dirty printout to screen . . .
    print '\n'.join(map(str, rows))
     
    for row in rows:
        writer.writerow(row) 
