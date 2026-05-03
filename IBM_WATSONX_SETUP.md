# 🤖 IBM watsonx.ai Integration Guide

## Overview
This guide will help you integrate IBM's free LLM models (like Granite) into Bob Teacher Assistant.

## Option 1: IBM watsonx.ai (Recommended)

### Step 1: Get IBM Cloud Account
1. Go to: https://cloud.ibm.com/registration
2. Sign up for a free IBM Cloud account
3. Verify your email

### Step 2: Create watsonx.ai Instance
1. Go to: https://cloud.ibm.com/catalog/services/watsonx-ai
2. Select the **Lite (Free)** plan
3. Click "Create"

### Step 3: Get API Credentials
1. Go to your watsonx.ai instance
2. Click on "Manage" → "Access (IAM)"
3. Create an API key
4. Copy your:
   - API Key
   - Project ID
   - Region (e.g., us-south)

### Step 4: Install Required Packages
```bash
pip install ibm-watsonx-ai ibm-cloud-sdk-core
```

### Step 5: Update .env File
Add these to your `.env` file:
```
# IBM watsonx.ai Configuration
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

## Option 2: IBM Granite via Hugging Face (Free)

### Step 1: Get Hugging Face Token
1. Go to: https://huggingface.co/join
2. Sign up for free
3. Go to Settings → Access Tokens
4. Create a new token

### Step 2: Install Required Packages
```bash
pip install transformers torch huggingface_hub
```

### Step 3: Update .env File
```
# Hugging Face Configuration
HUGGINGFACE_TOKEN=your_token_here
MODEL_NAME=ibm-granite/granite-3.0-8b-instruct
```

## Available IBM Models

### watsonx.ai Models (Free Tier):
- `ibm/granite-13b-chat-v2` - General purpose chat
- `ibm/granite-13b-instruct-v2` - Instruction following
- `meta-llama/llama-3-8b-instruct` - Meta's Llama 3
- `mistralai/mixtral-8x7b-instruct-v01` - Mixtral

### Hugging Face Models:
- `ibm-granite/granite-3.0-8b-instruct` - Latest Granite
- `ibm-granite/granite-3.0-2b-instruct` - Smaller, faster
- `ibm-granite/granite-3.1-8b-instruct` - Newest version

## Next Steps

Choose one option above and I'll help you:
1. Modify the app.py to use IBM models
2. Update the requirements.txt
3. Test the integration

Which option do you prefer?
- Option 1: IBM watsonx.ai (cloud-based, more powerful)
- Option 2: Hugging Face (local or API, more flexible)