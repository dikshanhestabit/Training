from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime
from src.retriever.advanced_rag import AdvancedRAG
from src.retriever.image_search import ImageSearchRetriever
from src.pipelines.sql_pipeline import SQLPipeline

app = FastAPI(title="Week 7 Capstone - Advanced RAG API")

# Initializing components
adv_rag = AdvancedRAG()
image_rag = ImageSearchRetriever()
sql_pipe = SQLPipeline(db_path="src/data/customers.db")

LOG_FILE = "CHAT-LOGS.json"

class QueryRequest(BaseModel):
    query: str

def log_transaction(endpoint, request_data, response_data):
    """Logs every request and response to a flat JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "request": request_data,
        "response": response_data
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
            
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

@app.get("/")
def read_root():
    return {"message": "Capstone RAG API is live."}

@app.post("/ask")
def ask(req: QueryRequest):
    try:
        result = adv_rag.run(req.query)
        log_transaction("/ask", req.dict(), result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-image")
def ask_image(req: QueryRequest):
    try:
        # Multimodal text-to-image/text query
        context = image_rag.get_text_answer(req.query)
        # Using simple LLM for result synthesis (or could use AdvancedRAG)
        response = adv_rag.llm.generate_response(
            "Synthesize an answer using the provided multimodal context.",
            f"Context from images:\n{context}\n\nQuestion: {req.query}"
        )
        result = {"answer": response, "context": context}
        log_transaction("/ask-image", req.dict(), result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-sql")
def ask_sql(req: QueryRequest):
    try:
        result = sql_pipe.run(req.query)
        log_transaction("/ask-sql", req.dict(), result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # To run: python -m src.deployment.app
    uvicorn.run(app, host="0.0.0.0", port=8000)
