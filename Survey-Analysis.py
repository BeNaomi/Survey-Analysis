# This script is used to analyze survey data.
import pandas as pd
import numpy as np


# Load the data
data = pd.read_csv('YourDataFile.csv')

# Display the first 5 rows of the data
print(df.head())

# create a list of labels for the groups: relevant to survey of between subjects, that each
# participant has answered a set of questionsrelated to only one label and left other columns na
labels = ['label1', 'label2', 'label3', 'label4']

# check column names
for label in labels:
    # Create a list of items for each label, excluding item 5, which is not relevant
    # for the analysis in this case
    items = [f'{label}_{i}' for i in range(1, 8) if i != 5]
    print(f"{label}:")
    print(items)

# Step 1: Compute average for each group, excluding item 5
for label in labels:
    items = [f'{label}_{i}' for i in range(1, 8) if i != 5]
    # Convert to numeric only for these columns
    data[items] = data[items].apply(pd.to_numeric, errors='coerce')
    data[f'{label}_avg'] = data[items].mean(axis=1)

# Step 2: Compute the average of the averages for each group

def assign_label(row):
    group_avgs = {label: row[f'{label}_avg'] for label in labels}
    # Filter out NaNs
    group_avgs = {k: v for k, v in group_avgs.items() if pd.notna(v)}
    if not group_avgs:
        return np.nan
    # Find the group with the maximum average
    return max(group_avgs, key=group_avgs.get)
# Assign the group based on the maximum average (others will be NaN)
data['Group'] = data.apply(assign_label, axis=1)

print(data['Group'].value_counts())
print(data[[f'{label}_avg' for label in labels] + ['Group']].head(10))


#create dependent var column
dv_items = ['DV1', 'DV2', 'DV3', 'DV4']

# Make sure all columns are numeric
# Ensure data types are numeric
data.loc[:, dv_items] = data[dv_items].apply(pd.to_numeric, errors='coerce')

# Calculate the DV mean
data.loc[:, 'DV'] = data[dv_items].mean(axis=1).round(2)

# Create the DV column
data['DV'] = data[dv_items].mean(axis=1)

# round the DV column to 2 decimal places
data['DV'] = data['DV'].round(2)

# descriptive statistics
data.groupby('Group')['DV'].agg(['mean', 'std', 'count']).round(2)

# plot of descriptive statistics
import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(x='Group', y='DV', data=data)
plt.title('DV by Group')
plt.show()

#ANOVA test
from scipy.stats import f_oneway

# Perform ANOVA
groups = [group['DV'].dropna() for name, group in data.groupby('Group')]
f_stat, p_val = f_oneway(*groups)

print(f"ANOVA result: F = {f_stat:.2f}, p = {p_val:.4f}")

#add moderator
import statsmodels.api as sm
from statsmodels.formula.api import ols

# include a ***Categorial*** moderator variable
modelCV = ols('DV ~ C(Group) * C(Moderator)', data=data).fit()

anova_table = sm.stats.anova_lm(modelCV, typ=2)
print(anova_table.round(4))
print(modelCV.summary())

# include a ***Continuous*** moderator variable
modelCC = ols('DV ~ C(Group) * ContinuousModerator', data=data).fit()

anova_tableCI = sm.stats.anova_lm(modelCC, typ=2)
print(anova_tableCC.round(4))
print(modelCC.summary())

