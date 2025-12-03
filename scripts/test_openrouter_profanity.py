"""
Test LLM profanity classification via OpenRouter on 3 sample messages from GameTox dataset.
This script validates that the LLM can correctly identify toxic vs clean messages.
Uses OpenAI SDK with OpenRouter base URL and free tier model.
"""

import os
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

def get_classification(client, message_text):
    """
    Use LLM via OpenRouter to classify a single message as TOXIC or CLEAN.

    Args:
        client: OpenAI client instance configured for OpenRouter
        message_text: The message to classify

    Returns:
        str: "TOXIC" or "CLEAN"
    """

    prompt = f"""You are a content moderation system for a family-friendly online game.

Task: Determine if this message contains profanity, hate speech, harassment, or toxic content.

Message: "{message_text}"

Respond with ONLY one word:
- "TOXIC" if inappropriate
- "CLEAN" if appropriate

Your response:"""

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

        # Extract and clean the response
        classification = response.choices[0].message.content.strip().upper()

        # Ensure response is valid
        if "TOXIC" in classification:
            return "TOXIC"
        elif "CLEAN" in classification:
            return "CLEAN"
        else:
            # Default to the first word if format is unexpected
            return classification.split()[0] if classification else "UNKNOWN"

    except Exception as e:
        print(f"Error during classification: {str(e)}")
        return "ERROR"

def test_profanity_classification():
    """Test LLM on 3 sample messages from the GameTox dataset."""

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found in .env file")
        return

    # Initialize OpenAI client with OpenRouter base URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Load the dataset
    try:
        df = pd.read_csv("data/gametox.csv")
    except FileNotFoundError:
        print("❌ ERROR: data/gametox.csv not found")
        return

    # Select 3 test messages: 1 toxic (1.0), 1 clean (0.0), and 1 interesting case
    # Filter for label 1.0 and 0.0 only (ignore any other values like 2.0)
    toxic_messages = df[df['label'] == 1.0]
    clean_messages = df[df['label'] == 0.0]

    # Pick specific interesting examples
    test_cases = []

    # Case 1: Clear toxic message
    if len(toxic_messages) > 0:
        toxic_msg = toxic_messages.iloc[0]  # "move your ace plebs"
        test_cases.append({
            'message': toxic_msg['message'],
            'label': 'TOXIC',
            'index': 1
        })

    # Case 2: Clear clean message
    if len(clean_messages) > 0:
        clean_msg = clean_messages.iloc[2]  # "nice"
        test_cases.append({
            'message': clean_msg['message'],
            'label': 'CLEAN',
            'index': 2
        })

    # Case 3: Another toxic message for variety
    if len(toxic_messages) > 1:
        toxic_msg2 = toxic_messages.iloc[1]  # "idiots"
        test_cases.append({
            'message': toxic_msg2['message'],
            'label': 'TOXIC',
            'index': 3
        })

    if len(test_cases) < 3:
        print("❌ ERROR: Not enough test cases in dataset")
        return

    print("Testing LLM on 3 sample messages from GameTox...")
    print()

    correct_count = 0

    # Test each message
    for i, test_case in enumerate(test_cases, 1):
        message = test_case['message']
        expected_label = test_case['label']

        print(f"Message {i}: \"{message}\"")
        print(f"Actual label: {expected_label}")

        # Get LLM's prediction
        prediction = get_classification(client, message)
        print(f"LLM prediction: {prediction}")

        # Check if correct
        is_correct = (prediction == expected_label)
        if is_correct:
            correct_count += 1
            print("Result: ✓ CORRECT")
        else:
            print("Result: ✗ INCORRECT")

        print()

        # Rate limit: wait 3 seconds between API calls
        if i < len(test_cases):
            time.sleep(3)

    # Calculate and display accuracy
    accuracy = (correct_count / len(test_cases)) * 100
    print(f"Accuracy: {correct_count}/{len(test_cases)} ({accuracy:.0f}%)")
    print()

    if correct_count == len(test_cases):
        print("✅ LLM successfully classified all test messages!")
    else:
        print(f"⚠️  LLM classified {correct_count} out of {len(test_cases)} correctly.")

if __name__ == "__main__":
    test_profanity_classification()
