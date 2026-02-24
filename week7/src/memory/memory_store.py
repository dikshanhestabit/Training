import json
import os

class MemoryStore:
    def __init__(self, storage_path="src/memory/chat_history.json", max_messages=5):
        self.storage_path = storage_path
        self.max_messages = max_messages
        self.history = self._load_history()

    def _load_history(self):
        """Loads chat history from the JSON file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self):
        """Saves current chat history to the JSON file."""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.history, f, indent=4)

    def add_message(self, role, content):
        """Adds a message to history and maintains window size."""
        self.history.append({"role": role, "content": content})
        # Keep only the last N messages (treating a user-assistant pair as 2 messages)
        # The task specifies "Memory for last 5 messages"
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
        self._save_history()

    def get_context_string(self):
        """Returns history as a formatted string for LLM prompts."""
        context = ""
        for msg in self.history:
            role = "User" if msg["role"] == "user" else "AI"
            context += f"{role}: {msg['content']}\n"
        return context

    def clear(self):
        """Clears the history."""
        self.history = []
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)

if __name__ == "__main__":
    # Internal test logic
    memory = MemoryStore(max_messages=5)
    print("Initial History:", memory.get_context_string())
    
    memory.add_message("user", "Hello, who are you?")
    memory.add_message("assistant", "I am your RAG assistant.")
    memory.add_message("user", "What can you do?")
    
    print("\nUpdated History:\n", memory.get_context_string())
    print("Messages Count:", len(memory.history))
