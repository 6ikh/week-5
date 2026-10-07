import plotly.express as px
import pandas as pd

# update/add code below ...

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv').rename(columns=str.lower)

df.head(5)

# 1
def survival_demographics():
    age_bins = [0, 12, 19, 59, float('inf')]
    age_labels = ['Child', 'Teenager', 'Adult', 'Senior']
    df['AgeCategory'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)

survival_demographics()

print(df[['age', 'AgeCategory']].head(10))

# 2&3
grouped = df.groupby(['pclass', 'sex', 'AgeCategory']).agg(
    n_passengers=('survived', 'count'),
    n_survivors=('survived', 'sum'),
    survival_rate=('survived', 'mean')
).reset_index()

print(grouped.head(10))