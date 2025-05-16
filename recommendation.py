from data_processing import *
import pandas as pd

def cost_bucket(x):
    if x < 300:
        return 'Low'
    elif x <= 700:
        return 'Medium'
    else:
        return 'High'

df['cost_category'] = df['Average Cost for two'].apply(cost_bucket)

df['primary_cuisine'] = df['Cuisines'].apply(lambda x: x.split(',')[0].strip() if pd.notnull(x) else x)

def filter_and_rank(user_cuisine, user_budget, user_location, top_n=10):
    filtered = df[
        df['primary_cuisine'].str.contains(user_cuisine.lower(), na=False) &
        (df['cost_category'] == user_budget) &
        (df['Locality'].str.contains(user_location, case=False, na=False))  # or 'City'
    ].copy()

    filtered['score'] = (
        filtered['Aggregate rating'].fillna(0) * 0.7 +
        (filtered['Votes'].fillna(0) / filtered['Votes'].max()) * 0.3
    )

    filtered = filtered.sort_values(by='score', ascending=False).head(top_n)
    return filtered

def explain(row):
    return f"Matched on {row['primary_cuisine']} cuisine and {row['Currency']} {row['Average Cost for two']} budget with {row['Aggregate rating']} rating"
