# Search MCP Server

A Model Context Protocol (MCP) server that generates Google dorks for advanced search queries using Claude AI.

## Features

- Generate Google dorks from natural language queries
- Specialized search patterns for:
  - Finding people across social media platforms
  - Company research
  - Technical information
  - Document discovery
  - And more...
- Anthropic Claude 3 powered query understanding
- JSON formatted results

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Anthropic API key:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```

## Usage with Claude Desktop

1. Add the following to your Claude Desktop config:
```json
{
    "mcpServers": {
        "search-mcp": {
            "command": "python",
            "args": ["path/to/search_mcp/main.py"],
            "env": {
                "ANTHROPIC_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

2. Example queries:
   - "Find software engineers at Google who graduated from MIT"
   - "Find cybersecurity experts on Twitter who tweet about AI"
   - "Find research papers about machine learning published in 2024"
   - "Find GitHub repositories about blockchain written in Python"

## Response Format

The server returns JSON-formatted Google dorks, for example:
```json
{
    "basic_search": "site:linkedin.com/in \"software engineer\" \"Google\" \"MIT\"",
    "advanced_search": "site:linkedin.com/in \"software engineer\" \"Google\" \"MIT\" after:2023",
    "alternative_platforms": "site:twitter.com \"software engineer\" \"Google\" \"MIT\" OR site:github.com \"Google\" \"MIT\""
}
```

## Development

To run the server locally:
```bash
python main.py
```

## License

MIT License 