# HTRC ACS project

"Generating basic illustration metadata" (2019-20)

Midyear report

Final report

Zenodo repository

Some assets are located in non-versioned folders:

--- | ---

ivpy, which is in `_image-labeling`, I ran conda (ml-mhl?) from cmd prompt
crops are stored in ivpy/src/htrc for now.

## rsync

UPDATE: gsutil rsync does not work well. I'm running plain rsync into the VM. Hopefully the persistent disks are elastic. Otherwise, I'll run out of data.

Lessons: https://course.fast.ai/start_gcp

- Provisioned a persistent disk (PD) of 2TB ahead of time
- Used most up-to-date fast.ai libraries
- Quotas apply to projects, so be careful about deleting
- Buckets are also associated with projects -- ditto
- Stuck with the fastai19 project

https://wiki.htrc.illinois.edu/display/COM/Downloading+Extracted+Features

Boris (9/21/20): Ok, the crops are available via rsync at `proxy.htrc.indiana.edu::krewson/crops`.
For example, to rsync everything you could do:

```
$ rsync -aP --itemize-changes proxy.htrc.indiana.edu::krewson/crops .
```

This will retrieve the entire `crops` folder containing the stubbytree hierarchy to your disk… it’s about 550GB or thereabout.

The option `-P` means `--partial --progress`. Option `-a` means archive mode, which is recursive with hard-links turned into files and permissions/attributes NOT preserved. 

There is a file called `files.txt` in the crops/ folder that contains all the file paths in the stubby tree.
You can get this file listing only via:

```
$ rsync -aP proxy.htrc.indiana.edu::krewson/crops/files.txt .
```

- [x] Test the server by getting `files.txt` locally to WSL2 (109 MB)

Let me know if you have questions. Also let me know when you finish downloading all of it so I can remove the data.

The Google Cloud Storage version. Run from the VM, using a named tmux connection on my SSH connection, so that data doesn't flow through my local machine! Helpful links:

- https://cloud.google.com/filestore/docs/copying-data
- https://cloud.google.com/storage/docs/gsutil/commands/rsync

```
$ gsutil rsync [OPTION] src_url dst_url
```

Run with test flag `-n` to see what would happen. Don't select `-d` since this is a one-time transfer, and there is no need to delete extra files from the bucket.

```
$ gsutil -m rsync -n -r proxy.htrc.indiana.edu::krewson/crops gs://hathitrust-full_1800-50
```

How long does it take? Boris estimates 4-5 days. GCP says storage will cost about $12 per month.

## Status

- [x] [Data] Bought 4TB HDD drive
- [ ] [Data] Waiting full 600GB dataset (in progress); process `carter-hendee` data from this

- [ ] [Viz] Build charts of images over time (similar to MHL project)
- [ ] [Viz] Pixplot questions for October 2020 demo:
  - Can you add additional data to same viz? (or is new folder created)
  - How can labels be used IN the browser? (colors? more info on click?)
- [Research] This HAS to be the angle on chapter 3 (but how to integrate with disability)
- [Research] Ask about volume deduplication (Underwood or Bamman, surely)
  - Q: Can image comparison help with deduplication?

## Fast.ai workflow

Warning! Any tips and guides stored in the notebooks will be UNAVAILABLE if the instance goes down. So make sure to version this stuff in my own repo. Huge headache.

Remember to update library on the VMs:

https://course.fast.ai/start_gcp.html#step-4-access-fastai-materials-and-update-packages

Eliminate most-wrong. See: https://github.com/fastai/course-v3/blob/master/nbs/dl1/lesson2-download.ipynb (includes REST route); also https://towardsdatascience.com/fastai-image-classification-32d626da20.

### Invoke

Takeaways: deactivate all Conda (including base). Use pip 3.7. Build pixplot assets on the VM and then scp back to local. Works OK for smaller sized datasets. use the -m flag with some of the copy utils for parallel.

scp can be used with intstance name and zone argument supplied:

https://cloud.google.com/compute/docs/instances/transfer-files#transfergcloud

After starting up the VM from the Google Cloud console online, run in WSL (doesn't work in conda shell!):

> gcloud compute ssh --zone=us-west2-b jupyter@my-fastai-instance -- -L 8080:localhost:8080

Or, since the LA region is often unavailable:

> gcloud compute ssh --zone=us-east4-a jupyter@my-fastai-instance-east -- -L 8080:localhost:8080

The notebooks are [here](http://localhost:8080/tree).

http://www.robots.ox.ac.uk/~vgg/projects/seebibyte/index.html

https://docs.fast.ai/tutorial.inference.html

### Data Transfer

Use the browser tool to upload a zipped directory of training images to a Google Cloud Bucket. This is the easy part. Then [transfer from the bucket to the instance](https://cloud.google.com/storage/docs/downloading-objects), using `gsutil cp`. I needed to do this twice, since the West region VM is not usable anymore. Very frustrating.

> gsutil cp gs://[BUCKET_NAME]/[OBJECT_NAME] [SAVE_TO_LOCATION]
> gsutil cp gs://19c-book-illustrations/19c-book-illustrations.zip .

See:

https://cloud.google.com/storage/docs/gsutil/commands/cp

Finally, if you zipped the training images on Windows, you will need the [P7 tool](https://anaconda.org/bioconda/p7zip) to unzip them on the Linux Google VM. You need to create a conda environment to get the right permissions!

> conda install -c bioconda p7zip

Then, noting the weird syntax for the "extract" command:

> 7za x [.zip]

Difficult!


## HathiTrust APIs

UPDATE: I now favor `pip` and `venv` for all dependency management. `conda` is too unpredictable.

Bibliographic metadata can be fetched from HTRC workset [toolkit](https://github.com/htrc/HTRC-WorksetToolkit). 

Hathi's UI for advanced catalog search is [here](https://catalog.hathitrust.org/Search/Advanced). You still cannot add to a collection from catalog search! This is very limiting.

Third-party wrappers: 

- Data, Bib, and Solr (search) APIs: https://github.com/rlmv/hathitrust-api
	- Now Python3 compatible: `pip install hathitrust-api`

### HTRC Capsule

Login: `stephenkrewson` (password saved with Chrome)
Email: `stephen.krewson@yale.edu`

http://www.loc.gov/standards/mets/




# Deprecated

## Project Structure (2016)

N.B. this is not actively maintained. Q: how to make a table in Typora?

file | purpose | note

--- | --- | ---

`books.txt` | list of books to download | one unique HT ID per line; generated by `ht_search_volumes.py`
`config.py` | stores HT API keys | not versioned, you'll need to get your own keys
`ht_download_images.py` | downloads all image pages for each book in `books.txt` | if a folder already exists with the name of an ID it is skipped; IDs that contain colons are skipped
`ht_search_volumes.py` | concatenates IDs returned from a bibliographic search onto `books.txt` | syntax for providing search fields (author, date, etc.) is given in a usage comment in the code
`ht_run_extraction.sh` | creates the `extracted` subfolder within all volume directories | skips volume if `extracted` already exists
`ht_classify_score.py` | from `extracted` subfolder, generates a corresponding Numpy array for each image in `vectors` sibling folder | adaptation of Inception model (2015)

