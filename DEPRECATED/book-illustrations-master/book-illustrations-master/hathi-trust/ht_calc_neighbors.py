"""
Author: Stephen Krewson

Given a directory containing folders named with HathiTrust unique volume ID,
this script runs through each folder and combines the .npy arrays in its
/vectors subfolder into a nearest neighbors matrix.

Saves matrix as nearest_neighbors_DATE.npy

N.B. run from Anaconda prompt (Windows) in "tensorflow" environment

USAGE: python ht_calc_neighbors.py
"""


import cv2
import glob
import datetime
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import os
import pickle
from sklearn.neighbors import NearestNeighbors
import sys


class Neighbors():
	def __init__(self, location=None):
		# quit early if supplied directory is not a directory
		try:
			if not os.path.isdir(self.location):
				exit("Please provide a valid directory.")
		# default to the current directory if none given
		except AttributeError:
			self.location = os.getcwd()

		# only calculate the 30 closest neighbors
		self.K = 30

		# validate the project structure
		# really consider using ht sdk for collections
		for d in os.listdir(self.location):
			if os.path.isdir(d):
				print(d)
			else:
				print("not a directory", d)


	def run(self):
		# first load the arrays out of their files before shaping
		# remember the corresponding path to each image
		arrays = []
		paths  = []

		# iterator gives back everything in volume folders that is array
		# for July 2017 Parley 1827-1855 run, there were 4383 vectors!
		for f in glob.iglob(self.location + "/*/vectors/*npy"):
			arrays.append(np.load(f))

			# ASSUMES: within project, both /extracted and /vectors exist
			# consequenctly, image has same base name, minus .npy extension
			# we will also need to move up and over into the img/ directory
			path = f.rsplit('.', 1)[0]
			path = path.replace("vectors", "extracted")
			paths.append(path)

		# shape should be N (images) x 2048
		X = np.stack(arrays, axis=0)
        print("shape=", X.shape)
        exit(0)
        # from tutorial: http://scikit-learn.org/stable/modules/neighbors.html
        # should I parameterize the K value?
        nbrs = NearestNeighbors(n_neighbors=self.K).fit(X)
        distances, indices = nbrs.kneighbors(X)

        '''
		# annotate the saved stuff with a date
		d = datetime.date.today()

		# save the array of paths that map to nearest neighbors matrix
		with open('{}_saved_paths.pkl'.format(d.isoformat()), 'wb') as f:
			pickle.dump(paths, f)

		# save the neighbor mapping in the matrix itself
		np.save('{}_saved_distances.npy'.format(d.isoformat()), distances)
		np.save('{}_saved_indices.npy'.format(d.isoformat()), indices)

		print("Nearest neighbors calculation complete.")
		print(distances.shape)
		print(indices.shape)
		print(len(paths))
		'''

# In case we want to run in standalone mode from CLI
if __name__ == '__main__':

	if len(sys.argv) > 2:
		exit("too many args")

	if len(sys.argv) is 2:
		neighbors = Neighbors(sys.argv[1])
	else:
		neighbors = Neighbors()

	# generate the matrix and save
	#neighbors.run()
