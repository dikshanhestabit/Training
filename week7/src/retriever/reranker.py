import numpy as np
from typing import List, Dict
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        # Initializing the reranker
        self.model_name = model_name
        try:
            print(f"Loading Reranking Model: {self.model_name}")
            self.model = CrossEncoder(model_name)
            self.available = True
        except Exception as e:
            print(f"Warning: Could not load CrossEncoder model. Falling back to simple scoring. Error: {e}")
            self.available = False

    def rerank(self, query: str, results: List[Dict]) -> List[Dict]:
        # Reranking retrieved results
        if not results:
            return []

        if not self.available:
            # Fallback: Just return results as they are (already sorted by distance)
            return results

        # Prepare pairs for the Cross-Encoder: (query, document_text)
        pairs = [[query, res['metadata']['text']] for res in results]
        
        # Calculate scores
        scores = self.model.predict(pairs)
        
        # Attach scores to results
        for res, score in zip(results, scores):
            res['rerank_score'] = float(score)
            
        # Sort results by rerank score (descending)
        reranked_results = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
        
        return reranked_results

if __name__ == "__main__":
    # Quick test harness
    test_query = "Explain how credit underwriting works"
    test_results = [
        {"metadata": {"text": "Credit underwriting is the process of evaluating a borrower's creditworthiness.", "source": "doc1"}},
        {"metadata": {"text": "The weather today is sunny with a chance of rain.", "source": "doc2"}},
        {"metadata": {"text": "Underwriting involves checking income, debt, and credit history.", "source": "doc3"}}
    ]
    
    reranker = Reranker()
    final_results = reranker.rerank(test_query, test_results)
    
    print("\n--- Reranking Results ---")
    for i, res in enumerate(final_results):
        score = res.get('rerank_score', 'N/A')
        print(f"{i+1}. Score: {score:.4f} | Content: {res['metadata']['text'][:100]}...")
