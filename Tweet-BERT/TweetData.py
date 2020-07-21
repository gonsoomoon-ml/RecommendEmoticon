import pandas as pd
import pickle
import re
import boto3
import numpy as np
import os


class TweetData(object):
    # Desc: Load tweet input data
    def __init__(self, tweets):
        self.file_name = 'data/emojis.csv'
        self.tweets = tweets
        self.emoji_to_idx = {}
        self.emoji_file_name = "emoji_to_idx.pickle"
        self.save_dir = 'data'
                
    
    def make_sentimet_label(self):
        # Desc: make dictionary of {emoticon:label}
        emojis = list(sorted(set(self.tweets['sentiment'])))
        self.emoji_to_idx = {em: idx for idx, em in enumerate(emojis)}
        self.save_emoji_data()
#        print(self.emoji_to_idx)

    def set_sentimet_label(self, emoji_to_idx):
        # Desc: make dictionary of {emoticon:label}
        self.emoji_to_idx = emoji_to_idx
        print("emoji_to_idx is set")


    def save_emoji_data(self):
        # Desc : save emoji_to_idx as pickle file
        save_path = os.path.join(self.save_dir, self.emoji_file_name)    
        
        with open(save_path, 'wb') as handle:
            pickle.dump(self.emoji_to_idx, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("{} is saved".format(save_path))


    def load_emoji_data(self):
        save_path = os.path.join(self.save_dir, self.emoji_file_name)    
        
        with open(save_path, 'rb') as handle:
            emoji_to_idx = pickle.load(handle)    
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


    def normalize_text(self, s):
        # Desc: retrun cleaned text
        s = s.lower()

        # remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
        s = re.sub('\s\W',' ',s)
        s = re.sub('\W\s',' ',s)

        # make sure we didn't introduce any double spaces
        s = re.sub('\s+',' ',s)

        return s
    
    def make_texts_lables(self):
        #remove punctuations and double spaces
        texts = [self.normalize_text(s) for s in self.tweets['content']]
        #convert category to a number
        labels = [self.get_emo_label_id(l) for l in self.tweets['sentiment']]

        return texts, labels
    
    def split_train_test_data(self, texts, labels, train_test_ratio):
        # Desc: Split data into train and test

        total_num_records = len(texts)
        num_train_records = int(total_num_records * train_test_ratio)
        #print(num_train_records)
        train_text = texts[0:num_train_records]
        test_text = texts[num_train_records:total_num_records]

        train_label = labels[0:num_train_records]
        test_label = labels[num_train_records:total_num_records]


        return  train_text, train_label, test_text, test_label
    
    def save_input_data(self, save_dir, file_name, data):
        save_path = os.path.join(save_dir, file_name)    

        if isinstance(data, np.ndarray):
            np.save(save_path, data)
        else:
            data_df = pd.DataFrame(data)
            data_df.to_csv(save_path, index=False)

        print("{} is saved".format(save_path))


    def load_input_data(self, save_dir, file_name):
        save_path = os.path.join(save_dir, file_name)
        data = pd.read_csv(save_path)
        print("{} is loaded".format(save_path))

        return data
