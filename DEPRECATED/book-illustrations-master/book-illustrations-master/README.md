# book-illustrations
Code and ideas for extracting and collating images from books

Usage: `./download_img_archive.pl <archive.org unique book ID>`


# HathiTrust

I am using the HathiTrust Data API via [Bo Marchman's Python wrapper](https://github.com/rlmv/hathitrust-api).

The volume metadata exposes a sequence object, which in turn has feature
descriptions for each sequence item (essentially a page, though HT gives you the
mapping between the book's pages and the ordinal sequence number in the PDF).

One of the features is IMAGE_ON_PAGE, generated (I think) from the OCR process
that HT runs upon ingesting a book. At any rate, the idea is once again that
used by Kalev Leetaru: save time computing *where* the images are.




# TODO

setup new SSH for git auth

test once archive.org is back online...
