import os
import yaml
from typing import List, Dict, Tuple
from src.embeddings.embedder import OpenAIEmbedder
from pypdf import PdfReader

# Loading and splitting documents
class DocumentIngestor:
    def __init__(self, config_path: str = "src/config/model.yaml"):
        # Loading configurations
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.chunk_size_tokens = self.config.get('chunk_size_tokens', 800)
        self.embedder = OpenAIEmbedder(config_path)
        
        # Using the transformer tokenizer for accurate counting
        if self.embedder.provider == "local":
            self.tokenizer = self.embedder.local_model.tokenizer
        else:
            # Fallback for OpenAI or if tokenizer not available
            import transformers
            self.tokenizer = transformers.AutoTokenizer.from_pretrained("gpt2")

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    # Extracting text from PDF with page numbers
    def load_pdf(self, file_path: str) -> List[Tuple[int, str]]:
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append((i + 1, text))
        return pages

    # Creating chunks based on token count with sliding window overlap
    def split_text(self, pages: List[Tuple[int, str]], source_name: str, year: str, doc_type: str, tags: List[str]) -> List[Dict]:
        overlap_size = self.config.get('chunk_overlap_tokens', 80)
        chunks = []
        
        # Combine all text into a single stream of tokens with page mapping
        all_tokens = []
        token_to_page = []
        
        for page_num, page_text in pages:
            tokens = self.tokenizer.encode(page_text)
            all_tokens.extend(tokens)
            token_to_page.extend([page_num] * len(tokens))
            
        # Sliding window approach
        start_idx = 0
        while start_idx < len(all_tokens):
            end_idx = min(start_idx + self.chunk_size_tokens, len(all_tokens))
            chunk_tokens = all_tokens[start_idx:end_idx]
            
            # Decode tokens back to text
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            # Identify pages covered by this chunk
            chunk_pages = sorted(list(set(token_to_page[start_idx:end_idx])))
            
            chunks.append({
                "content": chunk_text.strip(),
                "metadata": {
                    "source": source_name,
                    "page_numbers": chunk_pages,
                    "year": year,
                    "type": doc_type,
                    "tags": tags
                }
            })
            
            # Move window based on size and overlap
            # If we reached the end, break
            if end_idx == len(all_tokens):
                break
            start_idx += (self.chunk_size_tokens - overlap_size)
            
        return chunks

if __name__ == "__main__":
    import json
    from src.vectorstore.manager import VectorStoreManager
    
    # Path settings
    pdf_path = "src/data/raw/13999998018cc53440310d94a26d1e8957e2277f.pdf"
    cleaned_dir = "src/data/cleaned"
    chunks_dir = "src/data/chunks"
    
    # Creating dirs
    os.makedirs(cleaned_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)
    
    ingestor = DocumentIngestor()
    
    print(f"Reading PDF: {pdf_path}")
    pages = ingestor.load_pdf(pdf_path)
    
    # Saving cleaned text
    full_text = "\n\n".join([p[1] for p in pages])
    with open(f"{cleaned_dir}/enterprise_data.txt", "w") as f:
        f.write(full_text)
    print(f"Saved cleaned text to {cleaned_dir}")
    
    # Chunking with metadata
    chunks = ingestor.split_text(
        pages=pages,
        source_name="enterprise_data.pdf",
        year="2024",
        doc_type="financial_report",
        tags=["sec", "10-k", "annual_report"]
    )
    
    # Saving chunks to disk
    with open(f"{chunks_dir}/enterprise_data_chunks.json", "w") as f:
        json.dump(chunks, f, indent=4)
    print(f"Saved {len(chunks)} chunks to {chunks_dir}")
    
    texts = [c['content'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]
    
    # Including text in metadata
    for i in range(len(metadatas)):
        metadatas[i]['text'] = texts[i]
    
    print(f"Generating embeddings using {ingestor.embedder.model_name}...")
    embeddings = ingestor.embedder.embed_documents(texts)
    
    # Storing vectors locally (Dynamically detect dimension)
    dimension = len(embeddings[0])
    print(f"Detected Dimension: {dimension}")
    
    store = VectorStoreManager(dimension=dimension)
    store.add_documents(embeddings, metadatas)
    store.save()
    
    print("Success! index.faiss built with comprehensive metadata, token-based chunking, and overlap.")
