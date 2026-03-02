import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def merge_lora_adapters(base_model_name, adapter_path, output_path):
    print(f"Loading base model: {base_model_name}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    
    # Loading model
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"Loading adapters from: {adapter_path}")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    
    # Merging weights
    merged_model = model.merge_and_unload()
    
    # Saving model
    print(f"Saving merged model to: {output_path}")
    merged_model.save_pretrained(output_path)
    
    # Saving tokenizers
    tokenizer_slow = AutoTokenizer.from_pretrained(base_model_name, use_fast=False)
    tokenizer_slow.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    
    print("Merge complete!")

if __name__ == "__main__":
    BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    ADAPTER_PATH = "./src/adapters"
    OUTPUT_PATH = "./src/merged_model"
    
    if not os.path.exists(ADAPTER_PATH):
        print(f"Error: Adapter path {ADAPTER_PATH} not found.")
    else:
        merge_lora_adapters(BASE_MODEL, ADAPTER_PATH, OUTPUT_PATH)
