# Stephen Krewson, June 25, 2019
#
# Refactors functionality from classify-image-junk/src/sample.py

import pandas as pd
import sys


# field names corrected July 1, 2019--using July data
HATHIFILE = "hathifiles/hathi_full_20190701.txt.gz"
HATHICOLS = "hathifiles/hathi_field_list.txt"


def ids_from_hathifile(htfile, htcols, start, end):
    """
    Return all volumes from start to end, inclusive
    HathiFiles stored at: https://www.hathitrust.org/hathifiles
    Currently (2019) the only way to programmatically search HT
    """

    # See: https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
    # https://stackoverflow.com/questions/13651117/how-can-i-filter-lines-on-load-in-pandas-read-csv-function

    with open(htcols, "r") as fp:
        col_names = fp.readline().strip('\n').split('\t')
        num_cols = len(col_names)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    iter_csv = pd.read_csv(
        htfile, 
        sep='\t', 
        header=None,
        names=col_names,
        engine='c', 
        dtype={'htid': 'str', 'rights_date_used': 'object'},
        iterator=True,
        chunksize=10000,
        error_bad_lines=False)

    df = pd.DataFrame()
    for i, chunk in enumerate(iter_csv):

        # 17m / 10k ~= 1700 chunks (30-60 minutes on my laptop)
        print("Processing chunk", i)

        # force each chunk to have an integer publication date
        # N.B unknown pub dates are marked with '9999'
        chunk['rights_date_used'] = chunk['rights_date_used'].apply(pd.to_numeric, errors='coerce', downcast='integer')
        
        # the conditions:
        # 1) date range within [START,END]
        # 2) access_profile_code == 'google' (ignore case)
        conditions = (chunk['rights_date_used'] >= start) & (chunk['rights_date_used'] <= end) & (chunk['access_profile_code'] == 'google') 

        # concatenate valid rows, idx doesn't matter
        df = pd.concat([df, chunk[conditions]], ignore_index=True)

    print("Size of filtered table:", df.shape)
    return df


# Using conda environment 'htrc'
if __name__ == '__main__':

    if len(sys.argv) != 4:
        sys.exit("USAGE: python ids_from_range.py <START_DATE> <END_DATE> <OUT.csv>")

    # positional args
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    out = sys.argv[3]

    print("Creating {} for Google-digitized HathiTrust volumes from {} TO {}.".format(out, start, end))

    # get valid rows and save (preserve HathiFile delimiter)
    volumes = ids_from_hathifile(HATHIFILE, HATHICOLS, start, end)
    volumes.to_csv(out, sep='\t', index=False, compression='gzip')
    