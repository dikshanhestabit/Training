import time
import uuid
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.deploy.config import settings
from src.deploy.model_loader import model_loader

# Setting up the logger for the app
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Local LLM API",
    description="A deployable local LLM microservice for RAG and Agents.",
    version="1.0.0"
)

# --- Defining request and response models ---

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = Field(default=settings.DEFAULT_MAX_TOKENS)
    temperature: Optional[float] = Field(default=settings.DEFAULT_TEMPERATURE)
    top_p: Optional[float] = Field(default=settings.DEFAULT_TOP_P)
    top_k: Optional[int] = Field(default=settings.DEFAULT_TOP_K)
    stream: Optional[bool] = False

class ChatMessage(BaseModel):
    role: str # "system", "user", "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = Field(default=settings.DEFAULT_MAX_TOKENS)
    temperature: Optional[float] = Field(default=settings.DEFAULT_TEMPERATURE)
    top_p: Optional[float] = Field(default=settings.DEFAULT_TOP_P)
    top_k: Optional[int] = Field(default=settings.DEFAULT_TOP_K)
    stream: Optional[bool] = False

# --- Creating helper functions for prompt formatting ---

def format_chat_prompt(messages: List[ChatMessage]) -> str:
    """Formats messages into a prompt string for TinyLlama Chat template."""
    formatted_prompt = ""
    for msg in messages:
        if msg.role == "system":
            formatted_prompt += f"<|system|>\n{msg.content}</s>\n"
        elif msg.role == "user":
            formatted_prompt += f"<|user|>\n{msg.content}</s>\n"
        elif msg.role == "assistant":
            formatted_prompt += f"<|assistant|>\n{msg.content}</s>\n"
    
    # Ensure it ends with <|assistant|> for the model to complete
    if not formatted_prompt.endswith("<|assistant|>\n"):
        formatted_prompt += "<|assistant|>\n"
    
    return formatted_prompt

# --- Defining API endpoints ---

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": settings.MODEL_PATH}

@app.post("/generate")
async def generate_text(request: GenerateRequest, raw_req: Request):
    req_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"[{req_id}] Generate request received.")

    llm = model_loader.get_model()

    if request.stream:
        def stream_generator():
            for output in llm(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                stream=True
            ):
                token = output["choices"][0]["text"]
                yield token
            
            duration = time.time() - start_time
            logger.info(f"[{req_id}] Stream completed in {duration:.2f}s")

        return StreamingResponse(stream_generator(), media_type="text/plain")

    else:
        output = llm(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )
        
        duration = time.time() - start_time
        result = output["choices"][0]["text"]
        logger.info(f"[{req_id}] Request completed in {duration:.2f}s")
        return {"id": req_id, "text": result, "duration": duration}

@app.post("/chat")
async def chat_completion(request: ChatRequest, raw_req: Request):
    req_id = str(uuid.uuid4())
    start_time = time.time()
    logger.info(f"[{req_id}] Chat request received with {len(request.messages)} messages.")

    prompt = format_chat_prompt(request.messages)
    llm = model_loader.get_model()

    if request.stream:
        def chat_stream_generator():
            for output in llm(
                prompt=prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                top_k=request.top_k,
                stream=True
            ):
                token = output["choices"][0]["text"]
                yield token
            
            duration = time.time() - start_time
            logger.info(f"[{req_id}] Chat stream completed in {duration:.2f}s")

        return StreamingResponse(chat_stream_generator(), media_type="text/plain")

    else:
        output = llm(
            prompt=prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k
        )
        
        duration = time.time() - start_time
        result = output["choices"][0]["text"]
        logger.info(f"[{req_id}] Chat request completed in {duration:.2f}s")
        return {
            "id": req_id, 
            "message": {"role": "assistant", "content": result},
            "duration": duration
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
