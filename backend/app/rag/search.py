from backend.app.rag.embeddings import create_embeddings
from backend.app.rag.vector_store import search_documents


def search(query: str, top_k: int = 3):
    """
    Search the vector database using semantic similarity.
    """

    query_embedding = create_embeddings([query])[0]

    results = search_documents(
        query_embedding,
        top_k=top_k
    )

    return results


if __name__ == "__main__":
    query = "What AI project did the candidate develop?"

    results = search(query)

    print("\nQUERY:")
    print(query)

    print("\nRELEVANT DOCUMENTS:\n")

    for i, document in enumerate(results["documents"][0], start=1):
        print(f"--- Result {i} ---")
        print(document)
        print()