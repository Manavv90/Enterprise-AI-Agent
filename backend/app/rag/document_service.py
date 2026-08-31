from pathlib import Path

from backend.app.rag.document_loader import load_pdf
from backend.app.rag.text_splitter import split_text
from backend.app.rag.embeddings import create_embeddings
from backend.app.rag.vector_store import add_documents


DOCUMENTS_DIR = Path("data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


def process_document(file_path: str, source: str) -> int:
    """
    Process a PDF and store its chunks in ChromaDB.
    """

    # 1. Extract text
    text = load_pdf(file_path)

    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")

    # 2. Split into chunks
    chunks = split_text(text)

    if not chunks:
        raise ValueError("No chunks were created from the document.")

    # 3. Create embeddings
    embeddings = create_embeddings(chunks)

    # 4. Store in ChromaDB
    add_documents(
        chunks,
        embeddings,
        source
    )

    return len(chunks)