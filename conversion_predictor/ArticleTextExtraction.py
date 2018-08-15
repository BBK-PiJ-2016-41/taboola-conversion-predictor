import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from urllib import parse


class UrlTransformer:

    def __init__(self, data_frame):
        try:
            if data_frame['url'].dtype != 'object':
                raise ValueError('URL not expected data type - please use text object')
            if 'ad_id' not in data_frame.columns.values:
                raise KeyError('Ad ID not found')
            self.df = data_frame.reset_index()
        except KeyError:
            raise
        except ValueError:
            raise

    def extract_html(self):
        return_df = self.df.copy()
        return_df['html'] = return_df['url'].apply(lambda row: requests.get(row, allow_redirects=False).text)
        return return_df.drop('url', axis=1)

    def extract_domains(self):
        df_copy = self.trim_domains()
        gle = LabelEncoder()
        labels = gle.fit_transform(df_copy['domain'])
        df_copy['domain_label'] = labels
        ohe = OneHotEncoder()
        feature_array = ohe.fit_transform(df_copy[['domain_label']]).toarray()
        feature_labels = list(gle.classes_)
        features_final = pd.DataFrame(feature_array, columns=feature_labels)
        combined = pd.merge(df_copy, features_final, left_index=True, right_index=True)
        combined.set_index('ad_id')
        return combined.drop('domain_label', axis=1)

    def trim_domains(self):
        df_copy = self.df.copy()
        df_copy['domain'] = df_copy['url'].apply(lambda row: parse.urlparse(row).netloc.split('.')[1])
        return df_copy.drop('url', axis=1)


class HtmlTransformer:

    def __init__(self, df):
        self.html = df

    def extract_text(self):
        TODO

    def extract_clickouts(self):
        TODO

    def extract_num_paras(self):
        TODO

    def extract_words_para(self):
        TODO

    def extract_words_sentence(self):
        TODO

    def extract_total_words(self):
        TODO

    def extract_num_numbers(self):
        TODO

    def extract_syllables_word(self):
        TODO

    def extract_all(self):
        TODO


class TextProcessor:


    def __init__(self, txt):
        self.text = txt

    def lemmatize(self):
        TODO

    def remove_stop_words(self):
        TODO

    def tf_idf(self):
        TODO

    def cosine_similarity(self):
        TODO

    def pos_tagger(self):
        TODO

    def extract_all(self):
        TODO