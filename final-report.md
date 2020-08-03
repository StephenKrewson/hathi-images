---
title: "Derived Metadata for Early 19C Illustrations: ACS Grant Final Report"
author: "Stephen W. Krewson"
date: "August 3, 2020"
---

# Early 19C Illustration Metadata: Final Report

The "Deriving Basic Illustration Metadata" project has successfully concluded with the creation of a large and novel dataset of illustration metadata. The dataset was produced in four stages using two retrained convolutional neural networks as well as one standard model (InceptionV3).

The key deliverables of this projects are the following:

- A CSV file identifying all illustrated regions from HathiTrust volumes published between 1800 and 1850
- A nearest-neighbors index created from vector representations of these 2.5M regions of interest (ROIs)
- Sample notebooks for working with the metadata and index files

The metadata and index files are included in the project's [Zenodo repository](https://zenodo.org/record/3940528#.XyRNSZ5KjIU). The notebooks and project code can be found on [GitHub](https://github.com/htrc/ACS-krewson). For more detailed usage information, consult the README files for these repositories.

## Stage 1: Classification

We began by identifying all Google-digitized volumes published during the years 1800-1850 (inclusive). These **500,013** volumes are contained in the file `google_ids_1800-1850.txt.gz`, which is a subset of the July 2019 [Hathifile](https://www.hathitrust.org/hathifiles). The Hathifile fields include basic publication information and are listed in `hathi_field_list.txt`.

From this comprehensive set of early-nineteenth century volumes, we find all potentially illustrated pages using OCR-derived metadata. Apply a retrained CNN model to filter out noisy candidate pages.

This model is built with Tensorflow and is located here: `model1`. Code for interacting with the model is here.

My midpoint report describes the early steps in greater detail and can be found [here](https://wiki.htrc.illinois.edu/display/COM/A+Half-Century+of+Illustrated+Pages%3A+ACS+Lab+Notes).

## Stage 2: Region of interest (ROI) extraction

There **2,584,888** total ROIs. 

## Stage 3: Dimensionality reduction
## Stage 4: Indexing and visualization

## Project assets

Here is what is on Zenodo: https://zenodo.org/record/3940528 (DOI: 10.5281/zenodo.3940528).

https://wiki.htrc.illinois.edu/display/COM/A+Half-Century+of+Illustrated+Pages%3A+ACS+Lab+Notes

| File | Description |
| ---- | ----------- |
|      |             |
|      |             |
|      |             |

Link: 

2,584,888 numpy vectors. Each 4128 bytes. 15GB

Use of stubbytree vs. pairtree (old).

Deliverable: CSV with vectors attached???

### Project statistics

Total number of volumes: 183,553
Total number of page image files (scans): 1,922,602
Total size of above page image files: 685,371,546,511 bytes (685+ GB)
Total number of crops (generated in step2): 2,584,888
Total size of above crop files: 553,399,284,753 bytes (553+ GB)
Total size of text OCR for above pages: 2,407,897,173 bytes (2.4+ GB)
Page image formats:
   1,901,456 image/jp2
      21,269 image/tiff
Page image labels (from step1):
   1,077,544 inline_image
     845,181 plate_image

## Discussion

Discussion.

There are several applications for this dataset...

- Reverse image search

Cite Melvers and Smit and some other papers from MHL.

## Acknowledgements

That this project was successfully completed is due to the following individuals. Through a year of many changes, and my own lapses in concentration, they stuck with me and are fully responsible for a really nice result.

- Ryan Dubnicek, for his empathetic,  and calm project management
- Boris Capitanu for his technical abilities and good humor and willingness to 
- Eleanor Dickson Koehl, for perceptive questions about the project's place in the wider world of DH research
- Doug Duhaime for use of his vectorization code and generous advice. As well as for bringing this grant to my attention.
