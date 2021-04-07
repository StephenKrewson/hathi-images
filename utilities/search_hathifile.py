# Stephen Krewson, July 24, 2020
#
# Search HathiFile (excerpt) for publisher/publishing place
# Comment: I have pretty extensive experience with Internet Archive,
# but Hathi still has no search API

import pandas as pd
import re, sys


# the volumes used in the ACS project
HATHIFILE = "google_ids_1800-1850.txt.gz"

# corrected field names file. See also:
# https://www.hathitrust.org/hathifiles_description
HATHICOLS = "hathifiles/hathi_field_list.txt"


def search_hathifile(ht_file, col_file):
    """
    Return rows matching the query, as well as stubbytree path for htid
    """

    # See: https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
    # https://stackoverflow.com/questions/13651117/how-can-i-filter-lines-on-load-in-pandas-read-csv-function

    with open(col_file, "r") as fp:
        col_names = fp.readline().strip('\n').split('\t')
        num_cols = len(col_names)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    iter_csv = pd.read_csv(
        ht_file, 
        sep='\t', 
        header=None,
        names=col_names,
        engine='c',
        # quicker if we can assert some types for the fields
        dtype={
            'htid': 'str',
            'rights_date_used': 'object',
            'pub_place': 'str', # sadly, this is just the partner lib
            'imprint': 'str'
        },
        iterator=True,
        chunksize=5000,
        error_bad_lines=False)

    df = pd.DataFrame()


    # really good resource on fuzzy matching
    # http://jonathansoma.com/lede/algorithms-2017/classes/fuzziness-matplotlib/fuzzing-matching-in-pandas-with-fuzzywuzzy/

    for i, chunk in enumerate(iter_csv):

        # Use a basic regex with matching group
        # find: "Munroe, Francis", "Munroe and Francis", "Munroe & Francis"
        conditions = (chunk['imprint'].str.contains(
            r"\bMunroe(?:,| and| &) Francis\b",
            na=False,
            flags=re.IGNORECASE)
        )

        # concatenate valid rows, idx doesn't matter
        df = pd.concat([df, chunk[conditions]], ignore_index=True)

    print("Size of filtered table:", df.shape)
    return df


# Using conda environment 'htrc'
if __name__ == '__main__':

    # results from search query (hardcoded)
    volumes = search_hathifile(HATHIFILE, HATHICOLS)

    vols = volumes['htid'].tolist()

    # turn the vols into stubbytree structure
    # this should really be done in a notebook...
    for vol in vols:
        print(vol)
    