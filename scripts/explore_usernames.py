import pandas as pd

# Load the usernames
df = pd.read_csv('data/reddit_usernames.csv')

# Show first 10 usernames
print("First 10 usernames:")
print(df.head(10))

# Show total count
print(f"\nTotal usernames: {len(df)}")

# Show a random sample
print("\nRandom sample of 10 usernames:")
print(df.sample(10))
