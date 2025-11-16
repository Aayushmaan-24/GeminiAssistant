from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiChatWithRealTimeSearch:
    def __init__(self, api_key):
        """Initialize the Gemini client with API key."""
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        self.chat_history = []
        self.chat = None
    
    def initialize_chat(self, system_instruction=""):
        """Initialize a chat session with optional system instruction."""
        config = {}
        if system_instruction:
            config['system_instruction'] = system_instruction
        
        self.chat = self.client.chats.create(
            model=self.model,
            config=config
        )
    
    def enable_real_time_search(self):
        """Enable real-time Google Search capability."""
        search_tool = {'google_search': {}}
        config = {'tools': [search_tool]}
        self.chat = self.client.chats.create(model=self.model, config=config)
    
    def send_message(self, user_message, use_search=False):
        """
        Send a message and get response with optional real-time search.
        
        Args:
            user_message (str): The user's message
            use_search (bool): Whether to enable real-time search for this query
            
        Returns:
            str: The model's response
        """
        if self.chat is None:
            self.initialize_chat()
        
        # If search is needed, reinitialize with search tool
        if use_search:
            self.enable_real_time_search()
        
        # Add user message to history
        self.chat_history.append({"role": "user", "content": user_message})
        
        try:
            # Send message to Gemini
            response = self.chat.send_message(user_message)
            
            # FIXED: Use response.text directly instead of response.candidates.content.parts.text
            assistant_response = response.text
            
            # Add assistant response to history
            self.chat_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        
        except AttributeError as e:
            error_msg = f"Error processing response: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def get_conversation_history(self):
        """Retrieve the full conversation history."""
        return self.chat_history
    
    def clear_history(self):
        """Clear conversation history and start fresh."""
        self.chat_history = []
        self.chat = None
    
    def display_history(self):
        """Display formatted conversation history."""
        for i, message in enumerate(self.chat_history, 1):
            role = message["role"].upper()
            content = message["content"]
            print(f"\n[{i}] {role}:\n{content}")


def main():
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    # Initialize the chatbot
    bot = GeminiChatWithRealTimeSearch(api_key=api_key)
    
    # Set up initial system instruction
    system_msg = "You are a helpful AI assistant with access to real-time information."
    bot.initialize_chat(system_instruction=system_msg)
    
    print("=" * 60)
    print("Gemini Chat with Real-Time Search")
    print("=" * 60)
    
    # Example 1: Regular conversation
    print("\n--- Regular Conversation ---")
    response1 = bot.send_message("What is Python used for?")
    print(f"Bot: {response1}")
    
    response2 = bot.send_message("Can you give me a practical example?")
    print(f"Bot: {response2}")
    
    # Example 2: Real-time search query
    print("\n--- Real-Time Search Query ---")
    response3 = bot.send_message(
        "What is the current price of Bitcoin?",
        use_search=True
    )
    print(f"Bot: {response3}")
    
    # Example 3: Another real-time query
    print("\n--- Weather Query ---")
    response4 = bot.send_message(
        "What is the current weather in Mumbai?",
        use_search=True
    )
    print(f"Bot: {response4}")
    
    # Display full conversation history
    print("\n--- Conversation History ---")
    bot.display_history()


if __name__ == "__main__":
    main()