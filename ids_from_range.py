# Stephen Krewson, June 25, 2019
#
# Refactors functionality from classify-image-junk/src/sample.py

import pandas as pd


# Usually around 1 GB in size; just DL and store locally
# updates are not super important for this project
HATHIFILE = "hathifiles/hathi_full_20190601.txt.gz"
HATHICOLS = "hathifiles/hathi_field_list.txt"


def ids_from_hathifile(start, end):
    """
    Return all volumes from start to end, inclusive
    HathiFiles stored at: https://www.hathitrust.org/hathifiles
    Currently (2019) the only way to programmatically search HT
    """

    # June 2018 is 4GB! col 0=volume_id, col 16=pub_date
    # https://stackoverflow.com/questions/25962114/how-to-read-a-6-gb-csv-file-with-pandas
    # https://stackoverflow.com/questions/13651117/how-can-i-filter-lines-on-load-in-pandas-read-csv-function

    # 
    iter_csv = pd.read_csv(HATHIFILE, sep='\t', header=HATHICOLS, engine='c', 
        dtype={0: 'str', 16: 'object'}, usecols=[0,16], iterator=True, 
        chunksize=10000)

    df = pd.DataFrame()

    # N.B. not all pub dates are valid numbers
    count = 0
    for chunk in iter_csv:
        count += 1
        if count % 50 == 0:
            print(count)

        # force each chunk to have valid publication date
        chunk[16] = chunk[16].apply(pd.to_numeric, errors='coerce')
        chunk = chunk.dropna()
        
        # add this chunk to total
        df = pd.concat([
            df,
            chunk[(chunk[16] >= start) & (chunk[16] <= end)]], 
            ignore_index=True)

    print("Size:", df.shape)
    return df


# TODO: use argparse
if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.exit("USAGE: python -m src.ids_from_range <START_DATE> <END_DATE> <OUT.csv>")

    # positional args
    start = argv[1]
    end = argv[2]
    out = argv[3]

    print("Creating {} for HathiTrust volumes from {} TO {}.".format(out, start, end))

    volumes = ids_from_hathifile(start, end)