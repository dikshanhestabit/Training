import os
import yaml
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Loading environment variables from .env file
load_dotenv()

# Creating a class to handle local embeddings (Path A)
class OpenAIEmbedder:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Loading configurations from yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.provider = self.config.get('provider', 'local')
        self.model_name = self.config.get('embedding_model', 'all-MiniLM-L6-v2')

        if self.provider == "openai":
            self.api_key = os.getenv(self.config.get('api_key_env', 'OPENAI_API_KEY'))
            # Only initialize OpenAI if key is present
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
            else:
                self.provider = "local" # Fallback to local
        
        if self.provider == "local":
            # Loading a free local model from Sentence-Transformers
            print(f"Initializing Local Embedder: {self.model_name}")
            self.local_model = SentenceTransformer(self.model_name)

    # Generating embeddings for multiple text chunks
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name
            )
            return [data.embedding for data in response.data]
        else:
            # Running local embedding on CPU
            embeddings = self.local_model.encode(texts)
            return embeddings.tolist()

    # Generating embedding for a single user question
    def embed_query(self, text: str) -> List[float]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=[text],
                model=self.model_name
            )
            return response.data[0].embedding
        else:
            # Running local query embedding
            embedding = self.local_model.encode([text])[0]
            return embedding.tolist()
