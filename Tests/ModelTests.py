from conversion_predictor.Model import BasicModel
from conversion_predictor.Visualisation import Visualisation
from conversion_predictor.Model import LinearRegressionModel, LassoRegressionModel, RidgeRegressionModel
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


class LinearModelTests(TestCase):

    def setUp(self):
        target = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        target.set_index('ad_id', inplace=True)
        target = target.drop('url', 1)
        target = target.drop('page_text', 1)
        target = target.drop('headline', 1)
        target = target.apply(pd.to_numeric)
        self.linear_model = LinearRegressionModel(target, 'cvr')

    def test_score(self):
        score = self.linear_model.score()
        self.assertGreater(1, score)
        self.assertLess(0, score)
        self.linear_model.print_score()

    def test_rmse(self):
        rmse = self.linear_model.root_mean_squared_error()
        self.assertLess(0, rmse)

    def test_cross_val(self):
        score = self.linear_model.cross_validation_score(5)
        self.linear_model.print_cross_val(5)


class LassoModelTests(TestCase):

    def setUp(self):
        target = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        target.set_index('ad_id', inplace=True)
        target = target.drop('url', 1)
        target = target.drop('page_text', 1)
        target = target.drop('headline', 1)
        target = target.apply(pd.to_numeric)
        self.linear_model = LassoRegressionModel(target, 'cvr')

    def test_score(self):
        score = self.linear_model.score()
        self.assertGreater(1, score)
        self.assertLess(0, score)
        self.linear_model.print_score()

    def test_rmse(self):
        rmse = self.linear_model.root_mean_squared_error()
        self.assertLess(0, rmse)

    def test_cross_val(self):
        score = self.linear_model.cross_validation_score(5)
        self.linear_model.print_cross_val(5)

    def test_coef(self):
        print(self.linear_model.coef())

class RidgeModelTests(TestCase):

    def setUp(self):
        target = pd.read_json("C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutput9.json")
        target.set_index('ad_id', inplace=True)
        target = target.drop('url', 1)
        target = target.drop('page_text', 1)
        target = target.drop('headline', 1)
        target = target.apply(pd.to_numeric)
        self.linear_model = RidgeRegressionModel(target, 'cvr')

    def test_score(self):
        score = self.linear_model.score()
        self.assertGreater(1, score)
        self.assertLess(0, score)
        self.linear_model.print_score()

    def test_rmse(self):
        rmse = self.linear_model.root_mean_squared_error()
        self.assertLess(0, rmse)

    def test_cross_val(self):
        score = self.linear_model.cross_validation_score(5)
        self.linear_model.print_cross_val(5)