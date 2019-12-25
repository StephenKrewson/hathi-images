from collections import Counter
import json
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

counts = []


with open("output.jsonl", 'r') as fp:
    for i, line in enumerate(fp):
        data = json.loads(line)
        page_count = len(data['pages'])
        if page_count == 975:
            print(data)
            break
        if i % 10000 == 0:
            print(i, page_count)
        counts.append(page_count)

"""
print(len(counts))

mean = np.mean(counts)
median = np.median(counts)
mode = stats.mode(counts)
maxcount = max(counts)

print("mean, median, mode, and max")
print(mean, median, mode, maxcount)

bins = [1,2,4,10,20,40,100,200,400,maxcount]

plt.hist(counts, bins=bins)
plt.title("Histogram of illustrated page counts (n=183553)")
plt.xlabel("Count of illustrated pages in volume")
plt.xticks([1,20,40,100,200,400,maxcount])
plt.ylabel("Number of volumes")
plt.show()
"""