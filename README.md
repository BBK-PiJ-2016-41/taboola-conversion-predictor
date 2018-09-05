# Conversion Predictor

This software is a simple data processing pipeline. It ingests data from the advertising platform of your choice, and applies text preprocessing in order to transform ad-level data into features suitable for a machine learning model. It then offers a choice of options for regression analysis in order to determine the feature that best contribute to conversion rate.

## Getting Started

It is recommended to download this software via PyCharm. Otherwise, there is a command-line interface available; please download the conversion_predictor folder.

### Prerequisites

You will need Python 3.6 or higher installed on your machine. Additionally, the following packages are used by the project:

```
PyInstaller	3.3.1	3.3.1
altgraph	0.16.1	0.16.1
beautifulsoup4	4.6.3	4.6.3
certifi	2018.8.13	2018.8.24
chardet	3.0.4	3.0.4
cycler	0.10.0	0.10.0
future	0.16.0	0.16.0
idna	2.7	2.7
kiwisolver	1.0.1	1.0.1
macholib	1.11	1.11
matplotlib	2.2.3	3.0.0rc2
nltk	3.3	3.3
numpy	1.15.0	1.15.1
pandas	0.23.3	0.23.4
pefile	2018.8.8	2018.8.8
pip	10.0.1	18.0
pyparsing	2.2.0	2.2.0
pypiwin32	223	223
python-dateutil	2.7.3	2.7.3
pytz	2018.5	2018.5
pywin32	223	223
requests	2.19.1	2.19.1
scikit-learn	0.19.2	0.20rc1
scipy	1.1.0	1.1.0
seaborn	0.9.0	0.9.0
setuptools	39.1.0	40.2.0
six	1.11.0	1.11.0
sklearn	0.0	0.0
urllib3	1.23	1.23
```

### Example using an ad platform (e.g. Taboola)

The application will ask which format you wish to use. You will need to input your Taboola Client ID and Client Secret when prompted, then give the start and end date of the time period you wish to analyse.

### Example using data from file

The application will ask you for the full file path of the file containing your data. It should contain the columns: ad_id, headline_text, url, cpc, ctr, cvr.

### Exploring the data and exploring the models

The application will offer options for Exploratory Data Analysis and analysing the models themselves. For this, it uses the Cmd package. You will be able to input commands via the keyboard.
To see which commands are available to you, type 'help'. To see what a particular command does, type 'help <command>'.
For more information, please see the documentation: https://wiki.python.org/moin/CmdModule.

## Running the tests

The automated tests can be found in the Tests folder. They can be run using UnitTest in PyCharm.

## Coding style

This code was developed using PEP8.

## Deployment

An executable version of this software is available using PyInstaller. It is available from the author at no cost.

## Built With

* PyCharm
* PyInstaller

## Contributing

Please contact the author directly if you would like to contribute.

## Authors

Kathryn Buckley (BBK-PiJ-2016-41)

## Acknowledgments

* Stephen Coyne
* https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57
* https://stackoverflow.com/questions/46759492/syllable-count-in-python
