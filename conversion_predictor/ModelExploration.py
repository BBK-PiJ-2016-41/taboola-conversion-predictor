import cmd


class ModelExploration(cmd.Cmd):

    def __init__(self, regression_model):
        super(ModelExploration, self).__init__()
        self.model = regression_model

    def do_score(self, arg=None):
        self.model.score()

    def do_printscore(self, arg=None):
        self.model.print_score()

    def help_score(self):
        print('Outputs the score of the model.')

    def do_crossvalidation(self, folds):
        try:
            self.model.cross_validation_score(int(folds))
        except ValueError:
            print('Please include the number of folds.')

    def do_printcrossvalidation(self, folds):
        try:
            self.model.print_cross_val(int(folds))
        except ValueError:
            print('Please include the number of folds.')

    def help_crossvalidation(self):
        print('Outputs the cross-validated score of the model.'
              '\nPlease specify the number of folds.')

    def do_rootmeansquarederror(self, arg=None):
        self.model.root_mean_squared_error()

    def do_printrootmeansquared(self, arg=None):
        self.model.print_rmse()

    def help_rootmeansquarederror(self):
        print('Outputs the root mean squared error of the model.')

    def do_alpha(self, alpha, arg=None):
        if self.model.__class__.__name__ != 'LinearRegressionModel':
            self.model.reset_alpha(alpha)
        else:
            print('Linear regression model does not take an alpha parameter.')

    def help_alpha(self):
        print('Enter a new alpha parameter to tune Lasso and Ridge regression models.'
              '\nThis method is not available for Linear models.')

    def do_lassodisplay(self, arg=None):
        if self.model.__class__.__name__ != 'LassoRegressionModel':
            print('Only LASSO regression can use this feature.')
        else:
            self.model.display_coef()

    def help_lassodisplay(self):
        print('Displays LASSO coefficient graph.')

    def do_featuredisplay(self, arg=None):
        model_type = self.model.__class__.__name__
        if model_type == 'RandomForestRegressionModel' or model_type == 'GradientBoostingRegressionModel':
            print(self.model.feature_importance())
        else:
            print('Only Random Forest and Gradient Boosting regression can use this feature.')

    def help_featuredisplay(self):
        print('Displays feature importance for Random Forest and Gradient Boosting.')

    def do_EOF(self, line):
        return True
