import os
import re
import tensorflow as tf
import pandas as pd
import matplotlib.pyplt as plt


def save_masks(arrays, img_list, model, mask_save_path = "../Data/predicted_masks", shape = SHAPE):
    '''
    Takes in a list of image arrays, gets 
    predicted mask and saves them
    
    ARGS:
        arrays = list of arrays to get masks for 
        img_list = list or Pandas series with the file 
                   names of the original image 
        mask_save_path = path to save segmentation masks to
        shape = shape of segmenation masks
        
    RETURNS:
        Returns none, saves masks to mask_save_path 
        directory
    '''
    user_num_regex = r'\d{5}'
    site_num_regex = r'(\d{1,2}).png'

    for i in range(len(arrays)):
        pred = model.predict(tf.expand_dims(arrays[i], 0))
        pred = pred.reshape(shape[0], shape[1])
        
        if type(img_list) == list:
            img = img_list[i]
        elif type(img_list) == pd.core.series.Series:
            img = img_list.iloc[i]
        
        user_num = re.findall(user_num_regex, img)[0]
        site_num = re.findall(site_num_regex, img)[0]
        
        plt.imsave(os.path.join(mask_save_path, f"user_{user_num}_{site_num}.png"), pred, cmap = 'Greys')


def load_model(weights, weights_path = ''):
    '''
    Helper function to load in model 

    ARGS:
        weights = file with model weights
        path = optional, path to model weights if its not in 
               same direction 

    RETURNS:
        tensorflow model with weights
    '''
    return model.load_weights(os.path.join(weights_path, weights)).expect_partial()


if __name__ == "__main__'':
    arrays = sys.argv[1]
    img_list = sys.argv[2]
    mask_save_path = sys.argv[3]
    shape = sys.argv[4]
    weights = sys.argv[5]
    weights_path = sys.argv[6]

    model = load_model(weights, weights_path)
    save_masks(array, img_list, model, mask_save_path, shape)
