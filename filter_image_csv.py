# Stephen Krewson, August 24, 2019
#
# filter_image_csv.py
#
# Takes a CSV with a column 
#
# Run python filter_image_csv.py [--help] for usage 


import argparse
from fastai.vision import *
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description='Using a 12-class CNN model, runs inference on a CSV list of image assets and writes out a list of only those images for which the class inline_image was the highest prediction.')

    parser.add_argument('--input', required=True, action='store_true', help='Path to input CSV file.')

    parser.add_argument('--fields', required=True, action='store_true', help='Path to .txt file listing column names for input CSV.')

    parser.add_argument('--output', required=True, action='store_true', help='Path to output directory for filtered CSV file. Must have write permissions.')
    
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)