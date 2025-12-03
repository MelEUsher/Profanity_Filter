import pandas as pd

# Load the dataset (note: it's CSV not TSV)
df = pd.read_csv('data/gametox.csv')

# Show first 5 rows
print("First 5 messages:")
print(df.head())

# Show how many messages we have
print(f"\nTotal messages: {len(df)}")

# Show column names
print(f"\nColumns: {df.columns.tolist()}")
