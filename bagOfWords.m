% First test of bag of words with Parley dataset
% Stephen Krewson, 11/19/2017
% https://www.mathworks.com/help/vision/ug/image-classification-with-bag-of-visual-words.html

% platform-independent absolute path to the dataset
% this script should only be run from the directory containing it AND the
% dataset

function main()

addpath(genpath(pwd))

setDir = fullfile(pwd,'train5');

% convention is folders are the labels (five year windows for pub date)
imds = imageDatastore(setDir,'IncludeSubfolders',true,'LabelSource','foldernames');

% 70% validate and 30% test; grayscale JPG and PNG images both present
[trainingSet,testSet] = splitEachLabel(imds,0.3,'randomize');

% might as well try this on the cluster; wrap into main() function
bag = bagOfFeatures(trainingSet);

size(bag)
fprintf("All done!\n");
