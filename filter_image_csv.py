# Stephen Krewson, August 24, 2019
#
# filter_image_csv.py
#
# Input: a CSV file where an image resource is the *first* column
# Output: the same CSV file but with all the rows removed that do not
# have `inline_image`as the top prediction for the image
#
# Run python filter_image_csv.py [--help] for usage 


import argparse
import csv
#from fastai.vision import *
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Using a 12-class CNN model, runs inference on a CSV list of image assets and writes out a list of only those images for which the class inline_image was the highest prediction.')
    parser.add_argument('--input', required=True, type=argparse.FileType('r'), help='Path to input CSV file.')
    parser.add_argument('--model', required=True, type=argparse.FileType('r'), help='Path to pickled CNN model.')
    parser.add_argument('--output', required=True, type=dir_path, help='Path to output directory for filtered CSV file. Must have write permissions.')
    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"dir:{path} is not a valid path.")


### Main script ###
args = parse_args()

# open the model (should be .pkl file)

# argparse has already opened the CSV chunk
for row in csv.reader(args.input):

    # now do inference
    print(row[0])
