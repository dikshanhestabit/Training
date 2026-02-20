import os
import json
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from transformers import BlipProcessor, BlipForConditionalGeneration
from src.embeddings.clip_embedder import CLIPEmbedder
from src.vectorstore.manager import VectorStoreManager

class ImageIngestor:
    # ingest images and pdfs
    def __init__(self, index_path="src/vectorstore/multimodal_index.faiss"):
        # Initialize models
        print("Initializing Ingestion Models (OCR, BLIP, CLIP)...")
        self.clip_embedder = CLIPEmbedder()
        
        # BLIP for captioning
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        self.index_path = index_path
        # CLIP base patch32 has dimension 512
        self.vector_store = VectorStoreManager(dimension=512, index_path=self.index_path)

    def generate_caption(self, image: Image.Image) -> str:
    # create caption
        inputs = self.blip_processor(image, return_tensors="pt")
        out = self.blip_model.generate(**inputs)
        return self.blip_processor.decode(out[0], skip_special_tokens=True)

    def process_image(self, image_path: str, metadata_ext: dict = None) -> dict:
    # process single image
        img = Image.open(image_path).convert("RGB")
        
        # 1. OCR Extraction
        ocr_text = pytesseract.image_to_string(img).strip()
        
        # 2. Caption Generation
        caption = self.generate_caption(img)
        
        # 3. CLIP Embedding
        embedding = self.clip_embedder.embed_image(image_path)
        
        metadata = {
            "file_path": image_path,
            "ocr_text": ocr_text,
            "caption": caption,
            "type": "image"
        }
        if metadata_ext:
            metadata.update(metadata_ext)
            
        return {
            "embedding": embedding,
            "metadata": metadata
        }

    def process_scanned_pdf(self, pdf_path: str):
    # process pdf pages
        print(f"Processing scanned PDF: {pdf_path}")
        pages = convert_from_path(pdf_path)
        results = []
        
        temp_dir = "src/data/temp_images"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, page in enumerate(pages):
            temp_path = os.path.join(temp_dir, f"temp_page_{i}.png")
            page.save(temp_path, "PNG")
            
            res = self.process_image(temp_path, metadata_ext={
                "source_pdf": pdf_path,
                "page_number": i + 1,
                "type": "pdf_page"
            })
            # Update path to original PDF for reference (or keep temp if desired)
            res["metadata"]["file_path"] = pdf_path 
            results.append(res)
            
            # Clean up temp image
            os.remove(temp_path)
            
        return results

    def ingest_directory(self, directory_path: str):
    # ingest entire folder
        all_embeddings = []
        all_metadata = []
        
        supported_images = ('.png', '.jpg', '.jpeg')
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if filename.lower().endswith(supported_images):
                print(f"Ingesting Image: {filename}")
                res = self.process_image(file_path)
                all_embeddings.append(res["embedding"])
                all_metadata.append(res["metadata"])
                
            elif filename.lower().endswith('.pdf'):
                print(f"Ingesting Scanned PDF: {filename}")
                results = self.process_scanned_pdf(file_path)
                for res in results:
                    all_embeddings.append(res["embedding"])
                    all_metadata.append(res["metadata"])
        
        if all_embeddings:
            print(f"Adding {len(all_embeddings)} vectors to Multimodal Index...")
            self.vector_store.add_documents(all_embeddings, all_metadata)
            self.vector_store.save()
            print("Successfully saved multimodal index.")

if __name__ == "__main__":
    # Ensure raw data directories exist
    os.makedirs("src/data/raw/graphs", exist_ok=True)
    os.makedirs("src/data/raw/forms", exist_ok=True)
    os.makedirs("src/data/raw/scanned_pdfs", exist_ok=True)
    
    ingestor = ImageIngestor()
    
    print("--- Starting Multimodal Ingestion ---")
    
    # Process Graphs
    if os.path.exists("src/data/raw/graphs"):
        ingestor.ingest_directory("src/data/raw/graphs")
        
    # Process Forms
    if os.path.exists("src/data/raw/forms"):
        ingestor.ingest_directory("src/data/raw/forms")
        
    # Process Scanned PDFs
    if os.path.exists("src/data/raw/scanned_pdfs"):
        ingestor.ingest_directory("src/data/raw/scanned_pdfs")

    print("--- Ingestion Complete ---")
