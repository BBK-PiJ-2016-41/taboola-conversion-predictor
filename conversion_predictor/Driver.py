import pandas as pd
from conversion_predictor.Connector import TaboolaConnector
import cmd as Cmd
import sys


def main():
        # Intro text
        display_intro_text()
        response = input('(please press any key to continue)')

        # User should select ad platform
        data_option = run_data_collection_preamble()
        data = 0
        if data_option == 'T':
            data = run_extraction('Taboola')
        else:
            print('We\'ll need you to specify a file containing Ad ID, Headline, URL, CPC, CTR, Conversion Rate.')
            file_name = input('Please enter the full path of the file containing your ad data.').replace('\\', '\\\\')
            data = pd.read_csv(file_name)

        # Alternatively user should provide file with ad text, URLs, cvrs, cpc and ctr
        # data_file = 'C:\\Users\\Kathryn\\Documents\\Birkbeck\\MSc Project\\DataOutputSkeleton.csv'
        #         # data_frame = pd.read_csv(data_file)

        # prompt user for each category of feature engineering
        # contains master dataframe - add new features after each stage of engineering
        # Once dataframe is complete, suggest options for EDA
        # Once EDA is performed, suggest options for model
        # Output relevant visualisations and model scores to command line and to file


def display_intro_text():
    intro_text = """    Welcome to the Conversion Rate Predictor.
    This application will analyse text-based features of your CDN campaigns, and suggest which are
    most likely to contribute positively towards a high conversion rate.
    You can use this information to inform campaign strategy and testing priorities.
    
    You can choose to extract data from Taboola, or supply the application with a file containing
    some basics including ad headline and url.
    
    Let's get started!
    
    """
    print(intro_text)


def run_data_collection_preamble():
    explanation_text = """
    Firstly, please select your data collection method.
    """
    option_text = """
    To extract data from Taboola, enter T.
    To extract data from a file, enter F.
    """
    print(explanation_text)
    response = input(option_text)
    while response != 'T' and response != 'F':
        response = input('Please enter T for Taboola or F for File.')
    return response


def run_extraction(platform):
    class_name = platform + 'Connector'
    try:
        connector = getattr(sys.modules[__name__], class_name)
    except AttributeError:
        'The connector you have tried to access does not exist.'

    start_date = input('Please enter the start date in the format YYYY-MM-DD')
    end_date = input('Please enter the end date in the format YYYY-MM-DD')
    auth = input('Please provide your access token.')
    print('Please provide a text file containing the IDs of the campaigns you would like to analyse.'
          'For best results, provide IDs of English campaigns only.')
    campaign_ids_file = input('Please enter the full file path:')
    connector.set_start_date(start_date)
    connector.set_end_date(end_date)
    connector.set_credentials(auth)
    connector.get_campaign_ids(campaign_ids_file)
    return connector.get_data()
    # user should provide date range, relevant credentials
    # User should specify file containing campaign IDs (should be English only)


def run_feature_engineering():
    TODO


def run_eda():
    TODO


def run_regression():
    TODO


def output_results():
    TODO


# class DataCollectionPrompt(Cmd):
#     TODO


if __name__ == '__main__':
    main()
