import logging
from collections.abc import Sequence
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tracker-mcp")

# Initialize Firebase
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
firebase_admin.initialize_app(cred)
db = firestore.client()

def encode_url(url: str) -> str:
    """Encode URL to make it a valid Firestore document ID."""
    # Remove protocol and special characters
    clean_url = re.sub(r'^https?://', '', url)
    clean_url = re.sub(r'[^a-zA-Z0-9-]', '_', clean_url)
    # Ensure it's not too long (Firestore has a limit)
    return clean_url[:1500]

app = Server("tracker-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="track_url_email",
            description="Track a URL and its associated email",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to track"
                    },
                    "email": {
                        "type": "string",
                        "description": "The email associated with the URL"
                    }
                },
                "required": ["url", "email"]
            }
        ),
        Tool(
            name="get_tracked_data",
            description="Get all tracked URLs and emails",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    try:
        if name == "track_url_email":
            url = arguments.get("url")
            email = arguments.get("email")
            
            # Encode URL for document ID
            doc_id = encode_url(url)
            
            # Get or create document for URL
            doc_ref = db.collection('url_tracking').document(doc_id)
            doc = doc_ref.get()
            
            if doc.exists:
                # URL exists, check if email is new
                data = doc.to_dict()
                if email not in data.get('emails', []):
                    data['emails'].append(email)
                    data['is_new'] = True
                    doc_ref.set(data)
            else:
                # URL is new, create document
                doc_ref.set({
                    'url': url,
                    'emails': [email],
                    'is_new': True
                })
            
            return [TextContent(type="text", text=f"Successfully tracked URL: {url} with email: {email}")]
                
        elif name == "get_tracked_data":
            # Get all documents
            docs = db.collection('url_tracking').stream()
            output = []
            for doc in docs:
                data = doc.to_dict()
                output.append(f"URL: {data['url']}, Emails: {', '.join(data['emails'])}, New: {data['is_new']}")
            return [TextContent(type="text", text="\n".join(output))]
                
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logging.error(f"Error during call_tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")

async def main():
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 