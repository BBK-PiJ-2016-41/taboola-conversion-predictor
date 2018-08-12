import pandas as pd
import numpy as np
import re


class AdExtractor:
    def __init__(self, data_frame):
        """
        Constructor for AdExtractor.
        :param data_frame: A data_frame of two columns containing the ad_id and headline_text
        """
        self.df = data_frame
        self.punctuation = r'[,?!.:;&]'

    def num_dynamic_params(self):
        return_df = self.df
        return_df['num_params'] = return_df['headline_text'].apply(lambda row: len(re.findall(r'\${', row)))
        return return_df

    def num_punc_marks(self):
        return_df = self.df
        return_df['num_puncs'] = return_df['headline_text'].apply(lambda row: len(re.findall(self.punctuation, row)))
        return return_df

    def run_all(self):
        TODO
