"""Test script to verify Gemini API is working"""
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    print(f"API Key found: {'Yes' if GEMINI_API_KEY else 'No'}")
    print(f"API Key (first 10 chars): {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'None'}")
    
    if GEMINI_API_KEY:
        print("\nConfiguring Gemini AI...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        print("Creating model with gemini-1.5-flash...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("Testing API call...")
        response = model.generate_content("Say 'Hello, API is working!' in one sentence.")
        
        print("\nSUCCESS! API Response:")
        print(response.text)
        print("\nThe Gemini API is working correctly!")
        
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nThis might be due to:")
    print("1. Invalid API key")
    print("2. API quota exceeded")
    print("3. Network connectivity issues")
    print("4. Model name not supported")

# Made with Bob
