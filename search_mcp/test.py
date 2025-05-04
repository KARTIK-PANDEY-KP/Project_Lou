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

def test_anthropic_api():
    """Test Anthropic API connection"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    logger.info(f"Testing API Key: {api_key[:10]}...")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        # Test a simple message
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            temperature=0,
            messages=[{"role": "user", "content": "Hello"}]
        )
        logger.info("Anthropic API test successful!")
        return True
    except Exception as e:
        logger.error(f"Anthropic API test failed: {str(e)}")
        return False

def test_google_scraping():
    """Test Google search scraping"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get('https://www.google.com/search?q=test', headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        results = []
        
        for result in soup.select('div.g'):
            title_elem = result.select_one('h3')
            if title_elem:
                results.append(title_elem.text)
        
        logger.info(f"Google scraping test successful! Found {len(results)} results")
        return True
    except Exception as e:
        logger.error(f"Google scraping test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting local tests...")
    
    # Test Anthropic API
    api_success = test_anthropic_api()
    
    # Test Google scraping
    scraping_success = test_google_scraping()
    
    # Print summary
    logger.info("\nTest Summary:")
    logger.info(f"Anthropic API: {'✓' if api_success else '✗'}")
    logger.info(f"Google Scraping: {'✓' if scraping_success else '✗'}") 