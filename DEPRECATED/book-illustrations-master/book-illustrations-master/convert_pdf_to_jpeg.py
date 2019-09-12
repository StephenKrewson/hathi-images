import os
import re
import sys

from wand.image import Image

with Image(filename='books/subset.1837_Universal_Boston.pdf') as img:
    
    # Easier to work in blob format
    blob = img.make_blob('pdf')
    pdf = Image(blob=blob)
    
    pages = len(pdf.sequence)
    print "Pages =", pages
    
    image = Image(
        width=pdf.width,
        height=pdf.height * pages
    )
    
    for i in xrange(pages):
        image.composite(
            img.sequence[i],
            top=pdf.height * i,
            left=0
        
        )
    
    img.make_blob('jpeg')


def convert_pdf_to_jpeg(blob):
    '''From stack overflow'''
    
    pdf = Image(blob=blob)
    pages = len(pdf.sequence)
    
    print pages

    image = Image(
        width=pdf.width,
        height=pdf.height * pages
    )

    return image.make_blob('jpg')
    
# Call the function
#convert_pdf_to_jpeg(Image(blob=open('books/subset.1837_Universal_Boston.pdf')))
