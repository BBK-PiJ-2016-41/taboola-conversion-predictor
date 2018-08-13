import re

class UrlTransformer:


    def __init__(self, df):
        self.dataframe = df

    def extract_html(self):
        TODO

    def extract_domains(self):
        TODO


class HtmlTransformer:


    def __init__(self, df):
        self.html = df

    def extract_text(self):
        TODO

    def extract_clickouts(self):
        TODO

    def extract_num_paras(self):
        TODO

    def extract_words_paras(self):
        TODO

    def extract_words_sentence(self):
        TODO

    def extract_total_words(self):
        TODO

    def extract_num_numbers(self):
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
