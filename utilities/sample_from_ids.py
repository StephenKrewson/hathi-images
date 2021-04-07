# Stephen Krewson, July 23, 2019
#
# Given a subset of HathiFile, randomly sample an appropriate number of
# records and then get a list of all IMG_ON_PAGE. Save as pickled file?
#
# Idea is to pass to utility for downloading

import pandas as pd
import pickle
from random import sample, seed
import sys


# hardcode this for now...
SUBSET = "all_ids_1800_1850.csv.gz"
SAMPLE = "sample_ids_1800_1850.pkl"


def calculate_sample_size(n):
    # Z table value for 95% confidence interval (normal distribution)
    Z = 1.96
    # probability in population of having attribute (in this case, we could
    # think of half of books being illustrated); assuming 50% gives the
    # maximum variability and is safest assumption
    p = 0.5
    # precision rate of 2%--just using some pretty standard values
    e = 0.02

    # Cochran's formula
    # https://petewarden.com/2017/12/14/how-many-images-do-you-need-to-train-a-neural-network/
    # https://www.checkmarket.com/blog/how-to-estimate-your-population-and-survey-sample-size/
    # https://www.checkmarket.com/sample-size-calculator/
    size = Z**2 * p * (1 - p) / e**2

    # adjust by population size n
    adjusted = size / 1 + ((size - 1) / n)
    return round(adjusted)


def ht_file_sample(htfile):
    """
    Statistically defensible sample of volumes from HathiFile
    - Assumes: htfile is already filtered in desired way
    - Assumes: Column 1 is the Hathi unique identifier
        (because filtering step adds an index)
    - Assumes: separator is a comma (default for to_csv)
    """

    # Ensure consistency across runs
    seed(42)

    # Don't assume the subset is small enough to read directly into memory!
    # col 0: volume_id, col 16: pub_date
    iter_csv = pd.read_csv(
        htfile, 
        sep=',', 
        header=None, 
        engine='c', 
        iterator=True,
        chunksize=10000,
        error_bad_lines=False)

    # build up a list of all ids
    volumes = []
    for chunk in iter_csv:
        volumes += chunk[1].tolist()

    # calculate sample
    N = len(volumes)
    n = calculate_sample_size(N)
    sample_ids = sample(volumes, n)
    
    #print("Sampled {} from {} items".format(n, N))
    return sample_ids


# USAGE: python sample_from_ids.py
if __name__ == '__main__':

    sample_ids = ht_file_sample(SUBSET)

    with open(SAMPLE, 'wb') as fp:
        pickle.dump(sample_ids, fp)
