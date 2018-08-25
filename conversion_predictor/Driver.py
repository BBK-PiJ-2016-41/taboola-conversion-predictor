import pandas as pd
import sys
from conversion_predictor.Connector import TaboolaConnector
from conversion_predictor.TokenRefresher import TaboolaTokenRefresher
from conversion_predictor.AdHeadlineExtraction import AdExtractor
from conversion_predictor.ArticleTextExtraction import UrlTransformer, HtmlTransformer, TextProcessor
from conversion_predictor.DataExploration import DataExploration
from conversion_predictor.ModelExploration import ModelExploration
from conversion_predictor.Model import Visualisation, LinearRegressionModel, LassoRegressionModel, RidgeRegressionModel


def main():
        # Intro text
        display_intro_text()
        response = input('(please press any key to continue)')

        # User should select ad platform
        data_option = run_data_collection_preamble()
        if data_option == 'T':
            data = pd.DataFrame(run_extraction('Taboola'))
            data = reformat_columns(data)
            data.set_index('ad_id', inplace=True)
        else:
            # Alternatively user should provide file with ad text, URLs, cvrs, cpc and ctr
            print('We\'ll need you to specify a file containing the columns ad_id, headline_text, url, cpc, ctr, cvr.')
            file_name = input('Please enter the full path of the file containing your ad data.').replace('\\', '\\\\')
            try:
                data = pd.read_csv(file_name, index_col='ad_id')
            except FileNotFoundError:
                print('Please specify an existing file.')

        print('This is a sample of the data we will be analysing:')
        print(data.head())

        # Option to use token data - depends on data set. Could rearrange to just do it for ad headline?
        # token_data = text_extractor.tf_idf()
        # print(token_data.head())
        processed_data = run_preprocessing(data)
        # Once dataframe is complete, suggest options for EDA
        processed_data.drop('headline_text', axis=1)
        processed_data.drop('url', axis=1)
        processed_data.drop('domain', axis=1)
        processed_data = processed_data.apply(pd.to_numeric)
        processed_data = processed_data.fillna(processed_data.mean())
        print('Data preprocessing is now complete. You have some options for Exploratory Data Analysis.')
        viz = Visualisation(processed_data)
        command_interpreter = DataExploration(viz)
        command_interpreter.cmdloop()
        # Once EDA is performed, suggest options for model
        print('You now have several options for regression analysis. The train/test split is set to 0.3')
        regression_type = 1
        while regression_type == 1:
            regression_type = input('Please enter Linear, Ridge or Lasso, or 0 to exit the regression phase: ')
            if regression_type == 'Lasso':
                model = LassoRegressionModel(processed_data, 'cvr')
            elif regression_type == 'Ridge':
                model = RidgeRegressionModel(processed_data, 'cvr')
            elif regression_type == 'Linear':
                model = LinearRegressionModel(processed_data, 'cvr')
            else:
                continue
            model_explorer = ModelExploration(model)
            model_explorer.cmdloop()

        output_file = input('Please specify the file you would like to output your data to.')
        processed_data.to_csv(output_file)


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
        connector = getattr(sys.modules[__name__], class_name)()
    except AttributeError:
        'The connector you have tried to access does not exist.'
    auth = get_auth(platform)
    start_date = input('Please enter the start date in the format YYYY-MM-DD')
    end_date = input('Please enter the end date in the format YYYY-MM-DD')
    print('Please provide a text file containing the IDs of the campaigns you would like to analyse.'
          'For best results, provide IDs of English campaigns only.')
    campaign_ids_file = input('Please enter the full file path:')
    connector.set_start_date(start_date)
    connector.set_end_date(end_date)
    connector.get_campaign_ids(campaign_ids_file)
    connector.set_credentials(auth)
    return connector.get_data()[1]
    # user should provide date range, relevant credentials
    # User should specify file containing campaign IDs (should be English only)


def get_auth(platform):
    class_name = platform + 'TokenRefresher'
    try:
        token_extractor = getattr(sys.modules[__name__], class_name)()
    except AttributeError:
        'The connector you have tried to access does not exist.'
    return token_extractor.refresh_tokens()[1]


def run_preprocessing(data):
    print('Extracting features from ad headline....')
    try:
        ad_extractor = AdExtractor(data[['headline_text']])
    except KeyError:
        print('Please make sure your file contains the following columns: '
              'columns ad_id, headline_text, url, cpc, ctr, cvr')
    data = data.join(ad_extractor.run_all())
    print('Extracting features from URL...')
    url_extractor = UrlTransformer(data[['url']])
    data = data.join(url_extractor.extract_domains(), on='ad_id')
    html_data = url_extractor.extract_html()
    print('Extracting features from HTML...')
    html_extractor = HtmlTransformer(html_data)
    data = data.join(html_extractor.extract_all())
    print('Extracting text comparison data...')
    text_extractor = TextProcessor(data[['headline_text']].join(html_extractor.extract_text()))
    data = data.join(text_extractor.cosine_similarity())
    # data.to_csv('C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\TextFilesAndCsvs\\TestOutput.csv')
    return data


def output_results():
    TODO


def reformat_columns(data):
    columns = {
        'ctr': 'ctr',
        'item': 'ad_id',
        'item_name': 'headline_text',
        'url': 'url',
        'clicks': 'clicks',
        'actions': 'conversions',
        'cvr': 'cvr',
        'cpc': 'cpc'
    }
    data_copy = pd.DataFrame()
    for column in columns:
        data_copy[columns[column]] = data[column]

    return data_copy


if __name__ == '__main__':
    main()
