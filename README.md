# HTRC ACS project

"Generating basic illustration metadata" (2019-20)

- Midyear report: https://wiki.htrc.illinois.edu/display/COM/A+Half-Century+of+Illustrated+Pages%3A+ACS+Lab+Notes
- Final report: https://wiki.htrc.illinois.edu/display/COM/Advanced+Collaborative+Support+%28ACS%29+Awards [[pdf](https://wiki.htrc.illinois.edu/download/attachments/31588360/ACS-2019-2020-FinalReport-HathiTrust%2BNames.pdf?version=1&modificationDate=1595948576000&api=v2)]
- Zenodo repository: https://zenodo.org/record/3940528

Check the `_datasets` and `_image-labeling` folders for additional resources, such as `ivpy` montage tool. My current VM is described on fast.ai's [website](https://course.fast.ai/start_gcp). It can be accessed with:

```
gcloud beta compute ssh htrc-images
```

In fully-specified form this would be:

```
gcloud beta compute ssh --zone us-west1-b --project global-matrix-245215 htrc-images
```

Run `gcloud config list` to see what default values are being used. The user "jupyter" should be used for accessing fast.ai's Jupyter Notebooks.

## Downloading and backing up the full ROI dataset

Boris provided the crops via a temporary `rsync` endpoint at `proxy.htrc.indiana.edu::krewson/crops`. From within a `tmux` session on a VM with a 2TB boot drive, I ran:

```
$ rsync -aP --itemize-changes proxy.htrc.indiana.edu::krewson/crops .
```

This retrieved the entire `crops` folder containing the stubbytree hierarchy to the VM's persistent disk. The size was 553GB. Unfortunately, `gsutil rsync` tool did not work, since the HTRC server was not in Cloud Object format.

Since GPU quotas and buckets are also associated with projects, I stuck with the global-matrix-245215 project.

From the VM, after renaming the `crops` folder, I ran the following to copy the data to the cheaper bucket storage:

```
$ gsutil -m rsync -r hathitrust-full_1800-50/ gs://hathitrust-full_1800-50
```

I first tested with the flag `-n` to see what would happen. Don't select `-d` since this is a one-time transfer, and there is no need to delete extra files from the bucket. A key principle is to keep lots of data in the buckets, where it's cheaper to store. Then, extract subsets and run compute-intensive tasks on them (e.g. PixPlot vectorization).

- Conclusion: make boot disk the 2TB maximum. Mounting and resizing extra disks requires LOTS of extra knowledge of df and lsblk and growpart. Something to study up on, though.
- Other breakthrough: run tmux ON the remote server!! Then detach and exit. Job will hum merrily along. Otherwise, as soon as my laptop goes to sleep, the SSH connection is broken and it's all over. And it was too weird to run tmux within tmux. Just like the Zoo c. 2017!

- https://wiki.htrc.illinois.edu/display/COM/Downloading+Extracted+Features

- https://cloud.google.com/filestore/docs/copying-data

- https://cloud.google.com/storage/docs/gsutil/commands/rsync

- https://cloud.google.com/storage/docs/gsutil/commands/cp (for pure GCP transfers, I favor `rsync -m`)

- If you zipped the training images on Windows, you may need the [P7 tool](https://anaconda.org/bioconda/p7zip) to unzip them on the Linux Google VM. You need to create a conda environment to get the right permissions -- difficult!

  ```
  conda install -c bioconda p7zip
  7za x [.zip]
  ```

## HTRC 10-min presentation

- [x] [Data] Bought 4TB HDD drive
- [x] [Data] Waiting full 600GB dataset (in progress); process `carter-hendee` data from this

- [ ] [Viz] Build charts of images over time (similar to MHL project)
- [ ] [Viz] Pixplot questions for October 2020 demo:
  - Can you add additional data to same viz? (or is new folder created)
  - How can labels be used IN the browser? (colors? more info on click?)
- [Research] This HAS to be the angle on chapter 3 (but how to integrate with disability)
- [Research] Ask about volume deduplication (Underwood or Bamman, surely); can images be used for dedup?

https://course.fast.ai/start_gcp.html#step-4-access-fastai-materials-and-update-packages

Eliminate most-wrong. See: https://github.com/fastai/course-v3/blob/master/nbs/dl1/lesson2-download.ipynb (includes REST route); also https://towardsdatascience.com/fastai-image-classification-32d626da20.

https://docs.fast.ai/tutorial.inference.html


## HathiTrust APIs

UPDATE: I now favor `pip` and `venv` for all dependency management. `conda` is too unpredictable.

Bibliographic metadata can be fetched from HTRC workset [toolkit](https://github.com/htrc/HTRC-WorksetToolkit). 

Hathi's UI for advanced catalog search is [here](https://catalog.hathitrust.org/Search/Advanced). You still cannot add to a collection from catalog search! This is very limiting.

Third-party wrappers: 

- Data, Bib, and Solr (search) APIs: https://github.com/rlmv/hathitrust-api (now Python3 compatible: `pip install hathitrust-api`)

### HTRC Capsule

Login: `stephenkrewson` (password saved with Chrome)
Email: `stephen.krewson@yale.edu`


# Deprecated project structure (c. 2016)

| File                    | Purpose                                                      | Note                                                         |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `books.txt`             | list of books to download                                    | one unique HT ID per line; generated by `ht_search_volumes.py` |
| `config.py`             | stores HT API keys                                           | not versioned, you'll need to get your own keys              |
| `ht_download_images.py` | downloads all image pages for each book in `books.txt`       | if a folder already exists with the name of an ID it is skipped; IDs that contain colons are skipped |
| `ht_search_volumes.py`  | concatenates IDs returned from a bibliographic search onto `books.txt` | syntax for providing search fields (author, date, etc.) is given in a usage comment in the code |
| `ht_run_extraction.sh`  | creates the `extracted` subfolder within all volume directories | skips volume if `extracted` already exists                   |
| `ht_classify_score.py`  | from `extracted` subfolder, generates a corresponding Numpy array for each image in `vectors` sibling folder | adaptation of Inception model (2015)                         |

