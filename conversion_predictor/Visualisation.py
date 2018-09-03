import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Visualisation:
    # credit: https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57
    def __init__(self, data_frame):
        """
        Constructor for the Visualisation class.
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
            self.df.hist(bins=10, color='steelblue', edgecolor='black',
                         linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
        else:
            # play with these dimensions a bit more
            self.df[col].hist(bins=10, color='steelblue', edgecolor='black',
                              linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
        plt.tight_layout(rect=(0, 0, 1.5, 1.5))
        plt.show()

    def pairwise_correlation_matrix(self):
        """
        Generates a pairwise correlation matrix with the attributes in the dataframe.
        :return:
        """
        f, ax = plt.subplots(figsize=(10, 6))
        corr = self.df.corr()
        hm = sns.heatmap(round(corr, 2), annot=True, ax=ax, cmap="coolwarm", fmt='.2f',
                         linewidths=.05)
        f.subplots_adjust(top=0.93)
        t = f.suptitle('Conversion Rate Attributes Correlation Heatmap', fontsize=14)
        plt.show()

    def pairwise_scatter_plot(self, columns=None):
        """
        Generates a pairwise scatter plot with the attributes in the dataframe.
        Has an option to specify a column subset to use in comparison.
        :param columns:
        :return:
        """
        if columns == None:
            columns = self.df.columns.values
        else:
            columns = list(filter(lambda column: column in self.columns, columns))
        pp = sns.pairplot(self.df[columns], height=2, aspect=2,
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

