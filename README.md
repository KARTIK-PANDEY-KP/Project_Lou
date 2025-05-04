# 🤖 Project Lou - Your AI-Powered Search Assistant

## 🌟 What is Lou?

Lou is an intelligent search assistant that revolutionizes how you find information online. By combining the power of natural language processing with advanced search capabilities, Lou helps you discover exactly what you're looking for - without the hassle of crafting perfect search queries.

## ✨ Key Features

- **Natural Language Search**: Simply tell Lou what you need in plain English
- **Smart Query Generation**: Automatically converts your requests into optimized search queries
- **Google Custom Search Integration**: Leverages Google's powerful search engine for accurate results
- **Intelligent Filtering**: Removes duplicate and irrelevant results
- **Easy-to-Use API**: Simple integration with your existing applications

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/KARTIK-PANDEY-KP/Project-Lou.git
```

2. Install dependencies:
```bash
cd search_mcp
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create a .env file with your API keys
GOOGLE_API_KEY=your_api_key
GOOGLE_CSE_ID=your_cse_id
```

## 💡 Example Usage

```python
from search_mcp.main import process_search_query

# Ask Lou anything in natural language
result = process_search_query("Find graduation photographers at USC for 2025")
```

## 🛠️ Project Structure

- `search_mcp/`: Core search functionality
  - `main.py`: Main search processing logic
  - `test.py`: Unit tests
  - `requirements.txt`: Project dependencies

## 🤝 Contributing

We welcome contributions! Feel free to:
- Submit bug reports
- Propose new features
- Create pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Why Lou?

Lou is more than just a search tool - it's your intelligent assistant that understands your intent and finds exactly what you need. Whether you're researching, gathering information, or looking for specific services, Lou makes the process effortless and efficient.

---
Made with ❤️ by Kartik Pandey 