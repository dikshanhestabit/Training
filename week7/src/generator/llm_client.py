import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Handling the model connections and provider logic
class LLMClient:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Loading configurations from yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.provider = self.config.get('provider', 'openai')
        self.model_name = self.config.get('model_name', 'gpt-4o')
        
        # Setting up the OpenAI client (Optional for Day 1)
        if self.provider == "openai":
            api_key = os.getenv(self.config.get('api_key_env', 'OPENAI_API_KEY'))
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                self.client = None
        else:
            # Placeholder for local models like Mistral/Llama
            self.client = None

    # Creating the final response from the LLM
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        return ""
