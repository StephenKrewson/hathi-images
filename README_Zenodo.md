# Summary

This Zenodo repository contains customized models and derived metadata files from the "Deriving Basic Illustration Metadata" project, 2019-2020. The project was supported by an Advanced Collaborative Support Grant from the HathiTrust Research Council (HTRC). The following individuals worked on the project:

- Stephen Krewson (Yale University) -- Principal investigator
- Ryan Dubnicek (HTRC) -- Project manager
- Boris Capitanu (HTRC) -- Lead developer

Eleanor Dickson Koehl (HTRC) helped resolve questions about HathiTrust access permissions. Doug Duhaime (Yale DHLab) provided pointers about image vectorization and is the developer of the PixPlot visualization tool.

The code used to run the processing pipeline is available at GITHUB.

## File list

| File                                   | Description                                                  |
| -------------------------------------- | ------------------------------------------------------------ |
| `google_ids_1800-1850.txt.gz`          | A subset of the July 2019 Hathifile containing all volumes 1800-1850 that were digitized by Google. These volumes were the basis for all subsequent steps. |
| `hathi_field_list.txt`                 | The Hathifile column names                                   |
| `stage1_fastai-retrained-cnn.pkl`      | A convolutional neural network (CNN) retrained with 19C page images. Given a candidate page, returns the likeliest of 10 class labels. Only images labeled `inline_image` or `plate_image` were retained in Stage 1. |
| `stage2_mask-rcnn-bbox-weights.h5`     | A Mask-RCNN model developed by Matterport. The model was retrained with page images for which illustrated regions were annotated with a bounding box. Given an image, the model predicts regions of interest (ROIs) that are likely to contain illustrations. These ROI bounding boxes are used to crop the input image. |
| `roi-vectors.tar`                      | 1000-dimensional vector representations of all the cropped images (ROIs) from Stage 2. These vector representations were derived using InceptionV3, a standard image classification CNN. |
| `early-19C-illustrations_metadata.csv` | Each row of this summary table corresponds to one of the 2.5m ROIs derived by the project. The fields are: `htid`, |
|                                        |                                                              |
|                                        |                                                              |
|                                        |                                                              |

