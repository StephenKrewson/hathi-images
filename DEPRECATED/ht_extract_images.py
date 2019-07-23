"""
Author: Michael Menz

Usage: python ht_extract_images.py --images_dir <DIR> --output_dir <DIR>

Requirements: OpenCV, Python 2.7, numpy 

TODO
	- create Anaconda environment with HT reqs
	- handle pages with two or more engravings
"""


import argparse
import cv2
import numpy as np
import os
from random import shuffle


# bounds for side length in pixels of image
LOW_BOUND = 100

# threshold for overlap to remove image
OVERLAP_FRACTION = 0.3


class BoundingBox:
    def overlaps(self, abbox):
        diff = LOW_BOUND / 3
        x_condition = self.x1 < abbox.x0 - diff or abbox.x1 < self.x0 - diff
        y_condition = self.y1 < abbox.y0 - diff or abbox.y1 < self.y0 - diff
        if x_condition or y_condition:
            return False
        return True

    def __str__(self):
        return "((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1)

    def __repr__(self):
        return "((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1)

    def slice_image(self, img):
        return img[self.y0:self.y1, self.x0:self.x1]

    def meets_low_bound(self, low_bound):
        x_high = self.x1 - self.x0 > low_bound * 1.5
        y_high = self.y1 - self.y0 > low_bound * 1.5
        x_low = self.x1 - self.x0 > low_bound / 4
        y_low = self.y1 - self.y0 > low_bound / 4
        return (x_high or y_high) and (x_low and y_low)

    def expand_by_bbox(self, abbox):
        self.x0 = min(self.x0, abbox.x0)
        self.y0 = min(self.y0, abbox.y0)
        self.x1 = max(self.x1, abbox.x1)
        self.y1 = max(self.y1, abbox.y1)
        self.area = (self.y1 - self.y0) * (self.x1 - self.x0)

    def __init__(self, x, y, w, h):
        self.x0 = x
        self.y0 = y
        self.x1 = x + w
        self.y1 = y + h
        self.area = w * h


def combine_rectangles(rectangles):
    did_combine = True
    while did_combine:
        did_combine = False
        will_remove = []
        for i in range(len(rectangles)):
            for j in range(i):
                if rectangles[i].overlaps(rectangles[j]):
                    rectangles[j].expand_by_bbox(rectangles[i])
                    did_combine = True
                    will_remove.append(i)
        for index in sorted(list(set(will_remove)), reverse=True):
            rectangles.pop(index)


# def remove_text(rectangles, img):
#     will_remove = []
#     for i, bbox in enumerate(rectangles):
#         # filter out rectangles that are text
#         small_img = Image.fromarray(bbox.slice_image(img))
#         txt = pytesseract.image_to_string(small_img)
#         if len(txt) > 5 and txt.count('\\') < 5:
#             will_remove.append(i)
#     for index in sorted(list(set(will_remove)), reverse=True):
#         rectangles.pop(index)


def bounding_boxes_for_image(image_path):
    img = cv2.imread(image_path, 0)

    thresh, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # See: https://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack
    hierarchy, contours, _ = cv2.findContours(bw_img, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # check if (x,y) is top corner--ignore if so (bbox is just img itself)
        if w < LOW_BOUND / 4 or h < LOW_BOUND / 4 or (x == 1 and y == 1):
            continue
        bbox = BoundingBox(x, y, w, h)
        rectangles.append(bbox)

    # top 10 biggest bounding boxes
    rectangles = sorted(rectangles, key=lambda x: x.area, reverse=True)[:10]

    # filter out rectangles that are below the low bound
    # filter out rectangles that are simply image itself
    #rectangles = filter(lambda x: x.meets_low_bound(LOW_BOUND), rectangles)

    # remove_text(rectangles, img)
    # this is a complete hack and relies on fact that for initial HathiTrust
    # data, the first bounding box is the image itself AND there is usually
    # only one image per page (this decent assumption for Parley books)
    # need to return it as array, however, since rest of code expects array

    # ensure there's no index error for this hack
    if len(rectangles) < 2:
        return img, rectangles

    # old return value commented out
    return img, [rectangles[1]] #sorted(rectangles, key=lambda x: x.area, reverse=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='')
    parser.add_argument('--image_dir', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    parser.add_argument('--low_bound', type=int, default=250)
    parser.add_argument('--overlap', type=float, default=0.8)
    args = parser.parse_args()

    if not args.image_path and not args.image_dir:
        print('Please provide an image_path or an image_dir')
        exit(1)

    image_paths = []
    prefixes = []
    extensions = []

    if args.image_dir:
		# make sure we only get files and not subdirectories
        filenames = filter(lambda x: os.path.isfile(os.path.join(args.image_dir, x)), os.listdir(args.image_dir))
        #print "testing", filenames
        for filename in filenames:

            image_paths.append(os.path.join(args.image_dir, filename))
            prefixes.append(filename.split('.')[0])
            extensions.append(filename.split('.')[1])
            # also store the extension

    else:
        image_paths.append(args.image_path)
        prefixes.append(args.image_path.split('.')[0])

    LOW_BOUND = args.low_bound
    OVERLAP_FRACTION = args.overlap

    for prefix, image_path, extension in zip(prefixes, image_paths, extensions):
        img, bboxes = bounding_boxes_for_image(image_path)


        for i, large in enumerate(bboxes):
            illustration = large.slice_image(img)

            if not args.output_dir:
                cv2.imshow("illustration %d" % (i), illustration)
                cv2.waitKey(0)
            else:
                # fixed bug where this was hardcoded for jpegs
                outpath = os.path.join(args.output_dir,
                                       "%s_ex_%d.%s" % (prefix, i, extension))
                cv2.imwrite(outpath, illustration)
