from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso


class BasicModel(ABC):

    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        """
        Constructor for the BasicModel class and subclasses.
        Converts data types in dataframe to floats and fills in any NaN values with the mean of the column.
        Calls the method generate_test_split() to get test subsets.
        :param data_frame: The dataframe containing ad data.
        :param target_variable_col: The column to specify the target variable.
        :param split_size: The ratio of test to training data.
        """
        self.df = data_frame
        self.target = target_variable_col
        self.df = self.df.apply(pd.to_numeric)
        self.columns = self.df.columns.values
        for column in self.columns:
            self.df[column] = self.df[column].astype(float)
        self.df = self.df.fillna(self.df.mean())
        self.X, self.y, self.X_train, self.X_test, self.y_train, self.y_test = self.generate_test_split(split_size)

    def generate_test_split(self, split_size):
        """
        Splits the dataset into test and training data.
        :param split_size: The ratio of test to training data.
        :return: Training and test data sets based on the specified target variable.
        """
        x = self.df.drop([self.target], 1).values
        y = self.df[self.target].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=split_size)
        return x, y, x_train, x_test, y_train, y_test

    def cross_validation(self, folds):
        TODO

    @abstractmethod
    def fit_model(self):
        """
        Fits the relevant model as specified by the child class.
        :return:
        """
        pass

    @abstractmethod
    def predict(self):
        """
        Predicts model outcome as specified by the child class.
        :return:
        """
        pass

    @abstractmethod
    def score(self):
        """
        Generates the model accuracy score as specified by the child class.
        :return:
        """
        pass

    @abstractmethod
    def rmse(self):
        pass



class LinearRegressionModel(BasicModel):

    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        super().__init__(data_frame, target_variable_col, split_size)
        self.lm = LinearRegression()
        self.fit_model()
        self.prediction = self.predict()

    def fit_model(self):
        self.lm.fit(self.X_train, self.y_train)

    def predict(self):
        return self.lm.predict(self.X_test)

    def score(self):
        return self.lm.score(self.X_test, self.y_test)

    def print_score(self):
        print(self.score())

    def rmse(self):
        pass


class LassoRegressionModel(BasicModel):

    def __init__(self, data_frame, target_variable_col, split_size=0.3, alpha=0.1):
        super().__init__(data_frame, target_variable_col, split_size)
        self.alpha = alpha
        self.lm = Lasso(self.alpha)

    # this method returns something when others do not
    def fit_model(self):
        coef = self.lm.fit(self.X, self.y).coef_
        return coef

    def predict(self):
        self.lm.predict(self.X_test)

    def score(self):
        score = self.lm.score(self.X_test, self.y_test)
        print(score)
        return score

    def rmse(self):
        pass

    def reset_alpha(self, alpha):
        """
        Enables the user to set the alpha parameter for model tuning.
        :param alpha: The alpha parameter value.
        :return:
        """
        self.alpha = alpha
        self.lm = Lasso(self.alpha)


class RidgeRegressionModel(BasicModel):

    def __init__(self, data_frame, target_variable_col, split_size=0.3, alpha=0.1):
        super().__init__(data_frame, target_variable_col, split_size)
        self.alpha = alpha
        self.rm = Ridge(self.alpha)

    def fit_model(self):
        self.rm.fit(self.X_train, self.y_train)

    def predict(self):
        self.rm.predict(self.X_test)

    def score(self):
        score = self.rm.score(self.X_test, self.y_test)
        print(score)
        return score

    def rmse(self):
        pass

    def reset_alpha(self, alpha):
        """
        Enables the user to set the alpha parameter for model tuning.
        :param alpha: The alpha parameter value.
        :return:
        """
        self.alpha = alpha
        self.rm = Ridge(self.alpha)
