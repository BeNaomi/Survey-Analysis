# This script is used to analyze survey data.
import sys
import os
import pandas as pd 
import numpy as np
import statsmodels.api as sm

# Load the data
df = pd.read_csv('location/FileName.csv')

# Display the first 5 rows of the data
print(df.head())

# Print the data type of each column
print(df.dtypes)

#clean N/A
df = df.dropna()

# Take a look at the data
print(df.describe())

 # Check the number of NaN values in each column
 # This will become handy when we want to compare columns and need to ensure 
 # that we have the same number of rows in each column

 print(df.isna().sum()) 

#calculate correlation between two columns

correlation = df['Column1'].corr(df['Column2'])
print("Correlation:", correlation)

#calculate the mean of a column
MeanColumn = df['Column1'].mean()

#create a new column: interaction between two columns
df['Interaction'] = df['Column1'] * df['Column2']

# define the independent variable
X = df['Column1']

# define the dependent variable
Y = df['Column2']

# Fit the regression model
X = sm.OLS(Y, X).fit()

# Print the summary of the model
print(model.summary())


