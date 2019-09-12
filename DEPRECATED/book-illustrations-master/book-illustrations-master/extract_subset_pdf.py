import re
import sys
import os

from pdfrw import PdfReader, PdfWriter

loc_pages = "pages"
loc_books = "books"

# Store the human-coded page nums in simple txt files separated by commas
for f in os.listdir(loc_pages):
    with open(os.path.join(loc_pages, f)) as handle:
        data = handle.read().strip('\n')
        data = [int(p) for p in data.split(',')]
        print data
        
        # Corresponding book has same filename, diff extension
        path_book = os.path.splitext(f)[0] + ".pdf"
        path_book = os.path.join(loc_books, path_book)
        
        # Try to open it
        pages = PdfReader(path_book).pages
        out_data = PdfWriter()
        
        for p in data:
            out_data.addpage(pages[p-1])
        
        out_data.write('subset.%s' % os.path.basename(path_book))
