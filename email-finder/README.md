# Email Finder MCP Server

A Model Context Protocol (MCP) server that finds emails associated with LinkedIn profiles using the AnyMailFinder API.

## Features

- Find email addresses from LinkedIn profile URLs
- Email validation status
- Profile information including:
  - Full Name
  - Job Title
  - Company Name
- Async/await implementation for better performance
- MCP integration for Claude Desktop

## Setup

1. Install dependencies:
```bash
pip install aiohttp mcp.server
```

2. Set up your API key:
   - Get your API key from [AnyMailFinder](https://anymailfinder.com)
   - Set it as an environment variable:
     ```bash
     set ANYMAILFINDER_KEY=your_api_key_here
     ```
   - Or use it directly in the code (not recommended for production)

## Usage

1. Start the MCP server:
```bash
python email_mcp_server.py
```

2. The server exposes the following tool:
   - `find_email`: Takes a LinkedIn profile URL and returns email information

3. Example response:
```json
{
    "success": true,
    "data": {
        "fullName": "John Doe",
        "title": "Software Engineer",
        "companyName": "Tech Corp",
        "email": "john.doe@techcorp.com",
        "validation": "valid"
    }
}
```

## Integration with Claude Desktop

1. Add the following configuration to your Claude Desktop config:
```json
{
    "mcpServers": {
        "email-finder": {
            "command": "python",
            "args": ["path/to/email_mcp_server.py"],
            "env": {
                "ANYMAILFINDER_KEY": "your_api_key_here"
            }
        }
    }
}
```

2. Use the `find_email` tool in Claude Desktop by providing a LinkedIn URL.

## Error Handling

The server handles various error cases:
- Invalid API key
- Rate limiting
- Network errors
- Invalid LinkedIn URLs

## License

MIT License 