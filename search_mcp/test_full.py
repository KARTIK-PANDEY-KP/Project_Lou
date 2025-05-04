import os
from dotenv import load_dotenv
import anthropic
import json
import requests
from bs4 import BeautifulSoup
import time
import random

# Load environment variables
load_dotenv()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")

# Sample template similar to what's in main.py
SAMPLE_PROMPT = """
# Google Dork Syntax Quick Reference
# How to Use This Document:
# 1. Copy the syntax you need from the sections below
# 2. Replace the placeholders with your actual search terms

# Example Usage:
# To find PDFs about AI on a specific domain:
# site:example.com filetype:pdf "artificial intelligence"

User Query: find photographers for graduation 2025 near USC University of Southern California Los Angeles Instagram

Return ONLY the JSON with dorks, nothing else.
"""

def test_anthropic_api_identical_to_main():
    """Test Anthropic API connection with identical parameters to main.py"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    logger.info(f"Testing API Key: {api_key[:10]}...")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Call Claude with identical parameters to main.py
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": SAMPLE_PROMPT
                }
            ]
        )
        logger.info("Anthropic API test successful!")
        logger.info(f"Response: {message.content[0].text[:100]}...")  # First 100 chars
        return True
    except Exception as e:
        logger.error(f"Anthropic API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting full identical test...")
    test_anthropic_api_identical_to_main() 