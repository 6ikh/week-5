import plotly.express as px
import pandas as pd

# update/add code below ...

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv').rename(columns=str.lower)

# 1
def survival_demographics():
    age_bins = [0, 12, 19, 59, float('inf')]
    age_labels = ['Child', 'Teenager', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)
    df['age_group'] = df['age_group'].astype('category')

# 2&3
    grouped = df.groupby(['pclass', 'sex', 'age_group']).agg(
        n_passengers=('survived', 'count'),
        n_survivors=('survived', 'sum'),
        survival_rate=('survived', 'mean')
    ).reset_index()

    all_combinations = pd.MultiIndex.from_product(
        [df['pclass'].unique(), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )
    grouped = grouped.set_index(['pclass', 'sex', 'age_group']).reindex(all_combinations, fill_value=0).reset_index()
    grouped['age_group'] = pd.Categorical(grouped['age_group'], categories=age_labels, ordered=True)

    return grouped

grouped = survival_demographics()

print(grouped.head(10))

def visualize_demographic():
    grouped = survival_demographics()

    males = grouped[grouped['sex'] == 'male'].copy()
    males['survival_percent'] = males['survival_rate'] * 100

    fig = px.bar(
        males,
        x="age_group",
        y="survival_percent",
        color="pclass",
        barmode="group",
        category_orders={"age_group": ["Child", "Teenager", "Adult", "Senior"]},
        labels={
            "survival_percent": "Survival Rate (%)",
            "age_group": "Age Group",
            "pclass": "Passenger Class"
        },
        title="Male Survival Rates Across Passenger Classes",
        text_auto=".1f"
    )

    fig.update_layout(
        yaxis_title="Survival Rate (%)",
        legend_title="Passenger Class",
        yaxis_range=[0, 105]
    )

    return fig