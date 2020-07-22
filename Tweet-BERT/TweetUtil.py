import pandas as pd
import pickle
import re
import boto3
import numpy as np
import os


class TweetUtil(object):
    # Desc: Load tweet input data
    def __init__(self):
        self.emoji_to_idx = {}
        self.save_dir = 'data'        

    def load_emoji_data(self, emoji_dict_path):
        save_path = os.path.join(self.save_dir, emoji_dict_path)           
        with open(save_path, 'rb') as handle:
            emoji_to_idx = pickle.load(handle)  
            
        self.emoji_to_idx = emoji_to_idx   
        print("emoji_to_idx is loaded")    
        return emoji_to_idx


    def get_emoji_to_idx(self):
        return self.emoji_to_idx 
        
        
    def get_emo_label_id(self, category):
        # Desc: return label based on emoticon
        return self.emoji_to_idx[category]

    def get_emo_class_label(self, prediction):
        # Desc: return emoticon based on label
        for key, value in self.emoji_to_idx.items():
            if value == prediction:
                return key
