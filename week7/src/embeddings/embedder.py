import os
import yaml
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Loading environment variables from .env file
load_dotenv()

# Embedding class for local and openai models
class OpenAIEmbedder:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Loading model configurations
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.provider = self.config.get('embedding_provider', self.config.get('provider', 'local'))
        self.model_name = self.config.get('embedding_model', 'all-MiniLM-L6-v2')

        if self.provider == "openai":
            self.api_key = os.getenv(self.config.get('api_key_env', 'OPENAI_API_KEY'))
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
            else:
                self.provider = "local"
        
        elif self.provider == "gemini":
            import google.generativeai as genai
            self.api_key = os.getenv('GEMINI_API_KEY')
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model_name = self.config.get('embedding_model', "models/embedding-001")
            else:
                self.provider = "local"

        if self.provider == "local":
            # Loading a free local model from Sentence-Transformers
            print(f"Initializing Local Embedder: {self.model_name}")
            self.local_model = SentenceTransformer(self.model_name)
        elif self.provider not in ["openai", "gemini"]:
             # Default to local if provider is unknown
            print(f"Unknown provider '{self.provider}', falling back to local.")
            self.provider = "local"
            self.local_model = SentenceTransformer(self.config.get('embedding_model', 'all-MiniLM-L6-v2'))

    # Embedding document batches
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name
            )
            return [data.embedding for data in response.data]
        elif self.provider == "gemini":
            import google.generativeai as genai
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document"
            )
            return result['embedding']
        else:
            # Local encoding
            embeddings = self.local_model.encode(texts)
            return embeddings.tolist()

    # Embedding individual queries
    def embed_query(self, text: str) -> List[float]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                input=[text],
                model=self.model_name
            )
            return response.data[0].embedding
        elif self.provider == "gemini":
            import google.generativeai as genai
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        else:
            # Local query encoding
            embedding = self.local_model.encode([text])[0]
            return embedding.tolist()
