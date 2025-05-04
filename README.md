# 🤖 Project Lou - Your AI-Powered Assistant Suite

## 🌟 What is Project Lou?

Project Lou is a comprehensive suite of AI-powered tools that help you automate and enhance your workflow. It combines multiple specialized MCP (Model Context Protocol) servers to provide a seamless experience for searching, tracking, and managing information.

## ✨ Key Components

### 1. Search MCP 🔍
- Natural Language Search using Google Custom Search
- Smart Query Generation
- Intelligent Filtering
- Easy-to-Use API

### 2. Tracker MCP 📊
- Track URLs and associated emails
- Support for multiple emails per URL
- Real-time data storage with Firebase
- Track new/updated status

### 3. LinkedIn RapidAPI MCP 👥
- Fetch LinkedIn profile information
- Professional data extraction
- Automated profile analysis

### 4. Email Finder MCP 📧
- Find email addresses
- Email verification
- Contact discovery

### 5. GSuite MCP 📅
- Gmail integration
- Calendar management
- Google Workspace automation

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/KARTIK-PANDEY-KP/Project-Lou.git
```

2. Set up each MCP server:

### Search MCP
```bash
cd search_mcp
pip install -r requirements.txt
# Set GOOGLE_API_KEY and GOOGLE_CSE_ID in .env
```

### Tracker MCP
```bash
cd tracker_mcp
pip install -r requirements.txt
# Add firebase-credentials.json
```

### LinkedIn RapidAPI MCP
```bash
cd rapidapi_mcp_server
pip install -r requirements.txt
# Set RAPIDAPI_KEY in .env
```

### Email Finder MCP
```bash
cd email-finder
pip install -r requirements.txt
# Set ANYMAILFINDER_KEY in .env
```

### GSuite MCP
```bash
cd mcp-gsuite
pip install -r requirements.txt
# Configure OAuth2 credentials
```

## 🛠️ Project Structure

```
Project-Lou/
├── search_mcp/         # Search functionality
├── tracker_mcp/        # URL and email tracking
├── rapidapi_mcp_server/# LinkedIn integration
├── email-finder/       # Email discovery
└── mcp-gsuite/        # Google Workspace integration
```

## 🔐 API Keys and Security

Each MCP server requires specific API keys or credentials:
- Search MCP: Google API Key & CSE ID
- Tracker MCP: Firebase Admin SDK credentials
- LinkedIn MCP: RapidAPI Key
- Email Finder: AnyMailFinder API Key
- GSuite MCP: Google OAuth2 credentials

⚠️ Never commit API keys or credentials to version control!

## 💡 Example Usage

### Search
```python
Use the web_search tool with your query
```

### Track URLs and Emails
```python
Use the track_url_email tool with:
- url: "https://example.com"
- email: "user@example.com"
```

### LinkedIn Profile
```python
Use the get_person_profile tool with LinkedIn URL
```

### Find Email
```python
Use the find_email tool with name and domain
```

### GSuite
```python
Use the gmail or calendar tools for Google Workspace tasks
```

## 🤝 Contributing

We welcome contributions! Feel free to:
- Submit bug reports
- Propose new features
- Create pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Why Project Lou?

Project Lou is your comprehensive AI assistant suite that:
- Automates repetitive tasks
- Enhances productivity
- Provides intelligent insights
- Integrates seamlessly with popular services
- Makes complex workflows simple

Whether you're researching, managing contacts, or automating your workflow, Project Lou's suite of tools makes the process effortless and efficient.

---
Made with ❤️ by Kartik Pandey 