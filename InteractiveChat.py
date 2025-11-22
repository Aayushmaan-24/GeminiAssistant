from google import genai
import os
from dotenv import load_dotenv

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
        """
        if self.chat is None:
            self.initialize_chat()
        
        if use_search:
            self.enable_real_time_search()
        
        self.chat_history.append({"role": "user", "content": user_message})
        
        try:
            response = self.chat.send_message(user_message)
            assistant_response = response.text
            
            self.chat_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
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
        if not self.chat_history:
            print("No conversation history yet.")
            return
        
        print("\n" + "=" * 60)
        print("CONVERSATION HISTORY")
        print("=" * 60)
        
        for i, message in enumerate(self.chat_history, 1):
            role = message["role"].upper()
            content = message["content"]
            print(f"\n[{i}] {role}:")
            print(f"{content[:200]}..." if len(content) > 200 else content)


def interactive_chat():
    """Interactive chat interface."""
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    bot = GeminiChatWithRealTimeSearch(api_key=api_key)
    system_msg = "You are a helpful AI assistant with access to real-time information."
    bot.initialize_chat(system_instruction=system_msg)
    
    print("=" * 60)
    print("Gemini Chat with Real-Time Search - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  'search' - Use real-time search for your next query")
    print("  'history' - View full conversation history")
    print("  'clear' - Clear conversation history")
    print("  'exit' - Exit the chat")
    print("\n" + "=" * 60 + "\n")
    
    use_search = False
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break
            
            elif user_input.lower() == "history":
                bot.display_history()
                continue
            
            elif user_input.lower() == "clear":
                bot.clear_history()
                print("\n✓ Conversation history cleared.\n")
                continue
            
            elif user_input.lower() == "search":
                use_search = True
                print("🔍 Real-time search enabled for next query. Ask your question:")
                continue
            
            # Send message
            print("\n⏳ Processing...\n")
            response = bot.send_message(user_input, use_search=use_search)
            
            # Reset search flag
            use_search = False
            
            print(f"Bot: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break


if __name__ == "__main__":
    interactive_chat()