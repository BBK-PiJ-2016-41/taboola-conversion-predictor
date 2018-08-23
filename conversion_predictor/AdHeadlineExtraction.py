import re


class AdExtractor:
    def __init__(self, data_frame):
        """
        Constructor for AdExtractor.
        :param data_frame: A data_frame of two columns containing the ad_id and headline_text
        :raise KeyError: if expected columns (ad_id, headline_text) are not present
        :raise ValueError: if headline_text is not a text object
        Also sets a regex for punctuation for use in punctuation method.
        """

        try:
            if data_frame['headline_text'].dtype != 'object':
                raise ValueError('Headline text not expected data type - please use text object')
        except KeyError:
            raise
        except ValueError:
            raise

        self.df = data_frame
        self.punctuation = r'[,?!.:;&]'

    def num_dynamic_params(self):
        """
        Calculates the number of dynamic parameters in the ad headline text.
        :return: a dataframe containing the ad_id and number of dynamic parameters contained in the text, without
        the headline_text column
        """
        return_df = self.df.copy()
        return_df['num_params'] = return_df['headline_text'].apply(lambda row: len(re.findall(r'\${', row)))
        return return_df.drop('headline_text', axis=1)

    def num_punc_marks(self):
        """
        Calculates the number of punctuation marks in the ad headline text.
        :return: a dataframe containing the ad_id and number of punctuation marks contained in the text, without
        the headline_text column
        """
        return_df = self.df.copy()
        return_df['num_puncs'] = return_df['headline_text'].apply(lambda row: len(re.findall(self.punctuation, row)))
        return return_df.drop('headline_text', axis=1)

    def run_all(self):
        """
        Runs both the punctuation and parameter methods in a single call.
        :return: a dataframe containing the ad_id and, number of dynamic parameters and number of punctuation marks
        contained in the text, without the headline_text column
        """
        return self.num_dynamic_params().join(self.num_punc_marks())
