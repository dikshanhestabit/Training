# Week 8 Capstone: Local LLM API

This project provides a deployable local LLM microservice built with FastAPI and `llama-cpp-python`. It is optimized for the quantized **TinyLlama-1.1B** model fine-tuned for polyglot coding instructions.

## Features
- **FastAPI Inference Server**: High-performance asynchronous API.
- **Quantized Model Support**: Uses GGUF format for low memory footprint (~600MB).
- **Infinite Chat Mode**: Supports multi-turn conversations via a `messages` history.
- **Streamed Generations**: Real-time token streaming for better UX.
- **Advanced Controls**: Full control over `temperature`, `top_p`, `top_k`, and `max_tokens`.
- **Production Ready**: Includes request logging, unique IDs, and a `DOCKERFILE`.

## Setup & Installation

### 1. Local Setup
```bash
# Install dependencies
pip install -r requirements.txt
pip install pydantic-settings llama-cpp-python

# Start the server
uvicorn src.deploy.app:app --host 0.0.0.0 --port 8000
```

### 2. Docker Setup
```bash
# Build the image
docker build -t local-llm-api .

# Run the container
docker run -p 8000:8000 local-llm-api
```

## API Endpoints

### `POST /generate`
Basic text completion.

**Payload:**
```json
{
  "prompt": "Write a Python function to reverse a string.",
  "max_tokens": 128,
  "temperature": 0.7,
  "top_k": 40,
  "stream": false
}
```

### `POST /chat`
Multi-turn conversation (OpenAI-compatible style).

**Payload:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "How do I use a dictionary in Python?"},
    {"role": "assistant", "content": "You can use a dictionary by..."},
    {"role": "user", "content": "Give me an example."}
  ],
  "temperature": 0.8,
  "stream": true
}
```

## Configuration
Configuration is managed in `src/deploy/config.py` and can be overridden via environment variables:
- `MODEL_PATH`: Path to the `.gguf` model file.
- `LOG_LEVEL`: Logging level (DEBUG, INFO, etc.).
- `PORT`: API port (default 8000).
