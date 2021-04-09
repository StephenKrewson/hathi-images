# HTRC ACS project

My project "Generating Basic Illustration Metadata" ran from May 2019 to August 2020. I presented some examples from the work, using PixPlot, during HathiTrust's Community Week in October 2020.

Deliverables:

- ACS [mid-year report](https://wiki.htrc.illinois.edu/display/COM/A+Half-Century+of+Illustrated+Pages%3A+ACS+Lab+Notes)
- ACS [final reports](https://wiki.htrc.illinois.edu/display/COM/Advanced+Collaborative+Support+%29ACS%29+Awards); my [pdf](https://wiki.htrc.illinois.edu/download/attachments/31588360/ACS-2019-2020-FinalReport-HathiTrust%2BNames.pdf?version=1&modificationDate=1595948576000&api=v2)
- Project [Zenodo repository](https://zenodo.org/record/3940528)
- Community Week slides: `reports-presentations/ACS_2020-HT-Community-Week`
- Complete 1800-1850 [image dataset](https://console.cloud.google.com/storage/browser/hathitrust-full_1800-50) on Google Cloud Storage

## Google Cloud VM and cloud storage

After my HT talk, I deleted by VM to save money on billing. The cloud storage costs about $6 per month, which is very reasonable. To view my current Google Cloud projects, run:

```
gcloud config list
```

Once I provision the project with a VM, I can login in with either long or short form:

```
gcloud beta compute ssh --zone us-west1b --project global-matrix-245215 fastai20
gcloud beta compute ssh fastai20
```

The user "jupyter" should be used for accessing fast.ai's Jupyter Notebooks.

The location of the data is:

```
https://console.cloud.google.com/storage/browser/hathitrust-full_1800-50
```

Here's a basic checklist for spinning up a new VM:

- Make sure the gcloud SDK is up to date: https://cloud.google.com/sdk/docs/quickstart. I had some trouble with expired keys. Make sure `apt-get update` runs fine.
- Follow the fastai steps to create a GPU-enabled VM: https://course.fast.ai/start_gcp. This worked for me in the past, so why mess with it.



## Python setup

As of April 2021, I am using Python 3.8 with pip 20.0.2 on WSL2, Ubuntu 20.0.4. This gives me the closest match with my Linux VM and is extremely fast. The dependencies are simple: I need jupyter and pandas for working in the query notebook. I install these packages within a virtual environment.

Like `pip`, the `venv` module is [installed already](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) with Python 3. Just use the conventional name `env` since, unlike conda, the virtual environment is located in your project's directory.

```
python3 -m venv env
source env/bin/activate
which python3
python3 -m pip install <libraries>
deactivate
```

Make sure env/* is in the .gitignore.


## Dissertation goals (2021)

- [ ] Identify case study involving Peter Parley. This might involve illustration reuse or data on how the Parley character was visually represented. Don't proceed until you have a good sense of the goal.
- [ ] Decide on query and collect volumes. It's likely easier to get the data from within a Google VM. Move to VM before running the [PixPlot](https://github.com/YaleDHLab/pix-plot) analysis job. Note that the searching can be done on a flat file using a Jupyter notebook locally. (right??) Take notes on how to do this and put them in this README.
- [ ] Create VM with standard GPU and generate PixPlot. Use pip and follow PixPlot dependencies exactly. Take notes so that I remember what I've done.
- [ ] Analyze PixPlot graph (should be less than 5k images) and create one or two montages as well as a selection of detailed figures. Add to dissertation project.
- [ ] Write a quick DH methods section and figure out the progression of evidence and ideas in the chapter.
- [ ] Get feedback and revise or submit, depending on the time.

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

## Additional image processing resources

Check the `_datasets` and `_image-labeling` folders on my computer for additional resources, such as `ivpy` montage tool.
