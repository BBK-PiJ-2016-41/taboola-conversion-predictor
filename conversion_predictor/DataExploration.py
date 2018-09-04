import cmd


class DataExploration(cmd.Cmd):
    """
    A class to enable Exploratory Data Analysis. Inherits from Cmd package.
    """

    def __init__(self, data_visualiser):
        """
        Constructor for the DataExploration class. Inherits from the Cmd package.
        :param data_visualiser: the data visualisation class providing the visualisation functionality
        """
        super(DataExploration, self).__init__()
        self.viz = data_visualiser

    def do_printcolumns(self, col=None):
        """
        Prints the columns in the dataframe in question
        :param col:
        """
        print(self.viz.columns)

    def help_printcolumns(self):
        """
        Describes the printcolumns function to the user
        """
        print('Print out the column names in the dataframe.')

    def do_describe(self, attributes=None):
        """
        Calls the describe function on the dataframe to give column details. Can be restricted to a subset of columns.
        :param attributes: The subset of columns required, if any.
        """
        if len(attributes) > 0:
            attributes_array = attributes.split(',')
            self.viz.describe(attributes_array)
        else:
            self.viz.describe()

    def help_describe(self):
        """
        Describes the describe function to the user
        """
        print('Print a description of the dataframe.\nYou can optionally specify column names in order ' +
              'to describe a subset of the dataframe.\nPlease use a comma (,) as a separator.')

    def do_histograms(self, col=None):
        """
        Outputs thumbnail histograms for all columns in the dataframe. You can optionally specify a single column name.
        :param col: The column for which histograms should be shown
        """
        self.viz.histograms(col)

    def help_histograms(self):
        """
        Describes the histograms function to the user
        """
        print('Display histograms for all fo the columns in the dataframe.\nYou can optionally specify a ' +
              'single column name in order to show a histogram of that single column.')

    def do_pairwisecorrelation(self, col=None):
        """
        Outputs a pairwise correlation matrix for all the columns in the dataframe.
        :param col:
        """
        self.viz.pairwise_correlation_matrix()

    def help_pairwisecorrelation(self):
        """
        Describes the pairwise correlation function to the user
        """
        print('Display the pairwise correlation matrix for all columns in the dataframe.')

    def do_scatterplot(self, columns=None):
        """
        Produces a pairwise scatter plot for all the columns in the dataframe. Optionally, specify
        a subset of columns.
        :param columns:
        """
        if len(columns) > 0:
            columns = columns.split(',')
            self.viz.pairwise_scatter_plot(columns)
        else:
            self.viz.pairwise_scatter_plot()

    def help_scatterplot(self):
        """
        Describes the scatterplot function to the user
        """
        print('Display a pairwise scatter plot for all of the columns in the dataframe.\nOptionally ' +
              'specify a subset of columns, separated by a comma (,).')

    def do_selectscatterplot(self, cols):
        """
        Displays a scatterplot of two selected columns.
        :param cols: The columns to be displayed in a scatterplot.
        """
        cols = cols.split(',')
        self.viz.selected_plot(cols[0], cols[1])

    def help_selectscatterplot(self):
        """
        Describes the select scatterplot function to the user
        """
        print('Display a single scatter plot for two specified columns, separated by a comma (,).')

    def do_EOF(self, line):
        """
        Closes the Cmd-based interface and moves onto the next stage of the application.
        :param line:
        :return: True
        """
        return True
