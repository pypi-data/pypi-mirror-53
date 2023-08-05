from setuptools import setup

setup(name='LogRegrWrapperClass',
      version='0.2',
      description='Take home test Logistic Regression Wrapper class',
      url='http://github.com/padvyas/LogRegrWrapperClass',
      author='Padmapriya S',
      author_email='padmapriya.sethuraman@gmail.com',
      license='MIT',
      packages=['LogRegrWrapperClass'],
	  package_data={'LogRegrWrapperClass': ['*,txt','*.csv','license.txt']},
	  include_package_data=True,
      install_requires=[],
      zip_safe=False)