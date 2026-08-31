# Enterprise AI Agent

An AI-powered enterprise knowledge assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions from uploaded documents. The system combines **FastAPI, ChromaDB, Sentence Transformers, and a local Llama 3 LLM through Ollama** to provide grounded, source-aware responses.

## 🚀 Features

* 📄 Upload and process PDF documents
* ✂️ Automatically split documents into chunks
* 🧠 Generate semantic embeddings using Sentence Transformers
* 🔎 Perform semantic search using ChromaDB
* 🤖 Generate answers using local Llama 3 through Ollama
* 📚 Return document sources with answers
* 🎯 Similarity threshold to reduce irrelevant responses
* 🔐 Prevent duplicate document uploads
* 📋 List uploaded documents and chunk counts
* 🗑️ Delete documents and their stored embeddings
* 🌐 REST API built with FastAPI
* 📖 Interactive Swagger API documentation

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      User Query     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI /chat     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Sentence Transformer│
                    │     Embeddings      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │   Vector Search     │
                    └──────────┬──────────┘
                               │
                     Relevant Chunks
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Similarity Check  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Llama 3 / Ollama  │
                    │     Local LLM       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Sources    │
                    └─────────────────────┘
```

## 🛠️ Tech Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| FastAPI               | Backend REST API          |
| Sentence Transformers | Text embeddings           |
| ChromaDB              | Vector database           |
| Ollama                | Local LLM runtime         |
| Llama 3               | Answer generation         |
| PyPDF                 | PDF text extraction       |
| Pydantic              | Request validation        |
| Uvicorn               | ASGI server               |
| Git/GitHub            | Version control           |

## 📁 Project Structure

```text
Enterprise-AI-Agent/
│
├── backend/
│   └── app/
│       ├── core/
│       │   └── config.py
│       │
│       ├── rag/
│       │   ├── document_loader.py
│       │   ├── document_service.py
│       │   ├── embeddings.py
│       │   ├── rag_pipeline.py
│       │   ├── search.py
│       │   ├── text_splitter.py
│       │   └── vector_store.py
│       │
│       ├── services/
│       │   └── llm_service.py
│       │
│       └── main.py
│
├── data/
│   └── documents/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Manavv90/Enterprise-AI-Agent.git
cd Enterprise-AI-Agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama and download the Llama 3 model:

```bash
ollama pull llama3:8b
```

Verify:

```bash
ollama list
```

### 5. Start the API

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 📡 API Endpoints

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| GET    | `/`                     | API status               |
| GET    | `/health`               | Health check             |
| GET    | `/documents`            | List stored documents    |
| POST   | `/chat`                 | Ask questions using RAG  |
| POST   | `/documents/upload`     | Upload and process a PDF |
| DELETE | `/documents/{filename}` | Delete a document        |

## 💬 Example

Upload a document and ask:

```json
{
  "message": "What position is mentioned?"
}
```

Example response:

```json
{
  "response": "The position mentioned is \"System Engineer\".",
  "sources": [
    "Graduate Engineer Trainee (GET) Graduate Trainee - HCLTech.pdf"
  ]
}
```

If the information cannot be found:

```json
{
  "response": "I could not find this information in the provided documents.",
  "sources": []
}
```

## 🎯 RAG Pipeline

The system follows these steps:

1. Upload a PDF
2. Extract text from the document
3. Split the text into smaller chunks
4. Generate embeddings for each chunk
5. Store embeddings in ChromaDB
6. Convert the user's question into an embedding
7. Retrieve the most relevant chunks
8. Apply a similarity threshold
9. Provide relevant context to Llama 3
10. Generate a grounded response with document sources

## 🔒 Data & Security

Local documents, ChromaDB data, environment files, and virtual environments are excluded from Git using `.gitignore`.

Sensitive API keys should be stored in `.env` and never committed to the repository.

## 📌 Future Improvements

* Conversation memory
* Multi-turn chat
* Task management
* User authentication
* Improved retrieval and reranking
* Frontend dashboard
* Automated testing
* Production deployment
* Monitoring and logging

## 👨‍💻 Author

**Manav Saini**

Computer Science & Engineering Graduate

GitHub: https://github.com/Manavv90
