from src.embeddings.embedder import OpenAIEmbedder
from src.vectorstore.manager import VectorStoreManager

# Engine for user queries
class QueryEngine:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        self.embedder = OpenAIEmbedder(config_path)
        # Dynamic dimension detection
        sample_embedding = self.embedder.embed_query("target")
        dimension = len(sample_embedding)
        self.vector_store = VectorStoreManager(dimension=dimension)
        self.vector_store.load()

    # Searching context
    def query(self, question: str, k: int = 5):
        query_embedding = self.embedder.embed_query(question)
        return self.vector_store.search(query_embedding, k=k)

if __name__ == "__main__":
    import sys
    engine = QueryEngine()
    
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        print(f"Searching for: {user_query}")
        
        results = engine.query(user_query)
        
        # Displaying hits with full metadata
        for i, res in enumerate(results):
            meta = res['metadata']
            print(f"\nResult {i+1}:")
            print(f"Source: {meta.get('source')} | Pages: {meta.get('page_numbers')}")
            print(f"Year: {meta.get('year')} | Type: {meta.get('type')} | Tags: {meta.get('tags')}")
            print(f"Content: {meta['text'][:400]}...")
            print(f"Distance: {res['distance']:.4f}")
    else:
        print("Usage: python -m src.retriever.query_engine 'question'")
