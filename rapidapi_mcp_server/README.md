# RapidAPI LinkedIn MCP Server

A Model Context Protocol (MCP) server for LinkedIn integration using RapidAPI. This server provides a more reliable and faster way to fetch LinkedIn profile data compared to browser-based scraping.

## 🚀 Features

- Fast and reliable LinkedIn profile data fetching using RapidAPI
- No browser automation required
- No login credentials needed
- Simple and efficient implementation
- Real-time data access

## 📋 Prerequisites

- Python 3.8 or higher
- RapidAPI key (included in the configuration)
- Claude Desktop installed

## 🔧 Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The server is pre-configured with a RapidAPI key. To use it with Claude Desktop:

1. Copy `claude_config.json` to your Claude Desktop configuration directory:
   ```bash
   copy claude_config.json "C:/Users/your_username/AppData/Roaming/Claude/claude_desktop_config.json"
   ```

2. Restart Claude Desktop

## 💻 Usage

1. Start a conversation with Claude
2. Use the `get_person_profile` tool to fetch LinkedIn profile data
3. Example usage:
   ```
   Can you tell me about this person's profile? https://www.linkedin.com/in/example/
   ```

## 🔐 Security

- The server uses a secure API key for authentication
- No personal LinkedIn credentials are required
- All data is fetched through RapidAPI's secure endpoints

## ⚠️ Limitations

- Requires a valid RapidAPI subscription
- Rate limits may apply based on your RapidAPI plan
- Some LinkedIn data may not be available through the API

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 