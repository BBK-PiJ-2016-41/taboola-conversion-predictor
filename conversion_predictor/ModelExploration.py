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
        self.model.cross_validation_score(int(folds))

    def do_printcrossvalidation(self, folds):
        self.model.print_cross_val(int(folds))

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
            print('Only LASSO regression model has a visual display.')
        else:
            self.model.display_coef()

    def help_lassodisplay(self):
        print('Displays LASSO coefficient graph.')

    def do_EOF(self, line):
        return True
