# My Inference Benchmark Report 

## 1. Summary
Benchmarking different versions of the `TinyLlama-1.1B` model to understand how performance varies across hardware and optimization settings. I tested the Base model on a GPU, and then compared it against my Fine-tuned (QLoRA) and Quantized (GGUF) versions on both CPU and GPU.

## 2. My Performance Results

| Model Type | Device | Context | Latency | TPS | VRAM (GB) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HuggingFace Base** | CUDA (T4) | 512 | 3.51s | **28.53** | 2.06 |
| **HuggingFace Base** | CUDA (T4) | 1024 | 4.15s | 24.18 | 2.06 |
| **HuggingFace Base** | CUDA (T4) | 2048 | 4.54s | 22.14 | 2.06 |
| **GGUF (Q4_0)** | CPU | 512 | 20.89s | 4.88 | 0.00 |
| **GGUF (Q4_0)** | CPU | 1024 | 30.89s | 3.30 | 0.00 |
| **GGUF (Q4_0)** | CPU | 2048 | 56.98s | 1.79 | 0.00 |
| **HF (Fine-tuned)**| CPU | 512 | 40.07s | 2.50 | 0.00 |
| **HF (Fine-tuned)**| CPU | 1024 | 42.52s | 2.35 | 0.00 |
| **HF (Fine-tuned)**| CPU | 2048 | 58.66s | 1.26 | 0.00 |

## 3. What I Learned from Optimizations

### Scaling the Context Window
I noticed that as I increased the context window, the performance took a hit. 
- On the **GPU**, doubling the context only added about **0.6s** of latency. 
- On the **CPU**, it was much worse—doubling the context added over **10 seconds**. This shows me that if I want to handle long conversations, a GPU is almost mandatory.

### Why Quantization Matters
I ran a direct comparison on my local CPU between the standard model and the quantized GGUF version. I found that **quantization made the model nearly 2x faster** (4.88 TPS vs 2.50 TPS) even though they were running on the exact same hardware. This is a huge win for local deployment.

## 4. Hardware Observations
- **GPU (CUDA):** I got great results here with **~28.5 TPS**. The VRAM usage stayed low at **2.06 GB**, which means I could potentially run even larger models on this T4 GPU.
- **CPU:** While I can run models here for free, the speed is much lower. I'd only use this for background tasks or low-priority testing.

## 5. My Analysis of Advanced Techniques

### KV Caching
I enabled KV caching in my script, and it worked exactly as expected. It prevented the model from re-calculating old tokens, which kept my generation times consistent as the replies got longer.

### Speculative Decoding (Theory)
I also looked into Speculative Decoding. It's a cool idea where a tiny "draft model" predicts tokens for a big "target model" to verify. Since my TinyLlama is already so fast, I don't think I need this right now, but I'd definitely use it if I was running a massive 70B model.

### vLLM Engine
I tried to run the vLLM engine, but I hit some compilation errors with the older Tesla T4 hardware. I decided to skip it for now and focus on the HuggingFace and GGUF results which are already quite optimized.
