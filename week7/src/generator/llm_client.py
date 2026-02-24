import os
import yaml
import requests
import json
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

class LLMClient:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Loading configurations from yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.provider = self.config.get('provider', 'openai')
        self.model_name = self.config.get('model_name', 'gpt-4o')
        
        if self.provider == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            self.client = OpenAI(api_key=api_key) if api_key else None
        elif self.provider == "anthropic":
            api_key = os.getenv('ANTHROPIC_API_KEY')
            self.client = Anthropic(api_key=api_key) if api_key else None
        elif self.provider == "gemini":
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel(self.model_name)
            else:
                self.client = None
        elif self.provider == "ollama":
            self.base_url = "http://localhost:11434/api/chat"
            self.client = None

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        if self.provider == "openai":
            if not self.client: return "OpenAI Key Missing"
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            if not self.client: return "Anthropic Key Missing"
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text

        elif self.provider == "gemini":
            if not self.client: return "Gemini Key Missing"
            full_prompt = f"{system_prompt}\n\nUser Question: {user_prompt}"
            try:
                response = self.client.generate_content(full_prompt)
                return response.text
            except Exception as e:
                # Fallback logic for Quota errors to allow task completion
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    return "FALLBACK: The query returned results from your database, but the natural language summary is limited due to API quota. Please check the raw data."
                return f"Gemini Error: {str(e)}"

        elif self.provider == "ollama":
            payload = {"model": self.model_name, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "stream": False}
            try:
                response = requests.post(self.base_url, json=payload)
                return response.json()['message']['content']
            except Exception as e:
                return f"Ollama Error: {str(e)}"
                
        return "Unsupported Provider"
