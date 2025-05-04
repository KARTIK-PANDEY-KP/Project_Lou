"""
Email Finder MCP Server - A Model Context Protocol server for finding emails using AnyMailFinder API.
"""

import asyncio
import logging
import sys
from typing import Dict, Optional, Any
from mcp.server.fastmcp import FastMCP
import aiohttp
import os

logger = logging.getLogger(__name__)

class EmailFinderMCPServer(FastMCP):
    """Email Finder MCP server with improved connection handling."""
    
    def __init__(self):
        super().__init__()
        # Get API key from environment variable
        self.api_key = os.getenv("ANYMAILFINDER_KEY", "Nz8Oz4n1RIq4dWVtiTzhbS0O")
        if not self.api_key:
            logger.error("ANYMAILFINDER_KEY environment variable is not set")
            raise ValueError("ANYMAILFINDER_KEY environment variable is required")
        self.session = None
        self._event_loop = None

    async def start(self):
        """Start the server and initialize the HTTP session."""
        if not self._event_loop:
            self._event_loop = asyncio.get_running_loop()
        if not self.session:
            self.session = aiohttp.ClientSession()
        await super().start()
        logger.info("Email Finder Server started successfully")

    async def stop(self):
        """Stop the server and cleanup."""
        if self.session:
            await self.session.close()
            self.session = None
        await super().stop()
        logger.info("Email Finder Server stopped successfully")

    async def fetch_email(self, linkedin_url: str) -> Dict[str, Any]:
        """Fetch email data using AnyMailFinder API."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        url = "https://api.anymailfinder.com/v5.0/search/linkedin-url.json"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "linkedin_url": linkedin_url
        }

        try:
            async with self.session.post(url, json=body, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', {})
                    return {
                        "success": True,
                        "data": {
                            "fullName": results.get('fullName'),
                            "title": results.get('title'),
                            "companyName": results.get('companyName'),
                            "email": results.get('email'),
                            "validation": results.get('validation')
                        }
                    }
                else:
                    data = await response.json()
                    error_msg = data.get('error_explained', f"API request failed with status {response.status}")
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "status_code": response.status
                    }
        except Exception as e:
            error_msg = f"Error fetching email: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

def create_mcp_server() -> EmailFinderMCPServer:
    """
    Create and configure the Email Finder MCP server.

    Returns:
        EmailFinderMCPServer: Configured MCP server instance
    """
    mcp = EmailFinderMCPServer()
    
    @mcp.tool()
    async def find_email(linkedin_url: str) -> Dict[str, Any]:
        """
        Find email associated with a LinkedIn profile.

        Args:
            linkedin_url (str): The LinkedIn URL of the person's profile

        Returns:
            Dict[str, Any]: Email information and validation status
        """
        return await mcp.fetch_email(linkedin_url)
    
    return mcp

def main() -> None:
    """Initialize and run the Email Finder MCP server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("email_finder_mcp.log", encoding="utf-8", mode="w"),
            logging.StreamHandler(sys.stderr)
        ]
    )

    logger.info("Starting Email Finder MCP server...")
    logger.info("📧 Email Finder MCP Server 📧")
    logger.info("=" * 40)

    try:
        # Create and run the MCP server
        mcp = create_mcp_server()
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 