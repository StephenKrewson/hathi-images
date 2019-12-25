# A Half-Century of Illustrated Pages: ACS Lab Notes

We've reached the mid-point of my [Advanced Collaborative Support project](https://www.hathitrust.org/hathitrust-research-center-awards-five-acs-projects), "Deriving Basic Illustration Metadata." Many thanks to Ryan Dubnicek and Eleanor Dickson Koehl for coordinating the project and to Boris Capitanu for his always-stellar technical support.

Right now, sitting on a supercomputer named Big Red at the University of Indiana, is a rather remarkable dataset: *every illustrated page from every Google-scanned volume in the HathiTrust Digital Library (HT) for the period 1800-1849*. Although the image processing pipeline we are using is by no means new, the ability to work so comprehensively is. Furthermore, the working hypothesis of this kind of "historical illustration" study is that graphic elements in printed objects exhibit technical and stylistic similarity over time, but this development is *uneven*. That is to say, illustrations "change with the times" (i.e. the emergence of techniques like lithography will both exert a pressure on both publishers and artists) but reuse and copying of "older" styles is common.  

To evaluate such hypotheses, the best option is definitely to look at everything possible for a significant but tractable slice of time. Only with a comprehensive imageset can we cluster in a way that might tell us something about this "unevenness." A 50-year sample pushes up against the limits of what can be stored on disk for a project; but it is doable. It also may better reflect the inherent cycles of technological change (Kondratiev? although this begs the question of whether 1800 is such a point for image technology; I think it is).   

Here's a by-the-numbers breakdown:

- There were **500,013** qualifying volumes (as of September 2019) in HT for the first half of the nineteenth century. To come up with this list of unique volume ids, I filtered the latest [HathiFile](https://www.hathitrust.org/hathifiles) by date range (`1800-1849`), media type, (`text`) and scanning institution (`google`). 
  - This was a tricky but fun exercise since the HathiFiles are roughly a Gigabyte in size--far too large to read into memory with a Pandas method like `.read_csv()`. Reading the file in chunks is the way to go (it still takes ~15 min on my i7 laptop).
  - The vast majority of volumes for this period have been scanned by Google; we opted for this restriction because Google-scanned books come with some extra metadata that is useful for identifying illustrated pages.
- After the first processing stage, which uses a retrained neural network to estimate if candidate pages are illustrated or not, the set of volumes was winnowed down to **183,553**. This means that, according to the model, roughly (183,553 / 500,013 * 100)  = **37%** of early-nineteenth century books contain one or more illustrated pages. This certainly seems plausible; although I would like to check it against relevant bibliographic studies of 19C publishing.
  - The results of stage one were summarized in a 228 Mb JSONL file by Boris. Each line of the file is a JSON object corresponding to a volume. One of the fields 
- Of this set of probably-illustrated volumes, there were 1,999,999 individual pages estimated by my model to feature illustrations.

This post sketches our basic data pipeline, highlighting a few decisions that are especially important for large-scale image processing.

The main takeaways from the first phase of "Deriving Basic Illustration Metadata" are:

1. Use GCP and commodity stuff!
2. Image processing needs to be done in batch, in parallel
3. Postpone conversion/reorganization as long as possible

Code can be found at:

https://github.com/htrc/ACS-krewson

## Pipeline

Link to BioDiversity Library (and their implementation)

Things worth going into a bit more detail on:

- Pairtree
- Parallelism
- fast.ai
- JP2 conversion

Here's an image, courtesy of Damon Crockett's ivyp:

![533 illustrated pages extracted in phase one.](img/phase1_montage_533.png)

## Discussion

## Next Steps

- Bounding boxes (test?)
- "Fingerprinting"
- Clustering
- Interpretation

## HTRC Update Post Examples

*from Ryan:*

As requested and only (!) a couple of weeks late, here are links to some example blog posts from a group from our last ACS round:

- https://newreadia.wordpress.com/2018/10/10/extracting-and-organizing-htrc-corpora-tool-and-walkthrough/
  - Presents "Program Era Project" extractor tool that tries to get ISBN and other metadata and puts it into JSON form (from zipped pairtree)
- https://dsps.lib.uiowa.edu/programera/2018/02/09/breaking-down-the-htrc-data-capsule/
  - Basic graphs on (multi)authorship for Iowa Workshop study; basic "data profile" and plan for further text analysis
- https://dsps.lib.uiowa.edu/programera/2017/11/20/collaborating-with-hathitrust/
  - In-depth drive of StyleCard and LitMap (data shown in plot.ly)

You’ll see that the focus of the posts varies, as does the length and the depth to which results are discussed. Whatever makes sense for the progress of your project will almost certainly work for us, but let me know if you have any questions or if you wanted to share a draft in advance, even. Sharing a draft is definitely not required, though.