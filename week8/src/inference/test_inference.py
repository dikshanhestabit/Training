import os
os.environ["VLLM_USE_V1"] = "0"
import torch
import time
import argparse
import csv
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

# Checking if llama-cpp is available for GGUF
try:
    from llama_cpp import Llama
except ImportError:
    print("llama-cpp-python not installed. GGUF support disabled.")
    Llama = None

# Checking if vLLM is available for optimized inference
try:
    from vllm import LLM, SamplingParams
except ImportError:
    print("vLLM not installed. vLLM support disabled.")
    LLM = None

# Getting current VRAM usage to track GPU memory
def get_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        return torch.cuda.max_memory_allocated() / (1024 ** 3)  # GB
    return 0

# Running the core benchmark for a specific model and context window
def conduct_benchmark(model, tokenizer, prompt, model_type, device, max_new_tokens=100, stream=False, context_window=512):
    print(f"\n--- Benchmarking {model_type} on {device} (Context: {context_window}) ---")
    
    # Using a conservative heuristic to fill the context window without overshooting
    safe_chars = (context_window - max_new_tokens - 100) * 3
    dummy_text = "filler " * (max(0, safe_chars) // 7)
    full_prompt = dummy_text + "\n\nQuestion: " + prompt + "\nAnswer:"
    
    if model_type == "hf":
        # Preparing inputs for HuggingFace models
        inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=context_window - max_new_tokens).to(device)
        input_len = inputs["input_ids"].shape[1]
        
        # Setting up streamer if I want to see tokens in real-time
        streamer = TextStreamer(tokenizer, skip_prompt=True) if stream else None
        
        # Generating tokens and measuring performance
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                min_new_tokens=max_new_tokens // 2,
                streamer=streamer,
                use_cache=True,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        output_len = outputs.shape[1]
        tokens_generated = output_len - input_len
        
    elif model_type == "gguf":
        if Llama is None: return None
        # Calling llama.cpp for GGUF inference
        output = model(
            full_prompt,
            max_tokens=max_new_tokens,
            echo=False,
            stream=stream,
            temperature=0.7
        )
        
        if stream:
            tokens_generated = 0
            for chunk in output:
                text = chunk['choices'][0]['text']
                if text:
                    print(text, end="", flush=True)
                    tokens_generated += 1
            print()
        else:
            tokens_generated = len(tokenizer.encode(output['choices'][0]['text']))
            
    elif model_type == "vllm":
        if LLM is None: return None
        # Using PagedAttention via vLLM for high throughput
        sampling_params = SamplingParams(max_tokens=max_new_tokens, temperature=0.7, min_tokens=max_new_tokens // 2)
        outputs = model.generate([full_prompt], sampling_params)
        tokens_generated = len(outputs[0].outputs[0].token_ids)
        
    return tokens_generated

# Starting the main execution flow
def main():
    # Setting up command line arguments
    parser = argparse.ArgumentParser(description="My LLM Inference Benchmarking Tool")
    parser.add_argument("--model_path", type=str, required=True, help="Path to model or model ID")
    parser.add_argument("--model_type", type=str, choices=["hf", "gguf", "vllm"], default="hf")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--stream", action="store_true", help="Enable token streaming")
    parser.add_argument("--context_windows", type=int, nargs="+", default=[512, 1024, 2048], help="Context windows to test")
    
    args = parser.parse_args()
    
    # Picking the right device based on my hardware
    device = torch.device(args.device if torch.cuda.is_available() or args.device == "cpu" else "cpu")
    print(f"Using device: {device}")

    tokenizer = None
    model = None
    
    # Loading the selected model type
    if args.model_type == "hf":
        print(f"Loading HF model: {args.model_path}")
        try:
            tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
        except Exception as e:
            # Falling back to base tokenizer if my fine-tuned one is missing
            print(f"Warning: Tokenizer load failed. Trying Base TinyLlama tokenizer.")
            tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            args.model_path, 
            torch_dtype=torch.float16 if args.device == "cuda" else torch.float32,
            device_map=device if args.device == "cuda" else None,
            trust_remote_code=True
        )
    elif args.model_type == "gguf":
        print(f"Loading GGUF model: {args.model_path}")
        # Initializing llama.cpp with my preferred context length
        model = Llama(model_path=args.model_path, n_ctx=max(args.context_windows))
        tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    elif args.model_type == "vllm":
        print(f"Loading vLLM model: {args.model_path}")
        # Forcing float16 and eager mode for T4 GPU compatibility
        model = LLM(
            model=args.model_path, 
            dtype="float16", 
            enforce_eager=True,
            gpu_memory_utilization=0.8
        )
        tokenizer = None

    # Defining test prompts for benchmarking
    test_prompts = [
        "Write a 3-paragraph essay on the history of the internet."
    ]
    
    results = []
    
    # Iterating through different context windows to measure scaling
    for cw in args.context_windows:
        for prompt in test_prompts:
            # Running a quick warm-up if I'm using HuggingFace
            if args.model_type == "hf":
                 _ = model.generate(**tokenizer("Warm up", return_tensors="pt").to(device), max_new_tokens=5)
            
            # Recording start time for precise measurement
            start_time = time.perf_counter()
            tokens = conduct_benchmark(model, tokenizer, prompt, args.model_type, args.device, context_window=cw, stream=args.stream, max_new_tokens=100)
            end_time = time.perf_counter()
            
            # Calculating final metrics
            duration = end_time - start_time
            tps = tokens / duration if duration > 0 else 0
            vram = get_gpu_memory()
            
            print(f"Results: {tokens} tokens, {duration:.2f}s, {tps:.2f} tokens/s, {vram:.2f} GB VRAM")
            
            results.append({
                "model_type": args.model_type,
                "device": args.device,
                "context_window": cw,
                "tokens_generated": tokens,
                "duration": duration,
                "tps": tps,
                "vram_gb": vram
            })

    # Appending results to my CSV file for logging
    os.makedirs("src/benchmarks", exist_ok=True)
    with open("src/benchmarks/results.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model_type", "device", "context_window", "tokens_generated", "duration", "tps", "vram_gb"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
