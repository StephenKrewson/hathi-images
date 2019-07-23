# Stephen Krewson, June 25, 2019
#
# Refactors functionality from classify-image-junk/src/sample.py

import pandas as pd
import sys


# Usually around 1 GB in size; just DL and store locally
# updates are not super important for this project
HATHIFILE = "hathifiles/hathi_full_20190601.txt.gz"
HATHICOLS = "hathifiles/hathi_field_list.txt"


def ids_from_hathifile(htfile, htcols, start, end):
    """
    Return all volumes from start to end, inclusive
    HathiFiles stored at: https://www.hathitrust.org/hathifiles
    Currently (2019) the only way to programmatically search HT
    """

    # June 2018 is 4GB! col 0=volume_id, col 16=pub_date
    # https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
    # https://stackoverflow.com/questions/13651117/how-can-i-filter-lines-on-load-in-pandas-read-csv-function

    # get tab-separated column names; there are 26
    # UPDATE! these names are wrong!
    with open(htcols, "r") as fp:
        col_names = fp.readline().strip('\n').split('\t')
        num_cols = len(col_names) 

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    iter_csv = pd.read_csv(
        htfile, 
        sep='\t', 
        header=None, 
        engine='c', 
        dtype={'htid': 'str', 16: 'object'},
        iterator=True,
        chunksize=10000,
        error_bad_lines=False)

    df = pd.DataFrame()

    # N.B. not all pub dates are valid numbers
    for chunk in iter_csv:

        # force each chunk to have a numeric pub date
        chunk[16] = chunk[16].apply(pd.to_numeric, errors='coerce')
        
        # concatenate valid rows, idx doesn't matter
        df = pd.concat(
            [df, chunk[(chunk[16] >= start) & (chunk[16] <= end)]],
            ignore_index=True)

    print("Size:", df.shape)
    return df


# TODO: use argparse
if __name__ == '__main__':

    if len(sys.argv) != 4:
        sys.exit("USAGE: python -m src.ids_from_range <START_DATE> <END_DATE> <OUT.csv>")

    # positional args
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    out = sys.argv[3]

    print("Creating {} for HathiTrust volumes from {} TO {}.".format(out, start, end))

    # get valid rows and save
    volumes = ids_from_hathifile(HATHIFILE, HATHICOLS, start, end)
    
    # will this work from Windows shell?? better to compress by hand
    volumes.to_csv(out, index=False, compression='gz')