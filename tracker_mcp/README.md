# Tracker MCP

A Model Context Protocol (MCP) server for tracking URLs and their associated emails using Firebase Firestore.

## Features

- Track URLs and their associated emails
- Support for multiple emails per URL
- Track new/updated status
- Real-time data storage with Firebase
- Easy integration with Claude Desktop

## Tools

### 1. track_url_email
Tracks a URL and its associated email.

**Parameters:**
- `url`: The URL to track (string)
- `email`: The email associated with the URL (string)

**Example Usage:**
```
Use the track_url_email tool with:
- url: "https://example.com"
- email: "user@example.com"
```

### 2. get_tracked_data
Retrieves all tracked URLs and their associated emails.

**Example Usage:**
```
Use the get_tracked_data tool
```

## Setup

1. **Prerequisites:**
   - Python 3.8+
   - Firebase project with Firestore enabled
   - Firebase Admin SDK credentials

2. **Installation:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration:**
   - Place your Firebase credentials file at `firebase-credentials.json`
   - Add the following to your Claude Desktop config:
   ```json
   "tracker-mcp": {
     "command": "C:\\path\\to\\tracker_mcp\\venv\\Scripts\\Python.exe",
     "args": ["C:\\path\\to\\tracker_mcp\\main.py"],
     "cwd": "C:\\path\\to\\tracker_mcp",
     "env": {
       "FIREBASE_CREDENTIALS_PATH": "C:\\path\\to\\firebase-credentials.json",
       "PYTHONUNBUFFERED": "1",
       "PYTHONIOENCODING": "utf-8",
       "PYTHONPATH": "C:\\path\\to\\tracker_mcp"
     },
     "requiredTools": [
       "track_url_email",
       "get_tracked_data"
     ],
     "disabled": false
   }
   ```

## Data Structure

The data is stored in Firebase Firestore with the following structure:

```json
{
  "url_tracking": {
    "url": {
      "url": "https://example.com",
      "emails": ["user1@example.com", "user2@example.com"],
      "is_new": true
    }
  }
}
```

## Security

- Firebase credentials are stored locally and not committed to version control
- All sensitive data is stored securely in Firebase
- Access control is managed through Firebase security rules

## Dependencies

- mcp>=1.3.0
- firebase-admin>=6.8.0
- python-dotenv>=1.0.1

## Development

1. **Testing:**
   - Run the server: `python main.py`
   - Test with Claude Desktop integration

2. **Contributing:**
   - Create a new branch for features
   - Follow PEP 8 style guide
   - Add tests for new features

## License

MIT License

## Support

For issues and feature requests, please open an issue in the repository. 