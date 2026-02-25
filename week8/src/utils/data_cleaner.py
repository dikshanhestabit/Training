import json
import os
import argparse
import numpy as np
from transformers import AutoTokenizer
from collections import Counter

class DataCleaner:
    def __init__(self, model_name="Qwen/Qwen2.5-1.5B"):
        print(f"setting up tokenizer for {model_name}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        except Exception as e:
            print(f"Warning: Could not load tokenizer '{model_name}'. Falling back to default whitespace splitter. Error: {e}")
            self.tokenizer = None

    def load_jsonl(self, file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
        return data

    def save_jsonl(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in data:
                f.write(json.dumps(entry) + '\n')
        print(f"Saved {len(data)} samples to {file_path}")

    def get_token_count(self, text):
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        return len(text.split())

    def analyze_dataset(self, data):
        counts = []
        types = []
        
        for entry in data:
            # combining instruction, input, and output for length check
            full_text = entry.get("instruction", "") + entry.get("input", "") + entry.get("output", "")
            counts.append(self.get_token_count(full_text))
            
            # checking if a type exists to track distribution
            if "type" in entry:
                types.append(entry["type"])
            else:
                types.append("unknown")

        stats = {
            "total_samples": len(data),
            "token_stats": {
                "min": int(np.min(counts)) if counts else 0,
                "max": int(np.max(counts)) if counts else 0,
                "mean": float(np.mean(counts)) if counts else 0,
                "median": float(np.median(counts)) if counts else 0,
                "std": float(np.std(counts)) if counts else 0
            },
            "distribution": dict(Counter(types))
        }
        return stats, counts

    def remove_duplicates(self, data):
        seen = set()
        unique_data = []
        duplicates_count = 0
        
        for entry in data:
            # using a string key to find duplicates
            identifier = f"{entry.get('instruction', '')} | {entry.get('input', '')}"
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(entry)
            else:
                duplicates_count += 1
                
        print(f"Removed {duplicates_count} duplicates.")
        return unique_data

    def remove_outliers(self, data, token_counts, threshold_std=3):
        if not token_counts:
            return data
            
        mean = np.mean(token_counts)
        std = np.std(token_counts)
        
        clean_data = []
        outliers_count = 0
        
        for entry, count in zip(data, token_counts):
            if abs(count - mean) <= threshold_std * std:
                clean_data.append(entry)
            else:
                outliers_count += 1
                
        print(f"Removed {outliers_count} outliers (threshold: {threshold_std} stds).")
        return clean_data

def run_cleaning_pipeline(cleaner, input_path, output_path):
    print(f"\n--- processing: {input_path} ---")
    data = cleaner.load_jsonl(input_path)
    
    print("analyzing raw data...")
    stats, counts = cleaner.analyze_dataset(data)
    print(f"initial stats: {json.dumps(stats, indent=2)}")
    
    # Step 1: removing duplicates
    unique_data = cleaner.remove_duplicates(data)
    
    # Step 2: re-calculating counts so we can find outliers
    _, counts = cleaner.analyze_dataset(unique_data)
    
    # Step 3: removing outliers
    clean_data = cleaner.remove_outliers(unique_data, counts)
    
    cleaner.save_jsonl(clean_data, output_path)
    
    print("analyzing cleaned result...")
    clean_stats, _ = cleaner.analyze_dataset(clean_data)
    print(f"cleaned stats: {json.dumps(clean_stats, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="Clean and analyze LLM instruction datasets.")
    parser.add_argument("--input", type=str, help="Path to input JSONL file")
    parser.add_argument("--output", type=str, help="Path to output cleaned JSONL file")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-1.5B", help="Model name for tokenizer")
    
    args = parser.parse_args()
    cleaner = DataCleaner(args.model)

    # if specific files are provided, just do those
    if args.input and args.output:
        run_cleaning_pipeline(cleaner, args.input, args.output)
    else:
        # otherwise, automatically try to clean both train and val in src/data
        files_to_clean = [
            ("src/data/train.jsonl", "src/data/train_clean.jsonl"),
            ("src/data/val.jsonl", "src/data/val_clean.jsonl")
        ]
        
        found_any = False
        for inp, out in files_to_clean:
            if os.path.exists(inp):
                run_cleaning_pipeline(cleaner, inp, out)
                found_any = True
        
        if not found_any:
            print("no default files found in src/data/. please specify --input and --output.")

if __name__ == "__main__":
    main()
