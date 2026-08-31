from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.app.rag.document_service import process_document
from backend.app.rag.rag_pipeline import answer_question
from backend.app.rag.vector_store import (
    list_documents,
    delete_document,
    document_exists
)

app = FastAPI(
    title="Enterprise AI Agent",
    description="AI-powered enterprise knowledge and task assistant",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str
    source: str | None = None


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Agent API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
@app.get("/documents")
def get_documents():
    """
    Return all documents currently stored in ChromaDB.
    """

    return {
        "documents": list_documents()
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = answer_question(
        query=request.message,
        source=request.source
    )

    return result


@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF document.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    if document_exists(file.filename):
        raise HTTPException(
            status_code=409,
            detail="Document already exists."
        )

    file_path = Path("data/documents") / Path(file.filename).name
    file_path = Path("data/documents") / Path(file.filename).name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks_count = process_document(
            str(file_path),
            file.filename
        )

        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename,
            "chunks": chunks_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        file.file.close()


@app.delete("/documents/{filename}")
def remove_document(filename: str):
    """
    Delete all chunks belonging to a document.
    """

    deleted_chunks = delete_document(filename)

    if deleted_chunks == 0:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document deleted successfully",
        "filename": filename,
        "deleted_chunks": deleted_chunks
    }