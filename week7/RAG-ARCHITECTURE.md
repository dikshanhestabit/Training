# RAG Architecture

## Overview
This system implements a Retrieval-Augmented Generation (RAG) architecture designed to handle enterprise-scale knowledge retrieval. It follows a modular design consisting of an Ingestion Pipeline, a Vector Store, and a Query Engine.

## Components

### 1. Ingestion Pipeline (`src/pipelines/ingest.py`)
- **Document Loading**: Supports Markdown, Text, and **PDF files** (using pypdf).
- **Cleaning**: Periodic removal of redundant whitespaces and formatting artifacts.
- **Recursive Chunking**: Splits documents by paragraphs to balance context retention and retrieval precision.
- **Metadata Tagging**: Each chunk is tagged with its source file name and content for retrieval display.

### 2. Embedding Module (`src/embeddings/embedder.py`)
- **Provider**: Local (Path A) using `SentenceTransformer`.
- **Model**: `all-MiniLM-L6-v2`.
- **Dimensions**: Converts text chunks into 384-dimensional dense vectors.
- **Offline Performance**: Handles all vector calculations on the CPU without requiring API keys.

### 3. Vector Store (`src/vectorstore/manager.py`)
- **Engine**: FAISS (Facebook AI Similarity Search).
- **Index Type**: `IndexFlatL2` for exact similarity search.
- **Persistence**: Both the vector index (`.faiss`) and chunk metadata (`.pkl`) are stored locally for fast retrieval.

### 4. Retriever & Query Engine (`src/retriever/query_engine.py`)
- **Semantic Search**: Maps natural language queries to the local embedding space.
- **Top-K Retrieval**: Returns the top relevant context chunks with their content preview.
