# Enterprise AI Agent

An AI-powered enterprise knowledge assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions from uploaded documents.

The system combines **FastAPI, ChromaDB, Sentence Transformers, Ollama, and Llama 3** to provide grounded, source-aware responses through a lightweight web interface.

---

## 🚀 Features

### AI & RAG

- 📄 Upload and process PDF documents
- ✂️ Automatically split documents into chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- 🔎 Perform semantic search using ChromaDB
- 🎯 Similarity threshold to reduce irrelevant retrieval
- 🤖 Generate answers using local Llama 3 through Ollama
- 📚 Return document sources with answers
- 🧩 Support document-specific queries

### Document Management

- 📋 List uploaded documents
- 📊 Display document chunk counts
- 🔐 Prevent duplicate document uploads
- 🗑️ Delete documents and their stored embeddings

### Frontend

- 💬 Interactive AI chat interface
- 📤 PDF upload interface
- 📚 Document sidebar
- 📄 Source references in AI responses
- 🔄 New chat functionality
- ⚡ Real-time communication with FastAPI
- 📱 Responsive web layout

### Backend

- 🌐 REST API using FastAPI
- 🔒 CORS configuration for frontend communication
- ❤️ Health check endpoint
- 📖 Interactive Swagger API documentation

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      Web UI         │
                         │  HTML/CSS/JavaScript │
                         └──────────┬──────────┘
                                    │
                         Upload / Query
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │      REST API       │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
        ┌─────────────────────┐             ┌─────────────────────┐
        │ Document Processing │             │    User Question    │
        └──────────┬──────────┘             └──────────┬──────────┘
                   │                                   │
                   ▼                                   ▼
        ┌─────────────────────┐             ┌─────────────────────┐
        │    Text Chunking    │             │ Query Embedding     │
        └──────────┬──────────┘             └──────────┬──────────┘
                   │                                   │
                   ▼                                   ▼
        ┌─────────────────────┐             ┌─────────────────────┐
        │ Sentence           │             │ Semantic Search     │
        │ Transformer        │             │                     │
        └──────────┬──────────┘             └──────────┬──────────┘
                   │                                   │
                   ▼                                   ▼
              ┌─────────────────────────────────────────────┐
              │                  ChromaDB                   │
              │              Vector Database                │
              └──────────────────────┬──────────────────────┘
                                     │
                              Relevant Context
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │  Similarity Check   │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    Llama 3 /        │
                           │      Ollama         │
                           │      Local LLM      │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │  Answer + Sources   │
                           └─────────────────────┘