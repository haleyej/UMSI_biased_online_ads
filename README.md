# UMSI Capstone Project: Biased Online Ads
Noah Chazonoff, Brandon Huggard, Haley Johnson, Dani Lazarus, and Nicole Savitsky

The model weights and the extracted ad segments are too large to host to Github (>50MB), please see Google Drive links
* <a href = "https://drive.google.com/file/d/1Z7ZsmYvKICdjNg5ye6Jv11LeiFFsebZP/view?usp=share_link">final weights</a>
* <a href = "https://drive.google.com/file/d/1bg4chDVzaXWazBcjy7TLG5qrDZ5m6bWu/view?usp=share_link">data (raw images, predicted masks, extracted ads)</a>

## Ad Identification 
In our model, ads are identified in three steps. First, the ad is passed through an <a href = "https://paperswithcode.com/method/efficientnet">efficientnet model,</a> which generates a semantic segmentation mask. This mask indicates what part of the image is an advertisement (foreground) and what is just website content (background). This segmentatiion mask is extract the ad from the rest of the image. Then, the extracted ads are passed into an optical character recognition model, that identifies what words appear in the ad.  

## Contents
This repository contains all the code and files we used to complete our capstone project, as well as sample outputs. 

In particular, the files in the code directory do the following:
* sample_users: directory with code we used to sample ads from full dataset for annotations 
* segment_model.ipynb: code to train, fine-tune and plot results from efficientnet model
* get_predicted_masks.py: code to get ads from an original image using the predicted semantic segmentation masks, duplicates some functionality in segment_model.ipynb for ease of use 
* extract_ads.ipynb: notebook to develop / test code to extract ads from an image, using the segmentation masks generated by the efficientnet model
* extract_ads.py: functionality of extract_ads.ipynb in a .py file, for ease of use
* optical_character_recongition.ipynb: code to extract contents from ads using optical character recongition 

The plots directory contains:
* model training history, showing the test / validation loss and accuracy each epoch
* receiver operating characteristic curve (roc) for model

Both plots are generated by code in segment_model.ipynb

## Resources Used
* <a href = "https://github.com/qubvel/segmentation_models">segmentation models package</a>
* <a href = "https://towardsdatascience.com/metrics-to-evaluate-your-semantic-segmentation-model-6bcb99639aa2">metrics to evaluate your semantic segmentation model (info on dice coefficeint</a>
* <a href = "https://medium.com/swlh/focal-loss-what-why-and-how-df6735f26616">binary focal loss explained</a>
