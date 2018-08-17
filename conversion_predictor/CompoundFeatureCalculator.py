class CompoundFeatureCalculator:

    def __init__(self, data_frame):
        try:
            if data_frame['headline_text'].dtype != 'object':
                raise ValueError('Headline text not expected data type - please use text object')
            self.df = data_frame.set_index('ad_id')
        except KeyError:
            raise
        except ValueError:
            raise

    def calc_compound(self, col1, col2):
        TODO