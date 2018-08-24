import cmd


class DataExploration(cmd.Cmd):

    def __init__(self, data_visualiser):
        super(DataExploration, self).__init__()
        self.viz = data_visualiser

    def do_describe(self, attributes=None):
        if len(attributes) > 0:
            attributes_array = attributes.split(',')
            self.viz.describe(attributes_array)
        else:
            self.viz.describe()

    def help_describe(self):
        print('Print a description of the dataframe.\nou can optionally specify column names in order ' +
              'to describe a subset of the dataframe.\nPlease use a comma (,) as a separator.')

    def do_histograms(self, col=None):
        self.viz.histograms(col)

    def help_histograms(self):
        print('Display histograms for all fo the columns in the dataframe.\nYou can optionally specify a ' +
              'single column name in order to show a histogram of that single column.')

    def do_pairwise_correlation(self):
        self.viz.pairwise_correlation_matrix()

    def help_pairwise_correlation(self):
        print('Display the pairwise correlation matrix for all columns in the dataframe.')

    def do_scatter_plot(self, columns=None):
        if len(columns) > 0:
            columns = columns.split(',')
            self.viz.pairwise_scatter_plot(columns)
        else:
            self.viz.pairwise_scatter_plot()

    def help_scatter_plot(self):
        print('Display a pairwise scatter plot for all of the columns in the dataframe.\nOptionally ' +
              'specify a subset of columns, separated by a comma (,).')

    def do_select_scatter_plot(self, cols):
        cols = cols.split(',')
        self.viz.selected_plot(cols[0], cols[1])

    def help_select_scatter_plot(self):
        print('Display a single scatter plot for two specified columns, separated by a comma (,).')

    def do_EOF(self, line):
        return True
