class CompoundFeatureCalculator:

    def __init__(self, data_frame):
        """
        Constructor for Compound Feature Calculator
        :param data_frame: a dataframe containing the ad id and the columns needing combining.
        """
        self.df = data_frame

    def calc_compound(self, col1, col2):
        """
        Creates a compound feature based on the two specified columns by multiplying their values together.
        :param col1: The first column name
        :param col2: The second column name
        :return: a dataframe containing the new combined column
        """
        copy_df = self.df.copy()
        columns = copy_df.columns.values
        if col1 not in columns or col2 not in columns:
            raise KeyError('Please specify columns contained in your dataframe: ' + ' '.join(columns))
        copy_df[col1 + col2] = copy_df.apply(lambda row: (row[col1] * row[col2]), axis=1)
        print(copy_df[[col1 + col2]])
        return copy_df[[col1 + col2]]
