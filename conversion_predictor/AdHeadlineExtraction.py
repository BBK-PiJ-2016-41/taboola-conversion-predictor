import pandas as pd
import numpy as np
import re


class AdExtractor:
    def __init__(self, data_frame):
        """
        Constructor for AdExtractor.
        :param data_frame: A data_frame of two columns containing the ad_id and headline_text
        """
        try:
            self.df = data_frame.set_index('ad_id')
        except KeyError:
            raise

        self.punctuation = r'[,?!.:;&]'

    def num_dynamic_params(self):
        return_df = self.df.copy()
        return_df['num_params'] = return_df['headline_text'].apply(lambda row: len(re.findall(r'\${', row)))
        return return_df.drop('headline_text', axis=1)

    def num_punc_marks(self):
        return_df = self.df.copy()
        return_df['num_puncs'] = return_df['headline_text'].apply(lambda row: len(re.findall(self.punctuation, row)))
        return return_df.drop('headline_text', axis=1)

    def run_all(self):
        return self.num_dynamic_params().join(self.num_punc_marks(), on='ad_id')
