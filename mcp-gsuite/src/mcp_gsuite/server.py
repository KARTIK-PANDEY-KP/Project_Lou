import logging
from collections.abc import Sequence
from functools import lru_cache
import subprocess
from typing import Any
import traceback
from dotenv import load_dotenv
from mcp.server import Server
import threading
import sys
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import json
from . import gauth
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import (
    urlparse,
    parse_qs,
)
from . import tool_registry
import httplib2

class OAuthServer(HTTPServer):
    def __init__(self, server_address, auth_complete):
        self.auth_complete = auth_complete
        super().__init__(server_address, OauthListener)

class OauthListener(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/code":
            self.send_response(404)
            self.end_headers()
            return

        query = parse_qs(url.query)
        if "code" not in query:
            self.send_response(400)
            self.end_headers()
            return
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Auth successful! You can close the tab!".encode("utf-8"))
        self.wfile.flush()

        try:
            storage = {}
            creds = gauth.get_credentials(authorization_code=query["code"][0], state=storage)
            self.server.auth_complete.set()  # Signal through server instance
        except Exception as e:
            logging.error(f"Error during auth: {e}")
            self.server.auth_complete.set()  # Signal even on error

        # Shutdown server in background thread
        t = threading.Thread(target=self.server.shutdown)
        t.daemon = True
        t.start()

load_dotenv()

from . import tools_gmail
from . import tools_calendar
from . import toolhandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-gsuite")

def start_auth_flow(user_id: str):
    auth_url = gauth.get_authorization_url(user_id, state={})
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        subprocess.Popen(['open', auth_url])
    else:
        logging.info(f"opening auth url: {auth_url}")
        import webbrowser
        webbrowser.open(auth_url)

    # Create event to signal auth completion
    auth_complete = threading.Event()
    
    # start server for code callback in background thread
    server_address = ('localhost', 4100)  # Bind only to localhost
    logging.info(f"starting server at {server_address}")
    
    server = OAuthServer(server_address, auth_complete)
    
    def run_server():
        logging.info(f"server started")
        server.serve_forever()
        logging.info(f"server stopped")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for auth to complete or timeout after 5 minutes
    logging.info("Waiting for OAuth completion...")
    if not auth_complete.wait(timeout=300):  # 5 minute timeout
        logging.error("OAuth flow timed out")
        server.shutdown()
        raise TimeoutError("OAuth flow timed out")
    
    logging.info("OAuth flow completed successfully")
    return server

def setup_oauth2(user_id: str):
    accounts = gauth.get_account_info()
    if len(accounts) == 0:
        raise RuntimeError("No accounts specified in .gauth.json")
    if user_id not in [a.email for a in accounts]:
        raise RuntimeError(f"Account for email: {user_id} not specified in .gauth.json")

    credentials = gauth.get_stored_credentials(user_id=user_id)
    logging.info(f"credentials: {credentials}")
    if not credentials:
        logging.info(f"no credentials found for {user_id}, starting auth flow")
        start_auth_flow(user_id=user_id)
    else:
        logging.info(f"credentials found for {user_id}")
        if credentials.access_token_expired:
            logging.info(f"credentials expired. try refresh")
            credentials.refresh(httplib2.Http())

        # this call refreshes access token
        logging.info(f"refreshing credentials")
        user_info = gauth.get_user_info(credentials=credentials)
        logging.info(f"user_info: {user_info}")
        #logging.error(f"User info: {json.dumps(user_info)}")
        gauth.store_credentials(credentials=credentials, user_id=user_id)
        logging.info(f"stored credentials for {user_id}")


app = Server("mcp-gsuite")

# Register all tools
tool_registry.add_tool_handler(tools_gmail.QueryEmailsToolHandler())
tool_registry.add_tool_handler(tools_gmail.GetEmailByIdToolHandler())
tool_registry.add_tool_handler(tools_gmail.CreateDraftToolHandler())
tool_registry.add_tool_handler(tools_gmail.DeleteDraftToolHandler())
tool_registry.add_tool_handler(tools_gmail.ReplyEmailToolHandler())
tool_registry.add_tool_handler(tools_gmail.GetAttachmentToolHandler())
tool_registry.add_tool_handler(tools_gmail.BulkGetEmailsByIdsToolHandler())
tool_registry.add_tool_handler(tools_gmail.BulkSaveAttachmentsToolHandler())
tool_registry.add_tool_handler(tools_gmail.SendEmailToolHandler())

tool_registry.add_tool_handler(tools_calendar.ListCalendarsToolHandler())
tool_registry.add_tool_handler(tools_calendar.GetCalendarEventsToolHandler())
tool_registry.add_tool_handler(tools_calendar.CreateCalendarEventToolHandler())
tool_registry.add_tool_handler(tools_calendar.DeleteCalendarEventToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [th.get_tool_description() for th in tool_registry.get_all_tool_handlers().values()]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    try:        
        if not isinstance(arguments, dict):
            raise RuntimeError("arguments must be dictionary")
        
        if toolhandler.USER_ID_ARG not in arguments:
            raise RuntimeError("user_id argument is missing in dictionary.")

        setup_oauth2(user_id=arguments.get(toolhandler.USER_ID_ARG, ""))
        logging.info(f"setup_oauth2 done for {arguments.get(toolhandler.USER_ID_ARG, '')}")
        tool_handler = tool_registry.get_tool_handler(name)
        if not tool_handler:
            raise ValueError(f"Unknown tool: {name}")

        return tool_handler.run_tool(arguments)
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error during call_tool: str(e)")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")


async def main():
    # print(sys.platform)
    logging.info(sys.platform)
    accounts = gauth.get_account_info()
    for account in accounts:
        creds = gauth.get_stored_credentials(user_id=account.email)
        if creds:
            logging.info(f"found credentials for {account.email}")

    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )