from src.embeddings.embedder import OpenAIEmbedder
from src.vectorstore.manager import VectorStoreManager

# Building the engine to handle user questions
class QueryEngine:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        self.embedder = OpenAIEmbedder(config_path)
        # Detecting dimension automatically
        # openai is 1536, local all-MiniLM-L6-v2 is 384
        dimension = 1536 if self.embedder.provider == "openai" else 384
        self.vector_store = VectorStoreManager(dimension=dimension)
        self.vector_store.load()

    # Searching the retriever for context
    def query(self, question: str, k: int = 5):
        query_embedding = self.embedder.embed_query(question)
        results = self.vector_store.search(query_embedding, k=k)
        return results

if __name__ == "__main__":
    import sys
    
    # Building the engine
    engine = QueryEngine()
    
    # Getting query from command line
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        print(f"Searching for: {user_query}")
        
        results = engine.query(user_query)
        
        # Displaying the results
        for i, res in enumerate(results):
            print(f"\nResult {i+1} (Source: {res['metadata']['source']}):")
            print(f"Content: {res['metadata']['text'][:500]}...") # Showing first 500 chars
            print(f"Match Distance: {res['distance']:.4f}")
    else:
        print("Usage: python -m src.retriever.query_engine 'your question'")
