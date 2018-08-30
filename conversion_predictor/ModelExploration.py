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

    def help_score(self):
        print('Outputs the score of the model.')

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
