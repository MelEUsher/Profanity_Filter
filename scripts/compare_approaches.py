#!/usr/bin/env python3
"""
Compare Regex (Level 1) vs LLM (Level 2) profanity filtering approaches.

This script:
1. Loads the same 50-message sample used for LLM testing
2. Applies regex-based filtering using the profanity wordlist
3. Compares regex predictions vs LLM predictions
4. Calculates metrics for both approaches
5. Identifies and analyzes disagreements
6. Saves comprehensive comparison results
"""

import pandas as pd
import re
from pathlib import Path


def load_profanity_words(filepath):
    """Load profanity words from file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip()]
    return words


def regex_filter(text, profanity_words):
    """
    Apply regex-based profanity filter.

    Returns 1 (toxic) if any profanity word found, 0 (clean) otherwise.
    Uses word boundary matching to avoid partial word matches.
    """
    if pd.isna(text):
        return 0

    text_lower = text.lower()

    # Check each profanity word
    for word in profanity_words:
        # Create pattern with word boundaries
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower):
            return 1

    return 0


def calculate_metrics(y_true, y_pred):
    """Calculate classification metrics."""
    # Convert to binary
    y_true = [int(y) for y in y_true]
    y_pred = [int(y) for y in y_pred]

    # Calculate confusion matrix
    tp = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 1)
    fp = sum(1 for true, pred in zip(y_true, y_pred) if true == 0 and pred == 1)
    tn = sum(1 for true, pred in zip(y_true, y_pred) if true == 0 and pred == 0)
    fn = sum(1 for true, pred in zip(y_true, y_pred) if true == 1 and pred == 0)

    # Calculate metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn
    }


def determine_winner(regex_value, llm_value):
    """Determine which approach performed better for a metric."""
    if abs(regex_value - llm_value) < 0.001:
        return "Tie"
    return "Regex" if regex_value > llm_value else "LLM"


def main():
    # Define file paths
    sample_file = Path('data/gametox_sample_50.csv')
    llm_predictions_file = Path('results/level2_llm_predictions.csv')
    profanity_words_file = Path('data/profanity_words.txt')
    output_file = Path('results/level1_vs_level2_comparison.csv')

    print("=" * 70)
    print("REGEX vs LLM PROFANITY FILTER COMPARISON")
    print("=" * 70)
    print()

    # Load data
    print("Loading data files...")
    df_sample = pd.read_csv(sample_file)
    df_llm = pd.read_csv(llm_predictions_file)
    profanity_words = load_profanity_words(profanity_words_file)

    print(f"  ✓ Loaded {len(df_sample)} messages from sample")
    print(f"  ✓ Loaded {len(df_llm)} LLM predictions")
    print(f"  ✓ Loaded {len(profanity_words)} profanity words")
    print()

    # Apply regex filter to the same 50 messages
    print("Applying regex filter to messages...")
    df_sample['regex_prediction'] = df_sample['message'].apply(
        lambda x: regex_filter(x, profanity_words)
    )
    print("  ✓ Regex filtering complete")
    print()

    # Merge with LLM predictions
    df_comparison = df_sample.copy()
    df_comparison['llm_prediction'] = df_llm['llm_prediction']

    # Convert labels to integers for consistency
    df_comparison['actual_label'] = df_comparison['label'].astype(int)

    # Calculate metrics for both approaches
    print("=" * 70)
    print("METRICS COMPARISON (Same 50 Messages)")
    print("=" * 70)

    regex_metrics = calculate_metrics(
        df_comparison['actual_label'],
        df_comparison['regex_prediction']
    )

    llm_metrics = calculate_metrics(
        df_comparison['actual_label'],
        df_comparison['llm_prediction']
    )

    # Print comparison table
    print(f"{'Metric':<20} {'Regex':<15} {'LLM':<15} {'Winner':<10}")
    print("-" * 70)

    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        regex_val = regex_metrics[metric]
        llm_val = llm_metrics[metric]
        winner = determine_winner(regex_val, llm_val)
        print(f"{metric.capitalize():<20} {regex_val:<15.3f} {llm_val:<15.3f} {winner:<10}")

    print()
    print("=" * 70)
    print("CONFUSION MATRICES")
    print("=" * 70)
    print()
    print("Regex:")
    print(f"  True Positives:  {regex_metrics['tp']:<3}  False Positives: {regex_metrics['fp']}")
    print(f"  False Negatives: {regex_metrics['fn']:<3}  True Negatives:  {regex_metrics['tn']}")
    print()
    print("LLM:")
    print(f"  True Positives:  {llm_metrics['tp']:<3}  False Positives: {llm_metrics['fp']}")
    print(f"  False Negatives: {llm_metrics['fn']:<3}  True Negatives:  {llm_metrics['tn']}")
    print()

    # Find disagreements
    df_comparison['disagree'] = (
        df_comparison['regex_prediction'] != df_comparison['llm_prediction']
    )
    disagreements = df_comparison[df_comparison['disagree']]

    print("=" * 70)
    print(f"DISAGREEMENTS: {len(disagreements)} messages where they differed")
    print("=" * 70)
    print()

    # Categorize disagreements
    for idx, row in disagreements.iterrows():
        message = row['message']
        actual = 'TOXIC' if row['actual_label'] == 1 else 'CLEAN'
        regex_pred = 'TOXIC' if row['regex_prediction'] == 1 else 'CLEAN'
        llm_pred = 'TOXIC' if row['llm_prediction'] == 1 else 'CLEAN'

        regex_correct = row['regex_prediction'] == row['actual_label']
        llm_correct = row['llm_prediction'] == row['actual_label']

        regex_mark = '✓' if regex_correct else '✗'
        llm_mark = '✓' if llm_correct else '✗'

        print(f'Message: "{message}"')
        print(f"  Actual:   {actual}")
        print(f"  Regex:    {regex_pred} {regex_mark}")
        print(f"  LLM:      {llm_pred} {llm_mark}")

        if regex_correct and not llm_correct:
            print(f"  → Regex was correct, LLM was wrong")
        elif llm_correct and not regex_correct:
            print(f"  → LLM was correct, Regex was wrong")
        else:
            print(f"  → Both were wrong")
        print()

    # Save comparison results
    output_df = df_comparison[[
        'message', 'label', 'regex_prediction', 'llm_prediction'
    ]].copy()

    output_df['regex_correct'] = (
        output_df['regex_prediction'] == output_df['label'].astype(int)
    )
    output_df['llm_correct'] = (
        output_df['llm_prediction'] == output_df['label'].astype(int)
    )

    output_df.to_csv(output_file, index=False)

    print("=" * 70)
    print(f"Full comparison saved to: {output_file}")
    print("=" * 70)
    print()

    # Summary statistics
    both_correct = len(output_df[output_df['regex_correct'] & output_df['llm_correct']])
    both_wrong = len(output_df[~output_df['regex_correct'] & ~output_df['llm_correct']])
    only_regex = len(output_df[output_df['regex_correct'] & ~output_df['llm_correct']])
    only_llm = len(output_df[~output_df['regex_correct'] & output_df['llm_correct']])

    print("SUMMARY:")
    print(f"  Both correct:       {both_correct} messages")
    print(f"  Both wrong:         {both_wrong} messages")
    print(f"  Only Regex correct: {only_regex} messages")
    print(f"  Only LLM correct:   {only_llm} messages")
    print()


if __name__ == '__main__':
    main()
