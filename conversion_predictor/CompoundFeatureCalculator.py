class CompoundFeatureCalculator:

    def __init__(self, data_frame):
        try:
            self.df = data_frame.set_index('ad_id')
        except KeyError:
            raise

    def calc_compound(self, col1, col2):
        columns = self.df.columns.values
        if col1 not in columns or col2 not in columns:
            raise KeyError('Please specify columns contained in your dataframe: ' + ' '.join(columns))
        self.df[col1 + '_' + col2] = self.df.apply(lambda row: (row[col1] * row[col2]), axis=1)
        return self.df
