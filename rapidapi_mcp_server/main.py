"""
RapidAPI LinkedIn MCP Server - A Model Context Protocol server for LinkedIn integration using RapidAPI.
"""

import asyncio
import logging
import sys
from typing import Dict, Optional, Any
from mcp.server.fastmcp import FastMCP
import aiohttp
import os

logger = logging.getLogger(__name__)

class RapidAPILinkedInMCPServer(FastMCP):
    """RapidAPI LinkedIn MCP server with improved connection handling."""
    
    def __init__(self):
        super().__init__()
        # Get API key from environment variable
        self.api_key = os.getenv("RAPIDAPI_KEY")
        if not self.api_key:
            logger.error("RAPIDAPI_KEY environment variable is not set")
            raise ValueError("RAPIDAPI_KEY environment variable is required")
        self.session = None
        self._event_loop = None

    async def start(self):
        """Start the server and initialize the HTTP session."""
        if not self._event_loop:
            self._event_loop = asyncio.get_running_loop()
        if not self.session:
            self.session = aiohttp.ClientSession()
        await super().start()
        logger.info("Server started successfully")

    async def stop(self):
        """Stop the server and cleanup."""
        if self.session:
            await self.session.close()
            self.session = None
        await super().stop()
        logger.info("Server stopped successfully")

    async def fetch_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """Fetch LinkedIn profile data using RapidAPI."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        headers = {
            "x-rapidapi-host": "fresh-linkedin-profile-data.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }
        
        params = {
            "linkedin_url": linkedin_url,
            "include_skills": "false",
            "include_certifications": "false",
            "include_publications": "false",
            "include_honors": "false",
            "include_volunteers": "false",
            "include_projects": "false",
            "include_patents": "false",
            "include_courses": "false",
            "include_organizations": "false",
            "include_profile_status": "false",
            "include_company_public_url": "false"
        }

        try:
            async with self.session.get(
                "https://fresh-linkedin-profile-data.p.rapidapi.com/get-linkedin-profile",
                headers=headers,
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_msg = f"API request failed with status {response.status}"
                    logger.error(error_msg)
                    return {"error": error_msg}
        except Exception as e:
            error_msg = f"Error fetching profile: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

def create_mcp_server() -> RapidAPILinkedInMCPServer:
    """
    Create and configure the RapidAPI LinkedIn MCP server.

    Returns:
        RapidAPILinkedInMCPServer: Configured MCP server instance
    """
    mcp = RapidAPILinkedInMCPServer()
    
    @mcp.tool()
    async def get_person_profile(linkedin_url: str) -> Dict[str, Any]:
        """
        Get a person's LinkedIn profile data.

        Args:
            linkedin_url (str): The LinkedIn URL of the person's profile

        Returns:
            Dict[str, Any]: Structured data from the person's profile
        """
        return await mcp.fetch_profile(linkedin_url)
    
    return mcp

def main() -> None:
    """Initialize and run the RapidAPI LinkedIn MCP server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("rapidapi_mcp.log", encoding="utf-8", mode="w"),
            logging.StreamHandler(sys.stderr)
        ]
    )

    logger.info("Starting RapidAPI LinkedIn MCP server...")
    logger.info("🔗 RapidAPI LinkedIn MCP Server 🔗")
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