# UMSI Capstone Project: Biased Online Ads
Noah Chazonoff, Brandon Huggard, Haley Johnson, Dani Lazarus, and Nicole Savitsky

Weights and extracted segments are too large to upload to Github, please see Google Drive links
* <a href = "https://drive.google.com/file/d/1Z7ZsmYvKICdjNg5ye6Jv11LeiFFsebZP/view?usp=share_link">final weights</a>
* <a href = "https://drive.google.com/file/d/1bg4chDVzaXWazBcjy7TLG5qrDZ5m6bWu/view?usp=share_link">data (raw images, predicted masks, extracted ads)</a>

## Contents
This repository contains all the code and finals we used to complete our capstone project

## Ad Identification 
In our model, ads are identified in three steps. First, the ad is passed through an <a href = "https://paperswithcode.com/method/efficientnet">efficientnet model,</a> which generates a semantic segmentation mask. This mask indicates what part of the image is an advertisement (foreground) and what is just website content (background). This segmentatiion mask is extract the ad from the rest of the image. Then, the extracted ads are passed into an optical character recognition model, that identifies what words appear in the ad.  
