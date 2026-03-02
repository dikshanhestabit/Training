import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import os

def quantize_model(model_path, output_dir, bits=8):
    print(f"Loading model for {bits}-bit quantization from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    if bits == 8:
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    elif bits == 4:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )
    else:
        raise ValueError("Only 8-bit and 4-bit quantization are supported.")

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    output_path = os.path.join(output_dir, f"model-int{bits}")
    print(f"Saving {bits}-bit quantized model to: {output_path}")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print(f"{bits}-bit quantization complete!")

if __name__ == "__main__":
    MERGED_MODEL_PATH = "./src/merged_model"
    QUANTIZED_DIR = "./src/quantized"
    
    if not os.path.exists(MERGED_MODEL_PATH):
        print(f"Error: Merged model at {MERGED_MODEL_PATH} not found. Please run merge_adapters.py first.")
    else:
        os.makedirs(QUANTIZED_DIR, exist_ok=True)
        # Quantizing 8-bit
        quantize_model(MERGED_MODEL_PATH, QUANTIZED_DIR, bits=8)
        # Quantizing 4-bit
        quantize_model(MERGED_MODEL_PATH, QUANTIZED_DIR, bits=4)
