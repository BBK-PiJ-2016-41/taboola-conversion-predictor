import pandas as pd
import sys
from conversion_predictor.Connector import TaboolaConnector
from conversion_predictor.TokenRefresher import TaboolaTokenRefresher
from conversion_predictor.AdHeadlineExtraction import AdExtractor
from conversion_predictor.CompoundFeatureCalculator import CompoundFeatureCalculator
from conversion_predictor.ArticleTextExtraction import UrlTransformer, HtmlTransformer, TextProcessor
from conversion_predictor.DataExploration import DataExploration
from conversion_predictor.ModelExploration import ModelExploration
from conversion_predictor.Visualisation import Visualisation
from conversion_predictor.Model import LinearRegressionModel, LassoRegressionModel, RidgeRegressionModel, \
    RandomForestRegressionModel, GradientBoostingRegressionModel
from conversion_predictor.Factory import ConnectorFactory, TokenRefresherFactory


def main():
    """
    The main driver class for the conversion-predictor application.
    :return:
    """

    # Intro text
    display_intro_text()
    response = input('(please press any key to continue)')

    # Instantiate factories for ad platform access
    connector_factory = ConnectorFactory()
    token_factory = TokenRefresherFactory()

    # User should select ad platform
    data_option = run_data_collection_preamble()
    platform = switcher(data_option)
    print(platform)
    if platform != 'File':
        successful_connection = 0
        while successful_connection == 0:
            try:
                connector = connector_factory.get_object(platform)
                print(connector.address)
                token_refresher = token_factory.get_object(platform)
                successful_connection = 1
                data = pd.DataFrame(run_extraction(connector, token_refresher))
                data = reformat_columns(data)
                data.set_index('ad_id', inplace=True)
            except AttributeError:
                print('The platform you have selected is not supported.')
                data_option = run_data_collection_preamble()
                platform = switcher(data_option)
                if platform == 'File':
                    break

    if platform == 'File':
        # Alternatively user should provide file with ad text, URLs, cvrs, cpc and ctr
        print('We\'ll need you to specify a file containing the columns ad_id, headline_text, url, cpc, ctr, cvr.')
        file_name = input('Please enter the full path of the file containing your ad data.').replace('\\', '\\\\')
        try:
            data = pd.read_csv(file_name, index_col='ad_id')
        except FileNotFoundError:
            print('Please specify an existing file.')

    print('This is a sample of the data we will be analysing:')
    print(data.head())

    processed_data, text_processed_data = run_preprocessing(data)
    cleaned_data = clean_columns_formats(text_processed_data)
    # Once dataframe is complete, suggest options for EDA
    print('Data preprocessing is now complete. You have some options for Exploratory Data Analysis.'
          '\nThis will not include the tokenised data for ease of visualisation.')
    viz = Visualisation(clean_columns_formats(processed_data))
    command_interpreter = DataExploration(viz)
    command_interpreter.cmdloop()

    cleaned_data.to_csv('C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\TextFilesAndCsvs\\TestOutput.csv')

    # Once EDA is performed, suggest options for model
    print('You now have several options for regression analysis. The train/test split is set to 0.3')
    regression_type = 1
    while regression_type != '0':
        regression_type = input('Please enter Linear, Ridge, Lasso, Random Forest or Gradient Boosting, or 0 to exit the regression phase: ')
        if regression_type == 'Lasso':
            model = LassoRegressionModel(clean_columns_formats(processed_data), 'cvr')
        elif regression_type == 'Ridge':
            model = RidgeRegressionModel(cleaned_data, 'cvr')
        elif regression_type == 'Linear':
            model = LinearRegressionModel(cleaned_data, 'cvr')
        elif regression_type == 'Random Forest':
            model = RandomForestRegressionModel(cleaned_data, 'cvr')
        elif regression_type == 'Gradient Boosting':
            model = GradientBoostingRegressionModel(cleaned_data, 'cvr')
        else:
            print('Please enter Linear, Ridge, Lasso, Random Forest, Gradient Boosting, or 0 to exit.')

        if regression_type != '0':
            model_explorer = ModelExploration(model)
            model_explorer.cmdloop()

    # Finally, output the data to the specified destination.
    output_file = input('Please specify the file you would like to output your data to.')
    processed_data.to_csv(output_file)


def display_intro_text():
    """
    Method to display the introduction to the application.
    """
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
    """
    Method to establish the data collection format.
    :return: The code letter for the required data collection format.
    """
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


def run_extraction(connector, authenticator):
    """
    Extracts the data from the specified location.
    :param connector: Class to make connection to ad platform
    :param authenticator: Class to provide authentication
    :return: The data extracted from the ad platform
    """
    auth = authenticator.refresh_tokens()[1]
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


def run_preprocessing(data):
    """
    Runs the data preprocessing steps in the pipeline
    :param data: The data extracted from ad platform or file
    :return: The features extracted from the data, token features (can be discarded in cases of feature proliferation)
    """
    print('Extracting features from ad headline....')
    try:
        ad_extractor = AdExtractor(data[['headline_text']])
    except KeyError:
        print('Please make sure your file contains the following columns: '
              'columns ad_id, headline_text, url, cpc, ctr, cvr')
    data = data.join(ad_extractor.run_all())
    # compound_calc = CompoundFeatureCalculator(data)
    # data = data.join(compound_calc.calc_compound('cpc', 'ctr'))
    print('Extracting features from URL...')
    url_extractor = UrlTransformer(data[['url']])
    data = data.join(url_extractor.extract_domains(), on='ad_id')
    html_data = url_extractor.extract_html()
    print('Extracting features from HTML...')
    html_extractor = HtmlTransformer(html_data)
    data = data.join(html_extractor.extract_all())

    print('Extracting text comparison data...')
    text_extractor = TextProcessor(data[['headline_text']].join(html_extractor.extract_text()))
    token_data = text_extractor.tf_idf()
    data = data.join(text_extractor.cosine_similarity())
    text_data = data.join(token_data, rsuffix='_hl')
    return data, text_data


def clean_columns_formats(data):
    """
    Drops any text based fields from the data to be run by the models
    :param data: the processed data
    :return: the dataframe without any text fields, and with missing values imputated
    """
    data = data.drop('headline_text', axis=1)
    data = data.drop('url', axis=1)
    data = data.drop('domain', axis=1)
    data = data.apply(pd.to_numeric)
    data = data.fillna(data.mean())
    return data


def switcher(input):
    """
    Produces the beginning of the class name for each data extraction type. File is the default return type.
    :param input: The code letter inputted by the user
    :return: The extraction type
    """
    dictionary = {
        'T': 'Taboola',
        'F': 'File'
    }
    return dictionary.get(input, 'File')


def reformat_columns(data):
    """
    Standardises the columns in the data produced by the ad platform.
    :param data: The data extracted from the ad platform
    :return: The data copied into new column names
    """
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
