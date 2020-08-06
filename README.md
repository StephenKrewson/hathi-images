# HathiTrust Projects

Code and assets from 2016 Data Mining project as well as 2019 HTRC collaborative grant. Contains instructions for accessing HT APIs and using fastai for model training.


Conda broke on WSL, need to fully clean up . files in ~

For ivpy, which is in (underscore) image-labeling, I ran conda (ml-mhl?) from cmd prompt
worked fine, though globbing and path names are an abomination. need to use that Path libary from fastai
crops are stored in ivpy/src/htrc for now.

need to commit the montage from the projects-htrc file.

do this on Wed.


## Todo

- [x] June 11: Project kickoff
- [x] June 25: Get/upload all 1800-1850 metadata from HathiFiles
- [ ] July 9: ???
- [ ] July 23: Sample list?
- [ ] August 19: eliminate most-wrong. See: https://github.com/fastai/course-v3/blob/master/nbs/dl1/lesson2-download.ipynb (includes REST route)
	- https://towardsdatascience.com/fastai-image-classification-32d626da20
- [ ] August 19: Map predictions over list of image URLs (DataBunch)
- [ ] August 20: Meeting! (nothing on Slack)

## Fast.ai Workflow

Warning! Any tips and guides stored in the notebooks will be UNAVAILABLE if the instance goes down. So make sure to version this stuff in my own repo. Huge headache.

Remember to update library on the VMs:

https://course.fast.ai/start_gcp.html#step-4-access-fastai-materials-and-update-packages

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

### Training

We'll use Lesson 2 - Download a Data Set as our guide and throw it in this repo.


## Hathi Search and APIs

Bibliographic metadata can be fetched from HTRC workset [toolkit](https://github.com/htrc/HTRC-WorksetToolkit). Recommended install is with [Anaconda](https://anaconda.org/pypi/htrc).

Hathi's UI for advanced catalog search is [here](https://catalog.hathitrust.org/Search/Advanced). You still cannot add to a collection from catalog search! This is very limiting.

Third-party wrappers: 

- Data, Bib, and Solr (search) APIs: https://github.com/rlmv/hathitrust-api
	- Now Python3 compatible; actively merging PRs
	- Install (with local `pip` from within `conda` environment): `pip install hathitrust-api`

Use `conda` environment `htrc`.


## Project Steps (2019)

### Generate Volume ID List

For 6/25/19 meeting, I need to present a list of HT volume IDs. "Education" is a decent subject heading--so is "History," which captures the Parley books--but many volumes (especially periodicals) lack any subject keywords.

There are many more comparative research questions (across formats and languages) that can be asked with a full sample. For 1800-1850, there are ~288,766 volumes. Since we are interested in serials and encyclopedias and similar printed formats, we would only want to exclude a few formats such as "Manuscript" and "CDROM." However, a more generalized way to do this is just to ignore volumes that do not contain a page sequence object.

**Warning!**

The 1800-1850 list can be generated ONLY by parsing the HathiFile (~1GB). This is because the Solr search API is completely deprecated--Hathi has made this clear! I wrote code to work with the HathiFile in `classify-image-junk` in the `src/sample.py` file.

Within this directory, run:

`python ids_by_date.py <START_DATE> <END_DATE> [<START-END.csv>]`

N.B. in my notebooks for the Yale DH Lab workshop the recommended way was using online HT search to generate JSON Collection file.

Boris requests (8/23):

Python script (+ requirements.txt) that efficiently does inference on ~100 CSV rows. He will take care of the parallelism on the HPC.

Script should have --input flag (argparse) for CSV input and --output flag for a directory where we can write the list of filtered rows.


### Acquire Sample Pages

For 7/23/19 meeting, I sampled and then generated mapping of sample volumes to IMAGE_ON_PAGE candidates.

In

### HTRC Capsule

Login: `stephenkrewson` (password saved with Chrome)
Email: `stephen.krewson@yale.edu`

http://www.loc.gov/standards/mets/




# Deprecated

## Project Structure (2016)

N.B. this is not actively maintained.

file 	| purpose | note
--- 	| --- 		| ---
`books.txt` | list of books to download | one unique HT ID per line; generated by `ht_search_volumes.py`
`config.py` | stores HT API keys | not versioned, you'll need to get your own keys
`ht_download_images.py` | downloads all image pages for each book in `books.txt` | if a folder already exists with the name of an ID it is skipped; IDs that contain colons are skipped
`ht_search_volumes.py` | concatenates IDs returned from a bibliographic search onto `books.txt` | syntax for providing search fields (author, date, etc.) is given in a usage comment in the code
`ht_run_extraction.sh` | creates the `extracted` subfolder within all volume directories | skips volume if `extracted` already exists
`ht_classify_score.py` | from `extracted` subfolder, generates a corresponding Numpy array for each image in `vectors` sibling folder | adaptation of Inception modeal (2015)

