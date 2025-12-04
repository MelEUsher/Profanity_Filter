"""
Level 2 - LLM-based Profanity Classifier
Uses OpenRouter API to classify 50 messages as toxic or clean.
Calculates accuracy, precision, recall, and confusion matrix.
"""

import os
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

def load_prompt_template():
    """Load the prompt template from file."""
    with open("data/prompt_template.txt", "r") as f:
        return f.read()

def get_llm_classification(client, prompt_template, message_text):
    """
    Use LLM via OpenRouter to classify a single message.

    Args:
        client: OpenAI client configured for OpenRouter
        prompt_template: The prompt template with {message} placeholder
        message_text: The message to classify

    Returns:
        int: 1 for TOXIC, 0 for CLEAN
    """
    # Fill in the prompt template
    prompt = prompt_template.replace("{message}", message_text)

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=10
        )

        # Extract and parse the response
        llm_response = response.choices[0].message.content.strip().upper()

        # Parse response
        if "TOXIC" in llm_response:
            return 1
        elif "CLEAN" in llm_response:
            return 0
        else:
            # If unclear, default to TOXIC (safer for moderation)
            return 1

    except Exception as e:
        print(f"    API Error: {str(e)[:50]}... - Defaulting to TOXIC")
        # On error, default to TOXIC (safer for moderation)
        return 1

def calculate_metrics(df):
    """
    Calculate accuracy, precision, recall, and confusion matrix.

    Args:
        df: DataFrame with 'label' and 'llm_prediction' columns

    Returns:
        dict: Dictionary containing all metrics
    """
    # Convert labels to binary (1.0 -> 1, 0.0 -> 0)
    actual = (df['label'] == 1.0).astype(int)
    predicted = df['llm_prediction']

    # Calculate confusion matrix components
    tp = ((actual == 1) & (predicted == 1)).sum()  # True Positives
    fp = ((actual == 0) & (predicted == 1)).sum()  # False Positives
    tn = ((actual == 0) & (predicted == 0)).sum()  # True Negatives
    fn = ((actual == 1) & (predicted == 0)).sum()  # False Negatives

    # Calculate metrics
    total = len(df)
    correct = tp + tn
    accuracy = correct / total if total > 0 else 0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return {
        'total': total,
        'correct': correct,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }

def main():
    """Main function to run the LLM classifier."""

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found in .env file")
        return

    # Initialize OpenAI client with OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Load prompt template
    prompt_template = load_prompt_template()

    # Load the 50-message sample
    df = pd.read_csv("data/gametox_sample_50.csv")

    print(f"Processing {len(df)} messages...")
    print("This will take about 2-3 minutes...")
    print()

    # Process each message
    predictions = []

    for idx, row in df.iterrows():
        message = row['message']
        actual_label = row['label']

        # Get LLM prediction
        prediction = get_llm_classification(client, prompt_template, message)
        predictions.append(prediction)

        # Prepare display strings
        actual_str = "TOXIC" if actual_label == 1.0 else "CLEAN"
        pred_str = "TOXIC" if prediction == 1 else "CLEAN"
        correct = "✓" if (actual_label == 1.0 and prediction == 1) or (actual_label == 0.0 and prediction == 0) else "✗"

        # Truncate message for display
        message_display = message[:50] if len(message) <= 50 else message[:47] + "..."

        # Print progress
        print(f"{idx + 1}/50 {correct} Actual: {actual_str} | Predicted: {pred_str} | '{message_display}'")

        # Sleep to respect rate limits (except on last message)
        if idx < len(df) - 1:
            time.sleep(3)

    # Add predictions to dataframe
    df['llm_prediction'] = predictions

    print()
    print("=" * 60)
    print("LEVEL 2 - LLM CLASSIFIER RESULTS")
    print("=" * 60)

    # Calculate metrics
    metrics = calculate_metrics(df)

    print(f"Total messages: {metrics['total']}")
    print(f"Correct predictions: {metrics['correct']}")
    print()
    print(f"True Positives: {metrics['tp']}")
    print(f"False Positives: {metrics['fp']}")
    print(f"True Negatives: {metrics['tn']}")
    print(f"False Negatives: {metrics['fn']}")
    print()
    print(f"Accuracy: {metrics['accuracy']:.3f} ({metrics['accuracy'] * 100:.1f}%)")
    print(f"Precision: {metrics['precision']:.3f} ({metrics['precision'] * 100:.1f}%)")
    print(f"Recall: {metrics['recall']:.3f} ({metrics['recall'] * 100:.1f}%)")
    print()

    # Save results
    output_path = "results/level2_llm_predictions.csv"
    df.to_csv(output_path, index=False)
    print(f"Detailed results saved to: {output_path}")

if __name__ == "__main__":
    main()
