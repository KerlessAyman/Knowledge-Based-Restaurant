import pandas as pd
df = pd.read_csv('zomato.csv', encoding='latin-1')
# Drop unnecessary columns
df.drop(columns=[
    'Restaurant ID',
    'Country Code',
    'Address',
    'Locality Verbose',
    'Switch to order menu',
    'Rating color',
    'Rating text'
], inplace=True, errors='ignore')

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing important info (note the correct column names)
df.dropna(subset=['Cuisines', 'Locality', 'Average Cost for two', 'Aggregate rating'], inplace=True)
# Normalize cuisine text
df['Cuisines'] = df['Cuisines'].str.lower().str.strip()

df['Cuisines'] = df['Cuisines'].str.replace('chinese food', 'chinese', regex=False)
df['Cuisines'] = df['Cuisines'].str.replace('italian cuisine', 'italian', regex=False)
df['Cuisines'] = df['Cuisines'].str.replace('north indian', 'indian', regex=False)
df['Cuisines'] = df['Cuisines'].str.replace('south indian', 'indian', regex=False)
df['Aggregate rating'] = pd.to_numeric(df['Aggregate rating'], errors='coerce')