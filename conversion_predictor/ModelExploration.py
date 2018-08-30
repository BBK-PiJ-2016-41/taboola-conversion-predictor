import cmd


class ModelExploration(cmd.Cmd):

    def __init__(self, regression_model):
        super(ModelExploration, self).__init__()
        self.model = regression_model

    def do_fit(self, arg=None):
        self.model.fit_model()

    def help_fit(self):
        print('Run this to fit the model.')
        if self.model.__class__.__name__ == 'LassoRegressionModel':
            print('This function will also print the coefficients.')

    def do_predict(self, arg=None):
        self.model.predict()

    def help_predict(self):
        print('Run this to train the model on the training data set.')

    def do_score(self, arg=None):
        self.model.score()

    def do_printscore(self, arg=None):
        self.model.print_score()

    def help_score(self):
        print('Outputs the score of the model.')

    def do_crossvalidation(self, folds=5):
        self.model.cross_validation_score(folds)

    def do_printcrossvalidation(self, folds=5):
        self.model.print_cross_val(folds)

    def help_crossvalidation(self):
        print('Outputs the cross-validated score of the model.'
              '\nYou have the option of specifying the number of folds (default 5).')

    def do_rootmeansquarederror(self, arg=None):
        self.model.root_mean_squared_error()

    def do_printrootmeansquared(self, arg=None):
        self.model.print_rsme()

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

    def do_EOF(self, line):
        return True
