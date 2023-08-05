# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:20:22 2019

@author: padma
"""

from LogRegrWrapperClass import WrapperClass
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.utils.estimator_checks import check_estimator
from sklearn.model_selection import train_test_split

#initiate the logistic regression wrapper class
wo = WrapperClass(LogisticRegression, {'solver':'lbfgs'})

#read the csv file
df = pd.read_csv("../DR_Demo_Lending_Club_reduced.csv")

#preprocess data
X = wo.preprocess(df)
cols = [col for col in X.columns if col !='is_bad']
y = X['is_bad']
X = X[cols]

#split for train and validation
X_train, X_test, y_train , y_test = train_test_split(X, y, test_size = 0.05)
#fit the model
#wo.fit(X_train,y_train)

#fit the model
wo.fit(X,y)

print(wo.model)

print("predict_proba")
y_pred = wo.predict_proba(X)
print(y_pred)


y_pred = wo.predict(X)
print("predicted target")
print(y_pred)


print("evaluate")
res = wo.evaluate(X,y)
print(res)

print("tune parameters")
res = wo.tune_parameters(X, y)
print(res)
