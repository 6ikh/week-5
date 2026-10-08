import plotly.express as px
import pandas as pd

# update/add code below ...

# loading in the dataset while lowercasing the column names
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv').rename(columns=str.lower)


# function for demographic survival
def survival_demographics():
    """Calculates survival stats grouped by class, sex, and age bin"""
    # create age groups, last being infinte
    age_bins = [0, 12, 19, 59, float('inf')]
    # create age group labels
    age_labels = ['Child', 'Teenager', 'Adult', 'Senior']
    # create a new column for age groups
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)
    # convert the age_group column to a categorical type
    df['age_group'] = df['age_group'].astype('category')
    # group by pclass, sex, and age_group
    grouped = df.groupby(['pclass', 'sex', 'age_group']).agg(
        # calculate the number of passengers, survivors, and survival rate
        n_passengers=('survived', 'count'),
        n_survivors=('survived', 'sum'),
        survival_rate=('survived', 'mean')
    ).reset_index()
    # create a MultiIndex for all combinations of pclass, sex, and age_group
    all_combinations = pd.MultiIndex.from_product(
        [df['pclass'].unique(), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )
    # reindex the grouped DataFrame to include all combinations
    # #filling missing values with 0
    grouped = grouped.set_index(['pclass', 'sex', 'age_group']).reindex(all_combinations, fill_value=0).reset_index()
    # convert the age_group column to a categorical type
    grouped['age_group'] = pd.Categorical(grouped['age_group'], categories=age_labels, ordered=True)
    # sort the grouped DataFrame by pclass, sex, and age_group
    return grouped


# call function and print the first 10 rows of the grouped DataFrame
grouped = survival_demographics()
print(grouped.head(10))


# function for visualization
def visualize_demographic():
    """Generates Plotly bar chart comparing male survival rates across classes"""
    grouped = survival_demographics()
    # filter the grouped DataFrame to include only male passengers
    males = grouped[grouped['sex'] == 'male'].copy()
    males['survival_percent'] = males['survival_rate'] * 100
    # create a bar chart using Plotly Express
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
    # update the layout of the figure
    fig.update_layout(
        yaxis_title="Survival Rate (%)",
        legend_title="Passenger Class",
        yaxis_range=[0, 105]
    )

    return fig


# function to group by family size and passenger class
def family_groups():
    """Calculate passenger counts & fare stats by family size and class"""
    df_copy = df.copy()
    # create a new column for family size
    df_copy['family_size'] = df_copy['sibsp'] + df_copy['parch'] + 1
    # group by pclass and family_size
    # aggregating the number of passengers and fare stats
    grouped = df_copy.groupby(['pclass', 'family_size']).agg(
        n_passengers=('fare', 'count'),
        avg_fare=('fare', 'mean'),
        min_fare=('fare', 'min'),
        max_fare=('fare', 'max')
    ).reset_index()
    # sort the grouped DataFrame by pclass and family_size
    grouped = grouped.sort_values(by=['pclass', 'family_size']).reset_index(drop=True)

    return grouped
grouped = family_groups()

print(grouped)


# extract the last names from the 'name' column and count their occurrences
def last_names():
    """Extracts passenger last names and returns count"""
    extracted_last_names = df['name'].str.split(',').str[0].str.strip()
    return extracted_last_names.value_counts()

print(last_names())

# function to visualize average fare by family size and passenger class
def visualize_families():
    """ Generates Plotly bar chart comparing average fare by family size"""
    grouped = family_groups()
    # convert the 'pclass' column to string for better visualization
    grouped['plclass'] = grouped['pclass'].astype(str)

    fig = px.bar(
        grouped,
        x='family_size',
        y='avg_fare',
        color='pclass',
        barmode='group',
        category_orders={'pclass': ['1', '2', '3']},
        labels={
            'family_size': 'Family Size',
            'avg_fare': 'Average Fare ($)',
            'pclass': 'Passenger Class'
        },
        title='Average Ticket Fare Comparison by Family Size Across Passenger Classes',
        text_auto='.1f'
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis_title='Average Fare ($)',
        legend_title='Passenger Class'
    )

    return fig

