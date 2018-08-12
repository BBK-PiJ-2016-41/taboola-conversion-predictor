import pandas as pd
import numpy as np
import re

class AdExtractor:

    def __init__(self, dataframe):
        """
        Constructor for AdExtractor.
        :param dataframe: A dataframe of two columns containing the ad_id and headline_text
        """
        self.df = dataframe

    def num_dynamic_params(self):
        return_df = self.df
        return_df['num_params'] = return_df['headline_text'].apply(lambda row: len(re.findall(r'\${', row)))
        return return_df

    def num_punc_marks(self):
        TODO

    def run_all(self):
        TODO