"""
IBM watsonx.ai Client
Simple REST API client for IBM watsonx.ai without heavy dependencies
"""

import requests
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException


class WatsonxClient:
    """Simple client for IBM watsonx.ai API"""
    
    def __init__(self, api_key, project_id, url="https://us-south.ml.cloud.ibm.com"):
        """
        Initialize watsonx client
        
        Args:
            api_key: IBM Cloud API key
            project_id: watsonx.ai project ID
            url: watsonx.ai service URL
        """
        self.api_key = api_key
        self.project_id = project_id
        self.url = url
        self.authenticator = IAMAuthenticator(api_key)
        self.token = None
        
    def get_token(self):
        """Get IAM access token"""
        try:
            self.token = self.authenticator.token_manager.get_token()
            return self.token
        except Exception as e:
            print(f"Error getting token: {e}")
            return None
    
    def generate_text(self, prompt, model_id="ibm/granite-13b-chat-v2", max_tokens=500, temperature=0.7):
        """
        Generate text using watsonx.ai
        
        Args:
            prompt: Input prompt
            model_id: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text or None if error
        """
        if not self.token:
            self.get_token()
        
        endpoint = f"{self.url}/ml/v1/text/generation?version=2023-05-29"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "stop_sequences": ["\n\n"]
            },
            "model_id": model_id,
            "project_id": self.project_id
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            
            result = response.json()
            if "results" in result and len(result["results"]) > 0:
                return result["results"][0]["generated_text"]
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling watsonx API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


# Available models in watsonx.ai free tier
AVAILABLE_MODELS = {
    "granite-13b-chat": "ibm/granite-13b-chat-v2",
    "granite-13b-instruct": "ibm/granite-13b-instruct-v2",
    "llama-3-8b": "meta-llama/llama-3-8b-instruct",
    "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct-v01",
    "flan-t5-xxl": "google/flan-t5-xxl",
    "flan-ul2": "google/flan-ul2"
}


def test_connection(api_key, project_id, url="https://us-south.ml.cloud.ibm.com"):
    """Test watsonx.ai connection"""
    client = WatsonxClient(api_key, project_id, url)
    
    print("Testing IBM watsonx.ai connection...")
    print(f"URL: {url}")
    print(f"Project ID: {project_id[:10]}...")
    
    # Test token generation
    token = client.get_token()
    if not token:
        print("❌ Failed to get authentication token")
        return False
    
    print("✅ Authentication successful")
    
    # Test text generation
    print("\nTesting text generation...")
    response = client.generate_text(
        "Say 'Hello from IBM watsonx!' in one sentence.",
        model_id="ibm/granite-13b-chat-v2",
        max_tokens=50
    )
    
    if response:
        print(f"✅ Text generation successful!")
        print(f"Response: {response}")
        return True
    else:
        print("❌ Text generation failed")
        return False


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("IBM_WATSONX_API_KEY")
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")
    url = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    
    if not api_key or not project_id:
        print("❌ Please set IBM_WATSONX_API_KEY and IBM_WATSONX_PROJECT_ID in .env file")
    else:
        test_connection(api_key, project_id, url)

# Made with Bob
