import pandas as pd
import numpy as np 
import os 
import matplotlib.pyplot as plt
import cv2
import sys


def extract_ads(target, image_path = IMAGE_PATH, mask_path = MASK_PATH, save_path = SAVE_PATH, shape = SHAPE, pad = 1):
    '''
    Function to extract the location of ad(s) from a segmentation mask
    and then crop the original image to just the ad(s)
    
    ARGS:
        target = file name of the mask / image 
                (they have the same names for matching, just stored in 
                 different directories)
        image_path = path to the directory with the screenshots / image data
        mask_path = path to the directory with the segmentation masks
        save_path = path to save the extracted ads to 
        shape = shape of all the data
        
    RETURNS:
        Returns none, saves extracted ads to save_path directory
        
    '''
    
    if target not in os.listdir(image_path): 
        print(target)
        return None
    
    img = cv2.imread(os.path.join(MASK_PATH, target))
    actual = cv2.resize(cv2.imread(os.path.join(IMAGE_PATH, target)), shape)
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 9)
    
    contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    
    for c in contours:
        cv2.drawContours(threshold, [c], -1, (255,255,255), -1)
       
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations = 4)
    contours = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    
    for i in range(len(contours)):
        c = contours[i]
        x, y, w, h = cv2.boundingRect(c)
        if pad > 0:
            x, y, w, h = (x + pad), (y + pad), (w + pad), (h + pad)
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 3)
        cropped_image = actual[y:y + h, x:x + w]
        
        user_info = target.split(".")[0]
        name = f"{user_info}_ad_{i + 1}.png"
        
        cv2.imwrite(os.path.join(save_path, name), cropped_image)


if __name__ == "__main__":
    IMAGE_PATH = sys.argv[1]
    MASK_PATH = sys.argv[2]
    SAVE_PATH = sys.argv[3]
    SHAPE = sys.argv[4]

    mask_files = os.listdir(MASK_PATH)

    for mask in mask_files:
        extract_ads(mask)