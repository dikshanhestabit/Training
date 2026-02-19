import os
import yaml
from typing import List, Dict
from src.embeddings.embedder import OpenAIEmbedder
from pypdf import PdfReader

# Loading and chunking the enterprise PDF
class DocumentIngestor:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.chunk_size = self.config.get('chunk_size', 800)
        self.embedder = OpenAIEmbedder(config_path)

    # Extracting text from PDF
    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    # Creating chunks for the vector store
    def split_text(self, text: str, source_name: str) -> List[Dict]:
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append({"content": current_chunk.strip(), "metadata": {"source": source_name}})
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append({"content": current_chunk.strip(), "metadata": {"source": source_name}})
        return chunks

if __name__ == "__main__":
    from src.vectorstore.manager import VectorStoreManager
    
    # Setting the paths
    pdf_path = "src/data/raw/13999998018cc53440310d94a26d1e8957e2277f.pdf"
    
    ingestor = DocumentIngestor()
    
    print(f"Reading PDF: {pdf_path}")
    doc_text = ingestor.load_pdf(pdf_path)
    
    chunks = ingestor.split_text(doc_text, "enterprise_data.pdf")
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    texts = [c['content'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]
    
    # Keeping the text content in metadata for retrieval display
    for i in range(len(metadatas)):
        metadatas[i]['text'] = texts[i]
    
    embeddings = ingestor.embedder.embed_documents(texts)
    
    # Storing vectors locally (384 dimensions for local model)
    store = VectorStoreManager(dimension=384)
    store.add_documents(embeddings, metadatas)
    store.save()
    
    print("Success! index.faiss built.")
