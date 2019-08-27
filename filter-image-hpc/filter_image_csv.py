# Stephen Krewson, August 24, 2019
#
# filter_image_csv.py
#
# Input: a CSV file where an image resource is the *first* column
# Output: the same CSV file but with all the rows removed that do not
# have `inline_image`as the top prediction for the image
#
# Example usage, with export.pkl model file in the working directory:
#
# python filter_image_csv.py --input images.csv --model . --output .


import argparse
import csv
from fastai.vision import *
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


# N.B. export.pkl is in data/project with all the other model files and the data (on the us-west region VM)

# necessary on Windows
#https://pytorch.org/docs/stable/notes/windows.html#multiprocessing-error-without-if-clause-protection
#torch.multiprocessing.freeze_support()

### Main script ###
# Based on: https://docs.fast.ai/tutorial.inference.html
# image CSV and export.pkl need to be in same dir as the script itself

args = parse_args()
path = os.getcwd()

# fastai helper to work with list of image paths in first column of CSV
# takes a path to the directory where "export.pkl" is located
# `test` argument allows inference on multiple images
# `cols` is which column of the CSV to use for the image paths
imgs = ImageList.from_csv(".", args.input, cols=0)
learner = load_learner(".", test=imgs)

# normal invoke is preds,y -- but there are no ground truth labels!
preds,_ = learner.get_preds(ds_type=DatasetType.Test)

print(learner.data.classes)
print(preds)
ys = torch.argmax(preds, dim=1)


for i,y in enumerate(ys):
    print(imgs.items[i], y, learner.data.classes[y])


