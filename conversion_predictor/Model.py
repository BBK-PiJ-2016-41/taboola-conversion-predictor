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


class Visualisation:
    # credit: https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57
    def __init__(self, data_frame):
        """
        Constructor for the Visualisation class. May be useful for EDA.
        :param data_frame: the dataframe containing the data to be visualised.
        Use built-in head() method in dataframe to print first few lines.
        """
        self.df = data_frame
        self.columns = self.df.columns.values

    def describe(self, attributes=[]):
        """
        Calls the describe() method on the dataframe, with an option to specify a subset of columns.
        :param attributes: optional parameter listing the columns for visualisation.
        :return:
        """
        if len(attributes) > 0:
            attributes = list(filter(lambda attribute: attribute in self.columns, attributes))
            print(self.df[attributes].describe())
        else:
            print(self.df.describe())

    def histograms(self, col='None'):
        """
        Calls the hist() method on the dataframe, with an option to specify a subset of columns.
        :param col: optional parameter listing the columns for visualisation.
        :return:
        """
        if col == 'None' or col not in self.columns:
            # play with these dimensions a bit more
            self.df.hist(bins=15, color='steelblue', edgecolor='black', linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
            plt.tight_layout(rect=(0, 0, 1.2, 1.2))
            plt.show()
        else:
            # play with these dimensions a bit more
            self.df[col].hist(bins=15, color='steelblue', edgecolor='black', linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
            plt.tight_layout(rect=(0, 0, 1.2, 1.2))
            plt.show()

    def pairwise_correlation_matrix(self):
        """
        Generates a pairwise correlationi matrix with the attributes in the dataframe.
        :return:
        """
        f, ax = plt.subplots(figsize=(10, 6))
        corr = self.df.corr()
        hm = sns.heatmap(round(corr, 2), annot=True, ax=ax, cmap="coolwarm", fmt='.2f',
                         linewidths=.05)
        f.subplots_adjust(top=0.93)
        t = f.suptitle('Conversion Rate Attributes Correlation Heatmap', fontsize=14)
        plt.show()

    def pairwise_scatter_plot(self, columns):
        """
        Generates a pairwise scatter plot with the attributes in the dataframe.
        Has an option to specify a column subset to use in comparison.
        :param columns:
        :return:
        """
        columns = list(filter(lambda column: column in self.columns, columns))
        pp = sns.pairplot(self.df[columns], size=1.8, aspect=1.8,
                          plot_kws=dict(edgecolor="k", linewidth=0.5),
                          diag_kind="kde", diag_kws=dict(shade=True))

        fig = pp.fig
        fig.subplots_adjust(top=0.93, wspace=0.3)
        t = fig.suptitle('Conversion Rate Attributes Pairwise Plots', fontsize=14)
        plt.show()

    def selected_scatter_plot(self, col1, col2):
        """
        Generates a scatter plat with the specified columns.
        :param col1: The first column
        :param col2: The second column
        :return:
        """
        plt.scatter(self.df[col1], self.df[col2],
                    alpha=0.4, edgecolors='w')

        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title(col1 + ' - ' + col2, y=1.05)
        plt.show()


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
        # pass in through constructor? dependency injection? or just keep separate?
        self.df = self.df.apply(pd.to_numeric)
        for column in self.columns:
            self.df[column] = self.df[column].astype(float)
        self.df = self.df.fillna(self.df.mean())
        self.visualisation = Visualisation(self.df)
        self.X, self.y, self.X_train, self.X_test, self.y_train, self.y_test = self.generate_test_split(split_size)

    def generate_test_split(self, split_size):
        """
        Splits the dataset into test and training data.
        :param split_size: The ratio of test to training data.
        :return: Training and test data sets based on the specified target variable.
        """
        x = self.df.drop([self.target], 1)
        y = self.df[self.target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, split_size)
        return x, y, x_train, x_test, y_train, y_test

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


class LinearRegressionModel(BasicModel):

    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        super().__init__(data_frame, target_variable_col, split_size)
        self.lm = LinearRegression()

    def fit_model(self):
        self.lm.fit(self.X_train, self.y_train)

    def predict(self):
        self.lm.predict(self.X_test)

    def score(self):
        self.score = self.lm.score(self.X_test, self.y_test)
        return self.score


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
        self.lm.score(self.X_test, self.y_test)

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
        return score

    def reset_alpha(self, alpha):
        """
        Enables the user to set the alpha parameter for model tuning.
        :param alpha: The alpha parameter value.
        :return:
        """
        self.alpha = alpha
        self.rm = Ridge(self.alpha)
