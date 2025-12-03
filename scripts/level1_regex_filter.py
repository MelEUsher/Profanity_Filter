import pandas as pd
import re

# Load profanity words
print("Loading profanity words...")
with open('data/profanity_words.txt', 'r') as f:
    profanity_words = [line.strip().lower() for line in f if line.strip()]

print(f"Loaded {len(profanity_words)} profanity words:")
print(profanity_words)
print()

# Create regex pattern with word boundaries
pattern = r'\b(' + '|'.join(re.escape(word) for word in profanity_words) + r')\b'
print(f"Regex pattern: {pattern}")
print()

# Load GameTox dataset (CSV, not TSV!)
print("Loading GameTox dataset...")
df = pd.read_csv('data/gametox.csv')

# Use correct column names
text_column = 'message'
label_column = 'label'

# Convert to lowercase and flag
df['text_lower'] = df[text_column].str.lower()
df['flagged'] = df['text_lower'].str.contains(pattern, regex=True, na=False)

# Get flagged messages
flagged_messages = df[df['flagged']]

# Print examples of flagged messages
print("=" * 70)
print("EXAMPLES OF FLAGGED MESSAGES (15 samples):")
print("=" * 70)
for idx, row in enumerate(flagged_messages.head(15).itertuples(), 1):
    message = getattr(row, text_column)
    label = getattr(row, label_column)
    label_str = "TOXIC" if label == 1.0 else "CLEAN"
    print(f"[{idx}] ({label_str}) {message}")
print()

# Calculate confusion matrix metrics
# True Positive: flagged AND toxic (label == 1.0)
# False Positive: flagged AND clean (label == 0.0)
# True Negative: not flagged AND clean (label == 0.0)
# False Negative: not flagged AND toxic (label == 1.0)

true_positives = len(df[(df['flagged'] == True) & (df[label_column] == 1.0)])
false_positives = len(df[(df['flagged'] == True) & (df[label_column] == 0.0)])
true_negatives = len(df[(df['flagged'] == False) & (df[label_column] == 0.0)])
false_negatives = len(df[(df['flagged'] == False) & (df[label_column] == 1.0)])

total_messages = len(df)
total_flagged = len(flagged_messages)

# Calculate metrics
accuracy = (true_positives + true_negatives) / total_messages if total_messages > 0 else 0
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

# Print metrics
print("=" * 70)
print("METRICS:")
print("=" * 70)
print(f"Total messages in dataset: {total_messages}")
print(f"Total messages flagged: {total_flagged}")
print(f"Percentage flagged: {(total_flagged / total_messages * 100):.2f}%")
print()
print("Confusion Matrix:")
print(f"  True Positives (flagged & toxic):     {true_positives}")
print(f"  False Positives (flagged & clean):    {false_positives}")
print(f"  True Negatives (not flagged & clean): {true_negatives}")
print(f"  False Negatives (not flagged & toxic): {false_negatives}")
print()
print("Performance Metrics:")
print(f"  Accuracy:  {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"  Precision: {precision:.4f} ({precision * 100:.2f}%)")
print(f"  Recall:    {recall:.4f} ({recall * 100:.2f}%)")
print()

# Print examples of false positives
false_positive_messages = df[(df['flagged'] == True) & (df[label_column] == 0.0)]
print("=" * 70)
print("EXAMPLES OF FALSE POSITIVES (10 samples):")
print("=" * 70)
for idx, message in enumerate(false_positive_messages[text_column].head(10), 1):
    print(f"[{idx}] {message}")
print()

# Save flagged messages to CSV
output_file = 'results/level1_flagged_messages.csv'
flagged_messages[[text_column, label_column, 'flagged']].to_csv(output_file, index=False)
print(f"✓ Saved {len(flagged_messages)} flagged messages to {output_file}")
