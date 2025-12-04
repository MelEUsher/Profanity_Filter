"""
Create a balanced 50-message sample from the GameTox dataset.
This sample will be used for LLM-based profanity classification testing.
"""

import pandas as pd

def create_balanced_sample():
    """
    Create a balanced sample of 50 messages (25 toxic, 25 clean) from GameTox dataset.
    """

    # Load the full dataset
    print("Loading GameTox dataset...")
    df = pd.read_csv("data/gametox.csv")

    print(f"Total messages in dataset: {len(df)}")
    print()

    # Filter toxic and clean messages
    toxic_messages = df[df['label'] == 1.0]
    clean_messages = df[df['label'] == 0.0]

    # Sample 25 from each category with fixed random state for reproducibility
    toxic_sample = toxic_messages.sample(n=25, random_state=42)
    clean_sample = clean_messages.sample(n=25, random_state=42)

    # Combine and shuffle
    sample = pd.concat([toxic_sample, clean_sample])
    sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save the sample
    output_path = "data/gametox_sample_50.csv"
    sample.to_csv(output_path, index=False)

    # Print summary
    print(f"Selected sample: {len(sample)} messages")
    print(f"  - Toxic: {len(sample[sample['label'] == 1.0])}")
    print(f"  - Clean: {len(sample[sample['label'] == 0.0])}")
    print()
    print(f"Sample saved to: {output_path}")
    print()

    # Show first 5 examples
    print("First 5 messages in sample:")
    for idx, row in sample.head(5).iterrows():
        label_str = "TOXIC" if row['label'] == 1.0 else "CLEAN"
        print(f"[{label_str}] {row['message']}")

if __name__ == "__main__":
    create_balanced_sample()
