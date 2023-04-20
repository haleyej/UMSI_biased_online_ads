import os
import pandas as pd
import numpy as np 
import re
import ast 

'''
Creates site look up table 
+ table of users to be sampled
'''

def create_site_look_up(user_id):
    '''
    Turns the commands file into a list of websites 
    that the simulated user visited and the associated
    suffixes in the image file names.
    
    Naming convention works whether you use the 
    screenshot parts or the full image that has 
    been stitched together from the parts.
    
    Args:
        user_id (str): Used to identify the correct commands file.
        
    Returns:
        pandas.DataFrame: DataFrame containing the suffix and corresponding site for each simulated user.
    '''
    commands = pd.read_csv(f"example_folder/users/{user_id}/screenshot_0/commands_u{user_id[5:]}_s0.tsv", sep = "\t", header = None, index_col = 0).reset_index(drop = True)
    commands.columns = ['action', 'site']
    commands['site'] = commands.site.apply(ast.literal_eval)
    
    suffix_to_site = {}
    for idx, _ in commands.groupby(commands.index // 2):
        if commands.iloc[idx * 2]['action'] == 'GET' and commands.iloc[idx * 2 + 1]['action'] == 'FULL SCREENSHOT':
            site = commands.iloc[idx * 2]['site']['url']
            suffix = commands.iloc[idx * 2 + 1]['site']['suffix'][1:]
            suffix_to_site[suffix] = site
            
    site_look_up = pd.DataFrame.from_dict(suffix_to_site, orient = 'index').reset_index()
    site_look_up.columns = ['suffix', 'site']
    
    return site_look_up

def block_randomization(user_summary, sites, n):
    '''
    Combines user summary with the sites table 
    to get all possible combinations of 
    group/site pairs.
    
    Performs block randomization on group/site combinations, 
    to get n examples from each.
    
    Returns a dataframe with the info about the sampled 
    simulated users.
    
    Args:
        user_summary (pandas.DataFrame): DataFrame containing user summary information.
        
        sites (pandas.DataFrame): DataFrame containing suffix and corresponding site for each simulated user.
        
        n (int): Number of examples to sample from each group/site combination.
    
    Returns:
        pandas.DataFrame: DataFrame containing the sampled user information.
    '''
    users_df = user_summary.copy()
    users_df.user_id = users_df.user_id.apply(lambda s: f'user_{s}')
    users_df['key'] = 1
    users_df = users_df[['user_id', 'group', 'key']].values
    users_df = pd.DataFrame(users_df)
    users_df.columns = ['user', 'group', 'key']
    
    sites['key'] = 1
    
    all_sites = users_df.merge(sites, on = 'key', how = 'outer')
    all_sites = all_sites.drop(columns = 'key')
    
    sample_df = all_sites.groupby(['suffix', 'group']).sample(n, random_state = 42)
    
    return sample_df
    

if __name__ == "__main__":
    user_summary = sys.argv[1]
    sites = sys.argv[2]
    sample_files_path = sys.argv[3]

    sample = block_randomization(user_summary, sites, 4)
    sample.to_csv(os.path.join("sampled_users.csv"), index = False)
