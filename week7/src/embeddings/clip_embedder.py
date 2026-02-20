import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Union

class CLIPEmbedder:
    # creating clip model
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading CLIP model: {model_name} on {self.device}...")
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_text(self, texts: Union[str, List[str]]) -> List[List[float]]:
    # embedding texts
        if isinstance(texts, str):
            texts = [texts]
        
        inputs = self.processor(text=texts, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            # Extract text features manually to ensure we get the projected tensor
            text_outputs = self.model.text_model(**inputs)
            text_features = self.model.text_projection(text_outputs.pooler_output)
        
        # Normalize features
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
        return text_features.cpu().numpy().tolist()

    def embed_image(self, image_path: str) -> List[float]:
    # embedding images
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            # Extract vision features manually to ensure we get the projected tensor
            vision_outputs = self.model.vision_model(**inputs)
            image_features = self.model.visual_projection(vision_outputs.pooler_output)
        
        # Normalize features
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        return image_features.cpu().numpy()[0].tolist()

if __name__ == "__main__":
    # Internal test check
    embedder = CLIPEmbedder()
    print("CLIP Embedder initialized successfully.")
