# Gemini AI Chat with Real-Time Search

A Python application that provides an interactive chat interface using Google's Gemini AI model (gemini-2.0-flash) with optional real-time Google Search capabilities.

## Features

- 🤖 **AI Chat Interface**: Interactive conversations with Google's Gemini 2.0 Flash model
- 🔍 **Real-Time Search**: Optional Google Search integration for up-to-date information
- 💬 **Conversation History**: Track and view full conversation history
- 🎯 **Two Modes**: 
  - Hardcoded examples for testing
  - Interactive command-line interface for live conversations
- 🔐 **Secure Configuration**: Environment variable-based API key management

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/aayushmaan/Internship/GenAIModel
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Interactive Chat Mode

Run the interactive chat interface:

```bash
python InteractiveChat.py
```

**Available Commands:**
- Type your message normally to chat
- `search` - Enable real-time search for your next query
- `history` - View full conversation history
- `clear` - Clear conversation history
- `exit` - Exit the chat

**Example Session:**
```
You: What is Python used for?
Bot: [Response from Gemini]

You: search
🔍 Real-time search enabled for next query. Ask your question:
You: What is the current price of Bitcoin?
Bot: [Response with real-time data]
```

### Hardcoded Examples Mode

Run the script with predefined examples:

```bash
python HardcodedChat.py
```

This will execute several example conversations demonstrating:
- Regular chat interactions
- Real-time search queries (Bitcoin price, weather, etc.)
- Conversation history display

## Project Structure

```
GenAIModel/
├── HardcodedChat.py      # Script with hardcoded example conversations
├── InteractiveChat.py    # Interactive command-line chat interface
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this file)
└── README.md            # This file
```

## Class: GeminiChatWithRealTimeSearch

Both scripts use the same `GeminiChatWithRealTimeSearch` class with the following methods:

- `__init__(api_key)`: Initialize the Gemini client
- `initialize_chat(system_instruction="")`: Initialize a chat session
- `enable_real_time_search()`: Enable Google Search capability
- `send_message(user_message, use_search=False)`: Send a message and get response
- `get_conversation_history()`: Retrieve full conversation history
- `clear_history()`: Clear conversation history
- `display_history()`: Display formatted conversation history

## Dependencies

Key dependencies include:
- `google-genai`: Google's Gemini AI SDK
- `python-dotenv`: Environment variable management
- `google-auth`: Authentication for Google APIs

See `requirements.txt` for the complete list of dependencies.

## Configuration

The application uses the following configuration:

- **Model**: `gemini-2.0-flash`
- **System Instruction**: "You are a helpful AI assistant with access to real-time information."
- **API Key**: Loaded from `GEMINI_API_KEY` environment variable (via `.env` file)

## Error Handling

The application includes error handling for:
- Missing API keys
- API response errors
- Invalid user inputs
- Keyboard interrupts (Ctrl+C)

## Notes

- The real-time search feature requires enabling the `google_search` tool for each query
- Conversation history is maintained in memory and cleared when the script exits
- The `.env` file should be added to `.gitignore` to keep your API key secure

## License

This project is under standard MIT license.

