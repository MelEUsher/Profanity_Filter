"""
Test OpenRouter API connection with a simple prompt.
This script verifies that the API key is configured correctly and the connection works.
Uses OpenAI SDK with OpenRouter base URL.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_connection():
    """Test the OpenRouter API with a simple hello world message."""

    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found in .env file")
        print("\nPlease add your API key to the .env file:")
        print("OPENROUTER_API_KEY=sk-or-v1-...")
        return False

    # Show truncated API key for verification (first 15 chars only)
    truncated_key = api_key[:15] + "..." if len(api_key) > 15 else api_key
    print(f"API Key found: {truncated_key} (hidden)")
    print()

    try:
        # Initialize the OpenAI client with OpenRouter base URL
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        print("Testing API connection...")
        print("Sending test message to LLM via OpenRouter...")
        print()

        # Send a simple test message using free tier model
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Please respond with a brief greeting to confirm the API is working."
                }
            ],
            max_tokens=100
        )

        # Extract the response text
        response_text = response.choices[0].message.content

        print(f"LLM Response: {response_text}")
        print()
        print("✅ SUCCESS! OpenRouter API is working correctly.")
        return True

    except Exception as e:
        print(f"❌ ERROR: Failed to connect to OpenRouter API")
        print(f"Error details: {str(e)}")
        print()
        print("Common issues:")
        print("- Invalid API key")
        print("- No internet connection")
        print("- API service temporarily unavailable")
        print("- Rate limit exceeded")
        return False

if __name__ == "__main__":
    test_api_connection()
