from __future__ import print_function
import json


# hathitrust ids are within the "gather" field
with open("carter-hendee-metadata.json", "r") as fp:
    data = json.load(fp)
htids = [item['htitem_id'] for item in data['gathers']]

