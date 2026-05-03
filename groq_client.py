"""
Groq API Client
Simple and fast LLM inference using Groq
"""

import requests
import json


class GroqClient:
    """Simple client for Groq API"""
    
    def __init__(self, api_key):
        """
        Initialize Groq client
        
        Args:
            api_key: Groq API key from https://console.groq.com
        """
        self.api_key = "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"
        self.base_url = "https://api.groq.com/openai/v1"
        
    def generate_text(self, prompt, model="llama-3.3-70b-versatile", max_tokens=500, temperature=0.7):
        """
        Generate text using Groq API
        
        Args:
            prompt: Input prompt
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text or None if error
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=body, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Groq API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


# Available Groq models (all free!)
AVAILABLE_MODELS = {
    "llama-3.3-70b": "llama-3.3-70b-versatile",  # Latest, most capable
    "llama-3.1-70b": "llama-3.1-70b-versatile",  # Very good
    "llama-3.1-8b": "llama-3.1-8b-instant",      # Fast
    "mixtral-8x7b": "mixtral-8x7b-32768",        # Good for reasoning
    "gemma-2-9b": "gemma2-9b-it",                # Google's Gemma
}


def test_connection(api_key):
    """Test Groq API connection"""
    client = GroqClient(api_key)
    
    print("Testing Groq API connection...")
    print(f"API Key: {api_key[:10]}...")
    
    # Test text generation
    print("\nTesting text generation with Llama 3.3...")
    response = client.generate_text(
        "Say 'Hello from Groq!' in one sentence.",
        model="llama-3.3-70b-versatile",
        max_tokens=50
    )
    
    if response:
        print("SUCCESS: Text generation successful!")
        print(f"Response: {response}")
        return True
    else:
        print("ERROR: Text generation failed")
        return False


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Please set GROQ_API_KEY in .env file")
        print("\nTo get a free API key:")
        print("1. Go to: https://console.groq.com")
        print("2. Sign up (free)")
        print("3. Go to API Keys section")
        print("4. Create a new API key")
        print("5. Add it to your .env file as: GROQ_API_KEY=your_key_here")
    else:
        test_connection(api_key)

# Made with Bob
