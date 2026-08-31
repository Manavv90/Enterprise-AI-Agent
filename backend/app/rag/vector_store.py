import chromadb


CHROMA_PATH = "data/chroma"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="enterprise_documents"
)


def add_documents(
    documents: list[str],
    embeddings: list[list[float]],
    source: str
) -> None:
    """
    Store document chunks, embeddings, and source metadata.
    """

    ids = [
        f"{source}_{index}"
        for index in range(len(documents))
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=[
            {"source": source}
            for _ in documents
        ]
    )


def search_documents(
    query_embedding: list[float],
    top_k: int = 3,
    source: str | None = None
) -> dict:
    """
    Search for relevant document chunks.

    If source is provided, search only that document.
    """

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }

    if source:
        query_args["where"] = {"source": source}

    return collection.query(**query_args)
def list_documents() -> list[dict]:
    """
    Return all unique documents stored in ChromaDB.
    """

    results = collection.get(include=["metadatas"])

    documents = {}

    for metadata in results["metadatas"]:
        source = metadata.get("source", "Unknown")

        if source not in documents:
            documents[source] = 0

        documents[source] += 1

    return [
        {
            "name": name,
            "chunks": chunks
        }
        for name, chunks in documents.items()
    ]
def delete_document(source: str) -> int:
    """
    Delete all chunks belonging to a document.

    Returns the number of deleted chunks.
    """

    results = collection.get(
        where={"source": source},
        include=["metadatas"]
    )

    ids = results["ids"]

    if not ids:
        return 0

    collection.delete(ids=ids)

    return len(ids)
def document_exists(source: str) -> bool:
    """
    Check whether a document already exists in ChromaDB.
    """

    results = collection.get(
        where={"source": source},
        include=["metadatas"]
    )

    return len(results["ids"]) > 0