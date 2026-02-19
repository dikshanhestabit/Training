import sys
import yaml
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.pipelines.context_builder import ContextBuilder

# Integrated pipeline for Day 2 improvements
class IntegratedRAG:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Initializing components
        self.retriever = HybridRetriever(config_path)
        self.reranker = Reranker()
        self.builder = ContextBuilder(max_chars=10000)

    # Executing the full retrieval chain
    def run(self, query: str, top_k: int = 5, filters=None):
        print(f"\n--- Processing Query: '{query}' ---")
        
        # 1. Hybrid Retrieval + MMR
        print("1. Performing Hybrid Retrieval & MMR Diversification...")
        raw_results = self.retriever.retrieve(query, top_k=10, filters=filters)
        
        # 2. Reranking
        print("2. Reranking results with Cross-Encoder...")
        reranked = self.reranker.rerank(query, raw_results)
        
        # 3. Context Building
        print("3. Building final context window...")
        final_results = reranked[:top_k]
        context = self.builder.build_context(final_results)
        
        return context, final_results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.retriever.integrated_rag 'query'")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    rag = IntegratedRAG()
    context, hits = rag.run(query)
    
    print("\n--- Top Reranked Context (Final Output) ---")
    print(context)
    
    print("\n--- Retrieval Debug Info ---")
    for i, h in enumerate(hits):
        print(f"[{i+1}] Source: {h['metadata']['source']} | Score: {h.get('rerank_score', 0):.4f}")
