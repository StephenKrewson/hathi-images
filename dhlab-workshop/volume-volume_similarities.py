from __future__ import print_function
from collections import defaultdict
from config import ht_keys as ht
from gensim.corpora import Dictionary
import gensim.downloader as api
from gensim.matutils import softcossim
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity, SoftCosineSimilarity
from hathidata.api import HathiDataClient
from htrc_features import FeatureReader
from itertools import chain
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
sns.set()

# figure out how to save this
w2v_model = api.load("glove-wiki-gigaword-50")

# establish a connection to the data API
access_key = ht['access_key']
secret_key = ht['secret_key']
data_api = HathiDataClient(access_key, secret_key)

# extract list of pages with images from each volume
vol_ids = ["hvd.32044021161005","osu.32435078698222"]
vol_image_pages = []
for vol in vol_ids:
	vol_meta = json.loads(data_api.request_vol_meta(vol, "json"))
	sequence = vol_meta['htd:seqmap'][0]['htd:seq']
	image_pages = [int(page['pseq']) for page in sequence if 'IMAGE_ON_PAGE' in page['htd:pfeat']]
	vol_image_pages.append(image_pages)

# init feature-reader on volume list
fr = FeatureReader(ids=vol_ids)

# build up dictionary keyed on tokens, sum counts over all volumes
counts = defaultdict(lambda: 0)
for vol in fr:
    VTL = vol.tokenlist(pages=False,case=False,pos=False,page_freq=False)
    VTL = VTL.reset_index()
    temp = VTL.to_dict('index')
    for k,v in temp.items():
        counts[v['lowercase']] += int(v['count'])

# mappings for both directions: just use an incrementing index as the ID
id2word = {}
word2id = {}
for i,k in enumerate(counts.keys()):
    id2word[i] = k
    word2id[k] = i
    
# additional brackets since from_corpus method takes a list argument
corpus = [[(word2id[k],v) for k,v in counts.items()]]

# gensim magic
dct = Dictionary.from_corpus(corpus, id2word=id2word)
similarity_matrix = w2v_model.similarity_matrix(dct)

# iterate back over volumes to treat image pages as docs
# loop over all the pages with images, each page becomes doc in BoW format
bow_docs = []
bow_idxs = []

for i,vol in enumerate(fr):
	#print(i,vol)
	# tokenlist from the entire volume, preserving page location info
	PTL = vol.tokenlist(case=False,pos=False)

	for pg in vol_image_pages[i]:
		try:
			bow = [(dct.token2id[k[1]],int(v['count'])) for k,v in PTL.loc[pg].to_dict('index').items()]
			bow_docs.append(bow)
			bow_idxs.append(str((vol.year,pg)))
		except KeyError:
			print(vol.year, "Page contains no OCR text:", pg)

# Outside of loop
# we will compare soft cos w2vec similarities against tf-idf
softcos_index = SoftCosineSimilarity(bow_docs, similarity_matrix, num_best=10)
tfidf_model = TfidfModel(bow_docs)


softcos_sims = MatrixSimilarity(softcos_index[bow_docs], num_features=len(dct))
tfidf_sims = MatrixSimilarity(tfidf_model[bow_docs], num_features=len(dct))

