import math
import numpy as np
from typing import List, Dict, Optional
from src.vectorstore.manager import VectorStoreManager
from src.embeddings.embedder import OpenAIEmbedder

class CustomBM25:
    # Initializing BM25 scoring
    def __init__(self, documents: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents = [doc.lower().split() for doc in documents]
        self.doc_len = [len(doc) for doc in self.documents]
        self.avg_doc_len = sum(self.doc_len) / len(self.documents) if documents else 0
        self.doc_count = len(documents)
        self.idf = self._calculate_idf()

    def _calculate_idf(self) -> Dict[str, float]:
        idf = {}
        all_words = set([word for doc in self.documents for word in doc])
        for word in all_words:
            doc_with_word = sum(1 for doc in self.documents if word in doc)
            idf[word] = math.log((self.doc_count - doc_with_word + 0.5) / (doc_with_word + 0.5) + 1.0)
        return idf

    def get_scores(self, query: str) -> np.ndarray:
        query_words = query.lower().split()
        scores = np.zeros(self.doc_count)
        for word in query_words:
            if word not in self.idf:
                continue
            idf = self.idf[word]
            for i, doc in enumerate(self.documents):
                freq = doc.count(word)
                numerator = idf * freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avg_doc_len)
                scores[i] += numerator / denominator
        return scores

class HybridRetriever:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        self.embedder = OpenAIEmbedder(config_path)
        # Detecting dimension dynamically
        sample_embedding = self.embedder.embed_query("target")
        dimension = len(sample_embedding)
        self.vector_store = VectorStoreManager(dimension=dimension)
        self.vector_store.load()
        
        # Initialize BM25 with current documents in vector store
        texts = [doc['text'] for doc in self.vector_store.metadata_store]
        self.bm25 = CustomBM25(texts)

    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        if not filters:
            return results
        
        filtered = []
        for res in results:
            match = True
            for key, value in filters.items():
                # Check if key exists in metadata and matches value
                if res['metadata'].get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(res)
        return filtered

    def _rrf_combine(self, vector_results: List[Dict], keyword_results: List[Dict], k: int = 60) -> List[Dict]:
        # Combining scores using RRF
        scores = {}
        
        # Unique ID for chunks
        def get_id(doc): return hash(doc['metadata']['text'])

        # Ranking vector results
        for rank, res in enumerate(vector_results):
            doc_id = get_id(res)
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

        # Ranking keyword results
        for rank, res in enumerate(keyword_results):
            doc_id = get_id(res)
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)

        # Merging results
        all_unique_results = {get_id(res): res for res in vector_results + keyword_results}
        
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        # Merging results
        all_unique_results = {get_id(res): res for res in vector_results + keyword_results}
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        
        final_results = []
        for doc_id in sorted_ids:
            res = all_unique_results[doc_id]
            res['rrf_score'] = scores[doc_id]
            final_results.append(res)
        return final_results

    def _mmr(self, query_embedding: List[float], results: List[Dict], top_k: int, lambda_param: float = 0.5) -> List[Dict]:
        # Diversifying results using MMR
        if not results or top_k <= 0: return []
        
        # Helper for cosine similarity
        def cos_sim(a, b):
            a, b = np.array(a), np.array(b)
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

        selected = [results[0]]
        candidates = results[1:]
        
        while len(selected) < top_k and candidates:
            best_score = -float('inf')
            best_idx = -1
            
            for i, cand in enumerate(candidates):
                # Relevance score
                relevance = cos_sim(query_embedding, cand['vector'])
                # Redundancy (max similarity to already selected)
                redundancy = max([cos_sim(cand['vector'], s['vector']) for s in selected])
                
                # MMR Formula
                score = lambda_param * relevance - (1 - lambda_param) * redundancy
                
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            if best_idx != -1:
                selected.append(candidates.pop(best_idx))
            else:
                break
        return selected

    def retrieve(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        # 1. Vector searching
        query_embedding = self.embedder.embed_query(query)
        vector_results = self.vector_store.search(query_embedding, k=20)
        
        # 2. Keyword searching
        bm25_scores = self.bm25.get_scores(query)
        top_keyword_indices = np.argsort(bm25_scores)[-20:][::-1]
        keyword_results = []
        for idx in top_keyword_indices:
            if bm25_scores[idx] > 0:
                # Reconstructing vector for keyword hit to support MMR
                vec = self.vector_store.index.reconstruct(int(idx))
                keyword_results.append({
                    "metadata": self.vector_store.metadata_store[idx],
                    "vector": vec.tolist(),
                    "bm25_score": bm25_scores[idx]
                })

        # 3. Hybrid combining (RRF)
        hybrid_results = self._rrf_combine(vector_results, keyword_results)

        # 4. Applying filters
        filtered_results = self._apply_filters(hybrid_results, filters)

        # 5. Diversifying (MMR)
        return self._mmr(query_embedding, filtered_results, top_k)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--year", type=str, default=None)
    parser.add_argument("--type", type=str, default=None)
    args = parser.parse_args()

    filters = {}
    if args.year: filters["year"] = args.year
    if args.type: filters["type"] = args.type

    retriever = HybridRetriever()
    results = retriever.retrieve(args.query, top_k=5, filters=filters)

    print(f"\n--- Hybrid Retrieval Results for: '{args.query}' ---")
    if filters: print(f"Filters applied: {filters}")
    
    for i, res in enumerate(results):
        print(f"\n[{i+1}] Source: {res['metadata'].get('source', 'Unknown')}")
        print(f"Content: {res['metadata']['text'][:200]}...")
        print(f"RRF Score: {res.get('rrf_score', 'N/A'):.4f}")
