from conversion_predictor.Model import BasicModel
from conversion_predictor.Model import Visualisation
from conversion_predictor.Model import LinearRegressionModel
import pandas as pd
from unittest import TestCase


class VisualisationTests(TestCase):

    def setUp(self):
        target = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        target.set_index('ad_id', inplace=True)
        target = target.drop('url', 1)
        target = target.drop('page_text', 1)
        target = target.drop('headline', 1)
        target = target.apply(pd.to_numeric)
        self.model = Visualisation(target)

    def test_data_head(self):
        self.model.head()

    def test_data_describe(self):
        self.model.describe()

    def test_data_describe_attributes(self):
        self.model.describe(attributes=['words_para', 'words_sentence'])

    def test_histograms(self):
        self.model.histograms()

    def test_single_histogram(self):
        self.model.histograms('cosine_similarity')

    def test_heatmap(self):
        self.model.pairwise_correlation_matrix()

    def test_scatterplot(self):
        self.model.pairwise_scatter_plot(['words_para', 'words_sentence'])

    def test_selected_scatterplot(self):
        self.model.selected_scatter_plot('words_para', 'words_sentence')

    # def test_subclass(self):
        # target = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        # target.set_index('ad_id', inplace=True)
        # target = target.drop('url', 1)
        # target = target.drop('page_text', 1)
        # target = target.drop('headline', 1)
        # target = target.apply(pd.to_numeric)
        # model = LinearRegressionModel(target, 'cvr')
        # model.selected_scatter_plot('words_para', 'words_sentence')
