import unittest
from LogRegrWrapperClass import WrapperClass
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.utils.estimator_checks import check_estimator
from schema import Schema, And, Use, Optional
import seaborn as sns


class Test(unittest.TestCase):
    wo = WrapperClass(LogisticRegression, {'solver':'lbfgs'})    
    titanic = sns.load_dataset('titanic')
    X = wo.preprocess(titanic)
    cols = [col for col in X.columns if col !='survived']
    y = X['survived']
    X = X[cols]
    
    # tests to check if the model is reproducable w.r.t default parameters
    def test_model_reproducable_params(self):
        self.wo.fit(self.X, self.y)
        log_reg = LogisticRegression()
        log_reg.set_params(solver='lbfgs')
        model =  log_reg.fit(self.X, self.y)
        y_local = model.predict(self.X)
        y_pred = self.wo.model.predict(self.X)
        self.assertEqual(model.get_params(),self.wo.model.get_params())
 
    # tests to check if the model is reproducable w.r.t predictions
    def test_model_reproducable_predictions(self):
        self.wo.fit(self.X, self.y)
        log_reg = LogisticRegression()
        model =  log_reg.fit(self.X, self.y)
        y_local = model.predict(self.X)
        y_pred = self.wo.model.predict(self.X)
        self.assertTrue(np.array_equal(y_local,y_pred))
        
    
    # Test to handle missing values
    # handled missing values in separate function to preprocess the dataset
    # Have not used pipelines to transform and fit.
    def test_handle_missing_values(self):
        df =self.titanic
        #df = self.wo.preprocess(df)
        is_na_flag = df.isna().sum().sum()
        if is_na_flag > 0:
            is_na_flag = True
        else:
            is_na_flag = False
        print(is_na_flag)
        test_flag = False
        if (is_na_flag):
            df = self.wo.preprocess(df)
            cols = [col for col in df.columns if col !='survived']
            y = df['survived']
            df = df[cols]
            self.wo.fit(df,y)
            test_flag = True
        self.assertEqual((test_flag and is_na_flag) or (not test_flag and not is_na_flag),1)
        
#    # Can handle new category levels at prediction time
#    def test_handle_new_cat_levels_predtime(self):
#        df = self.titanic
#        #Filter Queenstown from embark_town and introduce the category during 
#        #predict time to test if new category levels are handled during 
#        #prediction time
#        df1 = df[df.embark_town.isin(['Southampton','Cherbourg'])]
#        df1 = self.wo.preprocess(df1)
#        cols = [col for col in df1.columns if col !='survived']
#        y = df1['survived']
#        df1 = df1[cols]
#        self.wo.fit(df1,y)
#        df = df.dropna(axis=0, how="any")
#        df = self.wo.encoder.fit_transform(df)
#        y_pred = self.wo.model.predict(df)
#        if(y_pred.length() >0):
#            flag = True
#        else:
#            flag = False
#        self.assertTrue(flag)
#        
#        
    # Tests to check if the model functions returns result in the expected 
    # format
    def test_return_format_tp(self):
        res_tp = self.wo.tune_parameters(self.X,self.y)
        schema = Schema({'tol': And(float), 'fit_intercept': And(bool), 'solver': And(str),
               'scores': {'f1_score': And(float), 'logloss': And(float)}})
        validated = schema.is_valid(res_tp)
        self.assertTrue(validated)
    
    def test_return_format_eval(self):
        res_eval = self.wo.evaluate(self.X,self.y)
        schema = Schema({'f1_score': And(float), 'logloss': And(float)})
        validated = schema.is_valid(res_eval)
        self.assertTrue(validated)


if __name__ == '__main__':
    unittest.main()