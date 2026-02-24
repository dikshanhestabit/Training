# Deployment & Execution Notes

## System Architecture
This system is an Advanced RAG implementation featuring:
- **Conversational Memory**: Maintains a context window of the last 5 messages.
- **Evaluation Layer**: Uses LLM-as-a-judge to detect hallucinations and score faithfulness.
- **Refinement Loop**: Automatically regenerates answers if the first attempt fails the evaluation criteria.
- **Multi-modal Support**: Integrated text, image, and SQL query pipelines.

## API Endpoints

### 1. `/ask` (Advanced RAG)
- **Method**: POST
- **Payload**: `{"query": "string"}`
- **Features**: Memory + Refinement + Evaluation metrics.

### 2. `/ask-image` (Multimodal RAG)
- **Method**: POST
- **Payload**: `{"query": "string"}`
- **Features**: Retrieves image-based context and synthesizes a natural language answer.

### 3. `/ask-sql` (SQL Pipeline)
- **Method**: POST
- **Payload**: `{"query": "string"}`
- **Features**: Generates SQL, validates schema, and executes against `customers.db`.

## Execution Steps

### Prerequisites
Ensure all requirements from `requirements.txt` are installed:
```bash
pip install -r requirements.txt
```

### Running the API
Start the FastAPI server using Uvicorn:
```bash
python -m src.deployment.app
```
The API will be available at `http://localhost:8000`.

### Testing with CURL

**1. SQL Query (Verified against customers.db):**
```bash
curl -X POST http://localhost:8000/ask-sql -H "Content-Type: application/json" -d '{"query": "Show me the names of the first 5 customers in the database"}'
```

**2. Image Query (Verified against growth/pie charts):**
```bash
curl -X POST http://localhost:8000/ask-image -H "Content-Type: application/json" -d '{"query": "What kind of growth charts are available in the data?"}'
```

*(Note: For /ask results, ensure you run `python -m src.pipelines.ingest` first to populate the vector store index).*

## Logging & Traces
All interactions are logged in `CHAT-LOGS.json` at the root directory. Each log entry includes:
- Request/Response data
- Hallucination detection flags
- Faithfulness scores
- LLM confidence levels
