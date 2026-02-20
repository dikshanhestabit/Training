from src.embeddings.clip_embedder import CLIPEmbedder
from src.vectorstore.manager import VectorStoreManager

class ImageSearchRetriever:
    # multimodal retriever
    def __init__(self, index_path="src/vectorstore/multimodal_index.faiss"):
        self.clip_embedder = CLIPEmbedder()
        # CLIP dimension is 512
        self.vector_store = VectorStoreManager(dimension=512, index_path=index_path)
        self.vector_store.load()

    def search_by_text(self, query_text: str, k: int = 5):
    # search by text
        print(f"Searching for: '{query_text}'")
        query_embedding = self.clip_embedder.embed_text(query_text)[0]
        results = self.vector_store.search(query_embedding, k=k)
        return results

    def search_by_image(self, image_path: str, k: int = 5):
    # search by image
        print(f"Searching with image: {image_path}")
        query_embedding = self.clip_embedder.embed_image(image_path)
        results = self.vector_store.search(query_embedding, k=k)
        return results

    def get_text_answer(self, query_text: str, k: int = 3):
    # get text answer from images
        results = self.search_by_text(query_text, k=k)
        
        context_parts = []
        for i, res in enumerate(results):
            meta = res['metadata']
            context_parts.append(
                f"Result {i+1}:\n"
                f"- Caption: {meta['caption']}\n"
                f"- OCR Text: {meta['ocr_text'][:200]}..."
            )
        
        return "\n\n".join(context_parts)

if __name__ == "__main__":
    # Example search logic (not executed)
    searcher = ImageSearchRetriever()
    # results = searcher.search_by_text("A bar chart showing profit")
    # print(results)
