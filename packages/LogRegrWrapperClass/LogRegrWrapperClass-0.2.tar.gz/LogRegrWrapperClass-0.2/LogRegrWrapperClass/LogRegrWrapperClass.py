# Class written by Padmapriya Sethuraman on Sep 29 2019
from sklearn.base import BaseEstimator, ClassifierMixin
from functools import lru_cache
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, log_loss
from sklearn.model_selection import KFold, cross_val_score
import category_encoders as ce

'''
this is a module containing classes which wraps a classifier estimator

'''


class WrapperClass(BaseEstimator, ClassifierMixin):
    def __init__(self, base_estimator=LogisticRegression,
                 estimator_params=None):
        super().__init__()
        self.base_estimator = base_estimator
        self.estimator_params = estimator_params
        self.encoder = ce.OneHotEncoder()

    def fit(self, x, y):
        self.model = self._make_estimator().fit(x, y)

    def _make_estimator(self):
        """Make and configure a copy of the `base_estimator_` attribute.
        Warning: This method should be used to properly instantiate new
        sub-estimators. taken from sklearn github
        """
        estimator = self.base_estimator()
        if(self.estimator_params is not None):
            estimator.set_params(**self.estimator_params)
        return estimator

    def predict(self, x):
        y = self.model.predict(x)
        return(y)

    def predict_proba(self, x):
        y_prob = self.model.predict_proba(x)
        return(y_prob)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X)
        f1 = f1_score(y, y_pred, average='micro')
        ll = log_loss(y, y_pred)
        res = {'f1_score': f1, 'logloss': ll}
        return(res)

    def tune_parameters(self, X, y):
        # https://scikit-learn.org/stable/tutorial/statistical_inference/model_selection.html
        clf = self._make_estimator().fit(X, y)
        tol = clf.get_params()['tol']
        fit_intercept = clf.get_params()['fit_intercept']
        solver = clf.get_params()['solver']
        k_fold = KFold(n_splits=5)
        f1 = cross_val_score(clf, X, y, cv=k_fold, scoring='f1_micro')
        ll = cross_val_score(clf, X, y, cv=k_fold,
                             scoring='neg_log_loss')

        res = {'tol': tol, 'fit_intercept': fit_intercept, 'solver': solver,
               'scores': {'f1_score': np.mean(f1), 'logloss': np.mean(ll)}}
        return(res)

    def preprocess(self, X):

        # handle missing data
        # We can asks for input (options based on drop down box in front end)
        # on how do we want to handle missing values, like replace with default
        # value, mean value imputation and handle missing values for each
        # columns or sets of columns that needs similar transform
        # for the purpose of this take home test all missing values are handled
        # by dropping the row with NAs

        # We can get input on whether a categorical column is ordinal
        # or nominal and perform label encoding or one hot encoding accordingly
        # For the purpose of this take home test it is assumed that all
        # categorical variables are ordinal and will perform one hot encoding
        # dataset has '?' in it, convert these into NaN

        X = X.replace('?', np.nan)
        #drop columns with more than 90% NAS
        
        X = X[X.columns[X.isnull().mean() <= 0.9]]
        # drop the NaN
        X = X.dropna(axis=0, how="any")
        X = self.encoder.fit_transform(X)
        return(X)
