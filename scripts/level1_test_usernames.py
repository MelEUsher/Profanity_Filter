import pandas as pd
import re

# Load profanity words
print("Loading profanity words...")
with open('data/profanity_words.txt', 'r') as f:
    profanity_words = [line.strip().lower() for line in f if line.strip()]

print(f"Loaded {len(profanity_words)} profanity words")
print()

# Create regex pattern (same as before)
pattern = r'\b(' + '|'.join(re.escape(word) for word in profanity_words) + r')\b'
print(f"Regex pattern: {pattern}")
print()

# Load Reddit usernames
print("Loading Reddit usernames dataset...")
df = pd.read_csv('data/reddit_usernames.csv')

# Use the correct column name from explore_usernames.py
username_column = 'author'

print(f"Dataset loaded: {len(df)} usernames")
print()

# Convert to lowercase and flag
df['username_lower'] = df[username_column].str.lower()
df['flagged'] = df['username_lower'].str.contains(pattern, regex=True, na=False)

# Get flagged usernames
flagged_usernames = df[df['flagged']]

# Calculate statistics
total_usernames = len(df)
total_flagged = len(flagged_usernames)
percentage_flagged = (total_flagged / total_usernames) * 100 if total_usernames > 0 else 0

# Print statistics
print("=" * 70)
print("STATISTICS:")
print("=" * 70)
print(f"Total usernames: {total_usernames:,}")
print(f"Flagged usernames: {total_flagged:,}")
print(f"Percentage flagged: {percentage_flagged:.4f}%")
print()

# Print first 30 flagged usernames
print("=" * 70)
print("FIRST 30 FLAGGED USERNAMES:")
print("=" * 70)
for idx, username in enumerate(flagged_usernames[username_column].head(30), 1):
    print(f"[{idx}] {username}")
print()

# Save flagged usernames to CSV
output_file = 'results/level1_flagged_usernames.csv'
flagged_usernames[[username_column, 'flagged']].to_csv(output_file, index=False)
print(f"✓ Saved {total_flagged:,} flagged usernames to {output_file}")
