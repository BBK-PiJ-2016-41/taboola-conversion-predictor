import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from urllib import parse
from bs4 import BeautifulSoup
import re


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

    def __init__(self, data_frame):
        try:
            if data_frame['html'].dtype != 'object':
                raise ValueError('HTML not expected data type - please use text object')
            self.df = data_frame.set_index('ad_id')
        except KeyError:
            raise
        except ValueError:
            raise

        self.extract_text()

    def extract_text(self):
        self.df['text'] = self.df['html'].apply(lambda row: self.cleanup(row))

    def beautiful_soup(self, html_snippet):
        return BeautifulSoup(html_snippet, 'html.parser')

    def cleanup(self, html_snippet):
        soup = self.beautiful_soup(html_snippet)
        for script in soup(['script', 'style']):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def extract_clickouts(self):
        TODO

    def extract_num_paras(self):
        self.df['num_paras'] = self.df['html'].apply(lambda row: len(self.beautiful_soup(row).find_all('p')))
        return self.df[['num_paras']]

    def extract_words_para(self):
        if 'num_words' not in self.df.columns.values:
            self.extract_total_words()
        if 'num_paras' not in self.df.columns.values:
            self.extract_num_paras()
        self.df['words_para'] = round(self.df.num_words / self.df.num_paras, 4)
        return self.df[['words_para']]

    def extract_words_sentence(self):
        if 'num_words' not in self.df.columns.values:
            self.extract_total_words()
        if 'num_sentences' not in self.df.columns.values:
            self.extract_num_sentences()
        self.df['words_sentence'] = round(self.df.num_words / self.df.num_sentences, 4)
        return self.df[['words_sentence']]

    def extract_num_sentences(self):
        self.df['num_sentences'] = self.df['text'].apply(lambda row: len(re.split(r'[.!?]+', row)))
        return self.df[['num_sentences']]

    def extract_total_words(self):
        self.df['num_words'] = self.df['text'].apply(lambda row: len(re.findall(r'\w+', row)))
        return self.df[['num_words']]

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