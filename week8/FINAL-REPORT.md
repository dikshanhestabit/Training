# Week 8 Final Report

## 1. Executive Summary
This week focused on the end-to-end lifecycle of an LLM: from dataset preparation and fine-tuning to quantization and production-ready deployment as a microservice. The target was a polyglot coding assistant based on TinyLlama-1.1B.

## 2. Phase 1: QLoRA Fine-Tuning
- **Base Model**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`.
- **Technique**: QLoRA (4-bit quantization with LoRA adapters).
- **Optimization**: Successfully bypassed T4 GPU `BFloat16` limitations by casting tensors to `Float16`.
- **Outcome**: Model loss decreased from **2.16** to **0.11**, indicating successful domain adaptation for coding tasks.

## 3. Phase 2: Quantization & Optimization
- **Methods**: Compared FP16, INT8, INT4 (NF4), and GGUF.
- **Results**: 
    - **GGUF (Q4_0)** offered the best trade-off for edge deployment, reducing model size by ~70% (from 2.05GB to 0.59GB).
    - **INT4 (NF4)** provided the best balance of speed and memory on GPU (19 tok/s).
- **Conversion**: Fine-tuned adapters were merged with the base model and converted to GGUF using `llama.cpp`.

## 4. Phase 3: Deployment (Capstone)
- **Microservice**: Built a FastAPI inference server.
- **Capabilities**:
    - **Chat Endpoint**: Supports multi-turn (infinite) chat by maintaining conversation state in the request history.
    - **Streaming**: Implemented server-side events for real-time token generation.
    - **Containerization**: Provided a `DOCKERFILE` for consistent deployment across environments.
- **Architecture**: Separated configuration, model loading (singleton pattern), and API logic for maintainability.

## 5. Conclusion
The project demonstrates that small language models (SLMs) like TinyLlama can be effectively fine-tuned and quantized to run efficiently on commodity hardware (CPU or low-tier GPU) while maintaining high utility for specialized domains like coding.

