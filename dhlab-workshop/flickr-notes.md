Bookplates AND writing/signatures/marginalia as one class
REASON: human identifying marks (key to have bookplate of a person for NER)
ignore bookplates just from main institution
needs to be more specific

Justification: deep methods and ignoring heuristics justified for extra information about provenance and for genre distinctions as byproduct

TODO: build gallery of most challenging examples from each class

approach 1: full page classification + OpenCV bottom up for *known* images
Pros: for margnialia etc. it doesn't really make sense to get per-pixel annotation
Cons: OTOH, would be nice at least to have a region

approach 2: bounding box annotated dataset to get segmentation masks
Question: what about skewing? 

TODO: why do all hathi books from UC libraries not download via the API?
TODO: don't download PNG files! keep res full but do JPEG


need to nail down what it means to have big border; how to deal with mixed genre/format

combine strong border with tabular? tempting...

mitigating point: errors between classes I don't care about are cheap
that is, if it's junk vs. strong table, who cares. I just want accurate
on images and music and bookplates, etc.

Building the database: select from ECCO, HT, IA, and MHL: beginning of print to 1920: 2k per class, bounding box annotations

same 10-ish classes?

collaborate with woman at LOC on political cartoon extraction?

GO TO OFFICE HOURS
ask Peter for advice on publishing


TODO: verse vs. epigraph?? separate classifier yes/no for marginalia?


Notes from Art and Melissa Meeting, 4/9

Flickr --> organize

Question: is eliminating "sections" or partial bounding boxes always bad?

Example with nose:

http://coreygoldberg.blogspot.com/2017/02/batch-convert-images-from-png-to-jpeg.html

https://bitbucket.org/aawinder/


IDEA: only download ABBYY/Google's noisy estimate of illustration pages

WRINKLE: don't use heuristics about sequence location; since interested in bookplates (for MHL) and in making this purely pixel based.

IDEA: deep learning on *full page images* can take advantage of structural information in the way illustrations and scan errors occur.

cost: 0.6 s per image...fairly high

Given ~10 classes of errors, only need to do segmentation on some of them. And can toss all the junk right away. 

QUESTION: does Michael's segmenter work OK when there are images? What about skew correction etc. Maybe use Amy Winder's stuff?


TODO:

tensorflow confusion matrices,
package up model into notebook
    AND: if class is correct, save the bottleneck (AFTER bounding box?)
    THEN: can do nearest neighbors
email Bamman when notebook ready
ask Jaimie/DB/DD about sampling
reasonable numbers / time periods

follow up HT email since they haven't responded
follow up with Tom since he hasn't responded

MAKE MHL flowchart
Keep track of how many times Leetaru's heuristics would have failed??



Art expands by 150 pixels, uses double page

Going to run through Peter Leonard's PixPlot (users can circle clusters of images) IN A SPRINT RIGHT NOW (talk to Doug)

Figure out Flickr ID reuse

(get away from Flickr?)



Divide into albums

Good

Bookplates
Signatures
Marginalia (but not alot)


In Between

Decorative endpapers (marble swirls)
Tables



Bad (group)

Blank pages
Endpapers
Covers




Can I see Amy's code:

Student workers on M/W/F



Amy Winder

bitbucket.org/aawinder/



time of essence for student workers
aiming to have a workflow for Friday

just have them 

FedEx Confirmation #

97936318