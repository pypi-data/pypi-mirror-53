# Logistic Regression wrapper class for takehome test Padmapriya Sethuraman- Machine Learning Engineer

Unit test requirements:
=======================

Unit tests to verify if return format(for functions that return dict), model reproducibility,
missing values are complete and are working fine.

One hot encoding is used for categorical variables as of now
new category level is not being supported by this class.

Certain tree based algorithm and model can handle missing values
and new categories at prediction time.
For logistic regression one preprocessing step than can be followed
is combine train and test data to define category levels and split them
as train and test before fitting the model.

Unit tests to be written for testing input formats and ouput formats and 
accuracy of functions, models and predictions.

Comprehensive Test to be written for LogisticRegression options and different size of datasets and features

I would also add exception handling and logging to the class and unit test files.

PEP 8 format:
============

Used autopep8 on files and verified the class file and unit test files are in pep8 format using pydocstyle

pep8 --first LogRegrWrapperClass.py
C:\ProgramData\Anaconda3\lib\site-packages\pep8.py:2124: UserWarning:

pep8 has been renamed to pycodestyle (GitHub issue #466)
Use of the pep8 tool will be removed in a future release.
Please install and use `pycodestyle` instead.

$ pip install pycodestyle
$ pycodestyle ...
  '\n\n'
  
Verified that the binary classification Wrapper class is working for input file DR_Demo_Lending_Club_reduced.csv

Package installation:
=====================

The package can be installed using pip (the archive is uploaded to pypi)

A basic archive is created
Requirement.txt file with all required package is not created

The packages to be installed are
category_encoders
scikit-learn
numpy
pandas
seaborn (to load titanic dataset to run unit tests)

Answers to Short Answer Response questions are in file "Short Answer Portion Response_Padmapriya_S.txt" and is also given below
============================================
#Response for short answer portion - DataRobot Machine learning take home test
#Response written by Padmapriya Sethuraman on 9/29/2019


Your models have been implemented and customers are now using them in production.
1. Imagine the credit risk use case above. You have two models: a logistic regression
model with an F1-score of 0.60 and a neural network with an F1-score of 0.63. Which
model would you recommend for the bank and why?

I would recommend the logistic regression model with F1-score 0.60.
Given 2 models with closer score I would always prefer a model that 
can be explained better, especially for bank where there are regulations around explanation
on how a decision was made. Logistic regression model can be better explained in business terms
than a complex neural network model that is hard to explain in business terms.

2. A customer wants to know which features matter for their dataset. They have several
models created in the DataRobot platform such as random forest, linear regression, and
neural network regressor. They also are pretty good at coding in Python so wouldn't
mind using another library or function. How do you suggest this customer gets feature
importance for their data?

I would recommend Xgboost to get the feature importance. Since customer has good Python skills Xgboost has 
handy functions to get feature importance and plot the same.

Feature importance can be obtained from existing random forest model, Linear regression models as well, but
demands statistical skills to know how the pvalues and other statistical parameters are indicative of feature importance.
For example for linear regression one has to have a good knowledge about selecting features based on what contributes to 
the model best without introducing multi collinearity.