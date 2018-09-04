from abc import ABC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


class BasicModel(ABC):

    def __init__(self, data_frame, target_variable_col, model_type, split_size=0.3):
        """
        Constructor for the BasicModel class and subclasses.
        Converts data types in dataframe to floats and fills in any NaN values with the mean of the column.
        Calls the method generate_test_split() to get test subsets.
        :param data_frame: The dataframe containing ad data.
        :param target_variable_col: The column to specify the target variable.
        :param model_type the model to be used for training
        :param split_size: The ratio of test to training data.
        """
        self.df = data_frame
        self.target = target_variable_col
        self.df = self.df.apply(pd.to_numeric)
        self.columns = self.df.columns.values
        for column in self.columns:
            self.df[column] = self.df[column].astype(float)
        self.df = self.df.fillna(self.df.mean())
        self.lm = model_type
        self.X, self.y, self.X_train, self.X_test, self.y_train, self.y_test = self.generate_test_split(split_size)
        self.prediction = ''

    def generate_test_split(self, split_size):
        """
        Splits the dataset into test and training data.
        :param split_size: The ratio of test to training data.
        :return: Training and test data sets based on the specified target variable.
        """
        x = self.df.drop([self.target], 1).values
        y = self.df[self.target].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=split_size)
        return x, y, x_train, x_test, y_train, y_test

    def cross_validation_score(self, folds=5):
        """
        Runs cross-validation with the given number of folds.
        :param folds: Number of folds for cross-validation (k).
        :return: Mean of the results obtained, rounded to 6 dp.
        """
        results = cross_val_score(self.lm, self.X, self.y, cv=folds)
        return round(np.mean(results), 6)

    def print_cross_val(self, folds=5):
        """
        Prints the cross-validation output.
        :param folds: Number of folds for cross-validation (k).
        """
        print(self.cross_validation_score(folds))

    def fit_model(self):
        """
        Calls the method fit on the model instantiated by that particular class.
        """
        self.lm.fit(self.X_train, self.y_train)

    def predict(self):
        """
        Calls the predict method on the model instantiated by that particular class.
        :return: the prediction outcome.
        """
        return self.lm.predict(self.X_test)

    def score(self):
        """
        Calls the score method on the model instantiated by that particular class.
        :return: the score output, rounded to 6 dp.
        """
        return round(self.lm.score(self.X_test, self.y_test), 6)

    def print_score(self):
        """
        Prints the outcome of the score method.
        """
        print(self.score())

    def root_mean_squared_error(self):
        """
        Calls the root mean squared error method on the model instantiated by that particular class.
        :return: RMSE rounded to 6 dp.
        """
        return round(np.sqrt(mean_squared_error(self.y_test, self.prediction)), 6)

    def print_rmse(self):
        """
        Prints the outcome of the root mean squared error method.
        """
        print(self.root_mean_squared_error())


class LinearRegressionModel(BasicModel):
    """
    Inherits BasicModel class, using the Linear Regression model.
    """
    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        super().__init__(data_frame, target_variable_col, LinearRegression(), split_size)
        self.fit_model()
        self.prediction = self.predict()


class LassoRegressionModel(BasicModel):
    """
    Inherits BasicModel class, using the Lasso Regression model.
    """
    def __init__(self, data_frame, target_variable_col, split_size=0.3, alpha=0.1):
        super().__init__(data_frame, target_variable_col, Lasso(alpha, normalize=False), split_size)
        self.alpha = alpha
        self.fit_model()
        self.prediction = self.predict()

    def reset_alpha(self, alpha):
        """
        Enables the user to set the alpha parameter for model tuning.
        :param alpha: The alpha parameter value.
        :return:
        """
        self.alpha = float(alpha)
        self.lm = Lasso(self.alpha, normalize=False)
        self.fit_model()
        self.prediction = self.predict()

    def coef(self):
        """
        Extracts the correlation coefficients from the Lasso regression model.
        :return: The correlation coefficients as an array.
        """
        coef = self.lm.fit(self.X, self.y).coef_
        return coef

    def display_coef(self):
        """
        Displays the correlation coefficients on a line graph.
        :return:
        """
        coef = np.array(self.coef())
        index = np.argwhere(self.columns == 'cvr')
        columns = np.delete(self.columns, index)
        plt.plot(range(len(columns)), coef)
        plt.xticks(range(len(columns)), columns, rotation=90)
        plt.ylabel('Coefficients')
        plt.show()


class RidgeRegressionModel(BasicModel):
    """
    Inherits BasicModel class, using the Ridge Regression model.
    """
    def __init__(self, data_frame, target_variable_col, split_size=0.3, alpha=0.1):
        super().__init__(data_frame, target_variable_col, Ridge(alpha, normalize=True), split_size)
        self.alpha = alpha
        self.fit_model()
        self.prediction = self.predict()

    def reset_alpha(self, alpha):
        """
        Enables the user to set the alpha parameter for model tuning.
        :param alpha: The alpha parameter value.
        :return:
        """
        self.alpha = float(alpha)
        self.lm = Ridge(self.alpha, normalize=True)
        self.fit_model()
        self.prediction = self.predict()


class RandomForestRegressionModel(BasicModel):
    """
    Inherits BasicModel class, using the Random Forest Regression model.
    """
    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        super().__init__(data_frame, target_variable_col, RandomForestRegressor(n_estimators=10, criterion='mse'), split_size)
        self.fit_model()
        self.prediction = self.predict()

    def feature_importance(self):
        """
        Generates the feature importance scores from the model.
        :return: A dataframe containing the feature importance scores.
        """
        index = np.argwhere(self.columns == 'cvr')
        columns = np.delete(self.columns, index)
        return pd.DataFrame(self.lm.feature_importances_,
                            index=columns,
                            columns=['importance']).sort_values('importance', ascending=False)


class GradientBoostingRegressionModel(BasicModel):
    """
    Inherits BasicModel class, using the Gradient Boosting Regression model.
    """
    def __init__(self, data_frame, target_variable_col, split_size=0.3):
        super().__init__(data_frame, target_variable_col, GradientBoostingRegressor(n_estimators=10, criterion='mse'))
        self.fit_model()
        self.prediction = self.predict()

    def feature_importance(self):
        """
        Generates the feature importance scores from the model.
        :return: A dataframe containing the feature importance scores.
        """
        index = np.argwhere(self.columns == 'cvr')
        columns = np.delete(self.columns, index)
        dataframe = pd.DataFrame(self.lm.feature_importances_,
                            index=columns,
                            columns=['importance']).sort_values('importance', ascending=False)
        return dataframe.round(6)
