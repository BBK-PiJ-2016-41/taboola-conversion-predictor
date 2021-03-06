import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from urllib import parse
from bs4 import BeautifulSoup
import re
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk


class UrlTransformer:

    def __init__(self, data_frame):
        """
        Constructor for URL Transformer.
        :param a dataframe containing the ad id and URL
        :except Value Error if URL is not present/not expected data type
        :except Key Error if ad id is not present
        """
        try:
            if data_frame['url'].dtype != 'object':
                raise ValueError('URL not expected data type - please use text object')
            self.df = data_frame
        except KeyError:
            raise
        except ValueError:
            raise

        self.memo = {}

    def extract_html(self):
        """
        Extracts the html from the url provided.
        :return: A dataframe containing ad id and html
        """
        return_df = self.df.copy()
        return_df['html'] = return_df['url'].apply(lambda row: self.get_html(row))
        return return_df.drop('url', axis=1)

    def get_html(self, url):
        """
        Checks to see if the URL has been visited by the program before by checking the memo object. If it hasn't,
        visits the URL to extract HTML.
        :param url:
        :return: the HTML from the webpage.
        """
        if url in self.memo:
            html = self.memo[url]
        else:
            html = requests.get(url, allow_redirects=False).text
            self.memo[url] = html
        return html

    def extract_domains(self):
        """
        Creates a category for each domain in the dataframe using One Hot Encoder
        :return: a dataframe containing ad id and categorical representations of each domain
        """
        df_copy = self.trim_domains().copy().reset_index()
        gle = LabelEncoder()
        labels = gle.fit_transform(df_copy['domain'])
        df_copy['domain_label'] = labels
        ohe = OneHotEncoder()
        feature_array = ohe.fit_transform(df_copy[['domain_label']]).toarray()
        feature_labels = list(gle.classes_)
        features_final = pd.DataFrame(feature_array, columns=feature_labels)
        combined = pd.merge(df_copy, features_final, left_index=True, right_index=True)
        combined.set_index('ad_id', inplace=True)
        return combined.drop('domain_label', axis=1)

    def trim_domains(self):
        """
        Extracts the domains from the urls
        :return: a dataframe containing ad id and the domain extracted from the url.
        """
        df_copy = self.df.copy()
        df_copy['domain'] = df_copy['url'].apply(lambda row: parse.urlparse(row).netloc.split('.')[1])
        return df_copy[['domain']]


class HtmlTransformer:

    def __init__(self, data_frame):
        """
        Constructor for HTML Transformer.
        :param a dataframe containing the ad id and URL
        :except Value Error if HTML is not present/not expected data type
        :except Key Error if ad id is not present
        """
        try:
            if data_frame['html'].dtype != 'object':
                raise ValueError('HTML not expected data type - please use text object')
            self.df = data_frame
        except KeyError:
            raise
        except ValueError:
            raise

        self.extract_text()

    def extract_text(self):
        """
        Extracts the text from the raw html provided
        :return: a dataframe containing ad id and text
        """
        if 'text' not in self.df.columns.values:
            self.df['text'] = self.df['html'].apply(lambda row: self.cleanup(row))
        return self.df[['text']]

    def beautiful_soup(self, html_snippet):
        """
        A helper function for the cleanup of html
        :param html_snippet: a text string of html
        :return: a BeautifulSoup object to parse html
        """
        return BeautifulSoup(html_snippet, 'html.parser')

    def cleanup(self, html_snippet):
        """
        A helper function for text extraction
        :param html_snippet: a text string of html
        :return: a text string cleaned of javascript and styling
        """
        soup = self.beautiful_soup(html_snippet)
        for script in soup(['script', 'style']):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def extract_clickouts(self):
        """
        Counts the number of clickouts to the conversion form from each article page. Assumes
        that the most commonly used link is the form.
        :return: A dataframe containing ad id and the number of clickouts to the most commonly used link
        """
        self.df['num_clickouts'] = self.df['html'].apply(
            lambda row: self.count_links(self.beautiful_soup(row).find_all('a', href=True)))
        return self.df[['num_clickouts']]

    def count_links(self, soupy_links):
        """
        A helper function for extracting clickouts
        :param soupy_links: An array of all the links (tagged 'a' in BeautifulSoup object)
        :return: the count of the most common link in that set of links
        """
        hrefs = list(map(lambda link: link['href'], soupy_links))
        try:
            most_common = max(set(hrefs), key=hrefs.count)
        except ValueError:
            return None
        return hrefs.count(most_common)

    def extract_num_paras(self):
        """
        Extract the number of paragraphs in a given article
        :return: a dataframe containing ad id and the number of text blocks marked with the 'p' tag
        """
        self.df['num_paras'] = self.df['html'].apply(lambda row: len(self.beautiful_soup(row).find_all('p')))
        return self.df[['num_paras']]

    def extract_words_para(self):
        """
        Extract the number of words per paragraph
        :return: a dataframe containing ad id and the number of words per paragraph
        """
        if 'num_words' not in self.df.columns.values:
            self.extract_total_words()
        if 'num_paras' not in self.df.columns.values:
            self.extract_num_paras()
        self.df['words_para'] = round(self.df.num_words / self.df.num_paras, 4)
        return self.df[['words_para']]

    def extract_words_sentence(self):
        """
        Extract the number of words per sentence
        :return: a dataframe containing ad id and the number of words per sentence
        """
        if 'num_words' not in self.df.columns.values:
            self.extract_total_words()
        if 'num_sentences' not in self.df.columns.values:
            self.extract_num_sentences()
        self.df['words_sentence'] = round(self.df.num_words / self.df.num_sentences, 4)
        return self.df[['words_sentence']]

    def extract_num_sentences(self):
        """
        Extract the number of sentences
        :return: a dataframe containing ad id and the number of sentences
        """
        self.df['num_sentences'] = self.df['text'].apply(lambda row: len(re.split(r'[.!?]+', row)))
        return self.df[['num_sentences']]

    def extract_total_words(self):
        """
        Extract the number of words
        :return: a dataframe containing ad id and the number of words
        """
        self.df['num_words'] = self.df['text'].apply(lambda row: len(re.findall(r'\w+', row)))
        return self.df[['num_words']]

    def extract_syllables_word(self):
        """
        Extract the number of syllables per word
        :return: a dataframe containing ad id and the number of syllables per word
        """
        if 'num_words' not in self.df.columns.values:
            self.extract_total_words()
        df_copy = self.df.copy()
        df_copy['syllables'] = self.df['text'].apply(lambda row: sum(map(lambda word: self.syllable_count(word), row.split(' '))))
        self.df['syllables_word'] = round(df_copy.syllables/self.df.num_words, 4)
        return self.df[['syllables_word']]

    def syllable_count(self, word):
        """
        A helper function to count the number of syllables in a word
        Credit https://stackoverflow.com/questions/46759492/syllable-count-in-python
        :param word: the word needing syllables counting
        :return: the count of syllables
        """
        if len(word) == 0:
            return 0
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
                if word.endswith('e'):
                    count -= 1
        if count == 0:
            count += 1
        return count

    def extract_all(self):
        """
        Runs all of the above functions
        :return: a data frame with ad id and all of the above data points
        """
        print('...total words')
        self.extract_total_words()
        print('...number of sentences')
        self.extract_num_sentences()
        print('...number of paragraphs')
        self.extract_num_paras()
        print('...words per sentence')
        self.extract_words_sentence()
        print('...words per paragraph')
        self.extract_words_para()
        print('...syllables per word')
        self.extract_syllables_word()
        print('...number of clickouts')
        self.extract_clickouts()
        return self.df[['num_clickouts', 'words_sentence', 'words_para', 'syllables_word',
                        'num_paras', 'num_words', 'num_sentences']]


class TextProcessor:

    def __init__(self, data_frame):
        """
        Constructor for TextProcessor.
        :param data_frame: a data frame containing ad id, and text requiring processing
        """
        try:
            if data_frame['text'].dtype != 'object':
                raise ValueError('Text not expected data type - please use text object')
            self.df = data_frame
        except KeyError:
            raise
        except ValueError:
            raise
        nltk.download('stopwords')

    def lemmatize(self):
        """
        A function to lemmatize words in a given text body using NLTK implementation. Lemmatizes text columns
        with stop words removed.
        :return: a copy of the dataframe with lemmatization performed
        """
        df_copy = self.remove_stop_words().copy()
        df_copy['lemmatized_headline'] = df_copy['stop_word_headline'].apply(lambda row: self.lemmatizer(re.sub(r'[.\+\-!?\[\]\';\|():",*]', '', row)))
        df_copy['lemmatized_text'] = df_copy['stop_word_text'].apply(lambda row: self.lemmatizer(re.sub(r'[.\+\-!?\[\]\';\|():",*]', '', row)))
        return df_copy

    def lemmatizer(self, text):
        """
        A helper function for the lemmatize function - applies the lemmatization.
        :param text: the text to be lemmatized
        :return: the lemmatized text
        """
        wordnet_lemmatizer = WordNetLemmatizer()
        removed_extra_spaces = word_tokenize(' '.join(list(filter(None, text.split(r'\s')))))
        words_lemmatized = []
        for word in removed_extra_spaces:
            words_lemmatized.append(wordnet_lemmatizer.lemmatize(word))
        return ' '.join(words_lemmatized)

    def remove_stop_words(self):
        """
        Removes stop words from given text columns. Creates new columns in the dataframe to hold them.
        :return the dataframe containing the text fields with stop words removed
        """
        df_copy = self.df.copy()
        df_copy['stop_word_headline'] = df_copy['headline_text']\
            .apply(lambda row: self.stop_word_remover(re.sub(r'[.\+\-!?\[\]\';\|():",*]', '', row)))
        df_copy['stop_word_text'] = df_copy['text']\
            .apply(lambda row: self.stop_word_remover(re.sub(r'[.\+\-!?\[\]\';\|():",*]', '', row)))
        return df_copy

    def stop_word_remover(self, text):
        """
        A helper function for the remove stop words function.
        :param text: the text from which stop words should be removed
        :return: the text with stop words removed
        """
        removed_extra_spaces = word_tokenize(' '.join(list(filter(None, text.split(r'\s')))))
        stop_words = set(stopwords.words('english'))
        words_filtered = []
        for word in removed_extra_spaces:
            if word not in stop_words or word == 'this':
                words_filtered.append(word)
        return ' '.join(words_filtered)

    def tf_idf(self):
        """
        TF-IDF function - generates columns for each of the tokens with TF-IDF values. Treats ad text and
        headline text separately.
        :return: A combined dataframe with ad id and all the relevant token columns & values.
        """
        headline_df = self.lemmatize().copy()
        headline_df = headline_df.reset_index()
        headline_array = self.calculate_tf_idf(headline_df['lemmatized_headline'])
        # text_array = self.calculate_tf_idf(headline_df['lemmatized_text'])
        combined = headline_df.join(headline_array)
        combined.set_index('ad_id', inplace=True)
        combined = combined.drop('lemmatized_headline', axis=1)
        combined = combined.drop('lemmatized_text', axis=1)
        combined = combined.drop('stop_word_headline', axis=1)
        combined = combined.drop('stop_word_text', axis=1)
        combined = combined.drop('text', axis=1)
        combined = combined.drop('headline_text', axis=1)
        return combined  # .join(text_array, lsuffix='_headline', rsuffix='_text')

    def calculate_tf_idf(self, data_frame_column):
        """
        A helper function for the tf_idf function.
        :param data_frame_column: The column for which tf_idf should be calculated
        :return: A dataframe with the TF-IDF values for that column
        """
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(data_frame_column)
        tfidf_matrix = tfidf.toarray()
        vocab = vectorizer.get_feature_names()
        return pd.DataFrame(np.round(tfidf_matrix, 8), columns=vocab)

    def cosine_similarity(self):
        """
        Calculates cosine similarity between the headline and article text components of an ad.
        :return: a copy of the dataframe with ad id and cosine similarity.
        """
        headline_df = self.lemmatize()
        headline_df = headline_df.reset_index()
        headline_values = headline_df[['ad_id', 'lemmatized_headline']].values
        text_values = headline_df[['ad_id', 'lemmatized_text']].values
        combined_values = []
        for item in headline_values:
            item[0] = str(item[0]) + '_headline'
            combined_values.append(item)
        for item in text_values:
            item[0] = str(item[0]) + '_text'
            combined_values.append(item)
        combined_df = pd.DataFrame(combined_values, columns=['ad_id', 'text'])
        tf_idf = self.calculate_tf_idf(combined_df['text'])
        tf_idf = tf_idf.join(combined_df)
        tf_idf = tf_idf.drop('text', axis=1)
        similarity_matrix = cosine_similarity(tf_idf.drop('ad_id', axis=1))
        similarity_df = pd.DataFrame(similarity_matrix)
        copy_df = self.df.reset_index()
        copy_df['cosine_similarity'] = copy_df['ad_id'].apply(lambda row:
                                                similarity_df.iloc[tf_idf.loc[tf_idf['ad_id'] == str(row) + '_headline']
                                                .index[0]][tf_idf.loc[tf_idf['ad_id'] == str(row) + '_text'].index[0]])
        copy_df.set_index('ad_id', inplace=True)
        return copy_df[['cosine_similarity']]
