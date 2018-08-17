class CompoundFeatureCalculator:

    def __init__(self, data_frame):
        try:
            self.df = data_frame.set_index('ad_id')
        except KeyError:
            raise

    def calc_compound(self, col1, col2):
        TODO