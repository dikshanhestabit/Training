import faiss
import numpy as np
import pickle
import os
from typing import List, Dict

# Managing the FAISS indexes and metadata
class VectorStoreManager:
    def __init__(self, dimension: int = 1536, index_path: str = "src/vectorstore/index.faiss"):
        self.index_path = index_path
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata_store = []

    # Adding new vectors and their info to memory
    def add_documents(self, embeddings: List[List[float]], metadata: List[Dict]):
        embedding_np = np.array(embeddings).astype('float32')
        self.index.add(embedding_np)
        self.metadata_store.extend(metadata)

    # Saving the index to local files
    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".pkl", "wb") as f:
            pickle.dump(self.metadata_store, f)

    # Loading the saved index from disk
    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.index_path + ".pkl", "rb") as f:
                self.metadata_store = pickle.load(f)

    # Searching for matches
    def search(self, query_embedding: List[float], k: int = 5):
        query_np = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1:
                # Reconstructing the vector from index
                vec = self.index.reconstruct(int(idx))
                results.append({
                    "metadata": self.metadata_store[idx],
                    "vector": vec.tolist(),
                    "distance": float(distances[0][i])
                })
        return results
