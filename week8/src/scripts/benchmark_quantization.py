import os
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from llama_cpp import Llama # requires pip install llama-cpp-python

def get_model_size(model_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(model_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024**3) # Size in GB

def benchmark_transformers_model(model_name_or_path, bits=None):
    print(f"\nBenchmarking {model_name_or_path} ({bits if bits else 'FP16'})")
    
    # Loading model
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    
    if bits == 8:
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    elif bits == 4:
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    else:
        quantization_config = None

    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Running warmup
    prompt = "Explain the difference between Python and Java."
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    _ = model.generate(**inputs, max_new_tokens=1)
    
    # Benchmarking
    start_time = time.time()
    outputs = model.generate(**inputs, max_new_tokens=100)
    end_time = time.time()
    
    duration = end_time - start_time
    num_tokens = outputs.shape[1] - inputs.input_ids.shape[1]
    speed = num_tokens / duration
    
    print(f"Speed: {speed:.2f} tokens/s")
    print(f"Size: {get_model_size(model_name_or_path):.2f} GB")
    
    return {"speed": speed, "size": get_model_size(model_name_or_path)}

def benchmark_gguf_model(gguf_path):
    print(f"\nBenchmarking GGUF: {gguf_path}")
    
    llm = Llama(model_path=gguf_path, n_ctx=512)
    
    prompt = "Explain the difference between Python and Java."
    
    # Running warmup
    _ = llm(prompt, max_tokens=1)
    
    start_time = time.time()
    response = llm(prompt, max_tokens=100)
    end_time = time.time()
    
    duration = end_time - start_time
    num_tokens = response["usage"]["completion_tokens"]
    speed = num_tokens / duration
    
    print(f"Speed: {speed:.2f} tokens/s")
    print(f"Size: {os.path.getsize(gguf_path) / (1024**3):.2f} GB")
    
    return {"speed": speed, "size": os.path.getsize(gguf_path) / (1024**3)}

if __name__ == "__main__":
    MODELS = {
        "FP16": "./src/merged_model",
        "INT8": "./src/quantized/model-int8",
        "INT4": "./src/quantized/model-int4",
        "GGUF": "./src/quantized/model.gguf"
    }
    
    results = {}
    
    for name, path in MODELS.items():
        if not os.path.exists(path):
            print(f"Skipping {name}, path not found: {path}")
            continue
            
        if name == "FP16":
            results[name] = benchmark_transformers_model(path)
        elif name == "INT8":
            results[name] = benchmark_transformers_model(path, bits=8)
        elif name == "INT4":
            results[name] = benchmark_transformers_model(path, bits=4)
        elif name == "GGUF":
            results[name] = benchmark_gguf_model(path)
            
    print("\nBenchmark Summary:")
    for name, metrics in results.items():
        print(f"{name}: Size={metrics['size']:.2f}GB, Speed={metrics['speed']:.2f}tok/s")
