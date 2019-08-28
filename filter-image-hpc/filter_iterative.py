# filter_iterative.py
#
# Based on: https://docs.fast.ai/tutorial.inference.html
#
# Input: a CSV file where an image resource is the *first* column
# Output: the same CSV file but with all the rows removed that do not
# have `inline_image`as the top prediction for the image
#
# Example usage, with export.pkl model file in the working directory:
#
# USAGE: python filter_iterative.py --input test.csv --output .

import argparse
import csv
from fastai.vision import open_image
import imageio
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Using a 12-class CNN model, runs inference on a CSV list of image assets and writes out a list of only those images for which the class inline_image was the highest prediction.')
    parser.add_argument('--input', required=True, type=str, help='Path to input CSV file.')
    parser.add_argument('--output', required=True, type=dir_path, help='Path to output directory for filtered CSV file. Must have write permissions.')
    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"dir:{path} is not a valid path.")


args = parse_args()

# Model called export.pkl by default; should be in same dir as script
learner = load_learner(".")

# Full class list in learner.data.classes
good_labels = ["inline_image", "plate_image"]

# iterative, assumes only one filepath per line
with open(args.input) as csv_in:
    for row in csv_in:
        
        # split into path and extension
        img_path = row.rstrip()
        img, ext = os.path.splitext(img_path)
        print(img, ext)

        # convert from JP2
        #https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg-2000

        if ext is not "jpg":
            print("not a jpeg")
            continue
        
        #img = imageio.imread(image_path)
        #imageio.imwrite(img_dest, img, format=ext_out)

        image = open_image(img_path)
        label, _, _ = learner.predict(image)
        if str(label) in good_labels:
            print(image_path)

