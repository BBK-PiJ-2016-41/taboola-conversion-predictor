import cmd


class ModelExploration(cmd.Cmd):
    """
    A class to enable exploration of the regression models.. Inherits from Cmd package.
    """

    def __init__(self, regression_model):
        """
        Constructor for the ModelExploration class.
        :param data_visualiser: the model providing the functionality
        """
        super(ModelExploration, self).__init__()
        self.model = regression_model

    def do_score(self, arg=None):
        """
        Calls the score method on the model.
        :param arg:
        """
        self.model.score()

    def do_printscore(self, arg=None):
        """
        Calls the print_score method on the model.
        :param arg:
        """
        self.model.print_score()

    def help_score(self):
        """
        Explains the score method to the user.
        """
        print('Outputs the score of the model.')

    def do_crossvalidation(self, folds):
        """
        Calls the cross_validation method on the model.
        :param folds: the number of folds
        """
        try:
            self.model.cross_validation_score(int(folds))
        except ValueError:
            print('Please include the number of folds.')

    def do_printcrossvalidation(self, folds):
        """
        Calls the print_cross_val method on the model.
        :param folds: the number of folds
        """
        try:
            self.model.print_cross_val(int(folds))
        except ValueError:
            print('Please include the number of folds.')

    def help_crossvalidation(self):
        """
        Explains the cross-validation method to the user.
        """
        print('Outputs the cross-validated score of the model.'
              '\nPlease specify the number of folds.')

    def do_rootmeansquarederror(self, arg=None):
        self.model.root_mean_squared_error()

    def do_printrootmeansquared(self, arg=None):
        self.model.print_rmse()

    def help_rootmeansquarederror(self):
        """
        Explains the root mean squared method to the user.
        """
        print('Outputs the root mean squared error of the model.')

    def do_alpha(self, alpha, arg=None):
        """
        Resets the alpha parameter for Ridge and Lasso.
        :param alpha: The new value for the alpha parameter
        :param arg:
        """
        if self.model.__class__.__name__ != 'LinearRegressionModel':
            self.model.reset_alpha(alpha)
        else:
            print('Linear regression model does not take an alpha parameter.')

    def help_alpha(self):
        """
        Explains the alpha method to the user.
        """
        print('Enter a new alpha parameter to tune Lasso and Ridge regression models.'
              '\nThis method is not available for Linear models.')

    def do_lassodisplay(self, arg=None):
        """
        Outputs the coefficient display for Lasso.
        :param arg:
        :return:
        """
        if self.model.__class__.__name__ != 'LassoRegressionModel':
            print('Only LASSO regression can use this feature.')
        else:
            self.model.display_coef()

    def help_lassodisplay(self):
        """
        Explains the lasso display method to the user.
        """
        print('Displays LASSO coefficient graph.')

    def do_featuredisplay(self, arg=None):
        """
        Outputs the feature coefficients from Random Forest and Gradient Boosting
        :param arg:
        """
        model_type = self.model.__class__.__name__
        if model_type == 'RandomForestRegressionModel' or model_type == 'GradientBoostingRegressionModel':
            print(self.model.feature_importance())
        else:
            print('Only Random Forest and Gradient Boosting regression can use this feature.')

    def help_featuredisplay(self):
        """
        Explains the feature display method to the user.
        """
        print('Displays feature importance for Random Forest and Gradient Boosting.')

    def do_EOF(self, line):
        """
        Closes the Cmd-based interface and moves onto the next stage of the application.
        :param line:
        :return: True
        """
        return True
