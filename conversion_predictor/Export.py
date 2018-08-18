class CsvExport:

    def __init__(self, df, file):
        self.data_frame = df
        self.file_name = file

    def write_out(self):
        try:
            self.data_frame.to_csv(self.file_name)
        except IOError:
            raise
