import pandas as pd


def main():
        #user should provide date range
        #prompt user for each category of feature engineering
        #contains master dataframe

        data_file = 'C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutputSkeleton.csv'
        data_frame = pd.read_csv(data_file)
        print(data_frame)

if __name__ == '__main__':
    main()
