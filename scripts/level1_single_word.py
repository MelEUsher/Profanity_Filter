import pandas as pd

# Load the GameTox dataset (CSV format, NOT TSV)
df = pd.read_csv('data/gametox.csv')

# Use the correct column name: 'message' (not 'text')
text_column = 'message'
label_column = 'label'

# Convert to lowercase for matching
df['text_lower'] = df[text_column].str.lower()

# Find messages containing "damn"
contains_damn = df['text_lower'].str.contains('damn', na=False)
flagged_messages = df[contains_damn]

# Print examples
print("=" * 50)
print("EXAMPLES OF MESSAGES WITH 'damn':")
print("=" * 50)
print()

# Show first 20 flagged messages
for idx, message in enumerate(flagged_messages[text_column].head(20), 1):
    print(f"[Message {idx}] {message}")
    print()

# Calculate statistics
total_messages = len(df)
total_flagged = len(flagged_messages)
percentage_flagged = (total_flagged / total_messages) * 100

# Calculate correct flags vs false positives
correct_flags = len(flagged_messages[flagged_messages[label_column] == 1.0])
false_positives = len(flagged_messages[flagged_messages[label_column] == 0.0])

# Print statistics
print("=" * 50)
print("STATISTICS:")
print("=" * 50)
print(f"Total messages in dataset: {total_messages}")
print(f"Messages containing 'damn': {total_flagged}")
print(f"Percentage flagged: {percentage_flagged:.2f}%")
print(f"Correct flags (actually toxic): {correct_flags}")
print(f"Incorrect flags (false positives): {false_positives}")
