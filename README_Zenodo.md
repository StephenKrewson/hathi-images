# Summary

This repository contains customized models and derived metadata files from the "Deriving Basic Illustration Metadata" project, 2019-2020. The project was supported by an Advanced Collaborative Support Grant from the HathiTrust Research Council (HTRC). The following individuals worked on the project:

- Stephen Krewson (Yale University) -- Principal investigator
- Ryan Dubnicek (HTRC) -- Project manager
- Boris Capitanu (HTRC) -- Lead developer

Eleanor Dickson Koehl (HTRC) helped resolve questions about HathiTrust permissions and data access. Doug Duhaime (Yale DHLab) provided pointers about image vectorization and is the developer of the PixPlot visualization tool: https://github.com/YaleDHLab/pix-plot.

The code used to run the processing pipeline is available at https://github.com/htrc/ACS-krewson. Links to project reports will be maintained in that repository's README.

Questions about the project should be directed to *stephen dot krewson at gmail dot com*.

## File list

| File                                             | Description                                                  |
| ------------------------------------------------ | ------------------------------------------------------------ |
| `google_ids_1800-1850.txt.gz`                    | A subset of the July 2019 Hathifile containing all volumes 1800-1850 that were digitized by Google. These volumes were the basis for all subsequent steps. |
| `hathi_field_list.txt`                           | The Hathifile column names                                   |
| `stage1_fastai-retrained-cnn.pkl`                | A convolutional neural network (CNN) retrained with 19C page images. Given a candidate page, returns the likeliest of 10 class labels. Only images labeled `inline_image` or `plate_image` were retained in Stage 1. |
| `stage2_mask-rcnn-bbox-weights.h5`               | A Mask-RCNN model developed by Matterport. The model was retrained with page images for which illustrated regions were annotated with a bounding box. Given an image, the model predicts regions of interest (ROIs) that are likely to contain illustrations. These ROI bounding boxes are used to crop the input image. |
| `roi-vectors.tar`                                | 1000-dimensional `numpy` arrays (`*.npy`) representing the cropped images (ROIs) from Stage 2. These vector representations were derived using InceptionV3, a standard image classification CNN. Their shape is `(1,1000)`. |
| `early-19C-illustrations_metadata.csv`           | Each row of this summary table corresponds to one of the 2,584,888 ROI crops. The fields are: `htid`, `page_seq`, `page_label`, `crop_no`, `vector_path`.This is allows easy browsing of a given page on Hathitrust: `https://babel.hathitrust.org/cgi/pt?id=<htid>&view=1up&seq=<page_seq>`. The `crop_no` field reflects the possibility that a page could have multiple ROIs on it. |
| `early-19C-illustrations_full-index_list.txt.gz` | A list of all vector files used in the creation of the full-dataset Annoy nearest neighbors index. The order in this file provides the integer indices from `0`to `n-1` for each vector in the `.ann` index. |
| `early-19C-illustrations_full-index.ann`         | A memory-mapped Annoy nearest neighbors index created from `early-19C-illustrations_full-index_list.txt.gz`. Should be accessed with`AnnoyIndex(1000, 'angular')` to match the dimension and metric parameters from when it was built. The index was built with 100 trees and is very fast for finding a reasonable number of neighboring vectors (<100 works well). |
| `pixplot-metadata_munroe-francis.csv`            | A metadata file derived by searching `google_ids_1800-1850.txt.gz` for publishers (the `imprint` field) matching the firm "Munroe [and] Francis" (and variants). For the 360 matching `htids`, 1477 ROI crops existed. While the image data is not available through Zenodo, the CSV contains the `*.jpg` filenames that follow the project's conventions. The fields conform to those used by the PixPlot viewer: `filename` (path to image file), `label` (name of the subset: in this case, "munroe-francis"), `description` (volume title),  `year` (volume year of publication). |

