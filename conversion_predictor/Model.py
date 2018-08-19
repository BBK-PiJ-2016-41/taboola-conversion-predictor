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
        self.df = data_frame
        self.columns = self.df.columns.values

    def head(self):
        print(self.df.head())

    def describe(self, attributes=[]):
        if len(attributes) > 0:
            attributes = list(filter(lambda attribute: attribute in self.columns, attributes))
            print(self.df[attributes].describe())
        else:
            print(self.df.describe())

    def histograms(self, col="None"):
        if col == "None" or col not in self.columns:
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
        f, ax = plt.subplots(figsize=(10, 6))
        corr = self.df.corr()
        hm = sns.heatmap(round(corr, 2), annot=True, ax=ax, cmap="coolwarm", fmt='.2f',
                         linewidths=.05)
        f.subplots_adjust(top=0.93)
        t = f.suptitle('Conversion Rate Attributes Correlation Heatmap', fontsize=14)
        plt.show()

    def pairwise_scatter_plot(self, columns):
        columns = list(filter(lambda column: column in self.columns, columns))
        pp = sns.pairplot(self.df[columns], size=1.8, aspect=1.8,
                          plot_kws=dict(edgecolor="k", linewidth=0.5),
                          diag_kind="kde", diag_kws=dict(shade=True))

        fig = pp.fig
        fig.subplots_adjust(top=0.93, wspace=0.3)
        t = fig.suptitle('Conversion Rate Attributes Pairwise Plots', fontsize=14)
        plt.show()

    def selected_scatter_plot(self, col1, col2):
        plt.scatter(self.df[col1], self.df[col2],
                    alpha=0.4, edgecolors='w')

        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title(col1 + ' - ' + col2, y=1.05)
        plt.show()


class BasicModel:
    def __init__(self, data_frame, target_variable_col, split_size=0.3):
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
        x = self.df[self.target]
        y = self.df.drop([self.target], 1)
        x_train, x_test, y_train, y_test = train_test_split(X, y, split_size)
        return x, y, x_train, x_test, y_train, y_test

    def fit_model(self):
        pass

    def predict(self):
        pass

    def score(self):
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

    def reset_alpha(self, alpha):
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
        self.alpha = alpha
        self.rm = Ridge(self.alpha)

