from __future__ import print_function
from config import ht_keys
from hathidata.api import HathiDataClient
import json
import os
import sys

# USAGE: python download_image_pages.py
# run from the top-level repo folder


# connect
access_key = ht_keys['access_key']
secret_key = ht_keys['secret_key']
data_api = HathiDataClient(access_key, secret_key)

# insert your project name here
project = "carter-hendee"

with open(project + "_images.json", "r") as fp:
    volumes = json.load(fp)

# create <project> and img,ocr subfolders
if not os.path.exists(project):
    os.makedirs(project)
    os.makedirs(os.path.join(project,"img"))
    os.makedirs(os.path.join(project,"ocr"))
else:
    print("Project folder already exists:", project)


# just to save time: don't download books with lots of images but
# no actual images! two of these are music
# we don't delete at level of collection because it's useful to know
# what the mislabelings are in the collection (for classifier training)
blacklist = ["hvd.ah65up", "hvd.ah65u4"] #["mdp.39015030382652", "hvd.32044044506970", "hvd.ah65up","hvd.ah65u4"]

# loop over all volumes in the workset
idx = 0
for k,v in volumes.items():
    idx += 1

    # impermissible characters in directory names:
    # remember the mapping
    # : --> _
    # / --> -
    safe_k = k.replace(":","_")
    safe_k = safe_k.replace("/","-")

    img_dir = os.path.join(project,"img",safe_k)
    ocr_dir = os.path.join(project,"ocr",safe_k)

    # skip if directory is already created
    if os.path.isdir(img_dir) or os.path.isdir(ocr_dir) or k in blacklist:
        print("\tskipping", k)
        continue
    
    # status bar of sorts...
    print("[{}]\t{} images in volume={}".format(idx,len(v),k))
    # removing this check to get EVERYTHING
    if len(v) < 0:
        print("\tskipping: too few or too many images.")
        continue

    # otherwise, create the folders in each subfolder
    os.makedirs(img_dir)
    os.makedirs(ocr_dir)

    # loop over all the pages in the key value
    for pg in v:

        # resolution and format are defaults
        try:
            img = data_api.request_page_image(k, pg, resolution=0)
        except Exception as e:
            print("Could not download image on page {} (vol={})\t{}".format(pg,k,e))

        # the page before, if available
        try:
            ocr1 = data_api.request_page_ocr(k, pg-1)
        except Exception as e:
            print("Error on page {} (vol={})\t{}".format(pg,k,e))
            ocr1 = ""
        
        # the image page
        try:
            ocr2 = data_api.request_page_ocr(k, pg)
        except Exception as e:
            print("Error on page {} (vol={})\t{}".format(pg,k,e))
            ocr2 = ""
        
        # the page after, if available
        try:
            ocr3 = data_api.request_page_ocr(k, pg+1)
        except Exception as e:
            print("Error on page {} (vol={})\t{}".format(pg,k,e))
            ocr3 = ""

        # concat into three-page window
        ocr_combined = "{} {} {}".format(ocr1, ocr2, ocr3)
        
        # destination for image is within subfolder ID; name is just seq
        img_out = os.path.join(img_dir, str(pg) + ".png")
        ocr_out = os.path.join(ocr_dir, str(pg) + ".txt")
        
        # write out the image
        with open(img_out, 'wb') as fp:
            fp.write(img)

        # write out the ocr
        with open(ocr_out, 'w') as fp:
            fp.write(ocr_combined)

    # just do the first volume for now...
    #break

